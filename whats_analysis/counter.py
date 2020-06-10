#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:56:13 2020

@author: mauricio
"""


class Counter(object):
    
    def __init__(self, mod = 10000, init = 0, step = 1,
				 print_style = "newline", prefix = None, suffix = None):
        
        self.count = init
        self.mod = mod
        self.step = step
        self.suffix = suffix
        self.prefix = prefix
        
        
        if print_style == "newline":
            self.print_count = self._print_count_newline
        
        elif print_style == "in_place":
            self.print_count = self._print_count_in_place
        
        else:
            self.print_count = self._print_count_newline
        
    def run(self):
        self.count += self.step
        if self.mod:
            if self.count % self.mod == 0:
                self.print_count()
        else:
            self.print_count()
        
    def _print_count_newline(self):
        print(self.count)
    
    def _print_count_in_place(self):
        print("\r", self.prefix, self.count, self.suffix, sep = "", end = "")

