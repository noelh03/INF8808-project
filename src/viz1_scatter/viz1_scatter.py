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
    
def create_info_content():
    return html.Div(
        className="info-carousel",
        children=[
            dcc.Store(id="viz1-info-slide-idx", data=0),

            html.Div(
                id="viz1-info-slide-0",
                className="info-slide",
                children=[
                    html.Span("1 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-tag info-slide-icon"),
                            html.Span(" Le prix de vente influence-t-il le succès commercial des jeux sur Steam ?"),
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
                            html.A(
                                href="https://store.steampowered.com/app/550/Left_4_Dead_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/left4dead2.png", className="game-logo-img"),
                                    html.Span("Left 4 Dead 2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/413150/Stardew_Valley/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/stardew.png", className="game-logo-img"),
                                    html.Span("Stardew Valley", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/945360/Among_Us/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/amongus.png", className="game-logo-img"),
                                    html.Span("Among Us", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

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
                            html.Span(" Les jeux gratuits présentent-ils une dynamique de succès différente des jeux payants ?"),
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
                            html.A(
                                href="https://store.steampowered.com/app/570/Dota_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/dota-2.png", className="game-logo-img"),
                                    html.Span("Dota 2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/730/CounterStrike_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/csgo.png", className="game-logo-img"),
                                    html.Span("CS2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/pubg.png", className="game-logo-img"),
                                    html.Span("PUBG", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

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
                            html.Span(" Le succès commercial est-il fortement concentré sur une minorité de jeux ?"),
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
                            html.A(
                                href="https://store.steampowered.com/app/570/Dota_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/dota-2.png", className="game-logo-img"),
                                    html.Span("Dota 2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/730/CounterStrike_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/csgo.png", className="game-logo-img"),
                                    html.Span("CS2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/1172470/Apex_Legends/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="./assets/logos/apex.png", className="game-logo-img"),
                                    html.Span("Apex Legends", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

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