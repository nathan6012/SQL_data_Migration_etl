from fetch_db import fetch_from_database
import asyncio

from validate_customers import validate_customers_data

from validate_products import validate_products_data

from  validate_orders import validate_orders_data

from models import CustomerData,ProductData,OrdersData

from save_raw_csv import save_raw_csv

from transform_data import transform_data


async def main():
  x,y,z = await fetch_from_database()
  print("Data Extracted")

  save_raw_csv(x,y,z)
  print("Data to csv")
  
  
  c,c1 = validate_customers_data(x,CustomerData)
  print("Customer Data validated")
  
  
  p,p1= validate_products_data(y,ProductData)
  print("Product data Validated ")



  o,o1 = validate_orders_data(z,OrdersData)
  print("Orders Data Validated")
  print(len(o))
  
  print(o1)
 # print(len(o))

  
  cus,pro,ords = transform_data(c,c1,p,p1,o,o1)
  print(ords)
  
  
  
  
  
  
  
  print("Data validated")
  
  
  
  
  
if __name__=="__main__":
  asyncio.run(main())
  
  