from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util

with open('key.json') as json_data:
    d = json.load(json_data)
    userId = d['naver']['id']
    userPw = d['naver']['pw']

#hostname = "https://caldav.icloud.com"
hostname = "https://caldav.calendar.naver.com/principals/users/jspiner"

## 기본 client 생성
client = CaldavClient(
    hostname,
    userId,
    userPw
)

principal = client.getPrincipal()
homeset = principal.getHomeSet()

calendars = homeset.getCalendars()

for calendar in calendars:
    print(calendar.calendarName + " " + calendar.calendarUrl + " " + calendar.cTag)

eventList = calendars[0].getAllEvent()
for event in eventList:
    print (event.eTag)