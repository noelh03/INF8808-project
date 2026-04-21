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

import os
from dash import Dash, html, Input, Output, State, ctx, callback_context
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from viz1_scatter import viz1_scatter
from viz2_box import viz2_box
from viz3_line import viz3_line
from viz4_bubble import viz4_bubble
from viz5_dot import viz5_dot
from viz6_violin import viz6_violin
import main_components.sidebar as sidebar
import main_components.hero as hero
import utils.utils_app as utils_app
from utils.constants import (
    SCATTER_SLIDER_ID, SCATTER_GRAPH_ID, LINE_CHECKLIST_ID, LINE_GRAPH_ID, 
    LINE_ALL_ID, BUBBLE_GRAPH_ID, BUBBLE_Y_SLIDER_ID, BUBBLE_X_SLIDER_ID, 
    DOT_GRAPH_ID, DOT_SLIDER_ID, VIOLIN_GRAPH_ID, VIOLIN_SLIDER_ID)


# ---------------------------------------------------------------------------
# App initialization 
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
RAW_DATA_PATH = os.path.join(BASE_DIR, "assets", "data", "games.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "assets", "data", "processed")
VIZ1_DATA_PATH = os.path.join(PROCESSED_DIR, "viz1_scatter.csv")
VIZ4_DATA_PATH = os.path.join(PROCESSED_DIR, "viz4_bubble.csv")
VIZ6_DATA_PATH = os.path.join(PROCESSED_DIR, "viz6_violin.csv")

app = Dash(
    __name__,
    assets_folder=os.path.join(BASE_DIR, "assets"),
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
)
server = app.server
app.title = "Project | INF8808"

# ---------------------------------------------------------------------------
# Data loading 
# ---------------------------------------------------------------------------
data = pd.read_csv(RAW_DATA_PATH)
SCATTER_DATA = utils_app.load_csv_with_fallback(VIZ1_DATA_PATH, RAW_DATA_PATH)
BUBBLE_DATA = utils_app.load_csv_with_fallback(VIZ4_DATA_PATH, RAW_DATA_PATH)
VIOLIN_DATA = utils_app.load_csv_with_fallback(VIZ6_DATA_PATH, RAW_DATA_PATH)

if "nb_games_dev" in VIOLIN_DATA.columns:
    VIOLIN_REAL_MAX = int(VIOLIN_DATA["nb_games_dev"].max())
elif {"Publishers", "Name"}.issubset(data.columns):
    _tmp = data.copy()
    _tmp["nb_games_dev"] = _tmp.groupby("Publishers")["Name"].transform("count")
    VIOLIN_REAL_MAX = int(_tmp["nb_games_dev"].max())
else:
    VIOLIN_REAL_MAX = 50
VIOLIN_SLIDE_SLIDER_VALUES = [VIOLIN_REAL_MAX, 5, VIOLIN_REAL_MAX]

# ---------------------------------------------------------------------------
# Sections prep
# ---------------------------------------------------------------------------
sidebar.register_sidebar_callbacks(app)

viz1_scatter_layout = viz1_scatter.create_layout(
    SCATTER_DATA,
    price_range=(0, 100),
    slider_id=SCATTER_SLIDER_ID,
    graph_id=SCATTER_GRAPH_ID,
)
viz2_box_layout = viz2_box.create_layout(data)
viz3_line_layout = viz3_line.create_layout(data)
viz4_bubble_layout = viz4_bubble.create_layout(BUBBLE_DATA)
viz5_dot_layout = viz5_dot.create_layout(
    data,
    slider_id=DOT_SLIDER_ID,
    graph_id=DOT_GRAPH_ID,
)
viz6_violin_layout = viz6_violin.create_layout(
    VIOLIN_DATA,
    slider_id=VIOLIN_SLIDER_ID,
    graph_id=VIOLIN_GRAPH_ID,
)

# ---------------------------------------------------------------------------
# App layout assembly 
# ---------------------------------------------------------------------------
app.layout = html.Div(
    id="page-wrapper",
    children=[
        sidebar.create_sidebar(),
        html.Div(
            id="content",
            className="content",
            children=[
                hero.create_hero(),
                html.Main(
                    className="story-container",
                    children=[
                        utils_app.make_section(
                            "scatter",
                            "Prix et succès commercial",
                            "Comparer la performance commerciale estimée des jeux gratuits et payants, "
                            "et observer comment la distribution évolue selon l'intervalle de prix sélectionné.",
                            viz1_scatter_layout, "#hero", "#box",
                            info_content=viz1_scatter.create_info_content(),
                        ),
                        utils_app.make_section(
                            "box",
                            "Mode de jeu et succès commercial",
                            "Explorer si les jeux solo, hybrides ou exclusivement multijoueur "
                            "se distinguent par leur performance commerciale estimée, "
                            "et observer comment chaque catégorie se répartit sur l'échelle des propriétaires.",
                            viz2_box_layout, "#scatter", "#line",
                            info_content=viz2_box.create_info_content(),
                        ),
                        utils_app.make_section(
                            "line",
                            "Le succès commercial des différents genres selon leur année de sortie",
                            "Comparer l'évolution du nombre estimé de propriétaires par genre de 1997 à 2025, "
                            "et observer quels genres ont gagné ou perdu en importance au fil des années.",
                            viz3_line_layout, "#box", "#bubble",
                            info_content=viz3_line.create_info_content(),
                        ),
                        utils_app.make_section(
                            "bubble",
                            "Visibilité et succès commercial",
                            "Comparer la performance commerciale estimée des jeux selon leur nombre d’avis, et observer comment la distribution évolue selon l’intervalle de visibilité sélectionné.",
                            viz4_bubble_layout, "#line", "#dot",
                            info_content=viz4_bubble.create_info_content(),
                        ),
                        utils_app.make_section(
                            "dot",
                            "Satisfaction, temps de jeu et succès commercial",
                            "Comparer la satisfaction et le temps de jeu moyen des jeux selon leur nombre d’avis, et observer comment la distribution évolue selon l’intervalle de temps de jeu sélectionné.",
                            viz5_dot_layout, "#bubble", "#violin",
                            info_content=viz5_dot.create_info_content(),
                        ),
                        utils_app.make_section(
                            "violin",
                            "Le succès commercial selon l'expérience et le type d'éditeur",
                            "Comparer la distribution du succès commercial selon l'expérience des éditeurs, et observer si les indépendants et les majeurs se distinguent dans leur capacité à générer du succès.",
                            viz6_violin_layout,
                            "#dot",
                            "#hero",
                            info_content=viz6_violin.create_info_content(),
                        ),
                    ],
                ),
            ],
        ),
    ],
)



""" 
Callbacks for interactive components (filters, info carousels, etc.) 
"""

# ---------------------------------------------------------------------------
# Viz 1, filters and info carousel — navigate between the 3 insight slides
# ---------------------------------------------------------------------------
@app.callback(
    Output("viz1-info-slide-idx", "data"),
    Output("viz1-info-slide-0", "style"),
    Output("viz1-info-slide-1", "style"),
    Output("viz1-info-slide-2", "style"),
    Output("viz1-info-dot-0", "className"),
    Output("viz1-info-dot-1", "className"),
    Output("viz1-info-dot-2", "className"),
    Input("viz1-info-prev-btn", "n_clicks"),
    Input("viz1-info-next-btn", "n_clicks"),
    State("viz1-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def update_viz1_carousel(prev_clicks, next_clicks, current_idx):
    idx = current_idx or 0

    cb_ctx = callback_context
    if not cb_ctx.triggered:
        raise PreventUpdate

    button_id = cb_ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "viz1-info-next-btn":
        idx = (idx + 1) % 3
    elif button_id == "viz1-info-prev-btn":
        idx = (idx - 1) % 3

    styles = [{"display": "flex" if i == idx else "none"} for i in range(3)]
    dots = ["info-dot active" if i == idx else "info-dot" for i in range(3)]

    return idx, styles[0], styles[1], styles[2], dots[0], dots[1], dots[2]

@app.callback(
    Output(SCATTER_GRAPH_ID, "figure"),
    Input(SCATTER_SLIDER_ID, "value"),
    Input("viz1-info-slide-idx", "data"),
)
def update_scatter_price_range(price_range, question_idx):
    if not price_range or len(price_range) != 2:
        price_range = [0, 100]

    return viz1_scatter.create_figure(
        SCATTER_DATA,
        price_range=tuple(price_range),
        question_idx=question_idx or 0,
    )

# ---------------------------------------------------------------------------
# Viz 3, filters and info carousel — navigate between the 3 insight slides
# ---------------------------------------------------------------------------
@app.callback(
    Output("viz3-info-slide-idx", "data"),
    Output("viz3-info-slide-0", "style"),
    Output("viz3-info-slide-1", "style"),
    Output("viz3-info-slide-2", "style"),
    Output("viz3-info-dot-0", "className"),
    Output("viz3-info-dot-1", "className"),
    Output("viz3-info-dot-2", "className"),
    Input("viz3-info-prev-btn", "n_clicks"),
    Input("viz3-info-next-btn", "n_clicks"),
    State("viz3-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def advance_info_carousel(prev_clicks, next_clicks, current_idx):
    triggered = ctx.triggered_id
    current = current_idx or 0
    
    if triggered == "viz3-info-prev-btn":
        next_idx = (current - 1) % 3
    else:  # viz3-info-next-btn
        next_idx = (current + 1) % 3
    styles = [{"display": "flex" if i == next_idx else "none"} for i in range(3)]
    dots = ["info-dot active" if i == next_idx else "info-dot" for i in range(3)]
    return next_idx, styles[0], styles[1], styles[2], dots[0], dots[1], dots[2]

@app.callback(
    Output(LINE_GRAPH_ID, "figure"),
    Input(LINE_CHECKLIST_ID, "value"),
)
def update_line_genres(selected_genres):
    return viz3_line.create_figure(data, selected_genres=selected_genres or [])

@app.callback(
    Output(LINE_CHECKLIST_ID, "value"),
    Output(LINE_ALL_ID, "value"),
    Input(LINE_CHECKLIST_ID, "value"),
    Input(LINE_ALL_ID, "value"),
    Input(LINE_GRAPH_ID, "restyleData"),
    Input("viz3-info-slide-idx", "data"),
    State(LINE_GRAPH_ID, "figure"),
    State(LINE_CHECKLIST_ID, "value"),
    prevent_initial_call=True,
)
def sync_line_genre_filters(checklist_value, all_value, restyle_data, info_idx, figure, current_checklist):
    """
    Checklist + « Tous les genres » in one callback to avoid a Dash circular dependency
    (two callbacks that each output the other's input create a cycle at layout validation).
    """
    triggered = ctx.triggered_id
    all_genres_set = set(viz3_line.CHECKLIST_GENRES)
    full_list = list(viz3_line.CHECKLIST_GENRES)

    if triggered == LINE_ALL_ID:
        if "All" in (all_value or []):
            return full_list, ["All"]
        if set(current_checklist or []) >= all_genres_set:
            return [], []
        raise PreventUpdate

    if triggered == LINE_GRAPH_ID:
        if not restyle_data or not figure:
            raise PreventUpdate
        merged = utils_app._apply_restyle_patch_to_figure(figure, restyle_data)
        new_vals = utils_app._figure_to_viz3_checklist_values(merged)
        if new_vals == list(current_checklist or []):
            raise PreventUpdate
        all_out = ["All"] if set(new_vals or []) >= all_genres_set else []
        return new_vals, all_out

    if triggered == "viz3-info-slide-idx":
        # Keep line chart state coherent with the active narrative question.
        presets = {
            0: [g for g in viz3_line.CHECKLIST_GENRES if g != "Others"],  # Q1: core genres only
            1: list(viz3_line.CHECKLIST_GENRES),  # Q2: full context
            2: ["Massively Multiplayer", "Free To Play", "RPG"],  # Q3: focus genres
        }
        new_vals = presets.get(info_idx or 0, [g for g in viz3_line.CHECKLIST_GENRES if g != "Others"])
        all_out = ["All"] if set(new_vals) >= all_genres_set else []
        return new_vals, all_out

    if triggered == LINE_CHECKLIST_ID:
        cl = list(checklist_value or [])
        if set(cl) >= all_genres_set:
            return cl, ["All"]
        return cl, []

    raise PreventUpdate

# ---------------------------------------------------------------------------
# Viz 4, filters and info carousel — navigate between the 3 insight slides
# ---------------------------------------------------------------------------
@app.callback(
    Output("viz4-info-slide-idx", "data"),
    Output("viz4-info-slide-0", "style"),
    Output("viz4-info-slide-1", "style"),
    Output("viz4-info-slide-2", "style"),
    Output("viz4-info-dot-0", "className"),
    Output("viz4-info-dot-1", "className"),
    Output("viz4-info-dot-2", "className"),
    Input("viz4-info-prev-btn", "n_clicks"),
    Input("viz4-info-next-btn", "n_clicks"),
    State("viz4-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def update_viz4_carousel(prev_clicks, next_clicks, current_idx):
    idx = current_idx or 0

    cb_ctx = callback_context
    if not cb_ctx.triggered:
        raise PreventUpdate

    button_id = cb_ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "viz4-info-next-btn":
        idx = (idx + 1) % 3
    elif button_id == "viz4-info-prev-btn":
        idx = (idx - 1) % 3

    styles = [{"display": "flex" if i == idx else "none"} for i in range(3)]
    dots = ["info-dot active" if i == idx else "info-dot" for i in range(3)]

    return idx, styles[0], styles[1], styles[2], dots[0], dots[1], dots[2]

@app.callback(
    Output(BUBBLE_GRAPH_ID, "figure"),
    Output(BUBBLE_Y_SLIDER_ID, "value"),
    Output(BUBBLE_X_SLIDER_ID, "value"),
    Input(BUBBLE_Y_SLIDER_ID, "value"),
    Input(BUBBLE_X_SLIDER_ID, "value"),
    Input("viz4-info-slide-idx", "data"),
)
def update_bubble(max_visibility, sat_range, question_idx):
    """Un seul callback : sliders manuels ou changement de question (carrousel viz4)."""
    triggered = ctx.triggered_id
    q = question_idx or 0

    if triggered == "viz4-info-slide-idx":
        if q == 0:
            return (
                viz4_bubble.create_figure(BUBBLE_DATA, 10_000_000, [0, 1], q),
                10_000_000,
                [0, 1],
            )
        if q == 1:
            return (
                viz4_bubble.create_figure(BUBBLE_DATA, 3_000_000, [0.7, 1], q),
                3_000_000,
                [0.7, 1],
            )
        if q == 2:
            return (
                viz4_bubble.create_figure(BUBBLE_DATA, 2_000_000, [0, 1], q),
                2_000_000,
                [0, 1],
            )
        raise PreventUpdate

    return (
        viz4_bubble.create_figure(
            BUBBLE_DATA,
            max_visibility=max_visibility,
            sat_range=sat_range,
            question_idx=q,
        ),
        dash.no_update,
        dash.no_update,
    )

# ---------------------------------------------------------------------------
# Viz 5, filters and info carousel — 2 slides
# ---------------------------------------------------------------------------
@app.callback(
    Output("viz5-info-slide-idx", "data"),
    Output("viz5-info-slide-0", "style"),
    Output("viz5-info-slide-1", "style"),
    Output("viz5-info-dot-0", "className"),
    Output("viz5-info-dot-1", "className"),
    Input("viz5-info-prev-btn", "n_clicks"),
    Input("viz5-info-next-btn", "n_clicks"),
    State("viz5-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def advance_viz5_info_carousel(prev_clicks, next_clicks, current_idx):
    triggered = ctx.triggered_id
    current = current_idx or 0
    
    if triggered == "viz5-info-prev-btn":
        next_idx = (current - 1) % 2
    else:
        next_idx = (current + 1) % 2
    
    styles = [{"display": "flex" if i == next_idx else "none"} for i in range(2)]
    dots = ["info-dot active" if i == next_idx else "info-dot" for i in range(2)]
    return next_idx, styles[0], styles[1], dots[0], dots[1]

@app.callback(
    Output(DOT_GRAPH_ID, "figure"),
    Input(DOT_SLIDER_ID, "value"),
)
def update_dot(max_playtime):
    return viz5_dot.create_figure(
        data,
        max_playtime if max_playtime is not None else viz5_dot.DOT_SLIDER_MAX,
    )
    
# ---------------------------------------------------------------------------
# Viz 6, filters and info carousel — navigate between the 3 insight slides
# ---------------------------------------------------------------------------
@app.callback(
    Output("viz6-info-slide-idx", "data"),
    Output("viz6-info-slide-0", "style"),
    Output("viz6-info-slide-1", "style"),
    Output("viz6-info-slide-2", "style"),
    Output("viz6-info-dot-0", "className"),
    Output("viz6-info-dot-1", "className"),
    Output("viz6-info-dot-2", "className"),
    Input("viz6-info-prev-btn", "n_clicks"),
    Input("viz6-info-next-btn", "n_clicks"),
    State("viz6-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def advance_viz6_info_carousel(prev_clicks, next_clicks, current_idx):
    triggered = ctx.triggered_id
    current = current_idx or 0
    
    if triggered == "viz6-info-prev-btn":
        next_idx = (current - 1) % 3
    else:
        next_idx = (current + 1) % 3
    
    styles = [{"display": "flex" if i == next_idx else "none"} for i in range(3)]
    dots = ["info-dot active" if i == next_idx else "info-dot" for i in range(3)]
    return next_idx, styles[0], styles[1], styles[2], dots[0], dots[1], dots[2]

@app.callback(
    Output(VIOLIN_SLIDER_ID, "value"),
    Input("viz6-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def sync_violin_slider_to_slide(slide_idx):
    return VIOLIN_SLIDE_SLIDER_VALUES[(slide_idx or 0) % 3]
 
@app.callback(
    Output(VIOLIN_GRAPH_ID, "figure"),
    Input(VIOLIN_SLIDER_ID, "value"),
    Input("viz6-info-slide-idx", "data"),
)
def update_violin(max_games, slide_idx):
    import viz6_violin.plot_generate as v6_plot
 
    if ctx.triggered_id == "viz6-info-slide-idx":
        max_games = VIOLIN_SLIDE_SLIDER_VALUES[(slide_idx or 0) % 3]
    elif max_games is None:
        max_games = VIOLIN_REAL_MAX
 
    my_df = v6_plot.filter_by_max_games(VIOLIN_DATA, max_games)
 
    fig = v6_plot.generate_plot(my_df)
    fig = v6_plot.update_axes_labels(fig)
    fig = v6_plot.update_legend(fig)
    fig = v6_plot.update_hover_template(fig)
    fig.update_layout(dragmode=False)
    return fig


if __name__ == "__main__":
    app.run(debug=False)
