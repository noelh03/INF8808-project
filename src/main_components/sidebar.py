"""
Sidebar navigation module for the scrollytelling interface.

This module:
- builds the sidebar layout and navigation links
- manages open/close interaction behavior
- enables smooth navigation between narrative sections

It enhances usability by providing a structured overview of the story flow.
"""

from dash import html, Output, Input, State, ctx
from utils.constants import (TOGGLE_BTN_ID, OVERLAY_ID, SIDEBAR_ID, NAV_ITEMS)


def nav_item(label, href, idx):
    """Create a sidebar navigation link."""
    return html.A(
        id=f"nav-link-{idx}",
        className="nav-link",
        href=href,
        n_clicks=0,
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
                        children=[nav_item(label, href, i) for i, (label, href) in enumerate(NAV_ITEMS)],
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
        *[Input(f"nav-link-{i}", "n_clicks") for i in range(len(NAV_ITEMS))],
        State(SIDEBAR_ID, "className"),
    )
    def toggle_sidebar(btn_clicks, overlay_clicks, *args):
        sidebar_class = args[-1] or "sidebar"
        trigger = ctx.triggered_id

        if trigger and str(trigger).startswith("nav-link"):
            return "sidebar", "overlay"

        if trigger == OVERLAY_ID:
            return "sidebar", "overlay"

        if trigger == TOGGLE_BTN_ID:
            classes = sidebar_class.split()
            if "open" in classes:
                return "sidebar", "overlay"
            return "sidebar open", "overlay open"

        return "sidebar", "overlay"