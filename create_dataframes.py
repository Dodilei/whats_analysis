#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 19:15:25 2020

@author: mauricio
"""

import pandas as pd

def full_dataframe(dictionary, features, convert_to = {}):
    # Create a dataframe with ALL messages in "dictionary"'s chats and include
    # all features listed in "features"
    # If a feature is included in "convert_to", the method will convert it's
    # entries to the datatype mapped
    
    # Create empty dataframe with as many rows are necessary
    frame = pd.DataFrame(index = range(sum([dictionary[chat].size for chat in dictionary])))

    # Created sorted list with chats to keep dataframe integrity
    sorted_chats = sorted(dictionary.keys())

    for feature in features:
        
        all_rows = pd.Series()
        
        # For each chat, append to all_rows and array containing
        # the feature's entries for each message
        # the Chat class returns these arrays using the __getiterm__ method
        # (see chat.py)
        for chat in sorted_chats:
            series = pd.Series(dictionary[chat][feature])
            all_rows = all_rows.append(series, ignore_index = True)
        
        # If wanted, convert features as asked
        if feature in convert_to.keys():
            all_rows = all_rows.astype(convert_to[feature])
        frame[feature] = all_rows
        
    return frame
    
