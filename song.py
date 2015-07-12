# -*- coding: utf-8 -*-
#TODO REMOVE COMMENTED CODE AND USELESS PARAMETERS LIKE sort
class Song:
	
	#add tag names included in 'str' into 'tags'
	#et retourne 'str' vidé de ses tags
	#e.g. optionalTags False : ' %tracknumber%. %title% $- %trackartist%$ 
	#           -> (' %%. %% $- %%$', ['tracknumber', 'title', 'trackartist'])
	#e.g. optionalTags True : ' %tracknumber%. %title% $- %trackartist%$ 
	#                    -> (' %tracknumber%. %title% $$', ['- %trackartist%'])
	@staticmethod
	def getTagName(str, optionalTags=False): #(str,tags):
		if optionalTags == True:
			separator="$"
		else:
			separator="%"
		indices = [i for i, x in enumerate(str) if x == separator]
		length = len(indices)//2
		tags = []
		for i in range(0, length):
			tags.append(str[indices[2*i]+1:indices[2*i+1]])
		for t in tags:
			str = str.replace(t, '')    
		return (str, tags)
	
	
	
	def __init__(self, tagDict, treeOrder):
		self.tags={}
		self.tags['file'] = tagDict['FILE']
		self.tags['length'] = tagDict['LENGTH']
		self.tags['samplerate'] = tagDict['SAMPLERATE']
		self.tags['channels'] = tagDict['CHANNELS']
		self.tags['bitrate'] = tagDict['BITRATE']
		(str, fields) = Song.getTagName(treeOrder)
		
		for f in fields:
		    if f.upper() in tagDict:
		        self.tags[f] = tagDict[f.upper()]
		    else:
		        #If albumartist is asked, it is mapped to the artist value
		        if f == 'albumartist' and 'ARTIST' in tagDict:
		            self.tags[f]=tagDict['ARTIST']
		        #trackartist is thus needed in some cases (e.g. compilation),
		        #can be mapped to artist if albumartist existed as a file tag
		        elif (f == 'trackartist' and 'ARTIST' in tagDict and 
		                'ALBUMARTIST' in tagDict and
		                tagDict['ARTIST'] != tagDict['ALBUMARTIST']):
		            self.tags[f]=tagDict['ARTIST']
		        else:
		            self.tags[f]='???'
	
	def toString(self):
		return str(self.tags)
	
	#return the list of values for tag names tagNameList
	def getValues(self, tagNameList):
		values = []
		for name in tagNameList:
		    if name in self.tags:
		        values.append(self.tags[name])
		    else:
		        values.append("error getValues func from Song")
		        '''
		        if attr == 'artist' and 'albumartist' in self.tags:
		            attribs.append(self.tags['albumartist'])
		        else:
		            attribs.append("error getValues func from Song")
		            print(self.tags)
		        '''
		return values
	
	'''
	#return the list of values for tag names tagNameList
	def getValuesSort(self, tagNameList):
	#print('called')
	values = []
	for name in tagNameList:
	    if name == 'tracknumber':
	        try: 
	            int(self.tags['tracknumber'])
	            isInt = True
	        except ValueError:
	            isInt = False
	        if isInt:
	            #Some kind of padding
	            values.append("%05d" % int(self.tags['tracknumber']))
	    elif name in self.tags:
	        values.append(self.tags[name])
	    else:
	        values.append("fucked up getValuesSort func from Song")
	        #if attr == 'albumartist' and 'artist' in self.tag:
	         #   attribs.append(self.tags['artist'])
	        #else:
	        #    attribs.append("error getValues func from Song")
	        
	    
	return values
	'''
	
	
	#return tag values customized with string around
	# '[%date%] | -%artist%' will give ['[1998]', '-DaftPunk']
	def getFormatedValues(self, treeOrder, sort=False):
		treeLevels = [x.strip() for x in treeOrder.split('|')]
		formatedValues = []
		for level in treeLevels:
		    (emptiedLevel, tagNames) = Song.getTagName(level)
		    '''if sort:
		        attribs = self.getAttribsSort(tags)
		    else:
		        attribs = self.getAttribs(tags)
		    '''
		    values = self.getValues(tagNames)
		    for val in values:
		        emptiedLevel = emptiedLevel.replace('%%', str(val), 1)
		    formatedValues.append(emptiedLevel)
		return formatedValues  
	
	#Add support for optional formating using '$ ... $'
	def getOptionalValues(self, treeOrder, sort=False):
		(emptiedTreeOrder, optionalParts) = Song.getTagName(treeOrder, True)
		optionalValues = []
		for part in optionalParts:
		    (emptiedPart, optionalTagNames) = Song.getTagName(part)
		    optionalValues = self.getValues(optionalTagNames)
		    for val in optionalValues:
		        emptiedPart = emptiedPart.replace('%%', str(val), 1)
		    optionalValues.append(emptiedPart)
		
		for val in optionalValues:
		    if '???' not in val:
		        emptiedTreeOrder = emptiedTreeOrder.replace('$$', str(val), 1)
		    else :
		        emptiedTreeOrder = emptiedTreeOrder.replace('$$', '', 1)
		return self.getFormatedValues(emptiedTreeOrder)
	
	
	#return true iif searchedStr exactly matches at least one field of the song
	#do not match case
	def exactMatch(self, searchedStr):
		searchedStr = searchedStr.lower()
		for value in self.tags.values():
		    if value.lower() == searchedStr:
		        return True
		return False
	
	
	#return true if searchedStr is a sub string of at least one field of song
	#do not match case
	def preciseMatch(self, searchedStr):
		searchedStr = searchedStr.lower()
		for value in self.tags.values():
			if str(value).lower().find(searchedStr) != -1:
				return True
		return False
	
	
	#return true if any substring of searchedStr of length 3 is
	#a sub string of at least one field of song, do not match case
	def fuzzyMatch(self, searchedStr):
		searchedStr = searchedStr.lower()
		if len(searchedStr) > 2:
		    for value in self.tags.values():
		        for index in range(0, len(searchedStr)-2):
		            substr = searchedStr[index]+searchedStr[index+1]+searchedStr[index+2]
		            if str(value).lower().find(substr) != -1:
		                return True
		else:
		    for value in self.tags.values():
		            if str(value).lower().find(searchedStr) != -1:
		                return True
		return False
	
	
	
tree_order = '%albumartist% (%genre%)| [%date%] - %album% | $Disc %discnumber% | $ %tracknumber%. %title% $- %trackartist%$'
dict_db = {"TRACKNUMBER": "9/10",
	"DATE": "2007",
	"CHANNELS": 2,
	"BITRATE": 320,
	"GENRE": "Rock",
	"FILE": "/mnt/Data/Documents/Boogie Bones/A/09 Brothers in arms.mp3",
	"ALBUM": "Berlin, Meistersaal",
	"ARTIST": "Mark Knopfler",
	"SAMPLERATE": 44100,
	"TITLE": "Brothers in arms",
	"LENGTH": 489}
	
'''
	song = Song(dict_db, tree_order)
	(emptiedString, tagNames) = song.getTagName(tree_order)
	print(tagNames)
	print(song.getValues(tagNames))
	
	print(song.getOptionalValues(tree_order))
'''