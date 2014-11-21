#!/usr/bin/python
import paramiko, sys, datetime, getpass

sys.path.append("/home/adam/Documents/ElasticSearch/Automation/modules/")
import logs

#This program will
	#Get info from EmailParser.py
	#Create an SSH connection with (Eventually generalize the resp id)10.218.1.150
	#COMMANDS TO RUN
	#	cd /nsm/bro/logs/YYYY-MM-DD
	#	find -name  conn.03:**:**-04:**:**.log.gz
	#		returns "./conn.03:00:01-04:00:21.log.gz"
	#	zcat conn.03:00:01-04:00:21.log.gz|grep ip |grep port
	#Use this to search through timestamps for the correct log
	#Process log.
	#
	#Use info from Emailparser to cd the correct day's directory and the appropriate hour
	#append log to 
	
####Tried Paramiko, not doing what I want. Trying Fabric now.############
####TO RUN THIS OPTION, YOU WILL NEED TO INSTALL PARAMIKO
# pip install paramiko	

class BroQuery:
	
	def __init__(self, date, ip, port, uniqID):
	#Constructor
		self.ip = ip
		self.port = port
		self.timestamp = logs.dtToTimestamp(date)
		self.uniqID = uniqID
		self.date = date
		self.filepath = "/nsm/bro/logs/" + str(self.date.date())
		self.DEBUG = True
		self.relevantLogs = []
	
	def getFileRange(self, type):
	#This program will search for the specific filename (since not all the files have the same timestamp)
	#Example: 'conn.13:01:45-14:01:11.gz'
	#Only the hour is theoretically 'known,' so we search for 'conn.13:**:**-14:**:**.gz'
	#That is the gist of this method.
		hour = int(self.date.hour)
		if type == conn:
			command = "find -name conn." + str(hour) + ":**:**-" + str(hour + 1) + ":**:**.log.gz"
		elif type == dhcp:
			command = "find -name dhcp." + str(hour) + ":**:**-" + str(hour + 1) + ":**:**.log.gz"
		else:
			exitMessage = "The filetype searched for is not 
			logs.exitGracefully(exitMessage)
		return command
		
	def zcat(self,file):
		command = "zcat "+ file + "|grep "+ self.ip+" |grep "+self.port
		return command
		
	
	#This method prompts user for credentials.
	#right now they are hard coded in. Not using this feature.
	#Probably will move to having a .config file.
	#Pending discussion with team.
	def getSSH(self):
		sshInfo = [None]*3
		sshInfo[0] = str(raw_input("Remote IP address: "))
		sshInfo[1] = str(raw_input("Username: "))
		sshInfo[2] = str(getpass.getpass("Password: "))
		return sshInfo
		
	def ILJ(self, log, search)
		#Indoor LumberJack
		ret = []*2
		if search == "resp":
			ret[0] = log[4]
			ret[1] = log[5]
		elif search == "internal":
			ret[0]=log[2]
			ret[1]=log[3]
		elif search == "mac":
			ret[0] = log[0]
			ret[1] = log[1]
		return ret
		
	#Need a function we can call if there are more than 1 logs found for each search. Just in case.
	#Should be a simple case of the smallest difference between timestamps.
	#------------------------------------------------------------------------------------------#
	#Resp search will yield two log results. Need to find the one with a 10. ip address.
	#Shouldn't need to do anything super-special.
	def SSH(self):
		changeDir = "cd " + self.createFilepath()
		try:
			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.connect("10.218.1.150", username="csirt", password="S3cur!ty")
	#------------------------------------------------------------------------------------#
			findFile = self.getFileRange("conn")
			(sshin1, sshout1, ssherr1) = client.exec_command(changeDir+";"+findFile)
			out = sshout1.readlines()
			fileName = str(out[0]).strip()[2:]
	#------------------------------------------------------------------------------------#		
			zcmd = self.zcat(fileName)
			(sshin2, sshout2, ssherr2) = client.exec_command(changeDir+";"+zcmd)
			out = sshout2.readlines()
			log = str(out[0]).strip().split()
			self.relevantLogs.append(log)
			
		finally:
			client.close()

	def SSHConnect(self, command):
	#Connects a shell to specified machine. 
	#Still need to discuss method with team. 
	#Not used yet, but probably will undergo many changes in the future.
		changeDir = "cd " + self.createFilepath()
		if self.DEBUG == True:
				print changeDir
		try:
			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.connect('10.218.1.150', username='csirt', password='S3cur!ty')
			(sshin1, sshout1, ssherr1) = client.exec_command(changeDir+";"+findFile)
			#--------------------------------------------------------------------------#
			out = sshout1.readlines()
			fileName = str(out[0]).strip()[2:]
			#--------------------------------------------------------------------------#
			zcmd = self.zcat(fileName)
			if self.DEBUG == True:
				print zcmd
			(sshin2, sshout2, ssherr2) = client.exec_command(changeDir+";"+zcmd)
			out = sshout2.readlines()
			log = str(out[0]).strip().split()
			self.relevantLogs.append(log)
			if self.DEBUG == True:
				print log
		finally:
			client.close()	
		
	def findFile(self)
		findFile = self.getFileRange()
			
			
	def doAll(self):
		self.SSH()

test = BroQuery(datetime.datetime(2014, 11, 9, 11, 53, 4, 770000), '129.15.127.238', '56787', '22297915215')
test.doAll()
