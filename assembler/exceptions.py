# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		errors.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Exception
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#									Exception for HLA
# ***************************************************************************************

class AssemblerException(Exception):
	def __init__(self,message):
		Exception.__init__(self)
		self.message = message
		print(message,AssemblerException.LINE)

AssemblerException.LINE = 0
AssemblerException.FILE = ""
