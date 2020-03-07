#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 13:56:29 2020

@author: mauricio
"""

import pandas as pd

def get_range(chat, wreturn = None):
    # Return the range of a chat (i.e. timespan)
    
    time = []
    for m in chat.messages:
        time.append(m.time)
    first = min(time)
    last = max(time)
    
    if wreturn == None:
        return (first, last)
    elif wreturn == "duration":
        return last-first
    elif wreturn == "all":
        return (first, last, last-first)

# not being used
def analyse_chat(tup):

    from chat import Chat

    return {tup[0]:Chat(*tup)}


def get_chats(dataframe, chat_name, return_as_dict = False):
    
    if type(chat_name) == str:
        
        if return_as_dict:
            new_df = dataframe.loc[dataframe.chat == chat_name].copy()
            new_df.reset_index(drop = True, inplace = True)
            return {chat_name: new_df}
        else:
            new_df = dataframe.loc[dataframe.chat == chat_name].copy()
            new_df.reset_index(drop = True, inplace = True)
            return new_df
        
    elif return_as_dict:
        chats_dict = {}
        for name in chat_name:
            new_df = dataframe.loc[dataframe.chat == name].copy()
            new_df.reset_index(drop = True, inplace = True)
            chats_dict[name] = new_df
        return chats_dict
    
    else:
        new_df = dataframe.loc[dataframe.chat in chat_name].copy()
        new_df.reset_index(drop = True, inplace = True)
        return new_df

def get_columns(dataframe, features):
    
    if type(features[0]) == list:
        
        lst_dataframes = []
        for lst_features in features:
            lst_dataframes.append(dataframe[lst_features].copy())
        return lst_dataframes
    
    elif type(features[0]) == str:
        
        return dataframe[features].copy()
    
    elif type(features) == str:
        
        return dataframe[features].copy()
    
    else:
        raise TypeError("'features' argument must be: str, list of strings or list of lists")


def get_types(dataframe, types, remove = False, return_as_dict = False):
    
    if type(types) == str:
        if remove:
            new_df = dataframe.loc[dataframe.type != types].copy()
            new_df.reset_index(drop = True, inplace = True)
            return new_df
        else:
            new_df = dataframe.loc[dataframe.type == types].copy()
            new_df.reset_index(drop = True, inplace = True)
            return new_df
    
    elif return_as_dict:
        
        if remove: raise TypeError("If 'remove' is set to True, 'return_as_dict' must be False")
        
        types_dict = {}
        for typ in types:
            new_df = dataframe.loc[dataframe.type == typ].copy()
            new_df.reset_index(drop = True, inplace = True)
            types_dict[typ] = new_df
        return types_dict
    
    else:
        if remove:
            new_df = dataframe.loc[dataframe.type not in types].copy()
            new_df.reset_index(drop = True, inplace = True)
            return new_df
        else:
            new_df = dataframe.loc[dataframe.type in types].copy()
            new_df.reset_index(drop = True, inplace = True)
            return new_df


def full_organize(dataframe, features, chats, types, remove = False, return_as_dict = (False, False)):
    
    if type(return_as_dict) not in (list, tuple, dict): raise TypeError("'return_as_dict' must be a container")
    if type(return_as_dict) == dict: 
        return_as_dict = (return_as_dict["chat"], return_as_dict["type"])
    
    data = get_chats(dataframe, chats, return_as_dict[0])
    
    if return_as_dict[0]:
        
        for name in data:
            data[name] = get_types(data[name], types, remove, return_as_dict[1])
            if return_as_dict[1]:
                for typ in data[name]:
                    data[name][typ] = get_columns(data[name][typ], features)
            else:
                data[name] = get_columns(data[name], features)
        return data
    
    else:
        
        data = get_types(data, types, remove, return_as_dict[1])
        if return_as_dict[1]:
            for typ in data:
                data[typ] = get_columns(data[typ], features)
            return data
        else:
            data = get_columns(data, features)
            return data

      
def make_time_bins(dataframe, bin_size = (1, "days"), combine = True,
                   features = "all", method_scalar = "sum", method_cat = "add",
                   keep_size = True, keep_orig_time = True,
                   bin_as_label = False, label = "left"):
    
    dataframe = dataframe.copy()
    
    labels = {"left": lambda x: x.left, "right": lambda x: x.right,
              "mid": lambda x: x.mid}
    bin_label = labels[label]
    
    cat = ["object", "category", "bool"]
    
    resolution = {"minutes":"T", "hours":"H", "days":"D", "weeks":"W",
                  "months":"M", "years":"Y"}
    freq = resolution[bin_size[1]]
    
    first = dataframe["time"].min().floor(freq)
    last = dataframe["time"].max().ceil(freq)
    
    d_range = pd.date_range(start = first, end = last, freq = bin_size[0]+freq)
    dataframe["bin"] = pd.cut(dataframe["time"], d_range, right = False)
    
    if not combine:
        
        if bin_as_label:
            new_series = dataframe["bin"].apply(bin_label)
        else:
            new_series = dataframe["bin"]
        
        if keep_orig_time:
            
            dataframe["bin"] = new_series
            return dataframe
        
        else:
            
            dataframe["time"] = new_series
            dataframe.drop("bin", axis = 1, inplace = True)
            return dataframe
    
    else:
            
        group = dataframe.groupby(by = dataframe["bin"].astype("object"))
        
        columns = dataframe.columns.values.tolist()
        new_df = pd.Dataframe(columns = columns)
        
        columns.remove("bin")
        columns.remove("time")
        
        if keep_size:
            if bin_as_label:
                new_series = dataframe["bin"].apply(bin_label)
            else:
                new_series = dataframe["bin"]
            
            if keep_orig_time:   
                new_df["time"] = dataframe["time"]
                new_df["bin"] = new_series
    
            else:
                new_df["time"] = new_series
                new_df.drop("bin", axis = 1, inplace = True)
               
        else:
            new_df.drop("bin", axis = 1, inplace = True)
            new_df["time"] = pd.Series(group["bin"].apply(lambda x: None).index)
            
        for column in columns:
            if column in features or features == "all":
                
                grouped = group[column]
                if dataframe[column].dtype.name in cat:
                    if keep_size:
                        group_map = grouped.apply(lambda x: x.values.tolist())
                        new_series = dataframe["bin"].map(group_map)
                        new_df[column] = new_series
                    else:
                        new_series = grouped.apply(lambda x: x.values.tolist())
                        new_series.reset_index(drop = True, inplace = True)
                        new_df[column] = new_series
                        
                else:
                    if keep_size:
                        group_map = grouped.sum()
                        new_series = dataframe["bin"].map(group_map)
                        new_df[column] = new_series
                    else:
                        new_series = grouped.sum()
                        new_series.reset_index(drop = True, inplace = True)
                        new_df[column] = new_series
            
            else:
                if keep_size:
                    new_df[column] = dataframe[column]
                else:
                    raise TypeError("If 'keep_size' is False, features must include all")
                
        return new_df

    
