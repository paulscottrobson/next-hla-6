# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		z80codegen.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Z80 Code Generator class.
#
# ***************************************************************************************
# ***************************************************************************************

from imagelib import *

# ***************************************************************************************
#					This is a code generator for the Z80 (Next)
# ***************************************************************************************

class Z80CodeGenerator(object):
	def __init__(self,image):
		self.image = image
		self.image.echo = True
		self.freeMemory = 0x8000
	#
	#		Get current address
	#
	def getAddress(self):
		return self.image.getCodeAddress()
	#
	#		Get word size
	#
	def getWordSize(self):
		return 2
	#
	#		Load a constant or variable into the accumulator.
	#
	def loadDirect(self,isConstant,value):
		self.image.cByte(0x21 if isConstant else 0x2A)
		self.image.cWord(value)
	#
	#		Do a binary operation on a constant or variable on the accumulator
	#
	def binaryOperation(self,operator,isConstant,value):
		pass
	#
	#		Store direct
	#
	def storeDirect(self,value):
		self.image.cByte(0x22)
		self.image.cWord(value)
	#
	#		Store A indirect to address [variable] + offset/[offset]
	#		
	def storeIndirect(self,dataSize,baseVariable,offsetIsConstant,offset):
		pass
	#
	#		Generate for code.
	#
	def forCode(self):
		pass
	#
	#		Gemerate endfor code.
	#
	def endForCode(self,loopAddress):
		pass
	#
	#	Compile a loop instruction. Test are z, nz, p or "" (unconditional). The compilation
	#	address can be overridden to patch forward jumps.
	#
	def jumpInstruction(self,test,target,override = None):
		pass
	#
	#		Allocate count bytes of meory, default is word size
	#
	def allocSpace(self,count = None,reason = None):
		count = 1 if count is None else count
		count *= self.getWordSize()
		self.freeMemory -= count
		return self.freeMemory
	#
	#		Load constant/variable to a temporary area
	#
	def loadParamRegister(self,regNumber,isConstant,value):
		cmds = [0x21,0x11,0x01,0xDD21] if isConstant else [0x2A,0xED5B,0xED4B,0xDD2A]
		if cmds[regNumber] >= 0x100:
			self.image.cByte(cmds[regNumber] >> 8)
		self.image.cByte(cmds[regNumber] & 0xFF)
		self.image.cWord(value)
	#
	#		Copy parameter to a temporary area
	#
	def storeParamRegister(self,regNumber,address):
		cmds = [0x22,0xED53,0xED43,0xDD22]
		if cmds[regNumber] >= 0x100:
			self.image.cByte(cmds[regNumber] >> 8)
		self.image.cByte(cmds[regNumber] & 0xFF)
		self.image.cWord(address)
	#
	#		Create a string constant (done outside procedures)
	#
	def createStringConstant(self,string):
		addr = self.getAddress()
		for c in string:
			self.image.cByte(ord(c))
		self.image.cByte(0)
		return addr
	#
	#		Call a subroutine
	#
	def callSubroutine(self,address):
		self.image.cByte(0xCD)
		self.image.cWord(address)
	#
	#		Return from subroutine.
	#
	def returnSubroutine(self):
		self.image.cByte(0xC9)

if __name__ == "__main__":
	cg = Z80CodeGenerator(BootImage())
	cg.loadDirect(True,42)
	cg.loadDirect(False,42)	
	print("------------------")
	cg.binaryOperation("%",True,44)
	cg.binaryOperation("&",False,44)	
	cg.binaryOperation("?",True,44)
	cg.binaryOperation("!",False,44)
	print("------------------")
	cg.storeDirect(46)
	print("------------------")
	cg.allocSpace(4)
	cg.allocSpace(1)	
	print("------------------")
	cg.createStringConstant("Hello world!")
	print("------------------")
	cg.callSubroutine(42)
	cg.returnSubroutine()
	print("------------------")
