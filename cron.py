from caldavclient import CaldavClient
import json 
import time 
from caldavclient import util
import time
import db_manager



while True:
    calendarList = db_manager.selectAllCalendar()
    print(calendarList)

    time.sleep(10)