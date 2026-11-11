import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

PROJECT_PATH = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_PATH / "app"
OUTPUT_PATH = PROJECT_PATH / "outputs"

if str(APP_PATH) not in sys.path:
    sys.path.insert(0, str(APP_PATH))

from components import setup_page

setup_page(
    title="Capacity Planning",
    active="Capacity Planning"
)


# --------------------------------------------------
# THEME AND STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(0, 190, 190, 0.07),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(55, 125, 235, 0.07),
                transparent 30%
            ),
            #f5f8fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e7edf5;
    }

    .page-eyebrow {
        color: #009caa;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .page-title {
        color: #142b4a;
        font-size: 2.35rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .page-description {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 22px;
    }

    .section-heading {
        color: #183451;
        font-size: 1.35rem;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 3px;
    }

    .section-description {
        color: #718096;
        font-size: 0.88rem;
        margin-bottom: 15px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2ebf4;
        border-radius: 15px;
        padding: 19px 20px;
        min-height: 112px;
        box-shadow:
            0 4px 15px rgba(35, 75, 120, 0.045),
            0 0 12px rgba(0, 174, 181, 0.045);
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        border-color: #a8dfe1;
        box-shadow:
            0 8px 22px rgba(35, 75, 120, 0.08),
            0 0 15px rgba(0, 174, 181, 0.10);
        transform: translateY(-2px);
    }

    .metric-label {
        color: #718096;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #173453;
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .metric-caption {
        color: #8a9aad;
        font-size: 0.76rem;
        margin-top: 7px;
    }

    .info-banner {
        background: linear-gradient(
            110deg,
            #effafa,
            #f2f7ff
        );
        border: 1px solid #ccebea;
        border-left: 4px solid #00aeb5;
        border-radius: 12px;
        padding: 15px 18px;
        margin: 16px 0 22px 0;
        color: #405b73;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .insight-card {
        background: #ffffff;
        border: 1px solid #e1eaf3;
        border-radius: 13px;
        padding: 16px 18px;
        box-shadow: 0 4px 14px rgba(30, 70, 110, 0.04);
        margin-bottom: 10px;
    }

    .insight-title {
        color: #009caa;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }

    .insight-text {
        color: #40566f;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e4ebf3;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 9px;
        border: 1px solid #b9dfe2;
        color: #087e89;
        background: #ffffff;
        font-weight: 650;
    }

    div[data-testid="stDownloadButton"] button:hover {
        border-color: #00aeb5;
        color: #006f79;
        background: #f0fbfb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

LINE_COLORS = {
    "Blue": "#397fe8",
    "Green": "#16a477",
    "Purple": "#8b6bd6"
}


def section_title(title, description=None):

    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True
    )

    if description:
        st.markdown(
            f'<div class="section-description">{description}</div>',
            unsafe_allow_html=True
        )


def metric_card(label, value, caption=""):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig, height=390):

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#ffffff",
        font=dict(
            family="Arial, sans-serif",
            color="#42566f",
            size=12
        ),
        title=dict(
            font=dict(
                size=17,
                color="#183451"
            ),
            x=0.02,
            xanchor="left"
        ),
        margin=dict(
            l=45,
            r=25,
            t=65,
            b=45
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0)"
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#d9e5ef",
            font=dict(color="#183451")
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#dce5ee",
        tickfont=dict(color="#64748b")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#edf2f7",
        zerolinecolor="#dce5ee",
        tickfont=dict(color="#64748b")
    )

    return fig


def load_csv(filename):

    file_path = OUTPUT_PATH / filename

    if not file_path.exists():
        return None

    try:
        return pd.read_csv(file_path)

    except Exception as error:
        st.error(
            f"Unable to read {filename}: {error}"
        )
        return None


def standardize_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-]+", "_", regex=True)
    )

    return df


def format_number(value, decimals=0):

    if pd.isna(value):
        return "N/A"

    return f"{value:,.{decimals}f}"


