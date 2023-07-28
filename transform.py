import pandas as pd
import numpy as np
import os

#from extract import customer_1


#Clean special characters
def clean_data(data):   
    customer = data.replace('[^a-z A-Z 0-9]', "", regex=True)
    return customer


#Vlookup materials
def xref_tables_materials(data):
    master = pd.read_csv('xref_tables/Material_master.csv')
    data = data.merge(master, left_on = 'customer_material', right_on= 'PART_NUMBER', how = 'left')
    data = data.drop(['CUSTOMER', 'PART_NUMBER'], axis = 1)
    return data


#Vlookup locations
def xref_tables_locations(data):
    master = pd.read_csv('xref_tables/Location_master.csv')
    data = data.merge(master, left_on = 'customer_store', right_on= 'BRANCH_ID', how = 'left')
    data = data.drop(['BRANCH_ID', 'CUSTOMER'], axis = 1)
    return data


#Assign sales
def sales(data):
    data['real_sales'] = data['sales']
    return data


#Assing unit price
def unit_price(data): 
    data['unit_price'] = data['real_sales']/data['qty_sold']
    data['unit_price'] = np.where(data['unit_price'] == np.inf,0,data['unit_price'])
    return data

def concatenamos_guardamos(data):
    cliente = data['customer_name_id'].unique()[0]
    look_up = pd.read_csv('Raw data/' + cliente +'.csv')
    look_up = pd.concat([look_up,data])
    look_up.to_csv('Raw data/' + cliente +'.csv', index=False)
    return look_up

#divide customer in valid and invalid table
def prod_tables(data):
    columns = ['INT_CUSTOMER_NBR', 'INT_PART_NUMBER']
    invalid_null, valid_null = [a for _, a in data.groupby(data[columns].notnull().all(1))]
    ignore_customer  = valid_null[valid_null['INT_CUSTOMER_NBR'] == 'IGNORE']
    ignore_materials = valid_null[valid_null['INT_PART_NUMBER'] == 'IGNORE']
    valid = valid_null[valid_null['INT_CUSTOMER_NBR'] != 'IGNORE']
    valid = valid[valid['INT_PART_NUMBER'] != 'IGNORE']
    invalid = pd.concat([invalid_null, ignore_customer, ignore_materials])

    cliente = data['customer_name_id'].unique()[0]
    valid_table = valid.to_csv('Prod data/valid_table/' + cliente +'.csv', index=False)
    invalid_table = invalid.to_csv('Prod data/invalid_table/' + cliente +'.csv', index=False)
    return valid, invalid

#consolidated_table
def consolidated_table(data):
    cliente = data['customer_name_id'].unique()[0]
    data = data[['customer_name_id', 'INT_PART_NUMBER' , 'INT_CUSTOMER_NBR', 'real_sales', 'unit_price', 'month', 'year']]
    consolidated = pd.read_csv('Business_data/consolidated_table.csv')
    consolidated = consolidated.drop(consolidated[consolidated['customer_name_id'] == cliente].index)
    consolidated = pd.concat([data,consolidated],ignore_index= True)
    consolidated.to_csv('Business_data/consolidated_table.csv', index= False)   
    return consolidated
#consolidated_table()


