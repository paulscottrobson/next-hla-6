# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		makekernel.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st January 2019
#		Purpose :	Builds assembly language file from composite library parts
#
# ***************************************************************************************
# ***************************************************************************************

import sys,os,re

assert len(sys.argv) >= 2,"Insufficient components"
print("Creating composite assembler file")
hOut = open("temp"+os.sep+"__source.asm","w")									# output file
wordCount = 0																	# used to name labels
for libs in sys.argv[1:]:														# work through all libs
	print("\tImporting from library "+libs)										
	for root,dirs,files in os.walk("lib.source"+os.sep+libs):					# work through all files
		for f in files:
			print("\t\t\tImporting file "+f)
			src = open(root+os.sep+f).readlines()
			for l in src:
				if l.startswith("@word"):										# if found @word
					m = re.match("\@word\s*(.*)\((.*)\)\s*$",l.lower())			# break it up
					assert m is not None,"Bad line "+l
					params = [x for x in m.group(2).split(",") if x != ""]		# examine parameters
					label = m.group(1)+":"+str(len(params))
					label = "import_"+("_".join(["{0:02x}".format(ord(x)) for x in label]))
					hOut.write(label+"\n")
					wordCount += 1								
				else:
					hOut.write(l.rstrip()+"\n")
hOut.close()
print("Loaded {0} words".format(wordCount))