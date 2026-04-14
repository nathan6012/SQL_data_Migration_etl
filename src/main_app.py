import sys
import os
import logging 

logging.basicConfig(level=logging.INFO)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from prefect import flow, task
import asyncio

from fetch_db import fetch_from_database

from validate_customers import validate_customers_data

from validate_products import validate_products_data

from  validate_orders import validate_orders_data

from models import CustomerData,ProductData,OrdersData

from save_raw_csv import save_raw_csv

from transform_data import transform_data

from load_to_Db import load_to_postgres



### key_Variables 
# cus/c,c1/cc = customers 

#pro/p/p1/pp  = products

#ords/o/o1/oo = orders 
### 


@task(retries=3,log_prints=True)
async def fetch_fron_db_task():
  cc, pp, oo = await fetch_from_database()
  return cc, pp, oo
  

@task(name="Save_to_csv")
def saw_raw_csv_files_task(cus,pro,ords):
  return save_raw_csv(cus,pro,ords)



@task(name="Validate_customers")  
def Validate_customers_task(cus,Model):
  
  return validate_customers_data(cus,Model)




@task(name="validate_products") 
def validate_products_task(pro,Model):
  
  return validate_products_data(pro,Model)
  

@task(name="validate_orders")
def validate_orders_task(ords,Model):
  
  return validate_orders_data(ords,Model)
 
 
  

@task(name="Transform_data")
def transform_data_task(c,c1,p,p1,o,o1):
  return transform_data(c,c1,p,p1,o,o1)
  
  
@task(name="load_to_postgres")
async def load_to_postgres_task(cus_l,pro_l,ords_l):
  
  return await load_to_postgres(cus_l,pro_l,ords_l)
  
  
  
@flow(name="Db_to_Db_Main_Flow", log_prints=True)
async def main():
  cc,pp,oo = await fetch_fron_db_task()
 
  logging.info("\nData Fetched from Db")
  
  
  saw_raw_csv_files_task(cc,pp,oo)
  
  logging.info("\ncsv files saved for backfill")
  await asyncio.sleep(0.5)
  
  logging.info("\nData validation started")
  
  c,c1 = Validate_customers_task(cc,CustomerData)
  
  
  p,p1 = validate_products_task(pp,ProductData)


  o,o1 = validate_orders_task(oo,OrdersData)
  
  
  
  logging.info("\nData Passed Validation")
  await asyncio.sleep(0.1)
  logging.info("\nTransfromation started")
  
  cus,pro,ords = transform_data_task(c,c1,p,p1,o,o1)
  
 
  await asyncio.sleep(0.5)
  logging.info("\nData ready for Database load")
  
  await load_to_postgres_task(cus,pro,ords)
  
  logging.info("\npipeline Completed")
  await asyncio.sleep(0.1)
  
if __name__=="__main__":
  asyncio.run(main())
  
  