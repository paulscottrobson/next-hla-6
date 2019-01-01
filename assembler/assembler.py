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
from commandassembler import *

# ***************************************************************************************
#									Main Assembler class
# ***************************************************************************************

class AssemblerWorker(object):
	def __init__(self,codeGenerator):
		self.codeGen = codeGenerator 											# save the code generator

		self.locals = Dictionary()												# local identifiers
		self.globals = Dictionary()												# global identifiers
		self.procedures = Dictionary()											# procedures.
		self.externals = Dictionary()											# external identifiers

		self.rxIdentifier = "[\$\_a-z][a-z0-9\.\_]*"							# rx matching identifier
		self.preProcessor = PreProcessor()										# preprocessor worker.
		self.identProcessor = IdentifierProcessor()								# identifier worker.
		self.cmdAssembler = CommandAssembler(codeGenerator,self.rxIdentifier)	# assemble a command

																				# add return here, because it's permanent
		retid = VariableIdentifier("$return",codeGenerator.allocSpace(None,"$return"))
		self.externals.addIdentifier(retid)

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
		self.identProcessor.extractVariables(code,self.globals,self.codeGen,"\$"+self.rxIdentifier)	
																				# replace globals in source
		code = self.identProcessor.processVariables(code,self.globals,self.externals,"\$"+self.rxIdentifier)	
		#print(code)

		code = re.split("(proc"+self.rxIdentifier+"\(.*?\))",code)				# split into procedures

		if not code[0].startswith("proc"):										# nothing before.
			if code[0].replace(AssemblerWorker.LINE,"").replace(":","") != "":	# should be nothing else
				raise AssemblerException("Code before first procedure definition")
			AssemblerException.LINE = code[0].count(AssemblerWorker.LINE)		# fix start line
			del code[0]															# remove it

		if len(code) % 2 != 0:													# should be even number.		
			raise AssemblerException("Procedure with no body")

		for cn in range(0,len(code),2):											# +0 header +1 body
			#print(code[cn],code[cn+1])
			mHeader=re.match("^proc("+self.rxIdentifier+")\((.*)\)$",code[cn])	# split up the header
			assert mHeader is not None

			self.locals = Dictionary()											# new locals dictionary.
																				# Look for locals.
			self.identProcessor.extractVariables(code[cn+1],		\
									self.locals,self.codeGen,self.rxIdentifier)
																				# process the header.
			ident = self.identProcessor.processHeader(mHeader.group(1),	\
							mHeader.group(2),self.locals,self.codeGen,self.rxIdentifier)
			self.procedures.addIdentifier(ident)								# add procedure to dict.

			pcode = self.identProcessor.processVariables(code[cn+1],			# replace the locals.
									self.locals,self.externals,self.rxIdentifier)
			pcode = pcode.replace(AssemblerWorker.ADDR+"@","")					# makes @ operator work.
			pcode = pcode.split(":")											# split into individual commands
			for cmd in pcode:
				if cmd == AssemblerWorker.LINE:									# line marker
					AssemblerException.LINE += 1
				elif cmd != "":													# assemble non blank.
					self.cmdAssembler.assemble(cmd,self.globals,self.externals,self.locals.find("index"))
			self.cmdAssembler.checkStructure()									# check structure ukay.
		#
		#		Finished assembly
		#

AssemblerWorker.LINE = "~"														# marks new line.
AssemblerWorker.ADDR = "@"														# indicates address.



if __name__ == "__main__":
	src = """

external demo 					// a sample dictionary file.

proc init(p1,p2,p3)
	$p4 = p1 + p2 + p3
	$p6 = "hello"
	$p4?$p6 = 42
	$p6!2 = 0x2a73+$p4 
	$test = p1?4
endproc

proc struct(c):
	index = 13
	if (c#0):$a=1:endif
	while (c<0):c=c+1:endwhile
	for (c):$a=$a+1:endfor
	$return = 69
endproc

proc test.version()
	test.version()
	init($demo,count,42)
	$demo = @$demo
	count = 0
	count = count + 1
	struct(42)
endproc
""".split("\n")

	aw = AssemblerWorker(SampleCodeGenerator())
	aw.assemble(src)
