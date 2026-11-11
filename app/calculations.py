import numpy as np
import pandas as pd


# ============================================================
# 1. COLUMN VALIDATION
# ============================================================

def validate_columns(df, required_columns):

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return True


# ============================================================
# 2. DATA PREPARATION
# ============================================================

def prepare_ridership_data(df):

    validate_columns(
        df,
        ["date", "line", "ridership"]
    )

    data = df.copy()

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    data["line"] = (
        data["line"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    data["ridership"] = pd.to_numeric(
        data["ridership"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["date", "line", "ridership"]
    )

    data = data[data["ridership"] >= 0]

    return data


# ============================================================
# 3. NETWORK KPIs
# ============================================================

def calculate_network_kpis(df):

    data = prepare_ridership_data(df)

    daily = (
        data.groupby("date")["ridership"]
        .sum()
        .reset_index()
    )

    total_ridership = data["ridership"].sum()

    average_daily_ridership = (
        daily["ridership"].mean()
        if not daily.empty else 0
    )

    if not daily.empty:

        peak_index = daily["ridership"].idxmax()

        peak_day = daily.loc[
            peak_index, "date"
        ]

        peak_ridership = daily.loc[
            peak_index, "ridership"
        ]

    else:

        peak_day = None
        peak_ridership = 0

    return {
        "total_ridership": total_ridership,
        "average_daily_ridership": average_daily_ridership,
        "peak_ridership": peak_ridership,
        "peak_day": peak_day,
        "operating_line_days": len(data),
        "number_of_lines": data["line"].nunique(),
        "number_of_days": data["date"].nunique()
    }


# ============================================================
# 4. DAILY NETWORK RIDERSHIP
# ============================================================

def calculate_daily_network(df):

    data = prepare_ridership_data(df)

    daily = (
        data.groupby("date")["ridership"]
        .sum()
        .reset_index()
    )

    daily.columns = [
        "date",
        "network_ridership"
    ]

    return daily.sort_values("date")


# ============================================================
# 5. MOVING AVERAGE
# ============================================================

def calculate_moving_average(
    df,
    window=7,
    value_column="network_ridership"
):

    data = df.copy()

    if value_column not in data.columns:
        raise ValueError(
            f"Column '{value_column}' not found."
        )

    data[value_column] = pd.to_numeric(
        data[value_column],
        errors="coerce"
    )

    data["moving_average"] = (
        data[value_column]
        .rolling(
            window=window,
            min_periods=1
        )
        .mean()
    )

    return data


# ============================================================
# 6. LINE PERFORMANCE
# ============================================================

def calculate_line_performance(df):

    data = prepare_ridership_data(df)

    result = (
        data.groupby("line")
        .agg(
            total_ridership=("ridership", "sum"),
            average_ridership=("ridership", "mean"),
            maximum_ridership=("ridership", "max"),
            operating_days=("date", "nunique")
        )
        .reset_index()
    )

    total = result["total_ridership"].sum()

    result["contribution_percent"] = (
        result["total_ridership"] / total * 100
        if total > 0 else 0
    )

    return result.sort_values(
        "total_ridership",
        ascending=False
    )


# ============================================================
# 7. WEEKDAY PERFORMANCE
# ============================================================

def calculate_weekday_performance(df):

    data = prepare_ridership_data(df)

    data["weekday"] = data["date"].dt.day_name()

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    result = (
        data.groupby("weekday")["ridership"]
        .mean()
        .reindex(weekday_order)
        .reset_index()
    )

    result.columns = [
        "weekday",
        "average_ridership"
    ]

    return result


# ============================================================
# 8. MONTHLY RIDERSHIP
# ============================================================

def calculate_monthly_ridership(df):

    data = prepare_ridership_data(df)

    data["month"] = (
        data["date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    result = (
        data.groupby(
            ["month", "line"]
        )["ridership"]
        .sum()
        .reset_index()
    )

    return result.sort_values("month")


# ============================================================
# 9. DAILY LINE COMPARISON
# ============================================================

def calculate_daily_line_comparison(df):

    data = prepare_ridership_data(df)

    result = (
        data.groupby(
            ["date", "line"]
        )["ridership"]
        .sum()
        .reset_index()
    )

    return result.sort_values("date")


# ============================================================
# 10. PEAK DEMAND
# ============================================================

def calculate_peak_demand(df):

    data = prepare_ridership_data(df)

    result = (
        data.groupby("line")["ridership"]
        .max()
        .reset_index()
    )

    result.columns = [
        "line",
        "peak_ridership"
    ]

    return result.sort_values(
        "peak_ridership",
        ascending=False
    )


# ============================================================
# 11. FORECAST METRICS
# ============================================================

def calculate_forecast_metrics(
    actual,
    predicted
):

    actual = np.asarray(
        actual,
        dtype=float
    )

    predicted = np.asarray(
        predicted,
        dtype=float
    )

    if len(actual) != len(predicted):
        raise ValueError(
            "Actual and predicted arrays must have equal lengths."
        )

    if len(actual) == 0:
        raise ValueError(
            "Actual and predicted arrays cannot be empty."
        )

    mae = np.mean(
        np.abs(actual - predicted)
    )

    rmse = np.sqrt(
        np.mean(
            (actual - predicted) ** 2
        )
    )

    nonzero = actual != 0

    mape = (
        np.mean(
            np.abs(
                (actual[nonzero] - predicted[nonzero])
                / actual[nonzero]
            )
        ) * 100
        if np.any(nonzero) else np.nan
    )

    denominator = np.sum(
        np.abs(actual)
    )

    wape = (
        np.sum(
            np.abs(actual - predicted)
        ) / denominator * 100
        if denominator != 0 else np.nan
    )

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "WAPE": wape
    }


# ============================================================
# 12. FORECAST ERRORS
# ============================================================

def calculate_forecast_errors(
    actual,
    predicted
):

    if len(actual) != len(predicted):
        raise ValueError(
            "Actual and predicted arrays must have equal lengths."
        )

    result = pd.DataFrame({
        "actual": actual,
        "predicted": predicted
    })

    result["error"] = (
        result["actual"] - result["predicted"]
    )

    result["absolute_error"] = (
        result["error"].abs()
    )

    result["percentage_error"] = np.where(
        result["actual"] != 0,
        result["absolute_error"]
        / result["actual"] * 100,
        np.nan
    )

    return result


# ============================================================
# 13. MODEL COMPARISON
# ============================================================

def calculate_model_comparison(
    actual,
    predictions
):

    rows = []

    for model_name, predicted in predictions.items():

        metrics = calculate_forecast_metrics(
            actual,
            predicted
        )

        metrics["model"] = model_name

        rows.append(metrics)

    return (
        pd.DataFrame(rows)
        [["model", "MAE", "RMSE", "MAPE", "WAPE"]]
        .sort_values("MAE")
    )


# ============================================================
# 14. RESIDUAL STATISTICS
# ============================================================

def calculate_residual_statistics(residuals):

    residuals = pd.Series(
        residuals
    ).dropna()

    if residuals.empty:

        return {
            "mean_residual": np.nan,
            "median_residual": np.nan,
            "std_residual": np.nan,
            "minimum_residual": np.nan,
            "maximum_residual": np.nan
        }

    return {
        "mean_residual": residuals.mean(),
        "median_residual": residuals.median(),
        "std_residual": residuals.std(),
        "minimum_residual": residuals.min(),
        "maximum_residual": residuals.max()
    }


# ============================================================
# 15. CAPACITY REQUIREMENTS
# ============================================================

def calculate_capacity_requirements(
    predicted_ridership,
    peak_hour_share=0.10,
    peak_direction_share=0.60,
    train_capacity=1200
):

    # ----------------------------------------
    # INPUT CONVERSION
    # ----------------------------------------

    ridership = np.asarray(
        predicted_ridership,
        dtype=float
    )

    peak_hour_share = float(peak_hour_share)
    peak_direction_share = float(peak_direction_share)
    train_capacity = float(train_capacity)

    # ----------------------------------------
    # VALIDATE NUMERICAL INPUTS
    # ----------------------------------------

    if not np.isfinite(ridership).all():
        raise ValueError(
            "Ridership must contain only finite values."
        )

    if (ridership < 0).any():
        raise ValueError(
            "Ridership cannot be negative."
        )

    if not np.isfinite(peak_hour_share):
        raise ValueError(
            "Peak-hour share must be finite."
        )

    if not 0 < peak_hour_share <= 1:
        raise ValueError(
            "Peak-hour share must be between 0 and 1."
        )

    if not np.isfinite(peak_direction_share):
        raise ValueError(
            "Peak-direction share must be finite."
        )

    if not 0 < peak_direction_share <= 1:
        raise ValueError(
            "Peak-direction share must be between 0 and 1."
        )

    if not np.isfinite(train_capacity):
        raise ValueError(
            "Train capacity must be finite."
        )

    if train_capacity <= 0:
        raise ValueError(
            "Train capacity must be positive."
        )

    # ----------------------------------------
    # PHPDT CALCULATION
    # ----------------------------------------

    phpdt = (
        ridership
        * peak_hour_share
        * peak_direction_share
    )

    # ----------------------------------------
    # REQUIRED TRAINS PER HOUR
    # ----------------------------------------

    required_trains_per_hour = np.ceil(
        phpdt / train_capacity
    ).astype(int)

    # ----------------------------------------
    # REQUIRED HEADWAY
    # ----------------------------------------

    required_headway = np.divide(
        60.0,
        required_trains_per_hour,
        out=np.full(
            required_trains_per_hour.shape,
            np.nan,
            dtype=float
        ),
        where=required_trains_per_hour > 0
    )

    # ----------------------------------------
    # RETURN RESULTS
    # ----------------------------------------

    return {
        "PHPDT": phpdt,
        "required_trains_per_hour": required_trains_per_hour,
        "required_headway_minutes": required_headway
    }

# ============================================================
# 16. CAPACITY SUMMARY
# ============================================================

def calculate_capacity_summary(df):

    data = df.copy()

    validate_columns(
        data,
        ["line"]
    )

    numeric_columns = [
        "predicted_ridership",
        "PHPDT",
        "required_trains_per_hour",
        "required_headway_minutes"
    ]

    aggregation = {}

    for column in numeric_columns:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

            aggregation[column] = (
                "max"
                if column in [
                    "PHPDT",
                    "required_trains_per_hour",
                    "required_headway_minutes"
                ]
                else "mean"
            )

    if not aggregation:
        raise ValueError(
            "No supported capacity columns found."
        )

    return (
        data.groupby("line")
        .agg(aggregation)
        .reset_index()
    )


# ============================================================
# 17. DATA QUALITY
# ============================================================

def calculate_data_quality(df):

    total_cells = (
        len(df) * len(df.columns)
    )

    missing_cells = int(
        df.isna().sum().sum()
    )

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_cells": missing_cells,
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_percentage": (
            missing_cells / total_cells * 100
            if total_cells > 0 else 0
        )
    }


# ============================================================
# 18. MISSING VALUES
# ============================================================

def calculate_missing_values(df):

    result = (
        df.isna()
        .sum()
        .reset_index()
    )

    result.columns = [
        "column",
        "missing_count"
    ]

    result["missing_percentage"] = (
        result["missing_count"]
        / len(df) * 100
        if len(df) > 0 else 0
    )

    return result


# ============================================================
# 19. OUTLIER DETECTION
# ============================================================

def detect_outliers_iqr(
    df,
    column="ridership"
):

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found."
        )

    data = df.copy()

    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    data["is_outlier"] = (
        (data[column] < lower_limit)
        | (data[column] > upper_limit)
    )

    return data


# ============================================================
# 20. CORRELATION
# ============================================================

def calculate_correlation(df):

    numeric_data = df.select_dtypes(
        include=np.number
    )

    return numeric_data.corr()


# ============================================================
# 21. SUMMARY STATISTICS
# ============================================================

def calculate_summary_statistics(df):

    return df.describe().T


# ============================================================
# END OF CALCULATIONS MODULE
# ============================================================