'''
    Contains source code for the fifth visualisation of the project. 
    It is a ? plot, showing the relationship ... TODO
'''
from dash import html, dcc

import viz5_dot.preprocess
import viz5_dot.plot_generate

def create_figure(my_df):
    '''
        Calls the functions to preprocess the data and generate the plot for the fifth visualisation.
    '''
    my_df = viz5_dot.preprocess.step1(my_df)
    my_df = viz5_dot.preprocess.step2(my_df)
    
    fig = viz5_dot.plot_generate.generate_plot(my_df)
    fig = viz5_dot.plot_generate.update_template(fig)
    fig = viz5_dot.plot_generate.update_legend(fig)
    fig = viz5_dot.plot_generate.update_axes_labels(fig)
    fig = viz5_dot.plot_generate.update_hover_template(fig)
    #TODO : call other functions if added in plot_generate.py

    return fig

def create_layout(my_df):
    fig = create_figure(my_df)
    
    #TODO : uncomment
    # fig.update_layout(height=600, width=1000)
    # fig.update_layout(dragmode=False)

    return html.Div(id="dot", className='viz-block', children=[
        html.H3("Dot Plot"),
        dcc.Graph(className='graph', figure=fig, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
        ))
    ])