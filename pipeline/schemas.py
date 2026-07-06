from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum


class ClinicalSetting(str, Enum):
    LRTI   = "lrti"
    SEPSIS = "sepsis"
    POSTOP = "postop"
    ED     = "ed"


class PCTMeasurement(BaseModel):
    value: float
    day: int
    date: Optional[str] = None


class PatientInput(BaseModel):
    pct_value: float
    clinical_setting: ClinicalSetting
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    systolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    gcs_score: Optional[int] = None
    spo2: Optional[float] = None
    crp: Optional[float] = None
    wbc: Optional[float] = None
    lactate: Optional[float] = None
    creatinine: Optional[float] = None
    bilirubin: Optional[float] = None
    platelets: Optional[int] = None
    clinical_unstable: bool = False
    high_risk_patient: bool = False
    symptom_onset_hours: Optional[int] = None
    on_antibiotics: bool = False
    antibiotic_day: Optional[int] = None
    renal_failure: bool = False
    recent_surgery: bool = False
    burns_trauma: bool = False
    immunosuppressed: bool = False
    cardiac_failure: bool = False
    previous_pct: Optional[List[PCTMeasurement]] = None
    clinical_notes: Optional[str] = None

    @field_validator('clinical_notes')
    @classmethod
    def sanitize_clinical_notes(cls, v):
        if v is None:
            return v
        import re
        banned_patterns = [
            r'ignore\s+(all\s+)?previous\s+instructions',
            r'you\s+are\s+now\s+a',
            r'new\s+instruction[s]?',
            r'system\s+prompt',
            r'disregard\s+(all\s+)?',
            r'\[INST\]',
            r'###\s*instruction',
            r'</?(system|prompt|instruction)\s*>',
            r'override\s+(all\s+)?',
        ]
        for pattern in banned_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(
                    "Clinical notes contain invalid content. "
                    "Please enter only clinical observations."
                )
        if len(v) > 2000:
            raise ValueError("Clinical notes must be under 2000 characters.")
        return v


class AgentOutput(BaseModel):
    agent_name: str
    reasoning: str
    output: dict
    warnings: List[str] = []
    needs_clinician: bool = False


class StewardshipReport(BaseModel):
    patient_summary: str
    pct_interpretation: str
    recommendation: str
    recommendation_strength: str
    rationale: str
    kinetic_analysis: Optional[str] = None
    warnings: List[str] = []
    override_flags: List[str] = []
    next_steps: List[str] = []
    gray_zone: bool = False
    clinician_review_required: bool = False
    disclaimer: str = (
        "This system is for research purposes only. "
        "Clinical decisions remain the sole responsibility of the treating clinician."
    )
    agents: List[AgentOutput] = []
    pipeline_metadata: Optional[List[dict]] = []
    total_tokens_est: Optional[int] = None
    total_cost_usd_est: Optional[float] = None
    total_latency_seconds: Optional[float] = None
