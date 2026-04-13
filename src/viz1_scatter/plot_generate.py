import plotly.express as px
from .hover_template import get_hover_template


COL_PRICE = "Price"
COL_OWNERS = "Estimated owners (average)"
COL_TYPE = "Type de jeu"
COL_NAME = "Name"


def generate_plot(df, price_range=(0, 100), question_idx=0):
    required_columns = [COL_PRICE, COL_OWNERS, COL_TYPE, COL_NAME]
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

    # ==========================================================
    # QUESTION 1 : Vue générale prix / succès
    # Une seule couleur, sans légende
    # ==========================================================
    if question_idx == 0:
        fig = px.scatter(
            filtered_df,
            x=COL_PRICE,
            y=COL_OWNERS,
            hover_name=COL_NAME,
            log_y=True,
            opacity=0.72,
            custom_data=[COL_TYPE],
            color_discrete_sequence=["#6678E8"],
        )

        fig.update_traces(
            marker=dict(size=5, line=dict(width=0)),
            hovertemplate=get_hover_template(),
        )

        fig.update_layout(showlegend=False)

    # ==========================================================
    # QUESTION 2 : Gratuit vs Payant
    # ==========================================================
    elif question_idx == 1:
        fig = px.scatter(
            filtered_df,
            x=COL_PRICE,
            y=COL_OWNERS,
            color=COL_TYPE,
            hover_name=COL_NAME,
            log_y=True,
            opacity=0.72,
            custom_data=[COL_TYPE],
            color_discrete_map={
                "Payant": "#6678E8",
                "Gratuit": "#D98A6C",
            },
        )

        fig.update_traces(
            marker=dict(size=5, line=dict(width=0)),
            hovertemplate=get_hover_template(),
        )

    # ==========================================================
    # QUESTION 3 : Concentration du succès
    # ==========================================================
    elif question_idx == 2:
        plot_df = filtered_df.copy()

        plot_df["Catégorie succès"] = plot_df[COL_OWNERS].apply(
            lambda x: "Top succès" if x >= 1_000_000 else "Autres jeux"
        )

        fig = px.scatter(
            plot_df,
            x=COL_PRICE,
            y=COL_OWNERS,
            color="Catégorie succès",
            hover_name=COL_NAME,
            log_y=True,
            opacity=0.72,
            custom_data=[COL_TYPE],
            color_discrete_map={
                "Autres jeux": "#C7D2E3",
                "Top succès": "#6678E8",
            },
        )

        fig.update_traces(
            marker=dict(size=5, line=dict(width=0)),
            hovertemplate=get_hover_template(),
        )

        fig.add_hline(
            y=1_000_000,
            line_width=2,
            line_dash="dot",
            line_color="#D64545",
            annotation_text="Zone des plus gros succès",
            annotation_position="top left",
        )

    # ==========================================================
    # FALLBACK
    # ==========================================================
    else:
        fig = px.scatter(
            filtered_df,
            x=COL_PRICE,
            y=COL_OWNERS,
            color=COL_TYPE,
            hover_name=COL_NAME,
            log_y=True,
            opacity=0.72,
            custom_data=[COL_TYPE],
            color_discrete_map={
                "Payant": "#6678E8",
                "Gratuit": "#D98A6C",
            },
        )

        fig.update_traces(
            marker=dict(size=5, line=dict(width=0)),
            hovertemplate=get_hover_template(),
        )

    # ==========================================================
    # STYLE COMMUN
    # ==========================================================
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
            title_text="Type de jeu" if question_idx != 2 else "Concentration du succès",
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