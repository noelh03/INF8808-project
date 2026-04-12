'''
    This file contains the code for the plot.
'''

import plotly.express as px
import math
from .hover_template import get_hover_template

COL_SAT = "Satisfaction"
COL_VIS = "Visibility"
COL_OWNERS = "Estimated owners (average)"
COL_NAME = "Name"

def generate_plot(df, max_visibility=None, sat_range=None):
    '''
        Generates the plot.

        Args:
            df: The dataframe to display
            max_visibility: The maximum visibility to display (used for filtering the data)
            sat_range: A tuple containing the minimum and maximum satisfaction values to display (used for filtering the data)
        Returns:
            The generated figure
    '''
    
    required_columns = [COL_SAT, COL_VIS, COL_OWNERS, COL_NAME]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    filtered_df = df.copy()

    if max_visibility is not None:
        filtered_df = filtered_df[filtered_df[COL_VIS] <= max_visibility]
    if sat_range is not None:
        filtered_df = filtered_df[
            (filtered_df[COL_SAT] >= sat_range[0]) &
            (filtered_df[COL_SAT] <= sat_range[1])
        ]

    fig = px.scatter(
        filtered_df,
        x=COL_SAT,
        y=COL_VIS,
        size=COL_OWNERS,
        hover_name=COL_NAME,
        log_y=False,
        opacity=0.6,
        size_max=60,
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=0),
        )
    )
    
    fig = update_axes(fig, max_visibility=max_visibility, sat_range=sat_range)
    fig = update_layout(fig)
    fig = update_hover_template(fig)

    return fig

def update_axes(fig, max_visibility=None, sat_range=None):
    '''
        Updates the axes labels with their corresponding titles and styling.

        Args:
            fig: The figure to be updated
            max_visibility: The maximum visibility to display
            sat_range: A tuple containing the minimum and maximum satisfaction values to display
        Returns:
            The updated figure
    '''
    
    n_ticks = 10
    if max_visibility == 0:
        y_dtick = 1
    else:
        raw_dtick = max_visibility / n_ticks
        
        magnitude = 10 ** math.floor(math.log10(raw_dtick))
        y_dtick = round(raw_dtick / magnitude) * magnitude

    padding = max_visibility * 0.03 if max_visibility > 0 else 1
    
    fig.update_xaxes(
        title_text="Satisfaction (ratio)",
        range=[-0.02 + sat_range[0], sat_range[1] + 0.02] if sat_range else None,
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
    
    fig.update_yaxes(
        title_text="Visibilité (nombre d’avis)",
        range=[-padding, max_visibility + padding],
        tickmode="linear",
        dtick=y_dtick,
        tickformat="~s",
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
        Updates the layout of the figure with styling and formatting.

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
        margin=dict(l=72, r=130, t=28, b=62),
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
        transition=dict(
            duration=500,
            easing="cubic-in-out"
        )
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