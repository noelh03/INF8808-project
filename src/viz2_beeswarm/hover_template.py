'''
    Provides the tooltip templates for the beeswarm visualisation.
'''


def get_hover_template():
    """
    Build the tooltip template for individual game points.

    Returns:
        str: Plotly hovertemplate string.
    """
    return (
        "<b>%{customdata[0]}</b><br>"
        "<b>Propriétaires estimés :</b> %{customdata[1]}<br>"
        "<extra></extra>"
    )
