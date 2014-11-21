import os.path, sys

from ..features.macfinder import esquery
from emailparser import emailparser

##This script runs esquery and emailparser together to return the results.
# It takes an input of a filepath and checks if the input is a file or directory.
# If it is a directory it runs all the files within the directory
#If it is a file it will run only the specified file.

class esmacfinder:
	#Constructor
	def __init__(self, filepath):
	#Initializes and uses command line input for the filepath.
		self.filepath = filepath

	#Functions
	def run(self):
		dir = os.path.isdir(self.filepath)
		if dir == False:
			email = emailparser(self.filepath)
			parsed = email.doAll()
			query = esquery.EsQuery(parsed[0], parsed[1], parsed[2], parsed[3])
			query.twrk()
		else:
			fileList = os.listdir(self.filepath)
			for file in fileList:
				path = self.filepath + file
				self.checkFile(path)
				email = emailparser(path)
				parsed = email.doAll()
				query = esquery.EsQuery(parsed[0], parsed[1], parsed[2], parsed[3])
				query.twrk()

	def checkFile(self, filename):
		try:
			ins = open(filename)
		except IOError:
			message = "Something is wrong with your input file or its location."
			logs.exitGracefully(message)


class bromacfinder:
	#Constructor
	def __init__(self, filepath):
		self.filepath = filepath

	def run(self):
		print 'hi'
		#Functions
		#def Multiple(self):
		#	dir = os.path.isdir(self.filepath)
		#	if dir == False:
		#		print "Given path is not a directory. Verify that this is the correct path or try running the command with the '-s' argument instead."
		#		sys.exit(0)
		#	else:
		#		fileList = os.listdir(self.filepath)
		#		for file in fileList:
		#			path = self.filepath + file
		#			email = EmailParser(path, "ES")
		#			parsed = email.doAll()
		#			query = ESCopyright(parsed[0],parsed[1],parsed[2], parsed[3])
		#			query.twrk()
		#
		#def Single(self):
		#	dir = os.path.isfile(self.filepath)
		#	if dir == False:
		#		print "Given path is not a path to a single file. Try adding the '-m' argument to your command."
		#		sys.exit(0)
		#	else:
		#		email = EmailParser(self.filepath, "ES")
		#		parsed = email.doAll()
		#		query = ESCopyright(parsed[0],parsed[1],parsed[2], parsed[3])
		#		print query.twrk()

		#esTest = esmacfinder
		#print esTest.__init__()