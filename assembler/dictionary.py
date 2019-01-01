# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		dictionary.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Dictionary and Identifier classes.
#
# ***************************************************************************************
# ***************************************************************************************

# ***************************************************************************************
#						Identifiers to store in the dictionary
# ***************************************************************************************

class Identifier(object):
	def __init__(self,name,value):
		self.name = name.strip().lower()
		self.value = value
	def getName(self):
		return self.name
	def getValue(self):
		return self.value
	def toString(self):
		return "{0} {1}:{2:x}".format(self.getTypeName(),self.getName(),self.getValue())
	def getTypeName(self):
		assert False

class VariableIdentifier(Identifier):
	def getTypeName(self):
		return "Var"

class ConstantIdentifier(Identifier):
	def getTypeName(self):
		return "Con"
		
class ProcedureIdentifier(Identifier):
	def __init__(self,name,value,paramCount):
		Identifier.__init__(self,name,value)
		self.paramCount = paramCount
	def getParameterCount(self):
		return self.paramCount
	def getTypeName(self):
		return "Prc"
	def toString(self):
		return Identifier.toString(self)+"("+str(self.getParameterCount())+")"

# ***************************************************************************************
#					Dictionary object, holds one set of identifiers
# ***************************************************************************************

class Dictionary(object):
	def __init__(self):
		self.clearIdentifiers()
	#
	#		Clear identifiers
	#
	def clearIdentifiers(self):
		self.identifiers = {}
	#
	#		Add an identifier to the dictionary, testing for collision.
	#
	def addIdentifier(self,ident):
		name = ident.getName()
		if name in self.identifiers:											# check doesn't already exist
			raise AssemblerException("Duplicate identifier "+name)
		self.identifiers[name] = ident											# update dictionary.
	#
	#		Find an identifier
	#
	def find(self,key):
		key = key.strip().lower()
		return None if key not in self.identifiers else self.identifiers[key]
	#
	#		Convert to string
	#
	def toString(self):
		keys = [x for x in self.identifiers.keys()]
		keys.sort()
		return "\n".join([self.identifiers[x].toString() for x in keys])

if __name__ == "__main__":
	d = Dictionary()
	d.addIdentifier(VariableIdentifier("v1",2048))
	d.addIdentifier(ConstantIdentifier("c1",42))
	d.addIdentifier(ProcedureIdentifier("prc1",1048576,3))
	print(d.toString())