"""
Tooltip template module for the genre evolution line chart.

This module:
- defines the hover tooltip content for multi-series line traces
- displays genre name, release year, and estimated commercial success
"""


def get_hover_template():
    """
    Return the hover tooltip template for the line chart.

    Displays:
        - Genre name (from customdata)
        - Release year (x-axis value)
        - Estimated number of owners (y-axis value, formatted with thousands separator)

    Returns:
        str: Plotly hovertemplate string.
    """
    return (
        "<b>%{customdata[0]}</b><br>"
        "Année : %{x}<br>"
        "Propriétaires estimés : %{y:,.0f}"
        "<extra></extra>"
    )
