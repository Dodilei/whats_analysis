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

from plotting_resources import graph_area

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

app = dash.Dash(__name__)

app.layout = html.Div(id="main", children=[
	
	html.Div(id = "hidden", style={"display": "none"}),
	
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
		*graph_area("AD", chat_options)
		]),
	
	html.H3(id = "testing")
	])

@app.callback(
	Output(component_id="main_graph_area", component_property="children"),
	[Input(component_id="graph_type_choice_drop", component_property="value")]
	)
def update_main_area(choice):
	
	if choice == "ABS":
		return graph_area("AD", chat_options)
	elif choice == "DUA":
		return graph_area("RL", chat_options) #wrong
	elif choice == "PER":
		return graph_area("RD", chat_options)
	else:
		return None


#MAKE ONE FOR EACH, i dont care
@app.callback(
	Output(component_id="hidden", component_property="children"),
	[
    Input(component_id="graph_chats_choice", component_property="value")]
	)
def update_graph(chat_choices):

	if type(chat_choices) == int:
		@app.callback(
			Output(component_id="graph_chats_choice_label", component_property="children"),
			[
			 Input(component_id="graph_chats_choice2", component_property="value")
			]
			)
		def att_label2(new_choices, chat_choices = chat_choices):
			
			chat_choices = [chat_choices]+[new_choices]
			
			return str(chat_choices)
	
	else:
		return str(chat_choices)
		
		
if __name__ == '__main__':
    app.run_server(debug=True)