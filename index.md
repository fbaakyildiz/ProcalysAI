# ProcalysAI

[Back to Portfolio](https://fbaakyildiz.github.io/?skipIntro=1#projects)

Clinical decision-support prototype for PCT-guided antibiotic stewardship using structured patient data, serial procalcitonin kinetics, and a hardened multi-agent LLM pipeline.

> Research use only. ProcalysAI is not a medical device and does not replace clinician judgment.

## Project Materials

| Resource | Link |
|---|---|
| Demo video | [Watch demo](https://www.youtube.com/watch?v=7yghCQTVTS8) |
| GitHub repository | [fbaakyildiz/ProcalysAI](https://github.com/fbaakyildiz/ProcalysAI) |
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

Antibiotic stewardship decisions often require combining biomarker thresholds, clinical instability, patient risk, and serial response trends. ProcalysAI was built to test whether a structured multi-agent workflow can produce more transparent, auditable recommendations than a single general-purpose prompt.

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

## Academic Prototype Disclaimer

This project was developed by me as part of the Technical University of Munich course “Foundations and Applications of Generative AI.” It is an academic prototype for educational and research purposes only. It is not a medical device, clinical decision-support product, diagnostic tool, or commercial Thermo Fisher Scientific product. It must not be used for patient care, diagnosis, treatment decisions, or antibiotic prescribing.

The project was based on publicly available educational materials and course-provided background information. It is not endorsed, approved, validated, or sponsored by Thermo Fisher or BRAHMS GmbH.

Any references to third-party names, products, trademarks, or biomarkers are for descriptive academic context only. All trademarks remain the property of Thermo Fisher Scientific or its affiliates.

[Read the full disclaimer](DISCLAIMER.md)

## Academic Disclaimer

This project is a research prototype. It should not be used for real clinical decision-making without regulatory review, clinical validation, governance, and production-grade security controls.
