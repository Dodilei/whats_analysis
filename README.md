# whats_analysis
Read and analyse Whatsapp chats

## 0. Prerequisites

All chat .txt files must be placed inside the [`Chat`](./Chat/ "Chat folder") folder (to get them, use the "export chat" option from whatsapp)

Some manual arrangements can improve code functionality and the readability of the data display:
- Place an empty newline in the beginning and end of each chat (if it doesn't exist yet)
- Merge chats with the same person (especially when someone changes their phone number, don't forget to update all the names inside de text file)
- Use clean, readable names (if a change is made, both the file name and all the entries in the text must be updated)

- Do not include chats with less than two messages (why would you??)
- When exporting the chats, do not export media (it's not supported, yet)

When the code starts, it'll ask you for information. In the default environment, the only information needed is your name.

Write as follows:
>\> info name: owner

>\> value: YOUR_NAME

Your name must be written exactly like it is in your whatsapp account. To be certain, check how it is displayed inside the chat txt files.

obs: you can delete all `empty.txt` files, they are there just to assure the folders with them will be there too.

## 1. Import, read and process chats

The first file to run is `main_read.py`.
This will open all chat files, get their raw text and name, and store them in a list.
This list is then used to create a dictionary, which maps the names to newly created `Chat` objects.

**Chat objects** (from the Chat class) are created with only a name and raw text. The class handles the message recognition and creation of Message objects.

**Message objects** are created with a header and raw text (from a single message), the class itself handles message classification and gets other relevant information.

After all chats are processed, the dictionary is saved as a pickle object for further use.

As of now, the code collects the following information:

  For Chat objects:
  - Owner's name
  - Chat name (person's name)
  - Chat's raw text (full text)
  - All it's Message objects
  - Start, end and duration
  - Size (in messages)
  
  For Message objects:
  - Header
  - Raw text
  - Parent chat
  - Raw size (chars)
  - Timestamp
  - Sequence number
  - Who sent it
  - Shape (text/singular)
  - Type
  - Subtype (if it exists)
  - Relative size*
  - Emoji count
  - Word count and list (if default text)
  

## 2. Collect and store data

The `main_data.py` file will get the data processed by `main_read.py` and organize it in a `Pandas` dataframe with all desired features.

In section of the code, the pickle object with the chat's classification will be loaded and feeded into a function.

This function (`full_dataframe()`, defined at `create_dataframes.py`) uses the methods defined in the `Chat` class to collect all the entries for each relevant feature (as listed above) as an array. Then, with `Pandas`, a dataframe is constructed with all the information. Each entry on the dataframe is a message from your chats, all chats are stored in a single datafame.

The program then saves the dataframe to a csv file.


## 3. Organize data

The `organize.py` code provides some useful and flexible methods to adapt and reshape the full chat's dataframe.

The methods and their uses are listed below:



## 3. Data display

Work in progress.


______________________________________________________________________________

_documentation will be created in the future_

_visualizing the data is the last part of the project and currently being improved_

*group chats are not currently supported*
