"""
Layout and figure controller for the price vs commercial success visualization.

This module:
- prepares the dataset specifically for the scatter visualization
- generates the interactive figure based on user input (price filter)
- defines the Dash layout structure including graph and filtering controls

It acts as the interface between data preprocessing, visualization logic,
and user interaction within the scrollytelling flow.
"""

from dash import dcc, html
from viz1_scatter.preprocess import preprocess_data
from viz1_scatter.plot_generate import generate_plot


SLIDER_MIN = 0
SLIDER_MAX = 1000
SLIDER_STEP = 10
SLIDER_HEIGHT = 300


def create_figure(df, max_price=100):
    processed_df = preprocess_data(df)
    return generate_plot(processed_df, max_price=max_price)


def create_layout(df, max_price=100, slider_id="scatter-price-slider", graph_id="scatter-price-graph"):
    fig = create_figure(df, max_price=max_price)
    slider_marks = {i: str(i) for i in range(0, SLIDER_MAX + 1, 100)}

    return html.Div(
        className="viz-inner",
        children=[
            html.Div(
                className="scatter-main-layout",
                children=[
                    dcc.Graph(
                        id=graph_id,
                        figure=fig,
                        config={"displayModeBar": False, "responsive": True},
                        className="graph",
                        style={"height": "100%"},
                    ),
                    html.Div(
                        className="scatter-side-panel",
                        children=[
                            html.Div("Filtrer par prix", className="slider-title"),
                            dcc.Slider(
                                id=slider_id,
                                min=SLIDER_MIN,
                                max=SLIDER_MAX,
                                step=SLIDER_STEP,
                                value=max_price,
                                vertical=True,
                                verticalHeight=SLIDER_HEIGHT,
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
        ],
    )