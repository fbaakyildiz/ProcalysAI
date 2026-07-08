# Benchmarks

Benchmark utilities for evaluating BrahmsAI recommendations against curated ground-truth cases.

## Files

- `benchmark_cases.py` contains the benchmark case set and expected recommendations.
- `benchmark_runner.py` runs the full FastAPI pipeline against all benchmark cases.
- `openrouter_test.py` runs a smaller OpenRouter-only sample.
- `benchmark_results.json` stores the latest benchmark output.

## Run Full Pipeline Benchmark

Start the app first:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Then run:

```bash
python benchmarks/benchmark_runner.py
```

The runner writes results to:

```text
benchmarks/benchmark_results.json
```

## Run OpenRouter Sample

```bash
export OPENROUTER_API_KEY="your-key"
python benchmarks/openrouter_test.py
```

Do not commit real API keys.
