'''
    Provides the tooltip templates for the second visualisation (beeswarm).
'''


def get_hover_template():
    '''
    Tooltip shown when hovering an individual game point.

    Returns:
        str: Plotly hovertemplate string.
    '''
    return (
        "<b>%{customdata[0]}</b><br>"
        "<b>Propriétaires estimés :</b> %{customdata[1]}<br>"
        "<extra></extra>"
    )
