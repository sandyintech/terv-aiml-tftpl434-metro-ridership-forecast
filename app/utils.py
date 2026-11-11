from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

APP_PATH = Path(__file__).resolve().parent
PROJECT_PATH = APP_PATH.parent

DATA_PATH = PROJECT_PATH / "data"
OUTPUT_PATH = PROJECT_PATH / "outputs"
MODEL_PATH = PROJECT_PATH / "models"


# ============================================================
# METRO LINE CONFIGURATION
# ============================================================

LINE_ORDER = [
    "Blue",
    "Green",
    "Purple"
]

LINE_COLORS = {
    "Blue": "#4F8CFF",
    "Green": "#22C55E",
    "Purple": "#A78BFA"
}


# ============================================================
# DATASET CONFIGURATION
# ============================================================

CLEANED_DATA_FILE = (
    OUTPUT_PATH / "cleaned_metro_ridership.csv"
)

REQUIRED_COLUMNS = [
    "date",
    "line",
    "ridership"
]


# ============================================================
# LOAD CLEANED RIDERSHIP DATA
# ============================================================

@st.cache_data(show_spinner="Loading metro ridership data...")
def load_ridership_data():

    if not CLEANED_DATA_FILE.exists():

        raise FileNotFoundError(
            f"Cleaned dataset not found: {CLEANED_DATA_FILE}\n"
            "Please ensure cleaned_metro_ridership.csv "
            "exists inside the outputs folder."
        )

    df = pd.read_csv(CLEANED_DATA_FILE)

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Dataset is missing required columns: "
            f"{missing_columns}"
        )

    # Standardise column values
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["line"] = (
        df["line"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["ridership"] = pd.to_numeric(
        df["ridership"],
        errors="coerce"
    )

    # Validate dates
    if df["date"].isna().any():

        raise ValueError(
            "Dataset contains invalid date values."
        )

    # Validate ridership
    if df["ridership"].isna().any():

        raise ValueError(
            "Dataset contains missing or invalid ridership values."
        )

    if (df["ridership"] < 0).any():

        raise ValueError(
            "Dataset contains negative ridership values."
        )

    # Validate metro line names
    invalid_lines = set(df["line"].unique()) - set(LINE_ORDER)

    if invalid_lines:

        raise ValueError(
            f"Unexpected metro line names: {invalid_lines}"
        )

    # Check duplicate line-date combinations
    duplicates = df.duplicated(
        subset=["date", "line"]
    )

    if duplicates.any():

        raise ValueError(
            "Duplicate date-line records found in the cleaned dataset."
        )

    # Sort dataset
    df = df.sort_values(
        ["date", "line"]
    ).reset_index(drop=True)

    return df


# ============================================================
# NETWORK DAILY RIDERSHIP
# ============================================================

def get_daily_network(df):

    if df.empty:

        return pd.DataFrame(
            columns=[
                "date",
                "network_ridership"
            ]
        )

    daily_network = (
        df.groupby("date", as_index=False)
        ["ridership"]
        .sum()
        .rename(
            columns={
                "ridership": "network_ridership"
            }
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    return daily_network


# ============================================================
# NUMBER FORMATTING
# ============================================================

def fmt_number(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:,.0f}"


def fmt_decimal(value, decimals=2):

    if pd.isna(value):
        return "N/A"

    return f"{value:,.{decimals}f}"


def fmt_percent(value, decimals=2):

    if pd.isna(value):
        return "N/A"

    return f"{value:.{decimals}f}%"


# ============================================================
# LOAD OUTPUT CSV FILES
# ============================================================

@st.cache_data
def load_output_csv(filename, required_columns=None, required=False):

    file_path = OUTPUT_PATH / filename

    if not file_path.exists():

        if required:

            raise FileNotFoundError(
                f"Required output file not found: {file_path}"
            )

        return pd.DataFrame()

    data = pd.read_csv(file_path)

    if required_columns:

        missing = [
            col for col in required_columns
            if col not in data.columns
        ]

        if missing:

            raise ValueError(
                f"{filename} is missing columns: {missing}"
            )

    return data