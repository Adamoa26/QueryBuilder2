import sys, os.path
sys.path.append("/home/adam/Documents/ElasticSearch/Automation/branches/Copyright/Currently Working")
from EmailParser import EmailParser
from ESQuery import ESQuery

class ESCopyright:
#Constructor
	def __init__(self, filepath):
		self.filepath = filepath
	
#Functions
	def multiple(self):
		dir = os.path.isdir(self.filepath)
		if dir == False:
			print "Given path is not a directory. Verify that this is the correct path or try running the command with the '-s' argument instead."
			sys.exit(0)
		else:
			fileList = os.listdir(self.filepath)
			for file in fileList:
				path = self.filepath + file
				email = EmailParser(path, "ES")
				parsed = email.doAll()
				query = ESQuery(parsed[0],parsed[1],parsed[2], parsed[3])
				query.twrk()
	def single(self):
		dir = os.path.isfile(self.filepath)
		if dir == False:
			print "Given path is not a path to a single file. Try adding the '-m' argument to your command."
			sys.exit(0)
		else:
			email = EmailParser(self.filepath, "ES")
			parsed = email.doAll()
			query = ESQuery(parsed[0],parsed[1],parsed[2], parsed[3])
			print query.twrk()
			
class BROCopyright:
#Constructor
	def __init__(self, filepath):
		self.filepath = filepath
	
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
	
#esTest = ESCopyright("/home/adam/Documents/ElasticSearch/Automation/HEAD/TestFiles/Email1.txt")
#esTest.single()