

from dash import html


def create_hero():
    return html.Section(
        id="hero",
        className="hero-section",
        children=[
            html.Div(className="hero-bg-orb hero-orb-1"),
            html.Div(className="hero-bg-orb hero-orb-2"),
            html.Div(className="hero-grid"),
            html.Div(
                className="hero-overlay",
                children=[
                    html.P("INF8808 · LIVRABLE FINAL", className="hero-kicker"),
                    html.H1(
                        "Succès\ncommercial des\njeux Steam",
                        className="hero-title",
                    ),
                    html.H2(
                        "Prix, mode de jeu et tendances de marché",
                        className="hero-subtitle",
                    ),
                    html.P(
                        "Cette application de scrollytelling explore plusieurs facteurs susceptibles "
                        "d'être associés à la performance commerciale des jeux publiés sur Steam.",
                        className="hero-description",
                    ),
                    html.A(
                        "Commencer l'exploration",
                        href="#scatter",
                        className="hero-button",
                    ),
                ],
            ),
        ],
    )