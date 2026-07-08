"""Small chart-builder wrappers around plotly.express, pre-wired to the shared theme."""

import pandas as pd
import plotly.express as px

from .theme import CATEGORICAL, SEQUENTIAL_BLUE, style_fig


def ordinal_ramp(n: int) -> list[str]:
    """n evenly spaced steps along the single-hue sequential ramp, light -> dark."""
    if n <= 1:
        return [SEQUENTIAL_BLUE[-1]]
    return px.colors.sample_colorscale(SEQUENTIAL_BLUE, [i / (n - 1) for i in range(n)])


_DIVERGING_SCALE = ["#0d366b", "#2a78d6", "#9ec5f4", "#e1e0d9", "#f0b3b2", "#e34948", "#8c1f1f"]


def diverging_ramp(n: int) -> list[str]:
    """n evenly spaced steps blue -> gray -> red, for bipolar (not good/bad) scales."""
    if n <= 1:
        return [_DIVERGING_SCALE[len(_DIVERGING_SCALE) // 2]]
    return px.colors.sample_colorscale(_DIVERGING_SCALE, [i / (n - 1) for i in range(n)])


def trend_line(df: pd.DataFrame, *, x="year", y="value", color="series", title="", y_suffix="") -> "px.Figure":
    # `year` mixes plain years with strings like "2021/22" (ESS round 10 spanned two years),
    # so it's always a string column — force a category axis or Plotly silently mis-coerces it
    # to numeric/date and mis-plots the mixed-format point.
    order = None
    if x == "year" and "ess_round" in df.columns:
        order = df.sort_values("ess_round")[x].drop_duplicates().tolist()

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=True,
        title=title,
        color_discrete_sequence=CATEGORICAL,
        category_orders={x: order} if order else None,
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig.update_xaxes(type="category")
    return style_fig(fig, y_suffix=y_suffix)


def grouped_bar(df: pd.DataFrame, *, x, y="value", color, title="", barmode="group", y_suffix="%", order=None) -> "px.Figure":
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode=barmode,
        title=title,
        color_discrete_sequence=CATEGORICAL,
        category_orders={x: order} if order else None,
    )
    return style_fig(fig, y_suffix=y_suffix)


def stacked_percent_bar(df: pd.DataFrame, *, x, y="value", color, title="", order=None, category_order=None, color_sequence=None) -> "px.Figure":
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode="stack",
        title=title,
        color_discrete_sequence=color_sequence or CATEGORICAL,
        category_orders={
            **({x: order} if order else {}),
            **({color: category_order} if category_order else {}),
        },
    )
    return style_fig(fig, y_suffix="%")


def horizontal_bar(df: pd.DataFrame, *, x="value", y, color=None, title="", y_suffix="%", order=None) -> "px.Figure":
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation="h",
        title=title,
        color_discrete_sequence=CATEGORICAL,
        category_orders={y: order} if order else None,
    )
    fig.update_xaxes(ticksuffix=y_suffix)
    return style_fig(fig, y_suffix="")


def horizontal_stacked_bar(df: pd.DataFrame, *, y, x="value", color, title="", order=None, category_order=None, color_sequence=None) -> "px.Figure":
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation="h",
        barmode="stack",
        title=title,
        color_discrete_sequence=color_sequence or CATEGORICAL,
        category_orders={
            **({y: order} if order else {}),
            **({color: category_order} if category_order else {}),
        },
    )
    fig.update_xaxes(ticksuffix="%")
    return style_fig(fig, y_suffix="")
