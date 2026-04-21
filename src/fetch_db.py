#add code
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



import asyncio
from sqlalchemy.ext.asyncio import create_async_engine,AsyncEngine, AsyncConnection

from sqlalchemy import inspect 

from sqlalchemy import (
    MetaData, Table, Column,insert,select,
    Integer, String, Float, ForeignKey, DateTime
)
from pathlib import Path
import pandas as pd





def ensure_data_folder() -> Path:
  """Ensure the 'data' folder exists and return its path."""
  pwd = Path(__file__).resolve().parent
  root = pwd.parent
  sub_folder = root / "data"
  sub_folder.mkdir(parents=True, exist_ok=True)
  return sub_folder
    
    
    

def get_db_url(db_path: Path) -> str:
  """Return the SQLAlchemy async DB URL."""
  return f"sqlite+aiosqlite:///{db_path}"




async def get_table(conn: AsyncConnection, table_name: str, metadata: MetaData) -> Table | None:
  """Return a Table object if it exists in the database, else None."""
  
  tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
  
  if table_name in tables:
    return await conn.run_sync(lambda sync_conn:Table(table_name, metadata, autoload_with=sync_conn))
  return None





async def fetch_table_data(conn: AsyncConnection, table: Table) -> list[dict]:
  """Fetch all rows from a table and return as list of dicts."""
  
  result = await conn.execute(select(table))
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]

# ------------------------------
# Main database fetch
# ------------------------------

async def fetch_from_database() -> tuple[list[dict], list[dict], list[dict]]:
    # Setup folder and DB
  data_folder = ensure_data_folder()
  db_file = data_folder / "sales.db"
  
  
  db_url = get_db_url(db_file)

    # Create async engine
  engine: AsyncEngine = create_async_engine(db_url, echo=False, pool_pre_ping=True,
  pool_size=5, max_overflow=10)
  
  
  metadata = MetaData()

  async with engine.connect() as conn:
        # Fetch tables dynamically
    customers = await get_table(conn, "customers", metadata)
    products = await get_table(conn, "products", metadata)
    orders = await get_table(conn, "orders", metadata)

        # Fetch data safely
    customers_data = await fetch_table_data(conn, customers) if customers is not None else []
    
    products_data = await fetch_table_data(conn, products) if products is not None else []
    
    orders_data = await fetch_table_data(conn, orders) if orders is not None else []
    
  await engine.dispose()
  
  
  return customers_data, products_data, orders_data

# ------------------------------
# Entry point
# ------------------------------

async def main():
  data_customers, data_products, data_orders = await fetch_from_database()


if __name__ == "__main__":
    asyncio.run(main())