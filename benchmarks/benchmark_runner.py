import json
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import requests

from benchmark_cases import BENCHMARK_CASES, GROUND_TRUTH

API_URL    = "http://localhost:8000/api/analyze"
HEALTH_URL = "http://localhost:8000/health"
WAIT_BETWEEN = 12  # seconds between cases (rate limiter)
RESULTS_PATH = Path(__file__).with_name("benchmark_results.json")


def check_server():
    try:
        r = requests.get(HEALTH_URL, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def run_case(case):
    try:
        r = requests.post(API_URL, json=case["input"], timeout=120)
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except requests.exceptions.Timeout:
        return None, "Request timed out after 120s"
    except Exception as e:
        return None, str(e)


def main():
    print("=" * 70)
    print("PCT STEWARDSHIP BENCHMARK")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    if not check_server():
        print("\nERROR: Server not running at http://localhost:8000")
        print("Start with:")
        print("  export GEMINI_API_KEY=...")
        print("  uvicorn main:app --host 127.0.0.1 --port 8000")
        sys.exit(1)

    print(f"\nServer healthy. Running {len(BENCHMARK_CASES)} benchmark cases...")
    print(f"Delay between cases: {WAIT_BETWEEN}s  |  Timeout per case: 120s\n")

    results = []
    start_time = time.time()

    for i, case in enumerate(BENCHMARK_CASES, 1):
        case_id   = case["id"]
        category  = case["category"]
        gt        = case["ground_truth"]
        gt_str    = case["ground_truth_strength"]
        pct_value = case["input"]["pct_value"]

        response, error = run_case(case)

        if error or response is None:
            rec            = "ERROR"
            llm_strength   = "ERROR"
            match          = False
            strength_match = False
            gray_zone      = None
            clinician_rev  = None
            warnings_count = 0
            total_tokens   = None
            total_cost     = None
            total_latency  = None
            print(
                f"Case {i:2d}/25: ID={case_id:2d} category={category:<30s} "
                f"GT={gt:<20s} LLM=ERROR   MATCH=False  |  ERROR: {error}"
            )
        else:
            rec            = response.get("recommendation", "unknown")
            llm_strength   = response.get("recommendation_strength", "unknown")
            match          = (rec == gt)
            strength_match = (llm_strength == gt_str)
            gray_zone      = response.get("gray_zone", False)
            clinician_rev  = response.get("clinician_review_required", False)
            warnings_count = len(response.get("warnings", []))
            total_tokens   = response.get("total_tokens_est")
            total_cost     = response.get("total_cost_usd_est")
            total_latency  = response.get("total_latency_seconds")
            print(
                f"Case {i:2d}/25: ID={case_id:2d} category={category:<30s} "
                f"GT={gt:<20s} LLM={rec:<20s} MATCH={'True ' if match else 'False'}"
            )

        results.append({
            "case_id":                      case_id,
            "category":                     category,
            "pct_value":                    pct_value,
            "ground_truth":                 gt,
            "ground_truth_strength":        gt_str,
            "llm_recommendation":           rec,
            "llm_strength":                 llm_strength,
            "match":                        match,
            "recommendation_strength_match": strength_match,
            "gray_zone_flagged":            gray_zone,
            "clinician_review_required":    clinician_rev,
            "warnings_count":               warnings_count,
            "total_tokens_est":             total_tokens,
            "total_cost_usd_est":           total_cost,
            "total_latency_seconds":        total_latency,
            "error":                        error,
        })

        if i < len(BENCHMARK_CASES):
            time.sleep(WAIT_BETWEEN)

    total_elapsed = round(time.time() - start_time, 1)

    # ── Save full results ──────────────────────────────────────────────────
    output = {
        "run_timestamp": datetime.now().isoformat(),
        "total_cases":   len(BENCHMARK_CASES),
        "results":       results,
    }
    with RESULTS_PATH.open("w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved -> {RESULTS_PATH}")

    # ── Summary ────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)

    correct = sum(1 for r in results if r["match"])
    print(f"\nOverall accuracy: {correct}/{len(results)} correct  ({100 * correct / len(results):.1f}%)")

    cat_stats: dict = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        cat_stats[r["category"]]["total"] += 1
        if r["match"]:
            cat_stats[r["category"]]["correct"] += 1

    print("\nAccuracy by category:")
    for cat in sorted(cat_stats):
        s   = cat_stats[cat]
        pct = 100 * s["correct"] / s["total"]
        bar = "#" * s["correct"] + "." * (s["total"] - s["correct"])
        print(f"  {cat:<35s}  {s['correct']}/{s['total']} ({pct:.0f}%)  [{bar}]")

    tokens_list  = [r["total_tokens_est"]    for r in results if r["total_tokens_est"]    is not None]
    cost_list    = [r["total_cost_usd_est"]   for r in results if r["total_cost_usd_est"]   is not None]

    print(f"\nTotal tokens used (est):     {sum(tokens_list):,}")
    print(f"Total estimated cost (USD):  ${sum(cost_list):.4f}")
    print(f"Total time elapsed:          {total_elapsed}s  ({total_elapsed / 60:.1f} min)")

    failures = [r for r in results if not r["match"]]
    if failures:
        print(f"\nFailed cases ({len(failures)}):")
        for r in failures:
            print(
                f"  ID={r['case_id']:2d}  {r['category']:<35s} "
                f"GT={r['ground_truth']:<20s} LLM={r['llm_recommendation']}"
            )
    else:
        print("\n✓ All 25 cases matched ground truth!")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
