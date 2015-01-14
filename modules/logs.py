import os, sys, datetime, re

	# Adam Elliott, Nov 2014
	# This module represents generalized functions that are central to the operation of this project package.
	# Each has been generalized in order to potentially extend their functionality.


def exitGracefully(message):
	'''
	# Method takes a message, prints it to the screen and exits the program.
	# Intended as a debugging-errorcatching thing.
	:returns
	None
	'''
	print message
	print "Exiting program."
	sys.exit(0)
	
def dtToTimestamp(date):
	'''
	# Converts a datetime object into a timestamp in milliseconds.
	:returns
	timestamp == int(##################)
	'''
	timestamp = int((date - datetime.datetime(1970,1,1)).total_seconds()*1000)
	return timestamp
	
def indexDate(date):
	'''
	# This function intakes a "YYYY-MM-DD" date
	# Returns a "YYYY.MM.DD"
	# Intended to return a value that matches ElasticSearch/Bro index names.
	:returns
	"YYYY.MM.DD"
	'''
	date1 = str(date)
	date2 = date1.split()
	date3 = date2[0]
	newDate = date3.replace("-",".")
	return newDate
	
def stripLine(line, replaceChars, splitChar):
	'''
	# Intakes "String", [Array of Chars to replace], "a char on which to split the string"
	# Intended to take a string such as "IP Address: 1.1.1.1" or "Notice ID: 2221019191"
	# and return only the value:
	:returns
	"1.1.1.1", "2221019191"
	'''
	newline = None
	i1 = line.find(splitChar) + 1
	i2 = len(line)
	line = line[i1:i2]
	for char in replaceChars:
		newline = line.replace(char, "")
	return newline.strip()

def sameDay(datetime1, increment):
	'''
	# This function takes two timedate functions and checks if they are the same day.
	# If they are the same day, it returns "True".
	# If not, it formats the second day.
	:returns
	False
	----or----
	"YYYY-MM-DD"
	'''
	datetime2 = (int(datetime1) - increment)/1000
	datetime1 /= 1000
	date1 = datetime.date.fromtimestamp(datetime1)
	date2 = datetime.date.fromtimestamp(datetime2)
	date3 = date1.strftime("%Y-%m-%d")
	date4 = date2.strftime("%Y-%m-%d")
	
	if date3 == date4:
		return True
	else:
		return date4

def comparetime(line, time):
	'''
	Compares two timestamps and returns the difference if it is greater than zero.
	Otherwise it returns 'false.'

	:param line: Log in which the right IP was found.
	:param time: Timestamp of even that was called.
	:return:
	int || False
	'''
	newline = line.split()
	t1 = newline[0]
	delta = time - float(t1)
	if abs(delta) >= 0:
		return abs(delta)
	else:
		return False


def getlog(doc, search, ip, timestamp = None):
	'''
	# This function will take the input of a system command, split it by lines, and search each line for the 'search' input.
	# Once it finds the 'search,' it will return the log itself.
	# Intended to search through a query output and ensure only a single and correct log is chosen to be processed later on.
	:returns
	[log]
	'''
	i = None
	change = 0
	if isinstance(doc, list) == False: 	#Built in variable. Checks to see if 'doc' is a 'list' object-type.
		resp = doc.split()
	else:
		resp = doc
	if search == "internal":
		for line in resp:
			if line == None:
				continue
			if re.search(r"10\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",line) != None:
				if timestamp != None:
					delta = comparetime(line, timestamp)
					if delta != False and change == 0:
						change = delta
						i = resp.index(line)
					elif delta != False and delta < change:
						change = delta
						i = resp.index(line)
					else:
						continue
				else:
					i = resp.index(line)
					break
	else:
		for line in resp:
			if line == None:
				continue
			if line.find(ip):
				if timestamp != None:
					delta = comparetime(line, timestamp)
					if delta != False and change == 0:
						change = delta
						i = resp.index(line)
					elif delta != False and delta < change:
						change = delta
						i = resp.index(line)
					else:
						continue
				else:
					i = resp.index(line)
					break
	if i == None or i > 15:
		print "Couldn't find a result for " + search + " address."
		return None
	return resp[i]

def brosearch(doc, search, ip):
	'''
	# Searches bro output logs for the correct log.
	# Returns only a single log instead of two or more(which could potentially change).
	:returns
	[BroLog]
	'''
	newdoc = str(doc.strip())
	respond = re.split('\s|\t', newdoc)
	ret = [None] * 2
	if search == "resp":
		for i in respond:
			if i.find(ip) != -1:
				i = respond.index(ip)
				if i == 2:
					ret[0] = respond[4]
					ret[1] = respond[5]
				else:
					continue
			else:
				continue
	elif search == "internal":
		ret[0] = respond[2]
		ret[1] = respond[3]
	elif search == "mac":
		ret[0] = respond[6]
		ret[1] = respond[0]
	return ret

