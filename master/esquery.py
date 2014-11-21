#!/usr/bin/python
import time, sys, datetime
sys.path.append("/home/adam/Documents/ElasticSearch/Automation/modules/")
import logs
#Adam Elliott, Nov 2014
#This class is intended to intake the output from the emailparser class and run a query process in ElasticSearch.
#Input = [timedate object, "ip", "port", "uniqueID"]
#Output = {Mac, InternalIP, all relevant logs} TO THE SCREEN.

class ESQuery:
#Default arguments 
	def __init__(self, date, ip, port, uniqID):
		self.ip = ip
		self.port = port
		self.timestamp = int(logs.dtToTimestamp(date))
		self.uniqID = uniqID
		self.indexDate = [logs.indexDate(str(date.date()))]
		self.DEBUG = False
		self.relevantLogs = []
		
#Functions
	def orig_query(self):
	#This function uses the output from emailparser and builds the first query in ES.
		#Finding the time range in which to search.
		increment = 60000	
		time = logs.increment(self.timestamp, increment, None)
		#Building the search query------------------------------#
		searchQuery = str("id.orig_h:" + str(self.ip) + " AND id.orig_p:" + str(self.port)) 
		query = logs.buildQuery(self.indexDate, searchQuery, time[0], time[1])
		#Sending the query to system Command#
		result = logs.EScommand(query,"id.resp_h\":")
		self.relevantLogs.append(result.pop())
		if self.DEBUG == True:
			print query
		else:
			if result == [None, None, None]:
				message = "\nSearched for: '" + searchQuery + "'  with no result.\n"
				logs.exitGracefully(message)
			else:
				return result
		
	def resp_query(self, ip, port):
	#Need to change the time range for this one.
		increment = 60000
		time = logs.increment(self.timestamp, increment, None)
		searchQuery = str("id.resp_h:" + str(ip) + " AND id.resp_p:" + str(port)) 
		query = logs.buildQuery(self.indexDate, searchQuery, time[0], time[1])
		if self.DEBUG == True:
			print query
		else:
			result = logs.EScommand(query,"\"id.orig_h\":\"10.")
			self.relevantLogs.append(result.pop())
		if result == [None, None, None]:
			message = "\nSearched for: '" + searchQuery + "'  with no result.\n"
			logs.exitGracefully(message)
		else:
			return result
		
	def recursiveDHCP(self, ip, increment):
		#default value for increment
		if increment == None or increment == "":
			increment = 900000 #15 Min
		else:
			increment = increment
		#DHCP query
		time = logs.increment(self.timestamp, increment, None)
		searchQuery = str("type:bro_dhcp AND id.orig_h:" + ip)
		sameday = logs.sameDay(self.timestamp, increment)
		if sameday != True:
			self.indexDate.append(sameday)
		query = logs.buildQuery(self.indexDate, searchQuery, time[0], time[1])
		if self.DEBUG == True:
			print query
		else:
			result = logs.EScommand(query,"mac\":")
			self.relevantLogs.append(result.pop())
			return result
		
		#check result and re-search if == None else return result
		if result[1] == None:
			if increment <= 172800000:
				increment *= 2
				result = self.recursiveDHCP(ip, increment)
			elif increment > 172800000:
				result[1] = "Couldn't find a DHCP lease within 48 hrs."
		return result
		
	def doYouWantMyQuery(self, timestamp, mac, ip):
		print "\n"
		print "----------------------------------------Here is what we found------------------------------------------------"
		print "\n"
		print "For Notice #: " + self.uniqID
		print "\n"
		print "Timestamp: " + str(timestamp)
		print "\n"
		print "Mac Address: " + str(mac)
		print "\n"
		print "Internal ip: " + str(ip)
		print "\n"
		print "Here are the relevant logs:"
		for each in self.relevantLogs:
			print "\n" + each + "\n"
			
	def twrk(self):
		EmailQuery = self.orig_query()
		RespQuery = self.resp_query(EmailQuery[1], EmailQuery[2])
		DhcpQuery = self.recursiveDHCP(RespQuery[1], None)
		self.doYouWantMyQuery(DhcpQuery[0],DhcpQuery[1],DhcpQuery[2])
	
#test = ESQuery(datetime.datetime(2014, 11, 12, 20, 3, 34), '129.15.127.233', '25772', '175361360') 
#test.twrk()