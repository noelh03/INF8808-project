'''
    Provides the template for the tooltips.
'''


def get_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : #TODO: add labels name.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    #TODO : Generate tooltip
    tooltip = (
        "<b>label1 :</b> %{}<br>" +
        "<b>label2 :</b> %{}<br>" +
        "<extra></extra>"
    )
    return tooltip
