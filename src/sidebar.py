from dash import html, Output, Input, State, callback_context


def create_sidebar():
    return html.Div(children=[

        html.Button("☰", id="toggle-btn", n_clicks=0, className="toggle-btn"),

        html.Div(id="overlay", className="overlay"),

        html.Div(id="sidebar", className="sidebar", children=[
            html.H3("Navigation"),
            html.A("Scatter Plot", href="#scatter"),
            html.A("Box Plot", href="#box"),
            html.A("Line Chart", href="#line"),
            html.A("Bubble Chart", href="#bubble"),
            html.A("Dot Plot", href="#dot"),
            html.A("Violin Plot", href="#violin"),
        ]),

    ])
    
def register_sidebar_callbacks(app):
    @app.callback(
        Output("sidebar", "className"),
        Output("overlay", "className"),
        Output("content", "className"),
        Input("toggle-btn", "n_clicks"),
        Input("overlay", "n_clicks"),
        State("sidebar", "className"),
    )
    def toggle_sidebar(btn, overlay_click, sidebar_class):
        ctx = callback_context
        if not ctx.triggered:
            return "sidebar", "overlay", "content"

        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger == "overlay":
            return "sidebar", "overlay", "content"
        if trigger == "toggle-btn":
            if "open" in sidebar_class:
                return "sidebar", "overlay", "content"
            else:
                return "sidebar open", "overlay open", "content shift"

        return "sidebar", "overlay", "content"