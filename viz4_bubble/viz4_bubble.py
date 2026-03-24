'''
    Contains source code for the fourth visualisation of the project. 
    It is a ? plot, showing the relationship ... TODO
'''

import viz4_bubble.preprocess
import viz4_bubble.plot_generate

def create_figure(my_df):
    '''
        Calls the functions to preprocess the data and generate the plot for the fourth visualisation.
    '''
    my_df = viz4_bubble.preprocess.step1(my_df)
    my_df = viz4_bubble.preprocess.step2(my_df)
    
    fig = viz4_bubble.plot_generate.generate_plot(my_df)
    fig = viz4_bubble.plot_generate.update_template(fig)
    fig = viz4_bubble.plot_generate.update_legend(fig)
    fig = viz4_bubble.plot_generate.update_axes_labels(fig)
    fig = viz4_bubble.plot_generate.update_hover_template(fig)
    #TODO : call other functions if added in plot_generate.py
    
    # fig.update_layout(height=600, width=1000)
    # fig.update_layout(dragmode=False)
    return fig