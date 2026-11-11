import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    title="Model Explainability",
    active="Explainability"
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

.explain-eyebrow {

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


.explain-heading {

    font-size: 38px;

    font-weight: 850;

    color: #123b55 !important;

    letter-spacing: -1.2px;

    line-height: 1.15;

    margin-bottom: 9px;

    text-shadow:
        0 3px 14px rgba(0, 170, 190, 0.10);
}


.explain-subheading {

    color: #637f95 !important;

    font-size: 14px;

    line-height: 1.8;

    max-width: 950px;

    margin-bottom: 22px;
}


/* ----------------------------------------------------------
   INFORMATION BANNER
---------------------------------------------------------- */

.explain-note {

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


.explain-note-title {

    color: #087f86 !important;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1px;

    margin-bottom: 7px;
}


.explain-note-content {

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
   CONTENT CONTAINERS
---------------------------------------------------------- */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background: #ffffff !important;

    border: 1px solid #dce9f1;

    border-radius: 15px;

    box-shadow: 0 4px 16px rgba(30, 80, 110, 0.045);
}


/* ----------------------------------------------------------
   FILTER INPUTS
---------------------------------------------------------- */

div[data-baseweb="input"] {

    background: #ffffff !important;

    border: 1px solid #cbdce8 !important;

    border-radius: 9px !important;
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

.explain-footer {

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

    .explain-heading {
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

PURPLE = "#9270db"

ORANGE = "#f59e42"

RED = "#e56b6f"

TEXT_COLOR = "#25465e"

GRID_COLOR = "rgba(80, 120, 150, 0.14)"


LINE_COLORS = {
    "Blue": "#397fe8",
    "Green": "#16a477",
    "Purple": "#9270db"
}


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
# 7. LOAD CSV FILES
# ============================================================

@st.cache_data(show_spinner="Loading explainability data...")
def load_csv(filename):

    file_path = OUTPUT_PATH / filename

    if not file_path.exists():
        return None

    return pd.read_csv(file_path)


def standardize_columns(dataframe):

    if dataframe is None:
        return None

    dataframe = dataframe.copy()

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return dataframe


# ============================================================
# 8. PAGE HEADER
# ============================================================

st.markdown("""
<div class="explain-eyebrow">
    MACHINE LEARNING | MODEL INTERPRETABILITY
</div>

<div class="explain-heading">
    Model Explainability
</div>

<div class="explain-subheading">
    Understand the features influencing model predictions,
    evaluate forecasting errors, examine line-level performance
    and investigate the relationship between external factors
    and prediction accuracy.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 9. INFORMATION BANNER
# ============================================================

note_html = (
    '<div class="explain-note">'
    '<div class="explain-note-title">'
    'UNDERSTANDING MODEL BEHAVIOUR'
    '</div>'
    '<div class="explain-note-content">'
    'This section examines feature importance and forecast errors '
    'to understand how the trained model behaves. '
    'Feature importance indicates predictive contribution, '
    'not a causal relationship.'
    '<br>'
    '<b>Analysis:</b> Feature Importance | Prediction Errors | '
    'Line-Level Performance'
    '</div>'
    '</div>'
)

st.markdown(
    note_html,
    unsafe_allow_html=True
)


# ============================================================
# 10. LOAD ALL DATA
# ============================================================

try:

    importance_df = standardize_columns(
        load_csv("feature_importance.csv")
    )

    error_df = standardize_columns(
        load_csv("forecast_error_analysis.csv")
    )

    line_error_df = standardize_columns(
        load_csv("line_error_summary.csv")
    )

except Exception as error:

    st.error(
        f"Unable to load explainability files: {error}"
    )

    st.stop()


# ============================================================
# 11. FEATURE IMPORTANCE
# ============================================================

section_title(
    "Feature Importance",
    "Identify the input variables that contributed most to model predictions."
)


if importance_df is not None and not importance_df.empty:

    required_columns = [
        "feature",
        "importance"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in importance_df.columns
    ]

    if missing_columns:

        st.warning(
            f"Feature importance file is missing columns: {missing_columns}"
        )

    else:

        importance_df["importance"] = pd.to_numeric(
            importance_df["importance"],
            errors="coerce"
        )

        importance_df = importance_df.dropna(
            subset=["feature", "importance"]
        ).copy()

        importance_df = importance_df.sort_values(
            "importance",
            ascending=False
        ).reset_index(drop=True)


        if not importance_df.empty:

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Total Features",
                    f"{len(importance_df)}"
                )


            with col2:

                st.metric(
                    "Most Important Feature",
                    str(importance_df.iloc[0]["feature"])
                )


            with col3:

                st.metric(
                    "Highest Importance",
                    f"{importance_df.iloc[0]['importance']:,.2f}"
                )


            # ----------------------------------------------
            # FEATURE IMPORTANCE CHART
            # ----------------------------------------------

            fig_importance = px.bar(

                importance_df.sort_values(
                    "importance",
                    ascending=True
                ),

                x="importance",

                y="feature",

                orientation="h",

                color="importance",

                color_continuous_scale=[
                    "#d9f3f3",
                    "#62c8ce",
                    "#397fe8"
                ],

                title="Feature Importance Ranking"

            )


            fig_importance.update_traces(

                marker_line_width=0,

                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Importance: %{x:,.4f}"
                    "<extra></extra>"
                )

            )


            fig_importance.update_layout(

                title=dict(
                    x=0.02,
                    font=dict(
                        size=16,
                        color="#173f59"
                    )
                ),

                xaxis_title="Importance Score",

                yaxis_title="Feature",

                coloraxis_showscale=False

            )


            style_chart(
                fig_importance,
                height=max(400, len(importance_df) * 32)
            )


            st.plotly_chart(
                fig_importance,
                width="stretch",
                key="feature_importance_chart"
            )


            # ----------------------------------------------
            # IMPORTANCE VARIABILITY
            # ----------------------------------------------

            if "std" in importance_df.columns:

                importance_df["std"] = pd.to_numeric(
                    importance_df["std"],
                    errors="coerce"
                )

                std_df = importance_df.dropna(
                    subset=["std"]
                ).copy()


                if not std_df.empty:

                    section_title(
                        "Feature Importance Variability",
                        "Examine how much feature importance changes across model evaluations."
                    )


                    fig_std = px.bar(

                        std_df.sort_values(
                            "std",
                            ascending=False
                        ),

                        x="feature",

                        y="std",

                        color="std",

                        color_continuous_scale=[
                            "#e9e2fa",
                            "#b59ce8",
                            "#8062c8"
                        ],

                        title="Variation in Feature Importance"

                    )


                    fig_std.update_layout(

                        title=dict(
                            x=0.02,
                            font=dict(
                                size=16,
                                color="#173f59"
                            )
                        ),

                        xaxis_title="Feature",

                        yaxis_title="Importance Standard Deviation",

                        xaxis_tickangle=-35,

                        coloraxis_showscale=False

                    )


                    style_chart(
                        fig_std,
                        height=420
                    )


                    st.plotly_chart(
                        fig_std,
                        width="stretch",
                        key="feature_variability_chart"
                    )


            # ----------------------------------------------
            # FEATURE IMPORTANCE TABLE
            # ----------------------------------------------

            section_title(
                "Feature Importance Details",
                "Detailed ranking of the model input features."
            )


            st.dataframe(
                importance_df,
                width="stretch",
                hide_index=True
            )


            importance_csv = importance_df.to_csv(
                index=False
            ).encode("utf-8")


            st.download_button(

                "Download Feature Importance",

                importance_csv,

                "feature_importance.csv",

                "text/csv"

            )


        else:

            st.warning(
                "No valid feature importance records were found."
            )


else:

    st.info(
        "feature_importance.csv was not found or contains no records."
    )


# ============================================================
# 12. FORECAST ERROR ANALYSIS
# ============================================================

section_title(
    "Forecast Error Analysis",
    "Compare actual and predicted ridership to understand model accuracy."
)


if error_df is not None and not error_df.empty:

    # ----------------------------------------------
    # STANDARDIZE COMMON COLUMN VARIATIONS
    # ----------------------------------------------

    column_aliases = {

        "actual": [
            "actual",
            "y_actual",
            "actual_ridership",
            "true_value",
            "ridership"
        ],

        "predicted": [
            "predicted",
            "prediction",
            "y_predicted",
            "predicted_ridership",
            "forecast"
        ],

        "absolute_error": [
            "absolute_error",
            "abs_error",
            "mae_error"
        ],

        "error": [
            "error",
            "signed_error",
            "forecast_error"
        ],

        "percentage_error": [
            "percentage_error",
            "percentage",
            "ape",
            "absolute_percentage_error"
        ],

        "date": [
            "date",
            "forecast_date"
        ],

        "line": [
            "line",
            "metro_line"
        ],

        "rainfall_mm": [
            "rainfall_mm",
            "rainfall",
            "rain"
        ]

    }


    rename_columns = {}


    for standard_name, possible_names in column_aliases.items():

        for name in possible_names:

            if name in error_df.columns:

                rename_columns[name] = standard_name

                break


    error_df = error_df.rename(
        columns=rename_columns
    )


    # ----------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # ----------------------------------------------

    numeric_columns = [

        "actual",

        "predicted",

        "error",

        "absolute_error",

        "percentage_error",

        "rainfall_mm"

    ]


    for column in numeric_columns:

        if column in error_df.columns:

            error_df[column] = pd.to_numeric(
                error_df[column],
                errors="coerce"
            )


    # ----------------------------------------------
    # DATE CONVERSION
    # ----------------------------------------------

    if "date" in error_df.columns:

        error_df["date"] = pd.to_datetime(
            error_df["date"],
            errors="coerce"
        )


    # ----------------------------------------------
    # CALCULATE MISSING ERROR COLUMNS
    # ----------------------------------------------

    if (
        "actual" in error_df.columns
        and "predicted" in error_df.columns
    ):

        if "error" not in error_df.columns:

            error_df["error"] = (
                error_df["predicted"]
                - error_df["actual"]
            )


        if "absolute_error" not in error_df.columns:

            error_df["absolute_error"] = (
                error_df["error"].abs()
            )


        if "percentage_error" not in error_df.columns:

            valid_actual = error_df["actual"].abs().replace(
                0,
                float("nan")
            )

            error_df["percentage_error"] = (
                error_df["absolute_error"]
                / valid_actual
            ) * 100


    # ----------------------------------------------
    # CLEAN ERROR DATA
    # ----------------------------------------------

    if "line" in error_df.columns:

        error_df["line"] = (
            error_df["line"]
            .astype(str)
            .str.strip()
        )


    if "absolute_error" in error_df.columns:

        error_df = error_df.dropna(
            subset=["absolute_error"]
        ).copy()


    if error_df.empty:

        st.warning(
            "No valid forecast error records are available."
        )

    elif "absolute_error" not in error_df.columns:

        st.warning(
            "The forecast error file does not contain recognizable error values."
        )

    else:

        # ------------------------------------------
        # ERROR KPIs
        # ------------------------------------------

        avg_error = error_df["absolute_error"].mean()

        max_error = error_df["absolute_error"].max()

        median_error = error_df["absolute_error"].median()


        k1, k2, k3 = st.columns(3)


        with k1:

            st.metric(
                "Average Absolute Error",
                f"{avg_error:,.0f}"
            )


        with k2:

            st.metric(
                "Maximum Absolute Error",
                f"{max_error:,.0f}"
            )


        with k3:

            st.metric(
                "Median Absolute Error",
                f"{median_error:,.0f}"
            )


        if (
            "percentage_error" in error_df.columns
            and error_df["percentage_error"].notna().any()
        ):

            st.metric(
                "Average Absolute Percentage Error",
                f"{error_df['percentage_error'].mean():.2f}%"
            )


        # ------------------------------------------
        # ACTUAL VS PREDICTED
        # ------------------------------------------

        if (
            "actual" in error_df.columns
            and "predicted" in error_df.columns
        ):

            section_title(
                "Actual vs Predicted Ridership",
                "Points closer to the diagonal reference line indicate more accurate predictions."
            )


            scatter_df = error_df.dropna(
                subset=["actual", "predicted"]
            ).copy()


            if not scatter_df.empty:

                fig_actual = px.scatter(

                    scatter_df,

                    x="actual",

                    y="predicted",

                    color="line" if "line" in scatter_df.columns else None,

                    color_discrete_map=LINE_COLORS,

                    opacity=0.72,

                    title="Actual vs Predicted Values"

                )


                min_value = min(
                    scatter_df["actual"].min(),
                    scatter_df["predicted"].min()
                )


                max_value = max(
                    scatter_df["actual"].max(),
                    scatter_df["predicted"].max()
                )


                fig_actual.add_trace(

                    go.Scatter(

                        x=[min_value, max_value],

                        y=[min_value, max_value],

                        mode="lines",

                        name="Perfect Prediction",

                        line=dict(
                            color=ORANGE,
                            width=2.5,
                            dash="dash"
                        )

                    )

                )


                fig_actual.update_layout(

                    title=dict(
                        x=0.02,
                        font=dict(
                            size=16,
                            color="#173f59"
                        )
                    ),

                    xaxis_title="Actual Ridership",

                    yaxis_title="Predicted Ridership"

                )


                style_chart(
                    fig_actual,
                    height=500
                )


                st.plotly_chart(
                    fig_actual,
                    width="stretch",
                    key="actual_predicted_chart"
                )


        # ------------------------------------------
        # ERROR DISTRIBUTION
        # ------------------------------------------

        section_title(
            "Error Distribution",
            "Understand how forecast errors are distributed across predictions."
        )


        fig_distribution = px.histogram(

            error_df,

            x="absolute_error",

            nbins=40,

            color_discrete_sequence=[BLUE],

            title="Distribution of Absolute Forecast Errors"

        )


        fig_distribution.update_traces(
            marker_line_width=0,
            opacity=0.85
        )


        fig_distribution.update_layout(

            title=dict(
                x=0.02,
                font=dict(
                    size=16,
                    color="#173f59"
                )
            ),

            xaxis_title="Absolute Forecast Error",

            yaxis_title="Number of Predictions"

        )


        style_chart(
            fig_distribution,
            height=420
        )


        st.plotly_chart(
            fig_distribution,
            width="stretch",
            key="error_distribution_chart"
        )


        # ------------------------------------------
        # ERROR BY METRO LINE
        # ------------------------------------------

        if "line" in error_df.columns:

            section_title(
                "Forecast Error by Metro Line",
                "Compare average prediction errors across individual metro lines."
            )


            line_error = (

                error_df.groupby("line", as_index=False)

                ["absolute_error"]

                .mean()

                .sort_values(
                    "absolute_error",
                    ascending=False
                )

            )


            fig_line_error = px.bar(

                line_error,

                x="line",

                y="absolute_error",

                color="line",

                color_discrete_map=LINE_COLORS,

                text=line_error["absolute_error"].map(
                    lambda value: f"{value:,.0f}"
                ),

                title="Average Absolute Error by Metro Line"

            )


            fig_line_error.update_traces(
                textposition="outside",
                cliponaxis=False
            )


            fig_line_error.update_layout(

                title=dict(
                    x=0.02,
                    font=dict(
                        size=16,
                        color="#173f59"
                    )
                ),

                showlegend=False,

                xaxis_title="Metro Line",

                yaxis_title="Mean Absolute Error"

            )


            style_chart(
                fig_line_error,
                height=420
            )


            st.plotly_chart(
                fig_line_error,
                width="stretch",
                key="line_error_chart"
            )


        # ------------------------------------------
        # RAINFALL VS ERROR
        # ------------------------------------------

        if "rainfall_mm" in error_df.columns:

            section_title(
                "Rainfall vs Forecast Error",
                "Explore whether rainfall levels are associated with changes in prediction errors."
            )


            rainfall_df = error_df.dropna(
                subset=[
                    "rainfall_mm",
                    "absolute_error"
                ]
            ).copy()


            if not rainfall_df.empty:

                fig_rainfall = px.scatter(

                    rainfall_df,

                    x="rainfall_mm",

                    y="absolute_error",

                    color="line" if "line" in rainfall_df.columns else None,

                    color_discrete_map=LINE_COLORS,

                    opacity=0.7,

                    title="Rainfall and Absolute Forecast Error"

                )


                fig_rainfall.update_layout(

                    title=dict(
                        x=0.02,
                        font=dict(
                            size=16,
                            color="#173f59"
                        )
                    ),

                    xaxis_title="Rainfall (mm)",

                    yaxis_title="Absolute Forecast Error"

                )


                style_chart(
                    fig_rainfall,
                    height=420
                )


                st.plotly_chart(
                    fig_rainfall,
                    width="stretch",
                    key="rainfall_error_chart"
                )


        # ------------------------------------------
        # ERROR RECORDS
        # ------------------------------------------

        section_title(
            "Forecast Error Records",
            "Inspect individual actual values, predictions and calculated errors."
        )


        with st.expander(
            "View Detailed Error Records",
            expanded=False
        ):

            st.dataframe(
                error_df,
                width="stretch",
                hide_index=True
            )


        error_csv = error_df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(

            "Download Forecast Error Analysis",

            error_csv,

            "forecast_error_analysis.csv",

            "text/csv"

        )


else:

    st.info(
        "forecast_error_analysis.csv was not found or contains no records."
    )


# ============================================================
# 13. LINE-LEVEL ERROR SUMMARY
# ============================================================

section_title(
    "Line-Level Error Summary",
    "Evaluate forecasting accuracy and prediction bias for each metro line."
)


if line_error_df is not None and not line_error_df.empty:

    line_error_df = line_error_df.copy()


    # ----------------------------------------------
    # STANDARDIZE KNOWN COLUMN VARIATIONS
    # ----------------------------------------------

    line_aliases = {

        "average_error": "average_signed_error",

        "mean_error": "average_signed_error",

        "maximum_error": "maximum_absolute_error",

        "max_error": "maximum_absolute_error"

    }


    line_error_df = line_error_df.rename(
        columns=line_aliases
    )


    if "line" not in line_error_df.columns:

        st.warning(
            "Line error summary must contain a line column."
        )

    elif "mae" not in line_error_df.columns:

        st.warning(
            "Line error summary must contain an MAE column."
        )

    else:

        line_error_df["line"] = (
            line_error_df["line"]
            .astype(str)
            .str.strip()
        )


        numeric_line_columns = [

            "mae",

            "average_signed_error",

            "maximum_absolute_error"

        ]


        for column in numeric_line_columns:

            if column in line_error_df.columns:

                line_error_df[column] = pd.to_numeric(
                    line_error_df[column],
                    errors="coerce"
                )


        line_error_df = line_error_df.dropna(
            subset=["mae"]
        ).copy()


        if not line_error_df.empty:

            # --------------------------------------
            # LINE KPI CARDS
            # --------------------------------------

            available_line_order = [
                line
                for line in ["Blue", "Green", "Purple"]
                if line in line_error_df["line"].values
            ]


            line_columns = st.columns(
                max(1, len(available_line_order))
            )


            for container, line in zip(
                line_columns,
                available_line_order
            ):

                row = line_error_df.loc[
                    line_error_df["line"] == line
                ]


                if not row.empty:

                    with container:

                        st.metric(
                            f"{line} Line MAE",
                            f"{row.iloc[0]['mae']:,.0f}"
                        )


            # --------------------------------------
            # MAE COMPARISON
            # --------------------------------------

            section_title(
                "Mean Absolute Error by Line",
                "Identify which metro line has the largest average prediction error."
            )


            fig_line_mae = px.bar(

                line_error_df.sort_values(
                    "mae",
                    ascending=False
                ),

                x="line",

                y="mae",

                color="line",

                color_discrete_map=LINE_COLORS,

                text=line_error_df.sort_values(
                    "mae",
                    ascending=False
                )["mae"].map(
                    lambda value: f"{value:,.0f}"
                ),

                title="Mean Absolute Error Comparison"

            )


            fig_line_mae.update_traces(
                textposition="outside",
                cliponaxis=False
            )


            fig_line_mae.update_layout(

                title=dict(
                    x=0.02,
                    font=dict(
                        size=16,
                        color="#173f59"
                    )
                ),

                showlegend=False,

                xaxis_title="Metro Line",

                yaxis_title="MAE"

            )


            style_chart(
                fig_line_mae,
                height=420
            )


            st.plotly_chart(
                fig_line_mae,
                width="stretch",
                key="line_mae_summary_chart"
            )


            # --------------------------------------
            # SIGNED ERROR
            # --------------------------------------

            if "average_signed_error" in line_error_df.columns:

                section_title(
                    "Average Signed Forecast Error",
                    "Positive values indicate overprediction; negative values indicate underprediction."
                )


                signed_data = line_error_df.dropna(
                    subset=["average_signed_error"]
                ).copy()


                if not signed_data.empty:

                    fig_signed = px.bar(

                        signed_data,

                        x="line",

                        y="average_signed_error",

                        color="line",

                        color_discrete_map=LINE_COLORS,

                        title="Average Signed Error by Line"

                    )


                    fig_signed.add_hline(

                        y=0,

                        line_dash="dash",

                        line_color=ORANGE,

                        annotation_text="Zero Error"

                    )


                    fig_signed.update_layout(

                        title=dict(
                            x=0.02,
                            font=dict(
                                size=16,
                                color="#173f59"
                            )
                        ),

                        showlegend=False,

                        xaxis_title="Metro Line",

                        yaxis_title="Average Signed Error"

                    )


                    style_chart(
                        fig_signed,
                        height=420
                    )


                    st.plotly_chart(
                        fig_signed,
                        width="stretch",
                        key="signed_error_chart"
                    )


            # --------------------------------------
            # LINE ERROR DETAILS
            # --------------------------------------

            section_title(
                "Line Error Details",
                "Detailed comparison of error metrics across metro lines."
            )


            st.dataframe(
                line_error_df,
                width="stretch",
                hide_index=True
            )


            line_csv = line_error_df.to_csv(
                index=False
            ).encode("utf-8")


            st.download_button(

                "Download Line Error Summary",

                line_csv,

                "line_error_summary.csv",

                "text/csv"

            )


        else:

            st.warning(
                "No valid line-level error records were found."
            )


else:

    st.info(
        "line_error_summary.csv was not found or contains no records."
    )


# ============================================================
# 14. MODEL INTERPRETATION
# ============================================================

section_title(
    "Understanding Model Explainability",
    "Interpret the results using the correct forecasting concepts."
)


col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown("### Feature Importance")

        st.write(
            "Shows the relative contribution of input features "
            "to the model's predictions. Higher importance does "
            "not prove that a feature causes ridership changes."
        )


    with st.container(border=True):

        st.markdown("### Mean Absolute Error")

        st.write(
            "Measures the average absolute difference between "
            "actual and predicted passenger counts. Lower values "
            "indicate smaller average errors."
        )


with col2:

    with st.container(border=True):

        st.markdown("### Prediction Bias")

        st.write(
            "Signed forecast error helps identify whether the "
            "model tends to overpredict or underpredict ridership."
        )


    with st.container(border=True):

        st.markdown("### Error Distribution")

        st.write(
            "Shows how prediction errors are spread across "
            "observations and helps identify unusually large errors."
        )


# ============================================================
# 15. FINAL NOTE
# ============================================================

note_html = (
    '<div class="explain-note">'
    '<div class="explain-note-title">'
    'IMPORTANT INTERPRETATION NOTE'
    '</div>'
    '<div class="explain-note-content">'
    'Feature importance indicates predictive contribution, '
    'not causation. Forecast errors measure differences between '
    'actual and predicted values. Positive signed error indicates '
    'overprediction, while negative signed error indicates '
    'underprediction. This project uses a synthetic dataset '
    'for demonstration.'
    '</div>'
    '</div>'
)

st.markdown(
    note_html,
    unsafe_allow_html=True
)


# ============================================================
# 16. FOOTER
# ============================================================

st.markdown("""
<hr>

<div class="explain-footer">
    METRO OPERATIONS ANALYTICS PLATFORM
    &nbsp; | &nbsp;
    MODEL EXPLAINABILITY
</div>
""", unsafe_allow_html=True)