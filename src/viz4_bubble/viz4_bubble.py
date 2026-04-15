'''
    Contains source code for the fourth visualisation of the project. 
    It is a bubble plot, showing the relationship between satisfaction and visibility, 
    with the size of the bubbles representing the estimated number of owners.
'''
from dash import html, dcc

from viz4_bubble import preprocess
from viz4_bubble.plot_generate import generate_plot

BUBBLE_SLIDER_MIN = 0
BUBBLE_SLIDER_MAX = 10000000
BUBBLE_SLIDER_STEP = 100000
BUBBLE_SLIDER_HEIGHT = 350

SAT_SLIDER_MIN = 0
SAT_SLIDER_MAX = 1
SAT_SLIDER_STEP = 0.1

BUBBLE_GRAPH_ID = "bubble-graph"
BUBBLE_Y_SLIDER_ID = "bubble-slider-y"
BUBBLE_X_SLIDER_ID = "bubble-slider-x"

_cached_processed_df = None


def get_processed_df(df):
    global _cached_processed_df
    if _cached_processed_df is None:
        if "Visibility" in df.columns and "Satisfaction" in df.columns and "Estimated owners (average)" in df.columns:
            _cached_processed_df = df.copy()
        else:
            _cached_processed_df = preprocess.preprocess_data(df)
    return _cached_processed_df


def get_default_filters(question_idx):
    if question_idx == 1:
        return 3_000_000, [0.7, 1]
    if question_idx == 2:
        return 2_000_000, [0, 1]
    return BUBBLE_SLIDER_MAX, [0, 1]


def create_figure(df, max_visibility=None, sat_range=None, question_idx=None):
    '''
        Calls the functions to preprocess the data and generate the plot for the bubble plot.
    '''
    processed_df = get_processed_df(df)

    if max_visibility is None or sat_range is None:
        default_visibility, default_sat_range = get_default_filters(question_idx)
        if max_visibility is None:
            max_visibility = default_visibility
        if sat_range is None:
            sat_range = default_sat_range

    fig = generate_plot(
        processed_df,
        max_visibility=max_visibility,
        sat_range=sat_range
    )
    return fig


def create_layout(df, max_visibility=BUBBLE_SLIDER_MAX, sat_range=None):
    '''
        Creates the layout for the bubble plot.
    '''
    if sat_range is None:
        sat_range = [SAT_SLIDER_MIN, SAT_SLIDER_MAX]

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
                                    "placement": "bottom",
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
                        value=sat_range,
                        marks=slider_x_marks,
                        tooltip={
                            "placement": "bottom",
                            "always_visible": False,
                        },
                    ),
                ],
            ),
        ],
    )