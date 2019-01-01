
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
	#
	#		Assemble a single instruction.
	#
	def assemble(self,line,globalDict,externalDict):
		print("\t\t ------ "+line+" ------")
		if line == "endproc":													# endproc
			self.codeGenerator.returnSubroutine()
#		elif line.startswith("if") or line.startswith("while"):					# if and while are very similar
#			self.startIfWhile(line)												# there's just a jump back in while
#		elif line == "endif" or line == "endwhile":
#			self.endIfWhile(line)
#		elif line.startswith("for"):											# for
#			self.startFor(line)
#		elif line == "endfor":													# endfor
#			self.endFor(line)
#		elif re.match("^"+self.rxIdentifier+"\(",line) is not None:				# <procedure>(parameters)
#			self.procedureCall(line)
#		else:
#			self.assembleExpression(line)										# try it as a straight expression.
	#
	#		Check structure stack.
	#
	def checkStructure(self):
		if len(self.structureStack) != 1:
			raise AssemblerException("Imbalanced marker")
	#
	#		Assemble a procedure invocation
	#
	def procedureCall(self,line):
		pass
	#
	#		Assemble code for if/while structure. While is an If which loops to the test :)
	#
	def startIfWhile(self,line):
		m = re.match("^(while|if)\((.*)([\#\=\<])0\)$",line)					# decode it.
		if m is None:															# couldn't
			raise AssemblerException("Structure syntax error")
		info = [ m.group(1), self.codeGen.getAddress() ]						# structure, loop address
		test = { "#":"z","=":"nz","<":"p" }[m.group(3)]							# this is the *fail* test
		info.append(test)
		self.assembleExpression(m.group(2))										# do the expression part
		info.append(self.codeGen.getAddress())									# struct,loop,toptest,testaddr
		self.codeGen.jumpInstruction(test,0)									# jump to afterwards on fail.
		self.structureStack.append(info)										# put on stack

	def endIfWhile(self,line):
		info = self.structureStack.pop()										# get top structure.
		if "end"+info[0] != line:												# is it not matching ?
			raise AssemblerException("Structure imbalance")
		if line == "endwhile":													# if while loop back before test.
			self.codeGen.jumpInstruction("",info[1])
		self.codeGen.jumpInstruction(info[2],self.codeGen.getAddress(),info[3])	# overwrite the jump.
	#
	#		Assemble code for for/endfor
	#
	def startFor(self,line):
		m = re.match("^for\((.*)\)$",line)										# split it up
		if m is None:															# check format.
			raise AssemblerException("Poorly formatted for")
		self.assembleExpression(m.group(1))										# compile the loop count value
		self.structureStack.append(["for",self.codeGen.getAddress()])			# push on the stack.
		self.codeGen.forCode()													# generate the for code.
		indexInfo = self.dictionary.find("index")								# index defined ?
		if indexInfo is not None:												# save index if it exists
			self.codeGen.storeDirect(indexInfo.getValue())
	#
	def endFor(self,line):
		info = self.structureStack.pop()										# get the element off the stack
		if info[0] != "for":													# check it is correct.
			raise AssemblerException("endfor without for")
		self.codeGen.endForCode(info[1])		#
