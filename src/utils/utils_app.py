import copy
from dash import html
import os
import pandas as pd

from viz3_line.preprocess import MAIN_GENRES as VIZ3_MAIN_GENRES


def load_csv_with_fallback(preferred_path, fallback_path):
    if os.path.exists(preferred_path):
        return pd.read_csv(preferred_path)
    return pd.read_csv(fallback_path)


def _apply_restyle_patch_to_figure(fig_dict, restyle_data):
    """
    Merge a Plotly restyle event into a figure dict (legend clicks / double-clicks).
    restyle_data: [patch_dict, trace_indices] as emitted by dcc.Graph restyleData.
    """
    if not fig_dict or not restyle_data or len(restyle_data) < 2:
        return fig_dict
    patch, indices = restyle_data[0], restyle_data[1]
    if patch is None or indices is None:
        return fig_dict

    fig = copy.deepcopy(fig_dict)
    n = len(fig.get("data", []))
    if n == 0:
        return fig

    if isinstance(indices, int):
        indices = [indices]
    else:
        indices = list(indices)

    for key, val in patch.items():
        if key == "visible" and isinstance(val, list) and len(val) == n:
            for i in range(n):
                fig["data"][i][key] = val[i]
            continue

        for i, idx in enumerate(indices):
            if idx < 0 or idx >= n:
                continue
            if isinstance(val, list):
                if len(val) == len(indices):
                    fig["data"][idx][key] = val[i]
                elif len(val) == 1:
                    fig["data"][idx][key] = val[0]
                else:
                    fig["data"][idx][key] = val[i] if i < len(val) else val[-1]
            else:
                fig["data"][idx][key] = val
    return fig


def _figure_to_viz3_checklist_values(fig_dict):
    """Derive checklist values from trace visibility (matches legend state)."""

    def trace_on_plot(tr):
        v = tr.get("visible")
        if v is None or v is True:
            return True
        if v in (False, "legendonly"):
            return False
        return True

    visible_main = set()
    others_on = False
    for tr in fig_dict.get("data", []):
        if not trace_on_plot(tr):
            continue
        name = tr.get("name")
        if name == "Others":
            others_on = True
        elif name in VIZ3_MAIN_GENRES:
            visible_main.add(name)

    ordered = [g for g in VIZ3_MAIN_GENRES if g in visible_main]
    if others_on:
        ordered.append("Others")
    return ordered


def make_section(section_id, title, description, viz_layout, prev_href, next_href, info_content=None):
    """
    Build a full story section with:
    - intro block (title, "?" info toggle, description)
    - section body: viz card on the left, side-nav arrows on the right

    info_content: optional Dash children for the "?" info panel.
                  Defaults to a placeholder message.
    """
    return html.Section(
        id=section_id,
        className="story-section",
        children=[
            html.Div(
                className="section-intro",
                children=[
                    html.Div(
                        className="section-title-row",
                        children=[
                            html.Div(children=[
                                html.H2(title, className="section-title"),
                            ]),
                        ],
                    ),
                    html.P(description, className="section-description"),
                ],
            ),
            html.Div(
                className="section-body",
                children=[
                    html.Div(viz_layout, className="viz-card"),
                    (
                        html.Div(
                            info_content,
                            className="section-inline-info",
                        )
                        if info_content is not None
                        else None
                    ),
                    html.Div(
                        className="section-side-nav",
                        children=[
                            html.A(
                                href=prev_href,
                                className="arrow-btn arrow-up",
                                title="Section précédente",
                                children=html.Span(className="arrow-chevron chevron-up"),
                            ),
                            html.A(
                                href=next_href,
                                className="arrow-btn arrow-down",
                                title="Section suivante",
                                children=html.Span(className="arrow-chevron chevron-down"),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

