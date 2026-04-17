'''
    Contains source code for the fifth visualisation of the project. 
    It is a dot plot, showing the relationship between satisfaction and playtime, 
    with the color of the dots representing the number of reviews.
'''
from dash import html, dcc
import viz5_dot.preprocess as preprocess
import viz5_dot.plot_generate as plot_generate

DOT_SLIDER_MIN = 0
DOT_SLIDER_MAX = 6000
DOT_SLIDER_STEP = 100
DOT_SLIDER_HEIGHT = 340


def ensure_preprocessed(df):
    if (
        "Visibility" in df.columns
        and "Satisfaction" in df.columns
        and "Satisfaction rounded" in df.columns
        and "Playtime hours" in df.columns
    ):
        return df.copy()

    processed = preprocess.compute_metrics(df.copy())
    processed = preprocess.filter_data(processed)
    return processed


def create_figure(df, max_playtime=6000):
    df = ensure_preprocessed(df)
    fig = plot_generate.generate_plot(df, max_playtime)
    return fig


def create_layout(df, max_playtime=6000, slider_id="dot-slider", graph_id="dot-graph"):
    fig = create_figure(df, max_playtime)
    slider_marks = {i: f"{i//1000}k" for i in range(0, DOT_SLIDER_MAX + 1, 1000)}

    return html.Div(className="viz-inner", children=[
        html.Div(className="dot-main-layout", children=[
            html.Div(
                className="dot-graph-column",
                children=[
                    dcc.Graph(
                        id=graph_id,
                        figure=fig,
                        config={"displayModeBar": False, "responsive": True},
                        className="graph dot-graph",
                        style={
                            "height": "100%",
                            "width": "100%",
                            "minHeight": 0,
                            "minWidth": 0,
                        },
                    ),
                ],
            ),

            html.Div(className="dot-side-panel", children=[
                html.Div("Filtrer par temps de jeu moyen", className="slider-title"),
                dcc.Slider(
                    id=slider_id,
                    min=DOT_SLIDER_MIN,
                    max=DOT_SLIDER_MAX,
                    step=DOT_SLIDER_STEP,
                    value=max_playtime,
                    vertical=True,
                    verticalHeight=DOT_SLIDER_HEIGHT,
                    marks=slider_marks,
                    tooltip={
                        "placement": "left",
                        "always_visible": True,
                    },
                ),
            ])
        ])
    ])
    
def create_info_content():
    return html.Div(
        className="info-carousel",
        children=[
            dcc.Store(id="viz5-info-slide-idx", data=0),
            html.Div(
                id="viz5-info-slide-0",
                className="info-slide",
                children=[
                    html.Span("1 / 2", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(
                                className="fa-solid fa-clock info-slide-icon",
                            ),
                            html.Span(
                                " Le temps de jeu moyen est-il lié à la satisfaction ?",
                            ),
                        ],
                    ),
                    html.P(
                        "Chaque point est un jeu : la satisfaction (avis positifs / total, "
                        "arrondie à une décimale) est lue au survol ; le graphique utilise un "
                        "placement type beeswarm : bandes fines selon le temps de jeu, avec "
                        "répartition horizontale des points (et colonnes supplémentaires si la "
                        "bande est très dense), pour mieux voir où s’accumulent les jeux. "
                        "En ordonnée : temps de jeu moyen à vie (données Steam), en heures. "
                        "Une grappe vers le bas indique beaucoup de titres peu joués en moyenne "
                        "malgré une note correcte ; les points plus hauts correspondent souvent "
                        "à des jeux très suivis."
                    ),
                ],
            ),
            html.Div(
                id="viz5-info-slide-1",
                className="info-slide",
                style={"display": "none"},
                children=[
                    html.Span("2 / 2", className="info-slide-counter"),
                    html.H4(
                        className="info-block-title",
                        children=[
                            html.I(
                                className="fa-solid fa-palette info-slide-icon",
                            ),
                            html.Span(
                                " Couleur du point et curseur vertical",
                            ),
                        ],
                    ),
                    html.P(
                        "La couleur représente le volume total d’avis (positifs + négatifs) : "
                        "plus la teinte est foncée, plus le jeu a été évalué souvent. Les points "
                        "très clairs ont peu d’avis : le ratio de satisfaction y est plus sensible "
                        "à quelques votes. Le curseur à droite fixe le temps de jeu moyen "
                        "maximum affiché sur l’axe vertical : en le baissant, tu te concentres "
                        "sur les jeux moins chronophages en moyenne et tu vois comment le nuage "
                        "se réorganise."
                    ),
                ],
            ),
            html.Div(
                className="info-carousel-footer",
                children=[
                    html.Button("←", id="viz5-info-prev-btn", className="info-nav-btn", n_clicks=0),
                    html.Div(
                        className="info-progress",
                        children=[
                            html.Span(id="viz5-info-dot-0", className="info-dot active"),
                            html.Span(id="viz5-info-dot-1", className="info-dot"),
                        ],
                    ),
                    html.Button("→", id="viz5-info-next-btn", className="info-nav-btn", n_clicks=0),
                ],
            ),
        ],
    )