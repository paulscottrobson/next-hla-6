# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		makeimport.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Builds dictionary file from encoded labels.
#
# ***************************************************************************************
# ***************************************************************************************

import sys,os,re
from dictionary import *
from labels import *

assert len(sys.argv) == 2
stem = sys.argv[1]													# base of lib e.g. standard for standard.lib
xDict = Dictionary()												# blank dictionary
labels = ZasmLabelExtractor(stem+".lst").getLabels()				# get labels

for l in labels.keys():												# scan labels for import_
	if l[:7] == "import_":									# is it IMPORT_, then decode name and add it.
		name = "".join([chr(int(x,16)) for x in l[7:].split("_")])
		procIdent = ProcedureIdentifier(name[:-2],labels[l],name[-1])
		xDict.addIdentifier(procIdent)
xDict.save(stem+".dict")
#print(xDict.toString())

