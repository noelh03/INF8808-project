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

import copy
from pathlib import Path

from dash import Dash, html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import pandas as pd

from viz1_scatter import viz1_scatter
from viz2_box import viz2_box
from viz3_line import viz3_line
from viz4_bubble import viz4_bubble
from viz5_dot import viz5_dot
from viz6_violin import viz6_violin
from viz3_line.preprocess import MAIN_GENRES as VIZ3_MAIN_GENRES
import sidebar

SCATTER_SLIDER_ID = "scatter-price-slider"
SCATTER_GRAPH_ID = "scatter-price-graph"

LINE_CHECKLIST_ID = viz3_line.LINE_CHECKLIST_ID
LINE_GRAPH_ID = viz3_line.LINE_GRAPH_ID
LINE_ALL_ID = viz3_line.LINE_ALL_ID
def _apply_restyle_patch_to_figure(fig_dict, restyle_data):
    """
    Merge a Plotly restyle event into a figure dict (legend clicks / double-clicks).
    restyle_data: [patch_dict, trace_indices] as emitted by dcc.Graph restyleData.
    """
    if not fig_dict or not restyle_data or len(restyle_data) < 2:
        return fig_dict
    patch, indices = restyle_data[0], restyle_data[1]
    if patch is None or indices is None:
        return fig_dict

    fig = copy.deepcopy(fig_dict)
    n = len(fig.get("data", []))
    if n == 0:
        return fig

    if isinstance(indices, int):
        indices = [indices]
    else:
        indices = list(indices)

    for key, val in patch.items():
        if key == "visible" and isinstance(val, list) and len(val) == n:
            for i in range(n):
                fig["data"][i][key] = val[i]
            continue

        for i, idx in enumerate(indices):
            if idx < 0 or idx >= n:
                continue
            if isinstance(val, list):
                if len(val) == len(indices):
                    fig["data"][idx][key] = val[i]
                elif len(val) == 1:
                    fig["data"][idx][key] = val[0]
                else:
                    fig["data"][idx][key] = val[i] if i < len(val) else val[-1]
            else:
                fig["data"][idx][key] = val
    return fig


def _figure_to_viz3_checklist_values(fig_dict):
    """Derive checklist values from trace visibility (matches legend state)."""

    def trace_on_plot(tr):
        v = tr.get("visible")
        if v is None or v is True:
            return True
        if v in (False, "legendonly"):
            return False
        return True

    visible_main = set()
    others_on = False
    for tr in fig_dict.get("data", []):
        if not trace_on_plot(tr):
            continue
        name = tr.get("name")
        if name == "Others":
            others_on = True
        elif name in VIZ3_MAIN_GENRES:
            visible_main.add(name)

    ordered = [g for g in VIZ3_MAIN_GENRES if g in visible_main]
    if others_on:
        ordered.append("Others")
    return ordered



