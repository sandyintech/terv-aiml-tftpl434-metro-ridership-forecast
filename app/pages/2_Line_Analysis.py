import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components import setup_page

from utils import (
    LINE_ORDER,
    LINE_COLORS,
    load_ridership_data,
    fmt_number
)

from calculations import (
    prepare_ridership_data,
    calculate_line_performance,
    calculate_monthly_ridership,
    calculate_daily_line_comparison,
    calculate_peak_demand
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

setup_page(
    title="Line Analysis",
    active="Line Analysis"
)


# ============================================================
# 2. PREMIUM LIGHT THEME
# ============================================================

st.markdown("""
<style>

:root {
    color-scheme: light;
}

/* ----------------------------------------------------------
   MAIN BACKGROUND
---------------------------------------------------------- */

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {

    background:
        radial-gradient(
            circle at 5% 3%,
            rgba(0, 190, 200, 0.075),
            transparent 27%
        ),

        radial-gradient(
            circle at 95% 8%,
            rgba(55, 125, 230, 0.065),
            transparent 28%
        ),

        #f4f8fc !important;

    color: #19364d !important;
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,0.92) !important;
}

[data-testid="stMainBlockContainer"],
.block-container {

    background: transparent !important;

    padding-top: 1.5rem;

    padding-bottom: 2rem;

    max-width: 1500px;
}


/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #edf5fa 100%
    ) !important;

    border-right: 1px solid #dce8f1;
}

[data-testid="stSidebar"] * {
    color: #25465e !important;
}


/* ----------------------------------------------------------
   PAGE HEADER
---------------------------------------------------------- */

.line-eyebrow {

    display: inline-block;

    padding: 6px 12px;

    border-radius: 30px;

    background: rgba(0, 174, 181, 0.09);

    border: 1px solid rgba(0, 174, 181, 0.20);

    color: #07878d !important;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.5px;

    margin-bottom: 13px;
}

.line-heading {

    font-size: 38px;

    font-weight: 850;

    color: #123b55 !important;

    letter-spacing: -1.2px;

    line-height: 1.15;

    margin-bottom: 9px;

    text-shadow:
        0 3px 14px rgba(0, 170, 190, 0.10);
}

.line-subheading {

    color: #637f95 !important;

    font-size: 14px;

    line-height: 1.8;

    max-width: 900px;

    margin-bottom: 25px;
}


/* ----------------------------------------------------------
   SECTION HEADINGS
---------------------------------------------------------- */

.section-heading {

    color: #173f59 !important;

    font-size: 21px;

    font-weight: 800;

    letter-spacing: -0.3px;

    margin-top: 30px;

    margin-bottom: 5px;
}

.section-description {

    color: #71899d !important;

    font-size: 13px;

    line-height: 1.6;

    margin-bottom: 15px;
}


/* ----------------------------------------------------------
   GENERAL TEXT
---------------------------------------------------------- */

.stMarkdown,
.stMarkdown p,
.stMarkdown li,
[data-testid="stCaptionContainer"] {

    color: #526d82;
}

label,
[data-testid="stWidgetLabel"] p {

    color: #294b64 !important;

    font-weight: 600 !important;
}


/* ----------------------------------------------------------
   KPI CARDS
---------------------------------------------------------- */

div[data-testid="stMetric"] {

    background: linear-gradient(
        145deg,
        #ffffff 0%,
        #f5fbff 100%
    ) !important;

    border: 1px solid rgba(0, 174, 190, 0.25);

    border-radius: 16px;

    padding: 19px 18px 16px 18px;

    min-height: 118px;

    box-shadow:
        0 4px 16px rgba(25, 75, 110, 0.06),
        0 0 12px rgba(0, 190, 200, 0.055),
        inset 0 0 12px rgba(0, 190, 200, 0.025);

    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {

    transform: translateY(-3px);

    border-color: #00b9bd;

    box-shadow:
        0 8px 22px rgba(20, 100, 140, 0.11),
        0 0 18px rgba(0, 210, 210, 0.15);
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {

    color: #68849a !important;

    font-size: 13px !important;
}

div[data-testid="stMetricValue"] {

    color: #123e59 !important;

    font-size: 27px !important;

    font-weight: 800 !important;
}

div[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}


/* ----------------------------------------------------------
   FILTER INPUTS
---------------------------------------------------------- */

div[data-baseweb="input"] {

    background: #ffffff !important;

    border: 1px solid #cbdce8 !important;

    border-radius: 9px !important;

    box-shadow: 0 2px 8px rgba(30, 80, 110, 0.04);
}

div[data-baseweb="input"]:focus-within {

    border-color: #00aeb5 !important;

    box-shadow: 0 0 0 2px rgba(0, 190, 190, 0.12);
}

div[data-baseweb="input"] input {

    color: #25465e !important;

    background: transparent !important;
}

div[data-baseweb="select"] > div {

    background: #ffffff !important;

    border-color: #cbdce8 !important;

    color: #25465e !important;

    border-radius: 9px !important;
}

div[data-baseweb="select"] input {
    color: #25465e !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background: #ffffff !important;
}

div[data-baseweb="menu"] li {
    color: #25465e !important;
}

div[data-baseweb="menu"] li:hover {
    background: #e5f5f5 !important;
}


/* ----------------------------------------------------------
   CONTENT CONTAINERS
---------------------------------------------------------- */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background: #ffffff !important;

    border: 1px solid #dce9f1;

    border-radius: 15px;

    box-shadow: 0 4px 16px rgba(30, 80, 110, 0.045);
}


/* ----------------------------------------------------------
   INSIGHT CARDS
---------------------------------------------------------- */

.insight-card {

    background: linear-gradient(
        135deg,
        #ffffff,
        #f1faff
    );

    border: 1px solid #d9eaf2;

    border-left: 4px solid #00aeb5;

    border-radius: 12px;

    padding: 15px 17px;

    min-height: 90px;

    box-shadow: 0 3px 12px rgba(30, 80, 110, 0.045);
}

.insight-label {

    color: #7890a3 !important;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.1px;

    margin-bottom: 7px;
}

.insight-value {

    color: #173f59 !important;

    font-size: 19px;

    font-weight: 800;
}

.insight-description {

    color: #71899d !important;

    font-size: 12px;

    margin-top: 5px;
}


/* ----------------------------------------------------------
   BUTTONS
---------------------------------------------------------- */

.stButton button,
.stDownloadButton button {

    border-radius: 9px !important;

    border: 1px solid #009fa8 !important;

    background: linear-gradient(
        135deg,
        #087f83,
        #079eaa
    ) !important;

    color: #ffffff !important;

    font-weight: 650 !important;

    box-shadow: 0 3px 10px rgba(0, 150, 160, 0.13);
}

.stButton button:hover,
.stDownloadButton button:hover {

    border-color: #00c8c8 !important;

    background: #056c78 !important;

    box-shadow: 0 0 14px rgba(0, 190, 190, 0.22);
}


/* ----------------------------------------------------------
   DATAFRAME
---------------------------------------------------------- */

div[data-testid="stDataFrame"] {

    background: #ffffff !important;

    border: 1px solid #d8e6ef;

    border-radius: 10px;

    overflow: hidden;
}


/* ----------------------------------------------------------
   EXPANDER
---------------------------------------------------------- */

[data-testid="stExpander"] {

    background: #ffffff !important;

    border: 1px solid #d8e6ef !important;

    border-radius: 12px !important;

    box-shadow: 0 3px 12px rgba(30, 80, 110, 0.04);
}

[data-testid="stExpander"] summary {
    color: #25465e !important;
}


/* ----------------------------------------------------------
   ALERTS AND DIVIDERS
---------------------------------------------------------- */

[data-testid="stAlert"] {

    background: #ffffff !important;

    color: #25465e !important;

    border-radius: 10px;

    border: 1px solid #dce8f0;
}

hr {
    border-color: #dce8f0 !important;
}


/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.line-footer {

    color: #7893a7 !important;

    font-size: 11px;

    letter-spacing: 1px;

    text-align: center;

    padding: 16px 0;
}


/* ----------------------------------------------------------
   RESPONSIVE
---------------------------------------------------------- */

@media (max-width: 768px) {

    .line-heading {
        font-size: 29px;
    }

    .section-heading {
        font-size: 19px;
    }

    div[data-testid="stMetric"] {
        padding: 14px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. CHART THEME
# ============================================================

CHART_BG = "#ffffff"
PAPER_BG = "#ffffff"

TEXT_COLOR = "#25465e"
GRID_COLOR = "rgba(80, 120, 150, 0.14)"

TEAL = "#00aeb5"
BLUE = "#397fe8"
ORANGE = "#f59e42"


def style_chart(fig, height=370):

    fig.update_layout(

        height=height,

        paper_bgcolor=PAPER_BG,

        plot_bgcolor=CHART_BG,

        font=dict(
            family="Arial",
            color=TEXT_COLOR,
            size=12
        ),

        margin=dict(
            l=40,
            r=25,
            t=55,
            b=50
        ),

        hovermode="closest",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color="#526d82",
                size=11
            )
        ),

        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#526d82",
            automargin=True
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False,
            color="#526d82",
            automargin=True
        ),

        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor=TEAL,
            font=dict(
                color="#19364d"
            )
        )

    )

    return fig


# ============================================================
# 4. REUSABLE SECTION TITLE
# ============================================================

def section_title(title, description):

    st.markdown(
        f"""
        <div class="section-heading">
            {title}
        </div>

        <div class="section-description">
            {description}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 5. REUSABLE INSIGHT CARD
# ============================================================

def insight_card(label, value, description=""):

    html = f"""
    <div class="insight-card">
        <div class="insight-label">{label}</div>
        <div class="insight-value">{value}</div>
        <div class="insight-description">{description}</div>
    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )

# ============================================================
# 6. PAGE HEADER
# ============================================================

st.markdown("""
<div class="line-eyebrow">
    METRO OPERATIONS ANALYTICS
</div>

<div class="line-heading">
    Metro Line Analysis
</div>

<div class="line-subheading">
    Explore individual metro line performance, passenger demand,
    growth patterns and operational behaviour.

    Compare ridership across different lines and identify
    the busiest periods within the metro network.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 7. LOAD DATA
# ============================================================

@st.cache_data(show_spinner="Loading metro ridership data...")
def get_data():

    return load_ridership_data()


try:

    raw_df = get_data()

    if raw_df is None or raw_df.empty:

        st.warning("No ridership data is available.")

        st.stop()

    df = prepare_ridership_data(raw_df)

except Exception as error:

    st.error(
        f"Unable to load or prepare ridership data: {error}"
    )

    st.stop()


if df is None or df.empty:

    st.warning(
        "No valid ridership records are available after data preparation."
    )

    st.stop()


# ============================================================
# 8. DATA VALIDATION
# ============================================================

required_columns = [
    "date",
    "line",
    "ridership"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        f"Required columns are missing: {missing_columns}"
    )

    st.stop()


df = df.copy()

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["ridership"] = pd.to_numeric(
    df["ridership"],
    errors="coerce"
)

df["line"] = df["line"].astype("string").str.strip()

df = df.dropna(
    subset=[
        "date",
        "line",
        "ridership"
    ]
)

if df.empty:

    st.warning(
        "No valid records remain after data validation."
    )

    st.stop()


# ============================================================
# 9. ANALYSIS FILTERS
# ============================================================

section_title(
    "Analysis Filters",
    "Choose the analysis period and the metro line you want to investigate."
)


with st.container(border=True):

    filter_col1, filter_col2 = st.columns(2)

    min_date = df["date"].min().date()

    max_date = df["date"].max().date()

    with filter_col1:

        selected_dates = st.date_input(
            "Select Date Range",

            value=(min_date, max_date),

            min_value=min_date,

            max_value=max_date,

            key="line_analysis_dates"
        )


    available_lines = [
        line for line in LINE_ORDER
        if line in df["line"].unique()
    ]

    # Include any valid lines not present in LINE_ORDER.

    for line in df["line"].unique():

        if line not in available_lines:

            available_lines.append(line)


    with filter_col2:

        selected_line = st.selectbox(
            "Select Metro Line",

            available_lines,

            key="line_analysis_selection"
        )


# ============================================================
# 10. DATE VALIDATION
# ============================================================

if not isinstance(selected_dates, (tuple, list)):

    st.info(
        "Select both a start date and an end date."
    )

    st.stop()


if len(selected_dates) != 2:

    st.info(
        "Select both a start date and an end date."
    )

    st.stop()


start_date, end_date = selected_dates


if start_date > end_date:

    st.warning(
        "Start date cannot be later than end date."
    )

    st.stop()


# ============================================================
# 11. FILTERED DATA
# ============================================================

filtered_df = df.loc[

    (df["date"].dt.date >= start_date)
    &
    (df["date"].dt.date <= end_date)

].copy()


line_df = filtered_df.loc[
    filtered_df["line"] == selected_line
].copy()


if filtered_df.empty:

    st.warning(
        "No records found for the selected date range."
    )

    st.stop()


if line_df.empty:

    st.warning(
        "No records available for the selected line and period."
    )

    st.stop()


line_color = LINE_COLORS.get(
    selected_line,
    TEAL
)


period_days = (
    pd.Timestamp(end_date) -
    pd.Timestamp(start_date)
).days + 1


st.caption(
    f"Analysis period: {start_date.strftime('%d %b %Y')} "
    f"to {end_date.strftime('%d %b %Y')} "
    f"| Selected line: {selected_line} "
    f"| Records: {len(line_df):,}"
)


# ============================================================
# 12. LINE PERFORMANCE KPIs
# ============================================================

section_title(
    f"{selected_line} Line Overview",
    "Key performance indicators for the selected metro line."
)


total_ridership = line_df["ridership"].sum()

average_ridership = line_df["ridership"].mean()

peak_ridership = line_df["ridership"].max()

operating_days = line_df["date"].nunique()


peak_record = line_df.loc[
    line_df["ridership"].idxmax()
]


k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "Total Ridership",
        fmt_number(total_ridership)
    )


with k2:

    st.metric(
        "Average Daily Ridership",
        fmt_number(average_ridership)
    )


with k3:

    st.metric(
        "Peak Daily Ridership",
        fmt_number(peak_ridership)
    )


with k4:

    st.metric(
        "Operating Days",
        fmt_number(operating_days)
    )


peak_date = pd.to_datetime(
    peak_record["date"]
).strftime("%d %B %Y")


st.caption(
    f"Highest recorded daily demand on {selected_line} Line: {peak_date}."
)


# ============================================================
# 13. DAILY RIDERSHIP TREND
# ============================================================

section_title(
    "Daily Ridership Trend",
    "Observe passenger demand fluctuations and the 7-day moving average."
)


daily = (
    line_df.groupby("date")["ridership"]
    .sum()
    .reset_index()
    .sort_values("date")
)


daily["moving_average"] = (
    daily["ridership"]
    .rolling(
        window=7,
        min_periods=1
    )
    .mean()
)


fig = go.Figure()


# Daily ridership area

fig.add_trace(
    go.Scatter(

        x=daily["date"],

        y=daily["ridership"],

        mode="lines",

        name="Daily Ridership",

        line=dict(
            color=line_color,
            width=1.6
        ),

        fill="tozeroy",

        fillcolor="rgba(0, 174, 181, 0.09)",

        opacity=0.9,

        hovertemplate=(
            "<b>%{x|%d %B %Y}</b><br>"
            "Ridership: %{y:,.0f}"
            "<extra></extra>"
        )

    )
)


# Moving average

fig.add_trace(
    go.Scatter(

        x=daily["date"],

        y=daily["moving_average"],

        mode="lines",

        name="7-Day Moving Average",

        line=dict(
            color=BLUE,
            width=3.2,
            shape="spline"
        ),

        hovertemplate=(
            "<b>%{x|%d %B %Y}</b><br>"
            "7-Day Average: %{y:,.0f}"
            "<extra></extra>"
        )

    )
)


fig.update_xaxes(
    tickformat="%d %b %Y",
    nticks=9,
    tickangle=-25
)

fig.update_yaxes(
    title="Passenger Count",
    tickformat=",.0f"
)


fig = style_chart(
    fig,
    420
)


with st.container(border=True):

    st.plotly_chart(
        fig,
        width="stretch"
    )


# Daily demand insights

highest_daily = daily.loc[
    daily["ridership"].idxmax()
]

lowest_daily = daily.loc[
    daily["ridership"].idxmin()
]


insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    insight_card(
        "HIGHEST DAILY DEMAND",
        fmt_number(highest_daily["ridership"]),

        pd.to_datetime(
            highest_daily["date"]
        ).strftime("%d %B %Y")
    )


with insight_col2:

    insight_card(
        "LOWEST DAILY DEMAND",
        fmt_number(lowest_daily["ridership"]),

        pd.to_datetime(
            lowest_daily["date"]
        ).strftime("%d %B %Y")
    )


# ============================================================
# 14. MONTHLY LINE PERFORMANCE
# ============================================================

section_title(
    "Monthly Ridership Performance",
    "Analyse monthly passenger demand and identify seasonal patterns."
)


try:

    monthly_data = calculate_monthly_ridership(
        line_df
    )

    if monthly_data is None or monthly_data.empty:

        st.info(
            "Monthly ridership information is unavailable."
        )

    else:

        fig = go.Figure()


        fig.add_trace(
            go.Bar(

                x=monthly_data["month"],

                y=monthly_data["ridership"],

                marker=dict(

                    color=line_color,

                    line=dict(
                        width=0
                    )

                ),

                name=selected_line,

                opacity=0.9,

                hovertemplate=(
                    "<b>%{x|%B %Y}</b><br>"
                    "Monthly Ridership: %{y:,.0f}"
                    "<extra></extra>"
                )

            )
        )


        fig.update_xaxes(
            tickformat="%b %Y",
            dtick="M2",
            tickangle=-25
        )

        fig.update_yaxes(
            title="Monthly Passengers",
            tickformat=",.0f"
        )


        fig = style_chart(
            fig,
            400
        )

        fig.update_layout(
            showlegend=False
        )


        with st.container(border=True):

            st.plotly_chart(
                fig,
                width="stretch"
            )


except Exception as error:

    st.error(
        f"Unable to generate monthly ridership chart: {error}"
    )


# ============================================================
# 15. METRO LINE COMPARISON
# ============================================================

section_title(
    "Metro Line Comparison",
    "Compare total and average passenger demand across all available lines."
)


line_performance = None


try:

    line_performance = calculate_line_performance(
        filtered_df
    )


    if line_performance is None or line_performance.empty:

        st.info(
            "Line comparison information is unavailable."
        )

    else:

        comparison_col1, comparison_col2 = st.columns(2)


        # ----------------------------------------------------
        # TOTAL RIDERSHIP COMPARISON
        # ----------------------------------------------------

        with comparison_col1:

            fig = px.bar(

                line_performance,

                x="line",

                y="total_ridership",

                color="line",

                color_discrete_map=LINE_COLORS,

                text="total_ridership"

            )


            fig.update_traces(

                marker_line_width=0,

                texttemplate="%{text:,.0f}",

                textposition="outside",

                cliponaxis=False,

                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Total Ridership: %{y:,.0f}"
                    "<extra></extra>"
                )

            )


            fig.update_yaxes(
                title="Total Ridership",
                tickformat=",.0f"
            )

            fig.update_layout(
                showlegend=False
            )

            fig = style_chart(
                fig,
                390
            )


            with st.container(border=True):

                st.markdown(
                    "**Total Ridership by Line**"
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )


        # ----------------------------------------------------
        # AVERAGE RIDERSHIP COMPARISON
        # ----------------------------------------------------

        with comparison_col2:

            fig = px.bar(

                line_performance,

                x="line",

                y="average_ridership",

                color="line",

                color_discrete_map=LINE_COLORS,

                text="average_ridership"

            )


            fig.update_traces(

                marker_line_width=0,

                texttemplate="%{text:,.0f}",

                textposition="outside",

                cliponaxis=False,

                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Average Daily Ridership: %{y:,.0f}"
                    "<extra></extra>"
                )

            )


            fig.update_yaxes(
                title="Average Daily Ridership",
                tickformat=",.0f"
            )

            fig.update_layout(
                showlegend=False
            )

            fig = style_chart(
                fig,
                390
            )


            with st.container(border=True):

                st.markdown(
                    "**Average Daily Ridership by Line**"
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )


