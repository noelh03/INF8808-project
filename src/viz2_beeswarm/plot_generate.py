"""
Visualization generation module for the beeswarm plot of commercial success by play mode.

This module:
- samples owner counts log-uniformly and stacks points into true beeswarm columns
- renders one scatter trace per play mode (Solo, Hybride, Multijoueur)
- overlays Q1/Q3 statistical markers as vertical dashed lines
- styles axes, legend, and hover labels consistently with the project theme
"""
import numpy as np
import plotly.graph_objects as go

from .hover_template import get_hover_template
from utils.constants import (COL_GAME_TYPE, COL_NAME, COL_OWNERS, COL_OWNERS_AVG, GAME_TYPE_ORDER, CATEGORY_CENTER, SAMPLE_PER_CATEGORY, LOG_BIN_WIDTH, Y_STEP, HALF_WIDTH, COLORS)


def _beeswarm_y(x_vals, center):
    """
    Compute y-positions for a beeswarm row.

    Args:
        x_vals: 1-D array of x-values (owner counts, positive).
        center: Numeric y-centre for this row.

    Returns:
        np.ndarray: 1-D array of y-positions, same length as x_vals.
    """
    x_log = np.log10(np.maximum(x_vals, 1.0))
    bin_idx = np.floor(x_log / LOG_BIN_WIDTH).astype(int)

    y = np.full(len(x_vals), float(center))
    for b in np.unique(bin_idx):
        indices = np.where(bin_idx == b)[0]
        n = len(indices)
        if n == 1:
            continue
        offsets = (np.arange(n) - (n - 1) / 2.0) * Y_STEP
        y[indices] = center + offsets

    return np.clip(y, center - HALF_WIDTH, center + HALF_WIDTH)


def _owners_midpoint(range_str):
    """
    Compute the midpoint of a Steam ownership range string.

    Args:
        range_str: String like '20,000 - 50,000'.

    Returns:
        float: Midpoint value, or np.nan if parsing fails.
    """
    if not isinstance(range_str, str):
        return np.nan
    parts = range_str.split(" - ")
    if len(parts) != 2:
        return np.nan
    try:
        lo = int(parts[0].replace(",", "").strip())
        hi = int(parts[1].replace(",", "").strip())
        return (lo + hi) / 2
    except ValueError:
        return np.nan


def _format_owners(value):
    """
    Format an owner count as a short human-readable string.

    Args:
        value: Numeric owner count.

    Returns:
        str: Formatted string such as '10 k' or '1.5 M'.
    """
    if value >= 1_000_000:
        v = value / 1_000_000
        s = f"{v:.1f}".rstrip("0").rstrip(".")
        return f"{s} M"
    if value >= 1_000:
        return f"{int(value / 1_000)} k"
    return f"{int(value)}"


def _format_range(range_str):
    """
    Format a Steam ownership range string into a compact human-readable form.

    Args:
        range_str: String like '20,000 - 50,000'.

    Returns:
        str: Formatted string such as '20 k - 50 k'.
    """
    if not isinstance(range_str, str):
        return str(range_str)
    parts = range_str.split(" - ")
    if len(parts) != 2:
        return range_str

    def fmt(v):
        try:
            n = int(v.replace(",", "").strip())
            return _format_owners(n)
        except ValueError:
            return v

    return f"{fmt(parts[0])} - {fmt(parts[1])}"