def make_section(section_id, kicker, title, description, viz_layout, prev_href, next_href, info_content=None):
    """
    Build a full story section with:
    - intro block (kicker, title, "?" info toggle, description)
    - section body: viz card on the left, side-nav arrows on the right

    info_content: optional Dash children for the "?" info panel.
                  Defaults to a placeholder message.
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
                                        info_content if info_content is not None
                                        else "Les informations complémentaires seront ajoutées ici.",
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

app = Dash(
    __name__,
    assets_folder=str(BASE_DIR / "assets"),
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
)
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
                            "Mode de jeu et succès commercial",
                            "Explorer si les jeux solo, hybrides ou exclusivement multijoueur "
                            "se distinguent par leur performance commerciale estimée, "
                            "et observer comment chaque catégorie se répartit sur l'échelle des propriétaires.",
                            viz2_box_layout, "#scatter", "#line",
                            info_content=html.Div(
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
                            ),
                        ),
                        make_section(
                            "line", "Section 3",
                            "Le succès commercial des différents genres selon leur année de sortie",
                            "Comparer l'évolution du nombre estimé de propriétaires par genre de 1997 à 2025, "
                            "et observer quels genres ont gagné ou perdu en importance au fil des années.",
                            viz3_line_layout, "#box", "#bubble",
                            info_content=html.Div(
                                className="info-carousel",
                                children=[
                                    dcc.Store(id="viz3-info-slide-idx", data=0),
                                    html.Div(
                                        id="viz3-info-slide-0",
                                        className="info-slide",
                                        children=[
                                            html.Span("1 / 3", className="info-slide-counter"),
                                            html.H4(
                                                className="info-block-title",
                                                children=[
                                                    html.I(className="fa-solid fa-trophy info-slide-icon"),
                                                    html.Span(
                                                        " Certains genres génèrent-ils un succès commercial supérieur aux autres ?",
                                                    ),
                                                ],
                                            ),
                                            html.P(
                                                "Oui ! Action domine avec 6,7 milliards de propriétaires cumulés. Son pic de 666 M en 2017 est le plus haut du graphique, porté par PUBG (150 M) et Unturned (75 M). Cependant, Dota 2 (150 M, Free To Play/Action) avait déjà créé un premier pic majeur en 2013. Indie (4,7 milliards) et Adventure (4,5 milliards) sont proches pour la seconde place: Adventure culmine à 551 M en 2017 grâce à PUBG, et avait connu un premier pic en 2015 avec GTA V (75 M). RPG (2,8 milliards) et Free To Play (2,3 milliards) complètent le top 5."
                                            ),
                                            html.Div(className="game-logo-strip", children=[
                                                html.A(href="https://store.steampowered.com/app/570/Dota_2/", target="_blank", className="game-logo-chip", children=[
                                                    html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                                                    html.Span("Dota 2", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/", target="_blank", className="game-logo-chip", children=[
                                                    html.Img(src="/assets/logos/pubg.png", className="game-logo-img"),
                                                    html.Span("PUBG", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/730/CounterStrike_2/", target="_blank", className="game-logo-chip", children=[
                                                    html.Img(src="/assets/logos/csgo.png", className="game-logo-img"),
                                                    html.Span("CS2", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/", target="_blank", className="game-logo-chip", children=[
                                                    html.Img(src="/assets/logos/gtaV.png", className="game-logo-img"),
                                                    html.Span("GTA V", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/1623730/Palworld/", target="_blank", className="game-logo-chip", children=[
                                                    html.Img(src="/assets/logos/palworld.png", className="game-logo-img"),
                                                    html.Span("Palworld", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/304930/Unturned/", target="_blank", className="game-logo-chip", children=[
                                                    html.Img(src="/assets/logos/unturned.png", className="game-logo-img"),
                                                    html.Span("Unturned", className="game-logo-label"),
                                                ]),
                                            ]),
                                        ],
                                    ),
                                    html.Div(
                                        id="viz3-info-slide-1",
                                        className="info-slide",
                                        style={"display": "none"},
                                        children=[
                                            html.Span("2 / 3", className="info-slide-counter"),
                                            html.H4(
                                                className="info-block-title",
                                                children=[
                                                    html.I(className="fa-solid fa-calendar-days info-slide-icon"),
                                                    html.Span(
                                                        " L’année de sortie influence-t-elle le succès commercial moyen d’un jeu ?",
                                                    ),
                                                ],
                                            ),
                                            html.P(
                                                "Avant 2013, toutes les courbes restent basses. C'est normal: Steam démarrait. Dota 2 crée le premier grand pic en 2013 : Le genre Action monte à 466 M, Free To Play à 298 M. C'est là que la plateforme commence à décoller ! Puis en 2017, PUBG (tagué Action, Adventure, Massively Multiplayer et Free To Play) propulse ces 4 genres à leurs records absolus en même temps. RPG est la seule exception : son record est en 2024 à 383 M, grâce à Palworld (75 M) et Black Myth: Wukong (75 M)."
                                            ),
                                            html.Div(className="game-logo-strip", children=[
                                                html.A(href="https://store.steampowered.com/app/570/Dota_2/", target="_blank", className="game-logo-chip game-logo-chip--year", children=[
                                                    html.Span("2013", className="game-logo-year-badge"),
                                                    html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                                                    html.Span("Dota 2", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/", target="_blank", className="game-logo-chip game-logo-chip--year", children=[
                                                    html.Span("2017", className="game-logo-year-badge"),
                                                    html.Img(src="/assets/logos/pubg.png", className="game-logo-img"),
                                                    html.Span("PUBG", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/1623730/Palworld/", target="_blank", className="game-logo-chip game-logo-chip--year", children=[
                                                    html.Span("2024", className="game-logo-year-badge"),
                                                    html.Img(src="/assets/logos/palworld.png", className="game-logo-img"),
                                                    html.Span("Palworld", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/2358720/Black_Myth_Wukong/", target="_blank", className="game-logo-chip game-logo-chip--year", children=[
                                                    html.Span("2024", className="game-logo-year-badge"),
                                                    html.Img(src="/assets/logos/blackmyth.png", className="game-logo-img"),
                                                    html.Span("Black Myth", className="game-logo-label"),
                                                ]),
                                            ]),
                                        ],
                                    ),
                                    html.Div(
                                        id="viz3-info-slide-2",
                                        className="info-slide",
                                        style={"display": "none"},
                                        children=[
                                            html.Span("3 / 3", className="info-slide-counter"),
                                            html.H4(
                                                className="info-block-title",
                                                children=[
                                                    html.I(className="fa-solid fa-chart-line info-slide-icon"),
                                                    html.Span(" Certains genres ont-ils gagné ou perdu en importance au fil du temps ?"),
                                                ],
                                            ),
                                            html.P(
                                                "Massively Multiplayer est le cas le plus flagrant : PUBG l'a propulsé à 332 M en 2017, mais dès 2019 il s'effondre à 27 M (-92 %). Free To Play a aussi décliné : ancré par Dota 2 dès 2013 (298 M), il culmine à 463 M en 2017, puis retombe à 270 M en 2020 malgré le sursaut d'Apex Legends (150 M). À l'inverse, RPG progresse constamment : 249 M en 2021, 383 M en 2024 (+54 % en 3 ans), grâce à Palworld et Black Myth: Wukong. Pour 2025, une baisse par rapport aux années précédentes est attendue : l'année vient de s'achever et les jeux sortis n'ont pas encore eu le temps d'accumuler autant de propriétaires estimés."
                                            ),
                                            html.Div(className="game-logo-strip", children=[
                                                html.A(href="https://store.steampowered.com/app/570/Dota_2/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--down", children=[
                                                    html.I(className="fa-solid fa-arrow-trend-down game-logo-trend-icon"),
                                                    html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                                                    html.Span("Dota 2", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--down", children=[
                                                    html.I(className="fa-solid fa-arrow-trend-down game-logo-trend-icon"),
                                                    html.Img(src="/assets/logos/pubg.png", className="game-logo-img"),
                                                    html.Span("PUBG", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/1172470/Apex_Legends/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--down", children=[
                                                    html.I(className="fa-solid fa-arrow-trend-down game-logo-trend-icon"),
                                                    html.Img(src="/assets/logos/apex.png", className="game-logo-img"),
                                                    html.Span("Apex", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/1623730/Palworld/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--up", children=[
                                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                                    html.Img(src="/assets/logos/palworld.png", className="game-logo-img"),
                                                    html.Span("Palworld", className="game-logo-label"),
                                                ]),
                                                html.A(href="https://store.steampowered.com/app/2358720/Black_Myth_Wukong/", target="_blank", className="game-logo-chip game-logo-chip--trend game-logo-chip--up", children=[
                                                    html.I(className="fa-solid fa-arrow-trend-up game-logo-trend-icon"),
                                                    html.Img(src="/assets/logos/blackmyth.png", className="game-logo-img"),
                                                    html.Span("Black Myth", className="game-logo-label"),
                                                ]),
                                            ]),
                                        ],
                                    ),
                                    html.Div(
                                        className="info-carousel-footer",
                                        children=[
                                            html.Div(
                                                className="info-progress",
                                                children=[
                                                    html.Span(id="viz3-info-dot-0", className="info-dot active"),
                                                    html.Span(id="viz3-info-dot-1", className="info-dot"),
                                                    html.Span(id="viz3-info-dot-2", className="info-dot"),
                                                ],
                                            ),
                                            html.Button(
                                                "→",
                                                id="viz3-info-next-btn",
                                                className="info-nav-btn",
                                                n_clicks=0,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
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


@app.callback(
    Output(LINE_GRAPH_ID, "figure"),
    Input(LINE_CHECKLIST_ID, "value"),
)
def update_line_genres(selected_genres):
    return viz3_line.create_figure(data, selected_genres=selected_genres or [])


@app.callback(
    Output(LINE_CHECKLIST_ID, "value"),
    Input(LINE_ALL_ID, "value"),
    Input(LINE_GRAPH_ID, "restyleData"),
    State(LINE_GRAPH_ID, "figure"),
    State(LINE_CHECKLIST_ID, "value"),
    prevent_initial_call=True,
)
def update_checklist(all_value, restyle_data, figure, current_checklist):
    """
    Single source of checklist mutations:
    - 'Tout' checkbox toggled → select or clear all genres
    - Legend click/double-click → sync checkboxes to what is visible on graph
    """
    triggered = ctx.triggered_id

    if triggered == LINE_ALL_ID:
        if "All" in (all_value or []):
            return list(viz3_line.CHECKLIST_GENRES)
        if set(current_checklist or []) >= set(viz3_line.CHECKLIST_GENRES):
            return []
        raise PreventUpdate

    if triggered == LINE_GRAPH_ID:
        if not restyle_data or not figure:
            raise PreventUpdate
        merged = _apply_restyle_patch_to_figure(figure, restyle_data)
        new_vals = _figure_to_viz3_checklist_values(merged)
        if new_vals == list(current_checklist or []):
            raise PreventUpdate
        return new_vals

    raise PreventUpdate


@app.callback(
    Output(LINE_ALL_ID, "value"),
    Input(LINE_CHECKLIST_ID, "value"),
    prevent_initial_call=True,
)
def sync_all_checkbox(selected_genres):
    """Keep the 'Tous les genres' checkbox in sync with individual genre checkboxes."""
    all_genres = set(viz3_line.CHECKLIST_GENRES)
    if set(selected_genres or []) >= all_genres:
        return ["All"]
    return []


# ---------------------------------------------------------------------------
# Viz 3 info carousel — navigate between the 3 insight slides
# ---------------------------------------------------------------------------
@app.callback(
    Output("viz3-info-slide-idx", "data"),
    Output("viz3-info-slide-0", "style"),
    Output("viz3-info-slide-1", "style"),
    Output("viz3-info-slide-2", "style"),
    Output("viz3-info-dot-0", "className"),
    Output("viz3-info-dot-1", "className"),
    Output("viz3-info-dot-2", "className"),
    Input("viz3-info-next-btn", "n_clicks"),
    State("viz3-info-slide-idx", "data"),
    prevent_initial_call=True,
)
def advance_info_carousel(n_clicks, current_idx):
    next_idx = ((current_idx or 0) + 1) % 3
    styles = [{"display": "flex"  if i == next_idx else "none"} for i in range(3)]
    dots = ["info-dot active" if i == next_idx else "info-dot" for i in range(3)]
    return next_idx, styles[0], styles[1], styles[2], dots[0], dots[1], dots[2]



if __name__ == "__main__":
    app.run(debug=True)
