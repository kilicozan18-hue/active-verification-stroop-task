# Active Verification Stroop Task (TÜBİTAK 2209-A)

Experimental paradigm and behavioral data-processing scripts developed at **Abdullah Gül University** under a nationally funded **TÜBİTAK 2209-A** undergraduate research grant (Application No. `1919B012553698`).

## Overview
This project investigates individual differences in **prophantasia**, **mental imagery vividness**, and **perceptual interference**. Using an Active Verification Stroop Task implemented in **PsychoPy**, the paradigm measures reaction-time (RT) interference and accuracy across varying voluntary imagery vividness profiles.

## Repository Structure
- `preprocess_stroop.py`: Automated Python pipeline for cleaning trial-level PsychoPy `.csv` logs, filtering outlier reaction times, and computing condition-level summary metrics for statistical modeling in SPSS.

## Tech Stack
- **Experiment Presentation:** PsychoPy (Python)
- **Data Preprocessing:** Python (`pandas`, `numpy`)
- **Statistical Analysis:** SPSS

## Ethics & Data Privacy
In compliance with institutional ethics guidelines, raw participant data files are excluded from this public repository.
