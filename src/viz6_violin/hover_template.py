'''
    Provides the template for the tooltip template for the violin plot traces.
'''


def get_hover_template():
    '''
        Returns the hovertemplate string for Plotly violin traces.
        
         Fields displayed:
            - Game name (bold, from hovertext)
            - Publisher type (from trace name)
            - Number of games published (x-axis value) 
            - Commercial success / estimated owners (y-axis value)

        Returns:
            str: A Plotly-compatible hovertemplate string
    '''
    tooltip = (
        "<b>%{hovertext}</b><br>"
        "<b>Type d'éditeur :</b> %{data.name}<br>"
        "<b>Nb jeux publiés :</b> %{x}<br>"
        "<b>Succès commercial :</b> %{y}<br>"
        "<extra></extra>"
    )
    return tooltip
