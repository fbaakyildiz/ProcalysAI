BENCHMARK_CASES = [

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 1 — Clear Withhold (PCT < 0.10, LRTI, no confounders)
    # Expected: withhold / strong
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "category": "Cat1_Clear_Withhold",
        "ground_truth": "withhold",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.06,
            "clinical_setting": "lrti",
            "temperature": 37.4,
            "respiratory_rate": 16,
            "systolic_bp": 128,
            "heart_rate": 72,
            "gcs_score": 15,
            "crp": 8.2,
            "wbc": 8.1,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "42-year-old female, mild cough 3 days, no fever. Outpatient. Chest X-ray clear."
        }
    },
    {
        "id": 2,
        "category": "Cat1_Clear_Withhold",
        "ground_truth": "withhold",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.08,
            "clinical_setting": "lrti",
            "temperature": 37.8,
            "respiratory_rate": 18,
            "systolic_bp": 122,
            "heart_rate": 80,
            "gcs_score": 15,
            "crp": 12.0,
            "wbc": 9.4,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "35-year-old male, AECOPD exacerbation. Mild wheeze, no consolidation on X-ray. FEV1 60%."
        }
    },
    {
        "id": 3,
        "category": "Cat1_Clear_Withhold",
        "ground_truth": "withhold",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.04,
            "clinical_setting": "lrti",
            "temperature": 37.2,
            "respiratory_rate": 14,
            "systolic_bp": 118,
            "heart_rate": 68,
            "gcs_score": 15,
            "crp": 5.1,
            "wbc": 7.2,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "28-year-old female, upper respiratory tract infection, sore throat, rhinorrhoea, 2 days. No systemic signs."
        }
    },

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 2 — Clear Start (PCT > threshold or override)
    # Expected: start / strong
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "category": "Cat2_Clear_Start",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 1.2,
            "clinical_setting": "lrti",
            "temperature": 39.4,
            "respiratory_rate": 26,
            "systolic_bp": 108,
            "heart_rate": 104,
            "gcs_score": 15,
            "crp": 142.0,
            "wbc": 16.8,
            "lactate": 1.8,
            "creatinine": 1.1,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "68-year-old male, 2 days productive cough, right lower lobe consolidation on CXR. Former smoker. Hemodynamically stable."
        }
    },
    {
        "id": 5,
        "category": "Cat2_Clear_Start",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 4.8,
            "clinical_setting": "sepsis",
            "temperature": 39.8,
            "respiratory_rate": 30,
            "systolic_bp": 92,
            "heart_rate": 118,
            "gcs_score": 14,
            "crp": 210.0,
            "wbc": 22.1,
            "lactate": 3.2,
            "creatinine": 1.8,
            "clinical_unstable": True,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "72-year-old female, 1 day fever and confusion. Suspected urosepsis. BP falling. Transferred to ICU."
        }
    },
    {
        "id": 6,
        "category": "Cat2_Clear_Start",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.82,
            "clinical_setting": "lrti",
            "temperature": 38.9,
            "respiratory_rate": 24,
            "systolic_bp": 114,
            "heart_rate": 96,
            "gcs_score": 15,
            "crp": 98.0,
            "wbc": 14.2,
            "lactate": 1.4,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "55-year-old male, bilateral infiltrates on CT, 3 days fever, productive cough. Legionella urinary antigen pending."
        }
    },
    {
        "id": 7,
        "category": "Cat2_Clear_Start",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 8.4,
            "clinical_setting": "sepsis",
            "temperature": 40.1,
            "respiratory_rate": 34,
            "systolic_bp": 78,
            "heart_rate": 124,
            "gcs_score": 12,
            "crp": 320.0,
            "wbc": 28.4,
            "lactate": 4.1,
            "creatinine": 2.4,
            "clinical_unstable": True,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "61-year-old male, severe sepsis, suspected abdominal source. Lactate 4.1. Transferred to ICU immediately."
        }
    },
    {
        "id": 8,
        "category": "Cat2_Clear_Start",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 2.1,
            "clinical_setting": "lrti",
            "temperature": 39.6,
            "respiratory_rate": 28,
            "systolic_bp": 104,
            "heart_rate": 110,
            "gcs_score": 15,
            "crp": 188.0,
            "wbc": 19.6,
            "lactate": 2.0,
            "creatinine": 1.3,
            "clinical_unstable": False,
            "high_risk_patient": True,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": True,
            "on_antibiotics": False,
            "clinical_notes": "77-year-old female, immunosuppressed on steroids for rheumatoid arthritis, admitted with pneumonia. High-risk profile."
        }
    },

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 3 — Gray Zone
    # Expected: clinician_decision
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "category": "Cat3_Gray_Zone",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 0.18,
            "clinical_setting": "lrti",
            "temperature": 38.2,
            "respiratory_rate": 20,
            "systolic_bp": 116,
            "heart_rate": 88,
            "gcs_score": 15,
            "crp": 32.0,
            "wbc": 10.8,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "58-year-old male, 4 days productive cough, mild infiltrate on CXR. Clinical picture borderline."
        }
    },
    {
        "id": 10,
        "category": "Cat3_Gray_Zone",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "moderate",
        "input": {
            "pct_value": 0.31,
            "clinical_setting": "lrti",
            "temperature": 38.5,
            "respiratory_rate": 21,
            "systolic_bp": 120,
            "heart_rate": 84,
            "gcs_score": 15,
            "crp": 45.0,
            "wbc": 11.2,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "49-year-old female, pneumonia suspected clinically but mild presentation. PCT in encourage zone but clinical picture mild."
        }
    },
    {
        "id": 11,
        "category": "Cat3_Gray_Zone",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 1.1,
            "clinical_setting": "sepsis",
            "temperature": 38.8,
            "respiratory_rate": 22,
            "systolic_bp": 106,
            "heart_rate": 94,
            "gcs_score": 15,
            "crp": 88.0,
            "wbc": 13.4,
            "lactate": 1.6,
            "creatinine": 1.2,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "64-year-old male, ICU day 1, suspected infection but source unclear. Stable but borderline PCT."
        }
    },
    {
        "id": 12,
        "category": "Cat3_Gray_Zone",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 0.22,
            "clinical_setting": "lrti",
            "temperature": 38.1,
            "respiratory_rate": 19,
            "systolic_bp": 124,
            "heart_rate": 78,
            "gcs_score": 15,
            "crp": 28.0,
            "wbc": 9.8,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "symptom_onset_hours": 8,
            "clinical_notes": "71-year-old female, elderly with mild pneumonia symptoms. PCT borderline. Symptom onset only 8 hours ago — PCT may not have peaked."
        }
    },
    {
        "id": 13,
        "category": "Cat3_Gray_Zone",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 0.72,
            "clinical_setting": "sepsis",
            "temperature": 38.6,
            "respiratory_rate": 20,
            "systolic_bp": 112,
            "heart_rate": 90,
            "gcs_score": 15,
            "crp": 56.0,
            "wbc": 12.1,
            "lactate": 1.3,
            "creatinine": 1.1,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "53-year-old male, possible early sepsis from wound infection. PCT 0.72 indeterminate. Clinically stable. Serial measurement planned."
        }
    },

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 4 — Override Cases (PCT low but clinical override required)
    # Expected: start / strong
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "category": "Cat4_Override",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.07,
            "clinical_setting": "lrti",
            "temperature": 38.0,
            "respiratory_rate": 18,
            "systolic_bp": 88,
            "heart_rate": 112,
            "gcs_score": 13,
            "crp": 15.0,
            "wbc": 9.2,
            "clinical_unstable": True,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "45-year-old male, PCT below threshold but hemodynamically unstable. BP 88 systolic. GCS declining. Clinical instability override required."
        }
    },
    {
        "id": 15,
        "category": "Cat4_Override",
        "ground_truth": "start",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.3,
            "clinical_setting": "sepsis",
            "temperature": 37.9,
            "respiratory_rate": 17,
            "systolic_bp": 116,
            "heart_rate": 82,
            "gcs_score": 15,
            "crp": 22.0,
            "wbc": 8.4,
            "clinical_unstable": False,
            "high_risk_patient": True,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": True,
            "on_antibiotics": False,
            "clinical_notes": "38-year-old female, neutropenic post-chemotherapy (ANC 0.1). PCT low but neutropenic high-risk profile mandates antibiotic initiation."
        }
    },
    {
        "id": 16,
        "category": "Cat4_Override",
        "ground_truth": "start",
        "ground_truth_strength": "moderate",
        "input": {
            "pct_value": 0.12,
            "clinical_setting": "lrti",
            "temperature": 38.3,
            "respiratory_rate": 22,
            "systolic_bp": 102,
            "heart_rate": 96,
            "gcs_score": 14,
            "crp": 18.0,
            "wbc": 8.8,
            "creatinine": 1.4,
            "clinical_unstable": False,
            "high_risk_patient": True,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "82-year-old male, frail elderly, high-risk profile, gray zone PCT. Family reports rapid deterioration over 12 hours."
        }
    },

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 5 — Confounder Cases
    # Expected: clinician_decision (confounder must be identified)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 17,
        "category": "Cat5_Confounder",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 1.8,
            "clinical_setting": "lrti",
            "temperature": 38.4,
            "respiratory_rate": 20,
            "systolic_bp": 116,
            "heart_rate": 84,
            "gcs_score": 15,
            "crp": 45.0,
            "wbc": 11.2,
            "creatinine": 3.8,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": True,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "66-year-old male, CKD stage 4 (creatinine 3.8). PCT elevated but likely due to reduced renal clearance — interpret with caution."
        }
    },
    {
        "id": 18,
        "category": "Cat5_Confounder",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 2.4,
            "clinical_setting": "postop",
            "temperature": 38.6,
            "respiratory_rate": 22,
            "systolic_bp": 118,
            "heart_rate": 96,
            "gcs_score": 15,
            "crp": 88.0,
            "wbc": 14.8,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": True,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "clinical_notes": "59-year-old female, 24 hours post major abdominal surgery. PCT elevated but non-infectious post-operative elevation expected in first 24-72h."
        }
    },
    {
        "id": 19,
        "category": "Cat5_Confounder",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "moderate",
        "input": {
            "pct_value": 0.14,
            "clinical_setting": "lrti",
            "temperature": 37.8,
            "respiratory_rate": 17,
            "systolic_bp": 122,
            "heart_rate": 74,
            "gcs_score": 15,
            "crp": 9.0,
            "wbc": 7.8,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": True,
            "on_antibiotics": False,
            "clinical_notes": "44-year-old female, renal transplant on tacrolimus. Pneumonia suspected. PCT may be blunted by immunosuppression — low PCT does not exclude infection."
        }
    },
    {
        "id": 20,
        "category": "Cat5_Confounder",
        "ground_truth": "clinician_decision",
        "ground_truth_strength": "weak",
        "input": {
            "pct_value": 0.09,
            "clinical_setting": "lrti",
            "temperature": 37.5,
            "respiratory_rate": 16,
            "systolic_bp": 120,
            "heart_rate": 76,
            "gcs_score": 15,
            "crp": 6.2,
            "wbc": 8.0,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": False,
            "symptom_onset_hours": 4,
            "clinical_notes": "51-year-old male, symptoms for only 4 hours. Suspected Legionella (travel history to endemic area). PCT may not have risen yet AND atypical pathogen expected to give low PCT."
        }
    },

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 6 — Kinetic Discontinue (on antibiotics, PCT declined ≥80%)
    # Expected: stop / strong
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "category": "Cat6_Kinetic_Discontinue",
        "ground_truth": "stop",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.18,
            "clinical_setting": "lrti",
            "temperature": 37.2,
            "respiratory_rate": 17,
            "systolic_bp": 124,
            "heart_rate": 76,
            "gcs_score": 15,
            "crp": 22.0,
            "wbc": 9.4,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": True,
            "antibiotic_day": 4,
            "previous_pct": [
                {"day": 0, "value": 2.8},
                {"day": 1, "value": 1.2},
                {"day": 2, "value": 0.4},
            ],
            "clinical_notes": "62-year-old male, day 4 of antibiotics for CAP. PCT declined from 2.8 to 0.18 — 94% decline. Clinically improved. Afebrile."
        }
    },
    {
        "id": 22,
        "category": "Cat6_Kinetic_Discontinue",
        "ground_truth": "stop",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.38,
            "clinical_setting": "sepsis",
            "temperature": 36.8,
            "respiratory_rate": 16,
            "systolic_bp": 128,
            "heart_rate": 72,
            "gcs_score": 15,
            "crp": 18.0,
            "wbc": 8.8,
            "lactate": 0.9,
            "creatinine": 1.1,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": True,
            "antibiotic_day": 5,
            "previous_pct": [
                {"day": 0, "value": 4.2},
                {"day": 1, "value": 2.1},
                {"day": 2, "value": 0.8},
            ],
            "clinical_notes": "70-year-old female, ICU day 5 after sepsis. PCT declined from 4.2 to 0.38 — 91% decline. Clinically recovered. Haemodynamically stable."
        }
    },
    {
        "id": 23,
        "category": "Cat6_Kinetic_Discontinue",
        "ground_truth": "stop",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 0.21,
            "clinical_setting": "lrti",
            "temperature": 37.0,
            "respiratory_rate": 15,
            "systolic_bp": 126,
            "heart_rate": 70,
            "gcs_score": 15,
            "crp": 15.0,
            "wbc": 8.2,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": True,
            "antibiotic_day": 3,
            "previous_pct": [
                {"day": 0, "value": 1.6},
                {"day": 1, "value": 0.8},
            ],
            "clinical_notes": "55-year-old female, day 3 of antibiotics for pneumonia. PCT declined from 1.6 to 0.21 — 87% decline. Below 0.25 threshold. Well and improving."
        }
    },

    # ══════════════════════════════════════════════════════════════════════
    # CATEGORY 7 — Treatment Failure (Day 4+, <80% decline or rising PCT)
    # Expected: escalate / strong
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 24,
        "category": "Cat7_Treatment_Failure",
        "ground_truth": "escalate",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 3.8,
            "clinical_setting": "sepsis",
            "temperature": 39.2,
            "respiratory_rate": 28,
            "systolic_bp": 96,
            "heart_rate": 108,
            "gcs_score": 13,
            "crp": 280.0,
            "wbc": 20.4,
            "lactate": 3.1,
            "creatinine": 1.6,
            "clinical_unstable": True,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": True,
            "antibiotic_day": 4,
            "previous_pct": [
                {"day": 0, "value": 4.1},
                {"day": 1, "value": 4.4},
                {"day": 2, "value": 3.9},
            ],
            "clinical_notes": "67-year-old male, day 4 of broad-spectrum antibiotics for sepsis. PCT trending upward then plateau — less than 10% change. Clinically deteriorating. Treatment failure suspected."
        }
    },
    {
        "id": 25,
        "category": "Cat7_Treatment_Failure",
        "ground_truth": "escalate",
        "ground_truth_strength": "strong",
        "input": {
            "pct_value": 1.9,
            "clinical_setting": "lrti",
            "temperature": 38.8,
            "respiratory_rate": 26,
            "systolic_bp": 102,
            "heart_rate": 100,
            "gcs_score": 14,
            "crp": 165.0,
            "wbc": 17.2,
            "lactate": 2.1,
            "creatinine": 1.2,
            "clinical_unstable": False,
            "high_risk_patient": False,
            "renal_failure": False,
            "recent_surgery": False,
            "burns_trauma": False,
            "immunosuppressed": False,
            "on_antibiotics": True,
            "antibiotic_day": 4,
            "previous_pct": [
                {"day": 0, "value": 2.2},
                {"day": 1, "value": 2.0},
                {"day": 2, "value": 1.8},
            ],
            "clinical_notes": "74-year-old female, day 4 of antibiotics for CAP. PCT declined only 14% from 2.2 to 1.9 — well below 80% threshold. Persistent fever. Treatment failure criteria met."
        }
    },

]

# Ground truth summary for scoring
GROUND_TRUTH = {c["id"]: {"recommendation": c["ground_truth"], "strength": c["ground_truth_strength"], "category": c["category"]} for c in BENCHMARK_CASES}
