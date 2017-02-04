from flask import Flask, render_template
from flask import Response
from flask import request
from caldavclient import CaldavClient
import db_manager
app = Flask(__name__)



@app.route('/')
def routeMain():
    return 'hello'

@app.route('/login')
def routeLogin():

    return render_template('login.html')

@app.route('/calendar', methods=['POST','GET'])
def routeCalendar():
    print("calendar")
    hostname = request.form['hostname']
    userId = request.form['userId']
    userPw = request.form['userPw']

    client = CaldavClient(
        hostname,
        userId,
        userPw
    )
    principal = client.getPrincipal()
    homeset = principal.getHomeSet()
    calendars = homeset.getCalendars()

    calendarList = ""
    for calendar in calendars:
#        print(calendar.calendarName + " " + calendar.calendarUrl + " " + calendar.cTag)
        calendarList+= "<input type=checkbox name=chk_info value='%s'>%s" % (calendar.calendarUrl, calendar.calendarName) + "</br>"

    db_manager.initInsertCalendars(client, principal, homeset, calendars)
    

    return render_template('calendar.html', calendarList = calendars)



if __name__ == "__main__":
	app.run()
