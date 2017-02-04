from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util
import time
import db_manager



while True:
    accountList = db_manager.selectAllAccount()

    for account in accountList:
        calendars = db_manager.selectCalendars(account['host_name'], account['user_id'])
        calendarList = []
        for calendar in calendars:
            calendarList.append(
                CaldavClient.Calendar(
                    calendarUrl = calendar['calendar_url'],
                    calendarName = calendar['calendar_name'],
                    cTag = calendar['c_tag']
                )
            )
        

        client = (
            CaldavClient(
                account['host_name'],
                account['user_id'],
                account['user_base64'],
            ).setPrincipal(account['home_set_cal_url'])   #db 에서 로드 
            .setHomeSet(account['home_set_cal_url'])  #db 에서 로드 
            .setCalendars(calendarList)       #db에서 로드해서 list calendar object 로 삽입
        )

        for calendar in calendarList:
            if calendar.isChanged():
                print("something changed")
                
                oldEventList = util.eventRowToList( #db에서 이전 event리스트들을 불러옴 
                    db_manager.selectEvents(
                        account['host_name'], 
                        account['user_id'], 
                        calendar.calendarId
                    )
                )
                newEventList = calendar.updateAllEvent()


                eventDiff = util.diffEvent(oldEventList, newEventList)

                #각각 추가삭제변경된 일정은 eventDiff.added(), removed(), changed()에서 리스트로 가져올 수 있음.
                print(eventDiff.added())
                print(eventDiff.removed())
                if len(eventDiff.added()) != 0:
                    print("일정이 추가되었다.")
                if len(eventDiff.removed()) !=0:
                    print("일정이 삭제되었다.")
                if len(eventDiff.changed()) !=0:
                    print("일정이 변경되었다.") 


    time.sleep(10)