def get_line_color(line):

    return LINE_COLORS.get(line, "#64748b")


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="page-eyebrow">
        METRO OPERATIONS | RESOURCE OPTIMIZATION
    </div>

    <div class="page-title">
        Capacity Planning
    </div>

    <div class="page-description">
        Estimate train frequency, passenger capacity requirements
        and service headways using forecasted metro ridership.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-banner">
        <strong>Planning methodology:</strong>
        These results are assumption-based estimates, not actual
        operating requirements. Daily ridership data alone cannot
        determine real hourly or directional passenger demand.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_capacity_data():

    daily = load_csv("daily_capacity_planning.csv")
    summary = load_csv("capacity_summary.csv")

    return daily, summary


daily_df, summary_df = load_capacity_data()


if daily_df is None or summary_df is None:

    st.error(
        "Capacity planning CSV files are missing or could not be loaded."
    )

    st.caption(
        "Expected files: outputs/daily_capacity_planning.csv "
        "and outputs/capacity_summary.csv"
    )

    st.stop()


daily_df = standardize_columns(daily_df)
summary_df = standardize_columns(summary_df)


# --------------------------------------------------
# STANDARDIZE COLUMN NAMES
# --------------------------------------------------

daily_df = daily_df.rename(
    columns={
        "required_headway_minutes": "headway_minutes"
    }
)

summary_df = summary_df.rename(
    columns={
        "maximum_phpdt": "max_phpdt",
        "average_phpdt": "avg_phpdt",
        "existing_trains_per_hour": "existing_tph",
        "required_headway_minutes": "headway_minutes",
        "average_error": "average_signed_error"
    }
)


# --------------------------------------------------
# VALIDATE REQUIRED COLUMNS
# --------------------------------------------------

required_daily_columns = [
    "date",
    "line",
    "predicted_ridership",
    "phpdt",
    "required_trains_per_hour",
    "headway_minutes"
]

missing_daily = [
    col for col in required_daily_columns
    if col not in daily_df.columns
]

if missing_daily:

    st.error(
        f"Daily capacity file is missing columns: {missing_daily}"
    )

    st.stop()


if "line" not in summary_df.columns:

    st.error(
        "Capacity summary file must contain a 'line' column."
    )

    st.stop()


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

daily_df["date"] = pd.to_datetime(
    daily_df["date"],
    errors="coerce"
)

daily_df["line"] = (
    daily_df["line"]
    .astype("string")
    .str.strip()
)

daily_df = daily_df.dropna(
    subset=["date", "line"]
).copy()


summary_df["line"] = (
    summary_df["line"]
    .astype("string")
    .str.strip()
)


daily_numeric = [
    "predicted_ridership",
    "phpdt",
    "required_trains_per_hour",
    "headway_minutes"
]

summary_numeric = [
    "average_daily_ridership",
    "maximum_daily_ridership",
    "max_phpdt",
    "avg_phpdt",
    "required_trains_per_hour",
    "headway_minutes",
    "existing_tph",
    "frequency_difference"
]


for col in daily_numeric:

    if col in daily_df.columns:

        daily_df[col] = pd.to_numeric(
            daily_df[col],
            errors="coerce"
        )


for col in summary_numeric:

    if col in summary_df.columns:

        summary_df[col] = pd.to_numeric(
            summary_df[col],
            errors="coerce"
        )


if daily_df.empty:

    st.error("No valid daily capacity records were found.")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.markdown("## Capacity Filters")

st.sidebar.caption(
    "Customize the metro lines and forecast period."
)

available_lines = sorted(
    daily_df["line"].dropna().unique().tolist()
)

selected_lines = st.sidebar.multiselect(
    "Select Metro Lines",
    options=available_lines,
    default=available_lines
)


min_date = daily_df["date"].min().date()
max_date = daily_df["date"].max().date()


