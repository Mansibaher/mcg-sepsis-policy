"""
MCG Sepsis & Other Febrile Illness (without focal infection)
Structured Admission Policy Implementation

Author: Mansi Aher
Date: February 2026

Purpose:
This script translates the MCG inpatient admission criteria into
explicit, auditable programmatic rules.

Clinical Logic:
- If ANY admission criterion is met -> Recommend inpatient admission.
- Missing data is explicitly tracked and never assumed.
- Designed for integration with EHR-based decision support systems.

Note:
Qualitative terms such as "severe", "persistent", or
"persists despite observation care" are assumed to be derived upstream
from structured clinical workflows.
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import json
import argparse
import sys


CRITERIA_LABELS: Dict[str, str] = {
    "hemodynamic_instability": "Hemodynamic instability",
    "bacteremia_if_cultures_performed": "Bacteremia (if blood cultures performed)",
    "hypoxemia": "Hypoxemia",
    "altered_mental_status_severe_or_persistent": "Severe or persistent altered mental status",
    "new_coagulopathy": "New coagulopathy (e.g., thrombocytopenia or prolonged PT)",
    "tachypnea_persists_despite_observation": "Tachypnea that persists despite observation care",
    "dehydration_severe_or_persistent": "Severe or persistent dehydration",
    "inability_to_maintain_oral_hydration_persists_after_observation":
        "Inability to maintain oral hydration requiring IV fluids that persists after observation care",
    "end_organ_dysfunction_severe_or_persistent": "Severe or persistent end-organ dysfunction",
    "core_temp_below_35c_due_to_infection": "Core temperature < 35C thought due to infection",
    "parenteral_antimicrobials_inpatient_only": "Parenteral antimicrobial regimen requiring inpatient basis",
    "isolation_required_not_possible_outside_hospital": "Isolation required not possible outside hospital",
}


@dataclass
class MCGSepsisAdmissionFlags:
    hemodynamic_instability: Optional[bool] = None
    bacteremia_if_cultures_performed: Optional[bool] = None
    hypoxemia: Optional[bool] = None
    altered_mental_status_severe_or_persistent: Optional[bool] = None
    new_coagulopathy: Optional[bool] = None
    tachypnea_persists_despite_observation: Optional[bool] = None
    dehydration_severe_or_persistent: Optional[bool] = None
    inability_to_maintain_oral_hydration_persists_after_observation: Optional[bool] = None
    end_organ_dysfunction_severe_or_persistent: Optional[bool] = None
    core_temp_below_35c_due_to_infection: Optional[bool] = None
    parenteral_antimicrobials_inpatient_only: Optional[bool] = None
    isolation_required_not_possible_outside_hospital: Optional[bool] = None

    patient_id: Optional[str] = None
    encounter_id: Optional[str] = None


@dataclass
class PolicyDecision:
    admit_inpatient: bool
    triggered_criteria: List[str]
    missing_inputs: List[str]
    summary: str
    debug: Dict[str, Any] = field(default_factory=dict)


# Build internal criteria dictionary for evaluation
# This allows easy extensibility if new criteria are added later.


def evaluate_mcg_sepsis_admission(flags: MCGSepsisAdmissionFlags) -> PolicyDecision:

    criteria_map: Dict[str, Optional[bool]] = {
        "hemodynamic_instability": flags.hemodynamic_instability,
        "bacteremia_if_cultures_performed": flags.bacteremia_if_cultures_performed,
        "hypoxemia": flags.hypoxemia,
        "altered_mental_status_severe_or_persistent": flags.altered_mental_status_severe_or_persistent,
        "new_coagulopathy": flags.new_coagulopathy,
        "tachypnea_persists_despite_observation": flags.tachypnea_persists_despite_observation,
        "dehydration_severe_or_persistent": flags.dehydration_severe_or_persistent,
        "inability_to_maintain_oral_hydration_persists_after_observation":
            flags.inability_to_maintain_oral_hydration_persists_after_observation,
        "end_organ_dysfunction_severe_or_persistent": flags.end_organ_dysfunction_severe_or_persistent,
        "core_temp_below_35c_due_to_infection": flags.core_temp_below_35c_due_to_infection,
        "parenteral_antimicrobials_inpatient_only": flags.parenteral_antimicrobials_inpatient_only,
        "isolation_required_not_possible_outside_hospital": flags.isolation_required_not_possible_outside_hospital,
    }

# Identify which admission criteria are explicitly met
# (True means clinician-defined threshold already satisfied)

    triggered_keys = [k for k, v in criteria_map.items() if v is True]
    missing_keys = [k for k, v in criteria_map.items() if v is None]

    triggered_labels = [CRITERIA_LABELS[k] for k in triggered_keys]
    missing_labels = [CRITERIA_LABELS[k] for k in missing_keys]

    admit = len(triggered_keys) >= 1

# Core logic:
# Admission is recommended if >= 1 criterion is met

    summary = (
        "Recommend inpatient admission: >=1 MCG admission criterion met."
        if admit
        else "Inpatient admission not indicated by this policy."
    )

# Track any missing or unavailable inputs
    return PolicyDecision(
        admit_inpatient=admit,
        triggered_criteria=triggered_labels,
        missing_inputs=missing_labels,
        summary=summary,
        debug={"criteria_values": criteria_map},
    )

# Loading Json files
def load_flags_from_json(path: str) -> MCGSepsisAdmissionFlags:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    allowed_fields = set(MCGSepsisAdmissionFlags.__dataclass_fields__.keys())
    filtered = {k: v for k, v in raw.items() if k in allowed_fields}

    return MCGSepsisAdmissionFlags(**filtered)


def print_decision(flags: MCGSepsisAdmissionFlags, decision: PolicyDecision) -> None:
    print("\nMCG Sepsis Admission Policy")
    print("--------------------------------")
    print(f"Patient ID:   {flags.patient_id}")
    print(f"Encounter ID: {flags.encounter_id}")

    print("\nAdmission Recommended:", decision.admit_inpatient)
    print("Summary:", decision.summary)

    print("\nTriggered Criteria:")
    if decision.triggered_criteria:
        for c in decision.triggered_criteria:
            print(" -", c)
    else:
        print(" - (none)")

    print("\nMissing Inputs:")
    if decision.missing_inputs:
        for m in decision.missing_inputs:
            print(" -", m)
    else:
        print(" - (none)")

    print("\nClinical Interpretation:")
    if decision.admit_inpatient:
        print(" At least one admission-level severity indicator is present.")
        print(" Inpatient monitoring and management are recommended.")
    else:
        print(" No admission-level severity indicators detected.")
        print(" Consider outpatient or observation management per clinician judgment.")


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="MCG Sepsis Admission Policy Evaluator")
    parser.add_argument("--input", help="Path to JSON input file")
    args = parser.parse_args(argv)

    if args.input:
        flags = load_flags_from_json(args.input)
        decision = evaluate_mcg_sepsis_admission(flags)
        print_decision(flags, decision)
    else:
        print("No input file provided. Please use --input <file.json>")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