except Exception as error:

    st.error(
        f"Unable to generate line comparison charts: {error}"
    )


# ============================================================
# 16. MONTHLY DEMAND COMPARISON
# ============================================================

section_title(
    "Monthly Demand Comparison",
    "Compare passenger demand trends across all metro lines."
)


try:

    all_monthly = calculate_monthly_ridership(
        filtered_df
    )


    if all_monthly is None or all_monthly.empty:

        st.info(
            "Monthly comparison data is unavailable."
        )

    else:

        fig = px.line(

            all_monthly,

            x="month",

            y="ridership",

            color="line",

            color_discrete_map=LINE_COLORS,

            markers=True

        )


        fig.update_traces(

            line=dict(
                width=2.8
            ),

            marker=dict(
                size=6
            )

        )


        fig.update_xaxes(
            tickformat="%b %Y",
            dtick="M2",
            tickangle=-25
        )


        fig.update_yaxes(
            title="Monthly Ridership",
            tickformat=",.0f"
        )


        fig = style_chart(
            fig,
            420
        )


        with st.container(border=True):

            st.plotly_chart(
                fig,
                width="stretch"
            )


except Exception as error:

    st.error(
        f"Unable to generate monthly line comparison: {error}"
    )


# ============================================================
# 17. PEAK DEMAND COMPARISON
# ============================================================

