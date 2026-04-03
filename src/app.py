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

LINE_CHECKLIST_ID = viz3_line.LINE_CHECKLIST_ID
LINE_GRAPH_ID = viz3_line.LINE_GRAPH_ID

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
    graph_id=SCATTER_GRAPH_ID
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
                                html.H1("Succès\ncommercial des\njeux Steam", className="hero-title"),
                                html.H2("Prix, mode de jeu et tendances de marché", className="hero-subtitle"),
                                html.P(
                                    "Cette application de scrollytelling explore plusieurs facteurs susceptibles "
                                    "d’être associés à la performance commerciale des jeux publiés sur Steam.",
                                    className="hero-description"
                                ),
                                html.A("Commencer l’exploration", href="#scatter", className="hero-button")
                            ]
                        )
                    ]
                ),
                html.Main(
                    className="story-container",
                    children=[
                        html.Section(
                            id="scatter",
                            className="story-section",
                            children=[
                                html.Div(
                                    className="section-intro",
                                    children=[
                                        html.P("Section 1", className="section-kicker"),
                                        html.H2("Prix et succès commercial", className="section-title"),
                                        html.P(
                                            "Comparer la performance commerciale estimée des jeux gratuits et payants, "
                                            "et observer comment la distribution évolue selon l’intervalle de prix sélectionné.",
                                            className="section-description"
                                        )
                                    ]
                                ),
                                html.Div(viz1_scatter_layout, className="viz-card")
                            ]
                        ),
                        html.Section(
                            id="box",
                            className="story-section",
                            children=[
                                html.Div(
                                    className="section-intro",
                                    children=[
                                        html.P("Section 2", className="section-kicker"),
                                        html.H2("Titre à finaliser", className="section-title"),
                                        html.P(
                                            "Description à finaliser.",
                                            className="section-description"
                                        )
                                    ]
                                ),
                                html.Div(viz2_box_layout, className="viz-card")
                            ]
                        ),
                        html.Section(
                            id="line",
                            className="story-section",
                            children=[
                                html.Div(
                                    className="section-intro",
                                    children=[
                                        html.P("Section 3", className="section-kicker"),
                                        html.H2("Évolution des genres par succès commercial", className="section-title"),
                                        html.P(
                                            "Comparer l'évolution du nombre estimé de propriétaires par genre "
                                            "de 1997 à 2025, et observer quels genres ont gagné ou perdu en "
                                            "importance au fil des années.",
                                            className="section-description"
                                        )
                                    ]
                                ),
                                html.Div(viz3_line_layout, className="viz-card")
                            ]
                        ),
                        html.Section(
                            id="bubble",
                            className="story-section",
                            children=[
                                html.Div(
                                    className="section-intro",
                                    children=[
                                        html.P("Section 4", className="section-kicker"),
                                        html.H2("Titre à finaliser", className="section-title"),
                                        html.P(
                                            "Description à finaliser.",
                                            className="section-description"
                                        )
                                    ]
                                ),
                                html.Div(viz4_bubble_layout, className="viz-card")
                            ]
                        ),
                        html.Section(
                            id="dot",
                            className="story-section",
                            children=[
                                html.Div(
                                    className="section-intro",
                                    children=[
                                        html.P("Section 5", className="section-kicker"),
                                        html.H2("Titre à finaliser", className="section-title"),
                                        html.P(
                                            "Description à finaliser.",
                                            className="section-description"
                                        )
                                    ]
                                ),
                                html.Div(viz5_dot_layout, className="viz-card")
                            ]
                        ),
                        html.Section(
                            id="violin",
                            className="story-section",
                            children=[
                                html.Div(
                                    className="section-intro",
                                    children=[
                                        html.P("Section 6", className="section-kicker"),
                                        html.H2("Titre à finaliser", className="section-title"),
                                        html.P(
                                            "Description à finaliser.",
                                            className="section-description"
                                        )
                                    ]
                                ),
                                html.Div(viz6_violin_layout, className="viz-card")
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output(SCATTER_GRAPH_ID, "figure"),
    Input(SCATTER_SLIDER_ID, "value")
)
def update_scatter_price_range(max_price):
    return viz1_scatter.create_figure(data, max_price=max_price)


@app.callback(
    Output(LINE_GRAPH_ID, "figure"),
    Input(LINE_CHECKLIST_ID, "value")
)
def update_line_genres(selected_genres):
    return viz3_line.create_figure(data, selected_genres=selected_genres or [])


if __name__ == "__main__":
    app.run(debug=True)