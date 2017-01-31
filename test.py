from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util
import time

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
    print(calendar.calendarName + " " + calendar.calendarId + " " + calendar.cTag)

##최초 동기화 
eventList = calendars[0].getAllEvent()
for event in eventList:
    print (event.eventId + " " + event.eTag)

## 아래 정보를 db에 저장 
"""
ACCOUNT 
    host_name           -> hostname
    user_id             -> userId 
    user_pw             -> 추후 BASE64로 처리 
    home_set_cal_url    -> principal.getHomeSet().homesetUrl

CALENDAR 
    host_name           -> hostname
    user_id             -> userId 
    calendar_id         -> homeset.getCalendars()[n].calendarId     (선택된 캘린더들 전부다)
    calendar_url        -> homeset.getCalendars()[n].calendarUrl
    calendar_name       -> homeset.getCalendars()[n].calendarName
    cTag                -> homeset.getCalendars()[n].cTag      

EVENT 
    host_name           -> hostname
    user_id             -> userId 
    calendar_id         -> homeset.getCalendars()[n].calendarId     (선택된 캘린더들 전부다)
    eventId             -> calendar.getAllEVent()[i].eventId
    eventUrl            -> calendar.getAllEVent()[i].eventUrl
    eTag                -> calendar.getAllEVent()[i].eTag

"""

"""

## 주기적 동기화 

#client 객체에 db에서 데이터를 불러와 넣어줌 
client = (
    CaldavClient(
        hostname,
        userId,
        userPw
    ).setPrincipal("principal_url")   #db 에서 로드 
    .setHomeSet("home_set_cal_url")  #db 에서 로드 
    .setCalendars("calendarList")       #db에서 로드해서 list calendar object 로 삽입
)
list calendar object 만드는법 
calendarList = []
for i in db.inter()
    calendar = Calendar(
        calendarUrl = calendarUrl,
        calendarName = calendarName,
        cTag = cTag
    )
    calendarList.append(calendar)

"""


"""test code """

calendarList=[]
calendarList.append(
    CaldavClient.Calendar(
        calendarUrl = "",
        calendarName = "",
        cTag = ""
    )
)

client = (
    CaldavClient(
        hostname,
        userId,
        userPw
    ).setPrincipal("https://caldav.calendar.naver.com:443/principals/users/jspiner")   #db 에서 로드 
    .setHomeSet("https://caldav.calendar.naver.com:443/principals/users/jspiner/")  #db 에서 로드 
    .setCalendars(calendarList)       #db에서 로드해서 list calendar object 로 삽입
)


while True:
    print("start sync")

    time.sleep(10)