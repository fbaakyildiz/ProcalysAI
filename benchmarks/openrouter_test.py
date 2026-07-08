import json
import os
import time

import requests

from benchmark_cases import BENCHMARK_CASES, GROUND_TRUTH

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-4-scout:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SELECTED_IDS = [1, 5, 9, 14, 18, 21, 24]

SYSTEM = """You are a clinical decision support agent applying the B.R.A.H.M.S PCT algorithm.

LRTI thresholds:
- PCT < 0.10 ng/mL → withhold (strongly discouraged)
- PCT 0.10-0.25 → clinician_decision (gray zone)
- PCT 0.25-0.50 → clinician_decision (consider, clinical judgment)
- PCT > 0.50 → start (strongly encouraged)
- Discontinuation: PCT < 0.25 OR ≥80% decline from peak → stop

Sepsis thresholds:
- PCT < 0.5 → withhold (low risk)
- PCT 0.5-2.0 → clinician_decision (indeterminate)
- PCT > 2.0 → start (high risk)
- Discontinuation: PCT < 0.5 OR ≥80% decline → stop

Override rules (ignore PCT, always START if):
- clinical_unstable = True
- high_risk_patient = True

Kinetic: if on_antibiotics=True and previous_pct provided, calculate % decline from peak.
If ≥80% decline → stop. If Day 4+ and <80% decline → escalate (treatment failure).

Respond ONLY with valid JSON, no markdown:
{
  "recommendation": "start|withhold|stop|monitor|escalate|clinician_decision",
  "reasoning": "one sentence referencing exact PCT value and threshold",
  "pct_band": "which band the PCT falls into",
  "override_triggered": true or false,
  "gray_zone": true or false
}"""


def call_openrouter(case_input: dict) -> tuple[dict | None, str | None]:
    if not OPENROUTER_API_KEY:
        return None, "OPENROUTER_API_KEY environment variable is not set"

    user_prompt = f"Patient data: {json.dumps(case_input)}"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": user_prompt},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        data = r.json()
        raw = data["choices"][0]["message"]["content"]
        return json.loads(raw), None
    except requests.exceptions.Timeout:
        return None, "Request timed out after 60s"
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON in response: {e}"
    except Exception as e:
        return None, str(e)


def main():
    cases = [c for c in BENCHMARK_CASES if c["id"] in SELECTED_IDS]
    cases.sort(key=lambda c: SELECTED_IDS.index(c["id"]))

    print("=" * 70)
    print(f"OPENROUTER BENCHMARK  —  {MODEL}")
    print(f"Cases: {SELECTED_IDS}  (1 per category)")
    print("=" * 70)

    results = []

    for i, case in enumerate(cases, 1):
        case_id  = case["id"]
        category = case["category"]
        gt       = case["ground_truth"]

        response, error = call_openrouter(case["input"])

        if error or response is None:
            rec   = "ERROR"
            match = False
            reasoning  = error
            pct_band   = "—"
            override   = "—"
            gray_zone  = "—"
            tick = "✗"
            print(f"\nCase {i}/7  ID={case_id}  {category}")
            print(f"  GT={gt:<22s}  LLM=ERROR  {tick}")
            print(f"  Error: {error}")
        else:
            rec       = response.get("recommendation", "unknown")
            reasoning = response.get("reasoning", "")
            pct_band  = response.get("pct_band", "")
            override  = response.get("override_triggered", False)
            gray_zone = response.get("gray_zone", False)
            match     = (rec == gt)
            tick      = "✓" if match else "✗"
            print(f"\nCase {i}/7  ID={case_id}  {category}")
            print(f"  GT={gt:<22s}  LLM={rec:<22s}  {tick}")
            print(f"  Reasoning:  {reasoning}")
            print(f"  PCT band:   {pct_band}")
            print(f"  Override:   {override}  |  Gray zone: {gray_zone}")

        results.append({
            "case_id":   case_id,
            "category":  category,
            "gt":        gt,
            "llm":       rec,
            "match":     match,
            "reasoning": reasoning,
        })

        if i < len(cases):
            time.sleep(3)

    # ── Summary ────────────────────────────────────────────────────────────
    correct   = [r for r in results if r["match"]]
    incorrect = [r for r in results if not r["match"]]

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nAccuracy: {len(correct)}/7  ({100 * len(correct) / 7:.0f}%)")

    if correct:
        print(f"\nCorrect ({len(correct)}):")
        for r in correct:
            print(f"  ✓  ID={r['case_id']}  {r['category']}")

    if incorrect:
        print(f"\nFailed ({len(incorrect)}):")
        for r in incorrect:
            print(f"  ✗  ID={r['case_id']}  {r['category']:<35s}  GT={r['gt']:<22s}  LLM={r['llm']}")

    print()


if __name__ == "__main__":
    main()
