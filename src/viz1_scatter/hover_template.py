"""
    Provides the template for the tooltips.
"""


def get_hover_template():
    '''
        Sets the template for the hover tooltips.

        Used when each point represents a single game.

        Contains labels followed by their corresponding
        value and units where appropriate:
        Prix, Type, Succès estimé.

        The labels' font is bold and the values are normal weight.

        returns:
            The content of the tooltip
    '''
    tooltip = (
        "<b>%{hovertext}</b><br>"
        "Prix : %{x:.2f} $<br>"
        "Type : %{customdata[0]}<br>"
        "Succès estimé : %{y:,.0f}"
        "<extra></extra>"
    )
    return tooltip


def get_aggregated_hover_template():
    '''
        Sets the template for aggregated hover tooltips.

        Used when multiple games are grouped into a single point.

        Displays:
        - Prix
        - Succès estimé
        - Nombre de jeux
        - Liste des jeux

        returns:
            The content of the tooltip
    '''
    tooltip = (
        "<b>Prix :</b> %{x}$<br>"
        "<b>Succès commercial estimé :</b> %{y:,.0f}<br>"
        "<b>Nombre de jeux :</b> %{customdata[0]}<br><br>"
        "<b>Jeux :</b><br>"
        "%{customdata[1]}"
        "<extra></extra>"
    )
    return tooltip


def format_game_list_hover(game_names, limit=10):
    '''
        Formats a list of game names for the hover tooltip.

        Limits the number of displayed games and adds a summary
        if there are remaining hidden games.

        params:
            game_names: list of game names
            limit: maximum number of games to display

        returns:
            HTML formatted string for tooltip
    '''
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