from common.connector import db_connector
from common import util

import json
import requests

with open('common/conf.json') as conf_json:
	conf = json.load(conf_json)

result=db_connector.query("select * from event")
rows=util.fetch_all_json(result)

for row in rows:
	print(row)
	print(type(row))

def extractEvent(url, ics_list):
	evt_list=[]
	# loop

	# file open

	# generate data (event name, dt:start~end, location)

	# remove file

	return evt_list