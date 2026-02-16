# MCG Sepsis Admission Policy Implementation

Author: Mansi Aher  
Date: February 2026  

## Overview

This project implements the MCG Sepsis & Other Febrile Illness 
(without focal infection) inpatient admission criteria as a structured policy in Python.

Core Rule:
Recommend inpatient admission if ≥ 1 admission criterion is present.

The system:
- Tracks triggered criteria
- Tracks missing inputs explicitly
- Avoids unsafe assumptions
- Provides human-readable output
- Accepts JSON input for EHR-style integration

---

## How to Run

TRUE case:

    python policy_json.py --input patient_true.json

FALSE case:

    python policy_json.py --input patient_false.json

---

## Design Approach

- Boolean flags represent clinically evaluated thresholds
- Missing data (null) is explicitly tracked
- Policy logic is separated from presentation layer
- Structured for future integration into EHR systems

---

## Assumptions

- Clinical severity thresholds (e.g., severe, persistent) are determined upstream.
- This implementation supports decision support, not autonomous diagnosis.
- Final decisions must involve licensed clinicians.
