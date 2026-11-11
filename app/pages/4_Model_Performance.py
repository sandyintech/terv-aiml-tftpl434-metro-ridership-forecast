import streamlit as st
import pandas as pd
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


# ============================================================
# 3. PAGE CONFIGURATION
# ============================================================

setup_page(
    title="Model Performance",
    active="Model Performance"
)


# ============================================================
# 4. PREMIUM WHITE THEME
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

.performance-eyebrow {

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


.performance-heading {

    font-size: 38px;

    font-weight: 850;

    color: #123b55 !important;

    letter-spacing: -1.2px;

    line-height: 1.15;

    margin-bottom: 9px;

    text-shadow:
        0 3px 14px rgba(0, 170, 190, 0.10);
}


.performance-subheading {

    color: #637f95 !important;

    font-size: 14px;

    line-height: 1.8;

    max-width: 950px;

    margin-bottom: 22px;
}


/* ----------------------------------------------------------
   INFORMATION BANNER
---------------------------------------------------------- */

.performance-note {

    background: linear-gradient(
        110deg,
        #ffffff 0%,
        #f0faff 100%
    );

    border: 1px solid #cfe7f0;

    border-left: 5px solid #00aeb5;

    border-radius: 13px;

    padding: 17px 20px;

    margin: 12px 0 24px 0;

    box-shadow:
        0 4px 16px rgba(20, 90, 120, 0.055),
        0 0 12px rgba(0, 190, 200, 0.05);
}


.performance-note-title {

    color: #087f86 !important;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1px;

    margin-bottom: 7px;
}


.performance-note-content {

    color: #25465e !important;

    font-size: 13px;

    line-height: 1.7;
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
        0 0 12px rgba(0, 190, 200, 0.055);

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

    font-size: 25px !important;

    font-weight: 800 !important;
}


/* ----------------------------------------------------------
   FILTER INPUTS
---------------------------------------------------------- */

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

.performance-footer {

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

    .performance-heading {
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

BLUE = "#397fe8"

TEAL = "#00aeb5"

GREEN = "#16a477"

ORANGE = "#f59e42"

RED = "#e56b6f"

CHART_BG = "#ffffff"

TEXT_COLOR = "#25465e"

GRID_COLOR = "rgba(80, 120, 150, 0.14)"


def style_chart(fig, height=400):

    fig.update_layout(

        height=height,

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            color=TEXT_COLOR,
            size=12
        ),

        margin=dict(
            l=50,
            r=30,
            t=60,
            b=55
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
# 6. REUSABLE SECTION TITLE
# ============================================================

def section_title(title, description):

    html = (
        f'<div class="section-heading">{title}</div>'
        f'<div class="section-description">{description}</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# 7. REUSABLE INSIGHT CARD
# ============================================================

def insight_card(label, value, description=""):

    html = (
        f'<div class="insight-card">'
        f'<div class="insight-label">{label}</div>'
        f'<div class="insight-value">{value}</div>'
        f'<div class="insight-description">{description}</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# 8. PAGE HEADER
# ============================================================

st.markdown("""
<div class="performance-eyebrow">
    MACHINE LEARNING | MODEL EVALUATION
</div>

<div class="performance-heading">
    Model Performance
</div>

<div class="performance-subheading">
    Evaluate forecasting models using validation metrics,
    compare prediction errors, examine LightGBM tuning results
    and identify the most reliable forecasting approach.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 9. INFORMATION BANNER
# ============================================================

note_html = (
    '<div class="performance-note">'
    '<div class="performance-note-title">'
    'MODEL EVALUATION OVERVIEW'
    '</div>'
    '<div class="performance-note-content">'
    'Results are based on the synthetic metro ridership dataset. '
    'They demonstrate model performance on this project dataset '
    'and should not be interpreted as actual metro operational results.'
    '<br>'
    '<b>Evaluation Metrics:</b> MAE, RMSE and MAPE'
    '<br>'
    '<b>Validation:</b> Rolling-origin validation and final holdout testing'
    '</div>'
    '</div>'
)

st.markdown(
    note_html,
    unsafe_allow_html=True
)


# ============================================================
# 10. LOAD RESULTS
# ============================================================

@st.cache_data(show_spinner="Loading model evaluation results...")
def load_results():

    metrics_path = OUTPUT_PATH / "final_metrics.csv"

    tuning_path = OUTPUT_PATH / "lightgbm_tuning_results.csv"

    if not metrics_path.exists():

        raise FileNotFoundError(
            f"Metrics file not found: {metrics_path}"
        )

    metrics = pd.read_csv(metrics_path)

    tuning = None

    if tuning_path.exists():

        tuning = pd.read_csv(tuning_path)

    return metrics, tuning


try:

    metrics_df, tuning_df = load_results()

except Exception as error:

    st.error(
        f"Unable to load model evaluation results: {error}"
    )

    st.stop()


if metrics_df is None or metrics_df.empty:

    st.error(
        "The model metrics file is empty."
    )

    st.stop()


# ============================================================
# 11. STANDARDIZE AND VALIDATE COLUMNS
# ============================================================

metrics_df.columns = (
    metrics_df.columns
    .str.strip()
    .str.lower()
)


required_columns = [
    "model",
    "mae",
    "rmse",
    "mape"
]


missing_columns = [
    col
    for col in required_columns
    if col not in metrics_df.columns
]


if missing_columns:

    st.error(
        f"Missing required metrics columns: {missing_columns}"
    )

    st.write(
        "Available columns:",
        metrics_df.columns.tolist()
    )

    st.stop()


metrics_df["model"] = (
    metrics_df["model"]
    .astype(str)
    .str.strip()
)


for column in ["mae", "rmse", "mape"]:

    metrics_df[column] = pd.to_numeric(
        metrics_df[column],
        errors="coerce"
    )


metrics_df = metrics_df.dropna(
    subset=required_columns
).copy()


metrics_df = metrics_df.loc[
    (metrics_df["mae"] >= 0)
    & (metrics_df["rmse"] >= 0)
    & (metrics_df["mape"] >= 0)
].reset_index(drop=True)


if metrics_df.empty:

    st.error(
        "No valid model evaluation records were found."
    )

    st.stop()


# ============================================================
# 12. MODEL SELECTION
# ============================================================

section_title(
    "Model Selection",
    "Choose the forecasting models you want to compare."
)


available_models = metrics_df["model"].drop_duplicates().tolist()


with st.container(border=True):

    selected_models = st.multiselect(

        "Select Models to Compare",

        options=available_models,

        default=available_models,

        key="performance_selected_models"

    )


if not selected_models:

    st.warning(
        "Select at least one model to continue."
    )

    st.stop()


filtered_df = metrics_df.loc[
    metrics_df["model"].isin(selected_models)
].copy()


if filtered_df.empty:

    st.warning(
        "No model results are available for the selection."
    )

    st.stop()


# ============================================================
# 13. BEST MODEL IDENTIFICATION
# ============================================================

best_model = filtered_df.sort_values(
    "mape",
    ascending=True
).iloc[0]


best_model_name = best_model["model"]


section_title(
    "Best Performing Model",
    "The model with the lowest MAPE among the selected models."
)


k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "Best Model",
        best_model_name
    )


with k2:

    st.metric(
        "MAPE",
        f"{best_model['mape']:.2f}%"
    )


with k3:

    st.metric(
        "Mean Absolute Error",
        f"{best_model['mae']:,.0f}"
    )


with k4:

    st.metric(
        "Root Mean Squared Error",
        f"{best_model['rmse']:,.0f}"
    )


# ============================================================
# 14. BEST MODEL INSIGHTS
# ============================================================

insight_col1, insight_col2, insight_col3 = st.columns(3)


with insight_col1:

    insight_card(
        "TOP RANKED MODEL",
        best_model_name,
        "Lowest MAPE among selected models"
    )


with insight_col2:

    insight_card(
        "TOTAL MODELS COMPARED",
        str(len(filtered_df)),
        "Forecasting algorithms evaluated"
    )


with insight_col3:

    insight_card(
        "LOWEST MAPE",
        f"{best_model['mape']:.2f}%",
        "Lower percentage indicates better accuracy"
    )


# ============================================================
# 15. PERFORMANCE RANKING
# ============================================================

section_title(
    "Model Evaluation Results",
    "Rank models based on their forecasting error metrics."
)


ranking_df = filtered_df.sort_values(
    "mape",
    ascending=True
).reset_index(drop=True)


ranking_df.insert(
    0,
    "Rank",
    range(1, len(ranking_df) + 1)
)


ranking_display = ranking_df[
    ["Rank", "model", "mae", "rmse", "mape"]
].copy()


ranking_display = ranking_display.rename(
    columns={
        "model": "Model",
        "mae": "MAE",
        "rmse": "RMSE",
        "mape": "MAPE"
    }
)


st.dataframe(

    ranking_display,

    width="stretch",

    hide_index=True,

    column_config={

        "Rank": st.column_config.NumberColumn(
            "Rank",
            format="%d"
        ),

        "Model": st.column_config.TextColumn(
            "Model"
        ),

        "MAE": st.column_config.NumberColumn(
            "MAE",
            format="localized"
        ),

        "RMSE": st.column_config.NumberColumn(
            "RMSE",
            format="localized"
        ),

        "MAPE": st.column_config.NumberColumn(
            "MAPE",
            format="%.2f%%"
        )

    }

)


# ============================================================
# 16. MAPE COMPARISON
# ============================================================

section_title(
    "MAPE Comparison",
    "Compare forecasting accuracy across the selected models."
)


mape_data = filtered_df.sort_values(
    "mape",
    ascending=True
).copy()


fig_mape = px.bar(

    mape_data,

    x="model",

    y="mape",

    color="model",

    color_discrete_sequence=[
        BLUE,
        TEAL,
        GREEN,
        ORANGE,
        RED
    ],

    text=mape_data["mape"].map(
        lambda value: f"{value:.2f}%"
    )

)


fig_mape.update_traces(

    textposition="outside",

    marker_line_width=0,

    cliponaxis=False

)


fig_mape.update_layout(

    title=dict(
        text="Forecasting Accuracy by Model",
        x=0.02,
        font=dict(
            size=16,
            color="#173f59"
        )
    ),

    xaxis_title="Forecasting Model",

    yaxis_title="MAPE (%)",

    showlegend=False

)


style_chart(
    fig_mape,
    height=420
)


st.plotly_chart(
    fig_mape,
    width="stretch",
    key="performance_mape_chart"
)


# ============================================================
# 17. ERROR METRIC COMPARISON
# ============================================================

section_title(
    "Error Metric Comparison",
    "Explore prediction errors using MAE or RMSE."
)


with st.container(border=True):

    metric_choice = st.selectbox(

        "Select Evaluation Metric",

        ["MAE", "RMSE"],

        index=0,

        key="performance_metric_choice"

    )


metric_column = metric_choice.lower()


error_data = filtered_df.sort_values(
    metric_column,
    ascending=True
).copy()


fig_error = px.bar(

    error_data,

    x="model",

    y=metric_column,

    color="model",

    color_discrete_sequence=[
        BLUE,
        TEAL,
        GREEN,
        ORANGE,
        RED
    ],

    text=error_data[metric_column].map(
        lambda value: f"{value:,.0f}"
    )

)


fig_error.update_traces(

    textposition="outside",

    marker_line_width=0,

    cliponaxis=False

)


fig_error.update_layout(

    title=dict(
        text=f"{metric_choice} Comparison Across Models",
        x=0.02,
        font=dict(
            size=16,
            color="#173f59"
        )
    ),

    xaxis_title="Forecasting Model",

    yaxis_title=metric_choice,

    showlegend=False

)


style_chart(
    fig_error,
    height=420
)


st.plotly_chart(
    fig_error,
    width="stretch",
    key="performance_error_chart"
)


# ============================================================
# 18. LIGHTGBM HYPERPARAMETER TUNING
# ============================================================

section_title(
    "LightGBM Hyperparameter Tuning",
    "Review the parameter combinations evaluated during model optimization."
)


if tuning_df is not None and not tuning_df.empty:

    tuning_df = tuning_df.copy()

    tuning_df.columns = (
        tuning_df.columns
        .str.strip()
        .str.lower()
    )


    st.caption(
        f"{len(tuning_df):,} hyperparameter configurations available."
    )


    with st.expander(
        "View LightGBM Tuning Results",
        expanded=False
    ):

        st.dataframe(
            tuning_df,
            width="stretch",
            hide_index=True
        )


    tuning_csv = tuning_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        label="Download LightGBM Tuning Results",

        data=tuning_csv,

        file_name="lightgbm_tuning_results.csv",

        mime="text/csv",

        width="stretch"

    )


else:

    st.info(
        "LightGBM tuning results are not available. "
        "The model performance comparison is still available."
    )


# ============================================================
# 19. MODEL-WISE PERFORMANCE SUMMARY
# ============================================================

section_title(
    "Performance Summary",
    "Detailed evaluation results for each selected forecasting model."
)


for rank, (_, row) in enumerate(
    filtered_df.sort_values("mape").iterrows(),
    start=1
):

    with st.container(border=True):

        left, right = st.columns([2, 1])


        with left:

            st.markdown(
                f"### {rank}. {row['model']}"
            )


            metric_col1, metric_col2, metric_col3 = st.columns(3)


            with metric_col1:

                st.metric(
                    "MAE",
                    f"{row['mae']:,.2f}"
                )


            with metric_col2:

                st.metric(
                    "RMSE",
                    f"{row['rmse']:,.2f}"
                )


            with metric_col3:

                st.metric(
                    "MAPE",
                    f"{row['mape']:.2f}%"
                )


        with right:

            if row["model"] == best_model_name:

                st.success(
                    "BEST PERFORMING MODEL"
                )

            else:

                st.info(
                    f"RANK #{rank}"
                )


# ============================================================
# 20. KEY FINDINGS
# ============================================================

section_title(
    "Key Findings",
    "Important observations from the model evaluation results."
)


# Use complete metrics dataset for fixed model comparisons.
# This prevents the model filter from changing the underlying
# SARIMAX versus LightGBM versus baseline interpretation.

all_models = metrics_df.copy()


sarimax_data = all_models.loc[
    all_models["model"].str.casefold() == "sarimax"
]


lightgbm_data = all_models.loc[
    all_models["model"].str.casefold() == "lightgbm"
]


baseline_data = all_models.loc[
    all_models["model"].str.casefold() == "seasonal naive"
]


if (
    not sarimax_data.empty
    and not lightgbm_data.empty
    and not baseline_data.empty
):

    sarimax = sarimax_data.iloc[0]

    lightgbm = lightgbm_data.iloc[0]

    baseline = baseline_data.iloc[0]


    if baseline["mape"] > 0:

        improvement = (

            (
                baseline["mape"]
                - sarimax["mape"]
            )

            / baseline["mape"]

        ) * 100

    else:

        improvement = None


    finding_col1, finding_col2 = st.columns(2)


    with finding_col1:

        insight_card(
            "SARIMAX MAPE",
            f"{sarimax['mape']:.2f}%",
            "Performance of the statistical forecasting model"
        )


    with finding_col2:

        insight_card(
            "LIGHTGBM MAPE",
            f"{lightgbm['mape']:.2f}%",
            "Performance of the machine learning model"
        )


    st.markdown("")


    if improvement is not None:

        st.markdown(
            f"""
            **Key observations**

            - SARIMAX achieved a MAPE of **{sarimax['mape']:.2f}%**.
            - LightGBM achieved a MAPE of **{lightgbm['mape']:.2f}%**.
            - Seasonal Naive achieved a MAPE of **{baseline['mape']:.2f}%**.
            - SARIMAX reduced MAPE by **{improvement:.2f}%**
              relative to the Seasonal Naive baseline.
            """
        )


    else:

        st.markdown(
            f"""
            **Key observations**

            - SARIMAX achieved a MAPE of **{sarimax['mape']:.2f}%**.
            - LightGBM achieved a MAPE of **{lightgbm['mape']:.2f}%**.
            - Seasonal Naive achieved a MAPE of **{baseline['mape']:.2f}%**.
            """
        )


else:

    st.info(
        f"{best_model_name} currently has the lowest MAPE "
        "among the selected models. Additional model comparisons "
        "will appear when their results are available."
    )


# ============================================================
# 21. METRIC INTERPRETATION
# ============================================================

section_title(
    "Understanding Evaluation Metrics",
    "What each metric tells us about forecasting performance."
)


interpretation_col1, interpretation_col2, interpretation_col3 = st.columns(3)


with interpretation_col1:

    insight_card(
        "MAE",
        "Mean Absolute Error",
        "Average absolute difference between actual and predicted passenger counts."
    )


with interpretation_col2:

    insight_card(
        "RMSE",
        "Root Mean Squared Error",
        "Penalizes larger prediction errors more heavily than MAE."
    )


with interpretation_col3:

    insight_card(
        "MAPE",
        "Mean Absolute Percentage Error",
        "Expresses average prediction error as a percentage."
    )


st.caption(
    "MAE and RMSE are measured in passenger counts. "
    "MAPE is expressed as a percentage. "
    "Lower values indicate better forecasting performance. "
    "MAPE can be unreliable when actual values are zero or very close to zero."
)


# ============================================================
# 22. DOWNLOAD MODEL METRICS
# ============================================================

section_title(
    "Download Evaluation Results",
    "Export model performance metrics for further analysis."
)


download_df = ranking_display.copy()


download_csv = download_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="Download Model Performance Results",

    data=download_csv,

    file_name="metro_model_performance.csv",

    mime="text/csv",

    width="stretch"

)


# ============================================================
# 23. FOOTER
# ============================================================

st.markdown("""
<hr>

<div class="performance-footer">
    METRO OPERATIONS ANALYTICS PLATFORM
    &nbsp; | &nbsp;
    MODEL PERFORMANCE & EVALUATION
</div>
""", unsafe_allow_html=True)