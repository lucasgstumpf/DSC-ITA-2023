import pandas as pd
import os
import pytz
import re
from metar import Metar
from datetime import datetime, timedelta

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed_data'))

def toDate24(df,coluna):
    brasilia_timezone = pytz.timezone('America/Sao_Paulo')

    # Converte o timestamp para o fuso horário de Brasília
    nova_coluna = coluna + "formatted"
    df[nova_coluna] = df[coluna].apply(lambda x: datetime.fromtimestamp(int(x)/1000, tz=brasilia_timezone).strftime("%A, %B %d, %Y %H:%M:%S"))

    return df

def removeDuplicatesRows(df):
    # Remove as linhas duplicadas com base em todas as colunas
    df_no_duplicates = df.drop_duplicates()
    return df_no_duplicates


def openDataframe(filename):
    filePath = os.path.join(DATA_PATH, filename)
    # Abre um arquivo CSV e carrega seu conteúdo em um DataFrame
    df = pd.read_csv(filePath, sep=',')
    return df

def saveDataframe(df, filename):
    filePath = os.path.join(DATA_PATH, filename)    
    # Salva um DataFrame em um arquivo CSV
    df.to_csv(filePath, sep=',', index=False)

def interpretaMetaR(df):

    df = df.replace('METAF', 'METAR')
    df = df.replace('\n', '')


    station = None
    type = None
    hora_formated = None
    temperature = None
    dew_point = None
    windDirection = None
    windVelocity = None
    visibility = None
    pressure = None
    weather = None
    sky = None
    skyFeet= None

    try: 

        obs = Metar.Metar(df[:-1])

        for item in obs.string().split('\n'):
            if("station" in item):
                station = item.split(" ")[1]
            if("type" in item):
                type = " ".join(item.split(" ")[1:])
            if("time" in item):
                timeZ = " ".join(item.split(" ")[1:])
                data_obj = datetime.strptime(timeZ, "%a %b %d %H:%M:%S %Y")
                nova_data_obj = data_obj - timedelta(hours=3)
                hora_formated = nova_data_obj.strftime("%a %b %d %H:%M:%S %Y")
            if("temperature" in item):
                temperature = item.split(" ")[1]
            if("dew point" in item):
                dew_point = item.split(" ")[2]
            if("wind" in item):
                wind = (item.split(" ")[1:])
                windDirection = wind[0]
                windVelocity = wind[2]
            if("visibility" in item):
                visibility = item.split(" ")[1]
            if("pressure" in item):
                pressure = item.split(" ")[1]
            if("weather" in item):
                weather = " ".join(item.split(" ")[1:])
            if("sky" in item):
                skyString = " ".join(item.split(" ")[1:])
                if(' at ' in skyString):
                    sky = ''.join(skyString.split(' at ')[0])
                else:
                    sky = ''.join(skyString.split(',')[0])
                
                allFeets = re.findall(r"(\d+)",skyString)
                if len(allFeets) > 0:
                    skyFeet = allFeets[0]
    except:
        pass

    return station, type, hora_formated, temperature,dew_point,windDirection,windVelocity,visibility,pressure,weather,sky,skyFeet

if __name__ == "__main__":
    df = openDataframe('bimtra_silver.csv')
    df = removeDuplicatesRows(df)
    saveDataframe(df, 'bimtra_silver.csv')
    print(df)