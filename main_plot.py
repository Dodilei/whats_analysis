#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:04:44 2020

@author: mauricio
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import organize as org


app = dash.Dash(__name__, external_stylesheets = ['$PROJECTS/whats_analysis/stylesheet.css'])


graph_area1 = [
	dcc.Dropdown(
		options=[
			{"label": "Chat1", "value": 1},
			{"label": "Chat2", "value": 2},
			{"label": "Chat3", "value": 3},
			{"label": "Chat4", "value": 4},
			],
		value=[1,2],
		multi=True)
	]

graph_area2 = [
	
	html.Div(className = "column", children=[
		
		dcc.RadioItems(id = "rd1",
			options=[
				{"label": "Chat1", "value": 1},
				{"label": "Chat2", "value": 2},
				{"label": "Chat3", "value": 3},
				{"label": "Chat4", "value": 4},
				],
			value = 1
		)]
	),

	html.Div(className = "column", children=[
		
		dcc.RadioItems(id = "rd2",
			options=[
				{"label": "Chat1", "value": 1},
				{"label": "Chat2", "value": 2},
				{"label": "Chat3", "value": 3},
				{"label": "Chat4", "value": 4},
				],
			value = 2
		)]
	)
]


app.layout = html.Div(id="main", children=[
	
	html.H1(children="Title", style={
		"textAlign": "center"
		
		}),
	
	html.Label("Graph type"),
	
	dcc.Dropdown(
		id = "graph_choice",
		options=[
			{"label": "Absolute", "value": "ABS"},
			{"label": "Duality", "value": "DUA"},
			{"label": "Percent", "value": "PER"}
			],
		value = "ABS"),
	
	html.Div(id="main_graph_area", className = "row")
	
	])

@app.callback(
	Output(component_id="main_graph_area", component_property="children"),
	[Input(component_id="graph_choice", component_property="value")]
	)
def update_main_area(choice):
	
	if choice == "ABS":
		return graph_area1
	elif choice == "DUA":
		return graph_area2
	else:
		return None


if __name__ == '__main__':
    app.run_server(debug=True)