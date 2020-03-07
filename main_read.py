# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 19:31:35 2019

@author: Dodilei
"""

#%% Import chat files

print("\n\nStarting...")

import os
import _pickle as pk

# Imports and sets all needed information (see set_information.py)
import set_information as i

print("Importing Files")
# Import chats and it's names

# Creates a list with tupples in the shape (name, text)
files = []
for file in os.listdir("./Chats"):
	with open("./Chats/%s" % (file), encoding="utf-8") as file_obj:
		files.append((file[19:-4], file_obj.read()))

#%% Classify chats and messages

print("Reading chats\n\n")
from chat import Chat

# Classify imported chats and messages
# Creates a dictionary as {Name: Chat class instance}
classified = {file[0]:Chat(*file) for file in files}


# Print large message counter
print("\n\r", len(i.Large), " large messages")

# Create files to store and manually analyse large messages
from large import large_export

large_export(i.path, i.Large)


#%% Save
print("\nSaving results...")

# Save result
with open("./results/classified_dictionary.obj", "wb") as r:
	pk.dump(classified, r)

print("Done")

