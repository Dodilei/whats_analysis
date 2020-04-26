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


class GA_Absolute_Default(object):

	def __init__(self, chat_options, _id = "graph_chats_choice"):
		
		self.chat_options = chat_options
		self.id = _id + "_AD"
		
	def component(self):
		return [
			
			html.Div(children=[
				
				dcc.Dropdown(id = self.id,
					className = "contrast",
					options=self.chat_options,
					value=[0,1],
					multi=True)
			]),
			
			html.H5(
				self.chat_options[0]["label"] + " and " +
				self.chat_options[1]["label"],
				id = self.id+"_label")
		]
	
	def inputs(self):
		
		return [
			Input(component_id=self.id, component_property="value")
			]
	
	def outputs(self):
		
		return Output(component_id=self.id+"_label", component_property="children")
	
	def callback_parameters(self):
		
		return self.outputs(), self.inputs()
	
	def callback_func(self, inp):
		
		string = ", ".join([self.chat_options[i]["label"] for i in inp[:-1]]) +\
		" and " + self.chat_options[inp[-1]]["label"]
		
		return string


class GA_Relative_Limited(object):

	def __init__(self, chat_options, _id = "graph_chats_choice"):
		
		self.chat_options = chat_options
		self.id = _id + "_RL"
		
	def component(self):
		return [
		
			html.Div(className = "row", children=[
			
				html.Div(className = "column", children=[
					
					dcc.Dropdown(id = self.id,
						className = "contrast",
						options=self.chat_options,
						value=0
						)]
				),
			
				html.Div(className = "column", children=[
					
					dcc.Dropdown(id = self.id+"2",
						className = "contrast",
						options=self.chat_options,
						value=1
						)]
				)
			]),
		
			html.H5(
				self.chat_options[0]["label"] + " and " +
				self.chat_options[1]["label"],
				id = self.id+"_label")
		]
	
	def inputs(self):
		
		return [
			Input(component_id=self.id, component_property="value"),
			Input(component_id=self.id+"2", component_property="value")
			]
	
	def outputs(self):
		
		return Output(component_id=self.id+"_label", component_property="children")
	
	def callback_parameters(self):
		
		return self.outputs(), self.inputs()
	
	def callback_func(self, inp):
		
		string = ", ".join([self.chat_options[i]["label"] for i in inp[:-1]]) +\
		" and " + self.chat_options[inp[-1]]["label"]
		
		return string

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
	   "AD": GA_Absolute_Default,
	   "RL": GA_Relative_Limited,
	   "RD": ga_relative_default
	   }

def graph_area(ga, chat_options, id = "graph_chats_choice"):
	return ids[ga](chat_options, id)