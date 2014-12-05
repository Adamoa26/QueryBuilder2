#!/usr/bin/python
from datetime import datetime
import logs

# Adam Elliott, Nov 2014
# This class is intended to intake a text file (for now) and parse through it.
# Looks for Timestamp, IP, port, and uniqueID and returns them as a list
#Return looks like this: [timdate object, "ip", "port", "uniqueID"]

class emailparser:
	#Default arguments
	def __init__(self, filename):
		self.filename = filename
		self.lines = [None] * 4
		self.date = None
		#Below is a list of known timestamp formats.
		self.formatlist = ["%d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ",
						   "%Y-%m-%d %H:%M:%S.%f GMT"]
		self.stripList = ["\n", "\r", "</ID>"]

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
			message = "There is a date formatting error between the original text and the Email Parser.\nMight want to add the new format to the list."
			logs.exitGracefully(message)
		else:
			return self.date

	def doLines(self, line):
		#This function seeks for the lines with the Timestamp, IP, Port, and Notice ID in the provided email, then runs stripLine() function on them.
		#No return data, but adds info to the self.lines[] array, which is ultimately returned by the class and the doAll() function.
		if line.find("Timestamp") != -1 or line.find("First found") != -1:
			if line.find("Recent") == -1:
				newline = logs.stripLine(line, self.stripList, ":")
				newline = self.timeFormat(newline)
				self.lines[0] = newline
		elif line.find("IP Address") != -1:
			newline = logs.stripLine(line, self.stripList, ":")
			self.lines[1] = newline
		elif line.find("Port") != -1:
			if line.find("<Port>") == -1:
				newline = logs.stripLine(line, self.stripList, ":")
				self.lines[2] = newline
		elif line.find("Reference ID:") != -1 or line.find("Notice ID:") != -1:
			newline = logs.stripLine(line, self.stripList, ":")
			self.lines[3] = newline
		elif line.find("Notice ID #") != -1:
			newline = logs.stripLine(line, self.stripList, "# ")
			self.lines[3] = newline
		elif line.find("<ID>") != -1:
			newline =logs.stripLine(line, self.stripList, ">")
			self.lines[3] = newline

	def readLines(self, filename):
		#This function opens the provided file and runs doLines() on each line.
		try:
			ins = open(filename)
		except IOError:
			message = "Something is wrong with your input file or its location."
			logs.exitGracefully(message)
		else:
			for line in ins:
				self.doLines(line)
			ins.close()

	def doAll(self):
		#This function strings all the other functions required to process through an email
		#Returns a list of the information gleaned from the email.
		self.readLines(self.filename)
		return self.lines
