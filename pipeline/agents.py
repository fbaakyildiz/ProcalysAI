import asyncio
import json
import logging
import os
import time
from datetime import datetime

from google import genai as google_genai
from google.genai import types as genai_types

from .rate_limiter import limiter
from .schemas import PatientInput, StewardshipReport, AgentOutput
from .prompts import PROMPTS

logger = logging.getLogger(__name__)

_client = None

VALID_RECOMMENDATIONS = {
    "start", "withhold", "stop",
    "monitor", "escalate", "clinician_decision"
}


def get_client():
    global _client
    if _client is None:
        _client = google_genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


async def _call_gemini_internal(system_prompt: str, user_prompt: str) -> str:
    """Internal Gemini call — extracted for timeout wrapping."""
    client = get_client()
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1,
                response_mime_type="application/json",
            ),
        ),
    )
    return response.text


async def call_gemini(system_prompt: str, user_prompt: str,
                      agent_name: str = "unknown") -> tuple[str, dict]:
    """
    Returns (raw_text, metadata) where metadata contains:
    token counts, latency, cost estimation
    """
    await limiter.wait()

    start_time = time.time()

    try:
        raw = await asyncio.wait_for(
            _call_gemini_internal(system_prompt, user_prompt),
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
                _call_gemini_internal(
                    system_prompt,
                    user_prompt + "\n\nCRITICAL: Respond with ONLY valid JSON. No markdown, no code fences."
                ),
                timeout=45.0
            )
            parsed = json.loads(raw)
        except (asyncio.TimeoutError, json.JSONDecodeError) as e:
            logger.error(f"{agent_name}: Retry failed — {e}")
            raise ValueError(f"Agent {agent_name} failed to produce valid JSON after retry")

    # Output validation — check for injection in LLM output
    if "injection_detected" in str(parsed.get("error", "")):
        logger.warning(f"{agent_name}: Injection detected by LLM")

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

    # Gemini 2.5 Flash pricing (paid tier for reference):
    # Input: $0.075 per 1M tokens, Output: $0.30 per 1M tokens
    input_cost  = (input_tokens  / 1_000_000) * 0.075
    output_cost = (output_tokens / 1_000_000) * 0.30

    metadata = {
        "agent": agent_name,
        "latency_seconds": latency,
        "input_tokens_est": input_tokens,
        "output_tokens_est": output_tokens,
        "total_tokens_est": input_tokens + output_tokens,
        "cost_usd_est": round(input_cost + output_cost, 6),
        "model": "gemini-2.5-flash",
    }

    return raw, metadata


async def run_pipeline(patient: PatientInput) -> StewardshipReport:
    patient_json = patient.model_dump_json(indent=2)
    all_metadata = []

    # A1 — Intake & Validation
    logger.info("Running A1: Intake & Validation")
    a1_raw, a1_meta = await call_gemini(
        PROMPTS["A1_SYSTEM"],
        PROMPTS["A1_USER"].format(patient_json=patient_json),
        agent_name="A1_Intake",
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
    a2_raw, a2_meta = await call_gemini(
        PROMPTS["A2_SYSTEM"],
        PROMPTS["A2_USER"].format(patient_json=patient_json, a1_output=a1_raw),
        agent_name="A2_Clinical",
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
    a3_raw, a3_meta = await call_gemini(
        PROMPTS["A3_SYSTEM"],
        PROMPTS["A3_USER"].format(patient_json=patient_json, a2_output=a2_raw),
        agent_name="A3_Kinetic",
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
    a4_raw, a4_meta = await call_gemini(
        PROMPTS["A4_SYSTEM"],
        PROMPTS["A4_USER"].format(
            patient_json=patient_json,
            a1_output=a1_raw,
            a2_output=a2_raw,
            a3_output=a3_raw,
        ),
        agent_name="A4_Report",
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

    # Consolidate warnings (deduplicated)
    all_warnings = []
    seen = set()
    for w in (
        a1_data.get("warnings", [])
        + a2_data.get("warnings", [])
        + a3_data.get("warnings", [])
        + a4_data.get("warnings", [])
    ):
        if w and w not in seen:
            seen.add(w)
            all_warnings.append(w)

    report = StewardshipReport(
        patient_summary=a4_data.get("patient_summary", ""),
        pct_interpretation=a4_data.get("pct_interpretation", ""),
        recommendation=a4_data.get("recommendation", "clinician_decision"),
        recommendation_strength=a4_data.get("recommendation_strength", "weak"),
        rationale=a4_data.get("rationale", ""),
        kinetic_analysis=a4_data.get("kinetic_analysis"),
        next_steps=a4_data.get("next_steps", []),
        warnings=all_warnings,
        override_flags=a4_data.get("override_flags", []),
        gray_zone=a4_data.get("gray_zone", False),
        clinician_review_required=a4_data.get("clinician_review_required", False),
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
