# ***************************************************************************************
#
#		Name : 		preprocessor.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Preprocessor stuff
#
# ***************************************************************************************
# ***************************************************************************************

import re
from exceptions import *

# ***************************************************************************************
#							Pre compilation source processors
# ***************************************************************************************

class PreProcessor(object):
	#
	#		Tidy up tabs, spaces and comments
	#
	def tidySource(self,source):
		source = [x if x.find("//") < 0 else x[:x.find("//")] for x in source] 	# remove comments
		source = [x.replace("\t"," ").strip() for x in source]					# get rid of tabs and strip
		return source
	#
	#		Load in any external dictionaries into the external dictionary
	#
	def loadExternalDictionaries(self,source,externalsDictionary):
		for i in range(0,len(source)):
			if source[i].startswith("external"):
				externalsDictionary.load(source[i][9:].strip())
				source[i] = ""
		return source
	#
	#		Convert quoted strings to constants, generating code for them.
	#
	def processQuotedStrings(self,source,codeGenerator):
		for i in range(0,len(source)):
			if source[i].find('"') >= 0:										# simple check
				if source[i].count('"') % 2 != 0:								# should be even
					raise AssemblerException("Quoted string imabalance")
				parts = re.split("(\".*?\")",source[i])							# split out strings
				for pn in range(0,len(parts)):									# scan them
					if parts[pn].startswith('"'):								# one found, replace it.
						parts[pn] = str(codeGenerator.createStringConstant(parts[pn][1:-1]))
				source[i] = "".join(parts)
		return source
	#
	#		Convert hexadecimal constants
	#
	def processHexConstants(self,source):
		parts = re.split("(0x[0-9a-f]+)",source)								# split out hex
		for pn in range(0,len(parts)):											# scan for them
			if parts[pn].startswith("0x"):
				parts[pn] = str(int(parts[pn][2:],16))
		return "".join(parts)
