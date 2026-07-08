import asyncio
import json
import logging
import os
import time
import urllib.error
import urllib.request
from datetime import datetime

from google import genai as google_genai
from google.genai import types as genai_types

from .rate_limiter import limiter
from .schemas import PatientInput, StewardshipReport, AgentOutput
from .prompts import PROMPTS

logger = logging.getLogger(__name__)

_client = None

PROVIDER_CONFIGS = {
    "gemini": {
        "display": "Google AI Studio",
        "model": "gemini-2.5-flash",
        "input_cost_per_million": 0.075,
        "output_cost_per_million": 0.30,
    },
    "openai": {
        "display": "OpenAI / ChatGPT",
        "model": "gpt-4o-mini",
        "input_cost_per_million": 0.15,
        "output_cost_per_million": 0.60,
    },
    "anthropic": {
        "display": "Anthropic / Claude",
        "model": "claude-3-5-haiku-latest",
        "input_cost_per_million": 0.80,
        "output_cost_per_million": 4.00,
    },
    "openrouter": {
        "display": "OpenRouter",
        "model": "meta-llama/llama-4-scout:free",
        "input_cost_per_million": 0.0,
        "output_cost_per_million": 0.0,
    },
}

VALID_RECOMMENDATIONS = {
    "start", "withhold", "stop",
    "monitor", "escalate", "clinician_decision"
}


def get_client(api_key: str | None = None):
    if api_key:
        return google_genai.Client(api_key=api_key)

    global _client
    if _client is None:
        env_key = os.environ.get("GEMINI_API_KEY")
        if not env_key:
            raise ValueError("Google AI Studio API key is required")
        _client = google_genai.Client(api_key=env_key)
    return _client


def detect_provider(api_key: str | None = None) -> str:
    key = (api_key or "").strip()
    if key.startswith("AIza"):
        return "gemini"
    if key.startswith("sk-or-"):
        return "openrouter"
    if key.startswith("sk-ant-"):
        return "anthropic"
    if key.startswith("sk-"):
        return "openai"
    if not key and os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    raise ValueError("Unsupported API key format. Use Gemini, OpenAI, Claude, or OpenRouter.")


def _post_json(url: str, headers: dict, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500]
        raise ValueError(f"Provider request failed with HTTP {e.code}: {detail}")


async def _call_gemini_internal(system_prompt: str, user_prompt: str, api_key: str | None = None) -> str:
    client = get_client(api_key)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.models.generate_content(
            model=PROVIDER_CONFIGS["gemini"]["model"],
            contents=user_prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1,
                response_mime_type="application/json",
            ),
        ),
    )
    return response.text


async def _call_openai_internal(system_prompt: str, user_prompt: str, api_key: str, provider: str) -> str:
    config = PROVIDER_CONFIGS[provider]
    url = (
        "https://openrouter.ai/api/v1/chat/completions"
        if provider == "openrouter"
        else "https://api.openai.com/v1/chat/completions"
    )
    payload = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    if provider == "openrouter":
        headers.update({
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "BrahmsAI",
        })
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: _post_json(url, headers, payload))
    return data["choices"][0]["message"]["content"]


async def _call_anthropic_internal(system_prompt: str, user_prompt: str, api_key: str) -> str:
    payload = {
        "model": PROVIDER_CONFIGS["anthropic"]["model"],
        "max_tokens": 4096,
        "temperature": 0.1,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
        None,
        lambda: _post_json("https://api.anthropic.com/v1/messages", headers, payload),
    )
    text_blocks = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
    return "\n".join(text_blocks).strip()


async def _call_model_internal(system_prompt: str, user_prompt: str, api_key: str | None = None) -> tuple[str, str]:
    provider = detect_provider(api_key)
    key = api_key.strip() if api_key else None
    if provider == "gemini":
        return await _call_gemini_internal(system_prompt, user_prompt, key), provider
    if not key:
        raise ValueError("API key is required")
    if provider in {"openai", "openrouter"}:
        return await _call_openai_internal(system_prompt, user_prompt, key, provider), provider
    if provider == "anthropic":
        return await _call_anthropic_internal(system_prompt, user_prompt, key), provider
    raise ValueError("Unsupported API provider")


