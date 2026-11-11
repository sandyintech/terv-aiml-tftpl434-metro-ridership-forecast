import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from pathlib import Path
import sys


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_PATH = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_PATH / "app"
OUTPUT_PATH = PROJECT_PATH / "outputs"

if str(APP_PATH) not in sys.path:
    sys.path.insert(0, str(APP_PATH))


# ============================================================
# 2. IMPORT PROJECT MODULES
# ============================================================

from components import setup_page
from utils import load_ridership_data, LINE_COLORS

# ============================================================
# 3. PAGE CONFIGURATION
# ============================================================

setup_page(
    title="Forecasting",
    active="Forecasting"
)


# ============================================================
# 4. PREMIUM WHITE THEME
# ============================================================

st.markdown("""
<style>

:root {
    color-scheme: light;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background:
        radial-gradient(circle at 5% 3%,
            rgba(0, 190, 200, 0.075), transparent 27%),
        radial-gradient(circle at 95% 8%,
            rgba(55, 125, 230, 0.065), transparent 28%),
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

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #edf5fa 100%)
        !important;
    border-right: 1px solid #dce8f1;
}

[data-testid="stSidebar"] * {
    color: #25465e !important;
}


/* PAGE HEADER */

.forecast-eyebrow {
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

.forecast-heading {
    font-size: 38px;
    font-weight: 850;
    color: #123b55 !important;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 9px;
    text-shadow: 0 3px 14px rgba(0, 170, 190, 0.10);
}

.forecast-subheading {
    color: #637f95 !important;
    font-size: 14px;
    line-height: 1.8;
    max-width: 950px;
    margin-bottom: 22px;
}


/* INFORMATION BANNER */

.forecast-note {
    background: linear-gradient(110deg, #ffffff 0%, #f0faff 100%);
    border: 1px solid #cfe7f0;
    border-left: 5px solid #00aeb5;
    border-radius: 13px;
    padding: 17px 20px;
    margin: 12px 0 24px 0;
    box-shadow: 0 4px 16px rgba(20, 90, 120, 0.055),
                0 0 12px rgba(0, 190, 200, 0.05);
}

.forecast-note-title {
    color: #087f86 !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 7px;
}

.forecast-note-content {
    color: #25465e !important;
    font-size: 13px;
    line-height: 1.7;
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
    background: linear-gradient(145deg, #ffffff 0%, #f5fbff 100%)
        !important;
    border: 1px solid rgba(0, 174, 190, 0.25);
    border-radius: 16px;
    padding: 19px 18px 16px 18px;
    min-height: 118px;
    box-shadow: 0 4px 16px rgba(25, 75, 110, 0.06),
                0 0 12px rgba(0, 190, 200, 0.055);
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #00b9bd;
    box-shadow: 0 8px 22px rgba(20, 100, 140, 0.11),
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


/* FILTER INPUTS */

div[data-baseweb="input"] {
    background: #ffffff !important;
    border: 1px solid #cbdce8 !important;
    border-radius: 9px !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #00aeb5 !important;
    box-shadow: 0 0 0 2px rgba(0, 190, 190, 0.12);
}

div[data-baseweb="input"] input {
    color: #25465e !important;
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


/* CONTENT CONTAINERS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #dce9f1;
    border-radius: 15px;
    box-shadow: 0 4px 16px rgba(30, 80, 110, 0.045);
}


/* INSIGHT CARDS */

.insight-card {
    background: linear-gradient(135deg, #ffffff, #f1faff);
    border: 1px solid #d9eaf2;
    border-left: 4px solid #00aeb5;
    border-radius: 12px;
    padding: 17px;
    min-height: 125px;
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
    font-size: 21px;
    font-weight: 800;
}

.insight-description {
    color: #71899d !important;
    font-size: 12px;
    margin-top: 6px;
}


```css
/* ----------------------------------------------------------
   BUTTONS
---------------------------------------------------------- */

.stButton button,
.stDownloadButton button {

    border-radius: 10px !important;

    border: 1px solid #009fa8 !important;

    background: linear-gradient(
        135deg,
        #087f83,
        #079eaa
    ) !important;

    color: #ffffff !important;

    font-weight: 700 !important;

    opacity: 1 !important;

    box-shadow:
        0 4px 12px rgba(0, 150, 160, 0.16);

    transition: all 0.25s ease;
}


/* Force button text to remain white */

.stButton button *,
.stDownloadButton button *,
.stButton button p,
.stDownloadButton button p,
.stButton button span,
.stDownloadButton button span {

    color: #ffffff !important;

    -webkit-text-fill-color: #ffffff !important;

    opacity: 1 !important;
}


/* Hover effect */

.stButton button:hover,
.stDownloadButton button:hover {

    background: linear-gradient(
        135deg,
        #056c78,
        #078b9b
    ) !important;

    border-color: #00c8c8 !important;

    box-shadow:
        0 0 16px rgba(0, 190, 190, 0.25);

    transform: translateY(-2px);
}
```


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


/* ALERTS */

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

.forecast-footer {
    color: #7893a7 !important;
    font-size: 11px;
    letter-spacing: 1px;
    text-align: center;
    padding: 16px 0;
}


@media (max-width: 768px) {
    .forecast-heading {
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
# 5. CHART THEME
# ============================================================

CHART_BG = "#ffffff"
PAPER_BG = "#ffffff"
TEXT_COLOR = "#25465e"
GRID_COLOR = "rgba(80, 120, 150, 0.14)"

TEAL = "#00aeb5"
BLUE = "#397fe8"
GREEN = "#16a477"
ORANGE = "#f59e42"


def style_chart(fig, height=400):

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
            l=50,
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
            font=dict(color="#19364d")
        )
    )

    return fig


# ============================================================
# 6. REUSABLE SECTION TITLE
# ============================================================

def section_title(title, description):

    st.markdown(
        f"""
        <div class="section-heading">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 7. REUSABLE INSIGHT CARD
# ============================================================

def insight_card(label, value, description=""):

    # Keep HTML compact so Streamlit does not render it as code.

    html = (
        f'<div class="insight-card">'
        f'<div class="insight-label">{label}</div>'
        f'<div class="insight-value">{value}</div>'
        f'<div class="insight-description">{description}</div>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# 8. PAGE HEADER
# ============================================================

st.markdown("""
<div class="forecast-eyebrow">
    MACHINE LEARNING | PREDICTIVE ANALYTICS
</div>

<div class="forecast-heading">
    Ridership Forecasting
</div>

<div class="forecast-subheading">
    Explore machine learning-based passenger demand predictions,
    network-level forecasting, metro line trends and prediction
    uncertainty across the forecast horizon.
</div>
""", unsafe_allow_html=True)


forecast_note_html = (
    '<div class="forecast-note">'
    '<div class="forecast-note-title">'
    'HISTORICAL DEMONSTRATION FORECAST'
    '</div>'
    '<div class="forecast-note-content">'
    '<b>Forecast Period:</b> July 1–28, 2025'
    '<br>'
    'This dashboard presents the historical demonstration '
    'forecast generated by the trained forecasting model. '
    'It is not a live 2026 forecast.'
    '<br>'
    '<b>Forecast Model:</b> LightGBM'
    '</div>'
    '</div>'
)

st.markdown(
    forecast_note_html,
    unsafe_allow_html=True
)


# ============================================================
# 9. LOAD FORECAST FILES
# ============================================================

@st.cache_data(show_spinner="Loading forecast data...")
def load_forecast_files():

    line_path = OUTPUT_PATH / "line_level_forecast.csv"
    network_path = OUTPUT_PATH / "network_forecast.csv"

    if not line_path.exists():
        raise FileNotFoundError(
            f"Line forecast file not found: {line_path}"
        )

    if not network_path.exists():
        raise FileNotFoundError(
            f"Network forecast file not found: {network_path}"
        )

    line_forecast = pd.read_csv(line_path)
    network_forecast = pd.read_csv(network_path)

    return line_forecast, network_forecast


try:

    df = load_ridership_data()
    forecast, network_forecast = load_forecast_files()

except Exception as error:

    st.error(f"Unable to load forecasting data: {error}")
    st.stop()


# ============================================================
# 10. INITIAL DATA CHECKS
# ============================================================

if df is None or df.empty:
    st.error("Historical ridership data is empty.")
    st.stop()

if forecast is None or forecast.empty:
    st.error("Line-level forecast data is empty.")
    st.stop()

if network_forecast is None or network_forecast.empty:
    st.error("Network-level forecast data is empty.")
    st.stop()


# ============================================================
# 11. DATA VALIDATION
# ============================================================

required_line_columns = {
    "date",
    "line",
    "predicted_ridership"
}

required_network_columns = {
    "date",
    "network_ridership",
    "lower_80",
    "upper_80"
}

required_actual_columns = {
    "date",
    "ridership"
}


if not required_line_columns.issubset(forecast.columns):

    missing = required_line_columns - set(forecast.columns)

    st.error(
        f"Line-level forecast is missing columns: {sorted(missing)}"
    )

    st.stop()


if not required_network_columns.issubset(network_forecast.columns):

    missing = required_network_columns - set(network_forecast.columns)

    st.error(
        f"Network-level forecast is missing columns: {sorted(missing)}"
    )

    st.stop()


if not required_actual_columns.issubset(df.columns):

    st.error(
        "Historical data must contain date and ridership columns."
    )

    st.stop()


# Convert dates

forecast["date"] = pd.to_datetime(
    forecast["date"],
    errors="coerce"
)

network_forecast["date"] = pd.to_datetime(
    network_forecast["date"],
    errors="coerce"
)

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)


# Convert numeric values

forecast["predicted_ridership"] = pd.to_numeric(
    forecast["predicted_ridership"],
    errors="coerce"
)

for column in [
    "network_ridership",
    "lower_80",
    "upper_80"
]:

    network_forecast[column] = pd.to_numeric(
        network_forecast[column],
        errors="coerce"
    )


df["ridership"] = pd.to_numeric(
    df["ridership"],
    errors="coerce"
)


# Remove invalid rows

forecast = forecast.dropna(
    subset=["date", "line", "predicted_ridership"]
).copy()

network_forecast = network_forecast.dropna(
    subset=[
        "date",
        "network_ridership",
        "lower_80",
        "upper_80"
    ]
).copy()

df = df.dropna(
    subset=["date", "ridership"]
).copy()


forecast["line"] = (
    forecast["line"]
    .astype(str)
    .str.strip()
)


forecast = forecast.sort_values(
    ["date", "line"]
).reset_index(drop=True)

network_forecast = network_forecast.sort_values(
    "date"
).reset_index(drop=True)

df = df.sort_values("date").reset_index(drop=True)


if forecast.empty or network_forecast.empty:
    st.error("No valid forecast records remain after validation.")
    st.stop()


# ============================================================
# 12. FORECAST PERIOD INFORMATION
# ============================================================

forecast_start = forecast["date"].min()
forecast_end = forecast["date"].max()

historical_start = df["date"].min()
historical_end = df["date"].max()


available_lines = [
    line for line in LINE_COLORS
    if line in forecast["line"].unique()
]

for line in forecast["line"].unique():

    if line not in available_lines:
        available_lines.append(line)


if not available_lines:
    st.error("No valid metro lines were found.")
    st.stop()


# ============================================================
# 13. FORECAST FILTERS
# ============================================================

section_title(
    "Forecast Filters",
    "Select metro lines and forecast dates to explore predicted demand."
)


with st.container(border=True):

    filter_col1, filter_col2 = st.columns([1.2, 1])

    with filter_col1:

        selected_lines = st.multiselect(
            "Select Metro Lines",
            options=available_lines,
            default=available_lines,
            key="forecast_selected_lines"
        )

    with filter_col2:

        selected_dates = st.date_input(
            "Select Forecast Period",
            value=(
                forecast_start.date(),
                forecast_end.date()
            ),
            min_value=forecast_start.date(),
            max_value=forecast_end.date(),
            key="forecast_selected_dates"
        )


if not selected_lines:
    st.warning("Please select at least one metro line.")
    st.stop()


if isinstance(selected_dates, (tuple, list)):

    if len(selected_dates) == 0:
        st.warning("Select a valid forecast date range.")
        st.stop()

    start_date = selected_dates[0]

    end_date = (
        selected_dates[1]
        if len(selected_dates) > 1
        else selected_dates[0]
    )

else:

    start_date = selected_dates
    end_date = selected_dates


if start_date > end_date:
    st.warning("Start date cannot be later than end date.")
    st.stop()


# ============================================================
# 14. FILTER FORECAST DATA
# ============================================================

start_timestamp = pd.Timestamp(start_date)

end_timestamp = (
    pd.Timestamp(end_date)
    + pd.Timedelta(days=1)
    - pd.Timedelta(seconds=1)
)


filtered_forecast = forecast.loc[
    forecast["line"].isin(selected_lines)
    & forecast["date"].between(
        start_timestamp,
        end_timestamp
    )
].copy()


# Network forecast always represents the complete network.

filtered_network = network_forecast.loc[
    network_forecast["date"].between(
        start_timestamp,
        end_timestamp
    )
].copy()


if filtered_forecast.empty:
    st.warning(
        "No line-level forecast data is available for the selected filters."
    )
    st.stop()


if filtered_network.empty:
    st.warning(
        "No network-level forecast data is available for the selected dates."
    )
    st.stop()


# ============================================================
# 15. FORECAST SUMMARY KPIs
# ============================================================

section_title(
    "Forecast Overview",
    "Summary of predicted passenger demand for the selected forecast period."
)


total_forecast = filtered_forecast[
    "predicted_ridership"
].sum()

average_daily_forecast = filtered_network[
    "network_ridership"
].mean()

peak_forecast = filtered_network[
    "network_ridership"
].max()

forecast_days = filtered_network[
    "date"
].nunique()

peak_network_record = filtered_network.loc[
    filtered_network["network_ridership"].idxmax()
]


k1, k2, k3, k4 = st.columns(4)


with k1:
    st.metric(
        "Selected Line Forecast",
        f"{total_forecast:,.0f}"
    )

with k2:
    st.metric(
        "Average Network Demand",
        f"{average_daily_forecast:,.0f}"
    )

with k3:
    st.metric(
        "Peak Network Forecast",
        f"{peak_forecast:,.0f}"
    )

with k4:
    st.metric(
        "Forecast Duration",
        f"{forecast_days} Days"
    )


st.caption(
    "Selected Line Forecast reflects only the lines chosen above. "
    "Network KPIs represent the complete metro network, regardless "
    "of the selected line filter."
)


# ============================================================
# 16. NETWORK-LEVEL FORECAST
# ============================================================

section_title(
    "Network-Level Ridership Forecast",
    "Predicted total network demand with the 80% prediction interval."
)


fig = go.Figure()


# Lower interval

fig.add_trace(
    go.Scatter(
        x=filtered_network["date"],
        y=filtered_network["lower_80"],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
        name="Lower 80%"
    )
)


# Upper interval fills down to lower interval

fig.add_trace(
    go.Scatter(
        x=filtered_network["date"],
        y=filtered_network["upper_80"],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(57, 127, 232, 0.13)",
        name="80% Prediction Interval",
        hovertemplate=(
            "<b>%{x|%d %B %Y}</b><br>"
            "Upper Bound: %{y:,.0f}"
            "<extra></extra>"
        )
    )
)


# Network forecast

fig.add_trace(
    go.Scatter(
        x=filtered_network["date"],
        y=filtered_network["network_ridership"],
        mode="lines+markers",
        name="Predicted Network Ridership",
        line=dict(
            color=BLUE,
            width=3.2
        ),
        marker=dict(
            size=7,
            color=BLUE
        ),
        hovertemplate=(
            "<b>%{x|%d %B %Y}</b><br>"
            "Predicted Ridership: %{y:,.0f}"
            "<extra></extra>"
        )
    )
)


fig.update_layout(
    title=dict(
        text="Daily Network Ridership Prediction",
        x=0.02,
        font=dict(size=16, color="#173f59")
    ),
    yaxis_title="Passenger Count",
    xaxis_title="Forecast Date"
)

style_chart(fig, height=430)

st.plotly_chart(
    fig,
    width="stretch",
    key="network_forecast_chart"
)


# ============================================================
# 17. NETWORK FORECAST INSIGHTS
# ============================================================

interval_width = (
    filtered_network["upper_80"]
    - filtered_network["lower_80"]
).mean()

average_lower = filtered_network["lower_80"].mean()
average_upper = filtered_network["upper_80"].mean()

insight_col1, insight_col2, insight_col3 = st.columns(3)


with insight_col1:

    insight_card(
        "PEAK NETWORK DEMAND",
        f"{peak_forecast:,.0f}",
        peak_network_record["date"].strftime("%d %B %Y")
    )


with insight_col2:

    insight_card(
        "AVERAGE DAILY DEMAND",
        f"{average_daily_forecast:,.0f}",
        "Predicted network passenger count"
    )


with insight_col3:

    insight_card(
        "AVERAGE INTERVAL WIDTH",
        f"{interval_width:,.0f}",
        "Average distance between upper and lower bounds"
    )


# ============================================================
# 18. LINE-LEVEL FORECAST
# ============================================================

section_title(
    "Metro Line Forecast",
    "Compare predicted passenger demand across the selected metro lines."
)


fig_line = go.Figure()


for line in selected_lines:

    line_data = filtered_forecast.loc[
        filtered_forecast["line"] == line
    ].sort_values("date")

    if line_data.empty:
        continue

    line_color = LINE_COLORS.get(line, BLUE)

    fig_line.add_trace(
        go.Scatter(
            x=line_data["date"],
            y=line_data["predicted_ridership"],
            mode="lines+markers",
            name=line,
            line=dict(
                color=line_color,
                width=2.8
            ),
            marker=dict(
                size=5
            ),
            hovertemplate=(
                "<b>%{x|%d %B %Y}</b><br>"
                f"{line}: " + "%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )


fig_line.update_layout(
    title=dict(
        text="Daily Ridership Forecast by Metro Line",
        x=0.02,
        font=dict(size=16, color="#173f59")
    ),
    xaxis_title="Forecast Date",
    yaxis_title="Predicted Passenger Count"
)

style_chart(fig_line, height=430)

st.plotly_chart(
    fig_line,
    width="stretch",
    key="line_forecast_chart"
)


# ============================================================
# 19. LINE-WISE FORECAST SUMMARY
# ============================================================

section_title(
    "Line-Wise Forecast Summary",
    "Compare total and average predicted demand for each selected metro line."
)


line_summary = (
    filtered_forecast
    .groupby("line")
    .agg(
        Total_Forecast=("predicted_ridership", "sum"),
        Average_Daily=("predicted_ridership", "mean"),
        Peak_Daily=("predicted_ridership", "max"),
        Forecast_Days=("date", "nunique")
    )
    .reset_index()
)


line_summary = line_summary.sort_values(
    "Total_Forecast",
    ascending=False
)


fig_summary = px.bar(
    line_summary,
    x="line",
    y="Total_Forecast",
    color="line",
    color_discrete_map=LINE_COLORS,
    text="Total_Forecast"
)


fig_summary.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside",
    marker_line_width=0
)


fig_summary.update_layout(
    title=dict(
        text="Total Predicted Ridership by Metro Line",
        x=0.02,
        font=dict(size=16, color="#173f59")
    ),
    xaxis_title="Metro Line",
    yaxis_title="Total Predicted Passengers",
    showlegend=False
)


style_chart(fig_summary, height=380)

st.plotly_chart(
    fig_summary,
    width="stretch",
    key="line_summary_chart"
)


display_summary = line_summary.copy()

display_summary["Total_Forecast"] = (
    display_summary["Total_Forecast"].round(0)
)

display_summary["Average_Daily"] = (
    display_summary["Average_Daily"].round(0)
)

display_summary["Peak_Daily"] = (
    display_summary["Peak_Daily"].round(0)
)


st.dataframe(
    display_summary,
    width="stretch",
    hide_index=True,
    column_config={
        "line": st.column_config.TextColumn("Metro Line"),
        "Total_Forecast": st.column_config.NumberColumn(
            "Total Forecast",
            format="localized"
        ),
        "Average_Daily": st.column_config.NumberColumn(
            "Average Daily",
            format="localized"
        ),
        "Peak_Daily": st.column_config.NumberColumn(
            "Peak Daily",
            format="localized"
        ),
        "Forecast_Days": st.column_config.NumberColumn(
            "Forecast Days",
            format="%d"
        )
    }
)


# ============================================================
# 20. HISTORICAL VS FORECAST COMPARISON
# ============================================================

section_title(
    "Historical vs Forecast Comparison",
    "View recent historical passenger demand alongside predicted network demand."
)


# Aggregate historical ridership by date.
# This also handles data containing multiple line records per day.

historical_daily = (
    df.groupby("date", as_index=False)
    .agg(
        actual_ridership=("ridership", "sum")
    )
    .sort_values("date")
)


# Show recent historical period before the forecast.

historical_display = historical_daily.loc[
    historical_daily["date"] < filtered_network["date"].min()
].tail(90)


comparison_fig = go.Figure()


if not historical_display.empty:

    comparison_fig.add_trace(
        go.Scatter(
            x=historical_display["date"],
            y=historical_display["actual_ridership"],
            mode="lines",
            name="Historical Ridership",
            line=dict(
                color=GREEN,
                width=2.5
            ),
            hovertemplate=(
                "<b>%{x|%d %B %Y}</b><br>"
                "Actual Ridership: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )


comparison_fig.add_trace(
    go.Scatter(
        x=filtered_network["date"],
        y=filtered_network["network_ridership"],
        mode="lines+markers",
        name="Forecast Ridership",
        line=dict(
            color=BLUE,
            width=3
        ),
        marker=dict(size=6),
        hovertemplate=(
            "<b>%{x|%d %B %Y}</b><br>"
            "Forecast Ridership: %{y:,.0f}"
            "<extra></extra>"
        )
    )
)


comparison_fig.update_layout(
    title=dict(
        text="Historical Demand and Forecast",
        x=0.02,
        font=dict(size=16, color="#173f59")
    ),
    xaxis_title="Date",
    yaxis_title="Passenger Count"
)


style_chart(comparison_fig, height=420)


st.plotly_chart(
    comparison_fig,
    width="stretch",
    key="historical_forecast_comparison"
)


if historical_display.empty:

    st.info(
        "No historical records were available before the selected forecast period."
    )

else:

    st.caption(
        f"Historical comparison uses the latest "
        f"{len(historical_display)} available days before the forecast period."
    )


# ============================================================
# 21. FORECAST DATA EXPLORER
# ============================================================

section_title(
    "Forecast Data Explorer",
    "Inspect the detailed predicted passenger counts and network prediction intervals."
)


with st.expander(
    "View Detailed Line-Level Forecast Records",
    expanded=False
):

    display_forecast = filtered_forecast.copy()

    display_forecast["date"] = (
        display_forecast["date"].dt.strftime("%d %b %Y")
    )

    display_forecast = display_forecast.rename(
        columns={
            "date": "Forecast Date",
            "line": "Metro Line",
            "predicted_ridership": "Predicted Ridership"
        }
    )

    st.dataframe(
        display_forecast,
        width="stretch",
        hide_index=True
    )


with st.expander(
    "View Network Forecast and Prediction Intervals",
    expanded=False
):

    display_network = filtered_network.copy()

    display_network["date"] = (
        display_network["date"].dt.strftime("%d %b %Y")
    )

    display_network = display_network.rename(
        columns={
            "date": "Forecast Date",
            "network_ridership": "Network Ridership",
            "lower_80": "Lower 80% Bound",
            "upper_80": "Upper 80% Bound"
        }
    )

    st.dataframe(
        display_network,
        width="stretch",
        hide_index=True
    )


# ============================================================
# 22. DOWNLOAD FORECAST DATA
# ============================================================

section_title(
    "Download Forecast Results",
    "Export the filtered forecast records for further analysis."
)


download_col1, download_col2 = st.columns(2)


with download_col1:

    line_csv = filtered_forecast.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Line Forecast CSV",
        data=line_csv,
        file_name="metro_line_forecast.csv",
        mime="text/csv",
        width="stretch"
    )


with download_col2:

    network_csv = filtered_network.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Network Forecast CSV",
        data=network_csv,
        file_name="metro_network_forecast.csv",
        mime="text/csv",
        width="stretch"
    )


# ============================================================
# 23. FOOTER
# ============================================================

st.markdown("""
<hr>

<div class="forecast-footer">
    METRO OPERATIONS ANALYTICS PLATFORM
    &nbsp; | &nbsp;
    MACHINE LEARNING FORECASTING
</div>
""", unsafe_allow_html=True)