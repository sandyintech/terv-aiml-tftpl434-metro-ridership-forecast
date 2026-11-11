from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import LINE_COLORS, LINE_ORDER


# ============================================================
# 1. GLOBAL CHART THEME
# ============================================================

CHART_BACKGROUND = "#FFFFFF"
PAPER_BACKGROUND = "#FFFFFF"

TEXT_COLOR = "#294B5A"
MUTED_TEXT = "#718795"

GRID_COLOR = "#E8EFF2"

PRIMARY_COLOR = "#1596A5"
SECONDARY_COLOR = "#F0A13A"

FONT_FAMILY = "Arial, sans-serif"


# ============================================================
# 2. COMMON CHART LAYOUT
# ============================================================

def apply_chart_style(
    fig,
    height=350,
    title=None,
    show_legend=True,
    hovermode="x unified",
):

    fig.update_layout(

        title=dict(
            text=title,
            font=dict(
                size=18,
                color=TEXT_COLOR,
                family=FONT_FAMILY,
            ),
            x=0.02,
            xanchor="left",
        ) if title else None,

        height=height,

        autosize=True,

        paper_bgcolor=PAPER_BACKGROUND,

        plot_bgcolor=CHART_BACKGROUND,

        font=dict(
            family=FONT_FAMILY,
            color=TEXT_COLOR,
            size=12,
        ),

        margin=dict(
            l=55,
            r=25,
            t=55 if title else 30,
            b=55,
        ),

        hovermode=hovermode,

        showlegend=show_legend,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0)",
            font=dict(
                size=11,
                color=TEXT_COLOR,
            ),
        ),

        hoverlabel=dict(
            bgcolor="#123F50",
            bordercolor="#123F50",
            font=dict(
                color="#FFFFFF",
                size=12,
                family=FONT_FAMILY,
            ),
        ),

    )

    fig.update_xaxes(

        showgrid=False,

        showline=True,

        linecolor="#D9E4E9",

        linewidth=1,

        tickfont=dict(
            color=MUTED_TEXT,
            size=11,
        ),

        title_font=dict(
            color=TEXT_COLOR,
            size=12,
        ),

        automargin=True,

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor=GRID_COLOR,

        gridwidth=1,

        zeroline=False,

        tickfont=dict(
            color=MUTED_TEXT,
            size=11,
        ),

        title_font=dict(
            color=TEXT_COLOR,
            size=12,
        ),

        automargin=True,

    )

    return fig


# ============================================================
# 3. LINE CHART
# ============================================================

def create_line_chart(
    df,
    x,
    y,
    color=None,
    title=None,
    x_title="Date",
    y_title="Ridership",
    height=350,
    markers=False,
):

    fig = px.line(

        df,

        x=x,

        y=y,

        color=color,

        markers=markers,

        color_discrete_map=LINE_COLORS,

        category_orders={
            "line": LINE_ORDER,
        },

    )

    fig.update_traces(

        line=dict(
            width=2.6,
        ),

        marker=dict(
            size=6,
        ),

    )

    fig.update_layout(

        xaxis_title=x_title,

        yaxis_title=y_title,

    )

    return apply_chart_style(
        fig,
        height=height,
        title=title,
    )


# ============================================================
# 4. RIDERSHIP TREND WITH MOVING AVERAGE
# ============================================================

def create_ridership_trend(
    df,
    date_column="date",
    value_column="network_ridership",
    rolling_window=7,
    height=380,
):

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce",
    )

    data[value_column] = pd.to_numeric(
        data[value_column],
        errors="coerce",
    )

    data = (
        data.dropna(subset=[date_column, value_column])
        .sort_values(date_column)
    )

    data["moving_average"] = (
        data[value_column]
        .rolling(
            rolling_window,
            min_periods=1,
        )
        .mean()
    )

    fig = go.Figure()

    # Daily ridership

    fig.add_trace(

        go.Scatter(

            x=data[date_column],

            y=data[value_column],

            name="Daily Ridership",

            mode="lines",

            line=dict(
                color="#1596A5",
                width=1.8,
            ),

            fill="tozeroy",

            fillcolor="rgba(21,150,165,0.10)",

            hovertemplate=(
                "<b>%{x|%d %b %Y}</b>"
                "<br>Ridership: %{y:,.0f}"
                "<extra></extra>"
            ),

        )

    )

    # Moving average

    fig.add_trace(

        go.Scatter(

            x=data[date_column],

            y=data["moving_average"],

            name=f"{rolling_window}-Day Moving Average",

            mode="lines",

            line=dict(
                color="#F0A13A",
                width=3,
            ),

            hovertemplate=(
                "Moving Average: %{y:,.0f}"
                "<extra></extra>"
            ),

        )

    )

    fig.update_layout(

        xaxis_title="Date",

        yaxis_title="Passenger Journeys",

    )

    fig.update_xaxes(
        tickformat="%b\n%Y",
        dtick="M3",
    )

    fig.update_yaxes(
        tickformat="~s",
    )

    return apply_chart_style(
        fig,
        height=height,
        title="Daily Ridership Trend",
    )


# ============================================================
# 5. BAR CHART
# ============================================================

