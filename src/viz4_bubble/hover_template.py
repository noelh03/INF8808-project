'''
    Provides the template for the tooltips.
'''


def get_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : Satisfaction, Visibilité, Succès estimé.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    tooltip = (
        "<b>%{hovertext}</b><br>"
        "Satisfaction : %{x:.2f}<br>"
        "Visibilité : %{y:,}<br>"
        "Succès estimé : %{marker.size:,.0f}"
        "<extra></extra>"
    )
    return tooltip
