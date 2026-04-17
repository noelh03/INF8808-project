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
    Hover classique pour un point = un jeu.
    """
    return (
        "<b>%{hovertext}</b><br>"
        "Prix : %{x:.2f} $<br>"
        "Type : %{customdata[0]}<br>"
        "Succès estimé : %{y:,.0f}"
        "<extra></extra>"
    )


def get_aggregated_hover_template():
    """
    Hover pour points agrégés (plusieurs jeux).
    """
    return (
        "<b>Prix :</b> %{x}$<br>"
        "<b>Succès commercial estimé :</b> %{y:,.0f}<br>"
        "<b>Nombre de jeux :</b> %{customdata[0]}<br><br>"
        "<b>Jeux :</b><br>"
        "%{customdata[1]}"
        "<extra></extra>"
    )


def format_game_list_hover(game_names, limit=10):
    """
    Formate une liste HTML de jeux pour le hover.
    """
    if not game_names:
        return "Aucun jeu"

    shown = game_names[:limit]

    formatted = "".join(
        f"• {name}<br>" for name in shown
    )

    remaining = len(game_names) - len(shown)

    if remaining > 0:
        formatted += f"<br><i>... et {remaining} autre(s)</i>"

    return formatted