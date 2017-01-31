from common.connector import db_connector
from common import util

import json
import requests
import os

def extractEvent(homeset_cal_id, cal_id, ics_list):
	evt_list=[]
	path=os.getcwd()+"/" # Declare for generate ics file path
	# Get auth
	res = db_connector.query("select user_base64 from account where host_name=%s",(homeset_cal_id,))
	rows = util.fetch_all_json(res)
	if rows[0]['user_base64'] is None:
		return #handle error message
	Auth="Basic "+rows[0]['user_base64']
	# loop 
	""" """
	for ics in ics_list:
		# file open
		url_resp = requests.request("GET",homeset_cal_id+cal_id+ics,headers={"Depth":"1","Authorization":Auth})
		ics_data = str(url_resp.text)
		#print(ics_data.findall('SUM'))
		#print(ics_data.find("SUMMARY:"))
		#print(ics_data)
		# generate data (event name, dt:start~end, location)
		
		# remove file
		# print()
	return evt_list

#with open('common/conf.json') as conf_json:
#	conf = json.load(conf_json)
def printAllEvent():
	result=db_connector.query("select * from event")
	rows=util.fetch_all_json(result)

	for row in rows:
		print(row)
		print(type(row))

def initInsertCalendars(client, principal, homeset, calendar_list):
	#print(client.hostname, client.auth[0], client.auth[1], homeset.homesetUrl)
	result = db_connector.query("INSERT INTO account VALUES (%s, %s, %s, %s)",(client.hostname, client.auth[0], client.auth[1], homeset.homesetUrl))

	for calendar in calendar_list:
		result2 = db_connector.query("INSERT INTO calendar VALUES (%s, %s, %s, %s, %s)",(client.hostname, client.auth[0], calendar.calendarId, calendar.calendarName, calendar.cTag))

		evt_list = calendar.getAllEvent()

		for evt in evt_list:
			result3 = db_connector.query("INSERT INTO event (host_name, user_id, calendar_id, event_id, e_tag) VALUES (%s, %s, %s, %s, %s)",(client.hostname, client.auth[0], calendar.calendarId, evt.eventId, evt.eTag))
"""	

homeset_cal_id="https://p58-caldav.icloud.com/10836055664/calendars/"
cal_id="home/"

ics_ls=[]
ics_ls.append("159EBF61-05FB-457F-BAE2-5C4A2EE85322.ics")
ics_ls.append("80D1290F-1647-48E4-A85B-A5746188BA80.ics")
extractEvent(homeset_cal_id, cal_id,ics_ls)
"""