def generate_plot(df):
    """
    Build the beeswarm figure with swarm points and statistical markers.

    Args:
        df: Preprocessed DataFrame.

    Returns:
        go.Figure: Beeswarm figure with traces and Q1/Q3 line shapes.
    """
    fig = go.Figure()

    for game_type in GAME_TYPE_ORDER:
        subset = df[df[COL_GAME_TYPE] == game_type].copy()
        center = CATEGORY_CENTER[game_type]
        color = COLORS[game_type]

        n = min(SAMPLE_PER_CATEGORY, len(subset))
        sample = subset.sample(n=n, random_state=42)

        x_vals = sample[COL_OWNERS_AVG].values
        y_vals = _beeswarm_y(x_vals, center)

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers',
            name=game_type,
            marker=dict(
                color=color,
                size=5,
                opacity=0.90,
                line=dict(width=0),
            ),
            customdata=np.column_stack([
                sample[COL_NAME].values,
                [_format_range(r) for r in sample[COL_OWNERS].values],
            ]),
            hovertemplate=get_hover_template(),
        ))

        midpoints = subset[COL_OWNERS].apply(_owners_midpoint)
        q1_val     = midpoints.quantile(0.25)
        q3_val     = midpoints.quantile(0.75)
        median_val = midpoints.median()

        if q1_val == q3_val:
            lines = [(median_val, "solid", 3.0, f"  Médiane : {_format_owners(median_val)}")]
        else:
            lines = [
                (q1_val, "dot", 3.0, f"  Q1 : {_format_owners(q1_val)}"),
                (q3_val, "dot", 3.0, f"  Q3 : {_format_owners(q3_val)}"),
            ]

        for x_val, dash, width, label in lines:
            fig.add_shape(
                type="line",
                x0=x_val, x1=x_val,
                y0=center - HALF_WIDTH, y1=center + HALF_WIDTH,
                xref="x", yref="y",
                line=dict(color=color, width=width, dash=dash),
                layer="above",
            )
            fig.add_trace(go.Scatter(
                x=[x_val],
                y=[center + HALF_WIDTH * 0.72],
                mode="text",
                text=[label],
                textposition="middle right",
                textfont=dict(size=11, color="#2E4057", family="Inter, Arial, sans-serif"),
                showlegend=False,
                hoverinfo="skip",
            ))

    for y_sep in [0.5, 1.5]:
        fig.add_hline(
            y=y_sep,
            line=dict(color="#DCE6F2", width=1),
            layer="below",
        )

    return fig


def update_template(fig):
    """
    Apply the visual theme to the figure.

    Args:
        fig: Plotly figure to update.

    Returns:
        go.Figure: Figure with updated layout theme.
    """
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F7FB",
        font=dict(
            family="Inter, Arial, sans-serif",
            size=13,
            color="#2E4057",
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D9E2F2",
            font=dict(
                family="Inter, Arial, sans-serif",
                size=12,
                color="#2E4057",
            ),
        ),
        margin=dict(l=130, r=40, t=28, b=72),
        autosize=True,
    )
    return fig


def update_legend(fig):
    """
    Configure the legend position and style.

    Args:
        fig: Plotly figure to update.

    Returns:
        go.Figure: Figure with updated legend settings.
    """
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.0,
            y=1.0,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#D9E2F2",
            borderwidth=1,
            font=dict(size=12),
        ),
    )
    return fig


def update_axes_labels(fig):
    """
    Set axis titles, log scale on X, and named category ticks on Y.

    Args:
        fig: Plotly figure to update.

    Returns:
        go.Figure: Figure with updated axis configuration.
    """
    fig.update_xaxes(
        title_text="Succès commercial estimé (propriétaires)",
        type="log",
        tickvals=[1e4, 1e5, 1e6, 1e7, 1e8],
        ticktext=["10k", "100k", "1M", "10M", "100M"],
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=14, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )
    fig.update_yaxes(
        title_text="Mode de jeu",
        tickvals=[0, 1, 2],
        ticktext=["Multijoueur", "Hybride", "Solo"],
        range=[-0.6, 2.6],
        showgrid=False,
        zeroline=False,
        showline=False,
        title_font=dict(size=14, color="#2E4057"),
        tickfont=dict(size=13, color="#506784"),
    )
    return fig


def update_hover_template(fig):
    """
    Hover templates are set per-trace in generate_plot; this is a no-op.

    Args:
        fig: Plotly figure to update.

    Returns:
        go.Figure: Unchanged figure.
    """
    return fig
