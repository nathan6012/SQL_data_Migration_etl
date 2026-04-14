import pandas as pd
from pandas import json_normalize

import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def transform_data(c,c1,p,p1,o,o1):
  
  #Customers ________________
  #customer_valid_data 
  df_c = pd.json_normalize(c)
  df_c1 = pd.json_normalize(c1) # is Empty
  
  
  df_c.columns = df_c.columns.str.lower()
  df_c.columns = df_c.columns.str.strip()  
  lis = ["data.email","data.city"]
    
  for col in lis:
    if col in df_c.columns:
      df_c[col] = df_c[col].replace("nan",None)
        
  df_c["data.name"] = df_c["data.name"].astype("str")
    
  df_c["data.id"] = df_c["data.id"].astype("int32")
    
  df_c = df_c.drop_duplicates()
  df_c = df_c.reset_index(drop=True)
    
    
  df_c = df_c.drop(columns=["idx"])
    
  df_c.columns=df_c.columns.str.replace("data.","",regex=False)
    
  
  print()
  
  customers = df_c.to_dict(orient='records')
  
  
  

  
    
  #products ___________________________ 
  
  df_p = pd.json_normalize(p)
  
  df_p1 = pd.json_normalize(p1)
  
  #print(df_p.dtypes)
  
  df_p.columns = df_p.columns.str.lower()
  df_p.columns = df_p.columns.str.strip()
  
  lis = ["data.category","data.price","data.name"]
  for col in lis:
    if col in df_c.columns:
      df_c[col] = df_c[col].replace("nan",None)
        
  df_p["data.name"] = df_p["data.name"].astype("str")
    
  df_p["data.id"] = df_p["data.id"].astype("int32")
  
  df_p["data.price"] = df_p["data.price"].astype("float32")
    
  df_p = df_p.drop_duplicates()
  df_p = df_p.reset_index(drop=True)
    
    
  df_p = df_p.drop(columns=["idx"])
  
  df_p.columns=df_p.columns.str.replace("data.","",regex=False)
    
  
  print()

  
  
  
  products = df_p.to_dict(orient='records')
  

  
  
  
  
  
  
  
  df_o = pd.json_normalize(o)
  df_o1 = pd.json_normalize(o1)
  
  
  
  df_o.columns = df_o.columns.str.lower()
  df_o.columns = df_o.columns.str.strip()
  
  lis = ["data.quantity","data.total_price"]
    
  for col in lis:
    if col in df_o.columns:
      df_o[col] = df_o[col].replace("nan",None)
        
  df_o["data.id"] = df_o["data.id"].astype("int32")
    
  df_o["data.product_id"] = df_o["data.product_id"].astype("int32")
  
  df_o["data.product_id"] = df_o["data.product_id"].astype("int32")
  
  df_o["data.total_price"] = df_o["data.total_price"].astype("float32")
  
  
  

  df_o["data.order_date"] = pd.to_datetime(df_o["data.order_date"],errors="coerce", format="mixed")

  df_o = df_o.drop_duplicates()
  df_o = df_o.reset_index(drop=True)
    
    
  df_o = df_o.drop(columns=["idx"])
    
  df_o.columns=df_o.columns.str.replace("data.","",regex=False)
    
  print()
  
 # print(df_o.dtypes)
  
  
  orders = df_o.to_dict(orient='records')
  
  
  
  
  
  return customers,products,orders 
  
  
  
def main():
  tranform_data()
  
if __name__=="__main__":
  main()
  