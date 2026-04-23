'''
This file contains the code for the scatter plot.
It includes the function to generate the plot, as well as helper
functions to aggregate overlapping points and update the plot styling.
'''

import math
import plotly.express as px

from .hover_template import (
    get_aggregated_hover_template,
    format_game_list_hover
)
from utils.constants import (
    COL_PRICE,
    COL_ESTIMATED_OWNERS_AVG,
    COL_TYPE,
    COL_NAME
)


def aggregate_overlapping_points(df, color_mode):
    """
        Group games sharing the exact same coordinates.

        Games are grouped by price and estimated owners average.
        Depending on the selected color mode, an additional grouping
        column is added.

        Args:
            df (pd.DataFrame): The input dataframe containing the game data.
            color_mode (str): Grouping mode used for color encoding.
                Possible values:
                - "single"
                - "type"
                - "success"

        Returns:
            pd.DataFrame: The aggregated dataframe with hover content
            and bubble sizes.
    """
    group_cols = [COL_PRICE, COL_ESTIMATED_OWNERS_AVG]

    if color_mode == "type":
        group_cols.append(COL_TYPE)

    if color_mode == "success":
        group_cols.append("Catégorie succès")

    aggregated = (
        df.groupby(group_cols, dropna=False)
        .agg(
            game_count=(COL_NAME, "size"),
            game_names=(COL_NAME, lambda names: list(names)),
            types_list=(COL_TYPE, lambda types: sorted(set(types))),
        )
        .reset_index()
    )

    aggregated["hover_names"] = aggregated["game_names"].apply(
        lambda names: format_game_list_hover(names, limit=10)
    )

    aggregated["bubble_size"] = aggregated["game_count"].apply(
        lambda n: 5 if n <= 1 else min(5 + math.sqrt(n) * 1.6, 18)
    )

    return aggregated


def generate_plot(df, price_range=(0, 100), question_idx=0):
    """
        Generate the scatter plot.

        Args:
            df (pd.DataFrame): The dataframe to display.
            price_range (tuple): Minimum and maximum price used for filtering.
            question_idx (int): Index of the analytical question to display.

        Returns:
            plotly.graph_objects.Figure: The generated figure.
    """
    required_columns = [COL_PRICE, COL_ESTIMATED_OWNERS_AVG, COL_TYPE, COL_NAME]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing}")

    min_price, max_price = price_range
    filtered_df = df[
        (df[COL_PRICE] >= min_price) & (df[COL_PRICE] <= max_price)
    ].copy()

    visible_max = max_price if max_price > 0 else 1

    if visible_max <= 120:
        x_dtick = 20
    elif visible_max <= 300:
        x_dtick = 50
    else:
        x_dtick = 100

    padding = visible_max * 0.03 if visible_max > 0 else 1

    if question_idx == 0:
        fig = generate_general_success_plot(filtered_df)

    elif question_idx == 1:
        fig = generate_type_comparison_plot(filtered_df)

    elif question_idx == 2:
        fig = generate_success_concentration_plot(filtered_df)

    else:
        fig = generate_type_comparison_plot(filtered_df)

    fig = update_layout(fig, question_idx)
    fig = update_axes(fig, min_price, max_price, padding, x_dtick)

    return fig


def generate_general_success_plot(df):
    """
        Generate the general price versus success view.

        Uses a single color and hides the legend.

        Args:
            df (pd.DataFrame): The filtered dataframe.

        Returns:
            plotly.graph_objects.Figure: The generated figure.
    """
    plot_df = aggregate_overlapping_points(df, color_mode="single")

    fig = px.scatter(
        plot_df,
        x=COL_PRICE,
        y=COL_ESTIMATED_OWNERS_AVG,
        size="bubble_size",
        hover_name=None,
        log_y=True,
        opacity=0.72,
        custom_data=["game_count", "hover_names"],
        color_discrete_sequence=["#6678E8"],
    )

    fig.update_traces(
        marker=dict(line=dict(width=0)),
        hovertemplate=get_aggregated_hover_template(),
    )

    fig.update_layout(showlegend=False)

    return fig


