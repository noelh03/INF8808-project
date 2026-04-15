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
from viz1_scatter import preprocess
from viz1_scatter.plot_generate import generate_plot


SLIDER_MIN = 0
SLIDER_MAX = 1000
SLIDER_STEP = 10

_cached_processed_df = None


def get_processed_df(df):
    global _cached_processed_df
    if _cached_processed_df is None:
        _cached_processed_df = preprocess.preprocess_data(df)
    return _cached_processed_df


def create_figure(df, price_range=(0, 100), question_idx=0):
    processed_df = get_processed_df(df)
    return generate_plot(
        processed_df,
        price_range=price_range,
        question_idx=question_idx,
    )


def create_layout(
    df,
    price_range=(0, 100),
    slider_id="scatter-price-slider",
    graph_id="scatter-price-graph",
    range_label_id="scatter-price-range-label",
):
    fig = create_figure(df, price_range=price_range, question_idx=0)

    return html.Div(
        className="viz-inner",
        children=[
            html.Div(
                className="scatter-main-layout",
                children=[
                    dcc.Graph(
                        id=graph_id,
                        figure=fig,
                        config={"displayModeBar": False},
                        className="graph scatter-graph",
                    ),
                    html.Div(
                        className="scatter-bottom-filter",
                        children=[
                            html.Div(
                                [
                                    html.Span("Filtrer par prix", className="slider-title"),
                                    html.Span(
                                        f"{price_range[0]} $ – {price_range[1]} $",
                                        id=range_label_id,
                                        className="slider-range-value",
                                    ),
                                ],
                                className="slider-header",
                            ),
                            dcc.RangeSlider(
                                id=slider_id,
                                min=SLIDER_MIN,
                                max=SLIDER_MAX,
                                step=SLIDER_STEP,
                                value=list(price_range),
                                allowCross=False,
                                marks={},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                            ),
                        ],
                    ),
                ],
            )
        ],
    )