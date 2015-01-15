#!/usr/bin/python
from datetime import datetime
import logs

# Adam Elliott, Nov 2014
# This class is intended to intake a text file (for now) and parse through it.
# Looks for Timestamp, IP, port, and uniqueID and returns them as a list
#Return looks like this: [timedate object, "ip", "port", "uniqueID"]
class parsechooser:
	#Default Args
	def __init__(self, filename):
		self.filename = filename

	def execute(self):
		#This function opens the provided file and runs doLines() on each line.
		try:
			ins = open(self.filename)
		except IOError:
			message = "Something is wrong with your input file or its location."
			logs.exitGracefully(message)
		else:
			firstline = str(ins.readlines())
			ins.close()
			if firstline.find("Greetings,") != -1:
				email = isacparser(self.filename)
				email.readLines()
				list = email.formatinfo()
				return list
			else:
				email = emailparser(self.filename)
				list = email.doAll()
				return list


class emailparser:
	#Default arguments
	def __init__(self, filename):
		self.filename = filename
		self.lines = [None] * 4 	#[Timestamp, IP, Port, Unique ID]
		self.date = None
		self.tslist = ["Timestamp","First found","Recent"] # try to find a workaround to use this.
		self.iplist = ["IP Address"]
		self.portlist = ["Port"]
		self.uidlist = ["Reference ID","Notice ID","ID", "CASE"]
		self.punctlist = [":", "# ", "<"]
				#Below is a list of known timestamp formats.
							#06 Oct 2014 19:53:34 GMT
		self.formatlist = ["%d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ",
						   "%Y-%m-%d %H:%M:%S.%f GMT", "%d %b %Y %H:%M:%S GMT"]
		self.stripList = ["\n", "\r", "</ID>", "</Port>", "</TimeStamp>", "</IP_Address>"]
		self.informationlist = []

	def findIP(self, line):
		for search in self.iplist:
			if line.find(search) != -1:
				newline = logs.stripLine(line, self.stripList, ":")
				self.lines[1] = newline

	def findTS(self, line):
		for search in self.tslist:
			if line.find(search) != -1:
				newline = logs.stripLine(line, self.stripList, ":")
				newline = self.timeFormat(newline)
				self.lines[0] = newline

	def findUID(self, line):
		for search in self.uidlist:
			if line.find(search) != -1:
				for punct in self.punctlist:
					if line.find(punct) != -1:
						newline = logs.stripLine(line, self.stripList, punct)
						if "@" in newline:
							continue
						else:
							self.lines[3] = newline

	def findPort(self, line):
		for search in self.portlist:
			if line.find(search) != -1:
				newline = logs.stripLine(line, self.stripList, ":")
				self.lines[2] = newline

	#functions
	def timeFormat(self, timestamp):
		#Normalizes time format
		#For/Except structure tries given list of known timestamp types
		#Returns as a timedate object.
		for dateFormat in self.formatlist:
			try:
				self.date = datetime.strptime(timestamp, dateFormat)
			except ValueError:
				self.date = None
			else:
				break
		if self.date == None:
			message = "There is a date formatting error between the original text and the Email Parser.\n" \
                      "Might want to add the new format to the list."
			logs.exitGracefully(message)
		else:
			return self.date

	def readLines(self, filename):
		#This function opens the provided file and runs doLines() on each line.
		try:
			ins = open(filename)
		except IOError:
			message = "Something is wrong with your input file or its location."
			logs.exitGracefully(message)
		else:
			for line in ins:
				if self.lines[0] is None:
					self.findTS(line)
				if self.lines[1] is None:
					self.findIP(line)
				if self.lines[2] is None:
					self.findPort(line)
				if self.lines[3] is None:
					self.findUID(line)
			ins.close()

	def doAll(self):
		#This function strings all the other functions required to process through an email
		#Returns a list of the information gleaned from the email.
		self.readLines(self.filename)
		self.informationlist.append(self.lines)
		return self.informationlist



class isacparser:
	def __init__(self, filename):
		self.filename = filename
		self.lines = [None] * 4 	#[Timestamp, IP, Port, Unique ID]
		self.records = []
		self.formatlist = ["%d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ",
						   "%Y-%m-%d %H:%M:%S.%f GMT", "%d %b %Y %H:%M:%S GMT"]
		self.informationlist = []

	def timeFormat(self, timestamp):
		date = None
		#Normalizes time format
		#For/Except structure tries given list of known timestamp types
		#Returns as a timedate object.
		for dateFormat in self.formatlist:
			try:
				date = datetime.strptime(timestamp, dateFormat)
			except ValueError:
				date = None
			else:
				break
		if date == None:
			message = "There is a date formatting error between the original text and the Email Parser.\n" \
                      "Might want to add the new format to the list."
			logs.exitGracefully(message)
		else:
			return date

	def readLines(self):
		#This function opens the provided file and runs doLines() on each line.
		try:
			ins = open(self.filename)
		except IOError:
			message = "Something is wrong with your input file or its location."
			logs.exitGracefully(message)
		else:
			trip = False
			for line in ins:
				if trip == False:
					if line.find("+") != -1:
						trip = True
				elif trip == True:
					if line.find("+") != -1:
						trip = False
						break
					else:
						newline = line.split("|")
						for i in newline:
							if i == "" or '':
								newline.remove(i)
								continue
							index = newline.index(i)
							newline[index] = i.strip()
						self.records.append(newline)
			ins.close()
		return self.records

	def formatinfo(self):
		for record in self.records:
			information = [None]*4
			information[0] = self.timeFormat(record[3])
			information[1] = record[2]
			information[2] = record[4]
			information[3] = str(record[0].strip())
			self.informationlist.append(information)
		return self.informationlist

#Testing#
#test = parsechooser('/home/adam/Documents/ElasticSearch/Copyright_Emails/October_2014/Batch2/1-224925637.txt')
#email = test.execute()
#for i in email:
#	print i

#test2 = parsechooser('/home/adam/Documents/ElasticSearch/Ren-Isac_Emails/Email1.txt')
#email = test2.execute()
#for i in email:
#	print i

#test3 = isacparser('/home/adam/Documents/ElasticSearch/Ren-Isac_Emails/Email2.txt')
#test3.readLines()
#print test3.formatinfo()

#test4 = isacparser('/home/adam/Documents/ElasticSearch/Ren-Isac_Emails/Email3.txt')
#test4.readLines()

#test5 = isacparser('/home/adam/Documents/ElasticSearch/Ren-Isac_Emails/Email4.txt')
#test5.readLines()

#test6 = isacparser('/home/adam/Documents/ElasticSearch/Ren-Isac_Emails/Email5.txt')
#test6.readLines()