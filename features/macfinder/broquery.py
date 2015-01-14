from querybuilder.modules import logs
import paramiko, sshcommands
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
    '''

	def __init__(self, date, ip, port, uniqID):
		'''
		# Constructor
		# This will intake directly from the emailparser class
		'''

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
		self.ERROR = False


	def newfilepath(self, date):
		self.filepath = "/nsm/bro/logs/" + date

	def zcat(self, type, file, ip, port):
		'''
		This method builds a zcat command from file, ip, and port input.
		:param type:
		:param file:
		:param ip:
		:param port:
		:return:
		'''
		if type == "conn":
			command = "zcat " + file + "| grep -w " + ip + " | grep -w " + port
		elif type == "dhcp":
			command = "zcat " + file + "| grep -w " + ip
		return command

	def sshConnect(self, command):
		'''
		Uses Paramiko to connect to remote server and execute the given command.
    	Returns command output

		:param command:
		:return:
		'''
		try:
			self.client = paramiko.SSHClient()
			self.client.load_system_host_keys()
			sshinfo = logs.getsshinfo()
			self.client.connect(sshinfo[0], username=sshinfo[1], password=sshinfo[2])  # Connects a shell to specified machine and runs all the relevant commands for the search.
			(sshin, sshout, ssherr) = self.client.exec_command(command)  # Executes command in remote shell.
			return sshout.readlines()  # Returns command output.
		except paramiko.SSHException as e:
			logs.exitGracefully(e)
		finally:
			self.client.close()  # Finally, it closes the self.client connection.

	def broCommand(self, query, find):
		'''
		:param query:
		:param find:
		:return:
		'''
		ans = self.sshConnect(query)
		result = logs.parse(ans, find)
		return result

	def encoder(self, things):
		'''
		:param things:
		:return:
		'''

		length = len(things)
		ret = [None] * length
		for i in things:
			pos = things.index(i)
			ret[pos] = i.encode("ascii")
		return ret

	def findfilename(self, type, hour):
		'''
		:return:
		[filename,(s)]
		'''
		filename = []
		changedir = "cd " + self.filepath  # builds a find command to find the filename we need.
		if hour == 23:
			find = "find -name " + str(type) + "." + str(hour).zfill(2) + ":**:**-00:**:**.log.gz"
		else:
			find = "find -name " + str(type) + "." + str(hour).zfill(2) + ":**:**-" + str(int(hour) + 1).zfill(2) + ":**:**.log.gz"
		out1 = self.sshConnect(changedir + ";" + find)  # Executing command to find the file
		if out1 == []:
			find = "find -name \"" + str(type) + "." + str(hour).zfill(2) + ":**:**-" + str(hour).zfill(2) + ":**:**.log.gz\""
			out2 = self.sshConnect(changedir + ";" + find)
			if out2 == []:
				self.errorFlag("Couldn't find filename associated with the hours " + str(hour) + " and " + str(int(hour) + 1).zfill(2))
				return None
			else:
				for name in out2:
					filename.append(str(name).strip()[2:])
		else:
			for name in out1:
				filename.append(str(name).strip()[2:])
		return filename

	def getInfo(self, type, info, ip, port, hour, increment = 0):
		'''
		This method searches for the correct file in which to search, then zgreps for the original IP from the input.
    	Outputs the interesting log and	grabs desired values from corresponding fields based on search.

		:param type:
		:param info:
		:param ip:
		:param port:
		:param hour:
		:param increment:
		:return:
		'''
		log = self.logger(type, info, ip, port, hour)
		if type == "conn" and log == None:
			self.errorFlag("\nCouldn't find a any results for this query in bro_conn.\n")
			log = "None"
		elif type == "dhcp" and log == None:
			if increment < 23:
				increment += 1
				date2 = self.timestamp - datetime.timedelta(hours=increment)
				self.newfilepath(date2.strftime('%Y-%m-%d'))
				log = self.getInfo("dhcp", info, ip, port, date2.strftime('%H'),increment)
			else:
				self.errorFlag("Couldn't find a DHCP lease within 48 hours from the event.")
				log =  "None"
		elif log[0] != None:
			self.relevantLogs.append(log.pop())  # adds to log list (for output later)
		return log

	def logger(self, type, info, ip, port, hour):
		'''
		:param type:
		:param info:
		:param ip:
		:param port:
		:param hour:
		:return:
		'''
		filename = self.findfilename(type, hour)  # Executing command to find the file
		changedir = "cd " + self.filepath  # builds a find command to find the filename we need.
		for name in filename:
			if name == None:
				continue
			else:
				zcat = self.zcat(type,name, ip, port)  # Building the zcat command and searching for the resp_IP
				if info == "resp":
					out2 = self.sshConnect(changedir + ";" + zcat)  # Connecting to execute commands
				elif info == "internal":
					out2 = self.sshConnect(changedir + ";" + zcat)  # Connecting to execute commands
				elif info == "mac":
					out2 = self.sshConnect(changedir + ";" + zcat)
				else:
					self.errorFlag("Info type not valid.")
					return None

				out3 = self.encoder(out2)
				if out3 == []:
					message = "No returns for queried " + type + "."
					self.errorFlag(message)
					return None
				else:
					time = logs.dtToTimestamp(self.timestamp)/1000
					log = logs.parse(out3, info, "BRO", ip, time )
				return log

	def twrk(self):
		'''

		:return:
		'''
		if self.ERROR == False:
			resInfo = self.getInfo("conn", "resp", self.ip, self.port, self.hour)
		else:
			return None
		if self.ERROR == False:
			intInfo = self.getInfo("conn", "internal", resInfo[0], resInfo[1], self.hour)
		else:
			return None
		if self.ERROR == False:
			macInfo = self.getInfo("dhcp", "mac", intInfo[0], intInfo[1], self.hour)
		if self.ERROR == False:
			logs.doYouWantMyQuery(self.uniqID, intInfo[0], macInfo[0], self.relevantLogs)
		else:
			return None


#---------------------------------------Test----------------------------------------#
#brotest = BroQuery(datetime.datetime(2014, 11, 21, 14, 46, 30, 700000), '129.15.131.114', '64014', '22298642748')
#brotest.twrk()