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
import os
from pathlib import Path

from dash import Dash, html, dcc, Input, Output, State, ctx
import dash
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
from dash import callback_context

SCATTER_SLIDER_ID = "scatter-price-slider"
SCATTER_GRAPH_ID = "scatter-price-graph"

LINE_CHECKLIST_ID = viz3_line.LINE_CHECKLIST_ID
LINE_GRAPH_ID = viz3_line.LINE_GRAPH_ID
LINE_ALL_ID = viz3_line.LINE_ALL_ID

BUBBLE_GRAPH_ID = "bubble-graph"
BUBBLE_Y_SLIDER_ID = "bubble-slider-y"
BUBBLE_X_SLIDER_ID = "bubble-slider-x"

DOT_GRAPH_ID = "dot-graph"
DOT_SLIDER_ID = "dot-slider"

VIOLIN_GRAPH_ID = "violin-graph"
VIOLIN_SLIDER_ID = "violin-slider"
VIOLIN_SLIDE_SLIDER_VALUES = [50, 5, 50]

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
                        ],
                    ),
                    html.P(description, className="section-description"),
                ],
            ),
            html.Div(
                className="section-body",
                children=[
                    html.Div(viz_layout, className="viz-card"),
                    (
                        html.Div(
                            info_content,
                            className="section-inline-info",
                        )
                        if info_content is not None
                        else None
                    ),
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


BASE_DIR = os.path.dirname(__file__)
RAW_DATA_PATH = os.path.join(BASE_DIR, "assets", "data", "games.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "assets", "data", "processed")
VIZ1_DATA_PATH = os.path.join(PROCESSED_DIR, "viz1_scatter.csv")
VIZ4_DATA_PATH = os.path.join(PROCESSED_DIR, "viz4_bubble.csv")
VIZ6_DATA_PATH = os.path.join(PROCESSED_DIR, "viz6_violin.csv")


def load_csv_with_fallback(preferred_path, fallback_path):
    if os.path.exists(preferred_path):
        return pd.read_csv(preferred_path)
    return pd.read_csv(fallback_path)

app = Dash(
    __name__,
    assets_folder=os.path.join(BASE_DIR, "assets"),
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
)
server = app.server
app.title = "Project | INF8808"

data = pd.read_csv(RAW_DATA_PATH)
SCATTER_DATA = load_csv_with_fallback(VIZ1_DATA_PATH, RAW_DATA_PATH)
BUBBLE_DATA = load_csv_with_fallback(VIZ4_DATA_PATH, RAW_DATA_PATH)
VIOLIN_DATA = load_csv_with_fallback(VIZ6_DATA_PATH, RAW_DATA_PATH)

if "nb_games_dev" in VIOLIN_DATA.columns:
    VIOLIN_REAL_MAX = int(VIOLIN_DATA["nb_games_dev"].max())
elif {"Publishers", "Name"}.issubset(data.columns):
    _tmp = data.copy()
    _tmp["nb_games_dev"] = _tmp.groupby("Publishers")["Name"].transform("count")
    VIOLIN_REAL_MAX = int(_tmp["nb_games_dev"].max())
else:
    VIOLIN_REAL_MAX = 50

VIOLIN_SLIDE_SLIDER_VALUES = [VIOLIN_REAL_MAX, 5, VIOLIN_REAL_MAX]
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
                            "scatter", "",
                            "Prix et succès commercial",
                            "Comparer la performance commerciale estimée des jeux gratuits et payants, "
                            "et observer comment la distribution évolue selon l'intervalle de prix sélectionné.",
                            viz1_scatter_layout, "#hero", "#box",
                            info_content=html.Div(
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
                                                            html.Img(src="/assets/logos/left4dead2.png", className="game-logo-img"),
                                                            html.Span("Left 4 Dead 2", className="game-logo-label"),
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
                                                        href="https://store.steampowered.com/app/945360/Among_Us/",
                                                        target="_blank",
                                                        className="game-logo-chip",
                                                        children=[
                                                            html.Img(src="/assets/logos/amongus.png", className="game-logo-img"),
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
                                                            html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                                                            html.Span("Dota 2", className="game-logo-label"),
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
                                                            html.Img(src="/assets/logos/dota-2.png", className="game-logo-img"),
                                                            html.Span("Dota 2", className="game-logo-label"),
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
                                                    html.A(
                                                        href="https://store.steampowered.com/app/1172470/Apex_Legends/",
                                                        target="_blank",
                                                        className="game-logo-chip",
                                                        children=[
                                                            html.Img(src="/assets/logos/apex.png", className="game-logo-img"),
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
                            ),
                        ),
                        make_section(
                            "box", "",
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
                            "line", "",
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
                                            html.Button(
                                                "←",
                                                id="viz3-info-prev-btn",
                                                className="info-nav-btn",
                                                n_clicks=0,
                                            ),
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
                            "bubble", "",
                            "Visibilité et succès commercial",
                            "Comparer la performance commerciale estimée des jeux selon leur nombre d’avis, et observer comment la distribution évolue selon l’intervalle de visibilité sélectionné.",
                            viz4_bubble_layout, "#line", "#dot",
                            info_content=html.Div(
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
                        ),
                        make_section(
                            "dot",
                            "",
                            "Satisfaction, temps de jeu et succès commercial",
                            "Comparer la satisfaction et le temps de jeu moyen des jeux selon leur nombre d’avis, et observer comment la distribution évolue selon l’intervalle de temps de jeu sélectionné.",
                            viz5_dot_layout,
                            "#bubble",
                            "#violin",
                            info_content=html.Div(
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
                            ),
                        ),
                        make_section(
                            "violin", "",
                            "Le succès commercial selon l'expérience et le type d'éditeur",
                            "Comparer la distribution du succès commercial selon l'expérience des éditeurs, et observer si les indépendants et les majeurs se distinguent dans leur capacité à générer du succès.",
                            viz6_violin_layout,
                            "#dot",
                            "#hero",
                            info_content=html.Div(
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
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)

@app.callback(
    Output(DOT_GRAPH_ID, "figure"),
    Input(DOT_SLIDER_ID, "value"),
)
def update_dot(max_playtime):
    return viz5_dot.create_figure(
        data,
        max_playtime if max_playtime is not None else viz5_dot.DOT_SLIDER_MAX,
    )


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
        merged = _apply_restyle_patch_to_figure(figure, restyle_data)
        new_vals = _figure_to_viz3_checklist_values(merged)
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
# Viz 1 info carousel — navigate between the 3 insight slides
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

# ---------------------------------------------------------------------------
# Viz 4 info carousel — navigate between the 3 insight slides
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
# Viz 5 info carousel — 2 slides
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
