from flask import Flask
from flask import render_template
from flask import request

import kratoslib

app = Flask(__name__)

@app.context_processor
def utility_oricessor():
    def show_kratos_data(dataname):
        return kratoslib.readKratosData(dataname)
    return dict(show_kratos_data=show_kratos_data)

@app.route("/")
def hello_odderhei():
    print("Index")
    return render_template('index.html')

@app.route("/setbereder/<place>", methods=['POST', 'GET'])
def set_bereder(place):
    print("Set bereder")
    print(request)
    return "Set Bereder " + place