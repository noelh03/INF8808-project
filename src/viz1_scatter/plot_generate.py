"""
Visualization generation module for the price vs commercial success scatter plot.

This module:
- filters the dataset according to the selected price range
- creates the Plotly scatter figure
- applies visual styling and layout customization
- integrates logarithmic scaling to better represent skewed ownership data

It focuses exclusively on figure construction logic.
"""

import plotly.express as px
from .hover_template import get_hover_template


COL_PRICE = "Price"
COL_OWNERS = "Estimated owners (average)"
COL_TYPE = "Type de jeu"
COL_NAME = "Name"


def generate_plot(df, max_price=100):
    required_columns = [COL_PRICE, COL_OWNERS, COL_TYPE, COL_NAME]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing}")

    filtered_df = df[df[COL_PRICE] <= max_price].copy()

    if max_price <= 120:
        x_dtick = 20
    elif max_price <= 300:
        x_dtick = 50
    else:
        x_dtick = 100

    padding = max_price * 0.03 if max_price > 0 else 1

    fig = px.scatter(
        filtered_df,
        x=COL_PRICE,
        y=COL_OWNERS,
        color=COL_TYPE,
        hover_name=COL_NAME,
        log_y=True,
        opacity=0.62,
        custom_data=[COL_TYPE],
        color_discrete_map={
            "Payant": "#6678E8",
            "Gratuit": "#D98A6C",
        },
    )

    fig.update_traces(
        marker=dict(
            size=5,
            line=dict(width=0),
        ),
        hovertemplate=get_hover_template(),
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F7FB",
        margin=dict(l=72, r=130, t=28, b=62),
        font=dict(
            family="Inter, Arial, sans-serif",
            size=13,
            color="#2E4057",
        ),
        legend=dict(
            title_text="Type de jeu",
            orientation="v",
            y=1,
            x=1.02,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(0,0,0,0)",
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

    fig.update_xaxes(
        title_text="Prix ($)",
        range=[-padding, max_price + padding],
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