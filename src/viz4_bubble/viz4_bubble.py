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

SAT_SLIDER_MIN = 0
SAT_SLIDER_MAX = 1
SAT_SLIDER_STEP = 0.1

BUBBLE_GRAPH_ID = "bubble-graph"
BUBBLE_Y_SLIDER_ID = "bubble-slider-y"
BUBBLE_X_SLIDER_ID = "bubble-slider-x"

def create_figure(df, max_visibility=None, sat_range=None, question_idx=None):
    '''
        Calls the functions to preprocess the data and generate the plot for the bubble plot.
    '''
    processed_df = preprocess_data(df)
    if question_idx == 0:
        max_visibility = BUBBLE_SLIDER_MAX
        sat_range = [0, 1]

    elif question_idx == 1:
        max_visibility = 3_000_000
        sat_range = [0.7, 1]

    elif question_idx == 2:
        max_visibility = 2_000_000
        sat_range = [0, 1]
    fig = generate_plot(processed_df, max_visibility=max_visibility, sat_range=sat_range)
    return fig

def create_layout(df, max_visibility=BUBBLE_SLIDER_MAX, sat_range=None):
    '''
        Creates the layout for the bubble plot.
    '''
    fig = create_figure(df, max_visibility=max_visibility, sat_range=sat_range)
    slider_y_marks = {i: f"{i//1000000}M" for i in range(0, BUBBLE_SLIDER_MAX + 1, 1000000)}
    slider_x_marks = {i/10: str(i/10) for i in range(11)}

    return html.Div(
    className="bubble-wrapper",
    children=[
        html.Div(
            className="bubble-main-layout",
            children=[
                html.Div(
                    className="bubble-y-slider",
                    children=[
                        dcc.Slider(
                            id=BUBBLE_Y_SLIDER_ID,
                            min=BUBBLE_SLIDER_MIN,
                            max=BUBBLE_SLIDER_MAX,
                            step=BUBBLE_SLIDER_STEP,
                            value=max_visibility,
                            vertical=True,
                            verticalHeight=BUBBLE_SLIDER_HEIGHT,
                            marks=slider_y_marks,
                            tooltip={
                                "placement": "left",
                                "always_visible": False,
                            },
                        ),
                    ],
                ),
                dcc.Graph(
                    id=BUBBLE_GRAPH_ID,
                    figure=fig,
                    config={"displayModeBar": False},
                    className="graph",
                ),
            ],
        ),
        html.Div(
            className="bubble-x-slider",
            children=[
                dcc.RangeSlider(
                    id=BUBBLE_X_SLIDER_ID,
                    min=SAT_SLIDER_MIN,
                    max=SAT_SLIDER_MAX,
                    step=SAT_SLIDER_STEP,
                    value=[SAT_SLIDER_MIN, SAT_SLIDER_MAX],
                    marks=slider_x_marks,
                    tooltip={
                        "placement": "left",
                        "always_visible": False,
                    },
                ),
            ],
        ),
    ],
)