'''
    Provides the template for the tooltips.
'''


def get_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : Game name, publisher type, number of games published, 
        commercial success.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    tooltip = (
        "<b>%{hovertext}</b><br>"
        "<b>Type d'éditeur :</b> %{data.name}<br>"
        "<b>Nb jeux publiés :</b> %{x}<br>"
        "<b>Succès commercial :</b> %{y}<br>"
        "<extra></extra>"
    )
    return tooltip
