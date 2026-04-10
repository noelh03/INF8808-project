"""Plotly hover template for the viz3 line chart."""

def get_hover_template():
    """Hover template: genre, year, owners (millions, same as y-axis)."""
    return (
        "<b>%{customdata[0]}</b><br>"
        "Année : %{x}<br>"
        "Propriétaires estimés : %{y:,.0f}M"
        "<extra></extra>"
    )
