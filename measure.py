# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 16:29:56 2020

@author: Dodilei
"""

import re

def purify(word):

	p1 = re.sub("[^a-zA-Záéíóúâêîôûãõç]-[^a-zA-Záéíóúâêîôûãõç]", "", word)
	p2 = re.sub("[^a-zA-Záéíóúâêîôûãõç-]+", "", p1)

	return p2

def measure_words(sample):

	lines = sample.split("\n")
	words = []
	for line_list in [re.split(" +", line) for line in lines]:
		for word in line_list:
			pure = purify(word)
			if pure:
				words.append(pure)

	return words
