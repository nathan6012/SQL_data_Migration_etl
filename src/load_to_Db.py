import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy import text,select,update 
#from sqlalchemy import inspect 
from sqlalchemy import Text,Float
from sqlalchemy.dialects.postgresql import insert as upsert 
from sqlalchemy import UniqueConstraint 
from sqlalchemy import(Table,Column,Integer,String,MetaData,ForeignKey,Index,Numeric)
from sqlalchemy import DateTime
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
load_dotenv()









async def load_to_postgres(cus,pro,ords):
  """Loads The Transformed Data to Posgres Db"""
  
  db_url = os.getenv("DATABASE_URL").strip()
  
  engine = create_async_engine(db_url,echo=False,
  pool_pre_ping=True,
  pool_size=5,
  max_overflow=10,)
  
  
  metadata = MetaData()
  
  customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
    Column("city", String),)

  products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("category", String),
    Column("price", Float),)


  orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", ForeignKey("customers.id")),
    Column("product_id", ForeignKey("products.id")),
    Column("quantity", Integer),
    Column("total_price", Float),
    Column("order_date",DateTime),)
    
  async with engine.begin() as conn:
    await conn.run_sync(metadata.create_all)
    
  
 
  async with engine.begin() as conn:
    stmt = upsert(customers).values(cus)
    stmt = stmt.on_conflict_do_update(
       index_elements=["id"],
       set_={
         "name": stmt.excluded.name,
          "email": stmt.excluded.email,
          "city": stmt.excluded.city,
        }
    )

    await conn.execute(stmt) 
    
    
 
 
 
  async with engine.begin() as conn:
    stmt = upsert(products).values(pro)
    stmt = stmt.on_conflict_do_update(
      index_elements=["id"],
      
      set_={"name": stmt.excluded.name,
      
      "category": stmt.excluded.category,
      
      "price": stmt.excluded.price })
    
    await conn.execute(stmt)
    
  
  async with engine.begin() as conn:
    stmt = upsert(orders).values(ords)
    stmt = stmt.on_conflict_do_update(
      index_elements=["id"],
      
      set_={"quantity": stmt.excluded.quantity,
      
      "total_price": stmt.excluded.total_price,
      
      "order_date": stmt.excluded.order_date })
    
    await conn.execute(stmt)
    
  
    
    
    
    
  await asyncio.sleep(0.3)      
  await engine.dispose()


  
async def main():
  await load_to_postgres()
  
if __name__ == "__main__":
  asyncio.run(main())
  