async def call_model(system_prompt: str, user_prompt: str,
                     agent_name: str = "unknown",
                     api_key: str | None = None) -> tuple[str, dict]:
    """
    Returns (raw_text, metadata) where metadata contains:
    token counts, latency, cost estimation
    """
    await limiter.wait()

    start_time = time.time()

    try:
        raw, provider = await asyncio.wait_for(
            _call_model_internal(system_prompt, user_prompt, api_key),
            timeout=45.0  # 45 second timeout per agent
        )
    except asyncio.TimeoutError:
        logger.error(f"{agent_name}: Timeout after 45s")
        raise ValueError(f"Agent {agent_name} timed out after 45 seconds")

    latency = round(time.time() - start_time, 2)

    # Validate JSON
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(f"{agent_name}: Non-JSON response, retrying...")
        await limiter.wait()
        try:
            raw = await asyncio.wait_for(
                _call_model_internal(
                    system_prompt,
                    user_prompt + "\n\nCRITICAL: Respond with ONLY valid JSON. No markdown, no code fences.",
                    api_key,
                ),
                timeout=45.0
            )
            if isinstance(raw, tuple):
                raw, provider = raw
            parsed = json.loads(raw)
        except (asyncio.TimeoutError, json.JSONDecodeError) as e:
            logger.error(f"{agent_name}: Retry failed — {e}")
            raise ValueError(f"Agent {agent_name} failed to produce valid JSON after retry")

    # Output validation — check for injection in LLM output
    if "injection_detected" in str(parsed.get("error", "")):
        logger.warning(f"{agent_name}: Injection detected by LLM")
        raise ValueError(f"Agent {agent_name} detected potential prompt injection in input data")

    # Validate recommendation field if A4
    if agent_name == "A4_Report":
        rec = parsed.get("recommendation", "")
        if rec not in VALID_RECOMMENDATIONS:
            logger.warning(f"{agent_name}: Invalid recommendation '{rec}' — defaulting to clinician_decision")
            parsed["recommendation"] = "clinician_decision"
            parsed["clinician_review_required"] = True
            raw = json.dumps(parsed)

    # Estimate token counts (approximate — Gemini doesn't always return usage)
    # Rough estimate: 1 token ≈ 4 characters
    input_tokens = len(system_prompt + user_prompt) // 4
    output_tokens = len(raw) // 4

    config = PROVIDER_CONFIGS[provider]
    input_cost = (input_tokens / 1_000_000) * config["input_cost_per_million"]
    output_cost = (output_tokens / 1_000_000) * config["output_cost_per_million"]

    metadata = {
        "agent": agent_name,
        "latency_seconds": latency,
        "input_tokens_est": input_tokens,
        "output_tokens_est": output_tokens,
        "total_tokens_est": input_tokens + output_tokens,
        "cost_usd_est": round(input_cost + output_cost, 6),
        "provider": config["display"],
        "model": config["model"],
    }

    return raw, metadata


def _dedupe(items: list) -> list:
    result = []
    seen = set()
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


async def validate_api_key(api_key: str) -> dict:
    if not api_key or not api_key.strip():
        raise ValueError("API key is required")
    provider = detect_provider(api_key)
    config = PROVIDER_CONFIGS[provider]
    try:
        raw, _ = await asyncio.wait_for(
            _call_model_internal(
                "Respond only with valid JSON.",
                "Return exactly this JSON object: {\"ok\": true}",
                api_key.strip(),
            ),
            timeout=25.0,
        )
        json.loads(raw)
    except asyncio.TimeoutError:
        raise ValueError("API key validation timed out")
    except Exception as e:
        logger.warning("%s API key validation failed: %s", config["display"], type(e).__name__)
        raise ValueError(f"{config['display']} API key is invalid or unavailable")
    return {"provider": provider, "provider_label": config["display"], "model": config["model"]}


async def validate_gemini_api_key(api_key: str) -> None:
    await validate_api_key(api_key)


