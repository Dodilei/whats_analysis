# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:59:22 2020

@author: Dodilei
"""

def large_export(path, Large):

	# Create files to manually analyse large messages
	f0 = open(path+"/large/large.txt", "w", encoding = "utf-8")
	f1 = open(path+"/large/trash_commas.txt", "w", encoding = "utf-8")
	f2 = open(path+"/large/trash_chars_high.txt", "w", encoding = "utf-8")
	f3 = open(path+"/large/trash_chars_low.txt", "w", encoding = "utf-8")
	f4 = open(path+"/large/trash_whitespaces.txt", "w", encoding = "utf-8")
	f5 = open(path+"/large/trash_letters.txt", "w", encoding = "utf-8")
	f6 = open(path+"/large/trash_dots.txt", "w", encoding = "utf-8")
	f7 = open(path+"/large/trash_chain.txt", "w", encoding = "utf-8")
	f8 = open(path+"/large/trash_interesting.txt", "w", encoding = "utf-8")
	f9 = open(path+"/large/trash_custom.txt", "w", encoding = "utf-8")

	# Save files
	fs = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9]
	for f in fs:
		f.close()

	# Fill files
	for self in Large:
		chars = set()
		length = 0
		for char in self.raw:
			length += 1
			chars.update(char)

		if not self._type == "trash":
			temp_type = "large"
		else:
			temp_type = self._subtype

		ft = open(path+"/large/"+temp_type+".txt", "a", encoding = "utf-8")
		ft.write(self.raw[:500]+"\n\n"+
		   "---------------------------------Large message: " +
		   str(len(chars)) + " " + str(len(self.raw)) + " \n" +
		   str(self.info) + "\n\n\n\n\n")
		
		ft.close()
