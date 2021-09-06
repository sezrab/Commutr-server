from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return "Hello, World!"

def result():
    print(request.form['foo']) # should display 'bar'
    return 'Received !' # response to your request.

app.run(host='0.0.0.0', port=80)
