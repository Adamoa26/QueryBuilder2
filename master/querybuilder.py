#!/usr/bin/python
import sys, argparse

from Queries import ESCopyright

parser = argparse.ArgumentParser(prog="QueryBuilder", description="This program builds queries more quickly than the GUI in Kibana")#replace the name here too!
parser.add_argument("-cp", "--copyright", 
					help="This option builds and executes a series of queries built do deal with copyright notification emails.\n By default this option requires a filepath to a single file.",
					action="store_true")
parser.add_argument("-es", "--elastic",
					help="This will run the query ElasticSearch",
					action="store_true")
parser.add_argument("-bro", "--brologs",
					help="This option will run the query on Bro Master",
					action="store_true")
parser.add_argument("-m", "--multiple", 
					help = "This option requires a filepath to a directory.\n It will process all '.txt' files within the given directory. ")
parser.add_argument("-s", "--single",
					help = "Requires full filepath including filename. Will run query on supplied file ONLY.")
					
args = parser.parse_args()

if args.copyright:
	if args.elastic:
		if args.multiple:
			filepath = args.multiple
			es = ESCopyright(filepath)
			es.multiple()
		elif args.single: 
			filepath = args.single
			es = ESCopyright(filepath)
			es.single()
	else:
		print "Not a valid entry. Need to specify [CASE TYPE] [SEARCH TYPE] [FILE TYPE -s or -M]"
else:
	#elif args.brologs
	#	if args.multiple:
	#		filepath = args.multiple
	#				#bro = ESCopyright(filepath)
	#				#bro.Multiple()
	#	elif args.single: 
	#		filepath = args.single		
	