def create_bar_chart(
    df,
    x,
    y,
    color=None,
    title=None,
    x_title=None,
    y_title=None,
    height=350,
    orientation="v",
):

    fig = px.bar(

        df,

        x=x,

        y=y,

        color=color,

        color_discrete_map=LINE_COLORS,

        orientation=orientation,

        text_auto=".2s",

    )

    fig.update_traces(

        marker_line_width=0,

        textposition="outside",

        cliponaxis=False,

        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Value: %{y:,.0f}"
            "<extra></extra>"
        ),

    )

    fig.update_layout(

        xaxis_title=x_title,

        yaxis_title=y_title,

    )

    if orientation == "v":

        fig.update_yaxes(
            tickformat="~s",
        )

    else:

        fig.update_xaxes(
            tickformat="~s",
        )

    return apply_chart_style(
        fig,
        height=height,
        title=title,
        hovermode="closest",
    )


# ============================================================
# 6. DONUT CHART
# ============================================================

def create_donut_chart(
    df,
    names,
    values,
    title=None,
    height=350,
):

    fig = px.pie(

        df,

        names=names,

        values=values,

        hole=0.65,

        color=names,

        color_discrete_map=LINE_COLORS,

    )

    fig.update_traces(

        textposition="inside",

        texttemplate="%{label}<br>%{percent}",

        marker=dict(

            line=dict(
                color="#FFFFFF",
                width=3,
            )

        ),

        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Passengers: %{value:,.0f}"
            "<br>Contribution: %{percent}"
            "<extra></extra>"
        ),

    )

    fig.update_layout(

        showlegend=False,

        margin=dict(
            l=15,
            r=15,
            t=30,
            b=15,
        ),

    )

    return apply_chart_style(

        fig,

        height=height,

        title=title,

        show_legend=False,

        hovermode="closest",

    )


# ============================================================
# 7. AREA CHART
# ============================================================

def create_area_chart(
    df,
    x,
    y,
    color=None,
    title=None,
    height=350,
):

    fig = px.area(

        df,

        x=x,

        y=y,

        color=color,

        color_discrete_map=LINE_COLORS,

    )

    fig.update_traces(

        line=dict(
            width=2,
        ),

        opacity=0.75,

    )

    return apply_chart_style(

        fig,

        height=height,

        title=title,

    )


# ============================================================
# 8. SCATTER CHART
# ============================================================

def create_scatter_chart(
    df,
    x,
    y,
    color=None,
    title=None,
    height=350,
):

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color=color,

        color_discrete_map=LINE_COLORS,

        opacity=0.75,

    )

    fig.update_traces(

        marker=dict(
            size=9,
            line=dict(
                width=1,
                color="#FFFFFF",
            ),
        ),

    )

    return apply_chart_style(

        fig,

        height=height,

        title=title,

    )


# ============================================================
# 9. HEATMAP
# ============================================================

def create_heatmap(
    df,
    x,
    y,
    values,
    title=None,
    height=400,
):

    fig = px.density_heatmap(

        df,

        x=x,

        y=y,

        z=values,

        histfunc="avg",

        color_continuous_scale=[
            "#EAF7F7",
            "#A7DDDC",
            "#49B7B8",
            "#168A98",
            "#103F58",
        ],

    )

    fig.update_coloraxes(

        colorbar=dict(
            title="Average",
            tickfont=dict(
                color=TEXT_COLOR,
            ),
        )

    )

    return apply_chart_style(

        fig,

        height=height,

        title=title,

        hovermode="closest",

    )


# ============================================================
# 10. ACTUAL VS PREDICTED CHART
# ============================================================

def create_actual_vs_predicted(
    df,
    date_column="date",
    actual_column="actual",
    predicted_column="predicted",
    height=380,
):

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce",
    )

    data = (
        data.dropna(
            subset=[
                date_column,
                actual_column,
                predicted_column,
            ]
        )
        .sort_values(date_column)
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=data[date_column],

            y=data[actual_column],

            name="Actual Ridership",

            mode="lines",

            line=dict(
                color="#1596A5",
                width=2.5,
            ),

        )

    )

    fig.add_trace(

        go.Scatter(

            x=data[date_column],

            y=data[predicted_column],

            name="Predicted Ridership",

            mode="lines",

            line=dict(
                color="#F0A13A",
                width=2.5,
                dash="dash",
            ),

        )

    )

    fig.update_layout(

        xaxis_title="Date",

        yaxis_title="Passenger Journeys",

    )

    fig.update_xaxes(
        tickformat="%b\n%Y",
    )

    fig.update_yaxes(
        tickformat="~s",
    )

    return apply_chart_style(

        fig,

        height=height,

        title="Actual vs Predicted Ridership",

    )


# ============================================================
# 11. RESIDUAL DISTRIBUTION
# ============================================================

def create_residual_chart(
    df,
    residual_column="residual",
    height=350,
):

    data = df.copy()

    data[residual_column] = pd.to_numeric(
        data[residual_column],
        errors="coerce",
    )

    data = data.dropna(
        subset=[residual_column]
    )

    fig = px.histogram(

        data,

        x=residual_column,

        nbins=35,

        color_discrete_sequence=[
            "#1596A5",
        ],

    )

    fig.update_traces(

        marker_line=dict(
            color="#FFFFFF",
            width=1,
        ),

        hovertemplate=(
            "Residual: %{x:,.0f}"
            "<br>Frequency: %{y}"
            "<extra></extra>"
        ),

    )

    fig.add_vline(

        x=0,

        line_dash="dash",

        line_color="#E69A38",

        line_width=2,

    )

    fig.update_layout(

        xaxis_title="Prediction Error",

        yaxis_title="Frequency",

    )

    return apply_chart_style(

        fig,

        height=height,

        title="Residual Error Distribution",

        hovermode="closest",

    )