section_title(
    "Peak Demand Comparison",
    "Identify the maximum daily passenger demand recorded on each line."
)


try:

    peak_data = calculate_peak_demand(
        filtered_df
    )


    if peak_data is None or peak_data.empty:

        st.info(
            "Peak demand information is unavailable."
        )

    else:

        fig = go.Figure()


        fig.add_trace(
            go.Bar(

                x=peak_data["line"],

                y=peak_data["peak_ridership"],

                marker=dict(

                    color=[
                        LINE_COLORS.get(
                            line,
                            TEAL
                        )
                        for line in peak_data["line"]
                    ],

                    line=dict(
                        color="#ffffff",
                        width=1
                    )

                ),

                text=peak_data["peak_ridership"],

                texttemplate="%{text:,.0f}",

                textposition="outside",

                cliponaxis=False,

                showlegend=False,

                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Peak Daily Ridership: %{y:,.0f}"
                    "<extra></extra>"
                )

            )
        )


        fig.update_yaxes(
            title="Peak Daily Ridership",
            tickformat=",.0f"
        )


        fig = style_chart(
            fig,
            380
        )


        with st.container(border=True):

            st.plotly_chart(
                fig,
                width="stretch"
            )


except Exception as error:

    st.error(
        f"Unable to generate peak demand comparison: {error}"
    )


