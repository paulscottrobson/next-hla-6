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

# ***************************************************************************************
#									Main Assembler class
# ***************************************************************************************

class AssemblerWorker(object):
	def __init__(self,codeGenerator):
		self.codeGen = codeGenerator 											# save the code generator
		self.keywords = "if,endif,while,endwhile,for,endfor,endproc".split(",")
		self.locals = Dictionary()												# local identifiers
		self.globals = Dictionary()												# global identifiers
		self.externals = Dictionary()											# external identifiers
		self.rxIdentifier = "[\$\_a-z][a-z0-9\.\_]*"							# rx matching identifier
		self.rxcIdentifier = re.compile("^"+self.rxIdentifier+"$")				# compiled version
	#
	#		Assemble a list of strings.
	#
	def assemble(self,code):
		print(code)





if __name__ == "__main__":
	src = """

external demo.dict 					// a sample dictionary file.

def init(p1,p2,p3)
	"hello" >$p4
	$2a73+$p4 >p5

""".split("\n")

	aw = AssemblerWorker(SampleCodeGenerator())
	aw.assemble(src)
