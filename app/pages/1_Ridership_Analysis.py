import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from textwrap import dedent

from components import setup_page

from utils import (
    LINE_ORDER,
    LINE_COLORS,
    load_ridership_data,
    fmt_number
)

from calculations import (
    calculate_network_kpis,
    calculate_daily_network,
    calculate_moving_average,
    calculate_line_performance,
    calculate_weekday_performance,
    calculate_monthly_ridership,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

setup_page(
    title="Ridership Analysis",
    active="Ridership Analysis"
)


# ============================================================
# PREMIUM LIGHT THEME
# ============================================================

st.markdown("""
<style>

:root {
    color-scheme: light;
}

/* MAIN BACKGROUND */

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


/* SIDEBAR */

[data-testid="stSidebarNav"] {
    display: none !important;
}

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


/* PAGE HEADER */

.ridership-eyebrow {
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

.ridership-heading {
    font-size: 38px;
    font-weight: 850;
    color: #123b55 !important;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 9px;
    text-shadow: 0 3px 14px rgba(0, 170, 190, 0.10);
}

.ridership-subheading {
    color: #637f95 !important;
    font-size: 14px;
    line-height: 1.8;
    max-width: 850px;
    margin-bottom: 25px;
}


/* SECTION HEADINGS */

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


/* GENERAL TEXT */

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


/* KPI CARDS */

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


/* FILTER INPUTS */

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

div[data-baseweb="select"] span[data-baseweb="tag"] {
    background: #087f83 !important;
    border: 1px solid #00b9b5 !important;
    border-radius: 7px !important;
}

div[data-baseweb="select"] span[data-baseweb="tag"] * {
    color: #ffffff !important;
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


/* CHART AND CONTENT CARDS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #dce9f1;
    border-radius: 15px;
    box-shadow: 0 4px 16px rgba(30, 80, 110, 0.045);
}


/* INSIGHT CARDS */

.insight-card {
    background: linear-gradient(
        135deg,
        #ffffff,
        #f1faff
    );

    border: 1px solid #d9eaf2;
    border-left: 4px solid #00aeb5;
    border-radius: 12px;
    padding: 20px;
    min-height: 145px;

    box-shadow:
        0 3px 12px rgba(30, 80, 110, 0.045),
        0 0 12px rgba(0, 174, 181, 0.05);

    transition: all 0.25s ease;
}

.insight-card:hover {
    transform: translateY(-3px);
    border-color: #9adce0;

    box-shadow:
        0 8px 20px rgba(0, 150, 170, 0.10);
}

.insight-label {
    color: #7890a3 !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.1px;
    margin-bottom: 12px;
}

.insight-value {
    color: #173f59 !important;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.3;
}

.insight-description {
    color: #71899d !important;
    font-size: 13px;
    margin-top: 9px;
}


/* BUTTONS */

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


/* DATAFRAME */

div[data-testid="stDataFrame"] {
    background: #ffffff !important;
    border: 1px solid #d8e6ef;
    border-radius: 10px;
    overflow: hidden;
}


/* EXPANDER */

[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #d8e6ef !important;
    border-radius: 12px !important;
    box-shadow: 0 3px 12px rgba(30, 80, 110, 0.04);
}

[data-testid="stExpander"] summary {
    color: #25465e !important;
}


/* ALERTS AND DIVIDERS */

[data-testid="stAlert"] {
    background: #ffffff !important;
    color: #25465e !important;
    border-radius: 10px;
    border: 1px solid #dce8f0;
}

hr {
    border-color: #dce8f0 !important;
}


/* FOOTER */

.ridership-footer {
    color: #7893a7 !important;
    font-size: 11px;
    letter-spacing: 1px;
    text-align: center;
    padding: 16px 0;
}


/* RESPONSIVE */

@media (max-width: 768px) {

    .ridership-heading {
        font-size: 29px;
    }

    .section-heading {
        font-size: 19px;
    }

    div[data-testid="stMetric"] {
        padding: 14px;
    }

    .insight-value {
        font-size: 23px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CHART THEME
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

        hovermode="x unified",

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
# REUSABLE SECTION TITLE
# ============================================================

def section_title(title, description):

    html = dedent(f"""
        <div class="section-heading">
            {title}
        </div>

        <div class="section-description">
            {description}
        </div>
    """).strip()

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# REUSABLE INSIGHT CARD
# ============================================================

def insight_card(label, value, description=""):

    html = dedent(f"""
        <div class="insight-card">

            <div class="insight-label">
                {label}
            </div>

            <div class="insight-value">
                {value}
            </div>

            <div class="insight-description">
                {description}
            </div>

        </div>
    """).strip()

    # st.html renders HTML directly. This avoids Streamlit treating the
    # markup as a code block in environments where markdown parsing differs.
    st.html(html)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    dedent("""
        <div class="ridership-eyebrow">
            METRO OPERATIONS ANALYTICS
        </div>

        <div class="ridership-heading">
            Ridership Analysis
        </div>

        <div class="ridership-subheading">
            Explore passenger demand, network behaviour,
            monthly trends and metro line contribution.
            Understand how ridership changes across time
            and across the metro network.
        </div>
    """).strip(),
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(show_spinner="Loading ridership data...")
def get_data():

    return load_ridership_data()


try:

    df = get_data()

except Exception as error:

    st.error(
        f"Unable to load ridership data: {error}"
    )

    st.stop()


if df is None or df.empty:

    st.warning("No ridership data is available.")

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

df = df.copy()

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
        "No valid ridership records remain after data preparation."
    )

    st.stop()


if not pd.api.types.is_numeric_dtype(df["ridership"]):

    st.error("Ridership values must be numeric.")

    st.stop()

if not df["ridership"].map(
    lambda value: pd.notna(value) and abs(value) != float("inf")
).all():

    st.error("Ridership contains invalid infinite values.")

    st.stop()

if (df["ridership"] < 0).any():

    st.error("Negative ridership values were detected.")

    st.stop()


# ============================================================
# ANALYSIS FILTERS
# ============================================================

section_title(
    "Analysis Filters",
    "Choose your analysis period and the metro lines to include."
)

with st.container(border=True):

    filter_col1, filter_col2 = st.columns([2, 2])

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    with filter_col1:

        selected_dates = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    with filter_col2:

        available_lines = [
            line for line in LINE_ORDER
            if line in df["line"].unique()
        ]

        selected_lines = st.multiselect(
            "Select metro lines",
            options=available_lines,
            default=available_lines
        )


# ============================================================
# DATE VALIDATION
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


if not selected_lines:

    st.warning(
        "Select at least one metro line."
    )

    st.stop()


# ============================================================
# FILTERED DATA
# ============================================================

filtered_df = df.loc[

    (df["date"].dt.date >= start_date)
    &
    (df["date"].dt.date <= end_date)
    &
    (df["line"].isin(selected_lines))

].copy()


if filtered_df.empty:

    st.warning(
        "No records found for the selected filters."
    )

    st.stop()


# ============================================================
# FILTER SUMMARY
# ============================================================

period_days = (
    pd.Timestamp(end_date) -
    pd.Timestamp(start_date)
).days + 1

st.caption(
    f"Showing {len(filtered_df):,} records "
    f"from {start_date.strftime('%d %b %Y')} "
    f"to {end_date.strftime('%d %b %Y')} "
    f"across {len(selected_lines)} selected metro line(s)."
)


# ============================================================
# NETWORK OVERVIEW
# ============================================================

section_title(
    "Network Overview",
    "Key ridership indicators for the selected analysis period."
)

try:

    kpis = calculate_network_kpis(
        filtered_df
    )

except Exception as error:

    st.error(
        f"Unable to calculate network KPIs: {error}"
    )

    st.stop()


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Total Ridership",
        fmt_number(kpis["total_ridership"])
    )


with kpi2:

    st.metric(
        "Average Daily Ridership",
        fmt_number(kpis["average_daily_ridership"])
    )


with kpi3:

    st.metric(
        "Peak Daily Ridership",
        fmt_number(kpis["peak_ridership"])
    )


with kpi4:

    st.metric(
        "Operating Line-Days",
        fmt_number(kpis["operating_line_days"])
    )


if kpis.get("peak_day") is not None:

    peak_date = pd.to_datetime(
        kpis["peak_day"]
    ).strftime("%d %B %Y")

    st.caption(
        f"Peak network demand was recorded on {peak_date}."
    )


# ============================================================
# DAILY RIDERSHIP TREND
# ============================================================

section_title(
    "Daily Ridership Trend",
    "Track daily passenger demand and identify the underlying trend."
)

try:

    daily_network = calculate_daily_network(
        filtered_df
    )

    if daily_network is None or daily_network.empty:

        st.info(
            "Daily ridership information is unavailable."
        )

    else:

        daily_network = calculate_moving_average(
            daily_network,
            window=7
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=daily_network["date"],
                y=daily_network["network_ridership"],
                mode="lines",
                name="Daily Ridership",
                line=dict(
                    color=TEAL,
                    width=1.5
                ),
                fill="tozeroy",
                fillcolor="rgba(0, 174, 181, 0.09)",
                opacity=0.9
            )
        )

        fig.add_trace(
            go.Scatter(
                x=daily_network["date"],
                y=daily_network["moving_average"],
                mode="lines",
                name="7-Day Moving Average",
                line=dict(
                    color=BLUE,
                    width=3.2,
                    shape="spline"
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
            430
        )

        with st.container(border=True):

            st.plotly_chart(
                fig,
                width="stretch"
            )

        # DAILY TREND INSIGHTS

        valid_daily = daily_network.dropna(
            subset=["network_ridership"]
        )

        if not valid_daily.empty:

            highest_day = valid_daily.loc[
                valid_daily["network_ridership"].idxmax()
            ]

            lowest_day = valid_daily.loc[
                valid_daily["network_ridership"].idxmin()
            ]

            insight_col1, insight_col2 = st.columns(2)

            with insight_col1:

                insight_card(
                    "HIGHEST DAILY DEMAND",
                    fmt_number(highest_day["network_ridership"]),
                    pd.to_datetime(
                        highest_day["date"]
                    ).strftime("%d %B %Y")
                )

            with insight_col2:

                insight_card(
                    "LOWEST DAILY DEMAND",
                    fmt_number(lowest_day["network_ridership"]),
                    pd.to_datetime(
                        lowest_day["date"]
                    ).strftime("%d %B %Y")
                )


except Exception as error:

    st.error(
        f"Unable to generate daily ridership chart: {error}"
    )


# ============================================================
# MONTHLY RIDERSHIP
# ============================================================

section_title(
    "Monthly Ridership",
    "Compare passenger demand across months and metro lines."
)

try:

    monthly_data = calculate_monthly_ridership(
        filtered_df
    )

    if monthly_data is None or monthly_data.empty:

        st.info(
            "Monthly ridership information is unavailable."
        )

    else:

        fig = px.bar(
            monthly_data,
            x="month",
            y="ridership",
            color="line",
            color_discrete_map=LINE_COLORS,
            barmode="group",
            custom_data=["line"]
        )

        fig.update_traces(
            marker_line_width=0,
            opacity=0.90,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Month: %{x|%B %Y}<br>"
                "Ridership: %{y:,.0f}"
                "<extra></extra>"
            )
        )

        fig.update_xaxes(
            tickformat="%b\n%Y",
            dtick="M2"
        )

        fig.update_yaxes(
            title="Total Passengers",
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
        f"Unable to generate monthly ridership chart: {error}"
    )


# ============================================================
# WEEKDAY DEMAND ANALYSIS
# ============================================================

section_title(
    "Weekday Demand Pattern",
    "Understand how average passenger demand changes throughout the week."
)

try:

    weekday_data = calculate_weekday_performance(
        filtered_df
    )

    if weekday_data is None or weekday_data.empty:

        st.info(
            "Weekday performance information is unavailable."
        )

    else:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=weekday_data["weekday"],
                y=weekday_data["average_ridership"],
                marker=dict(
                    color=weekday_data["average_ridership"],
                    colorscale=[
                        [0, "#176b87"],
                        [0.5, "#00aeb7"],
                        [1, "#00d4c4"]
                    ],
                    line=dict(
                        width=0
                    )
                ),
                text=weekday_data["average_ridership"],
                texttemplate="%{text:,.0f}",
                textposition="outside",
                cliponaxis=False,
                name="Average Ridership",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Average Ridership: %{y:,.0f}"
                    "<extra></extra>"
                )
            )
        )

        fig.update_yaxes(
            title="Average Passenger Count",
            tickformat=",.0f"
        )

        fig = style_chart(
            fig,
            380
        )

        fig.update_layout(
            showlegend=False
        )

        with st.container(border=True):

            st.plotly_chart(
                fig,
                width="stretch"
            )

        valid_weekdays = weekday_data.dropna(
            subset=["average_ridership"]
        )

        if not valid_weekdays.empty:

            busiest_day = valid_weekdays.loc[
                valid_weekdays["average_ridership"].idxmax()
            ]

            quietest_day = valid_weekdays.loc[
                valid_weekdays["average_ridership"].idxmin()
            ]

            insight1, insight2 = st.columns(2)

            with insight1:

                insight_card(
                    "BUSIEST WEEKDAY",
                    str(busiest_day["weekday"]),
                    f"Average demand: {fmt_number(busiest_day['average_ridership'])}"
                )

            with insight2:

                insight_card(
                    "QUIETEST WEEKDAY",
                    str(quietest_day["weekday"]),
                    f"Average demand: {fmt_number(quietest_day['average_ridership'])}"
                )


except Exception as error:

    st.error(
        f"Unable to generate weekday analysis: {error}"
    )


# ============================================================
# METRO LINE CONTRIBUTION
# ============================================================

section_title(
    "Metro Line Contribution",
    "Understand how much each selected line contributes to total passenger demand."
)

line_performance = None

try:

    line_performance = calculate_line_performance(
        filtered_df
    )

    if line_performance is None or line_performance.empty:

        st.info(
            "Line performance information is unavailable."
        )

    else:

        col1, col2 = st.columns(2)

        # DONUT CHART

        with col1:

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

                        font=dict(
                            size=15,
                            color="#173f59"
                        ),

                        showarrow=False

                    )

                ]

            )

            fig = style_chart(
                fig,
                390
            )

            fig.update_layout(
                showlegend=False
            )

            with st.container(border=True):

                st.markdown(
                    "**Ridership Share**"
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )


        # LINE COMPARISON BAR CHART

        with col2:

            fig = go.Figure()

            fig.add_trace(

                go.Bar(

                    x=line_performance["line"],

                    y=line_performance["total_ridership"],

                    marker=dict(

                        color=[
                            LINE_COLORS.get(
                                line,
                                TEAL
                            )
                            for line in line_performance["line"]
                        ],

                        line=dict(
                            color="#ffffff",
                            width=1
                        )

                    ),

                    text=line_performance["total_ridership"],

                    texttemplate="%{text:,.0f}",

                    textposition="outside",

                    cliponaxis=False,

                    showlegend=False,

                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Total Ridership: %{y:,.0f}"
                        "<extra></extra>"
                    )

                )

            )

            fig.update_yaxes(
                title="Total Ridership",
                tickformat=",.0f"
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


except Exception as error:

    st.error(
        f"Unable to generate line contribution charts: {error}"
    )


# ============================================================
# DETAILED LINE PERFORMANCE
# ============================================================

section_title(
    "Detailed Line Performance",
    "Compare total, average and peak passenger demand across metro lines."
)


if line_performance is not None and not line_performance.empty:

    display_performance = line_performance.copy()

    display_performance = display_performance.rename(

        columns={

            "line": "Metro Line",

            "total_ridership": "Total Ridership",

            "average_ridership": "Average Ridership",

            "maximum_ridership": "Maximum Ridership",

            "operating_days": "Operating Days",

            "contribution_percent": "Contribution (%)"

        }

    )

    column_config = {

        "Total Ridership": st.column_config.NumberColumn(
            format="%d"
        ),

        "Average Ridership": st.column_config.NumberColumn(
            format="%.0f"
        ),

        "Maximum Ridership": st.column_config.NumberColumn(
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
            display_performance,
            width="stretch",
            hide_index=True,
            column_config=column_config
        )

else:

    st.info(
        "No line performance records available."
    )


# ============================================================
# DATA EXPLORER
# ============================================================

section_title(
    "Ridership Data Explorer",
    "Inspect the filtered dataset and export selected records."
)

with st.expander(
    "Explore filtered ridership records",
    expanded=False
):

    st.caption(
        f"{len(filtered_df):,} records available for the selected filters."
    )

    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True
    )

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="Download Filtered Data",

        data=csv,

        file_name="metro_filtered_ridership.csv",

        mime="text/csv",

        width="content"

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    dedent("""
        <div class="ridership-footer">
            METRO OPERATIONS ANALYTICS PLATFORM
            &nbsp; | &nbsp;
            RIDERSHIP ANALYSIS
            &nbsp; | &nbsp;
            SYNTHETIC PROJECT DATA
        </div>
    """).strip(),
    unsafe_allow_html=True
)