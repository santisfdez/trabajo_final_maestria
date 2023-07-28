import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV

def read_data(data):
  
  data['timeline'] = pd.to_datetime(data[['year', 'month']].assign(day=1))
  data = data.copy()
  data = data[['timeline','real_sales']]
  data = data.groupby('timeline').sum().reset_index()
  return data

def split_data(data):
    x = data.iloc[:, 0:1]
    y = data.iloc[:, -1:]
    return x,y

def trained_model(x,y):
    DT_model = RandomForestRegressor(max_depth=2, random_state=0)
    result_model = DT_model.fit(x,y)
    return result_model

def predict(model,x):
    y_pred_test = model.predict(x)
    return y_pred_test

def final(data,y_pred_test):
    df_final = data.copy()
    df_final['forecast'] = y_pred_test
    return df_final

def initial_metrics(df_final):
    mse = mean_squared_error(df_final['real_sales'], df_final['forecast'])
    r2 = r2_score(df_final['real_sales'], df_final['forecast'])
    return mse, r2

def initial_graph(df_final, data):
    plt.figure(figsize=(10, 5))
    plt.plot(df_final['real_sales'], label='Valores reales')
    plt.plot(df_final['forecast'], label='predicts')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title(f'Proyecciones del modelo: Random Forest Regression')
    plt.legend(loc='upper right')
    cliente = data['customer_name_id'].unique()[0]
    plt.savefig('Graphics/' + cliente + '_Initial_Model.png')
    return 

def param_grid():
    param_grid = {
    'n_estimators': [50, 100, 200, 500],
    'max_depth': [None,5,10,20]
    }
    return param_grid

def param_fit(param_grid, x,y):
    model = RandomForestRegressor()
    grid_search = GridSearchCV(model, param_grid, scoring='neg_mean_squared_error', cv=5)
    grid_search.fit(x,y)
    return grid_search

def best_model(grid_search):
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    return best_model

def best_model_predict(best_model,df_final,x,name):
    y_pred = best_model.predict(x)  # X_test son las características de prueba
    df_final['forecast_hiper'] = y_pred
    cliente = name['customer_name_id'].unique()[0]
    df_final.to_csv('Proyections/' + cliente + '_Proyections_Best_model.csv')
    return df_final

def best_model_metrics(df_final):
    mse = mean_squared_error(df_final['real_sales'], df_final['forecast_hiper'])
    r2 = r2_score(df_final['real_sales'], df_final['forecast_hiper'])
    return mse, r2

def best_model_graphs(df_final, data):
    plt.figure(figsize=(10, 5))
    plt.plot(df_final['real_sales'], label='Valores reales')
    plt.plot(df_final['forecast'], label='predicts')
    plt.plot(df_final['forecast_hiper'], label='predicts_hiper')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title(f'Proyecciones del modelo: Random Forest Regression')
    plt.legend(loc='upper right')
    cliente = data['customer_name_id'].unique()[0]
    plt.savefig('Graphics/' + cliente + '_Best_Model.png')
    return
    
