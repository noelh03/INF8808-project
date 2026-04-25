'''
Contains source code for the first visualisation of the project.
It is a scatter plot showing the relationship between price and commercial success.

This module:
- prepares the dataset specifically for the scatter visualization
- generates the interactive figure based on user input (price filter)
- defines the Dash layout structure including graph and filtering controls

It acts as the interface between data preprocessing, visualization logic,
and user interaction within the scrollytelling flow.
'''

from dash import dcc, html

from viz1_scatter import preprocess
from viz1_scatter.plot_generate import generate_plot
from utils.constants import (
    SCATTER_SLIDER_MIN,
    SCATTER_SLIDER_MAX,
    SCATTER_SLIDER_STEP
)

_cached_processed_df = None


def get_processed_df(df):
    """
        Get the processed dataframe, using caching to avoid redundant processing.

        Args:
            df (pd.DataFrame): The input dataframe containing the game data.

        Returns:
            pd.DataFrame: The processed dataframe, ready for visualization.
    """
    global _cached_processed_df

    if _cached_processed_df is None:
        _cached_processed_df = preprocess.preprocess_data(df)

    return _cached_processed_df


def create_figure(df, price_range=(0, 100), question_idx=0):
    """
        Generate the scatter plot figure.

        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
            price_range (tuple): The price range filter values.
            question_idx (int): The index of the question displayed.

        Returns:
            fig: The generated scatter plot figure.
    """
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
    """
        Create the layout for the scatter plot.

        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
            price_range (tuple): The price range filter values.
            slider_id (str): The slider component ID.
            graph_id (str): The graph component ID.
            range_label_id (str): The label displaying the selected range.

        Returns:
            html.Div: The layout containing the graph and the price filter.
    """
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
                                className="slider-header",
                                children=[
                                    html.Span(
                                        "Filtrer par prix",
                                        className="slider-title"
                                    ),
                                    html.Span(
                                        f"{price_range[0]} $ – {price_range[1]} $",
                                        id=range_label_id,
                                        className="slider-range-value",
                                    ),
                                ],
                            ),

                            dcc.RangeSlider(
                                id=slider_id,
                                min=SCATTER_SLIDER_MIN,
                                max=SCATTER_SLIDER_MAX,
                                step=SCATTER_SLIDER_STEP,
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


# =========================
# HELPER UI
# =========================
def game_chip(name, img, url):
    return html.A(
        href=url,
        target="_blank",
        className="game-logo-chip",
        children=[
            html.Img(src=img, className="game-logo-img"),
            html.Span(name, className="game-logo-label"),
        ],
    )


def create_info_content():
    """
        Create the content for the information carousel.

        Returns:
            html.Div: The layout for the information carousel.
    """
    return html.Div(
        className="info-carousel",
        children=[
            dcc.Store(id="viz1-info-slide-idx", data=0),

            # =========================
            # SLIDE 1
            # =========================
            html.Div(
                id="viz1-info-slide-0",
                className="info-slide",
                children=[
                    html.Span("1 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-tag info-slide-icon"),
                            html.Span(
                                " Le prix de vente influence-t-il le succès commercial des jeux sur Steam ?"
                            ),
                        ],
                    ),
                    html.P(
                        "À partir de cette visualisation, on observe que la relation entre le prix et le succès commercial est très faible."
                        " Des jeux peu performants apparaissent à presque tous les niveaux de prix, tandis que certains jeux atteignent un succès élevé autant parmi les titres peu chers que parmi les titres plus coûteux."
                        " Le prix seul ne semble donc pas être un facteur déterminant du succès commercial."
                    ),
                    html.P(
                        "Dans les données observées entre 0 $ et 100 $, certains jeux payants très accessibles, comme Left 4 Dead 2 (1,99 $), Stardew Valley (8,99 $) ou Among Us (2,99 $), atteignent des niveaux de succès très élevés, ce qui montre qu’un faible prix n’empêche pas une large adoption."
                    ),

                    html.Div(
                        className="game-logo-strip",
                        children=[
                            game_chip("Left 4 Dead 2", "./assets/logos/left4dead2.png",
                                      "https://store.steampowered.com/app/550/Left_4_Dead_2/"),
                            game_chip("Stardew Valley", "./assets/logos/stardew.png",
                                      "https://store.steampowered.com/app/413150/Stardew_Valley/"),
                            game_chip("Among Us", "./assets/logos/amongus.png",
                                      "https://store.steampowered.com/app/945360/Among_Us/"),
                        ],
                    ),
                ],
            ),

            # =========================
            # SLIDE 2
            # =========================
            html.Div(
                id="viz1-info-slide-1",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("2 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-gamepad info-slide-icon"),
                            html.Span(
                                " Les jeux gratuits présentent-ils une dynamique de succès différente des jeux payants ?"
                            ),
                        ],
                    ),
                    html.P(
                        "Non. À partir de cette visualisation, on observe que les jeux gratuits sont regroupés à prix nul, et que certains d’entre eux atteignent des niveaux de succès commercial très élevés."
                        " Cependant, des jeux payants atteignent également des niveaux similaires, ce qui indique qu’il n’existe pas de différence systématique de succès entre jeux gratuits et payants. "
                        "Les données suggèrent donc que la gratuité peut favoriser un fort succès, sans pour autant garantir une performance supérieure aux jeux payants."
                    ),
                    html.P(
                        "Des jeux gratuits comme Dota 2, Counter-Strike 2 et PUBG: BATTLEGROUNDS figurent parmi "
                        "les titres les plus élevés du graphique, avec des niveaux de propriétaires estimés extrêmement importants."
                    ),

                    html.Div(
                        className="game-logo-strip",
                        children=[
                            game_chip("Dota 2", "./assets/logos/dota-2.png",
                                      "https://store.steampowered.com/app/570/Dota_2/"),
                            game_chip("CS2", "./assets/logos/csgo.png",
                                      "https://store.steampowered.com/app/730/CounterStrike_2/"),
                            game_chip("PUBG", "./assets/logos/pubg.png",
                                      "https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/"),
                        ],
                    ),
                ],
            ),

            # =========================
            # SLIDE 3
            # =========================
            html.Div(
                id="viz1-info-slide-2",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("3 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-chart-column info-slide-icon"),
                            html.Span(
                                " Le succès commercial est-il fortement concentré sur une minorité de jeux ?"
                            ),
                        ],
                    ),
                    html.P(
                        "Oui, de manière très marquée. "
                        "La grande majorité des jeux se concentre dans la partie basse du graphique, tandis qu’un nombre très limité de titres atteint des niveaux de succès exceptionnellement élevés. "
                        "La distribution du succès commercial apparaît donc fortement inégale."
                    ),
                    html.P(
                        "Les données montrent qu'environ 91 % des jeux se situent à 100 000 propriétaires estimés ou moins, "
                        "et près de 99 % restent sous 1 million. À l’inverse, seuls quelques titres dominent réellement le marché."
                        ", illustrant une forte concentration du succès sur une minorité de titres."
                    ),

                    html.Div(
                        className="game-logo-strip",
                        children=[
                            game_chip("Dota 2", "./assets/logos/dota-2.png",
                                      "https://store.steampowered.com/app/570/Dota_2/"),
                            game_chip("CS2", "./assets/logos/csgo.png",
                                      "https://store.steampowered.com/app/730/CounterStrike_2/"),
                            game_chip("Apex Legends", "./assets/logos/apex.png",
                                      "https://store.steampowered.com/app/1172470/Apex_Legends/"),
                        ],
                    ),
                ],
            ),

            # =========================
            # NAVIGATION
            # =========================
            html.Div(
                className="info-carousel-footer",
                children=[
                    html.Button("←", id="viz1-info-prev-btn", className="info-nav-btn", n_clicks=0),
                    html.Div(
                        className="info-progress",
                        children=[
                            html.Span(id="viz1-info-dot-0", className="info-dot active"),
                            html.Span(id="viz1-info-dot-1", className="info-dot"),
                            html.Span(id="viz1-info-dot-2", className="info-dot"),
                        ],
                    ),
                    html.Button("→", id="viz1-info-next-btn", className="info-nav-btn", n_clicks=0),
                ],
            ),
        ],
    )