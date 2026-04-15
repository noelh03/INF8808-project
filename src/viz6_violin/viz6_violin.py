'''
    Contains source code for the sixth visualisation of the project. 
    It is a violin plot showing the distribution of commercial success 
    (estimated owners) by publisher experience (number of games published),
    comparing Independent vs Major publishers.
'''
from dash import html, dcc

import viz6_violin.preprocess
import viz6_violin.plot_generate

VIOLIN_SLIDER_MIN = 1
VIOLIN_SLIDER_MAX = 50
VIOLIN_SLIDER_STEP = 1
VIOLIN_SLIDER_HEIGHT = 320

def create_figure(my_df):
    '''
        Calls the functions to preprocess the data and generate the plot for the sixth visualisation.
    '''
    my_df = viz6_violin.preprocess.step1(my_df)
    my_df = viz6_violin.preprocess.step2(my_df)
    my_df = viz6_violin.plot_generate.filter_by_max_games(my_df, VIOLIN_SLIDER_MAX)
    
    fig = viz6_violin.plot_generate.generate_plot(my_df)
    fig = viz6_violin.plot_generate.update_template(fig)
    fig = viz6_violin.plot_generate.update_legend(fig)
    fig = viz6_violin.plot_generate.update_axes_labels(fig)
    fig = viz6_violin.plot_generate.update_hover_template(fig)
    
    return fig

def create_layout(my_df, slider_id="violin-slider", graph_id="violin-graph"):
    preprocessed = viz6_violin.preprocess.step1(my_df.copy())
    real_max = int(preprocessed['nb_games_dev'].max())
    
    global VIOLIN_SLIDER_MAX
    VIOLIN_SLIDER_MAX = real_max   
    fig = create_figure(my_df)
    
    fig.update_layout(dragmode=False)

    slider_marks = {VIOLIN_SLIDER_MIN: str(VIOLIN_SLIDER_MIN)}
    for i in range(50, VIOLIN_SLIDER_MAX, 50):
        slider_marks[i] = str(i)
    slider_marks[VIOLIN_SLIDER_MAX] = str(VIOLIN_SLIDER_MAX)

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
                html.Div(
                    "Filtrer par nb de jeux publiés",
                    className="slider-title"
                ),
                dcc.Slider(
                    id=slider_id,
                    min=VIOLIN_SLIDER_MIN,
                    max=real_max,
                    step=VIOLIN_SLIDER_STEP,
                    value=real_max,
                    vertical=True,
                    verticalHeight=VIOLIN_SLIDER_HEIGHT,
                    marks=slider_marks,
                    tooltip={
                        "placement": "left",
                        "always_visible": True,
                    },
                ),
            ]),
        ]),
    ])