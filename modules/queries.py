import os.path
from querybuilder.features.macfinder import esquery
from querybuilder.features.macfinder import chalkboard
from emailparserII import emailparser
from modules.logs import exitGracefully

'''
# This script runs esquery and emailparser together to return the results.
# It takes an input of a filepath and checks if the input is a file or directory.
# If it is a directory it runs all the files within the directory
# If it is a file it will run only the specified file.
# Does the exact same thing for bro.
'''

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
				if file.endswith(".txt"):
					path = self.filepath + file
					self.checkFile(path)
					email = emailparser(path)
					parsed = email.doAll()
					query = esquery.EsQuery(parsed[0], parsed[1], parsed[2], parsed[3])
					query.twrk()
				else:
					continue

	def checkFile(self, filename):
		try:
			ins = open(filename)
			ins.close()
		except IOError as e:
			message = e
			exitGracefully(message)

class bromacfinder:
	#Constructor
	def __init__(self, filepath):
		self.filepath = filepath

	def run(self):
		dir = os.path.isdir(self.filepath)
		if dir == False:
			email = emailparser(self.filepath)
			parsed = email.doAll()
			query = chalkboard.BroQuery(parsed[0], parsed[1], parsed[2], parsed[3])
			query.twrk()
		else:
			last = self.filepath[-1]
			if last != "/":
				self.filepath = self.filepath + "/"
			fileList = os.listdir(self.filepath)
			for file in fileList:
				if file.endswith('.txt'):
					path = self.filepath + file
					self.checkFile(path)
					print file
					email = emailparser(path)
					parsed = email.doAll()
					query = chalkboard.BroQuery(parsed[0], parsed[1], parsed[2], parsed[3])
					query.twrk()
				else:
					continue

	def checkFile(self, filename):
		try:
			ins = open(filename)
			ins.close()
		except IOError as e:
			message = e
			exitGracefully(message)