# -*- coding: utf-8 -*-

"""
File name: app.py
Author: Olivia Gélinas (original author)
        Team 11 (adapted for the project)
Course: INF8808
Python Version: 3.8

This file contains the source code for the project.
"""
"""
Main application module for the Steam commercial success scrollytelling project.

This file:
- initializes the Dash application
- loads and prepares the dataset
- assembles all narrative sections and visualizations
- defines interactive callbacks

It serves as the entry point of the web application and orchestrates
the overall storytelling structure.
"""

from pathlib import Path

from dash import Dash, html, Input, Output
import pandas as pd

from viz1_scatter import viz1_scatter
from viz2_box import viz2_box
from viz3_line import viz3_line
from viz4_bubble import viz4_bubble
from viz5_dot import viz5_dot
from viz6_violin import viz6_violin
import sidebar


SCATTER_SLIDER_ID = "scatter-price-slider"
SCATTER_GRAPH_ID = "scatter-price-graph"


def make_section(section_id, kicker, title, description, viz_layout, prev_href, next_href):
    """
    Build a full story section with:
    - intro block (kicker, title, "?" info toggle, description)
    - section body: viz card on the left, side-nav arrows on the right
    """
    return html.Section(
        id=section_id,
        className="story-section",
        children=[
            html.Div(
                className="section-intro",
                children=[
                    html.Div(
                        className="section-title-row",
                        children=[
                            html.Div(children=[
                                html.P(kicker, className="section-kicker"),
                                html.H2(title, className="section-title"),
                            ]),
                            html.Details(
                                className="section-info-details",
                                children=[
                                    html.Summary("?", className="info-toggle-btn"),
                                    html.Div(
                                        "Les informations complémentaires seront ajoutées ici.",
                                        className="section-info-panel",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.P(description, className="section-description"),
                ],
            ),
            html.Div(
                className="section-body",
                children=[
                    html.Div(viz_layout, className="viz-card"),
                    html.Div(
                        className="section-side-nav",
                        children=[
                            html.A(
                                href=prev_href,
                                className="arrow-btn arrow-up",
                                title="Section précédente",
                                children=html.Span(className="arrow-chevron chevron-up"),
                            ),
                            html.A(
                                href=next_href,
                                className="arrow-btn arrow-down",
                                title="Section suivante",
                                children=html.Span(className="arrow-chevron chevron-down"),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "../src/assets/data/games.csv"

app = Dash(__name__)
server = app.server
app.title = "Project | INF8808"

data = pd.read_csv(DATA_PATH)

sidebar.register_sidebar_callbacks(app)

viz1_scatter_layout = viz1_scatter.create_layout(
    data,
    max_price=100,
    slider_id=SCATTER_SLIDER_ID,
    graph_id=SCATTER_GRAPH_ID,
)
viz2_box_layout = viz2_box.create_layout(data)
viz3_line_layout = viz3_line.create_layout(data)
viz4_bubble_layout = viz4_bubble.create_layout(data)
viz5_dot_layout = viz5_dot.create_layout(data)
viz6_violin_layout = viz6_violin.create_layout(data)

app.layout = html.Div(
    id="page-wrapper",
    children=[
        sidebar.create_sidebar(),
        html.Div(
            id="content",
            className="content",
            children=[
                html.Section(
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
                ),
                html.Main(
                    className="story-container",
                    children=[
                        make_section(
                            "scatter", "Section 1",
                            "Prix et succès commercial",
                            "Comparer la performance commerciale estimée des jeux gratuits et payants, "
                            "et observer comment la distribution évolue selon l'intervalle de prix sélectionné.",
                            viz1_scatter_layout, "#hero", "#box",
                        ),
                        make_section(
                            "box", "Section 2",
                            "Titre à finaliser",
                            "Description à finaliser.",
                            viz2_box_layout, "#scatter", "#line",
                        ),
                        make_section(
                            "line", "Section 3",
                            "Évolution des genres par succès commercial",
                            "Comparer l'évolution du nombre estimé de propriétaires par genre de 1997 à 2025, "
                            "et observer quels genres ont gagné ou perdu en importance au fil des années.",
                            viz3_line_layout, "#box", "#bubble",
                        ),
                        make_section(
                            "bubble", "Section 4",
                            "Titre à finaliser",
                            "Description à finaliser.",
                            viz4_bubble_layout, "#line", "#dot",
                        ),
                        make_section(
                            "dot", "Section 5",
                            "Titre à finaliser",
                            "Description à finaliser.",
                            viz5_dot_layout, "#bubble", "#violin",
                        ),
                        make_section(
                            "violin", "Section 6",
                            "Titre à finaliser",
                            "Description à finaliser.",
                            viz6_violin_layout, "#dot", "#hero",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output(SCATTER_GRAPH_ID, "figure"),
    Input(SCATTER_SLIDER_ID, "value"),
)
def update_scatter_price_range(max_price):
    return viz1_scatter.create_figure(data, max_price=max_price)


if __name__ == "__main__":
    app.run(debug=True)
