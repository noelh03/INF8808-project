"""
Layout and figure controller for the beeswarm plot of commercial success by play mode.

This module:
- preprocesses the raw games DataFrame into owner samples and play mode categories
- generates the beeswarm figure with statistical markers
- defines the Dash layout wrapping the interactive graph
- provides the info panel content with key findings and game highlights
"""
from dash import html, dcc

import viz2_beeswarm.preprocess
import viz2_beeswarm.plot_generate


def ensure_preprocessed(my_df):
    """
    Return the preprocessed DataFrame, computing it once if not already done.

    Args:
        my_df: Raw games DataFrame.

    Returns:
        pd.DataFrame: DataFrame with 'Estimated owners (average)' and 'game_type' columns.
    """
    if "Estimated owners (average)" in my_df.columns and "game_type" in my_df.columns:
        return my_df.copy()

    processed = viz2_beeswarm.preprocess.sample_owners_and_classify(my_df.copy())
    processed = viz2_beeswarm.preprocess.filter_valid_games(processed)
    return processed


def create_figure(my_df):
    """
    Build and return the beeswarm figure from the games DataFrame.

    Args:
        my_df: Raw or preprocessed games DataFrame.

    Returns:
        go.Figure: Fully configured beeswarm figure.
    """
    my_df = ensure_preprocessed(my_df)

    fig = viz2_beeswarm.plot_generate.generate_plot(my_df)
    fig = viz2_beeswarm.plot_generate.update_template(fig)
    fig = viz2_beeswarm.plot_generate.update_legend(fig)
    fig = viz2_beeswarm.plot_generate.update_axes_labels(fig)
    fig = viz2_beeswarm.plot_generate.update_hover_template(fig)

    return fig


def create_layout(my_df):
    """
    Build the Dash layout containing the beeswarm plot.

    Args:
        my_df: Raw or preprocessed games DataFrame.

    Returns:
        html.Div: Dash component wrapping the beeswarm figure.
    """
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

def create_info_content():
    """
    Build the info panel content for the beeswarm visualization.

    Returns:
        html.Div: Dash component with the analysis text and game logo strip.
    """
    return html.Div(
        className="info-slide",
        children=[
            html.H4(
                className="info-block-title",
                children=[
                    html.I(className="fa-solid fa-circle-question info-slide-icon"),
                    html.Span(" Le mode de jeu est-il associé à des différences de performance commerciale ?"),
                ],
            ),
                html.P(
                "Oui, mais de façon asymétrique. La majorité des jeux échouent "
                "commercialement peu importe le mode (77 % des Solo, 63 % des Hybrides "
                "et 66 % des Multijoueurs n'atteignent qu'environ 10 000 propriétaires). "
                "Cependant, les jeux Multijoueurs et Hybrides ont une queue droite bien "
                "plus longue : 13 % d'entre eux atteignent 350 000 propriétaires ou plus, "
                "contre seulement 3,7 % des jeux Solo. La moyenne des Multijoueurs "
                "(578 000) est 10x supérieure à celle des Solo (54 000). "
                "Les mégahits absolus comme CS2, Dota 2, PUBG et Apex Legends (100 M+) "
                "sont presque exclusivement multijoueurs ou hybrides."
            ),
            html.Div(className="game-logo-strip", children=[
                html.A(href="https://store.steampowered.com/app/730/CounterStrike_2/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--up", children=[
                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                    html.Img(src="/assets/logos/csgo.png", className="game-logo-img"),
                    html.Span("CS2", className="game-logo-label"),
                ]),
                html.A(href="https://store.steampowered.com/app/570/Dota_2/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--up", children=[
                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                    html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                    html.Span("Dota 2", className="game-logo-label"),
                ]),
                html.A(href="https://store.steampowered.com/app/1623730/Palworld/", target="_blank", className="game-logo-chip", children=[
                    html.Img(src="/assets/logos/palworld.png", className="game-logo-img"),
                    html.Span("Palworld", className="game-logo-label"),
                ]),
                html.A(href="https://store.steampowered.com/app/2358720/Black_Myth_Wukong/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--down", children=[
                    html.I(className="fa-solid fa-arrow-trend-down game-logo-trend-icon"),
                    html.Img(src="/assets/logos/blackmyth.png", className="game-logo-img"),
                    html.Span("Black Myth", className="game-logo-label"),
                ]),
            ]),
        ],
    )
