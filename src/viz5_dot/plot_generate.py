'''
    This file contains the code for the plot.
'''

import plotly.express as px

import viz1_scatter.hover_template

#TODO : add more functions if needed

def generate_plot(my_df):
    '''
        Generates the plot.

        #TODO : add more details about the plot (axes, colors, sizes, etc.)

        Args:
            my_df: The dataframe to display
            #TODO : add more arguments if needed
        Returns:
            The generated figure
    '''
    #TODO : Define figure

    return None

def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update labels
    # fig.update_xaxes(title_text="x axis")
    # fig.update_yaxes(title_text="y axis")
    return fig


def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    # TODO : Change if you want to use a different template
    # fig.update_layout(template='simple_white')
    return fig

def update_legend(fig):
    '''
        Updated the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update legend 
    # fig.update_layout(legend_title_text="Legend")
    return fig

def update_hover_template(fig):
    '''
        Sets the hover template of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''

    # DONE : Set the hover template (#TODO : change the hover template if you want to use a different one)
    template = viz1_scatter.hover_template.get_hover_template()
    
    # fig.update_traces(hovertemplate=template)

    # for frame in fig.frames:
    #     for trace in frame.data:
    #         trace.hovertemplate = template
            
    return fig