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
	def export(self):
		return self.exportID()+":"+self.getName()+":"+str(self.getValue())
	def getTypeName(self):
		assert False
	def exportID(self):
		assert False

class VariableIdentifier(Identifier):
	def getTypeName(self):
		return "Var"
	def exportID(self):
		return "V"

class ConstantIdentifier(Identifier):
	def getTypeName(self):
		return "Con"
	def exportID(self):
		return "C"
		
class ProcedureIdentifier(Identifier):
	def __init__(self,name,value,paramCount):
		Identifier.__init__(self,name,value)
		self.paramCount = paramCount
	def getParameterCount(self):
		return self.paramCount
	def getTypeName(self):
		return "Prc"
	def exportID(self):
		return "P"
	def toString(self):
		return Identifier.toString(self)+"("+str(self.getParameterCount())+")"
	def export(self):
		return Identifier.export(self)+":"+str(self.getParameterCount())

# ***************************************************************************************
#					Dictionary object, holds one set of identifiers
# ***************************************************************************************

class Dictionary(object):
	def __init__(self,fileName = None):
		self.clearIdentifiers()													# erase everything
		if fileName is not None:												# load in if filename
			self.load(fileName)
	#
	#		Load file into current dictionary
	#
	def load(self,fileName):
		for line in [x.strip() for x in open(fileName).readlines() if x.strip() != ""]:
			self.importIdentifier(line)
	#
	#		Export dictionary
	#
	def save(self,fileName):
		h = open(fileName,"w")													# write them all out
		for k in self.identifiers.keys():
			h.write(self.identifiers[k].export()+"\n")
		h.close()
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
	#		Import an identifier
	#
	def importIdentifier(self,txt):
		txt = txt.split(":")													# use : as seperator
		if txt[0] == "V":														# baby factory
			id = VariableIdentifier(txt[1],int(txt[2]))
		elif txt[0] == "C":
			id = ConstantIdentifier(txt[1],int(txt[2]))
		elif txt[0] == "P":
			id = ProcedureIdentifier(txt[1],int(txt[2]),int(txt[3]))
		else:
			assert False,txt+" in dictionary file."
		self.addIdentifier(id)													# add to dictionary.
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
	d.save("demo.dict")
	print()
	d2 = Dictionary()
	d2.load("demo.dict")
	print(d2.toString())
