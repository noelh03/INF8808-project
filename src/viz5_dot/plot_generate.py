'''
    This file contains the code for the plot.
'''
import math

import numpy as np
import pandas as pd
import plotly.express as px
from .hover_template import get_hover_template

COL_SAT = "Satisfaction rounded"
COL_PLAYTIME = "Playtime hours"
COL_VIS = "Visibility"
COL_NAME = "Name"
# Position X affichée : satisfaction arrondie + offset beeswarm
COL_X_PLOT = "_viz5_x_beeswarm"
# Demi-largeur max autour de chaque palier de satisfaction (ticks tous les 0,1)
_BEESWARM_HALF_SPAN = 0.044
# Au-delà de ce nombre de points sur une même bande de temps de jeu : sous-colonnes en x
_BEESWARM_MAX_PER_STRIP = 110


def _spread_indices_along_x(idx_order: np.ndarray, offsets: np.ndarray, x_lo: float, x_hi: float) -> None:
    """Remplit offsets pour les indices 0..n-1 (idx_order triés par y), répartis entre x_lo et x_hi."""
    m = len(idx_order)
    if m == 0:
        return
    if m == 1:
        offsets[idx_order[0]] = (x_lo + x_hi) / 2.0
        return
    offsets[idx_order] = np.linspace(x_lo, x_hi, m)


def _beeswarm_offsets_one_satisfaction(y: np.ndarray) -> np.ndarray:
    """
    Beeswarm (style Wilkinson / bandes) : fines tranches sur le temps de jeu ; dans chaque tranche,
    les points sont triés par y puis répartis horizontalement. Bande trop dense → plusieurs colonnes en x.
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    offsets = np.zeros(n, dtype=float)
    if n <= 1:
        return offsets

    ymin, ymax = float(y.min()), float(y.max())
    if ymax <= ymin + 1e-12:
        _spread_indices_along_x(np.argsort(y), offsets, -_BEESWARM_HALF_SPAN, _BEESWARM_HALF_SPAN)
        return offsets

    n_bins = int(np.clip(np.sqrt(n) * 3.2, 50, min(520, max(30, n // 2))))
    edges = np.linspace(ymin, ymax, n_bins + 1)
    b = np.clip(np.searchsorted(edges, y, side="right") - 1, 0, n_bins - 1)

    half = _BEESWARM_HALF_SPAN
    max_row = _BEESWARM_MAX_PER_STRIP

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


def _add_beeswarm_x(df: pd.DataFrame) -> pd.DataFrame:
    """
    Un beeswarm par palier de satisfaction arrondie. Le survol garde la vraie satisfaction (customdata).
    """
    out = df.copy()
    offsets_series = pd.Series(0.0, index=out.index, dtype=float)
    for _, sub in out.groupby(COL_SAT, sort=False):
        off = _beeswarm_offsets_one_satisfaction(sub[COL_PLAYTIME].to_numpy(dtype=float))
        offsets_series.loc[sub.index] = off
    out[COL_X_PLOT] = out[COL_SAT].astype(float) + offsets_series
    return out


def generate_plot(df, max_playtime=6000):
    '''
        Generates the plot.

        Args:
            df: The dataframe to display
            max_playtime: The maximum playtime to display (used for filtering the data)
        Returns:
            The generated figure
    '''
    filtered_df = _add_beeswarm_x(df[df[COL_PLAYTIME] <= max_playtime])

    fig = px.scatter(
        filtered_df,
        x=COL_X_PLOT,
        y=COL_PLAYTIME,
        color=COL_VIS,
        hover_name=COL_NAME,
        custom_data=[COL_SAT, COL_VIS],
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

    fig = update_axes(fig, max_playtime=max_playtime)
    fig = update_layout(fig)
    fig = update_hover_template(fig)

    return fig


def update_axes(fig, max_playtime=6000):
    '''
        Updates the axes labels with their corresponding titles and styling.

        Args:
            fig: The figure to be updated
            max_playtime: The maximum playtime to display (used for filtering the data)
        Returns:
            The updated figure
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
    else:
        raw_dtick = max_playtime / n_ticks
        padding = max_playtime * 0.03

        magnitude = 10 ** math.floor(math.log10(raw_dtick))
        y_dtick = round(raw_dtick / magnitude) * magnitude

    fig.update_yaxes(
        title_text="Temps de jeu moyen (heures)",
        range=[-padding, max_playtime + padding],
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
        Updates the layout of the figure.

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    fig.update_layout(
        autosize=True,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F7FB",
        margin=dict(l=72, r=24, t=52, b=62),
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
            title=dict(text="Nombre d'avis", side="right", font=dict(size=12)),
            x=0,
            y=1.06,
            xanchor="left",
            yanchor="bottom",
            len=0.42,
            thickness=12,
            nticks=6,
            tickformat="~s",
            outlinewidth=0,
        ),
    )

    return fig


def update_hover_template(fig):
    '''
        Sets the hover template of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''

    template = get_hover_template()
    fig.update_traces(hovertemplate=template)

    return fig
