# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		makeimport.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Builds dictionary file.
#
# ***************************************************************************************
# ***************************************************************************************

import sys,os,re
from dictionary import *

assert len(sys.argv) == 2
stem = sys.argv[1]													# base of lib e.g. standard for standard.lib
xDict = Dictionary()												# blank dictionary

																	# scan labels for import_
for l in [x.strip() for x in open(stem+".lib.vice").readlines() if x.strip() != ""]:
	m = re.match("^al\s+C\:([0-9A-F]+)\s+\_(.*)$",l)
	assert m is not None,"error "+l
	if m.group(2)[:7] == "IMPORT_":									# is it IMPORT_, then decode name and add it.
		name = "".join([chr(int(x,16)) for x in m.group(2)[7:].split("_")])
		procIdent = ProcedureIdentifier(name[:-2],int(m.group(1),16),int(m.group(2)[-1]))
		xDict.addIdentifier(procIdent)
Dict.save(stem+".dict")
#print(xDict.toString())

