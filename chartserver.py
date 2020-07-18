from flask import Flask, url_for , request , json , Response , jsonify, render_template
import logging
import datetime
import time
import pymongo
from flask_googlecharts import GoogleCharts
from flask_googlecharts import BarChart
from bson.json_util import dumps
from flask_cors import CORS

my_chart = BarChart("my_chart")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["smartfarmDB"]
mycol = mydb["mysensor"]

app = Flask(__name__)
CORS(app)
charts = GoogleCharts(app)
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/graph', methods = ['GET'])
def api_graph():

    return render_template('showchart.html')

@app.route('/graphlist', methods = ['GET'])
def api_graphlist():
    cursor = mycol.find().sort('date', -1)

    # ISODate("1902-01-31T00:00:00.000Z")

    if cursor:
        data_list = []
        count = 0

        for item in cursor:
            json_str = item['date']
            count = count + 1

            value_list = [count,item['value'], item['value']+3]
            data_list.append(value_list)

        list = dumps(data_list)

        print(list)

        return list

        # return render_template('showchart.html', list=list)


@app.route('/aagraph', methods = ['GET'])
def api_aagraph():
    list = mycol.find().sort('date', -1)
    # data = {}

    # for item in list:
    #     value = {"value": int(item['value'])}
    #     data.update(value)

    # data = {'Task' : 'Hours per Day',  'value' : 11, 'date' : 2}




    #data = {'Task' : 'Hours per Day', 'Work' : 11, 'Eat' : 2, 'Commute' : 2, 'Watching TV' : 2, 'Sleeping' : 7}

    print(list)
    return render_template('showchart.html', list=list)


    #return render_template('tableplace.html', emp_list = emp_list)


@app.route('/showlist', methods = ['GET'])
def api_showlist():

    return render_template('table.html')

@app.route('/updatelist', methods = ['GET'])
def api_updatelist():
    emp_list = mycol.find().sort('date', -1)

    return render_template('tableplace.html', emp_list = emp_list)


@app.route('/messages', methods = ['POST'])
def api_message():

#    print ("!!!message!!!")
#    print(request.data)
#    print(json.dumps(request.data))

    if request.headers['Content-Type'] == 'text/plain':
        print ("text/plain")
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        print("Json type", json.dumps(request.json))

        dateTime = datetime.datetime.utcnow()
        data = { "date": dateTime }

        raw = json.dumps(request.json)
        result = json.loads(raw)

        result.update(data)
        saveDB = mycol.insert_one(result)
        print(saveDB)
        myclient.close()

        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"


@app.route('/helloworld', methods = ['GET'])
def api_helloworld():
    data = {
        'hello'  : 'world',
        'number' : 3
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost'

    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/hellolog', methods = ['GET'])
def api_hellolog():
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('screaming bloody murder!')

    return "check your logs\n"


if __name__ == '__main__':
    app.run(host='localhost',port=3000)