selected_dates = st.sidebar.date_input(
    "Select Forecast Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if not selected_lines:

    st.warning("Select at least one metro line.")
    st.stop()


if not isinstance(selected_dates, (tuple, list)) or len(selected_dates) != 2:

    st.warning("Select both a start date and an end date.")
    st.stop()


start_date, end_date = selected_dates


if start_date > end_date:

    st.warning("Start date must be before end date.")
    st.stop()


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = daily_df[
    (daily_df["line"].isin(selected_lines))
    & (daily_df["date"].dt.date >= start_date)
    & (daily_df["date"].dt.date <= end_date)
].copy()


filtered_summary = summary_df[
    summary_df["line"].isin(selected_lines)
].copy()


if filtered_df.empty:

    st.warning(
        "No capacity records are available for the selected filters."
    )

    st.stop()


# --------------------------------------------------
# CAPACITY OVERVIEW
# --------------------------------------------------

st.divider()

section_title(
    "01 | Capacity Overview",
    "Key passenger demand and train service indicators for the selected period."
)


total_forecast = filtered_df[
    "predicted_ridership"
].sum(min_count=1)

average_phpdt = filtered_df[
    "phpdt"
].mean()

maximum_phpdt = filtered_df[
    "phpdt"
].max()

maximum_tph = filtered_df[
    "required_trains_per_hour"
].max()


c1, c2, c3, c4 = st.columns(4)


with c1:

    metric_card(
        "TOTAL FORECAST RIDERSHIP",
        format_number(total_forecast),
        "Combined selected line-days"
    )


with c2:

    metric_card(
        "AVERAGE PHPDT",
        format_number(average_phpdt),
        "Average peak-direction demand"
    )


with c3:

    metric_card(
        "MAXIMUM PHPDT",
        format_number(maximum_phpdt),
        "Highest estimated peak demand"
    )


with c4:

    metric_card(
        "MAXIMUM REQUIRED FREQUENCY",
        f"{format_number(maximum_tph)} TPH",
        "Estimated trains per hour"
    )


st.write("")


# --------------------------------------------------
# PHPDT ANALYSIS
# --------------------------------------------------

st.divider()

section_title(
    "02 | Peak Hour Peak Direction Traffic",
    "Track estimated peak-hour passenger demand across the selected metro lines."
)


st.caption(
    "PHPDT represents the estimated passenger demand in the peak hour "
    "and peak direction."
)


fig = px.line(
    filtered_df,
    x="date",
    y="phpdt",
    color="line",
    color_discrete_map=LINE_COLORS,
    markers=True,
    labels={
        "date": "Date",
        "phpdt": "PHPDT",
        "line": "Metro Line"
    },
    title="Daily PHPDT Forecast by Metro Line"
)


fig.update_traces(
    line=dict(width=2.8),
    marker=dict(size=5),
    hovertemplate=(
        "<b>%{fullData.name}</b><br>"
        "Date: %{x|%d %b %Y}<br>"
        "PHPDT: %{y:,.0f}"
        "<extra></extra>"
    )
)


fig = style_chart(fig, 420)


st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)


# --------------------------------------------------
# REQUIRED TRAIN FREQUENCY
# --------------------------------------------------

st.divider()

section_title(
    "03 | Required Train Frequency",
    "Estimated service frequency needed to accommodate projected peak demand."
)


fig = px.line(
    filtered_df,
    x="date",
    y="required_trains_per_hour",
    color="line",
    color_discrete_map=LINE_COLORS,
    markers=True,
    labels={
        "date": "Date",
        "required_trains_per_hour": "Trains per Hour",
        "line": "Metro Line"
    },
    title="Estimated Required Trains per Hour"
)


fig.update_traces(
    line=dict(width=2.8),
    marker=dict(size=5),
    hovertemplate=(
        "<b>%{fullData.name}</b><br>"
        "Date: %{x|%d %b %Y}<br>"
        "Frequency: %{y:.0f} trains/hour"
        "<extra></extra>"
    )
)


fig = style_chart(fig, 420)


st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)


# --------------------------------------------------
# HEADWAY ANALYSIS
# --------------------------------------------------

st.divider()

section_title(
    "04 | Estimated Train Headway",
    "Understand the estimated time interval between consecutive trains."
)


st.caption(
    "A lower headway indicates more frequent train services."
)


