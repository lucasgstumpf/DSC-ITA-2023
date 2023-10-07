import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import json


def req_api(api):
    response = requests.get(api)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def save_images(data, path):
    last_date = '' #última data salva
    
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'Image directory created: {path}\n\n')

    for i in tqdm(range(len(data))):
        url = data[i]['path']
        image_name = url.split('/')[-1]
        date_time = image_name.split('_')[1]
        date = date_time[:8]
        if date != last_date:
            last_date = date
            path_date = path + '/' + date + '/'
            if not os.path.exists(path_date):
                os.makedirs(path_date)
                print(f'==============\nImage Date directory created: {path_date}\n==============\n\n')

        response = requests.get(url)
        if response.status_code == 200:
            with open(path_date + image_name, 'wb') as f:
                f.write(response.content)
                print(f'\nImage saved: {image_name}\n')
        else:
            print(f'Error while saving image: {image_name}')


def main():
    token = "a779d04f85c4bf6cfa586d30aaec57c44e9b7173" #token fornecido por email
    data_inicio = "2023-05-01" # data mais antiga
    data_fim = "2023-05-02" # data mais recente

    api = f'http://montreal.icea.decea.mil.br:5002/api/v1/satelite?token={token}&idate={data_inicio}&fdate={data_fim}'
    data = req_api(api)
    path = './images'
    save_images(data, path)

main()