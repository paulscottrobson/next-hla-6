
# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		commandassembler.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Assemble a single command.
#
# ***************************************************************************************
# ***************************************************************************************

import re
from exceptions import *

# ***************************************************************************************
#				Worker object that converts preprocessed code to actual code
# ***************************************************************************************

class CommandAssembler(object):
	#
	#		Initialise.
	#
	def __init__(self,codeGenerator,rxIdentifier):
		self.codeGenerator = codeGenerator
		self.rxIdentifier = rxIdentifier
		self.structureStack = [ [ "MARKER",0 ] ]								# marker on stack.
		self.simplelexpr = re.compile("^\@(\d+)\=(.*)$")						# simple l-expr
		self.complexlexpr = re.compile("^\@(\d+)([\!\?])(\@?)(\d+)\=(.*)$")		# complex l-expr
		self.simpleTerm = re.compile("(\@?\d+)")								# term/constant
		self.splitSimpleTerm = re.compile("(\@?)(\d+)")							# same, 2 groups
	#
	#		Assemble a single instruction.
	#
	def assemble(self,line,procedureDict,externalDict,indexVariable):
		print("\t\t ------ "+line+" ------")
		if line == "endproc":													# endproc
			self.codeGenerator.returnSubroutine()
		elif line.startswith("if") or line.startswith("while"):					# if and while are very similar
			self.startIfWhile(line)												# there's just a jump back in while
		elif line == "endif" or line == "endwhile":
			self.endIfWhile(line)
		elif line.startswith("for"):											# for
			self.startFor(line,indexVariable)
		elif line == "endfor":													# endfor
			self.endFor(line)
		elif re.match("^"+self.rxIdentifier+"\(",line) is not None:				# <procedure>(parameters)
			self.procedureCall(line,procedureDict,externalDict)
		else:
			m = self.simplelexpr.match(line) 									# is it <var> = <expr>
			if m is not None:
				self.assembleExpression(m.group(2))
				self.codeGenerator.storeDirect(int(m.group(1)))	
				return
			m = self.complexlexpr.match(line) 									# is it <var>!><term> = <expr>
			if m is not None:
				self.assembleExpression(m.group(5))
				self.codeGenerator.storeIndirect(m.group(2),int(m.group(1)),m.group(3) == "",int(m.group(4)))
				return
			raise AssemblerException("Syntax error")
	#
	#		Compile an expression
	#
	def assembleExpression(self,expr):
		parts = [x for x in self.simpleTerm.split(expr) if x != ""]				# split it up
		if len(parts)%2 == 0:
			raise AssemblerException("Bad expression")
		m = self.splitSimpleTerm.match(parts[0])								# first term.
		assert m is not None
		self.codeGenerator.loadDirect(m.group(1) == "",int(m.group(2)))			# code for it.
		for n in range(1,len(parts),2):											# do each op/term pair
			m = self.splitSimpleTerm.match(parts[n+1])							# examine term and compile code
			self.codeGenerator.binaryOperation(parts[n],m.group(1) == "",int(m.group(2)))
	#
	#		Check structure stack.
	#
	def checkStructure(self):
		if len(self.structureStack) != 1:
			raise AssemblerException("Imbalanced marker")
	#
	#		Assemble a procedure invocation
	#
	def procedureCall(self,line,procedureDict,externalDict):
		m = re.match("^("+self.rxIdentifier+")\((.*?)\)$",line)					# split into parts
		if m is None:
			raise AssemblerException("Bad procedure call")
		name = m.group(1)														# get the parts
		parameters = [x for x in m.group(2).split(",") if x != ""]					
		procIdent = procedureDict.find(name)									# get info about it
		if procIdent is None:
			procIdent = externalDict.find(name)
		if procIdent is None:
			raise AssemblerException("Unknown procedure "+name)

		if procIdent.getParameterCount() != len(parameters):					# correct parameters
			raise AssemblerException("Wrong number of parameters")

		for i in range(0,len(parameters)):										# set up parameter registers
			m = self.splitSimpleTerm.match(parameters[i])
			if m is None:
				raise AssemblerException("Bad parameter")
			self.codeGenerator.loadParamRegister(i,m.group(1) == "",int(m.group(2)))
		self.codeGenerator.callSubroutine(procIdent.getValue())					# code to call subroutine.
	#
	#		Assemble code for if/while structure. While is an If which loops to the test :)
	#
	def startIfWhile(self,line):
		m = re.match("^(while|if)\((.*)([\#\=\<])0\)$",line)					# decode it.
		if m is None:															# couldn't
			raise AssemblerException("Structure syntax error")
		info = [ m.group(1), self.codeGenerator.getAddress() ]					# structure, loop address
		test = { "#":"z","=":"nz","<":"p" }[m.group(3)]							# this is the *fail* test
		info.append(test)
		self.assembleExpression(m.group(2))										# do the expression part
		info.append(self.codeGenerator.getAddress())							# struct,loop,toptest,testaddr
		self.codeGenerator.jumpInstruction(test,0)								# jump to afterwards on fail.
		self.structureStack.append(info)										# put on stack
	#
	def endIfWhile(self,line):
		info = self.structureStack.pop()										# get top structure.
		if "end"+info[0] != line:												# is it not matching ?
			raise AssemblerException("Structure imbalance")
		if line == "endwhile":													# if while loop back before test.
			self.codeGenerator.jumpInstruction("",info[1])
		self.codeGenerator.jumpInstruction(info[2],self.codeGenerator.getAddress(),info[3])	# overwrite the jump.
	#
	#		Assemble code for for/endfor
	#
	def startFor(self,line,indexVariable):
		m = re.match("^for\((.*)\)$",line)										# split it up
		if m is None:															# check format.
			raise AssemblerException("Poorly formatted for")
		self.assembleExpression(m.group(1))										# compile the loop count value
		self.structureStack.append(["for",self.codeGenerator.getAddress()])		# push on the stack.
		self.codeGenerator.forCode()											# generate the for code.
		if indexVariable is not None:											# save index if it exists
			self.codeGenerator.storeDirect(indexVariable.getValue())
	#
	def endFor(self,line):
		info = self.structureStack.pop()										# get the element off the stack
		if info[0] != "for":													# check it is correct.
			raise AssemblerException("endfor without for")
		self.codeGenerator.endForCode(info[1])		#

