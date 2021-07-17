from flask import Flask, Response, jsonify
import json
import pickle
import pandas as pd
import pmdarima as pm
import os
from statsmodels.tsa.arima_model import ARIMA
import time
from datetime import datetime, timedelta
import model
from zipfile import ZipFile

# Definición de la aplicación
app = Flask(__name__)

def predecir_modelo(interval):
    ###############
    # Temperature #
    ###############

    with ZipFile('./model_tem.pickle.zip', 'r') as myzip:
        myzip.extractall('./')

    model_tem = pickle.load( open( './model_tem.pickle', "rb" ) )
    fc_tem, confint_tem = model_tem.predict(n_periods=interval, return_conf_int=True)

    ############
    # Humidity #
    ############

    with ZipFile('./model_hum.pickle.zip', 'r') as myzip:
        myzip.extractall('./')

    model_hum = pickle.load( open( './model_hum.pickle', "rb" ) )
    fc_hum, confint_hum = model_hum.predict(n_periods=interval, return_conf_int=True)

    ##############
    # Prediction #
    ##############

    dates = pd.date_range((datetime.now() + timedelta(hours=3)).replace(second=0, microsecond=0), periods=interval, freq='H')
    pred = []

    for date, tem, hum in zip(dates, fc_tem, fc_hum):
        dt = time.mktime(date.timetuple())
        pred.append(
            {
                'hour': datetime.utcfromtimestamp(dt).strftime('%d-%m %H:%M'),
                'temp': tem,
                'hum': hum
            }
        )
    return pred

@app.route("/servicio/v1/prediccion/24horas", methods=['GET'])
def hours_24():
    response = Response(json.dumps(predecir_modelo(24)), status=200)
    response.headers['Content-Type']='application/json'
    return response

@app.route("/servicio/v1/prediccion/48horas", methods=['GET'])
def hours_48():
    response = Response(json.dumps(predecir_modelo(48)), status=200)
    response.headers['Content-Type']='application/json'
    return response

@app.route("/servicio/v1/prediccion/72horas", methods=['GET'])
def hours_72():
    response = Response(json.dumps(predecir_modelo(72)), status=200)
    response.headers['Content-Type']='application/json'
    return response
