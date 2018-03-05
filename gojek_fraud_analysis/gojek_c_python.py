import os
import csv
import pandas as pd

print(os.getcwd())
print(os.listdir())

## Read data
filename = 'gojek_problem_c.csv'
df = pd.read_csv(filename)
print(df.head())

## Data Exploration

# unique customer
uni_cust_id = df.customer_id.unique()
uni_cust_name = df.customer_name.unique()
print(len(uni_cust_id))
print(uni_cust_name)

print(df.shopping_estimated_price.describe())


