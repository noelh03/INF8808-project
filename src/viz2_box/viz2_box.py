'''
    Contains source code for the second visualisation of the project.
    Beeswarm plot showing commercial success (Estimated owners)
    by game play mode (Solo, Hybride, Multijoueur).
'''
from dash import html, dcc

import viz2_box.preprocess
import viz2_box.plot_generate


def create_figure(my_df):
    '''
    Preprocesses the data and generates the beeswarm figure.

    Args:
        my_df: Raw games DataFrame.
    Returns:
        Plotly figure.
    '''
    my_df = viz2_box.preprocess.step1(my_df)
    my_df = viz2_box.preprocess.step2(my_df)

    fig = viz2_box.plot_generate.generate_plot(my_df)
    fig = viz2_box.plot_generate.update_template(fig)
    fig = viz2_box.plot_generate.update_legend(fig)
    fig = viz2_box.plot_generate.update_axes_labels(fig)
    fig = viz2_box.plot_generate.update_hover_template(fig)

    return fig


def create_layout(my_df):
    fig = create_figure(my_df)

    fig.update_layout(height=560)
    fig.update_layout(dragmode=False)

    return html.Div(id="box-viz", className='viz-block', children=[
        dcc.Graph(
            className='graph',
            figure=fig,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False,
                responsive=True,
            ),
            style={"width": "100%"},
        ),
    ])
