'''
    Contains source code for the third visualisation of the project. 
    It is a ? plot, showing the relationship ... TODO
'''
from dash import html, dcc

import viz3_line.preprocess
import viz3_line.plot_generate

def create_figure(my_df):
    '''
        Calls the functions to preprocess the data and generate the plot for the third visualisation.
    '''
    my_df = viz3_line.preprocess.step1(my_df)
    my_df = viz3_line.preprocess.step2(my_df)
    
    fig = viz3_line.plot_generate.generate_plot(my_df)
    fig = viz3_line.plot_generate.update_template(fig)
    fig = viz3_line.plot_generate.update_legend(fig)
    fig = viz3_line.plot_generate.update_axes_labels(fig)
    fig = viz3_line.plot_generate.update_hover_template(fig)
    #TODO : call other functions if added in plot_generate.py
    
    return fig

def create_layout(my_df):
    fig = create_figure(my_df)
    
    #TODO : uncomment
    # fig.update_layout(height=600, width=1000)
    # fig.update_layout(dragmode=False)

    return html.Div(id="line", className='viz-block', children=[
        html.H3("Line Chart"),
        dcc.Graph(className='graph', figure=fig, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
        ))
    ])