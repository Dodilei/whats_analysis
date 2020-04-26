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

from plotting_resources import graph_area, GA_Absolute_Default, GA_Relative_Limited

dataframe = pd.read_csv("./results/full_dataframe.csv", parse_dates = ["time"])

data = org.full_organize(dataframe,
                         ["time", "raw_size", "type",
                          "who_sent", "emotes"],
                         "all",
                         "trash", remove = True,
                         return_as_dict = {"chat": True, "type": False}
                         )

names = data.keys()
chat_options = [{"label": name, "value": i} for i, name in enumerate(names)]

#%%

app = dash.Dash(__name__, suppress_callback_exceptions = True)

app.layout = html.Div(id="main", children=[

	html.H2(children="Whats Analysis", style={
		"textAlign": "center"
		
		}),
	
	html.Div(
		style = {
			"paddingBottom": "30px"
			},
		id = "graph_choice_area",
		children=[
		
		html.H4("Graph type", style = {"marginBlockEnd": "5px"}),
		
		dcc.Dropdown(
			className = "contrast",
			id = "graph_type_choice_drop",
			options=[
				{"label": "Absolute", "value": "ABS"},
				{"label": "Duality", "value": "DUA"},
				{"label": "Percent", "value": "PER"}
				],
			value = "ABS"),
		]),
	
	html.Div(id="main_graph_area", children=[
		*graph_area("RD", chat_options)
		]),
	
	html.H3(id = "testing")
	])

GA = GA_Absolute_Default(chat_options)

@app.callback(
	Output(component_id="main_graph_area", component_property="children"),
	[Input(component_id="graph_type_choice_drop", component_property="value")]
	)
def update_main_area(choice):
	
	if choice == "ABS":
		GA = GA_Absolute_Default(chat_options)
		return GA.component()
	elif choice == "DUA":
		GA = GA_Relative_Limited(chat_options)
		return GA.component() #wrong
	elif choice == "PER":
		return graph_area("RD", chat_options)
	else:
		return None


@app.callback(*GA.callback_parameters())
def call_(inp):
	return GA.callback_func(inp)
	
if __name__ == '__main__':
    app.run_server(debug=True)