"""
create_support_chart.py

Purpose:
Create a simple chart from aggregate affordable-housing survey findings.

This script is intentionally small and public-safe. It uses only aggregate
survey percentages and does not include raw survey responses, names, emails,
addresses, comments, or any personally identifiable information.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Resolve paths relative to the repository root.
# This makes the script easier to run from GitHub Codespaces, a local terminal,
# or another development environment.
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "survey_findings_aggregate.csv"
VISUALS_DIR = ROOT / "visuals"
OUTPUT_PATH = VISUALS_DIR / "survey_support_summary.png"


def load_survey_findings() -> pd.DataFrame:
    """Load the aggregate survey findings CSV."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find data file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = {"finding", "percentage", "description"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return df


def create_chart(df: pd.DataFrame) -> None:
    """Create and save a horizontal bar chart of survey support percentages."""
    VISUALS_DIR.mkdir(exist_ok=True)

    # Sort so the highest-support finding appears first.
    chart_data = df.sort_values("percentage", ascending=True)

    plt.figure(figsize=(9, 4.8))
    bars = plt.barh(chart_data["finding"], chart_data["percentage"])

    plt.xlim(0, 100)
    plt.xlabel("Share of respondents (%)")
    plt.title("Resident Support for Housing Policy Options")

    # Add percentage labels at the end of each bar for easier reading.
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}%",
            va="center",
        )

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()

    print(f"Saved chart to: {OUTPUT_PATH}")


def main() -> None:
    """Run the full chart-generation workflow."""
    findings = load_survey_findings()
    create_chart(findings)


if __name__ == "__main__":
    main()
