'''
    Contains source code for the fourth visualisation of the project. 
    It is a bubble plot, showing the relationship between satisfaction and visibility, 
    with the size of the bubbles representing the estimated number of owners.
'''
from dash import html, dcc

from viz4_bubble import preprocess
from viz4_bubble.plot_generate import generate_plot
from utils.constants import (BUBBLE_GRAPH_ID, BUBBLE_Y_SLIDER_ID, BUBBLE_X_SLIDER_ID, 
                            BUBBLE_SLIDER_MIN, BUBBLE_SLIDER_MAX, BUBBLE_SLIDER_STEP, 
                            SAT_SLIDER_MIN, SAT_SLIDER_MAX, SAT_SLIDER_STEP, BUBBLE_SLIDER_HEIGHT)

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
    
def create_info_content():
    return html.Div(
        className="info-carousel",
        children=[
            dcc.Store(id="viz4-info-slide-idx", data=0),

            html.Div(
                id="viz4-info-slide-0",
                className="info-slide",
                children=[
                    html.Span("1 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-comments info-slide-icon"),
                            html.Span(" Le volume d’avis est-il corrélé au succès commercial ?"),
                        ],
                    ),
                    html.P(
                        "Oui, très fortement. Les jeux ayant un très grand nombre d’avis "
                        "se situent presque systématiquement parmi les plus grands succès commerciaux. "
                        "Sur le graphique, les plus grosses bulles sont clairement concentrées "
                        "dans la partie haute, ce qui indique que la visibilité joue un rôle central."
                    ),
                    html.P(
                        "Des jeux comme Counter-Strike 2, Dota 2 ou PUBG illustrent parfaitement "
                        "cette tendance : ils cumulent des millions d’avis et dominent largement "
                        "en termes de succès commercial. La visibilité apparaît donc comme un "
                        "facteur clé pour atteindre un large public."
                    ),
                    html.Div(
                        className="game-logo-strip",
                        children=[
                            html.A(
                                href="https://store.steampowered.com/app/730/CounterStrike_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/csgo.png", className="game-logo-img"),
                                    html.Span("CS2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/570/Dota_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                                    html.Span("Dota 2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/pubg.png", className="game-logo-img"),
                                    html.Span("PUBG", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                id="viz4-info-slide-1",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("2 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-thumbs-up info-slide-icon"),
                            html.Span(" Le ratio d’évaluations positives est-il associé au succès commercial ?"),
                        ],
                    ),
                    html.P(
                        "La satisfaction des joueurs semble jouer un rôle, mais son impact est moins direct "
                        "que celui de la visibilité. Sur le graphique, des jeux avec une très forte satisfaction "
                        "(proches de 1) n’atteignent pas nécessairement un succès commercial élevé."
                    ),
                    html.P(
                        "Par exemple, des jeux très appréciés comme Stardew Valley, Terraria ou Hades "
                        "présentent un excellent ratio d’évaluations positives, mais leur succès reste "
                        "moins extrême que celui des jeux les plus visibles. La satisfaction semble donc "
                        "nécessaire pour fidéliser les joueurs, mais insuffisante à elle seule pour garantir "
                        "un succès massif."
                    ),
                    html.Div(
                        className="game-logo-strip",
                        children=[
                            html.A(
                                href="https://store.steampowered.com/app/413150/Stardew_Valley/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/stardew.png", className="game-logo-img"),
                                    html.Span("Stardew Valley", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/105600/Terraria/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/terraria.jpg", className="game-logo-img"),
                                    html.Span("Terraria", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/1145360/Hades/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/hades.jpg", className="game-logo-img"),
                                    html.Span("Hades", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                id="viz4-info-slide-2",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("3 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-scale-balanced info-slide-icon"),
                            html.Span(" Entre visibilité et satisfaction, quel facteur est le plus déterminant ?"),
                        ],
                    ),
                    html.P(
                        "La visibilité apparaît comme le facteur le plus déterminant du succès commercial. "
                        "Les jeux les plus performants sont avant tout ceux qui accumulent un grand nombre d’avis, "
                        "même si leur niveau de satisfaction n’est pas parfait."
                    ),
                    html.P(
                        "À l’inverse, certains jeux très bien notés mais peu visibles restent limités en succès. "
                        "Un exemple typique est celui de petits jeux de niche comme Supipara, qui présentent "
                        "une bonne satisfaction mais très peu d’avis. Cela montre que sans visibilité, "
                        "même un jeu apprécié peut rester confidentiel."
                    ),
                    html.Div(
                        className="game-logo-strip",
                        children=[
                            html.A(
                                href="https://store.steampowered.com/app/730/CounterStrike_2/",
                                target="_blank",
                                className="game-logo-chip game-logo-chip--trend game-logo-chip--up",
                                children=[
                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                    html.Img(src="/assets/logos/csgo.png", className="game-logo-img"),
                                    html.Span("CS2", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/413150/Stardew_Valley/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/stardew.png", className="game-logo-img"),
                                    html.Span("Stardew Valley", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/496350/Supipara_Chapter_1/",
                                target="_blank",
                                className="game-logo-chip game-logo-chip--trend game-logo-chip--down",
                                children=[
                                    html.I(className="fa-solid fa-arrow-trend-down game-logo-trend-icon"),
                                    html.Img(src="/assets/logos/supipara.png", className="game-logo-img"),
                                    html.Span("Supipara", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                className="info-carousel-footer",
                children=[
                            html.Button("←", id="viz4-info-prev-btn", className="info-nav-btn", n_clicks=0),
                    html.Div(
                        className="info-progress",
                        children=[
                            html.Span(id="viz4-info-dot-0", className="info-dot active"),
                            html.Span(id="viz4-info-dot-1", className="info-dot"),
                            html.Span(id="viz4-info-dot-2", className="info-dot"),
                        ],
                    ),
                            html.Button("→", id="viz4-info-next-btn", className="info-nav-btn", n_clicks=0),
                ],
            ),
        ],
    )