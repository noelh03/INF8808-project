'''
This file contains the code for the dot plot (viz5).
It includes generate_plot plus helpers to update axes, layout, and hover template.
'''
import math

import numpy as np
import pandas as pd
import plotly.express as px

from .hover_template import get_hover_template
from utils.constants import (
    BEESWARM_HALF_SPAN,
    BEESWARM_MAX_PER_STRIP,
    COL_NAME,
    COL_PLAYTIME,
    COL_SAT_ROUNDED,
    COL_VIS,
    COL_X_PLOT,
)


def _spread_indices_along_x(idx_order, offsets, x_lo, x_hi):
    """
        Fill horizontal offsets for indices ordered by y (one beeswarm strip).

        Args:
            idx_order: Indices in one bin, sorted by playtime.
            offsets: Full offset array (mutated in place).
            x_lo, x_hi: Horizontal span for this strip around rounded satisfaction.
    """
    m = len(idx_order)
    if m == 0:
        return
    if m == 1:
        offsets[idx_order[0]] = (x_lo + x_hi) / 2.0
        return
    offsets[idx_order] = np.linspace(x_lo, x_hi, m)


def _beeswarm_offsets_one_satisfaction(y):
    """
        X-offsets for one rounded-satisfaction group (Wilkinson-style beeswarm on playtime).

        Args:
            y (np.ndarray): Playtime values (hours) for games sharing the same rounded satisfaction.

        Returns:
            np.ndarray: Offsets to add to rounded satisfaction for plotting.
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    offsets = np.zeros(n, dtype=float)
    if n <= 1:
        return offsets

    ymin, ymax = float(y.min()), float(y.max())
    if ymax <= ymin + 1e-12:
        _spread_indices_along_x(np.argsort(y), offsets, -BEESWARM_HALF_SPAN, BEESWARM_HALF_SPAN)
        return offsets

    n_bins = int(np.clip(np.sqrt(n) * 3.2, 50, min(520, max(30, n // 2))))
    edges = np.linspace(ymin, ymax, n_bins + 1)
    b = np.clip(np.searchsorted(edges, y, side="right") - 1, 0, n_bins - 1)

    half = BEESWARM_HALF_SPAN
    max_row = BEESWARM_MAX_PER_STRIP

    for bin_id in range(n_bins):
        idx = np.where(b == bin_id)[0]
        if idx.size == 0:
            continue
        sub_y = y[idx]
        order = idx[np.argsort(sub_y, kind="mergesort")]
        m = order.size
        if m <= max_row:
            _spread_indices_along_x(order, offsets, -half, half)
            continue
        k = int(np.ceil(m / max_row))
        sub_width = (2.0 * half) / k
        for j in range(k):
            sl = slice(j * max_row, min((j + 1) * max_row, m))
            chunk = order[sl]
            cx = -half + sub_width * (j + 0.5)
            lo, hi = cx - 0.46 * sub_width, cx + 0.46 * sub_width
            _spread_indices_along_x(chunk, offsets, lo, hi)

    return offsets


def _add_beeswarm_x(df):
    """
        Add COL_X_PLOT = rounded satisfaction + per-group beeswarm offset.

        Args:
            df (pd.DataFrame): Filtered dataframe with COL_SAT_ROUNDED and COL_PLAYTIME.

        Returns:
            pd.DataFrame: Copy with COL_X_PLOT column.
    """
    out = df.copy()
    offsets_series = pd.Series(0.0, index=out.index, dtype=float)
    for _, sub in out.groupby(COL_SAT_ROUNDED, sort=False):
        off = _beeswarm_offsets_one_satisfaction(sub[COL_PLAYTIME].to_numpy(dtype=float))
        offsets_series.loc[sub.index] = off
    out[COL_X_PLOT] = out[COL_SAT_ROUNDED].astype(float) + offsets_series
    return out


def update_axes(fig, max_playtime=6000, data_max_playtime=None):
    '''
        Updates axis titles, ranges, and ticks. Y-axis may be shortened when most points
        sit well below the slider maximum (less empty vertical space).

        Args:
            fig: The figure to update.
            max_playtime: Slider upper bound (hours).
            data_max_playtime: Max playtime among points still shown after filtering.

        Returns:
            The updated figure.
    '''
    fig.update_xaxes(
        title_text="Satisfaction (arrondie)",
        range=[-0.07, 1.07],
        tickmode="linear",
        dtick=0.1,
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    n_ticks = 6
    if max_playtime == 0:
        y_dtick = 1
        padding = 1
        y_top = 1
    else:
        padding = max_playtime * 0.03
        full_top = max_playtime + padding
        if (
            data_max_playtime is not None
            and data_max_playtime > 0
            and data_max_playtime < max_playtime * 0.42
        ):
            y_top = min(
                full_top,
                max(data_max_playtime * 1.18, max_playtime * 0.07, 220.0) + padding * 0.6,
            )
        else:
            y_top = full_top

        y_span = max(y_top + padding, 1.0)
        raw_dtick = y_span / n_ticks
        magnitude = 10 ** math.floor(math.log10(max(raw_dtick, 1e-9)))
        y_dtick = max(1, round(raw_dtick / magnitude) * magnitude)

    fig.update_yaxes(
        title_text="Temps de jeu moyen (heures)",
        range=[-padding, y_top],
        tickmode="linear",
        dtick=y_dtick,
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    return fig


def update_layout(fig):
    '''
        Updates paper margins, fonts, and horizontal colorbar below the plot.

        Args:
            fig: The figure to update.

        Returns:
            The updated figure.
    '''
    fig.update_layout(
        autosize=True,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F7FB",
        margin=dict(l=56, r=8, t=12, b=78),
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
        coloraxis_colorbar=dict(
            orientation="h",
            title=dict(text="Nombre d'avis", side="top", font=dict(size=11)),
            x=0.5,
            xanchor="center",
            y=-0.24,
            yanchor="top",
            len=0.72,
            thickness=14,
            nticks=6,
            tickformat="~s",
            tickangle=0,
            outlinewidth=0,
        ),
    )

    return fig


def update_hover_template(fig):
    '''
        Sets the hover template on all traces.

        Args:
            fig: The figure to update.

        Returns:
            The updated figure.
    '''
    template = get_hover_template()
    fig.update_traces(hovertemplate=template)

    return fig


def generate_plot(df, max_playtime=6000):
    '''
        Generates the scatter plot: beeswarm x, playtime y, colour = visibility.

        Args:
            df: The dataframe to display (preprocessed).
            max_playtime: Upper bound on playtime (hours); rows above are excluded.

        Returns:
            The generated figure.
    '''
    required_columns = [COL_SAT_ROUNDED, COL_PLAYTIME, COL_VIS, COL_NAME]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    filtered_df = _add_beeswarm_x(df[df[COL_PLAYTIME] <= max_playtime])

    fig = px.scatter(
        filtered_df,
        x=COL_X_PLOT,
        y=COL_PLAYTIME,
        color=COL_VIS,
        hover_name=COL_NAME,
        custom_data=[COL_SAT_ROUNDED, COL_VIS],
        color_continuous_scale=[
            [0.0, "#6fb6ff"],
            [0.5, "#0062ff"],
            [1.0, "#0a1f6b"],
        ],
        opacity=0.42,
    )

    fig.update_traces(
        marker=dict(
            size=5,
            line=dict(width=0.4, color="rgba(255,255,255,0.45)"),
        ),
    )

    y_hi = float(filtered_df[COL_PLAYTIME].max()) if len(filtered_df) else None
    fig = update_axes(fig, max_playtime, y_hi)
    fig = update_layout(fig)
    fig = update_hover_template(fig)

    return fig