# ============================================================
# 18. RIDERSHIP CONTRIBUTION
# ============================================================

section_title(
    "Ridership Contribution",
    "Understand the percentage contribution of each metro line to network demand."
)


if line_performance is not None and not line_performance.empty:

    contribution_total = line_performance[
        "total_ridership"
    ].sum()


    fig = go.Figure(

        data=[

            go.Pie(

                labels=line_performance["line"],

                values=line_performance["total_ridership"],

                hole=0.68,

                marker=dict(

                    colors=[
                        LINE_COLORS.get(
                            line,
                            TEAL
                        )
                        for line in line_performance["line"]
                    ],

                    line=dict(
                        color="#ffffff",
                        width=3
                    )

                ),

                textinfo="label+percent",

                textposition="outside",

                textfont=dict(
                    color=TEXT_COLOR,
                    size=12
                ),

                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Ridership: %{value:,.0f}<br>"
                    "Contribution: %{percent}"
                    "<extra></extra>"
                )

            )

        ]

    )


    fig.update_layout(

        annotations=[

            dict(

                text=(
                    "<b>NETWORK</b><br>"
                    "<span style='font-size:12px'>"
                    "RIDERSHIP"
                    "</span>"
                ),

                x=0.5,
                y=0.5,

                showarrow=False,

                font=dict(
                    size=15,
                    color="#173f59"
                )

            )

        ]

    )


    fig = style_chart(
        fig,
        400
    )

    fig.update_layout(
        showlegend=False
    )


    with st.container(border=True):

        st.plotly_chart(
            fig,
            width="stretch"
        )