async def run_pipeline(patient: PatientInput, api_key: str | None = None) -> StewardshipReport:
    api_key = api_key.strip() if api_key else None
    patient_json = patient.model_dump_json(indent=2)
    all_metadata = []

    # A1 — Intake & Validation
    logger.info("Running A1: Intake & Validation")
    a1_raw, a1_meta = await call_model(
        PROMPTS["A1_SYSTEM"],
        PROMPTS["A1_USER"].format(patient_json=patient_json),
        agent_name="A1_Intake",
        api_key=api_key,
    )
    all_metadata.append(a1_meta)
    a1_data = json.loads(a1_raw)
    a1_out = AgentOutput(
        agent_name="A1_Intake",
        reasoning=a1_data.get("reasoning", ""),
        output=a1_data,
        warnings=a1_data.get("warnings", []),
        needs_clinician=a1_data.get("needs_clinician", False),
    )

    # A2 — Clinical Reasoning
    logger.info("Running A2: Clinical Reasoning")
    a2_raw, a2_meta = await call_model(
        PROMPTS["A2_SYSTEM"],
        PROMPTS["A2_USER"].format(patient_json=patient_json, a1_output=a1_raw),
        agent_name="A2_Clinical",
        api_key=api_key,
    )
    all_metadata.append(a2_meta)
    a2_data = json.loads(a2_raw)
    a2_out = AgentOutput(
        agent_name="A2_Clinical",
        reasoning=a2_data.get("reasoning", ""),
        output=a2_data,
        warnings=a2_data.get("warnings", []),
        needs_clinician=a2_data.get("needs_clinician", False),
    )

    # A3 — Kinetic Analysis & Context
    logger.info("Running A3: Kinetic Analysis")
    a3_raw, a3_meta = await call_model(
        PROMPTS["A3_SYSTEM"],
        PROMPTS["A3_USER"].format(patient_json=patient_json, a2_output=a2_raw),
        agent_name="A3_Kinetic",
        api_key=api_key,
    )
    all_metadata.append(a3_meta)
    a3_data = json.loads(a3_raw)
    a3_out = AgentOutput(
        agent_name="A3_Kinetic",
        reasoning=a3_data.get("reasoning", ""),
        output=a3_data,
        warnings=a3_data.get("warnings", []),
        needs_clinician=a3_data.get("needs_clinician", False),
    )

    # A4 — Final Report
    logger.info("Running A4: Final Report")
    a4_raw, a4_meta = await call_model(
        PROMPTS["A4_SYSTEM"],
        PROMPTS["A4_USER"].format(
            patient_json=patient_json,
            a1_output=a1_raw,
            a2_output=a2_raw,
            a3_output=a3_raw,
        ),
        agent_name="A4_Report",
        api_key=api_key,
    )
    all_metadata.append(a4_meta)
    a4_data = json.loads(a4_raw)
    a4_out = AgentOutput(
        agent_name="A4_Report",
        reasoning=a4_data.get("reasoning", ""),
        output=a4_data,
        warnings=a4_data.get("warnings", []),
        needs_clinician=a4_data.get("needs_clinician", False),
    )

    # Consolidate warnings and override flags deterministically.
    all_warnings = _dedupe(
        a1_data.get("warnings", [])
        + a2_data.get("warnings", [])
        + a3_data.get("warnings", [])
        + a4_data.get("warnings", [])
    )
    all_override_flags = _dedupe(
        a2_data.get("override_flags", [])
        + a4_data.get("override_flags", [])
    )
    upstream_needs_clinician = any([
        a1_data.get("needs_clinician", False),
        a2_data.get("needs_clinician", False),
        a3_data.get("needs_clinician", False),
        a4_data.get("needs_clinician", False),
    ])
    gray_zone = any([
        a2_data.get("gray_zone", False),
        a4_data.get("gray_zone", False),
    ])
    day4_alert = a3_data.get("day4_alert", False)
    if day4_alert:
        all_warnings = _dedupe(
            all_warnings
            + ["Day 4 alert: PCT decline below 80% threshold; clinician review required."]
        )

    report = StewardshipReport(
        patient_summary=a4_data.get("patient_summary", ""),
        pct_interpretation=a4_data.get("pct_interpretation", ""),
        recommendation=a4_data.get("recommendation", "clinician_decision"),
        recommendation_strength=a4_data.get("recommendation_strength", "weak"),
        rationale=a4_data.get("rationale", ""),
        kinetic_analysis=a4_data.get("kinetic_analysis"),
        next_steps=a4_data.get("next_steps", []),
        warnings=all_warnings,
        override_flags=all_override_flags,
        gray_zone=gray_zone,
        clinician_review_required=bool(
            a4_data.get("clinician_review_required", False)
            or upstream_needs_clinician
            or gray_zone
            or all_override_flags
            or day4_alert
        ),
        agents=[a1_out, a2_out, a3_out, a4_out],
        pipeline_metadata=all_metadata,
        total_tokens_est=sum(m["total_tokens_est"] for m in all_metadata),
        total_cost_usd_est=round(sum(m["cost_usd_est"] for m in all_metadata), 6),
        total_latency_seconds=round(sum(m["latency_seconds"] for m in all_metadata), 2),
    )

    logger.info(json.dumps({
        "event": "pipeline_complete",
        "timestamp": datetime.utcnow().isoformat(),
        "pct_value": patient.pct_value,
        "clinical_setting": patient.clinical_setting.value,
        "recommendation": report.recommendation,
        "recommendation_strength": report.recommendation_strength,
        "gray_zone": report.gray_zone,
        "clinician_review_required": report.clinician_review_required,
        "override_triggered": any(report.override_flags),
        "warnings_count": len(report.warnings),
        "agents": [m for m in all_metadata],
        "pipeline_total_tokens_est": sum(m["total_tokens_est"] for m in all_metadata),
        "pipeline_total_cost_usd_est": round(sum(m["cost_usd_est"] for m in all_metadata), 6),
        "pipeline_total_latency_seconds": round(sum(m["latency_seconds"] for m in all_metadata), 2),
    }))

    return report
