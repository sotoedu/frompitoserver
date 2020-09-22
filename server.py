from flask import Flask, url_for , request , json , Response , jsonify, render_template
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
  return render_template('index.html')

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
    app.run(host='0.0.0.0',port=5000)