def searchlog(doc, search):
	'''
	# This method will take a log from the getLog() method, split the log on commas, and search for the 'search' in addition to the "Timestamp"
	# Will reuturn an array of [The timestamp, search, search+1]
	# Intended to be used to grab ips and ports of RESP and ORIG, MAC from getLog() output.
	:returns
	[log,(s)]
	'''
	newdoc = str(doc.strip())
	searchMat = re.split(',', newdoc)
	respond = [None]*3
	for line in searchMat:
		if line.find("\"@timestamp\":") != -1:
			i = searchMat.index(line)
			respond[0] = stripLine(searchMat[i],["\""], ":")
		elif line.find(search) != -1:
			i = searchMat.index(line)
			respond[1] = stripLine(line,["\""], ":")
			respond[2] = stripLine(searchMat[i+1],["\""], ":")	
			break
		else:
			continue
	return respond

def parse(doc, search, type, ip = None, timestamp = None):
	'''
	#This function intakes a doc=<system command return>, search=<desired string to find> and passes them through getLog() and searchLog() functions.
	# Returns an array of information. Typically [timestamp, IP, port, log].
	# Intended for the log to be appended to a master list of relevant logs.
	# The other elements will be processed together.
	:returns
	[timestamp, ip/mac, port]
	'''
	if type == "ES":
		log = getlog(doc, search, ip)
		if log == None:
			return None
		else:
			loginfo = searchlog(log, search)
			loginfo.append(log)
	elif type == "BRO":
		log = getlog(doc, search, ip, timestamp)
		if log == None:
			return None
		else:
			loginfo = brosearch(log, search, ip)
			loginfo.append(log)
	else:
		loginfo = None
	return loginfo

def EScommand(query, find):
	'''
	# This function will build a system command and run it, returning the query.
	# Intakes query=<desired command> and find = <what to search for in the return>
	# Intended to run a query, input the result and 'find' into the parse() function and return the results.
	:returns
	[timestamp, ip/mac, port]
	'''
	f = os.popen(query)
	ans = f.read()
	result = parse(ans, find, "ES")
	return result
	
def buildQuery(indexDate, query, t1, t2):
	'''
	# This is the cookie cutter for building a query.
	# indexDate = [YYYY.MM.DD,<any additional days in which to search>]
	# query = <"ES compatible search string">
	# t1 = <timestamp> --From
	# t2 = <timestamp> --To
	:returns
	 Query string for EScommand.
	'''
	query = """curl -XGET 'http://10.218.1.178:9200/bro-""" + str(",".join(set(indexDate))) + """/_search?pretty' -d '{
  "query": {
    "filtered": {
      "query": {
        "bool": {
          "should": [
            {
              "query_string": {
                "query": \"""" + query + """\"
              }
            }
          ]
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "from": """ + str(t1) + """,
                  "to": """ + str(t2) + """
                }
              }
            }
          ]
        }
      }
    }
  },
  "highlight": {
    "fields": {},
    "fragment_size": 2147483647,
    "pre_tags": [
      "@start-highlight@"
    ],
    "post_tags": [
      "@end-highlight@"
    ]
  },
  "size": 500,
  "sort": [
    {
      "_score": {
        "order": "desc",
        "ignore_unmapped": true
      }
    }
  ]
}'"""
	return query
	
def increment(timestamp, increment, arg1=None):
	'''
	# This Function is intended to return two timestamps seperated by a specified range.
	# Intended to help increment searches automatically.
	# returns an array of two timestamps.
	:returns
	["from","to"]
	'''
	time = [None]*2
	timestamp = int(timestamp)
	if arg1 == None:
		#arg1 = "None" returns [timestamp - increment, timestamp + increment]
		time[0]= timestamp - increment
		time[1] = timestamp + increment
	elif arg1 == "From":
		#arg1 = "From" returns [timestamp - increment, timestamp]
		time[0] = timestamp - increment 
		time[1] = timestamp
	elif arg1 == "To":
		#arg1 = "To"  returns [timestamp, timestamp + increment]
		time[0] = timestamp
		time[1] = timestamp + increment
	else:
		print "The variable \"arg1\" has no valid argument."
	return time
	
def doYouWantMyQuery(origtime, uniqueid, mac, ip, logs):
	'''
	# This is the ouput command that prints all the data in a readable format to the screen.
	# Pretty self-explanatory, I think.
	:returns
	None
	'''
	print "#----------------------------------------Here is what we found---------------------------------------------#"
	print "Original Timestamp: " + str(origtime)
	print "For Notice #: " + str(uniqueid)
	print "Internal ip: " + str(ip)
	print "Mac Address: " + str(mac.replace(":", ""))
	print "\n"
	print "Here are the relevant logs:"
	print "\n"
	for each in logs:
		print each
	print "#-------------------------------------------------END------------------------------------------------------#"
	print "\n"
