'''
    Contains source code for the sixth visualisation of the project. 
    It is a violin plot showing the distribution of commercial success 
    (estimated owners) by publisher experience (number of games published),
    comparing Independent vs Major publishers.
'''
from dash import html, dcc

import viz6_violin.preprocess
import viz6_violin.plot_generate
from utils.constants import (VIOLIN_SLIDER_MIN, VIOLIN_SLIDER_MAX, VIOLIN_SLIDER_STEP, VIOLIN_SLIDER_HEIGHT)

def ensure_preprocessed(my_df):
    """
    Accept either:
    - raw dataframe with Publishers / Name / Estimated owners / Tags
    - already preprocessed dataframe with publisher / name / estimated_owners / nb_games_dev
    """
    if 'nb_games_dev' in my_df.columns and 'publisher' in my_df.columns:
        return my_df.copy()

    processed = viz6_violin.preprocess.step1(my_df.copy())
    processed = viz6_violin.preprocess.step2(processed)
    return processed


def create_figure(my_df):
    '''
        Calls the functions to preprocess the data and generate the plot for the sixth visualisation.
    '''
    my_df = ensure_preprocessed(my_df)
    my_df = viz6_violin.plot_generate.filter_by_max_games(my_df, VIOLIN_SLIDER_MAX)

    fig = viz6_violin.plot_generate.generate_plot(my_df)
    fig = viz6_violin.plot_generate.update_template(fig)
    fig = viz6_violin.plot_generate.update_legend(fig)
    fig = viz6_violin.plot_generate.update_axes_labels(fig)
    fig = viz6_violin.plot_generate.update_hover_template(fig)

    return fig


def create_layout(my_df, slider_id="violin-slider", graph_id="violin-graph"):
    preprocessed = ensure_preprocessed(my_df)
    real_max = int(preprocessed['nb_games_dev'].max())

    global VIOLIN_SLIDER_MAX
    VIOLIN_SLIDER_MAX = real_max

    fig = create_figure(preprocessed)
    fig.update_layout(dragmode=False)

    slider_marks = {VIOLIN_SLIDER_MIN: str(VIOLIN_SLIDER_MIN)}
    for i in range(50, VIOLIN_SLIDER_MAX, 50):
        slider_marks[i] = str(i)
    slider_marks[VIOLIN_SLIDER_MAX] = str(VIOLIN_SLIDER_MAX)

    return html.Div(className="viz-inner", children=[
        html.Div(className="dot-main-layout", children=[

            html.Div(
                className="dot-graph-column",
                children=[
                    dcc.Graph(
                        id=graph_id,
                        figure=fig,
                        config={"displayModeBar": False, "responsive": True},
                        className="graph",
                        style={"height": "100%"},
                    ),
                ],
            ),

            html.Div(className="dot-side-panel", children=[
                html.Div(
                    "Filtrer par nb de jeux publiés",
                    className="slider-title"
                ),
                dcc.Slider(
                    id=slider_id,
                    min=VIOLIN_SLIDER_MIN,
                    max=real_max,
                    step=VIOLIN_SLIDER_STEP,
                    value=real_max,
                    vertical=True,
                    verticalHeight=VIOLIN_SLIDER_HEIGHT,
                    marks=slider_marks,
                    tooltip={
                        "placement": "left",
                        "always_visible": True,
                    },
                ),
            ]),
        ]),
    ])
    
