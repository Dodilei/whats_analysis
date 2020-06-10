# -*- coding: utf-8 -*-
"""
Created on Tue Dec  31 08:45:43 2019

@author: Dodilei
"""

import re
import datetime as dt

from measure import measure_words
from counter import Counter

class Message(object):

	# Initialize counter
	ct = Counter(mod = 0, init = 0, step = 1,
			    print_style = "in_place",prefix = " Messages: ")
	
	# Emoji range to avoid errors when printing
	emojis = [chr(i) for i in range(127744, 129792)]

	_custom_trash_input = False
	_darklist = None
	_whitelist = None
	_symbols_range = None

	# Temporary debbuging lists
	Large = None
	Unidentified = None

	def __init__(self, header, text, parent):

        # Run counter
		Message.ct.run()

        # Variable to track unindentified messages
		self.identified = True

		self.header = header
		self.raw = text
		self.parent = parent

        # Sets raw size (number of chars)
		self.raw_size = len(self.raw)

        # Make all headers uniform and get the information contained
		self.cleanup_header()

		# Set message timestamp
		self.time = dt.datetime(
			*self.info[:3],
			*[int(i) for i in self.info[3].split(":")]
			)
        
        # Sets sequence number for messages with same timestamp
		self.seq = self.msg_seq()
        
		self.mine = bool(re.search(self.parent.owner, self.info[4]))
        
        # Get name of who sent the message
		#self.who = self.parent.name if not self.mine else self.parent.owner
		self.who = self.info[4]

        # Classify singular messages and default messages (text)
		self.classify()
        # Classify text messages
		if self._shape == "text": self.reclassify()

        # Set relevant quantities (words, chars, emojis)
		self.quantify()


	def cleanup_header(self):

		header_raw = re.fullmatch(
			"\n(\d{1,2})/(\d{1,2})/(\d{1,2}), (\d{2}:\d{2}) - (.+?): ",
			self.header
			)

		month = "0"*(2-len(header_raw.group(1))) + header_raw.group(1)
		day = "0"*(2-len(header_raw.group(2))) + header_raw.group(2)
		year = "20" + "0"*(2-len(header_raw.group(3))) + header_raw.group(3)

		time = header_raw.group(4)
		name = header_raw.group(5)

		self.header = (
						day + "/" +
						month + "/" +
						year + ", " +
						time + " - " +
						name + ": "
					  )
			
		self.info = [int(year), int(month), int(day), time, name]


	def msg_seq(self):
        
        # Gets message sequence number

		if (len(self.parent.messages) > 0
		    and
		    self.parent.messages[-1].time == self.time
			):
			
			return self.parent.messages[-1].seq +1

		else: return 0


	def classify(self):

		# Classifies the message:
        
        # MEDIA
		if re.fullmatch(
				"<Media omitted>", self.raw):
			
			self._shape = "singular"
			self._type = "media"
			self._subtype = None
        
		
        # DELETED
		elif self.mine and re.fullmatch(
				"You deleted this message", self.raw):
			
			self._shape = "singular"
			self._type = "deleted"
			self._subtype = None

		elif not self.mine and re.fullmatch(
				"This message was deleted", self.raw):
			
			self._shape = "singular"
			self._type = "deleted"
			self._subtype = None
        
		
        # LOCATION
		elif re.match("location: ", self.raw):
			self._shape = "singular"
			self._type = "local"
			self._subtype = "static"

		elif re.fullmatch("live location shared", self.raw):
			self._shape = "singular"
			self._type = "local"
			self._subtype = "live"


        # CONTACT
		elif re.fullmatch(
				"(?:.+?\.vcf) [(]file attached[)]", self.raw):
			
			self._shape = "singular"
			self._type = "contact"
			self._subtype = re.match(".+?\.vcf", self.raw)[0][:-4]


        # CALL
		elif re.fullmatch(
				"Missed(?: group)? (?:video|voice) call", self.raw):
			
			self._shape = "singular"
			self._type = "call"
			self._subtype = "missed"


        # DEFAULT
		else:
			self._shape = "text"
			self._type = "default"
			self._subtype = None


	def reclassify(self):
        
        # Classify text messages in more detail

		# Search for and classify very large messages
        # Tries to identify irrelevant(trash) messages
        
		_large = self.raw_size >= 450

        # If the message has not yet been classified as "large"
		if _large and not self._type == "large":

			chars = set(self.raw)
			length = self.raw_size

            # Messages will be classified irrelevant(trash) for:
            
            # LOW NUMBER OF CHARS
			if len(chars) < 10:
				self._type = "trash"
				self._subtype = "trash_chars_low"

				Message.Large.append(self)

				return True

            # HIGH NUMBER OF CHARS
			if len(chars) > 100:
				self._type = "trash"
				self._subtype = "trash_chars_high"

				Message.Large.append(self)

				return True

            # LESS THAN HALF ARE LETTERS
			l_count = 0
			for letter in "abcdefghijklmnopqrstuvwxyz":
				if letter in chars:
					l_count +=1

			if l_count/26 < 0.5:
				self._type = "trash"
				self._subtype = "trash_letters"

				Message.Large.append(self)

				return True

            # SPECIFIC CHAIN
			if re.match("\U0001F4A2", self.raw):
				self._type = "trash"
				self._subtype = "trash_chain"

				Message.Large.append(self)

				return True

            # LOW COUNT OF SPACES
			if self.raw.count(" ")/length < 0.1:
				self._type = "trash"
				self._subtype = "trash_whitespaces"

				Message.Large.append(self)

				return True

            # TOO MUCH DOTS
			if self.raw.count(".")/length > 0.1:
				self._type = "trash"
				self._subtype = "trash_dots"

				Message.Large.append(self)

				return True

            # TOO MUCH COMMAS
			if self.raw.count(",")/length > 0.15:
				self._type = "trash"
				self._subtype = "trash_commas"

				Message.Large.append(self)

				return True
			
			# Remaining messages, i.e. not removed by irrelevance,
            # can now be classified manually if they were not yet
			if Message._custom_trash_input:
				with open(Message._darklist, "a+", encoding="utf-8") as f:
					with open(Message._whitelist, "a+", encoding="utf-8") as f2:
						f.seek(0)
						f2.seek(0)
                        
                        # Search if message was classified
                        # If not, print it and ask for input
                        
                        # Input can be:
                        # empty, if message IS relevant
                        # in the shape "trash_"+{type} if IRRELEVANT
                        
                        # each trash type will be saved at different files
                        
                        # After the first classification
                        # messages do not need to be reclassified
                        
						if (not self.raw+"\ue000" in f.read()
							and not self.raw+"\ue000" in f2.read()
							):
							temp_raw = self.raw[:1000]
							for char in Message.emojis:
								temp_raw = temp_raw.replace(char, "")

							print(temp_raw)
							self._subtype = input()
							if "trash" in self._subtype:
								self._type = "trash"
								f.write(self.raw+"\ue000"+self._subtype+"\ue000")
							else:
								f2.write(self.raw+"\ue000")

			# Search for irrelevant message classification in darklist
			with open(Message._darklist, "r", encoding="utf-8") as _f:
				f = _f.read()
				if self.raw in f:
					if self.raw+"\ue000trash_interesting\ue000" in f:
						self._type = "trash"
						self._subtype = "trash_interesting"
					elif self.raw+"\ue000trash_chain\ue000" in f:
						self._type = "trash"
						self._subtype = "trash_chain"
					else:
						self._type = "trash"
						self._subtype = "trash_custom"
			
					Message.Large.append(self)

					return True
			
            # If the large message was not classified irrelevant
            # it'll be reclassified like a default text message
			self._type = "large"
			Message.Large.append(self)
			self.reclassify()

			return True

		# Search for a generic link
		_link = re.search("(.*?)https?://(.+?)\.(.+?)(?: |.*)(.*)", self.raw)

		if _link:

			#Search for double links
			_double = re.search("(.*?)https?://(.*?)https?://(.*?)", self.raw)

			if _double:
				self._type = "link"
				self._subtype = "doublelink"

				self.size = 0
				self.chars = 0

				return True

			# Search for and classify spotify shares
			_spotify = re.search("(.*?)https://open\.spotify\.com/(.+?)/(.*)",
								self.raw)

			if _spotify:
				self.s_noheader = False
				self._type = "spotify"
				self._subtype = _spotify.group(2)

				if self._subtype == "user" and re.match("(.+?)/playlist/", _spotify.group(3)):
					self._subtype == "playlist"

				if self._subtype == "track" and _spotify.group(1):
					self.s_music = re.search("(?:Here’s a song for you…|Aqui está uma música para você…) (.*?)\nhttps://open\.spotify\.com/track/.+", _spotify).group(1)

				elif self._subtype == "album" and _spotify.group(1):
					self.s_album = re.search("(?:Here’s an album for you…|Aqui está um álbum para você…) (.*?)\nhttps://open\.spotify\.com/album/.+", _spotify).group(1)

				elif self._subtype == "artist" and _spotify.group(1):
					self.s_artist = re.search("(?:Here’s an artist I want to share with you…|Aqui está um artista que eu gostaria de compartilhar com você…) (.*?)\nhttps://open\.spotify\.com/artist/.+", _spotify).group(1)
				
				elif self._subtype == "playlist" and _spotify.group(1):
					self.s_playlist = re.search("(?:Here’s a playlist for you…|Aqui está uma playlist para você…) (.*?)\nhttps://open\.spotify\.com/user/(.+?)/playlist/.+", _spotify).group(1)
				
				elif self._subtype == "user" and _spotify.group(1):
					self.s_user = re.search("https://open\.spotify\.com/user/(.+?)/.+", _spotify).group(1)

				elif not _spotify.group(1):
					self.s_noheader = True

				else: 
					#print("Unidentified spotify link: ", self.raw)
					Message.Unidentified.append([self.raw, self.parent.name])

				self.size = 20
				self.chars = 100

				return True

			# Search for and classify youtube shares
			_youtube = re.search("(.*?)https://www\.youtube\.com/(.+)", self.raw)
			_youtube2 = re.search("(.*?)https://youtu\.be/(.+)", self.raw)

			if _youtube or _youtube2:
				self._type = "youtube"

				if _youtube2:
					self._subtype = "video"

				elif re.match("watch\?(?:t=\d+?&)?(?:time_continue=\d+?&)?v=(.+)", _youtube.group(2)):
					self._subtype = "video"

				elif re.match("playlist\?list=(.+)", _youtube.group(1)):
					self._subtype = "playlist"

				elif re.match("channel/(.+)", _youtube.group(2)):
					self._subtype = "channel"

				elif re.match("user/(.+)", _youtube.group(2)):
					self._subtype = "user"
					self.y_user = re.match("user/(.+)", _youtube.group(2)).group(1)

				else:
					#print("Unidentified youtube link: ", self.raw)
					Message.Unidentified.append([self.raw, self.parent.name])

				self.size = 20
				self.chars = 100

				return True

			# Search for and classify imgur shares
			_imgur = re.search("(.*?)https://imgur\.com/(.+)", self.raw)

			if _imgur:
				self.i_noheader = False
				self._type = "imgur"

				if re.match("gallery/", _imgur.group(2)):
					self._subtype = "gallery"
					if _imgur.group(1):
						self.i_name = _imgur.group(1)
					else: self.i_noheader = True

				else:
					self._subtype = "single"
					if _imgur.group(1):
						self.i_name = _imgur.group(1)
					else: self.i_noheader = True

				self.size = 10
				self.chars = 50

				return True

			# Search for and classify instagram shares
			_instagram = re.search("(.*?)https://instagram\.com/(.+)", self.raw)

			if _instagram:
				self._type = "instagram"

				if re.match("p/(.+)", _instagram.group(2)):
					self._subtype = "post"

				elif re.match("(.+?)\?igshid.+", _instagram.group(2)):
					self._subtype = "profile"
					self.ig_user = re.match("(.+?)\?igshid.+", _instagram.group(2)).group(1)

				else:
					#print("Unidentified instagram link: ", self.raw)
					Message.Unidentified.append([self.raw, self.parent.name])

				self.size = 10
				self.chars = 50

				return True

			# Search for and classify twitter shares
			_twitter = re.search("(.*?)https://twitter\.com/(.+)", self.raw)

			if _twitter:
				self._type = "twitter"

				if re.match("(.+?)/status/.+", _twitter.group(2)):
					self._subtype = "tweet"
					self.t_user = re.match("(.+?)/status/.+", _twitter.group(2)).group(1)

				elif re.match("i/moments/.+", _twitter.group(2)):
					self._subtype = "moment"

				elif not re.search("[/]", _twitter.group(2)):
					self._subtype = "user"
					self.t_user = _twitter.group(2) #needs updating (azaghal?s=08)

				else:
					#print("Unidentified twitter link: ", self.raw)
					Message.Unidentified.append([self.raw, self.parent.name])

				self.size = 8
				self.chars = 40

				return True

			# Search for google drive shares
			_gdrive = re.search("(.*?)https://drive\.google\.com/drive/(.+)", self.raw)

			if _gdrive:
				self._type = "google_drive"

				if re.match("folders/.+", _gdrive.group(2)):
					self._subtype = "folder"

				else:
					#print("Unidentified gdrive link: ", self.raw)
					Message.Unidentified.append([self.raw, self.parent.name])

				self.size = 1
				self.chars = 0

				return True

			# Search for google maps shares
			_gmaps = re.search("(.*?)https://maps\.app\.goo\.gl/(.+)", self.raw)
			_gmaps2 = re.search("(.*?)https://www\.google\.com/maps/(.+)", self.raw)
			_gmaps3 = re.search("(.*?)https://goo\.gl/maps/(.+)", self.raw)

			if _gmaps or _gmaps2 or _gmaps3:
				self._type = "local"

				return True

			self._type = "link"
			sample = (_link.group(1)+_link.group(4))
			self.size = self.measure(sample = sample) #needs reworking
			self.chars = len(sample)

			return True
        
        # Search for messages copied from anoter chat
		_pasted_message = re.search("\[\d{1,2}h\d{1,2} \d{1,2}/\d{1,2}/\d{1,4}\] (.+?): ", self.raw)

		if _pasted_message:
			self._type = "pasted_message"

			pm_headers = re.findall("\[\d{1,2}h\d{1,2} \d{1,2}/\d{1,2}/\d{1,4}\] (.+?): ", self.raw)

			temp_raw = self.raw
			for h in pm_headers:
				temp_raw = temp_raw.replace(h, "")

			self.size = self.measure(sample = temp_raw)
			self.chars = len(self.raw) - 20*len(pm_headers)

			return True

        # If message was not classified as an special type
		self._type = "default"
		return True


	def quantify(self):

		# Measure sizes for text messages and set relative sizes for other types

		if self._type == "default":

			self.size = self.measure()
			self.chars = self.raw_size
			self.emotes = self.count_e()

		elif self._type == "media":

			self.size = 8
			self.chars = 80
			self.emotes = 0

		elif self._type == "link":

			self.size += 3
			self.chars += 15
			self.emotes = 0

		elif self._type == "deleted":

			self.size = 0
			self.chars = 0
			self.emotes = 0

		elif self._type == "local":

			self.size = 8
			self.chars = 40
			self.emotes = 0

		elif self._type == "contact":

			self.size = 0
			self.chars = 0
			self.emotes = 0

		elif self._type == "call":

			self.size = 1
			self.chars = 10
			self.emotes = 0

		elif "trash" in self._type:

			self.size = 0
			self.chars = 0
			self.emotes = 0

	def measure(self, sample = None):
        # Try to count the number of words in the message
        
		if not sample: sample = self.raw

		if self._type == "default":
			self.words = measure_words(sample)
			return len(self.words)

		return len(measure_words(sample))

	def count_e(self, sample = None):
        # Count the of emojis in the message
        
		if not sample: sample = self.raw

		count = 0
		#types = set()

		for c in self.raw:
			if c in Message._symbols_range:
				count += 1
				
		return count
