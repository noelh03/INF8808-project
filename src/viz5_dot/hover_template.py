'''
    Provides the template for the tooltips.
'''


def get_hover_template():
    '''
        Sets the template for the hover tooltips.

        Contains labels, followed by their corresponding
        value and units where appropriate (satisfaction from customdata,
        playtime on y-axis, total reviews).

        The labels' font is bold and the values are normal weight.

        Returns:
            str: Plotly hovertemplate string.
    '''
    tooltip = (
        "<b>%{hovertext}</b><br>"
        "Satisfaction : %{customdata[0]:.1f}<br>"
        "Temps moyen : %{y:.1f} h<br>"
        "Avis : %{customdata[1]:,.0f}"
        "<extra></extra>"
    )
    return tooltip
