"""
Sidebar navigation module for the scrollytelling interface.

This module:
- builds the sidebar layout and navigation links
- manages open/close interaction behavior
- enables smooth navigation between narrative sections

It enhances usability by providing a structured overview of the story flow.
"""

from dash import html, Output, Input, State, ctx

TOGGLE_BTN_ID = "toggle-btn"
OVERLAY_ID = "overlay"
SIDEBAR_ID = "sidebar"

NAV_ITEMS = [
    ("Accueil", "#hero"),
    ("L’effet du prix sur le succès", "#scatter"),
    ("Le rôle du mode de jeu", "#box"),
    ("Quels genres dominent dans le temps ?", "#line"),
    ("Visibilité ou satisfaction ?", "#bubble"),
    ("Le temps de jeu compte-t-il ?", "#dot"),
    ("Qui sont les leaders du marché ?", "#violin"),
]


def nav_item(label, href):
    """Create a sidebar navigation link."""
    return html.A(
        className="nav-link",
        href=href,
        children=[
            html.Span(className="nav-icon"),
            html.Span(label, className="nav-text"),
        ],
    )


def create_sidebar():
    """Create the sidebar layout."""
    return html.Div(
        children=[
            html.Button("☰", id=TOGGLE_BTN_ID, n_clicks=0, className="toggle-btn"),
            html.Div(id=OVERLAY_ID, className="overlay", n_clicks=0),
            html.Div(
                id=SIDEBAR_ID,
                className="sidebar",
                children=[
                    html.Div(
                        className="sidebar-header",
                        children=[
                            html.H2("Navigation", className="sidebar-title"),
                            html.P("SCROLLYTELLING", className="sidebar-subtitle"),
                        ],
                    ),
                    html.Nav(
                        className="sidebar-nav",
                        children=[nav_item(label, href) for label, href in NAV_ITEMS],
                    ),
                ],
            ),
        ]
    )


def register_sidebar_callbacks(app):
    """Register callbacks for opening and closing the sidebar."""

    @app.callback(
        Output(SIDEBAR_ID, "className"),
        Output(OVERLAY_ID, "className"),
        Input(TOGGLE_BTN_ID, "n_clicks"),
        Input(OVERLAY_ID, "n_clicks"),
        State(SIDEBAR_ID, "className"),
    )
    def toggle_sidebar(btn_clicks, overlay_clicks, sidebar_class):
        sidebar_class = sidebar_class or "sidebar"
        trigger = ctx.triggered_id

        if trigger is None:
            return "sidebar", "overlay"

        if trigger == OVERLAY_ID:
            return "sidebar", "overlay"

        if trigger == TOGGLE_BTN_ID:
            classes = sidebar_class.split()
            if "open" in classes:
                return "sidebar", "overlay"
            return "sidebar open", "overlay open"

        return "sidebar", "overlay"