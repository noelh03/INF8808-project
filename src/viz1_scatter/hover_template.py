"""
Tooltip template module for interactive visualizations.

This module:
- defines reusable hover templates for Plotly figures
- standardizes tooltip content formatting across visualizations
- improves readability and narrative clarity during user interaction

It centralizes tooltip design to ensure consistency and maintainability.
"""

def get_hover_template():
    """
    Return the hover tooltip template for the scatter plot.

    Returns:
        str: Plotly hovertemplate string.
    """
    return (
        "<b>%{hovertext}</b><br>"
        "Prix : %{x:.2f} $<br>"
        "Type : %{customdata[0]}<br>"
        "Succès estimé : %{y:,.0f}"
        "<extra></extra>"
    )