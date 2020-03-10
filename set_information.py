#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 14:08:02 2020

@author: mauricio
"""

from chat import Chat
import _pickle as pk

# If wanted, set the information needed with this function
def set_information(**mapping):
  global owner, path, _custom_trash_input
  if mapping == {}:

    inp = input("Do you want to set information?([y]/n)\n")
    while inp != "n":
      info = input("info name: ")
      mapping[info] = input("value: ")
      inp = input("Next?([y]/n)\n")

  for info in mapping.keys():
    if info == "owner": owner = mapping[info]
    elif info == "header_pattern": _header_pattern = mapping[info]
    elif info == "path": path = mapping[info]
    elif info == "custom_trash_input": _custom_trash_input = mapping[info]
    
  with open("./resources/user_data.obj", "wb") as r:
    pk.dump(mapping, r)

def reset_info():
  with open("./resources/user_data.obj", "wb") as r:
    pk.dump({}, r)

# Set the owner's name (regex and default)
owner = ""
with open("./resources/user_data.obj", "rb") as r:
  if owner == "": set_information(**pk.load(r))
_myname_regex = owner.replace(".", "\\.")

# Set a template to identify message starts
_header_pattern = "\n\d{1,2}/\d{1,2}/\d{1,2}, \d{2}:\d{2} - "

# Set the path to the project
try:
  path
except NameError:
  path = r"."

# Set the paths for darklist and whitelist
_darklist = path+"/resources/darklist.txt"
_whitelist = path+"/resources/whitelist.txt"

# Creates a set with relevant unicode symbols
symbols_range = set(pk.load(open(path+"/resources/unicode symbols/emoji_list.obj", "rb")))

# Set to True if you want to analyse large messages manually
try:
  _custom_trash_input
except NameError:
  _custom_trash_input = True

# List to keep track of large messages
Large = []
# List to keep track of unidentified messages
Unidentified = []

# Set Chat class variables
Chat._header_pattern = _header_pattern
Chat.me_regex = _myname_regex
Chat.owner = owner
Chat._custom_trash_input = _custom_trash_input
Chat._Large(Large)
Chat._Unidentified(Unidentified)
Chat.symbols_range(symbols_range)
Chat._lists(_whitelist, _darklist)
   
