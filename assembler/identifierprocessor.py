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
	def __init__(self):
		self.keywords = "if,endif,while,endwhile,for,endfor,endproc".split(",")
	#
	#		Extract variables (e.g the sequence :$<identifier> = and create them.
	#		can be used for global or local.
	#
	def extractVariables(self,source,dictionary,codeGen,rxIdentifier):
		parts = re.split("(\:"+rxIdentifier+"\=]*)",source)						# split out, check for !?(
		for pn in range(0,len(parts)):											# scan them
			if parts[pn] not in self.keywords:		
				if re.match("^\:"+rxIdentifier+"\=$",parts[pn]) is not None:	# NOT indirect assign or proc call
					if dictionary.find(parts[pn][1:-1]) is None:				# if doesn't exist already
						varIdent = VariableIdentifier(parts[pn][1:-1],codeGen.allocSpace(None,parts[pn][1:-1]))
						dictionary.addIdentifier(varIdent)
	#
	#		Process variables - replace them all with addresses - can be used for local and
	#		global. Do not process procedure calls.
	#
	def processVariables(self,source,globalDictionary,externalDictionary,rxIdentifier):
		parts = re.split("("+rxIdentifier+"[\(]*)",source)						# split out, check for (
		for pn in range(0,len(parts)):											# scan them
			if re.match("^"+rxIdentifier+"$",parts[pn]) is not None:			# NOT proc call
				if parts[pn] not in self.keywords:
					ident = globalDictionary.find(parts[pn])					# look it up	
					if ident is None:	
						ident = externalDictionary.find(parts[pn])				# try external.
					if ident is None:											# not defined.
						raise AssemblerException("Variable {0} not defined".format(parts[pn]))
					parts[pn] = AssemblerWorker.ADDR + str(ident.getValue())		# replace with address marker
		return "".join(parts)
	#
	#		Process the header.
	#
	def processHeader(self,name,parameters,localsDictionary,codeGenerator,rxIdentifier):
		#
		#		Split up parameter text, check not more than four.
		#
		parameters = [x for x in parameters.split(",") if x.strip() != ""]		# split parameters.
		if len(parameters) > 4:
			raise AssemblerException("Too many parameters.")
		#
		#		Create local variables for each parameter.
		#
		for pn in range(0,len(parameters)):										# for each parameter
			if re.match("^"+rxIdentifier+"$",parameters[pn]) is None:			# validate it.
				raise AssemblerException("Bad parameter "+parameters[pn])
			if localsDictionary.find(parameters[pn]) is None:
																				# create id/variable
				pid = VariableIdentifier(parameters[pn],codeGenerator.allocSpace(None,parameters[pn]))	
				localsDictionary.addIdentifier(pid)									# add to local dict
		#
		#		Create the actual first bit.
		#
		procIdent = ProcedureIdentifier(name,codeGenerator.getAddress(),len(parameters))
		#
		#		Code to store passing registers.
		#	
		for pn in range(0,len(parameters)):
			codeGenerator.storeParamRegister(pn,localsDictionary.find(parameters[pn]).getValue())
		#
		#		Return the identifier for the new procedure.
		#
		return procIdent
