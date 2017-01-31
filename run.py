from flask import Flask, render_template
from flask import Response
from flask import request

app = Flask(__name__)



@app.route('/')
def routeMain():
    return 'hello'

@app.route('/login')
def routeLogin():

    return render_template('login.html')

@app.route('/calendar', methods=['POST','GET'])
def routeCalendar():
    print(request.form)
    hostname = request.form['hostname']
    userId = request.form['userId']
    userPw = request.form['userPw']

    

    return render_template('calendar.html')



if __name__ == "__main__":
	app.run()