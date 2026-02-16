MCG Sepsis Admission Policy Implementation
Author: Mansi Aher

---

## Overview

This project implements the **MCG Sepsis & Other Febrile Illness (without focal infection)** inpatient admission criteria as a structured policy in Python.

**Core Rule:**  
Recommend inpatient admission if ≥ 1 admission criterion is present.

The system:
- Tracks triggered criteria  
- Tracks missing inputs explicitly  
- Avoids unsafe assumptions  
- Provides human-readable output  
- Accepts JSON input compatible with EHR-style integration  

---

## Clinical Data Capture (Design Approach)

In a real hospital environment, required inputs would be derived from:

- Vitals (e.g., oxygen saturation, blood pressure, temperature)  
- Laboratory results (e.g., platelets, coagulation tests, cultures)  
- Medication/treatment records (e.g., IV antibiotics, vasopressors)  
- Clinical documentation and observation workflows  


---

## Data Structure

Each admission criterion is modeled as:

- `true` → criterion met  
- `false` → criterion not met  
- `null` → data unavailable  

The policy logic evaluates these flags and generates:

- Admission recommendation  
- Triggered criteria list  
- Missing input list  
- Clinical interpretation summary  

---

## Assumptions

- Qualitative terms (e.g., “severe,” “persistent”) are determined upstream.  
- Missing inputs are not assumed to be false.  
- This implementation supports clinical decision-making but does not replace physician judgment.  

---

## How to Run

### TRUE case

```bash
python policy_json.py --input patient_true.json

### FALSE case

```bash
python policy_json.py --input patient_false.json


<<<<<<< HEAD
FALSE case: python policy_json.py --input patient_false.json
=======
>>>>>>> 36091fa (Fix README formatting)