def generate_type_comparison_plot(df):
    """
        Generate the free versus paid games view.

        Colors points according to the game type.

        Args:
            df (pd.DataFrame): The filtered dataframe.

        Returns:
            plotly.graph_objects.Figure: The generated figure.
    """
    plot_df = aggregate_overlapping_points(df, color_mode="type")

    fig = px.scatter(
        plot_df,
        x=COL_PRICE,
        y=COL_ESTIMATED_OWNERS_AVG,
        color=COL_TYPE,
        size="bubble_size",
        hover_name=None,
        log_y=True,
        opacity=0.72,
        custom_data=["game_count", "hover_names"],
        color_discrete_map={
            "Payant": "#6678E8",
            "Gratuit": "#D98A6C",
        },
    )

    fig.update_traces(
        marker=dict(line=dict(width=0)),
        hovertemplate=get_aggregated_hover_template(),
    )

    return fig


def generate_success_concentration_plot(df):
    """
        Generate the success concentration view.

        Separates top success games from other games and adds
        a horizontal reference line.

        Args:
            df (pd.DataFrame): The filtered dataframe.

        Returns:
            plotly.graph_objects.Figure: The generated figure.
    """
    plot_df = df.copy()

    plot_df["Catégorie succès"] = plot_df[COL_ESTIMATED_OWNERS_AVG].apply(
        lambda x: "Top succès" if x >= 1_000_000 else "Autres jeux"
    )

    plot_df = aggregate_overlapping_points(plot_df, color_mode="success")

    fig = px.scatter(
        plot_df,
        x=COL_PRICE,
        y=COL_ESTIMATED_OWNERS_AVG,
        color="Catégorie succès",
        size="bubble_size",
        hover_name=None,
        log_y=True,
        opacity=0.72,
        custom_data=["game_count", "hover_names"],
        color_discrete_map={
            "Autres jeux": "#C7D2E3",
            "Top succès": "#6678E8",
        },
    )

    fig.update_traces(
        marker=dict(line=dict(width=0)),
        hovertemplate=get_aggregated_hover_template(),
    )

    fig.add_hline(
        y=1_000_000,
        line_width=2,
        line_dash="dot",
        line_color="#D64545",
        annotation_text="Zone des plus gros succès",
        annotation_position="top left",
    )

    return fig


def update_layout(fig, question_idx):
    """
        Update the figure layout with styling and formatting.

        Args:
            fig: The figure to update.
            question_idx (int): Index of the analytical question displayed.

        Returns:
            The updated figure.
    """
    legend_title = (
        "Concentration du succès"
        if question_idx == 2
        else "Type de jeu"
    )

    fig.update_layout(
        autosize=True,
        uirevision="viz1-scatter",
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F7FB",
        margin=dict(l=58, r=12, t=20, b=52),
        font=dict(
            family="Inter, Arial, sans-serif",
            size=13,
            color="#2E4057",
        ),
        legend=dict(
            title_text=legend_title,
            orientation="v",
            y=0.98,
            x=0.98,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.78)",
            bordercolor="#D9E2F2",
            borderwidth=1,
            font=dict(size=12, color="#2E4057"),
            title_font=dict(size=13, color="#2E4057"),
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D9E2F2",
            font=dict(
                family="Inter, Arial, sans-serif",
                size=12,
                color="#2E4057",
            ),
        ),
    )

    return fig


def update_axes(fig, min_price, max_price, padding, x_dtick):
    """
        Update the axes labels and styling.

        Args:
            fig: The figure to update.
            min_price (float): Minimum visible price.
            max_price (float): Maximum visible price.
            padding (float): Padding added around the x-axis range.
            x_dtick (int): Tick interval for the x-axis.

        Returns:
            The updated figure.
    """
    fig.update_xaxes(
        title_text="Prix ($)",
        range=[min_price - padding, max_price + padding],
        tickmode="linear",
        dtick=x_dtick,
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    fig.update_yaxes(
        title_text="Succès commercial estimé",
        range=[3.8, 8.3],
        tickmode="array",
        tickvals=[1e4, 1e5, 1e6, 1e7, 1e8],
        ticktext=["10k", "100k", "1M", "10M", "100M"],
        showgrid=True,
        gridcolor="#DCE6F2",
        gridwidth=1,
        zeroline=False,
        showline=False,
        title_font=dict(size=16, color="#2E4057"),
        tickfont=dict(size=12, color="#506784"),
    )

    return fig