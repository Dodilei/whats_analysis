# whats_analysis
Read and analyse Whatsapp chats

# 0. Prerequisites

All chat .txt files must be placed inside the Chat folder (to get them, use the "export chat" option from whatsapp)

Some manual arrangements can improve code functionality and the readability of the data display:
- Place an empty newline in the beginning and end of each chat (if it doesn't exist yet)
- Merge chats with the same person (especially when someone changes their phone number, don't forget to update all the names inside de text file)
- Use clean, readable names (if a change is made, both the file name and all the entries in the text must be updated)

When the code starts, it'll ask you for information. In the default environment, the only information needed is your name:
Write as follows:
>> info name: owner
>> value: YOUR_NAME*

* Your name must be written exactly like it is in your whatsapp account. To be certain, check how it is displayed inside the chat txt files.

# 1. Import, read and process chats

The first file to run is "main_read.py".
This code will open all chat files, get their raw text and name and store in a list.
This list is then used to create a dictionary which maps the names to the Chat objects.

Chat objects (from the Chat class) are created with only the name and raw text, the class itself handles the message recognition and creation of Message objects.
Message objects are created with a header and raw text (from a single message), the class itself handles message classification and getting other relevant information.

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
  

# 2. Organize and store data

The "main_data.py" file will get the data processed by "main_read.py" and organize it in a Pandas dataframe with all desired features.


# 3. Data display

Work in progress.

_documentation will be created in the future_

_visualizing the data is the last part of the project and currently being improved_

*group chats are not currently supported*
