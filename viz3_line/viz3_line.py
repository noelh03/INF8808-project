'''
    Contains source code for the third visualisation of the project. 
    It is a ? plot, showing the relationship ... TODO
'''

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
    
    # fig.update_layout(height=600, width=1000)
    # fig.update_layout(dragmode=False)
    return fig