fig = px.line(
    filtered_df,
    x="date",
    y="headway_minutes",
    color="line",
    color_discrete_map=LINE_COLORS,
    markers=True,
    labels={
        "date": "Date",
        "headway_minutes": "Headway (Minutes)",
        "line": "Metro Line"
    },
    title="Estimated Headway by Metro Line"
)


fig.update_traces(
    line=dict(width=2.8),
    marker=dict(size=5),
    hovertemplate=(
        "<b>%{fullData.name}</b><br>"
        "Date: %{x|%d %b %Y}<br>"
        "Headway: %{y:.2f} minutes"
        "<extra></extra>"
    )
)


fig = style_chart(fig, 420)


st.plotly_chart(
    fig,
    width="stretch",
    config={"displayModeBar": False}
)


# --------------------------------------------------
# EXISTING VS REQUIRED FREQUENCY
# --------------------------------------------------

st.divider()

section_title(
    "05 | Existing vs Required Frequency",
    "Compare assumed existing train frequency with estimated frequency requirements."
)


st.caption(
    "Existing frequency is based on the assumptions stored in the project. "
    "Purple Line frequency may be unavailable in the current summary."
)


comparison_required = [
    "line",
    "existing_tph",
    "required_trains_per_hour"
]


if all(
    col in filtered_summary.columns
    for col in comparison_required
):

    comparison_df = filtered_summary.dropna(
        subset=[
            "existing_tph",
            "required_trains_per_hour"
        ]
    ).copy()


    if not comparison_df.empty:

        comparison_long = comparison_df.melt(
            id_vars=["line"],
            value_vars=[
                "existing_tph",
                "required_trains_per_hour"
            ],
            var_name="frequency_type",
            value_name="trains_per_hour"
        )


        comparison_long["frequency_type"] = (
            comparison_long["frequency_type"].replace(
                {
                    "existing_tph": "Existing Frequency",
                    "required_trains_per_hour": "Estimated Required Frequency"
                }
            )
        )


        fig = px.bar(
            comparison_long,
            x="line",
            y="trains_per_hour",
            color="frequency_type",
            barmode="group",
            text_auto=".1f",
            color_discrete_map={
                "Existing Frequency": "#9bb4c9",
                "Estimated Required Frequency": "#00aeb5"
            },
            labels={
                "line": "Metro Line",
                "trains_per_hour": "Trains per Hour",
                "frequency_type": "Frequency Type"
            },
            title="Existing vs Estimated Required Trains per Hour"
        )


        fig.update_traces(
            textposition="outside",
            marker_line_width=0
        )


        fig = style_chart(fig, 400)


        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False}
        )

    else:

        st.warning(
            "No existing frequency comparison data is available "
            "for the selected lines."
        )

else:

    st.warning(
        "The frequency comparison columns are unavailable "
        "in the capacity summary."
    )


# --------------------------------------------------
# LINE-WISE CAPACITY SUMMARY
# --------------------------------------------------

st.divider()

section_title(
    "06 | Line-wise Capacity Summary",
    "A consolidated view of ridership, passenger demand and frequency requirements."
)


display_columns = [
    "line",
    "average_daily_ridership",
    "maximum_daily_ridership",
    "avg_phpdt",
    "max_phpdt",
    "required_trains_per_hour",
    "headway_minutes",
    "existing_tph",
    "frequency_difference",
    "capacity_status"
]


available_columns = [
    col for col in display_columns
    if col in filtered_summary.columns
]


display_df = filtered_summary[
    available_columns
].copy()


display_df = display_df.rename(
    columns={
        "line": "Metro Line",
        "average_daily_ridership": "Average Daily Ridership",
        "maximum_daily_ridership": "Maximum Daily Ridership",
        "avg_phpdt": "Average PHPDT",
        "max_phpdt": "Maximum PHPDT",
        "required_trains_per_hour": "Required Trains / Hour",
        "headway_minutes": "Required Headway (Minutes)",
        "existing_tph": "Existing Trains / Hour",
        "frequency_difference": "Frequency Difference",
        "capacity_status": "Capacity Status"
    }
)


