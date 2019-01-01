# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		assembler.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Next High Level Assembler, main worker class
#					(no codegenerator)
#
# ***************************************************************************************
# ***************************************************************************************

import re
from exceptions import *
from dictionary import *
from samplecodegen import *
from preprocessor import *
from identifierprocessor import *

# ***************************************************************************************
#									Main Assembler class
# ***************************************************************************************

class AssemblerWorker(object):
	def __init__(self,codeGenerator):
		self.codeGen = codeGenerator 											# save the code generator
		self.keywords = "if,endif,while,endwhile,for,endfor,endproc".split(",")
		self.locals = Dictionary()												# local identifiers
		self.globals = Dictionary()												# global identifiers
		self.procedures = Dictionary()											# procedures.
		self.externals = Dictionary()											# external identifiers
		self.rxIdentifier = "[\$\_a-z][a-z0-9\.\_]*"							# rx matching identifier
		self.rxcIdentifier = re.compile("^"+self.rxIdentifier+"$")				# compiled version
		self.preProcessor = PreProcessor()										# preprocessor worker.
		self.identProcessor = IdentifierProcessor()								# identifier worker.
	#
	#		Assemble a list of strings.
	#
	def assemble(self,code):
		AssemblerException.LINE = 0

		code = self.preProcessor.tidySource(code)								# basic tidying up.
		code = self.preProcessor.loadExternalDictionaries(code,self.externals)	# load in any external dictionaries
		code = self.preProcessor.processQuotedStrings(code,self.codeGen)		# convert quoted strings
		#
		code = (":"+AssemblerWorker.LINE+":").join(code)						# put them all together
		code = code.lower().replace(" ","")										# make all l/c, remove spaces
		#
		code = self.preProcessor.processHexConstants(code)						# convert hex constants.
																				# scan for globals in source
		self.identProcessor.extractGlobals(code,self.globals,self.codeGen,self.rxIdentifier)	
																				# replace globals in source
		code = self.identProcessor.processGlobals(code,self.globals,self.externals,self.rxIdentifier)	
		print(code)

		code = re.split("(proc"+self.rxIdentifier+"\(.*?\))",code)				# split into procedures

		if not code[0].startswith("proc"):										# nothing before.
			if code[0].replace(AssemblerWorker.LINE,"").replace(":","") != "":	# should be nothing else
				raise AssemblerException("Code before first procedure definition")
			AssemblerException.LINE = code[0].count(AssemblerWorker.LINE)		# fix start line
			del code[0]															# remove it

		if len(code) % 2 != 0:													# should be even number.		
			raise AssemblerException("Procedure with no body")

		for cn in range(0,len(code),2):											# +0 header +1 body
			print(code[cn],code[cn+1])

		print(code)

AssemblerWorker.LINE = "~"														# marks new line.
AssemblerWorker.ADDR = "@"														# indicates address.



if __name__ == "__main__":
	src = """

external demo.dict 					// a sample dictionary file.

proc init(p1,p2,p3)
	"hello" >$p4 >$p6
	0x2a73+$p4 >p5 >$p6?2
	0>$test


proc test.version()
	0>$demo

""".split("\n")

	aw = AssemblerWorker(SampleCodeGenerator())
	aw.assemble(src)
