import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import asyncio
from sqlalchemy.ext.asyncio import create_async_engine  
from sqlalchemy import (
    MetaData, Table, Column,insert,select,
    Integer, String, Float, ForeignKey, DateTime
)
from sqlalchemy import inspect
from pathlib import Path
import json 







async def local_db():
  """ Simple Local Sqlite Db """

  pwd = Path(__file__).resolve().parent
  root = pwd.parent
  sub_folder = root/"data"
  sub_folder.mkdir(parents=True, exist_ok=True)
  
  db_file = sub_folder/"sales.db"
  db_url = f"sqlite+aiosqlite:///{db_file}"
  
#Creat db engine 
  engine = create_async_engine(db_url,
  pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,)
  
  meta_obj = MetaData()
  
  
  async with engine.connect() as conn:
    inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
    
    
  
  with open("Products_data.json","r") as f:
    data1 = json.load(f)
    #print(data1[0])
    
  with open("customers_data.json","r") as file:
    data2 = json.load(file)

    
  with open("orders_data.json","r") as fi:
    data3 = json.load(fi)
    
  
  customers = Table(
    "customers",
    meta_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
    Column("city", String),)

  products = Table(
    "products",
    meta_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("category", String),
    Column("price", Float),)

  orders = Table(
    "orders",
    meta_obj,
    Column("id", Integer, primary_key=True),
    Column("customer_id", ForeignKey("customers.id")),
    Column("product_id", ForeignKey("products.id")),
    Column("quantity", Integer),
    Column("total_price", Float),
    Column("order_date", String), )
    
  async with engine.begin() as conn:
    await conn.run_sync(meta_obj.create_all)  
    
  async with engine.begin() as conn:
    stmt = insert(customers)
    await conn.execute(stmt,data2)
  
  async with engine.begin() as conn:
    stmt = insert(products)
    await conn.execute(stmt,data1)
    
  async with engine.begin() as conn:
    stmt = insert(orders)
    await conn.execute(stmt,data3)
    print("Inserted data")
  
 # async with engine.connect() as conn:
   # stmt = select(orders)
  #  data = await conn.execute(stmt)
   # for x in data:
  #    print(x)
    
    
  await engine.dispose()
  


  


asyncio.run(local_db())

