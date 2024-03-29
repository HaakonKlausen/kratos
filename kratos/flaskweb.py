from flask import Flask
from flask import render_template
from flask import request, redirect

import kratoslib

app = Flask(__name__)

@app.context_processor
def utility_oricessor():
    def show_kratos_data(dataname):
        return kratoslib.readKratosDataFromSql(dataname)
    return dict(show_kratos_data=show_kratos_data)

@app.route("/")
def hello_odderhei():
    print("Index")
    return render_template('index.html')

@app.route("/setbereder/<place>/<state>", methods=['POST', 'GET'])
def set_bereder(place, state):
	dataname=place + ".bereder_setting"
	if state=="on":
		value="Alltid På"
	elif state=="off":
		value="Av"
	elif state=="optimize":
		value="Optimaliser"
	else:
		return "Error: illegal state"
	kratoslib.writeKratosDataToSql(dataname, value)
	return redirect("/")

@app.route("/setdevice/<device>/<place>/<state>", methods=['POST', 'GET'])
def set_device(device, place, state):
	dataname=f"{place}.{device}_setting"
	if state=="on":
		value="Alltid På"
	elif state=="off":
		value="Av"
	elif state=="optimize":
		value="Optimaliser"
	else:
		return "Error: illegal state"
	kratoslib.writeKratosDataToSql(dataname, value)
	return redirect("/")