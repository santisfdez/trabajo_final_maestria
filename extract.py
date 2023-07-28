import os
import numpy as np
import pandas as pd
from dicionarios import *


# read files
def read_identify(file_name):
    #csv
    try:
        look_up_1 = pd.read_csv('Source_data/' + file_name +'.csv')
        look_up_1['customer_name_id'] = file_name
        status = 'csv complete'
    except:
        try:
            #excel
            look_up_1 = pd.read_excel('Source_data/' + file_name + '.xlsx')
            look_up_1['customer_name_id'] = file_name
            status = 'excel complete'
        except:
            try:
                #txt
                look_up_1 = pd.read_csv('Source_data/' + file_name + '.txt', sep = "\t")
                look_up_1['customer_name_id'] = file_name
                status = 'txt complete'
            except:
                status = 'couldnt read'
                look_up_1 = pd.DataFrame()
    
    return look_up_1, status


def adjust_columns(data):
    #minusc
    data.columns = [x.lower() for x in data.columns]
    #renombramos
    data.rename(columns = nombre_columns,inplace =True)
    #capturamos parametros
    cliente = data['customer_name_id'].unique()[0]
    parametros = pd.read_excel('Functions/estructura_columnas.xlsx')
    ref = parametros.loc[parametros.cliente == cliente,'campos_obligatorios'].tolist()
    if not data.columns.tolist() == (ref):
        raise Exception("Error: The dataframe don't have the same columns.")
    return data
          

    
    












