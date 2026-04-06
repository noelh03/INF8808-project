'''
    This file contains the code for the plot.
'''
import math

import plotly.express as px
from .hover_template import get_hover_template

COL_SAT = "Satisfaction rounded"
COL_PLAYTIME = "Playtime hours"
COL_VIS = "Visibility"
COL_NAME = "Name"


def generate_plot(df, max_playtime=6000):
    '''
        Generates the plot.

        Args:
            df: The dataframe to display
            max_playtime: The maximum playtime to display (used for filtering the data)
        Returns:
            The generated figure
    '''
    filtered_df = df[df[COL_PLAYTIME] <= max_playtime]

    fig = px.scatter(
        filtered_df,
        x=COL_SAT,
        y=COL_PLAYTIME,
        color=COL_VIS,
        hover_name=COL_NAME,
        color_continuous_scale=[
            [0.0, "#6fb6ff"],
            [0.5, "#0062ff"],
            [1.0, "#0a1f6b"],
        ],
        opacity=0.65,
    )

    fig.update_traces(
        marker=dict(size=7),
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
        range=[-0.02, 1.02],
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
        # Même esprit que viz3 (ligne) : tracé pleine hauteur, peu de marge perdue
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
        # Barre de couleur horizontale en haut, comme la légende de la viz3
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