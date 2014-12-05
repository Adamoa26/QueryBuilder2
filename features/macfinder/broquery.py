from querybuilder.modules import logs
import paramiko
import datetime
class BroQuery:
	'''
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

    --------------------zcat-----------------------
    This method builds a zcat command from file, ip, and port input.

    --------------------sshConnect------------------------
    Uses Paramiko to connect to remote server and execute the given command.
    Returns command output

    --------------------getInfo------------------------
    This method searches for the correct file in which to search, then zgreps for the original IP from the input.
    Outputs the interesting log and	grabs desired values from corresponding fields based on search.



    I want to have a config file where the username/password info is stored locally.
    That will be the next branch of my project, I think.
    '''

	def __init__(self, date, ip, port, uniqID):
		# Constructor
		# This will intake directly from the emailparser class

		self.ip = ip
		self.port = port
		self.timestamp = date
		self.uniqID = uniqID
		self.date = date.strftime('%Y-%m-%d')
		self.hour = date.hour
		self.filepath = "/nsm/bro/logs/" + self.date
		self.DEBUG = True
		self.relevantLogs = [] * 3  #This will be a collection of logs that have interesting info. Will be printed at the end of the program.
		self.client = None

	def newfilepath(self, date):
		self.filepath = "/nsm/bro/logs/" + date
		print self.filepath

	def zcat(self, type, file, ip, port):
		if type == "conn":
			command = "zcat " + file + "| grep " + ip + " | grep " + port
		elif type == "dhcp":
			command = "zcat " + file + "| grep " + ip
		return command

	def sshConnect(self, command):
		try:
			self.client = paramiko.SSHClient()
			self.client.load_system_host_keys()
			self.client.connect('10.218.1.150', username='csirt',
								password='S3cur!ty')  # Connects a shell to specified machine and runs all the relevant commands for the search.
			(sshin, sshout, ssherr) = self.client.exec_command(command)  # Executes command in remote shell.
			return sshout.readlines()  # Returns command output.
		finally:
			self.client.close()  # Finally, it closes the self.client connection.

	def broCommand(self, query, find):
		ans = self.sshConnect(query)
		result = logs.parse(ans, find)
		return result

	def encoder(self, things):
		# This module takes a one-element list of unicode strings and changes them to ascii. Returns Correct format for most applications.
		length = len(things)
		ret = [None] * length
		for i in things:
			pos = things.index(i)
			ret[pos] = i.encode("ascii")
		return ret

	def findfilename(self,type ,hour):
		changedir = "cd " + self.filepath  # builds a find command to find the filename we need.
		find = "find -name " + str(type) + "." + str(hour) + ":**:**-" + str(int(hour) + 1).zfill(2) + ":**:**.log.gz"
		if find == []:
			logs.exitGracefully("Couldn't find filename associated with the hours" + str(hour) + " and " + str(int(hour) + 1).zfill(2))
		else:
			out1 = self.sshConnect(changedir + ";" + find)  # Executing command to find the file
			filename = str(out1[0]).strip()[2:]  # Returning and stripping all the unwanted chars
		return filename

	def getInfo(self, type, info, ip, port, hour, increment = 0):
		log = self.logger(type, info, ip, port, hour)
		if type == "conn" and log[0] == None:
			logs.exitGracefully("Couldn't find a any results for this query.")
		elif type == "dhcp" and log[0] == None:
			if increment < 23:
				increment += 1
				date2 = self.timestamp - datetime.timedelta(hours=increment)
				print date2.strftime("%H")
				self.newfilepath(date2.strftime('%Y-%m-%d'))
				log = self.getInfo("dhcp", info, ip, port, date2.strftime('%H'),increment)
			else:
				logs.exitGracefully("Couldn't find a DHCP lease within 48 hours from the event.")
		elif log[0] != None:
			self.relevantLogs.append(log.pop())  # adds to log list (for output later)
		return log

	def logger(self, type, info, ip, port, hour):
		filename = self.findfilename(type, hour)  # Executing command to find the file
		changedir = "cd " + self.filepath  # builds a find command to find the filename we need.
		zcat = self.zcat(type,filename, ip, port)  # Building the zcat command and searching for the resp_IP
		if info == "resp":
			print "Querying bro_conn for resp IP..."
			out2 = self.sshConnect(changedir + ";" + zcat)  # Connecting to execute commands
		elif info == "internal":
			print "Querying bro_conn for internal IP..."
			out2 = self.sshConnect(changedir + ";" + zcat)  # Connecting to execute commands
		elif info == "mac":
			print "Querying bro_dhcp for Mac Address..."
			out2 = self.sshConnect(changedir + ";" + zcat)
		else:
			logs.exitGracefully("Info type not valid.")
		out3 = self.encoder(out2)
		if out3 == []:
			log = [None]
		else:
			log = logs.parse(out3, info, "BRO", ip)
		return log

	def twrk(self):
		resInfo = self.getInfo("conn", "resp", self.ip, self.port, self.hour)
		intInfo = self.getInfo("conn", "internal", resInfo[0], resInfo[1], self.hour)
		macInfo = self.getInfo("dhcp", "mac", intInfo[0], intInfo[1], self.hour)
		logs.doYouWantMyQuery(self.timestamp, self.uniqID, intInfo[0], macInfo[0], self.relevantLogs)


brotest = BroQuery(datetime.datetime(2014, 11, 21, 14, 46, 30, 700000), '129.15.131.114', '64014', '22298642748')
brotest.twrk()

