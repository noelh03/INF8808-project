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