def create_info_content():
    return html.Div(
        className="info-carousel",
        children=[
            dcc.Store(id="viz6-info-slide-idx", data=0),

            html.Div(
                id="viz6-info-slide-0",
                className="info-slide",
                children=[
                    html.Span("1 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-compress info-slide-icon"),
                            html.Span(" Le succès commercial est-il concentré autour d'un nombre limité de développeurs ?"),
                        ],
                    ),
                    html.P("Oui, de façon très marquée."),
                    html.P(
                        "Dans chaque tranche de succès , des plus modestes (0 à 20 000) "
                        "aux plus élevées (10M à 20M) , les violons sont systématiquement "
                        "larges et denses près de 0, puis s'effacent rapidement. "
                        "Cela signifie que la grande majorité des jeux, peu importe leur "
                        "niveau de succès commercial, proviennent d'éditeurs ayant publié "
                        "très peu de jeux (1 à 5 en général)."
                    ),
                    html.P(
                        "Les éditeurs très prolifiques (>20 jeux publiés) sont présents "
                        "dans toutes les tranches sans exception, y compris les plus basses. "
                        "Le succès n'est donc pas réservé à une élite d'éditeurs expérimentés : "
                        "il est distribué largement parmi les petits studios."
                    ),                                            
                    html.P(
                        "Des jeux extrêmement populaires comme Counter-Strike 2, Dota 2 ou PUBG "
                        "illustrent bien ce phénomène : ils atteignent un succès massif sans que "
                        "cela soit nécessairement lié à une forte expérience en nombre de jeux publiés."
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
                id="viz6-info-slide-1",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("2 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-users info-slide-icon"),
                            html.Span(" Le succès est-il davantage dominé par les éditeurs majeurs ?"),
                        ],
                    ),
                    html.P("Non , c'est l'inverse."),
                    html.P(
                        "En se concentrant sur les éditeurs peu expérimentés (≤ 5 jeux publiés), "
                        "les violons bleu clair (indépendants) sont nettement plus larges que "
                        "les violons orange (majeurs) dans pratiquement toutes les tranches "
                        "de succès. Les indépendants sont donc bien plus nombreux à atteindre "
                        "chaque niveau, y compris les tranches supérieures (1M+ propriétaires)."
                    ),
                    html.P(
                        "Les éditeurs majeurs existent bien dans les tranches hautes, "
                        "mais en bien moins grand nombre. À expérience équivalente, "
                        "ce sont les indépendants qui produisent la majorité des succès commerciaux."
                    ),
                    html.P(
                        "Par exemple, des jeux indépendants comme Stardew Valley ou Terraria "
                        "atteignent un succès massif avec très peu de titres publiés, alors que "
                        "des productions majeures comme GTA V ou Call of Duty reposent sur des "
                        "studios très expérimentés mais ne dominent pas en nombre."
                    ),
                    html.Div(
                        className="game-logo-strip",
                        children=[
                            html.A(
                                href="https://store.steampowered.com/app/413150/Stardew_Valley/",
                                target="_blank",
                                className="game-logo-chip game-logo-chip--trend game-logo-chip--up",
                                children=[
                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                    html.Img(src="/assets/logos/stardew.png", className="game-logo-img"),
                                    html.Span("Stardew", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/105600/Terraria/",
                                target="_blank",
                                className="game-logo-chip game-logo-chip--trend game-logo-chip--up",
                                children=[
                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                    html.Img(src="/assets/logos/terraria.jpg", className="game-logo-img"),
                                    html.Span("Terraria", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/gtaV.png", className="game-logo-img"),
                                    html.Span("GTA V", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="viz6-info-slide-2",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("3 / 3", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(className="fa-solid fa-chart-line info-slide-icon"),
                            html.Span(" L'expérience d'un développeur constitue-t-elle un avantage structurel ?"),
                        ],
                    ),
                    html.P("Non, pas de façon claire."),
                    html.P(
                        "Si l'expérience était un avantage structurel, on s'attendrait à voir "
                        "les violons s'étirer davantage vers la droite (plus de jeux publiés) "
                        "dans les tranches de succès élevées. Ce n'est pas ce qu'on observe : "
                        "la forme des violons reste similaire d'une tranche à l'autre, "
                        "toujours très concentrée vers 0 à 5 jeux publiés."
                    ),
                    html.P(
                        "Les majeurs montrent une distribution légèrement plus étalée, "
                        "mais sans que cela corresponde à un meilleur succès commercial. "
                        "Publier davantage de jeux n'est pas un gage de succès : "
                        "l'expérience accumulée ne se traduit pas en avantage structurel mesurable."
                    ),
                    html.P(
                        "Des jeux comme Among Us ou Stardew Valley montrent qu’un succès massif "
                        "peut être atteint avec très peu d’expérience initiale, tandis que des "
                        "studios très prolifiques ne produisent pas systématiquement des succès "
                        "comparables."
                    ),
                    html.Div(
                        className="game-logo-strip",
                        children=[
                            html.A(
                                href="https://store.steampowered.com/app/945360/Among_Us/",
                                target="_blank",
                                className="game-logo-chip game-logo-chip--trend game-logo-chip--up",
                                children=[
                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                    html.Img(src="/assets/logos/amongus.png", className="game-logo-img"),
                                    html.Span("Among Us", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/413150/Stardew_Valley/",
                                target="_blank",
                                className="game-logo-chip game-logo-chip--trend game-logo-chip--up",
                                children=[
                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                    html.Img(src="/assets/logos/stardew.png", className="game-logo-img"),
                                    html.Span("Stardew", className="game-logo-label"),
                                ],
                            ),
                            html.A(
                                href="https://store.steampowered.com/app/730/CounterStrike_2/",
                                target="_blank",
                                className="game-logo-chip",
                                children=[
                                    html.Img(src="/assets/logos/csgo.png", className="game-logo-img"),
                                    html.Span("CS2", className="game-logo-label"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="info-carousel-footer",
                children=[
                    html.Button(
                        "←",
                        id="viz6-info-prev-btn",
                        className="info-nav-btn",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="info-progress",
                        children=[
                            html.Span(id="viz6-info-dot-0", className="info-dot active"),
                            html.Span(id="viz6-info-dot-1", className="info-dot"),
                            html.Span(id="viz6-info-dot-2", className="info-dot"),
                        ],
                    ),
                    html.Button(
                        "→",
                        id="viz6-info-next-btn",
                        className="info-nav-btn",
                        n_clicks=0,
                    ),
                ],
            ),
        ],
    )