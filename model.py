from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import pymongo
import pickle
from datetime import datetime, timedelta
import time
from zipfile import ZipFile
import zipfile


class Model:
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://1234:CC@cluster0.ff0rm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        datos = client.CCAirflow['SanFrancisco']
        datos = pd.DataFrame(list(datos.find()))

        # Dropping missing values
        datos = datos.dropna()

        ###############
        # Temperature #
        ###############

        model_tem = pm.auto_arima(
            datos['TEMP'].dropna(),
            start_p=1, start_q=1,
            test='adf',       # use adftest to find optimal 'd'
            max_p=3, max_q=3, # maximum p and q
            m=1,              # frequency of series
            d=None,           # let model determine 'd'
            seasonal=False,   # No Seasonality
            start_P=0,
            D=0,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True)

        pickle.dump(model_tem, open("./model_tem.pickle", "wb" ) )

        with ZipFile('./model_tem.pickle.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write('./model_tem.pickle')

        ############
        # Humidity #
        ############

        model_hum = pm.auto_arima(
            datos['HUM'].dropna(),
            start_p=1, start_q=1,
            test='adf',       # use adftest to find optimal 'd'
            max_p=3, max_q=3, # maximum p and q
            m=1,              # frequency of series
            d=None,           # let model determine 'd'
            seasonal=False,   # No Seasonality
            start_P=0,
            D=0,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True)

        pickle.dump(model_hum, open("./model_hum.pickle", "wb" ) )

        with ZipFile('./model_hum.pickle.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write('./model_hum.pickle')


if __name__ == "__main__":
    m = Model()
