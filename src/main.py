import logging
import asyncio
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

# imports
from fetch_db import fetch_from_database
from validate_customers import validate_customers_data
from validate_products import validate_products_data
from validate_orders import validate_orders_data
from models import CustomerData, ProductData, OrdersData
from save_raw_csv import save_raw_csv
from transform_data import transform_data
from load_to_Db import load_to_postgres

logging.basicConfig(level=logging.INFO)

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}
#2024, 1, 1 better year 
with DAG(
    dag_id="etl_sqlite_pipeline",
    start_date=datetime(2024, 1, 1), # Changed to past date so it can actually run
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["etl", "local_database"],
) as dag:

  @task(multiple_outputs=True)
  def extract_task():
    return asyncio.run(fetch_from_database())

  @task
  def save_raw_task(cus, pro, ords):
    save_raw_csv(cus, pro, ords)
    return "raw_saved"

  @task(multiple_outputs=True)
  def validate_customers_task(cus):
    return validate_customers_data(cus, CustomerData)

  @task(multiple_outputs=True)
  def validate_products_task(pro):
    return validate_products_data(pro, ProductData)

  @task(multiple_outputs=True)
  def validate_orders_task(ords):
    return validate_orders_data(ords, OrdersData)

  @task(multiple_outputs=True)
  def transform_task(c, c1, p, p1, o, o1):
    return transform_data(c, c1, p, p1, o, o1)

  @task
  def load_task(cus_l, pro_l, ords_l):
    return asyncio.run(load_to_postgres(cus_l, pro_l, ords_l))

    # ----------------------------
    # REFACTORED DAG FLOW
    # ----------------------------

    # 1. Extract (Store as one object, do not unpack with commas)
  raw_data = extract_task()

    # 2. Save raw data (Access keys directly from raw_data)
  save_raw_task(raw_data['cc'], raw_data['pp'], raw_data['oo'])

    # 3. Validate
    # Access keys from raw_data, results stored as objects
  v_cust = validate_customers_task(raw_data['cc'])
  
  v_prod = validate_products_task(raw_data['pp'])
  
  v_ord  = validate_orders_task(raw_data['oo'])

    # 4. Transform
    # Access keys from the validation objects
    # Assuming validation tasks return dicts with keys like 'valid' and 'invalid'
    # Change these keys ('c', 'c1', etc.) to match what your validation functions actually return
  transformed = transform_task(
        v_cust['valid'], v_cust['invalid'], 
        v_prod['valid'], v_prod['invalid'], 
        v_ord['valid'], v_ord['invalid']
    )

    # 5. Load
  load_task(transformed['cus_l'], transformed['pro_l'], transformed['ords_l'])



