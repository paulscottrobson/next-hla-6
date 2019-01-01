# ***************************************************************************************
#
#		Name : 		identifierprocessor.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Identifier Processing stuff.
#
# ***************************************************************************************
# ***************************************************************************************

import re
from exceptions import *
from dictionary import *
from assembler import *

# ***************************************************************************************
#							Processing around identifiers
# ***************************************************************************************

class IdentifierProcessor(object):
	#
	#		Extract globals (e.g the sequence >$<identifier>) NOT followed by !?( and create them.
	#
	def extractGlobals(self,source,globalDictionary,codeGen,rxIdentifier):
		parts = re.split("(\>\$"+rxIdentifier+"[\!\?\()]*)",source)				# split out, check for !?(
		for pn in range(0,len(parts)):											# scan them
			if re.match("^\>\$"+rxIdentifier+"$",parts[pn]) is not None:		# NOT indirect assign or proc call
				varIdent = VariableIdentifier(parts[pn][1:],codeGen.allocSpace())
				globalDictionary.addIdentifier(varIdent)
	#
	#		Process globals - replace them all with addresses
	#
	def processGlobals(self,source,globalDictionary,externalDictionary,rxIdentifier):
		print(source)
		parts = re.split("(\$"+rxIdentifier+"[\(]*)",source)					# split out, check for (
		for pn in range(0,len(parts)):											# scan them
			if re.match("^\$"+rxIdentifier+"$",parts[pn]) is not None:			# NOT proc call
				ident = globalDictionary.find(parts[pn])						# look it up	
				if ident is None:	
					ident = externalDictionary.find(parts[pn])
				if ident is None:												# not defined.
					raise AssemblerException("Global {0} not defined".format(parts[pn]))
				parts[pn] = AssemblerWorker.ADDR + str(ident.getValue())		# replace with address marker
		return "".join(parts)
