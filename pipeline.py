import os
import pandas as pd
from extract import *
from transform import *
from models import *

def pipeline(customers):
    x,y = read_identify(customer)
    z = adjust_columns(x)
    z = clean_data(z)
    z = xref_tables_materials(z)
    z = xref_tables_locations(z)
    z = sales(z)
    z = unit_price(z)
    z = concatenamos_guardamos(z)
    print(z.shape)
    z,t = prod_tables(z)
    w = consolidated_table(z)
    print(w.shape)
    z = read_data(z)
    x,y = split_data(z)
    DT_model = trained_model(x,y)
    y_pred = predict(DT_model,x)
    print(y_pred)
    df = final(z,y_pred)
    mse,r2 = initial_metrics(df)
    print(mse,r2)
    grap_1 = initial_graph(df,t)
    param = param_grid()
    param_fit_ = param_fit(param, x,y)
    best = best_model(param_fit_)
    best_predict = best_model_predict(best,df,x,t)
    print(best_predict)
    mse2,r22 = best_model_metrics(best_predict)
    print(mse2,r22)
    graph2 = best_model_graphs(best_predict,t)
    return best_predict

customerustomers_list = ['Customer1', 'Customer2','Customer3']

for customer in customerustomers_list:
    process = pipeline(customer)