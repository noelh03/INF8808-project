'''
    Contains the functions to generate and style the violin plot.
'''

import plotly.express as px

from . import hover_template
from .preprocess import OWNER_ORDER

OWNER_TICK_LABELS = [
    "0 - 20k",
    "20k - 50k",
    "50k - 100k",
    "100k - 200k",
    "200k - 500k",
    "500k - 1M",
    "1M - 2M",
    "2M - 5M",
    "5M - 10M",
    "10M - 20M",
]

PUBLISHER_COLORS = {
    "Independent": "#6fb6ff",
    "Major": "#D98A6C",
}


def generate_plot(my_df):
    '''
        Generates the violin plot figure with all styling applied.

        Args:
            my_df: Preprocessed DataFrame with columns nb_games_dev,
                   estimated_owners, publisher_type, and name
        Returns:
            The fully styled Plotly figure
    '''
    fig = px.violin(
        my_df,
        x="nb_games_dev",
        y="estimated_owners",
        color="publisher_type",
        hover_name="name",
        box=True,
        points="all",
        orientation="h",
        color_discrete_map=PUBLISHER_COLORS,
    )

    fig.update_traces(
        line=dict(width=1),
        meanline_visible=True,
        opacity=0.7,
        marker=dict(size=4, opacity=0.5),
        pointpos=0,
        jitter=0.3,
    )

    fig = update_axes_labels(fig)
    fig = update_layout(fig)
    fig = update_hover_template(fig)

    return fig


def update_axes_labels(fig):
    '''
        Updates the x and y axes titles, grid styling, and tick formatting.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    fig.update_xaxes(
        title_text="Nombre de jeux publiés (expérience développeur)",
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    fig.update_yaxes(
        title_text="Succès commercial (Estimated Owners)",
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
        categoryorder="array",
        categoryarray=OWNER_ORDER,
        tickvals=OWNER_ORDER,
        ticktext=OWNER_TICK_LABELS,
    )

    return fig


def update_layout(fig):
    '''
        Applies the full layout styling: theme, colors, fonts, margins,
        legend position, and violin display options.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    fig.update_layout(
        autosize=True,
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
        legend=dict(
            title_text="Type d'éditeur",
            orientation="h",
            x=0,
            y=1.05,
            xanchor="left",
            yanchor="bottom",
        ),
        violingap=0.05,
        violinmode="overlay",
    )
    return fig


def update_hover_template(fig):
    '''
        Applies the hover tooltip template to all traces.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    fig.update_traces(hovertemplate=hover_template.get_hover_template())
    return fig


def filter_by_max_games(my_df, max_games):
    '''
        Filters the dataframe to only keep rows where nb_games_dev <= max_games.
        Called by the slider callback before regenerating the figure.

        Args:
            my_df     : Preprocessed DataFrame
            max_games : int, maximum value of nb_games_dev to display
        Returns:
            Filtered DataFrame
    '''
    return my_df[my_df['nb_games_dev'] <= max_games]