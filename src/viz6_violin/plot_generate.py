'''
    This file contains the code for the plot.
'''

import plotly.express as px

from . import hover_template

def generate_plot(my_df):
    '''
        Generates the plot.
        Args:
            my_df: The dataframe to display
        Returns:
            The generated figure
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
        color_discrete_map={
            "Independent": "#6fb6ff",
            "Major": "#D98A6C"
        }
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
        Updates the axes labels with their corresponding titles.

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
        categoryarray=[
            "0 - 20000",
            "20000 - 50000",
            "50000 - 100000",
            "100000 - 200000",
            "200000 - 500000",
            "500000 - 1000000",
            "1000000 - 2000000",
            "2000000 - 5000000",
            "5000000 - 10000000",
            "10000000 - 20000000"
        ],
        tickvals=[
            "0 - 20000",
            "20000 - 50000",
            "50000 - 100000",
            "100000 - 200000",
            "200000 - 500000",
            "500000 - 1000000",
            "1000000 - 2000000",
            "2000000 - 5000000",
            "5000000 - 10000000",
            "10000000 - 20000000"
        ],
        ticktext=[
            "0 - 20k",
            "20k - 50k",
            "50k - 100k",
            "100k - 200k",
            "200k - 500k",
            "500k - 1M",
            "1M - 2M",
            "2M - 5M",
            "5M - 10M",
            "10M - 20M"
        ],
    )
 
    return fig
 

def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    fig.update_layout(
        dragmode=False
    )
    return fig
 
def update_legend(fig):
    '''
        Updated the legend title

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
        margin=dict(l=72, r=24, t=52, b=62),
        legend=dict(
            orientation="h",
            x=0,
            y=1.05,
            xanchor="left",
            yanchor="bottom",
            title_text="Type d'éditeur",
        ),
        violingap=0.05,
        violinmode="overlay",
    )
    return fig
 
def update_hover_template(fig):
    template = hover_template.get_hover_template()
    fig.update_traces(hovertemplate=template)
    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = template
    return fig
 
def update_layout(fig):
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
        legend_title_text="Type d'éditeur",
        violingap=0.05,
        violinmode="overlay",
    )
    return fig

def filter_by_max_games(my_df, max_games):
    '''
        Filters the dataframe to only keep rows where nb_games_dev <= max_games.
        Called by the slider callback before regenerating the figure.
 
        Args:
            my_df     : preprocessed dataframe
            max_games : int, maximum value of nb_games_dev to display
        Returns:
            Filtered dataframe
    '''
    return my_df[my_df['nb_games_dev'] <= max_games]