#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:36:27 2020

@author: mauricio
"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output


def ga_absolute_default(chat_options, id):
	return [
		
		html.Div(children=[
			
			dcc.Dropdown(id = id,
				className = "contrast",
				options=chat_options,
				value=[0,1],
				multi=True)
		]),
		
		html.H5(
			chat_options[0]["label"] + " and " + chat_options[1]["label"],
			id = id+"_label")
	]

def ga_relative_limited(chat_options, id):
	return [
		
		html.Div(className = "row", children=[
		
			html.Div(className = "column", children=[
				
				dcc.Dropdown(id = id,
					className = "contrast",
					options=chat_options,
					value=0
					)]
			),
		
			html.Div(className = "column", children=[
				
				dcc.Dropdown(id = id+"2",
					className = "contrast",
					options=chat_options,
					value=1
					)]
			)
		]),
		
		html.H5(
			chat_options[0]["label"] + " and " + chat_options[1]["label"],
			id = id+"_label")
	]

def ga_relative_default(chat_options, id):
	return [
		
		html.Div(children=[
			
			dcc.Dropdown(id = id,
				className = "contrast",
				options=chat_options,
				value=[0,1],
				multi=True),
			
			html.H5(
				chat_options[0]["label"] + " and " + chat_options[1]["label"],
				id = id+"_label")
		])
	]

#%%

ids = {
	   "AD": ga_absolute_default,
	   "RL": ga_relative_limited,
	   "RD": ga_relative_default
	   }

def graph_area(ga, chat_options, id = "graph_chats_choice"):
	return ids[ga](chat_options, id)