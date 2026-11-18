"""
Trial-level preprocessing pipeline for the Active Verification Stroop Task.
Filters practice trials, removes extreme RT outliers, and exports summary metrics.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def preprocess_participant_log(
    filepath: Path,
    min_rt: float = 0.200,
    max_rt: float = 3.000,
    sd_threshold: float = 2.5,
) -> pd.DataFrame:
    """Clean a single PsychoPy CSV output file and flag within-subject RT outliers."""
    df = pd.read_csv(filepath)

    # Exclude practice blocks if marked in the log
    if "is_practice" in df.columns:
        df = df[df["is_practice"] == 0].copy()

    # Keep valid response trials within absolute bounds
    df = df[df["rt"].between(min_rt, max_rt)].copy()

    # Compute condition-wise z-scores on correct trials for outlier trimming
    correct_mask = df["accuracy"] == 1
    df["rt_z"] = df.loc[correct_mask].groupby("condition")["rt"].transform(
        lambda x: (x - x.mean()) / x.std(ddof=1)
    )
    df["is_outlier"] = df["rt_z"].abs() > sd_threshold
    return df


def summarize_conditions(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate mean RT and accuracy per experimental condition."""
    valid_rt = clean_df[(clean_df["accuracy"] == 1) & (~clean_df["is_outlier"])]

    rt_summary = (
        valid_rt.groupby(["participant_id", "condition"])["rt"]
        .agg(mean_rt="mean", median_rt="median", valid_trials="count")
        .reset_index()
    )
    acc_summary = (
        clean_df.groupby(["participant_id", "condition"])["accuracy"]
        .mean()
        .reset_index(name="mean_accuracy")
    )
    return pd.merge(rt_summary, acc_summary, on=["participant_id", "condition"])


if __name__ == "__main__":
    raw_dir = Path("data/raw")
    output_file = Path("data/processed/stroop_summary.csv")

    if raw_dir.exists():
        summaries = [
            summarize_conditions(preprocess_participant_log(csv_path))
            for csv_path in sorted(raw_dir.glob("*.csv"))
        ]
        if summaries:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            pd.concat(summaries, ignore_index=True).to_csv(output_file, index=False)
