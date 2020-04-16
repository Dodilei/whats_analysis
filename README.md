# whats_analysis
Read and analyse Whatsapp chats

## Prerequisites

All chat .txt files must be placed inside the [`Chat`](./Chats/ "Chat folder") folder (to get them, use the "export chat" option from whatsapp)

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

The first file to run is [`main_read.py`][mr].
This will open all chat files, get their raw text and name, and store them in a list.
This list is then used to create a dictionary, which maps the names to newly created `Chat` objects.

**Chat objects** (from the [Chat class][chat]) are created with only a name and raw text. The class handles the message recognition and creation of Message objects.

**Message objects** (from the [Message class][msg]) are created with a header and raw text (from a single message), the class itself handles message classification and gets other relevant information.

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

The [`main_data.py`][md] file will get the data processed by `main_read.py` and organize it in a _Pandas_ dataframe with all desired features.

In section of the code, the pickle object with the chat's classification will be loaded and feeded into a function.

This function (_full_dataframe()_, defined at [`create_dataframes.py`][cdf]) uses the methods defined in the _Chat class_ to collect all the entries for each relevant feature (as listed above) as an array. Then, with _Pandas_, a dataframe is constructed with all the information. Each entry on the dataframe is a message from your chats, all chats are stored in a single datafame.

The program then saves the dataframe to a csv file.


## 3. Organize data

The [`organize.py`][org] code provides some useful and flexible methods to adapt and reshape the full chat's dataframe.

The methods and their uses are listed below:

##### The `get_chats` method

This method filters the desired chats from the dataframe, returning a new one.

Given a `dataframe`, the function accepts a `chat_name` argument, which can be a string or a list:
+ If *chat_name* is a string, a dataframe with all entries from the single chat whose name the string identifies will be returned.
+ If *chat_name* is a list, the entries from all chats corresponding to the names in the list will be returned. The result can be returned either:
  - as a dictionary mapping the names to dataframes of each chat if `return_as_dict = True`;
  - or a single dataframe like the original one if `return_as_dict = False`.

#### The `get_columns` method

This method filters the desired features (columns) from the dataframe, returning a new one (or more).

Given a `dataframe`, the function accepts a `features` argument, wich can be a string, a list of strings, or a list of lists:
+ If _features_ is a string, the single column corresponding to the string will be returned;
+ If _features_ is a list of strings, a dataframe with only the features identified by the strings will be returned;
+ If _features_ is a list of lists, a dataframe will be returned for each sublist, with the features identified by that sublist.

#### The `get_types` method

This method filters the desired types of messages from the dataframe, returning a new one.

Given a `dataframe`, the function accepts a `types` argument, wich can be a string or a list. In addition, a `remove` argument can be set to _True_, so the _types_ specified will be __removed__ from the dataframe.

+ If _types_ is a string and _remove_ is false, only the entries with the specified type will be in the dataframe returned, otherwise these entries will be removed.

+ If _types_ is a list of strings and _remove_ is false, a dataframe with all the entries whose types are in the _types_ list will be returned. If _remove_ is set to true, these entries will be removed from the resulting dataframe.
  - A *return_as_dict* argument can be set to _True_ so the result will be returned as a dictionary mapping each _type_ to a dataframe wich contains only entries from that type. This is not possible if _remove_ is also _True_.
  
#### The `make_time_bins` method

This method reshapes the dataframe so that the entries are gouped by a new time resolution. This is useful as it provides more flexibility when creating graphs and processing the data.

The default time resolution from WhatsApp is 1 minute.

Given a `dataframe`, the function accepts:

+ A `bin_size` parameter, wich specifies the new time resolution. This argument must be a tuple of two elements. The _second_ element specifies the unit of time, it can be: "minutes", "hours", "days", "weeks", "months" or "years". The _first_ element is a positive integer wich specifies the bin size, using the unit chosen.

+ A `keep_origin_time` paramenter, it chooses whether the dataframe's _Time_ column will be replaced with the new _bin_ feature or both of the features will be present in the new dataframe.

+ A `label` parameter, which chooses the way _bin_ entries will be presented. The choices are: _left_, _mid_, _right_, representing wich timestamp from the bin range will identify that bin. If the parameter is _None_, _bin_ entries will stay as time ranges.

+ A `combine` parameter, if it is set to _False_ the dataframe size doesn't change, all the entries stay the same but with a new time bin feature. If it is _True_, all the entries corresponding to a single time bin will be merged.

+ A `keep_size` parameter, used when _combine_ is set. When the parameter is _True_, the dataframe will mantain it's shape, combined features will be repeated, other features will stay as they are. If _False_, all features must be combined, and the shape of the dataframe changes, all entries in the same bin are merged into one.

+ A `features` parameter, used when _combine_ is set, can be the string "all", or a list of _features_. Features in the list (or all features) will be combined, those not in the list will not be changed. This parameter can ommit some features if *keep_size* is _True_, otherwise all features must be combined.

+ The parameters `method_cat` and `method_scalar` are not yet implemented in the function.


~ _work in progress_



______________________________________________________________________________

_documentation will be created in the future_

_visualizing the data is the last part of the project and currently being improved_

*group chats and exported media are not currently supported*

[//]: # (References go here)

[mr]: ./main_read.py (main_read.py file)
[md]: ./main_data.py (main_data.py file)
[chat]: ./chat.py (Chat class definition)
[msg]: ./message.py (Message class definition)
[org]: ./organize.py (organize.py file)
[cdf]: ./create_dataframes.py (full_dataframe method definition)
