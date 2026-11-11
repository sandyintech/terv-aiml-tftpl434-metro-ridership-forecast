
from pathlib import Path
import html

import streamlit as st


APP_DIR = Path(__file__).resolve().parent

NAVIGATION = [
    ("Overview", "Home.py", "🏠"),
    ("Ridership Analysis", "pages/1_Ridership_Analysis.py", "📊"),
    ("Line Analysis", "pages/2_Line_Analysis.py", "🚇"),
    ("Forecasting", "pages/3_Forecasting.py", "📈"),
    ("Model Performance", "pages/4_Model_Performance.py", "🎯"),
    ("Explainability", "pages/5_Explainability.py", "🧠"),
    ("Capacity Planning", "pages/6_Capacity_Planning.py", "⚙️"),
    ("Data Quality", "pages/7_Data_Quality.py", "🔍"),
]


# ============================================================
# 1. GLOBAL DESIGN SYSTEM
# ============================================================

def inject_global_styles():

    st.markdown(
        """
<style>

/* ---------- APPLICATION ---------- */

.stApp {
    background: #F2F6F8;
    color: #263C4A;
}

[data-testid="stAppViewContainer"] {
    background: #F2F6F8;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1650px;
    padding: 1.3rem 1.6rem 2rem 1.6rem;
}

html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
}

h1, h2, h3, h4 {
    color: #173D50 !important;
    font-weight: 700 !important;
}

p {
    color: #647987;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #123F50;
    border-right: 1px solid #24596B;
}

section[data-testid="stSidebar"] > div {
    background: #123F50;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #C2D9E0 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #376878;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
    color: #FFFFFF !important;
    border-radius: 8px;
    padding: 8px 10px;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background: #226176;
}


/* ---------- GLOBAL PAGE HEADER ---------- */

.global-page-header {
    margin-bottom: 24px;
    padding: 2px 0 8px 0;
}

.global-page-eyebrow {
    color: #1496A5;
    font-size: 0.73rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 7px;
}

.global-page-title {
    color: #173D50;
    font-size: 2.15rem;
    font-weight: 800;
    letter-spacing: -0.8px;
    line-height: 1.2;
    margin: 0 0 8px 0;
}

.global-page-subtitle {
    color: #718593;
    font-size: 0.94rem;
    line-height: 1.6;
    margin: 0;
}


/* ---------- EXISTING PAGE HEADING CLASSES ---------- */

.page-eyebrow {
    color: #1496A5;
    font-size: 0.73rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

.page-title {
    color: #173D50;
    font-size: 2rem;
    font-weight: 750;
    letter-spacing: -0.7px;
    margin-bottom: 5px;
}

.page-subtitle {
    color: #718593;
    font-size: 0.9rem;
}

.section-title {
    color: #173D50;
    font-size: 1.18rem;
    font-weight: 750;
    margin-bottom: 3px;
}

.section-description {
    color: #7C8F9C;
    font-size: 0.84rem;
    margin-bottom: 12px;
}


/* ---------- METRIC CARDS ---------- */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DFE8EC;
    border-left: 4px solid #1595A3;
    border-radius: 10px;
    padding: 14px 16px;
    min-height: 102px;
    box-shadow: 0 3px 10px rgba(25, 65, 80, 0.055);
    transition: 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #A5D8DC;
    box-shadow: 0 5px 16px rgba(20, 125, 140, 0.12);
    transform: translateY(-2px);
}

[data-testid="stMetricLabel"] {
    color: #718593 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #173F52 !important;
    font-size: 1.55rem !important;
    font-weight: 750 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.76rem !important;
}


/* ---------- CONTENT CARDS ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DFE8EC;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(25, 65, 80, 0.045);
}


/* ---------- INPUTS ---------- */

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div,
[data-testid="stDateInput"] input {
    background: #FFFFFF;
    border-color: #D5E1E7;
    border-radius: 8px;
}

label {
    color: #526B7A !important;
    font-weight: 600 !important;
}


/* ---------- BUTTONS ---------- */

.stButton > button {
    background: #147D8C;
    color: #FFFFFF;
    border: 1px solid #147D8C;
    border-radius: 8px;
    font-weight: 650;
}

.stButton > button:hover {
    background: #105F6D;
    color: #FFFFFF;
}


/* ---------- DOWNLOAD BUTTONS ---------- */

[data-testid="stDownloadButton"] button {
    border-radius: 8px;
    font-weight: 650;
}


/* ---------- TABLES ---------- */

[data-testid="stDataFrame"] {
    border: 1px solid #DFE8EC;
    border-radius: 9px;
    background: #FFFFFF;
}


/* ---------- EXPANDERS ---------- */

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #DFE8EC;
    border-radius: 9px;
}


/* ---------- DIVIDERS ---------- */

hr {
    border-color: #DCE6EA !important;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}


/* ---------- CHARTS ---------- */

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border-radius: 10px;
}


/* ---------- FOOTER ---------- */

.app-footer {
    color: #82939D;
    text-align: center;
    font-size: 0.78rem;
    padding: 12px 0;
}


/* ---------- RESPONSIVE ---------- */

@media(max-width: 768px) {

    [data-testid="stMainBlockContainer"] {
        padding: 1rem;
    }

    .global-page-title {
        font-size: 1.7rem;
    }

    .page-title {
        font-size: 1.55rem;
    }

}

</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 2. SIDEBAR
# ============================================================

def render_sidebar(active="Overview"):

    with st.sidebar:

        st.markdown("## 🚇 METRO")

        st.caption("RIDERSHIP INTELLIGENCE")

        st.divider()

        st.markdown("##### WORKSPACE")

        for title, path, icon in NAVIGATION:

            if (APP_DIR / path).exists():

                st.page_link(
                    path,
                    label=title,
                    icon=icon,
                )

            else:

                st.caption(f"{icon} {title} · Coming soon")

        st.divider()

        st.caption("METRO ANALYTICS PLATFORM")
        st.caption("Historical Analytics")
        st.caption("Machine Learning Forecasting")
        st.caption("Version 1.0")


# ============================================================
# 3. PAGE SETUP
# ============================================================

def setup_page(
    title="Metro Ridership Intelligence",
    active="Overview"
):

    st.set_page_config(
        page_title=title,
        page_icon="🚇",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_global_styles()

    render_sidebar(active)


# ============================================================
# 4. PAGE HEADER
# ============================================================

def page_header(eyebrow, title, subtitle=""):

    safe_eyebrow = html.escape(str(eyebrow).upper())
    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))

    subtitle_html = ""

    if subtitle:

        subtitle_html = f"""
        <div class="global-page-subtitle">
            {safe_subtitle}
        </div>
        """

    st.markdown(
        f"""
        <div class="global-page-header">

            <div class="global-page-eyebrow">
                {safe_eyebrow}
            </div>

            <div class="global-page-title">
                {safe_title}
            </div>

            {subtitle_html}

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 5. SECTION HEADING
# ============================================================

def section_heading(title, description=None):

    safe_title = html.escape(str(title))

    st.markdown(
        f'<div class="section-title">{safe_title}</div>',
        unsafe_allow_html=True,
    )

    if description:

        safe_description = html.escape(str(description))

        st.markdown(
            f'<div class="section-description">{safe_description}</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# 6. CHART STYLING
# ============================================================

def show_chart(
    figure,
    height=320,
    use_container_width=True,
    key=None,
):

    if figure is None:
        return

    if height is None or height <= 0:
        height = 320

    figure.update_layout(
        height=height,
        autosize=True,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Segoe UI, Arial, sans-serif",
            color="#405967",
            size=12,
        ),

        title_font=dict(
            color="#173D50",
            size=16,
        ),

        margin=dict(
            l=48,
            r=22,
            t=35,
            b=48,
        ),

        hoverlabel=dict(
            bgcolor="#173F52",
            bordercolor="#147D8C",
            font=dict(
                color="#FFFFFF",
                size=12,
            ),
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(
                color="#405967",
                size=11,
            ),
        ),
    )

    figure.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#CCD9DF",
        tickfont=dict(
            color="#405967",
            size=11,
        ),
        title_font=dict(
            color="#405967",
            size=12,
        ),
        automargin=True,
    )

    figure.update_yaxes(
        showgrid=True,
        gridcolor="#EAF0F3",
        zeroline=False,
        linecolor="#CCD9DF",
        tickfont=dict(
            color="#405967",
            size=11,
        ),
        title_font=dict(
            color="#405967",
            size=12,
        ),
        automargin=True,
    )

    st.plotly_chart(
        figure,
        width="stretch" if use_container_width else "content",
        key=key,
        config={
            "displayModeBar": False,
            "displaylogo": False,
            "responsive": True,
        },
    )


# ============================================================
# 7. DATAFRAME
# ============================================================

def show_dataframe(
    dataframe,
    height=300,
    hide_index=True
):

    if dataframe is None or dataframe.empty:

        st.info("No records available.")

        return

    st.dataframe(
        dataframe,
        width="stretch",
        height=height,
        hide_index=hide_index,
    )


# ============================================================
# 8. EMPTY STATE
# ============================================================

def empty_state(title, message):

    st.info(
        f"**{title}**\n\n{message}"
    )


# ============================================================
# 9. FOOTER
# ============================================================

def footer():

    st.divider()

    st.markdown(
        "##### 🚇 METRO RIDERSHIP INTELLIGENCE"
    )

    st.caption(
        "Historical Demand Analysis · Predictive Forecasting · "
        "Model Evaluation · Operational Planning"
    )

    st.caption(
        "Synthetic dataset used for analytical demonstration. "
        "Not official metro operational data."
    )
