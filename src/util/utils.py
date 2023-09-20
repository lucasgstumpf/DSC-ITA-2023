import pandas as pd
import os
import pytz
from datetime import datetime, timezone

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

if __name__ == "__main__":
    df = openDataframe('bimtra_silver.csv')
    df = removeDuplicatesRows(df)
    saveDataframe(df, 'bimtra_silver.csv')
    print(df)