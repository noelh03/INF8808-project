
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
from dash import Output, Input

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

viz1_scatter_fig = viz1_scatter.create_figure(data)
viz2_box_fig = viz2_box.create_figure(data)
viz3_line_fig = viz3_line.create_figure(data)
viz4_bubble_fig = viz4_bubble.create_figure(data)
viz5_dot_fig = viz5_dot.create_figure(data)
viz6_violin_fig = viz6_violin.create_figure(data)

@app.callback(
    Output("sidebar", "className"),
    Input("toggle-btn", "n_clicks")
)
def toggle_sidebar(n):
    if n and n % 2 == 1:
        return "sidebar open"
    return "sidebar"

app.layout = html.Div(className='content', children=[
    html.Button("☰", id="toggle-btn", n_clicks=0, className="toggle-btn"),

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

        html.Div(id="scatter", className='viz-block', children=[
            html.H3("Scatter Plot"),
            dcc.Graph(className='graph', figure=viz1_scatter_fig, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            ))
        ]),

        html.Div(id="box", className='viz-block', children=[
            html.H3("Box Plot"),
            dcc.Graph(className='graph', figure=viz2_box_fig, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            ))
        ]),

        html.Div(id="line", className='viz-block', children=[
            html.H3("Line Chart"),
            dcc.Graph(className='graph', figure=viz3_line_fig, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            ))
        ]),

        html.Div(id="bubble", className='viz-block', children=[
            html.H3("Bubble Chart"),
            dcc.Graph(className='graph', figure=viz4_bubble_fig, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            ))
        ]),

        html.Div(id="dot", className='viz-block', children=[
            html.H3("Dot Plot"),
            dcc.Graph(className='graph', figure=viz5_dot_fig, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            ))
        ]),

        html.Div(id="violin", className='viz-block', children=[
            html.H3("Violin Plot"),
            dcc.Graph(className='graph', figure=viz6_violin_fig, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            ))
        ]),
    ])
])
