# -*- coding: utf-8 -*-
"""
Created on Tue Dec  31 08:48:15 2019

@author: Dodilei
"""

import re

import organize as org

from message import Message


class Chat(object):
    
    me_regex = None
    owner = None
    _header_pattern = None
    
    _custom_trash_input = False
    _lists = False

    @staticmethod
    def symbols_range(lst):
        # Method to set Message class symbols list
        Message._symbols_range = lst

    @staticmethod
    def _lists(w, d):
        # Method to set Message class w and d lists
        _lists = True
        Message._whitelist = w
        Message._darklist = d
    
    @staticmethod
    def _Large(l):
        Message.Large = l
    
    @staticmethod
    def _Unidentified(u):
        Message.Unidentified = u
    
    # Methods that return arrays for dataframe
        
    def _get_times(self):
        
        times = []
        for m in self.messages:
            times.append(m.time)
            
        return times
    
    def _get_raw_sizes(self):
        
        rsizes = []
        for m in self.messages:
            rsizes.append(m.raw_size)
            
        return rsizes

    def _get_chars(self):
        
        chars = []
        for m in self.messages:
            try:
                chars.append(m.chars)
            except AttributeError:
                chars.append(None)
            
        return chars

    def _get_size_in_words(self):
        
        wsizes = []
        for m in self.messages:
            try:
                wsizes.append(m.size)
            except AttributeError:
                wsizes.append(None)
            
        return wsizes
    
    def _get_types(self):
        
        types = []
        for m in self.messages:
            types.append(m._type)
            
        return types    
    
    def _get_chat(self):
        
        chatlist = [self.name for i in range(len(self.messages))]         
        return chatlist
    
    def _get_who_sent(self):
        
        whos = []
        for m in self.messages:
            whos.append(m.who)
        
        return whos
    
    def _get_seqs(self):
        
        seqs = []
        for m in self.messages:
            try:
                seqs.append(m.seq)
            except AttributeError:
                seqs.append(None)
        
        return seqs
    
    def _get_shapes(self):
        
        shapes = []
        for m in self.messages:
            shapes.append(m._shape)

        return shapes

    def _get_subtypes(self):
        
        subtypes = []
        for m in self.messages:
            try:
                subtypes.append(m._subtype)
            except AttributeError:
                subtypes.append(None)
                
        return subtypes
    
    def _get_emotes(self):
        
        emotes = []
        for m in self.messages:
            try:
                emotes.append(m.emotes)
            except AttributeError:
                emotes.append(None)
                
        return emotes
    
    def _get_words(self):
        
        words = []
        for m in self.messages:
            try:
                words.append(m.words)
            except AttributeError:
                words.append([])
        
        return words
    
    def _get_mines(self):
        
        mines = []
        for m in self.messages:
            mines.append(m.mine)
            
        return mines
        
    # Mapping of attributes to methods above
    attribute_dict = {
        "time": _get_times,
        "raw_size": _get_raw_sizes,
        "chars": _get_chars,
        "size_in_words": _get_size_in_words,
        "type": _get_types,
        "chat": _get_chat,
        "who_sent": _get_who_sent,
        "seq": _get_seqs,
        "shape": _get_shapes,
        "subtype": _get_subtypes,
        "emotes": _get_emotes,
        "words": _get_words,
        "mine": _get_mines
        }
            
    # Creating Chat class iterator
    def __getitem__(self, key):
        
        if type(key) == str:
        
            return Chat.attribute_dict[key](self)
        
        else:
            
            return self.messages[key]
        

    def __init__(self, name, text):
        Message._custom_trash_input = Chat._custom_trash_input

        # Check if all information is set
        if not Chat._header_pattern:
            print("Set header regex pattern: ")
            Chat._header_pattern = input()

        if not Chat.me_regex:
            print("Set owner's name: ")
            Chat._myname = input()

        if not Chat._lists:
            raise FileNotFoundError("Custom lists path not specified\n\
                               Specify them with Chat._lists\n")
        
        
        self.name = name
        # Sets counter suffix to display chat names
        Message.ct.suffix = "  Current Chat: " + self.name + (" "*20)
        
        # Sets full chat txt as self.raw
        self.raw = text

        # Remove some default global messages
        self.remove_global_msg()

        # Creates messages empty list
        self.messages = []
        
        # Identify and classify all messages in this chat
        self.divide()
        
        
        # Sort messages by type
        self.messages_dict = {'media':[], 'pasted_message':[], 'local':[],
                          'twitter':[], 'google_drive':[], 'deleted':[],
                          'call':[], 'spotify':[], 'default':[],
                          'trash':[], 'instagram':[], 'link':[],
                          'imgur':[], 'contact':[], 'youtube':[]}

        for m in self.messages:
            self.messages_dict[m._type].append(m)
        
        
        # Get chat size
        self.size = len(self.messages)
            
        # Get chat time information
        self.start, self.end, self.duration = org.get_range(self, wreturn = "all")

        # Size of only text messages
        self.size_exclusive_t = len(
        [True for m in self.messages if m._shape == "text"]
        )
    
        # Size of only singular messages
        self.size_exclusive_s = len(
        [True for m in self.messages if m._shape == "singular"]
        )
        

    def divide(self):

        # Identify each message with it's header
        match_all = [*re.finditer(
        Chat._header_pattern +
        "(?:%s): " %
        (self.name + "|" + Chat.me_regex),
        self.raw)
        ]
        
        # Get message header and text
        # Create a Message object and append to self.messages
        for index, m in enumerate(match_all):

            header_start = m.span()[0]
            header_end = message_start = m.span()[1]

            if index < len(match_all) -1: 
                message_end = match_all[index+1].span()[0]
            else:
                message_end = len(self.raw)

            self.messages.append(
        Message(
          self.raw[header_start:header_end],
          self.raw[message_start:message_end],
          self)
          )

    def remove_global_msg(self):

        enc_msg = re.findall(
            Chat._header_pattern + 
            "(?:Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info.|As mensagens e chamadas desta conversa estão protegidas com a criptografia de ponta a ponta. Toque para mais informações.|[A-Za-z]+? changed their phone number. You're currently chatting with their new number. Tap to add it to your contacts.)",
            self.raw)

        for m in enc_msg:        
            self.raw = self.raw.replace(m, "")
    
    def get_range(self, wreturn = None):
        # Return the range of a chat (i.e. timespan)

        time = []
        for m in self.messages:
            time.append(m.time)
        first = min(time)
        last = max(time)

        if wreturn == None:
            return (first, last)
        elif wreturn == "duration":
            return last-first
        elif wreturn == "all":
            return (first, last, last-first)
