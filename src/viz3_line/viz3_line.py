"""
Layout and figure controller for the genre evolution line chart.

This module:
- loads and preprocesses the year × genre CSV independently of the main dataset
- generates the multi-series interactive line figure
- defines the Dash layout including the graph and the genre filter checklist
- exports component IDs used by the callback registered in app.py
"""

from dash import dcc, html

from viz3_line.preprocess import preprocess_data, MAIN_GENRES
from viz3_line.plot_generate import generate_plot, GENRE_COLORS, CHECKLIST_GENRES, OTHERS_COLOR

LINE_CHECKLIST_ID = "line-genre-checklist"
LINE_GRAPH_ID = "line-genre-graph"
LINE_ALL_ID = "line-all-toggle"

_df_long_cache = None


def _get_df_long(df):
    """
    Return the preprocessed long-format DataFrame, computing it once and
    caching the result for all subsequent calls (e.g. every checkbox change).

    Args:
        df: The raw games DataFrame (games.csv).

    Returns:
        pd.DataFrame: Long-format DataFrame with columns [Year, Genre, Owners].
    """
    global _df_long_cache
    if _df_long_cache is None:
        _df_long_cache = preprocess_data(df)
    return _df_long_cache


def create_figure(df, selected_genres=None):
    """
    Plot the genre evolution data from the games dataframe.

    Preprocessing is done once and cached; only the figure is regenerated
    on each call (e.g. when the genre filter checklist changes).

    Args:
        df: The raw games DataFrame (games.csv).
        selected_genres: List of checklist values that are active.
                         Defaults to CHECKLIST_GENRES (all shown).

    Returns:
        go.Figure: The configured multi-series line chart.
    """
    if selected_genres is None:
        selected_genres = CHECKLIST_GENRES
    df_long = _get_df_long(df)
    return generate_plot(df_long, selected_genres=selected_genres)


def create_layout(my_df):
    """
    Build the Dash layout for the genre evolution line chart section.

    The layout includes the line graph and a genre filter checklist displayed
    as a side panel, mirroring the viz1 scatter layout pattern.

    Args:
        my_df: The raw games DataFrame (games.csv).

    Returns:
        html.Div: The complete layout component.
    """
    fig = create_figure(my_df)

    color_map = {**GENRE_COLORS, "Others": OTHERS_COLOR}
    genre_options = [
        {
            "label": html.Span(
                genre,
                style={"color": color_map.get(genre, "#9E9E9E"), "fontWeight": "600"},
            ),
            "value": genre,
        }
        for genre in CHECKLIST_GENRES
    ]

    return html.Div(
        className="viz-inner",
        children=[
            html.Div(
                className="line-main-layout",
                children=[
                    dcc.Graph(
                        id=LINE_GRAPH_ID,
                        figure=fig,
                        config={"displayModeBar": False, "responsive": True},
                        className="graph",
                        style={"height": "100%"},
                    ),
                    html.Div(
                        className="line-side-panel",
                        children=[
                            html.Div("Filtrez par genre:", className="slider-title"),
                            dcc.Checklist(
                                id=LINE_CHECKLIST_ID,
                                options=genre_options,
                                value=[g for g in CHECKLIST_GENRES if g != "Others"],
                                className="genre-checklist",
                                labelClassName="genre-checklist-label",
                                inputClassName="genre-checklist-input",
                            ),
                            html.Hr(className="genre-checklist-divider"),
                            dcc.Checklist(
                                id=LINE_ALL_ID,
                                options=[{
                                    "label": html.Span(
                                        "Tous les genres",
                                        style={"fontWeight": "700", "color": "#111827"},
                                    ),
                                    "value": "All",
                                }],
                                value=[],
                                className="genre-checklist",
                                labelClassName="genre-checklist-label",
                                inputClassName="genre-checklist-input",
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
                ],),
                    html.Button(
                        "→",
                        id="viz3-info-next-btn",
                        className="info-nav-btn",
                        n_clicks=0,
                    ),
                ],
            ),
        ],
    )