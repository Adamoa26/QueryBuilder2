import os.path
from querybuilder.features.macfinder import esquery
from querybuilder.features.macfinder import chalkboard
from emailparserII import parsechooser
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
		self.searchinfo = []

	#Functions
	def run(self):
		dir = os.path.isdir(self.filepath)
		if dir == False:
			email = parsechooser(self.filepath)
			parsed = email.execute()
			for info in parsed:
				query = esquery.EsQuery(info[0], info[1], info[2], info[3])
				query.twrk()
		else:
			fileList = os.listdir(self.filepath)
			for file in fileList:
				if file.endswith(".txt"):
					path = self.filepath + file
					self.checkFile(path)
					email = parsechooser(self.filepath)
					parsed = email.execute()
					for info in parsed:
						query = esquery.EsQuery(info[0], info[1], info[2], info[3])
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
		self.searchinfo = []

	def run(self):
		dir = os.path.isdir(self.filepath)
		if dir == False:
			email = parsechooser(self.filepath)
			parsed = email.execute()
			for info in parsed:
				query = chalkboard.BroQuery(info[0], info[1], info[2], info[3])
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
					email = parsechooser(self.filepath)
					parsed = email.execute()
					for info in parsed:
						query = chalkboard.BroQuery(info[0], info[1], info[2], info[3])
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