
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas (original author)
            Team 11 (adapted for the project)
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for the project.
'''

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
from dash import Output, Input, State, callback_context

from viz1_scatter import viz1_scatter
from viz2_box import viz2_box
from viz3_line import viz3_line
from viz4_bubble import viz4_bubble
from viz5_dot import viz5_dot
from viz6_violin import viz6_violin

app = dash.Dash(__name__)
app.title = 'Project | INF8808'

with open('../src/assets/data/games.csv', 'r', encoding='utf-8') as data_file:
    data = pd.read_csv(data_file)

viz1_scatter_layout = viz1_scatter.create_layout(data)
viz2_box_layout = viz2_box.create_layout(data)
viz3_line_layout = viz3_line.create_layout(data)
viz4_bubble_layout = viz4_bubble.create_layout(data)
viz5_dot_layout = viz5_dot.create_layout(data)
viz6_violin_layout = viz6_violin.create_layout(data)


app.layout = html.Div(id="content", className='content', children=[
    html.Button("☰", id="toggle-btn", n_clicks=0, className="toggle-btn"),
    
    html.Div(id="overlay", className="overlay"),

    html.Div(id="sidebar", className="sidebar", children=[
        html.H3("Navigation"),
        html.A("Scatter Plot", href="#scatter"),
        html.A("Box Plot", href="#box"),
        html.A("Line Chart", href="#line"),
        html.A("Bubble Chart", href="#bubble"),
        html.A("Dot Plot", href="#dot"),
        html.A("Violin Plot", href="#violin"),
    ]),
    
    html.Header(children=[
        html.H1("Project's Title 1"),
        html.H2("Project's Title 2"),
        html.P("Project's description")
    ]),

    html.Main(className='viz-container', children=[
        viz1_scatter_layout,
        viz2_box_layout,
        viz3_line_layout,
        viz4_bubble_layout,
        viz5_dot_layout,
        viz6_violin_layout
    ])
])


@app.callback(
    Output("sidebar", "className"),
    Output("overlay", "className"),
    Output("content", "className"),
    Input("toggle-btn", "n_clicks"),
    Input("overlay", "n_clicks"),
    State("sidebar", "className"),
)
def toggle_sidebar(btn, overlay_click, sidebar_class):
    ctx = callback_context
    if not ctx.triggered:
        return "sidebar", "overlay", "content"

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger == "overlay":
        return "sidebar", "overlay", "content"
    if trigger == "toggle-btn":
        if "open" in sidebar_class:
            return "sidebar", "overlay", "content"
        else:
            return "sidebar open", "overlay open", "content shift"

    return "sidebar", "overlay", "content"