st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# CAPACITY INSIGHTS
# --------------------------------------------------

st.divider()

section_title(
    "07 | Capacity Insights",
    "Quick observations from the selected capacity planning results."
)


insight_columns = st.columns(3)


if "line" in filtered_df.columns and "phpdt" in filtered_df.columns:

    line_phpdt = (
        filtered_df.groupby("line")["phpdt"]
        .mean()
        .dropna()
    )

else:

    line_phpdt = pd.Series(dtype=float)


with insight_columns[0]:

    if not line_phpdt.empty:

        highest_line = line_phpdt.idxmax()

        highest_value = line_phpdt.max()

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">HIGHEST AVERAGE PHPDT</div>
                <div class="insight-text">
                    <strong>{highest_line} Line</strong><br>
                    Average estimated demand:
                    {highest_value:,.0f} passengers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("PHPDT comparison is unavailable.")


with insight_columns[1]:

    valid_headway = filtered_df[
        "headway_minutes"
    ].dropna()

    if not valid_headway.empty:

        lowest_headway = valid_headway.min()

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">LOWEST ESTIMATED HEADWAY</div>
                <div class="insight-text">
                    Minimum estimated interval:
                    <strong>{lowest_headway:.2f} minutes</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("Headway information is unavailable.")


with insight_columns[2]:

    valid_frequency = filtered_df[
        "required_trains_per_hour"
    ].dropna()

    if not valid_frequency.empty:

        highest_frequency = valid_frequency.max()

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">HIGHEST REQUIRED FREQUENCY</div>
                <div class="insight-text">
                    Maximum estimated service requirement:
                    <strong>{highest_frequency:.0f} trains/hour</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("Frequency information is unavailable.")


# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

st.divider()

section_title(
    "08 | Download Capacity Reports",
    "Export the filtered daily records and line-wise capacity summary."
)


download_col1, download_col2 = st.columns(2)


daily_csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


summary_csv = filtered_summary.to_csv(
    index=False
).encode("utf-8")


with download_col1:

    with st.container(border=True):

        st.markdown("**Daily Capacity Report**")

        st.caption(
            "Includes daily ridership forecasts, PHPDT, "
            "train frequency and headway."
        )

        st.download_button(
            label="Download Daily Report",
            data=daily_csv,
            file_name="metro_daily_capacity_report.csv",
            mime="text/csv",
            width="stretch"
        )


with download_col2:

    with st.container(border=True):

        st.markdown("**Capacity Summary Report**")

        st.caption(
            "Includes line-wise average and maximum capacity indicators."
        )

        st.download_button(
            label="Download Summary Report",
            data=summary_csv,
            file_name="metro_capacity_summary.csv",
            mime="text/csv",
            width="stretch"
        )


# --------------------------------------------------
# CAPACITY PLANNING ASSUMPTIONS
# --------------------------------------------------

st.divider()

section_title(
    "09 | Capacity Planning Assumptions",
    "Understand the assumptions used to estimate passenger demand and train frequency."
)


st.markdown(
    """
    <div class="info-banner">

    <strong>Planning assumptions</strong>

    <br><br>

    • Peak-hour share: <strong>10%</strong> of daily ridership.

    <br>

    • Peak-direction share: <strong>60%</strong> of peak-hour demand.

    <br>

    • Assumed train capacity: <strong>1,200 passengers</strong>.

    <br>

    • PHPDT is estimated using daily ridership and the assumed
    peak-hour and peak-direction shares.

    <br>

    • Required trains per hour are estimated using PHPDT
    divided by assumed train capacity.

    <br>

    • Headway is calculated from estimated trains per hour.

    <br><br>

    <strong>Important limitation:</strong>

    These calculations are planning estimates. Actual train scheduling
    requires hourly passenger counts, directional demand, train capacity,
    dwell times, service patterns and operational constraints.

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Metro Ridership Intelligence Platform | Capacity Planning Module"
)