else:

    st.info(
        "No ridership contribution data is available."
    )


# ============================================================
# 19. LINE PERFORMANCE SUMMARY
# ============================================================

section_title(
    "Line Performance Summary",
    "Detailed comparison of passenger demand and line contribution."
)


if line_performance is not None and not line_performance.empty:

    display_data = line_performance.rename(

        columns={

            "line": "Metro Line",

            "total_ridership": "Total Ridership",

            "average_ridership": "Average Daily Ridership",

            "maximum_ridership": "Peak Daily Ridership",

            "operating_days": "Operating Days",

            "contribution_percent": "Contribution (%)"

        }

    ).copy()


    column_config = {

        "Total Ridership": st.column_config.NumberColumn(
            format="%d"
        ),

        "Average Daily Ridership": st.column_config.NumberColumn(
            format="%.0f"
        ),

        "Peak Daily Ridership": st.column_config.NumberColumn(
            format="%d"
        ),

        "Operating Days": st.column_config.NumberColumn(
            format="%d"
        ),

        "Contribution (%)": st.column_config.NumberColumn(
            format="%.2f%%"
        )

    }


    with st.container(border=True):

        st.dataframe(

            display_data,

            width="stretch",

            hide_index=True,

            column_config=column_config

        )


else:

    st.info(
        "No line performance records available."
    )


# ============================================================
# 20. LINE DATA EXPLORER
# ============================================================

section_title(
    "Line Data Explorer",
    "Inspect and export individual metro line records."
)


with st.expander(
    f"Explore {selected_line} Line Records",
    expanded=False
):

    st.caption(
        f"{len(line_df):,} records available for the selected line."
    )


    st.dataframe(

        line_df,

        width="stretch",

        hide_index=True

    )


    csv = line_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        label="Download Line Data",

        data=csv,

        file_name=f"{selected_line.lower()}_ridership.csv",

        mime="text/csv",

        width="content"

    )


# ============================================================
# 21. FOOTER
# ============================================================

st.divider()


st.markdown(
    """
    <div class="line-footer">

        METRO OPERATIONS ANALYTICS PLATFORM

        &nbsp; | &nbsp;

        LINE ANALYSIS

        &nbsp; | &nbsp;

        SYNTHETIC PROJECT DATA

    </div>
    """,
    unsafe_allow_html=True
)
