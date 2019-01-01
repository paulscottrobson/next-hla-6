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

# ***************************************************************************************
#					This is a code generator for an idealised CPU
# ***************************************************************************************

class SampleCodeGenerator(object):
	def __init__(self):
		pass
	#
	#		Get current address
	#
	def getAddress(self):
		pass
	#
	#		Get word size
	#
	def getWordSize(self):
		return 2
	#
	#		Load a constant or variable into the accumulator.
	#
	def loadDirect(self,isConstant,value):
		pass
	#
	#		Do a binary operation on a constant or variable on the accumulator
	#
	def binaryOperation(self,operator,isConstant,value):
		pass
	#
	#		Store direct
	#
	def storeDirect(self,value):
		pass
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
		pass
	#
	#		Load constant/variable to a temporary area
	#
	def loadParamRegister(self,regNumber,isConstant,value):
		pass
	#
	#		Copy parameter to a temporary area
	#
	def storeParamRegister(self,regNumber,address):
		pass
	#
	#		Create a string constant (done outside procedures)
	#
	def createStringConstant(self,string):
		pass
	#
	#		Call a subroutine
	#
	def callSubroutine(self,address):
		pass
	#
	#		Return from subroutine.
	#
	def returnSubroutine(self):
		pass

if __name__ == "__main__":
	cg = Z80CodeGenerator()
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
