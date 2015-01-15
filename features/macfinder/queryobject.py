from sshcommands import *
from datetime import timedelta
from querybuilder.features.macfinder.logobject import ConnLog, DHCPLog
from querybuilder.modules.logs import dtToTimestamp


class Query:
	def __init__(self, searchtarget, timestamp, ip, port):
		self.ip = ip
		self.port = port
		self.timestamp = timestamp
		self.date = timestamp.strftime('%Y-%m-%d')
		self.hour = timestamp.hour
		self.filepath = "/nsm/bro/logs/" + self.date
		self.searchtarget = searchtarget
		self.ssh = SSHConnection()
		self.ERROR = False
		self.j = 1

		if searchtarget == "mac":
			self.logtype = "dhcp"
		elif searchtarget == "resp" or "internal":
			self.logtype = "conn"
		else:
			self.ERROR = True
			print "Invalid SearchTarget"

	def ErrorFlag(self, message):
		self.ERROR = True
		message = message

	def newfilepath(self, date):
		self.filepath = "/nsm/bro/logs/" + date

	def findfilename(self):
		"""
		:return:
		[filename,(s)]
		"""
		filename = []
		changedir = "cd " + self.filepath  # builds a find command to find the filename we need.
		if self.hour == 23:
			find = "find -name " + str(self.logtype) + "." + str(self.hour).zfill(2) #+ ":**:**-00:**:**.log.gz"
		else:
			find = "find " + str(self.logtype) + "." + str(self.hour).zfill(2) + "*" #":**:**-" + str(int(self.hour) + 1).zfill(2) + ":**:**.log.gz"
		out1 = self.ssh.SSHConnect(changedir + ";" + find)  # Executing command to find the file
		if out1 is None:
			find = "find -name \"" + str(self.logtype) + "." + str(self.hour).zfill(2) + ":**:**-" + str(self.hour).zfill(2) + ":**:**.log.gz\""
			out2 = self.ssh.SSHConnect(changedir + ";" + find)
			if out2 is None:
				self.ErrorFlag("Couldn't find filename associated with the hours " + str(self.hour) + " and " + str(int(self.hour) + 1).zfill(2))
				return None
			else:
				for name in out2:
					filename.append(str(name).strip()[2:])
		else:
			for name in out1:
				filename.append(str(name).strip()[0:])
		return filename


	#"| awk \'{if($1 ~ /" + timestamp + "/ && $3 == \"" + self.ip + "\" && $4 == \"" + self.port + "\") print $0 }\'"
	#"| awk \'{if($3 == \"" + self.ip + "\" && $4 == \"" + self.port + "\") print $0 }\'"

	def zcat(self, filename):
		timestamp =str(dtToTimestamp(self.timestamp)/1000)[:-2]
		command = None
		if self.searchtarget == "resp":
			command = "zcat " + filename + "| awk \'{if($1 ~ /" + timestamp + "/ && $3 == \"" + self.ip + "\" && $4 == \"" + self.port + "\") print $0 }\'"
		elif self.searchtarget == "internal":
			command = "zcat " + filename + "| awk \'{if($1 ~ /" + timestamp + "/ && $5 == \"" + self.ip + "\" && $6 == \"" + self.port + "\") print $0 }\'"
		elif self.searchtarget == "mac":
			command = "zcat " + filename + "| grep -w " + self.ip
		return command

	def encoder(self, things):
		"""
		:param things:
		:return:
		"""
		if not things:
			ret = None
		else:
			length = len(things)
			ret = [None]*length
			for i in things:
				pos = things.index(i)
				ret[pos] = i.encode("ascii")
		return ret

	def logger(self):
		logs = []
		filename = self.findfilename()  # Executing command to find the file
		if self.ERROR:
			return None
		else:
			changedir = "cd " + self.filepath  # builds a find command to find the filename we need.
			for name in filename:
				if name is None:
					continue
				else:
					zcat = self.zcat(name)  # Building the zcat command and searching for the resp_IP
					out2 = self.ssh.SSHConnect(changedir + ";" + zcat)  # Connecting to execute commands
					out3 = self.encoder(out2)
					if out3 is not None:
						for i in out3:
							if self.logtype == "conn" and i is not None:
								log = ConnLog(i)
								logs.append(log)
							elif self.logtype == "dhcp" and i is not None:
								log = DHCPLog(i)
								logs.append(log)
					elif not out3:
						if self.logtype == "dhcp" and self.j < 48:
							self.timestamp = self.timestamp - timedelta(hours=self.j)
							self.date = self.timestamp.strftime('%Y-%m-%d')
							self.hour = self.timestamp.hour
							self.j += 1
							logs = self.logger()
						elif self.logtype == "dhcp" and self.j >= 48:
							message = "Cant' find a DHCP log within 48 hrs of the event."
							self.ErrorFlag(message)
						elif self.logtype == "conn":
							message = ""
							self.ErrorFlag(message)
			return logs

	def doAll(self):
		arrayoflogs = self.logger()
		return arrayoflogs

#---------------------------------------------Tests-----------------------------------------------------------#
#Resp Test
#test1 = Query("resp", datetime.datetime(2014, 12, 06, 01, 39, 31, 21), "129.15.127.236", "27186", "22299499862")
#hello = test1.doAll()
#print hello

#Internal Test
#test2 = Query("internal", datetime.datetime(2014, 12, 06, 01, 39, 31, 21), "184.173.108.125", "48352", "22299499862")
#print test2.doAll()

#Mac Test
#test3 = Query("mac", datetime.datetime(2014, 12, 06, 01, 39, 31, 21), "10.194.66.126", "42954", "22299499862")
#print test3.doAll()
