from common.connector import db_connector
from common import util

import json
import requests
import os

# Update Calendar (C tag, E tag, and All change things about event)
def updateCalendar(homeset_cal_id, cal_id, add_ics_list, update_ics_list, delete_ics_list):
	# Get auth
	res = db_connector.query("select user_base64,user_id,host_name from account where host_name=%s",(homeset_cal_id,))
	rows = util.fetch_all_json(res)
	if rows[0]['user_base64'] is None:
		return #handle error message
	user_id = rows[0]['user_id']
	host_name = rows[0]['host_name']
	auth="Basic "+rows[0]['user_base64']
	req_headers={"Depth":"1","Authorization":auth}

	# Add event
	if add_ics_list is not None:
		addEvent(homeset_cal_id,cal_id, user_id, add_ics_list, req_headers)
	# Update event (Overwrite)
	if update_ics_list is not None:
		updateEvent(homeset_cal_id, cal_id, update_ics_list, req_headers)
	# Delete event
	if delete_ics_list is not None:
		deleteEvent(delete_ics_list)

def addEvent(homeset_cal_id,cal_id, user_id, ics_ls, req_headers):
	for ics in ics_list:
		# Unpacking event contents from extracting .ics
		evt_name, evt_start_dt, evt_end_dt, evt_loc = icsParser(homeset_cal_id, cal_id, ics, req_headers)

		# DB Insert
		# INSERT INTO event (host_name, user_id, calendar_id, event_id, e_tag) VALUES (%s, %s, %s, %s, %s)",(client.hostname, client.auth[0], calendar.calendarId, evt.eventId, evt.eTag))
		""" HOW INPUT E TAG INFO AFTER GET?
		TO-DO: FIX CALENDAR, EVENT CLASS

		if evt_loc is not None:
			#evt_query = db_connector.query("INSERT INTO event VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)",(homeset_cal_id, user_id, cal_id, ics, )
			pass
		else:
			evt_query = db_connector.query("UPDATE event SET event_name=%s,location=null,start_dt=%s,end_dt=%s WHERE host_name=%s and user_id=%s and calendar_id=%s and event_id=%s",(evt_name, evt_start_dt, evt_end_dt, host_name, user_id, cal_id, ics))
		"""

def deleteEvent(ics_list):
	for ics in ics_list:
		db_connector.query("DELETE FROM event WHERE event_id=%s",(ics,))


def updateEvent(homeset_cal_id, cal_id, ics_list, req_headers):
	# Update C tag in calendar table & E tag in event table
	# HOW INPUT E TAG ABOUT EACH EVENT AFTER GET? (SAME CASE, C TAG)
	# TO-DO: FIX CALENDAR, EVENT CLASS

	# Update Event contents
	for ics in ics_list:

		# Unpacking event contents
		evt_name, evt_start_dt, evt_end_dt, evt_loc = icsParser(homeset_cal_id, cal_id, ics, req_headers)

		# DB Update
		if evt_loc is not None:
			evt_query = db_connector.query("UPDATE event SET event_name=%s,location=%s,start_dt=%s,end_dt=%s WHERE host_name=%s and user_id=%s and calendar_id=%s and event_id=%s",(evt_name, evt_loc, evt_start_dt, evt_end_dt, host_name, user_id, cal_id, ics))
		else:
			evt_query = db_connector.query("UPDATE event SET event_name=%s,location=null,start_dt=%s,end_dt=%s WHERE host_name=%s and user_id=%s and calendar_id=%s and event_id=%s",(evt_name, evt_start_dt, evt_end_dt, host_name, user_id, cal_id, ics))

# Extract event name, start/end time, location from requesting ics file
def icsParser(homeset_cal_id, cal_id, evt_id, req_headers):
	# file open
	url_resp = requests.request("GET",homeset_cal_id+cal_id+ics,headers=req_headers)
	ics_data = str(url_resp.text)
	
	# Get Basic Info
	evt_name = ics_data[ics_data.find("SUMMARY:")+8:ics_data.find("DTSTART;")]
	evt_start_dt = ics_data[ics_data.find("DTSTART;")+8:ics_data.find("DTSTAMP:")]
	evt_end_dt = ics_data[ics_data.find("DTEND;")+6:ics_data.find("SUMMARY:")]
	
	# Convert dt from ICS to DB format
	evt_start_dt = dtConverter(evt_start_dt)
	evt_end_dt = dtConverter(evt_end_dt)

	# Duplicated data remove from ics file
	evt_loc = None
	tmp_ics_data = ics_data.replace("-LOCATION","") # Except X-LIC-LOCATION id column
	if tmp_ics_data.find("LOCATION:") is not -1:
		evt_loc = tmp_ics_data[tmp_ics_data.find("LOCATION:")+9:tmp_ics_data.find("SEQUENCE:")]

	return evt_name, evt_start_dt, evt_end_dt, evt_loc
	  


def dtConverter(dt_ics):
	# Mysql Date time format :  1000-01-01 00:00:00
	# ICS Date time format : TZID=Asia/Seoul:20170117T090000
	
	dummy1, dt_ics_splited = dt_ics.split(":")
	dt_ics_date, dt_ics_time = dt_ics_splited.split("T")
	dt_db_date = dt_ics_date[0:4]+"-"+dt_ics_date[4:6]+"-"+dt_ics_date[6:8]
	dt_db_time = dt_ics_time[0:2]+":"+dt_ics_time[2:4]+":"+dt_ics_time[4:6]

	return dt_db_date+" "+dt_db_time

def getAllEvent():
	result=db_connector.query("select * from event")
	rows=util.fetch_all_json(result)

	for row in rows:
		print(row)
		print(type(row))

	return rows

def initInsertCalendars(client, principal, homeset, calendar_list):
	#print(client.hostname, client.auth[0], client.auth[1], homeset.homesetUrl)
	result = db_connector.query("INSERT INTO account VALUES (%s, %s, %s, %s)",(client.hostname, client.auth[0], client.auth[1], homeset.homesetUrl))

	for calendar in calendar_list:
		result2 = db_connector.query("INSERT INTO calendar VALUES (%s, %s, %s, %s, %s)",(client.hostname, client.auth[0], calendar.calendarId, calendar.calendarName, calendar.cTag))

		evt_list = calendar.getAllEvent()
		req_headers={"Depth":"1","Authorization":client.auth[0]}
		
		for evt in evt_list:
			if evt.eventId.find(".ics"):
				evt_name, evt_start_dt, evt_end_dt, evt_loc = icsParser(client.hostname, calendar.calendarId, evt.eventId, req_headers)
				result3 = db_connector.query("INSERT INTO event VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(client.hostname, client.auth[0], calendar.calendarId, evt.eventId, evt_name, evt_start_dt, evt_end_dt, evt_loc, evt.eTag))

""" MOUDULE TESTER for extractEvent 
homeset_cal_id="https://p58-caldav.icloud.com/10836055664/calendars/"
cal_id="home/"
user_id="line_plus@naver.com"
user_bs="bGluZV9wbHVzQG5hdmVyLmNvbTpRV0UwOThxd2U="
ics_ls=[]
ics_ls.append("159EBF61-05FB-457F-BAE2-5C4A2EE85322.ics")
ics_ls.append("80D1290F-1647-48E4-A85B-A5746188BA80.ics")

addEvent(homeset_cal_id,cal_id, user_id, ics_ls)
extractEvent(homeset_cal_id, cal_id,ics_ls)
#deleteEvent(ics_ls)
"""