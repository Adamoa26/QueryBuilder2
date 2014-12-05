#!/usr/bin/python
import argparse
from modules.queries import *

parser = argparse.ArgumentParser(prog="QueryBuilder",
							 description="This program builds queries more quickly than the GUI in Kibana")
parser.add_argument("-es", "--elastic",
				help="This will run the query ElasticSearch")
parser.add_argument("-bro", "--brologs",
				help="This option will run the query on Bro Master")
parser.add_argument("-conf", "--configure",
				help="This option will run the configuration setup."
				)

args = parser.parse_args()
print args

if args.elastic:
	filepath = args.elastic
	es = esmacfinder(filepath)
	es.run()
elif args.brologs:
	filepath = args.brologs
	bro = bromacfinder(filepath)
	bro.run()
elif args.configure
else:
	print "Not a valid entry. Need to specify [WHERE TO SEARCH] [PATH TO FILE OR DIRECTORY]"

