"""Shared chart theming — one categorical order, applied consistently across pages."""

import plotly.graph_objects as go

# Fixed categorical hue order — never cycle, never reassign by rank.
CATEGORICAL = [
    "#2a78d6",  # 1 blue
    "#1baf7a",  # 2 aqua
    "#eda100",  # 3 yellow
    "#008300",  # 4 green
    "#4a3aa7",  # 5 violet
    "#e34948",  # 6 red
    "#e87ba4",  # 7 magenta
    "#eb6834",  # 8 orange
]

SEQUENTIAL_BLUE = ["#cde2fb", "#9ec5f4", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]

STATUS = {
    "good": "#0ca30c",
    "warning": "#fab219",
    "serious": "#ec835a",
    "critical": "#d03b3b",
}

INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

FONT_FAMILY = "system-ui, -apple-system, 'Segoe UI', sans-serif"


def series_color(index: int) -> str:
    return CATEGORICAL[index % len(CATEGORICAL)]


def style_fig(fig: go.Figure, *, show_legend: bool | None = None, y_suffix: str = "") -> go.Figure:
    """Apply consistent chrome: transparent surface, recessive gridlines, thin marks."""
    n_traces = len(fig.data)
    if show_legend is None:
        show_legend = n_traces >= 2

    has_title = bool(fig.layout.title.text)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=INK_SECONDARY, size=13),
        title=dict(font=dict(family=FONT_FAMILY, color=INK_PRIMARY, size=16)),
        # Vertical legend on the right (Plotly's default position) never collides with a
        # top-left title, unlike a horizontal legend hand-placed above the plot area.
        legend=dict(
            visible=show_legend,
            title_text="",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(color=INK_SECONDARY, size=12),
        ),
        margin=dict(l=10, r=10, t=50 if has_title else 20, b=10),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#fcfcfb", font=dict(family=FONT_FAMILY, color=INK_PRIMARY)),
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linecolor=BASELINE,
        tickfont=dict(color=INK_MUTED, size=12),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRIDLINE,
        zeroline=False,
        showline=False,
        tickfont=dict(color=INK_MUTED, size=12),
        ticksuffix=y_suffix,
    )
    return fig


def line_defaults() -> dict:
    return dict(line=dict(width=2.5), marker=dict(size=8))


def bar_defaults() -> dict:
    return dict(marker_line_width=0)
