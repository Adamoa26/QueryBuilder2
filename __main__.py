#!/usr/bin/python
import argparse
from modules.queries import *

parser = argparse.ArgumentParser(prog="QueryBuilder",
							 description="This program builds queries more quickly than the GUI in Kibana")
parser.add_argument("-es", "--elastic",
				help="This will run the query ElasticSearch")
parser.add_argument("-bro", "--brologs",
				help="This option will run the query on Bro Master")

args = parser.parse_args()
print args

if args.elastic:
	filepath = args.elastic
	es = esmacfinder(filepath)
	es.run()
else:
	print "Not a valid entry. Need to specify [WHERE TO SEARCH] [PATH TO FILE OR DIRECTORY]"
#else:
# elif args.brologs
# if args.multiple:
#		filepath = args.multiple
#				#bro = ESCopyright(filepath)
#				#bro.Multiple()
#	elif args.single:
#		filepath = args.single
