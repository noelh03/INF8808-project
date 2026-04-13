'''
    Provides the template for the tooltips.
'''


def get_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : Satisfaction, Temps moyen, Avis.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    tooltip = (
        "<b>%{hovertext}</b><br>"
        "Satisfaction : %{customdata[0]:.1f}<br>"
        "Temps moyen : %{y:.1f} h<br>"
        "Avis : %{customdata[1]:,.0f}"
        "<extra></extra>"
    )
    return tooltip