"""
Visualization generation module for the genre evolution multi-series line chart.

This module:
- renders each minor genre as its own thin gray line (background context)
- renders each main genre as a bold colored line on top
- applies smooth spline interpolation to soften the curves
- styles axes, legend, and hover labels consistently with the project theme
- supports dynamic filtering: main genres toggle individually, all minor genres
  toggle together via the "Others" checkbox
"""

import plotly.graph_objects as go
from .hover_template import get_hover_template
from .preprocess import MAIN_GENRES, get_other_genres, YEAR_MIN, YEAR_MAX

GENRE_COLORS = {
    "Action": "#F4A535",
    "Adventure": "#E91E8C",
    "Indie": "#9C27B0",
    "Massively Multiplayer": "#B71C1C",
    "Free To Play": "#43A047",
    "RPG": "#1565C0",
}

OTHERS_COLOR = "#B0BAC9"
CHECKLIST_GENRES = MAIN_GENRES + ["Others"]


def generate_plot(df_long, selected_genres=None):
    """
    Build the multi-series line figure from long-format data.

    Minor genres are each drawn as a thin gray line (grouped under "Others").
    Main genres are drawn as bold colored lines on top.

    Args:
        df_long: Long-format DataFrame with columns [Year, Genre, Owners].
        selected_genres: List of checklist values that are currently active.
                         Main genre names control their own trace; "Others"
                         controls all minor genre traces together.

    Returns:
        go.Figure: The fully configured Plotly figure.
    """
    if selected_genres is None:
        selected_genres = CHECKLIST_GENRES

    other_genres = get_other_genres(df_long)
    show_others = "Others" in selected_genres

    visible_main = [g for g in MAIN_GENRES if g in selected_genres]
    visible_other = other_genres if show_others else []
    visible_genres = visible_main + list(visible_other)

    if visible_genres:
        mask = df_long["Genre"].isin(visible_genres)
        visible_df = df_long[mask]
        y_max = visible_df["Owners"].max() * 1.08  # 8 % headroom
        x_range = [YEAR_MIN, YEAR_MAX]
        y_range = [0, y_max]
    else:
        x_range = [YEAR_MIN, YEAR_MAX]
        y_range = [0, 700_000_000]

    fig = go.Figure()

    # Minor genres: one gray trace each, only when "Others" is checked
    if show_others:
        first_other = True
        for genre in other_genres:
            genre_df = df_long[df_long["Genre"] == genre].sort_values("Year")
            if genre_df["Owners"].sum() == 0:
                continue

            fig.add_trace(
                go.Scatter(
                    x=genre_df["Year"],
                    y=genre_df["Owners"],
                    mode="lines",
                    name="Others",
                    legendgroup="others",
                    showlegend=first_other,
                    line=dict(
                        color=OTHERS_COLOR,
                        width=1.2,
                        shape="spline",
                        smoothing=0.8,
                    ),
                    opacity=0.55,
                    customdata=[[genre]] * len(genre_df),
                    hovertemplate=get_hover_template(),
                )
            )
            first_other = False

    # Main genres: one colored trace each, only when that genre is checked
    for genre in MAIN_GENRES:
        if genre not in selected_genres:
            continue

        genre_df = df_long[df_long["Genre"] == genre].sort_values("Year")
        fig.add_trace(
            go.Scatter(
                x=genre_df["Year"],
                y=genre_df["Owners"],
                mode="lines",
                name=genre,
                line=dict(
                    color=GENRE_COLORS[genre],
                    width=2.8,
                    shape="spline",
                    smoothing=0.8,
                ),
                customdata=[[genre]] * len(genre_df),
                hovertemplate=get_hover_template(),
            )
        )

    fig.update_layout(
        autosize=True,
        showlegend=True,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F7FB",
        margin=dict(l=72, r=20, t=56, b=62),
        font=dict(
            family="Inter, Arial, sans-serif",
            size=13,
            color="#2E4057",
        ),
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
            xanchor="left",
            yanchor="bottom",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color="#2E4057"),
            itemclick="toggle",
            itemdoubleclick="toggleothers",
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
        hovermode="closest",
    )

    fig.update_xaxes(
        title_text="Année de sortie",
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        dtick=2,
        range=x_range,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    fig.update_yaxes(
        title_text="Propriétaires estimés",
        tickformat=",",
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=y_range,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    return fig
