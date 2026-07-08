# BrahmsAI

[Back to Portfolio](https://fbaakyildiz.github.io/)

Clinical decision-support prototype for PCT-guided antibiotic stewardship using structured patient data, serial procalcitonin kinetics, and a hardened multi-agent LLM pipeline.

> Research use only. BrahmsAI is not a medical device and does not replace clinician judgment.

## Project Materials

| Resource | Link |
|---|---|
| Demo video | [Watch demo](https://www.youtube.com/watch?v=7yghCQTVTS8) |
| GitHub repository | [fbaakyildiz/BrahmsAI](https://github.com/fbaakyildiz/BrahmsAI) |
| Design document | [Open design document](docs/DESIGN.md) |
| Frontend source | [Open UI file](static/index.html) |
| Benchmark suite | [Open benchmarks](benchmarks/) |

## What The Project Does

- Interprets PCT thresholds for LRTI and sepsis workflows.
- Tracks serial PCT values and calculates treatment-response decline.
- Flags Day 4 treatment-failure risk when PCT decline is below the expected threshold.
- Applies clinical safety overrides for unstable or high-risk patients.
- Routes the case through four specialized agents: intake, clinical reasoning, kinetic context, and final report.
- Supports local use with Gemini, OpenAI, Claude, and OpenRouter API keys.
- Returns structured stewardship reports with rationale, warnings, review flags, and telemetry.

## Agent Pipeline

```text
Patient input
    ↓
A1 Intake and validation
    ↓
A2 PCT threshold reasoning
    ↓
A3 Kinetic and comorbidity context
    ↓
A4 Final stewardship report
```

## Why It Matters

Antibiotic stewardship decisions often require combining biomarker thresholds, clinical instability, patient risk, and serial response trends. BrahmsAI was built to test whether a structured multi-agent workflow can produce more transparent, auditable recommendations than a single general-purpose prompt.

The system emphasizes:

- structured JSON contracts
- prompt-injection protection
- deterministic safety flag preservation
- concise clinician-facing reports
- research-only local execution

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://localhost:8000
```

The app asks for a model API key in the browser before analysis starts. The key is kept in browser memory for the current session and passed only to the local FastAPI backend.

## Main Files

| Path | Purpose |
|---|---|
| `main.py` | FastAPI app and API endpoints |
| `pipeline/agents.py` | Provider routing and four-agent orchestration |
| `pipeline/prompts.py` | A1-A4 system and user prompts |
| `pipeline/schemas.py` | Pydantic request and response models |
| `static/index.html` | Single-file local UI |
| `docs/DESIGN.md` | Architecture and implementation notes |

## Academic Disclaimer

This project is a research prototype. It should not be used for real clinical decision-making without regulatory review, clinical validation, governance, and production-grade security controls.
