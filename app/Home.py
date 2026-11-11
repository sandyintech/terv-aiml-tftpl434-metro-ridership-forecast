from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components import (
    setup_page,
    section_heading,
    show_chart,
    show_dataframe,
    footer,
)

from utils import (
    LINE_COLORS,
    LINE_ORDER,
    load_ridership_data,
    get_daily_network,
    fmt_number,
)


# ============================================================
# 1. INITIALIZATION
# ============================================================

setup_page(
    title="Metro Ridership Intelligence",
    active="Overview",
)

APP_DIR = Path(__file__).parent


# ============================================================
# 2. COMPLETE DASHBOARD DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ==========================================
       MAIN DASHBOARD
    ========================================== */

    [data-testid="stMainBlockContainer"] {
        max-width: 1700px;
        padding: 1.2rem 1.5rem 2rem 1.5rem;
    }

    .stApp {
        background: #F2F6F8;
    }


    /* ==========================================
       HERO BANNER
    ========================================== */

    .metro-hero {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(
                circle at 90% 15%,
                rgba(80, 255, 236, 0.30),
                transparent 35%
            ),
            linear-gradient(
                115deg,
                #103C50 0%,
                #126A79 52%,
                #16A6A5 100%
            );

        border: 1px solid rgba(105, 239, 231, 0.55);
        border-radius: 17px;

        padding: 30px 34px;

        margin-bottom: 22px;

        box-shadow:
            0 8px 24px rgba(10, 112, 132, 0.24),
            0 0 22px rgba(24, 190, 190, 0.18),
            inset 0 1px 0 rgba(255,255,255,0.20);
    }

    .metro-hero::after {
        content: "";
        position: absolute;

        width: 260px;
        height: 260px;

        right: -80px;
        top: -120px;

        border-radius: 50%;

        background: rgba(114,255,238,0.12);
        filter: blur(15px);

        pointer-events: none;
    }

    .hero-label {
        color: #A9F2E9;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.5px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #FFFFFF !important;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.8px;
        line-height: 1.2;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #E0F8F7 !important;
        font-size: 14px;
        font-weight: 400;
        line-height: 1.8;
        max-width: 850px;
    }


    /* ==========================================
       SECTION HEADINGS
    ========================================== */

    .section-heading {
        color: #173F52;
        font-size: 19px;
        font-weight: 750;
        margin-bottom: 4px;
    }

    .section-subheading {
        color: #758A98;
        font-size: 12px;
        margin-bottom: 15px;
    }


    /* ==========================================
       KPI CARDS
    ========================================== */

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #FFFFFF,
            #F9FDFE
        );

        border: 1px solid #D9E8EC;
        border-left: 4px solid #13A0A8;

        border-radius: 12px;

        padding: 17px 18px;

        min-height: 112px;

        box-shadow:
            0 4px 12px rgba(22, 91, 108, 0.07),
            0 0 9px rgba(22, 169, 174, 0.07);

        transition: all 0.25s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);

        border-color: #64C9CA;

        box-shadow:
            0 8px 22px rgba(17, 130, 146, 0.15),
            0 0 17px rgba(26, 190, 185, 0.16);
    }

    [data-testid="stMetricLabel"] {
        color: #6B8290 !important;
        font-size: 12px !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        color: #16475A !important;
        font-size: 25px !important;
        font-weight: 800 !important;
    }


    /* ==========================================
       CHART PANELS
    ========================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;

        border: 1px solid #E0E9ED !important;
        border-radius: 13px !important;

        box-shadow:
            0 4px 14px rgba(28, 70, 88, 0.055),
            0 0 8px rgba(20, 160, 170, 0.035);

        padding: 8px;
    }

    [data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border-radius: 10px;
    }


    /* ==========================================
       INPUT CONTROLS
    ========================================== */

    [data-testid="stDateInput"] input {
        background: #FFFFFF !important;
        color: #173F52 !important;
        border: 1px solid #C9DDE3 !important;
        border-radius: 8px !important;
    }

    [data-testid="stMultiSelect"] {
        background: transparent;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: #147F8D !important;
        border-radius: 6px !important;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] span {
        color: #FFFFFF !important;
    }

    label {
        color: #526E7D !important;
        font-weight: 650 !important;
        font-size: 12px !important;
    }


    /* ==========================================
       TABLES
    ========================================== */

    [data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #DDE8EC;
        border-radius: 10px;
    }


    /* ==========================================
       NAVIGATION CARDS
    ========================================== */

    .module-number {
        color: #16A0A9;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
    }


    /* ==========================================
       DIVIDERS
    ========================================== */

    hr {
        border-color: #DCE7EA !important;
        margin-top: 14px !important;
        margin-bottom: 17px !important;
    }


    /* ==========================================
       RESPONSIVE
    ========================================== */

    @media(max-width: 768px) {

        .metro-hero {
            padding: 23px 20px;
        }

        .hero-title {
            font-size: 25px;
        }

        [data-testid="stMainBlockContainer"] {
            padding: 1rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. LOAD DATA
# ============================================================

try:

    df = load_ridership_data().copy()

except Exception as error:

    st.error(f"Unable to load dataset: {error}")
    st.stop()


required_columns = {
    "date",
    "line",
    "ridership",
}

if not required_columns.issubset(df.columns):

    st.error("Required dataset columns are missing.")
    st.stop()


df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce",
)

df["ridership"] = pd.to_numeric(
    df["ridership"],
    errors="coerce",
)

df = df.dropna(
    subset=["date", "line", "ridership"]
)

df = df[df["ridership"] >= 0]

if df.empty:

    st.warning("No valid ridership records found.")
    st.stop()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <style>

    /* Hero container styling */
    .st-key-metro_hero {
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(92, 255, 229, 0.30),
                transparent 35%
            ),
            linear-gradient(
                115deg,
                #103C50,
                #126A79,
                #16A6A5
            );

        padding: 30px 35px;
        border-radius: 18px;
        border: 1px solid rgba(105, 239, 231, 0.6);

        box-shadow:
            0 8px 28px rgba(10, 112, 132, 0.25),
            0 0 25px rgba(24, 190, 190, 0.20);

        margin-bottom: 25px;
    }

    .st-key-metro_hero [data-testid="stCaption"] {
        color: #A9F2E9 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.5px;
    }

    .st-key-metro_hero h1 {
        color: #FFFFFF !important;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .st-key-metro_hero p {
        color: #E0F8F7 !important;
        font-size: 14px;
        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(key="metro_hero"):

    st.caption("METRO OPERATIONS ANALYTICS PLATFORM")

    st.title("Ridership Intelligence")

    st.write(
        "A unified platform for historical passenger demand analysis, "
        "metro line performance, machine learning forecasting "
        "and operational capacity planning."
    )

# ============================================================
# 5. FILTER SECTION
# ============================================================

section_heading(
    "Dashboard Filters",
    "Configure the reporting period and selected metro lines.",
)

filter1, filter2 = st.columns([1.5, 1])

minimum_date = df["date"].min().date()
maximum_date = df["date"].max().date()

with filter1:

    selected_dates = st.date_input(
        "Reporting Period",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date,
        format="DD/MM/YYYY",
    )

with filter2:

    available_lines = [
        line
        for line in LINE_ORDER
        if line in df["line"].unique()
    ]

    selected_lines = st.multiselect(
        "Metro Lines",
        options=available_lines,
        default=available_lines,
    )


if not selected_lines:

    st.warning("Select at least one metro line.")
    st.stop()


if not isinstance(selected_dates, (tuple, list)) or len(selected_dates) != 2:

    st.info("Select both the start and end dates.")
    st.stop()


start_date, end_date = selected_dates

if start_date > end_date:

    st.error("Invalid reporting period.")
    st.stop()


filtered_df = df[
    (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
    & (df["line"].isin(selected_lines))
].copy()


if filtered_df.empty:

    st.warning("No records available for the selected filters.")
    st.stop()


# ============================================================
# 6. CALCULATIONS
# ============================================================

daily_network = get_daily_network(filtered_df)

daily_network["date"] = pd.to_datetime(
    daily_network["date"]
)

daily_network = daily_network.sort_values("date")

daily_network["moving_average"] = (
    daily_network["network_ridership"]
    .rolling(7, min_periods=1)
    .mean()
)

total_passengers = filtered_df["ridership"].sum()

average_daily = daily_network["network_ridership"].mean()

peak_row = daily_network.loc[
    daily_network["network_ridership"].idxmax()
]

peak_ridership = peak_row["network_ridership"]

peak_date = peak_row["date"]

operating_line_days = (
    filtered_df[["date", "line"]]
    .drop_duplicates()
    .shape[0]
)


# ============================================================
# 7. KPI SECTION
# ============================================================

st.divider()

section_heading(
    "Network Performance",
    "Key passenger demand indicators for the selected period.",
)

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Total Passengers",
        fmt_number(total_passengers),
    )

with k2:

    st.metric(
        "Average Daily Ridership",
        fmt_number(average_daily),
    )

with k3:

    st.metric(
        "Peak Daily Ridership",
        fmt_number(peak_ridership),
    )

with k4:

    st.metric(
        "Operating Line-Days",
        fmt_number(operating_line_days),
    )

st.caption(
    f"Peak demand: {peak_date:%d %B %Y} "
    f"| Reporting period: {start_date:%d %b %Y} "
    f"to {end_date:%d %b %Y}"
)


# ============================================================
# 8. RIDERSHIP TREND
# ============================================================

st.divider()

section_heading(
    "Ridership Trend",
    "Daily passenger demand and seven-day moving average.",
)

trend_fig = go.Figure()

trend_fig.add_trace(
    go.Scatter(
        x=daily_network["date"],
        y=daily_network["network_ridership"],
        name="Daily Ridership",
        mode="lines",
        line=dict(
            color="#1196A5",
            width=1.8,
        ),
        fill="tozeroy",
        fillcolor="rgba(17,150,165,0.10)",
        hovertemplate=(
            "<b>%{x|%d %B %Y}</b>"
            "<br>Passengers: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)

trend_fig.add_trace(
    go.Scatter(
        x=daily_network["date"],
        y=daily_network["moving_average"],
        name="7-Day Moving Average",
        mode="lines",
        line=dict(
            color="#F0A13A",
            width=3,
        ),
    )
)

trend_fig.update_layout(
    height=330,
    hovermode="x unified",
    xaxis=dict(
        title="Date",
        tickformat="%b\n%Y",
        dtick="M3",
        tickfont=dict(
            color="#344F5D",
            size=12,
        ),
    ),
    yaxis=dict(
        title="Passenger Journeys",
        tickformat="~s",
        tickfont=dict(
            color="#344F5D",
            size=12,
        ),
    ),
    legend=dict(
        orientation="h",
        y=1.13,
        x=0,
    ),
)

show_chart(trend_fig, height=330)


# ============================================================
# 9. DEMAND DISTRIBUTION
# ============================================================

st.divider()

section_heading(
    "Demand Distribution",
    "Passenger contribution and weekday travel behaviour.",
)

left_chart, right_chart = st.columns(2, gap="medium")


# ---------------- PASSENGER CONTRIBUTION ----------------

line_distribution = (
    filtered_df.groupby("line", as_index=False)
    ["ridership"]
    .sum()
)

with left_chart:

    with st.container(border=True):

        st.markdown("##### Passenger Contribution")

        contribution_fig = px.pie(
            line_distribution,
            names="line",
            values="ridership",
            hole=0.65,
            color="line",
            color_discrete_map=LINE_COLORS,
        )

        contribution_fig.update_traces(
            textposition="inside",
            texttemplate="%{label}<br>%{percent}",
            marker=dict(
                line=dict(
                    color="#FFFFFF",
                    width=3,
                )
            ),
            hovertemplate=(
                "<b>%{label} Line</b>"
                "<br>Passengers: %{value:,.0f}"
                "<br>Contribution: %{percent}"
                "<extra></extra>"
            ),
        )

        contribution_fig.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=15),
        )

        show_chart(contribution_fig, height=320)


# ---------------- WEEKDAY RIDERSHIP ----------------

weekday_df = filtered_df.copy()

weekday_df["weekday"] = weekday_df["date"].dt.day_name()

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

weekday_summary = (
    weekday_df.groupby("weekday", as_index=False)
    ["ridership"]
    .mean()
)

weekday_summary["weekday"] = pd.Categorical(
    weekday_summary["weekday"],
    categories=weekday_order,
    ordered=True,
)

weekday_summary = weekday_summary.sort_values("weekday")

weekday_colors = [
    "#B9E5E5",
    "#9AD7D9",
    "#7CCACD",
    "#5DB9C1",
    "#36A7B2",
    "#168F9F",
    "#116D7D",
]

with right_chart:

    with st.container(border=True):

        st.markdown("##### Average Weekday Ridership")

        weekday_fig = go.Figure()

        weekday_fig.add_trace(
            go.Bar(
                x=weekday_summary["weekday"].astype(str),
                y=weekday_summary["ridership"],
                marker=dict(
                    color=weekday_colors,
                    line=dict(
                        color="#FFFFFF",
                        width=1,
                    ),
                ),
                text=[
                    f"{value / 1000:.0f}k"
                    for value in weekday_summary["ridership"]
                ],
                textposition="outside",
                textfont=dict(
                    color="#405967",
                    size=11,
                ),
                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>Average Passengers: %{y:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

        weekday_fig.update_layout(
            height=320,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Passengers",
            yaxis=dict(
                tickformat="~s",
                range=[
                    0,
                    weekday_summary["ridership"].max() * 1.18,
                ],
            ),
            margin=dict(l=10, r=10, t=25, b=35),
        )

        show_chart(weekday_fig, height=320)


# ============================================================
# 10. MONTHLY RIDERSHIP
# ============================================================

st.divider()

section_heading(
    "Monthly Ridership Performance",
    "Compare passenger demand across individual metro lines.",
)

monthly_df = filtered_df.copy()

monthly_df["month"] = (
    monthly_df["date"].dt.to_period("M").astype(str)
)

monthly_summary = (
    monthly_df.groupby(
        ["month", "line"],
        as_index=False,
    )["ridership"]
    .sum()
)

monthly_fig = px.line(
    monthly_summary,
    x="month",
    y="ridership",
    color="line",
    markers=True,
    color_discrete_map=LINE_COLORS,
)

monthly_fig.update_traces(
    line=dict(width=2.8),
    marker=dict(size=6),
)

monthly_fig.update_layout(
    height=330,
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Passenger Journeys",
    yaxis=dict(
        tickformat="~s",
    ),
    legend=dict(
        orientation="h",
        y=1.13,
        x=0,
    ),
)

show_chart(monthly_fig, height=330)


# ============================================================
# 11. LINE PERFORMANCE
# ============================================================

st.divider()

section_heading(
    "Metro Line Performance",
    "Individual operating performance and passenger contribution.",
)

line_summary = (
    filtered_df.groupby("line")
    .agg(
        total_ridership=("ridership", "sum"),
        average_ridership=("ridership", "mean"),
        maximum_ridership=("ridership", "max"),
        operating_days=("date", "nunique"),
    )
    .reset_index()
)

network_total = line_summary["total_ridership"].sum()

line_summary["contribution"] = (
    line_summary["total_ridership"]
    / network_total
    * 100
)

line_summary["line"] = pd.Categorical(
    line_summary["line"],
    categories=LINE_ORDER,
    ordered=True,
)

line_summary = line_summary.sort_values("line")

line_columns = st.columns(len(line_summary))

for column, (_, row) in zip(
    line_columns,
    line_summary.iterrows(),
):

    line_name = str(row["line"])

    line_color = LINE_COLORS.get(
        line_name,
        "#168F9F",
    )

    with column:

        with st.container(border=True):

            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid {line_color};
                    padding: 9px 12px;
                    margin-bottom: 12px;
                    color: #173F52;
                    font-size: 17px;
                    font-weight: 800;
                    background: #F7FBFC;
                    border-radius: 5px;
                ">
                    {line_name} Line
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.metric(
                "Total Passengers",
                fmt_number(row["total_ridership"]),
            )

            st.metric(
                "Average Daily Ridership",
                fmt_number(row["average_ridership"]),
            )

            st.metric(
                "Network Contribution",
                f"{row['contribution']:.1f}%",
            )


# ============================================================
# 12. DETAILED SUMMARY
# ============================================================

st.markdown("##### Detailed Line Summary")

display_summary = line_summary.copy()

display_summary["line"] = display_summary["line"].astype(str)

display_summary = display_summary.rename(
    columns={
        "line": "Metro Line",
        "total_ridership": "Total Ridership",
        "average_ridership": "Average Daily Ridership",
        "maximum_ridership": "Maximum Daily Ridership",
        "operating_days": "Operating Days",
        "contribution": "Contribution (%)",
    }
)

for column in [
    "Total Ridership",
    "Average Daily Ridership",
    "Maximum Daily Ridership",
]:

    display_summary[column] = (
        display_summary[column]
        .round(0)
        .map(lambda value: f"{value:,.0f}")
    )

display_summary["Contribution (%)"] = (
    display_summary["Contribution (%)"]
    .map(lambda value: f"{value:.2f}%")
)

show_dataframe(
    display_summary,
    height=165,
)


# ============================================================
# 13. ANALYTICS WORKSPACE
# ============================================================

st.divider()

section_heading(
    "Analytics Workspace",
    "Explore the analytical modules of the platform.",
)

modules = [
    (
        "01",
        "Ridership Analysis",
        "📊",
        "Historical demand, monthly trends and weekday behaviour.",
        "pages/1_Ridership_Analysis.py",
    ),
    (
        "02",
        "Line Analysis",
        "🚇",
        "Individual line performance and passenger comparisons.",
        "pages/2_Line_Analysis.py",
    ),
    (
        "03",
        "Forecasting",
        "📈",
        "Network and individual line ridership predictions.",
        "pages/3_Forecasting.py",
    ),
    (
        "04",
        "Model Performance",
        "🎯",
        "Evaluate models using MAE, RMSE and MAPE.",
        "pages/4_Model_Performance.py",
    ),
    (
        "05",
        "Explainability",
        "🧠",
        "Feature importance and prediction error analysis.",
        "pages/5_Explainability.py",
    ),
    (
        "06",
        "Capacity Planning",
        "⚙️",
        "Peak-hour demand and train frequency planning.",
        "pages/6_Capacity_Planning.py",
    ),
    (
        "07",
        "Data Quality",
        "🔍",
        "Missing values, duplicates and dataset consistency.",
        "pages/7_Data_Quality.py",
    ),
]

module_columns = st.columns(3, gap="medium")

for index, module in enumerate(modules):

    number, title, icon, description, page_path = module

    with module_columns[index % 3]:

        with st.container(border=True):

            st.caption(f"MODULE {number}")

            st.markdown(f"### {icon} {title}")

            st.write(description)

            if (APP_DIR / page_path).exists():

                st.page_link(
                    page_path,
                    label=f"Explore {title}",
                    icon="➡️",
                    width="stretch",
                )

            else:

                st.caption("Module under development")


# ============================================================
# 14. DATASET INFORMATION
# ============================================================

st.divider()

section_heading(
    "Dataset Information",
    "Historical coverage and dataset provenance.",
)

with st.expander("View Dataset Details"):

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Dataset Records",
            f"{len(df):,}",
        )

    with c2:

        st.metric(
            "Metro Lines",
            df["line"].nunique(),
        )

    with c3:

        coverage_days = (
            df["date"].max() - df["date"].min()
        ).days + 1

        st.metric(
            "Date Coverage",
            f"{coverage_days:,} days",
        )

    st.write(
        f"**Start Date:** {df['date'].min():%d %B %Y}"
    )

    st.write(
        f"**End Date:** {df['date'].max():%d %B %Y}"
    )

    st.warning(
        "This project uses synthetic metro ridership data "
        "for analytical and machine learning demonstration. "
        "It is not official Chennai Metro Rail operational data."
    )


# ============================================================
# 15. FOOTER
# ============================================================

footer()