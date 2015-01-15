from queryobject import *
from querybuilder.modules import logs
import datetime


class BroQuery:
	"""
	This class will:
		# Intake info from EmailParser.py
		# Create an SSH connection with (Eventually generalize the resp id)10.218.1.150
		# Use info from Emailparser to cd the correct day's directory and the appropriate hour
		# COMMANDS TO RUN
		#	cd /nsm/bro/logs/YYYY-MM-DD
		#	find -name  conn.03:**:**-04:**:**.log.gz
		#	zcat conn.03:00:01-04:00:21.log.gz|grep ip |grep port
		# Use this to search through timestamps for the correct log
		# Append log to self.relevantlogs for output later
		# Process log.
	Repeat to find id.resp_h, id.resp_p, internal IP and port, and mac address.
	Process depends on PARAMIKO but is listed as a dependency within the package.
	"""

	def __init__(self, date, ip, port, uniqID):
		"""
		# Constructor
		# This will intake directly from the emailparser class
		"""

		self.ip = ip
		self.port = port
		self.timestamp = date
		self.uniqID = uniqID
		self.date = date.strftime('%Y-%m-%d')
		self.hour = date.hour
		self.filepath = "/nsm/bro/logs/" + self.date
		self.DEBUG = True
		self.relevantLogs = [] * 3  # This will be a collection of logs that have interesting info. Will be printed at/
		#  the end of the program.
		self.ssh = SSHConnection()
		self.ERROR = False
		self.interestingLogs = [] * 3

	def getbrolog(self, doc, search, ip):
		"""
		# This function will take the input of a system command, split it by lines, and search each line for /
		the 'search' input.
		# Once it finds the 'search,' it will return the log itself.
		# Intended to search through a query output and ensure only a single and correct log is chosen to be processed /
		later on.
		:returns
		[log]
		"""
		newtimestamp = (self.timestamp - datetime.datetime(1970, 1, 1)).total_seconds()
		if doc is None:
			print "No records found at all."
			return None
		else:
			log1 = None
			timediff = 3600
			if search == "resp" or search == "internal":
				for log in doc:
					if search == "internal":
						if log.internal() is False:
							continue
					delta = log.timeDifference(newtimestamp)
					if delta < timediff:
						timediff = delta
						log1 = log
					else:
						continue
				if timediff > 15 and timediff < 3600:
					print "No record exists within 15 seconds of the reported event."
					print "The closest matching record is off by " + str(timediff) + " seconds."
					return None
				elif log1 is None:
					print "No matching records found."
					return None
			elif search == "mac":
				for log in doc:
					if log.find(search, ip):
						log1 = log
						break
					else:
						continue
		return log1

	def clencher(self, target, timestamp, ip, port):
		query = Query(target, timestamp, ip, port)
		returns = query.doAll()
		log = self.getbrolog(returns, target, ip)
		if log is None:
			return None
		else:
			self.interestingLogs.append(log.readabletimestamp())
			return log

	def twrk(self):
		resplog = self.clencher("resp", self.timestamp, self.ip, self.port)
		if resplog is None:
			print "No result for the resp_h. Ending search.\n\n"
			return None
		intlog = self.clencher("internal", self.timestamp, resplog.get_resp_h(), resplog.get_resp_p())
		if intlog is None:
			print "No result for the internal IP. Ending search."
			print "Internal: " + resplog.get_orig_h() + ":" + resplog.get_orig_p() + "\n\n"
			return None
		maclog = self.clencher("mac", self.timestamp, intlog.get_orig_h(), intlog.get_orig_p())
		if maclog is None:
			print "No result for MAC. Ending search."
			print "Internal: " + intlog.get_orig_h() + "\n\n"
			return None
		logs.doYouWantMyQuery(self.timestamp, self.uniqID, maclog.get_mac(), maclog.get_assigned_ip(), self.interestingLogs)

#---------------------------------------Test----------------------------------------#
#brotest = BroQuery(datetime.datetime(2014, 12, 06, 01, 39, 31, 21), "129.15.127.236", "27186", "22299499862")
#brotest.twrk()
