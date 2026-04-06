'''
    Contains source code for the fourth visualisation of the project. 
    It is a bubble plot, showing the relationship between satisfaction and visibility, 
    with the size of the bubbles representing the estimated number of owners.
'''
from dash import html, dcc

from viz4_bubble.preprocess import preprocess_data
from viz4_bubble.plot_generate import generate_plot

BUBBLE_SLIDER_MIN = 0
BUBBLE_SLIDER_MAX = 10000000
BUBBLE_SLIDER_STEP = 100000
BUBBLE_SLIDER_HEIGHT = 300

def create_figure(df, max_visibility=None):
    '''
        Calls the functions to preprocess the data and generate the plot for the bubble plot.
    '''
    processed_df = preprocess_data(df)
    fig = generate_plot(processed_df, max_visibility=max_visibility)
    return fig

def create_layout(df, max_visibility=BUBBLE_SLIDER_MAX, slider_id="bubble-slider", graph_id="bubble-graph"):
    '''
        Creates the layout for the bubble plot.
    '''
    fig = create_figure(df, max_visibility=max_visibility)
    slider_marks = {i: f"{i//1000000}M" for i in range(0, BUBBLE_SLIDER_MAX + 1, 1000000)}

    return html.Div(
        className="bubble-main-layout",
        children=[
            dcc.Graph(
                id=graph_id,
                figure=fig,
                config={"displayModeBar": False, "responsive": True},
                className="graph",
                style={"height": "100%"},
            ),
            html.Div(
                className="bubble-side-panel",
                children=[
                    html.Div("Filtrer par nombre d'avis", className="slider-title"),
                    dcc.Slider(
                        id=slider_id,
                        min=BUBBLE_SLIDER_MIN,
                        max=BUBBLE_SLIDER_MAX,
                        step=BUBBLE_SLIDER_STEP,
                        value=max_visibility,
                        vertical=True,
                        verticalHeight=BUBBLE_SLIDER_HEIGHT,
                        marks=slider_marks,
                        tooltip={
                            "placement": "left",
                            "always_visible": True,
                        },
                    ),
                ],
            ),
        ],
    )