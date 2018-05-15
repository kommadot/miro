from flask import Flask, request, make_response
from flaskext.mysql import MySQL
import json
import uuid

from datetime import datetime
import time
import random
import xml.etree.ElementTree as ET
import urllib2

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123123'
app.config['MYSQL_DATABASE_DB'] = 'miro'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

token = dict()
sendData = dict()
subwayApiKey = '766255464e61736437386245474c64'

data = dict()

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


@app.route("/user/test", methods=['POST'])
def test():
        if request.method == 'POST': #show message, test ok

           userSession = request.form['session']
           if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

           num = random.randint(1, 100)

           for key in token:
             if token[key] == userSession:
                UserID = key
                con = mysql.connect()
                cursor = con.cursor()
                query = "INSERT INTO test VALUES ('%s')" % (UserID, receiverID, contents, num)
                cursor.execute(query)
                con.commit()
                cursor.close()
                sendData = {'result': 'success'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

        else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res


@app.route("/user", methods=['POST', '', 'PUT', 'DELETE'])
def user():
   if request.method == 'POST':         #sign up
      loginID = request.form['ID']
      loginPW = request.form['PW']
      if loginID is None or loginPW is None:
         sendData = {'what':'login', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res
      else:
         con = mysql.connect()
         cursor = con.cursor()
         query = "INSERT INTO user VALUES ('%s', '%s')" % (loginID, loginPW)
         cursor.execute(query)
         con.commit()
         cursor.close()
         sendData = {'result': 'success'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res

   if request.method == 'PUT':      #sign in
      loginID = request.form['ID']
      loginPW = request.form['PW']
      if loginID == None or loginPW == None:
         sendData = {'what':'login', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res

      con = mysql.connect()
      cursor = con.cursor()
      query = "SELECT ID FROM user WHERE ID='%s' AND PW='%s'" % (loginID, loginPW)
      cursor.execute(query)

      if not cursor.fetchall():
         cursor.close()
         sendData = {'what':'login', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res
      else: #
         cursor.close()
         token[loginID] = str(uuid.uuid4())
         data = dict(zip(('username', 'result', 'session'), (loginID, 'success', token[loginID])))
         json_data = json.dumps(data, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         UserID = loginID
         return res

   if request.method == 'DELETE':   #logout
      userSession = request.form['session']
      if userSession == None:
         return 'session bad request!'

      for key in token:
         if token[key] == userSession:
            del token[key]
            data = dict(zip(('result', 'a'), ('success', 'a')))
            json_data = json.dumps(data, ensure_ascii=False) #json form change
            res = make_response(json_data) #form change
            res.headers['Content-Type'] = 'application/json' #add header
            return res

      data = dict(zip(('result', 'a'), ('fail', 'a')))
      json_data = json.dumps(data, ensure_ascii=False)
      res = make_response(json_data)
      res.headers['Content-Type'] = 'application/json'
      return res

   else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res


@app.route("/user/message", methods=['POST', '', 'PUT', 'DELETE'])
def message():
    if request.method == 'POST':         #send message to other
        receiverID = request.form['receiverID']
        contents = request.form['contents']
        userSession = request.form['session']
        nowDateTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

        for key in token:
            if token[key] == userSession:
                UserID = key
                con = mysql.connect()
                cursor = con.cursor()
                query = "INSERT INTO message VALUES ('%s', '%s', '%s', null, '%s')" % (UserID, receiverID, contents, nowDateTime)
                cursor.execute(query)
                con.commit()
                cursor.close()
                sendData = {'result': 'success'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

    if request.method == 'DELETE':   #delete message **my fucntion**
       num = request.form['num']
       num = int(num)
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "DELETE FROM message WHERE receiverID='%s' AND No=%d" % (UserID, num)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res

@app.route("/user/message/1", methods=['POST'])
def message_show():
        if request.method == 'POST': #show message

           userSession = request.form['session']
           if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

           for key in token:
                if token[key] == userSession:
                   UserID = key
                   temp = []
                   con = mysql.connect()
                   cursor = con.cursor()
                   query = "SELECT * FROM message WHERE receiverID='%s'" % (UserID)
                   cursor.execute(query)
                   row_headers=[x[0] for x in cursor.description] #this will extract row headers
                   rv = cursor.fetchall()
                   for result in rv:
                       temp.append(dict(zip(row_headers,result)))

                   data['message'] = temp
                   json_data = json.dumps(data, cls=DatetimeEncoder, ensure_ascii=False)
                   res = make_response(json_data) #form change
                   res.headers['Content-Type'] = 'application/json' #add header
                   return res

        else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res


@app.route("/user/schedule", methods=['POST', '', 'PUT', 'DELETE'])
def schedule():
    if request.method == 'POST':         #add schedule
        contents = request.form['contents']
        endTime = request.form['time']  #2018-05-27 07:00:24
        userSession = request.form['session']
        if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

        for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "INSERT INTO schedule VALUES ('%s', '%s', null,'%s')" % (UserID, contents, endTime)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    if request.method == 'PUT': #update schedule
       num = request.form['num']
       contents = request.form['contents']
       num = int(num)
       endTime = request.form['time']  #2018-05-27 07:00:24
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "UPDATE schedule SET contents = '%s', date_time = '%s' WHERE ID = '%s' AND No = '%s'" % (contents, endTime, UserID, num)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    if request.method == 'DELETE':   #delete schedule
       num = request.form['num']
       num = int(num)
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "DELETE FROM schedule WHERE ID='%s' AND No=%d" % (UserID, num)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res

@app.route("/user/schedule/1", methods=['POST'])
def schedule_show():
    if request.method == 'POST':         #show schedule test ok
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
           if token[key] == userSession:
               UserID = key
               nowDateTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
               con = mysql.connect()
               cursor = con.cursor()
               query = "SELECT * FROM schedule WHERE ID='%s' AND date_time BETWEEN '%s' AND ('%s' + interval 4 day)" % (UserID, nowDateTime, nowDateTime)
               cursor.execute(query)
               temp=[]

               row_headers=[x[0] for x in cursor.description] #this will extract row headers
               rv = cursor.fetchall()
               for result in rv:
                   temp.append(dict(zip(row_headers,result)))

               data['schedule'] = temp
               json_data = json.dumps(data, cls=DatetimeEncoder, ensure_ascii=False)
               res = make_response(json_data) #form change
               res.headers['Content-Type'] = 'application/json' #add header
               return res

    else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res



@app.route("/user/market", methods=['POST', '', 'PUT', 'DELETE'])
def market():
    if request.method == 'POST':         #add market item
        title = request.form['title']
        contents = request.form['contents']
        link = request.form['link']
        madeBy = request.form['madeBy']
        num = request.form['num']
        num = int(num)
        userSession = request.form['session']
        if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

        for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "INSERT INTO market VALUES ('%s', '%s','%s','%s')" % (num, title, contents, link, madeBy)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    if request.method == 'PUT': #update market
       title = request.form['title']
       contents = request.form['contents']
       link = request.form['link']
       madeBy = request.form['madeBy']
       num = request.form['num']
       num = int(num)
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "UPDATE marekt SET title = '%s', contents = '%s', link = '%s' WHERE madeBy = '%s' AND No = '%s'" % (title, contents, link, UserID, num)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    if request.method == 'DELETE':   #delete market item
       num = request.form['num']
       num = int(num)
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
            if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "DELETE FROM market WHERE madeBy='%s' AND No=%d" % (UserID, num)
               cursor.execute(query)
               con.commit()
               cursor.close()
               sendData = {'result': 'success'}
               json_data = json.dumps(sendData, ensure_ascii=False)
               res = make_response(json_data)
               res.headers['Content-Type'] = 'application/json'
               return res

    else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res

@app.route("/user/market/1", methods=['POST'])   #show market list inform
def market_show():
    if request.method == 'POST':         #show market item
       userSession = request.form['session']

       if userSession == None:
                sendData = {'what':'session', 'result': 'fail'}
                json_data = json.dumps(sendData, ensure_ascii=False)
                res = make_response(json_data)
                res.headers['Content-Type'] = 'application/json'
                return res

       for key in token:
           if token[key] == userSession:
               UserID = key
               con = mysql.connect()
               cursor = con.cursor()
               query = "SELECT * FROM market"
               cursor.execute(query)
               temp=[]

               row_headers=[x[0] for x in cursor.description] #this will extract row headers
               rv = cursor.fetchall()
               for result in rv:
                   temp.append(dict(zip(row_headers,result)))

               data['market'] = temp
               json_data = json.dumps(data, cls=DatetimeEncoder, ensure_ascii=False)
               res = make_response(json_data) #form change
               res.headers['Content-Type'] = 'application/json' #add header
               return res

    else:
         sendData = {'what':'request', 'result': 'fail'}
         json_data = json.dumps(sendData, ensure_ascii=False)
         res = make_response(json_data)
         res.headers['Content-Type'] = 'application/json'
         return res


@app.route("/user/subway/1", methods=['POST']) #add subway inform
def add():
    if request.method == 'POST':
       houseToStartingH= request.form['time11']
       houseToStartingM= request.form['time12']
       houseToStartingS= request.form['time13']

       starting = request.form['station1']
       ending = request.form['station2']

       endingToDestinationH= request.form['time21']
       endingToDestinationM= request.form['time22']
       endingToDestinationS= request.form['time23']

       week = request.form['week']

       houseToStarting = houseToStartingH + ":"+ houseToStartingM + ":" + houseToStartingS
       endingToDestination = endingToDestinationH + ":" + endingToDestinationM + ":" + endingToDestinationS

       if week == None or starting == None or  houseToStartingH == None or  houseToStartingM == None or  houseToStartingS == None or ending == None or endingToDestinationH == None  or endingToDestinationM == None or endingToDestinationS == None:
          return 'plz fill in the blank'

       con = mysql.connect()
       cursor = con.cursor()
       query = "INSERT INTO subway  VALUES ('%s', '%s', '%s', '%s', '%s')" % (houseToStarting, starting, ending, endingToDestination, week)
       cursor.execute(query)
       con.commit()
       cursor.close()
       return 'add success! %s %s' % (starting, ending)

@app.route("/user/subway/2", methods=[''])   #show subway inform
def show():
    if request.method == 'POST':
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT station1 FROM subway WHERE week='%s'" % (week)
        cursor.execute(query)

        if not cursor.fetchall():
           cursor.close()
           return 'no subway'

@app.route("/user/subway/3", methods=['POST'])   #show subway inform
def subper(sub) :
    url = 'http://swopenapi.seoul.go.kr/api/subway/{subwayApiKey}}/json/realtimeStationArrival/0/5/{station}}'
    tree = ET.ElementTree(file=urllib2.urlopen(url))
    root = tree.root()
    return root



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug=True)