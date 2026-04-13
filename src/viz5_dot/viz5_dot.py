'''
    Contains source code for the fifth visualisation of the project. 
    It is a dot plot, showing the relationship between satisfaction and playtime, 
    with the color of the dots representing the number of reviews.
'''
from dash import html, dcc
import viz5_dot.preprocess as preprocess
import viz5_dot.plot_generate as plot_generate

DOT_SLIDER_MIN = 0
DOT_SLIDER_MAX = 6000
DOT_SLIDER_STEP = 100
DOT_SLIDER_HEIGHT = 260

def create_figure(df, max_playtime=6000):
    '''
        Calls the functions to preprocess the data and generate the plot for the fifth visualisation.
        
        Args:
            df: The dataframe to display
            max_playtime: The maximum playtime to display (used for filtering the data)
        Returns:
            The generated figure
    '''
    df = preprocess.compute_metrics(df)
    df = preprocess.filter_data(df)
    fig = plot_generate.generate_plot(df, max_playtime)

    return fig

def create_layout(df, max_playtime=6000, slider_id="dot-slider", graph_id="dot-graph"):
    '''
        Creates the layout for the fifth visualisation (dot plot).
        
        Args:
            df: The dataframe to display
            max_playtime: The maximum playtime to display (used for filtering the data)
            slider_id: The ID for the slider component
            graph_id: The ID for the graph component
        Returns:
            The layout for the fifth visualisation
    '''
    
    fig = create_figure(df, max_playtime)
    slider_marks = {i: f"{i//1000}k" for i in range(0, DOT_SLIDER_MAX + 1, 1000)}

    return html.Div(className="viz-inner", children=[
        html.Div(className="dot-main-layout", children=[
            html.Div(
                className="dot-graph-column",
                children=[
                    dcc.Graph(
                        id=graph_id,
                        figure=fig,
                        config={"displayModeBar": False, "responsive": True},
                        className="graph",
                        style={"height": "100%"},
                    ),
                ],
            ),

            html.Div(className="dot-side-panel", children=[
                html.Div("Filtrer par temps de jeu moyen", className="slider-title"),
                dcc.Slider(
                    id=slider_id,
                    min=DOT_SLIDER_MIN,
                    max=DOT_SLIDER_MAX,
                    step=DOT_SLIDER_STEP,
                    value=DOT_SLIDER_MAX,
                    vertical=True,
                    verticalHeight=DOT_SLIDER_HEIGHT,
                    marks=slider_marks,
                    tooltip={
                        "placement": "left",
                        "always_visible": True,
                    },
                ),
            ])
        ])
    ])