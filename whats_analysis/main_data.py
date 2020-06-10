#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 10:01:20 2020

@author: mauricio
"""

#%% Initialize
print("Starting...")

import _pickle as pk

import set_information as i
i.set_info()


#%% Load	
print("Loading data...")

#Load saved result	
with open(i.path+"/results/classified_dictionary.obj", "rb") as r:
	classified = pk.load(r)
	
	
#%% Create dataframes
print("Creating dataframes")

from create_dataframes import full_dataframe

# Return single full dataframe
chats_df = full_dataframe(dictionary = classified,
		features = ['time','raw_size','chars','size_in_words','type','chat',
        'who_sent', 'seq','shape','subtype','emotes','words','mine'],
		convert_to = {"seq": "category"})


#%% Save dataframes
print("Saving dataframes")

chats_df.to_csv("./results/full_dataframe.csv", index = False)

print("Done")