import sys
import os
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

# ----------------------------
# DAG CONFIG
# ----------------------------
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="etl_sqlite_pipeline",
    start_date=datetime(2026, 4, 28),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["etl", "local_database"],
) as dag:

    # ----------------------------
    # EXTRACT (ASYNC SAFE WRAPPER)
    # ----------------------------
  @task
  def extract_task():
    return asyncio.run(fetch_from_database())


    # ----------------------------
    # SAVE RAW
    # ----------------------------
  @task
  def save_raw_task(cus, pro, ords):
    save_raw_csv(cus, pro, ords)
    return "raw_saved"


    # ----------------------------
    # VALIDATION LAYER
    # ----------------------------
  @task
  def validate_customers_task(cus):
    return validate_customers_data(cus, CustomerData)


  @task
  def validate_products_task(pro):
    return validate_products_data(pro, ProductData)


  @task
  def validate_orders_task(ords):
    return validate_orders_data(ords, OrdersData)


    # ----------------------------
    # TRANSFORM LAYER
    # ----------------------------
  @task
  def transform_task(c, c1, p, p1, o, o1):
    return transform_data(c, c1, p, p1, o, o1)


    # ----------------------------
    # LOAD (ASYNC SAFE WRAPPER)
    # ----------------------------
  @task
  def load_task(cus_l, pro_l, ords_l):
    return asyncio.run(load_to_postgres(cus_l, pro_l, ords_l))


    # ----------------------------
    # DAG FLOW
    # ----------------------------

    # Extract
  cc, pp, oo = extract_task()

    # Save raw data
  save_raw_task(cc, pp, oo)

    # Validate
  c, c1 = validate_customers_task(cc)
  p, p1 = validate_products_task(pp)
  o, o1 = validate_orders_task(oo)

    # Transform
  cus_l, pro_l, ords_l = transform_task(c, c1, p, p1, o, o1)

    # Load
  load_task(cus_l, pro_l, ords_l)
  
# Fix proper Airflow 

# How to run airflow uaing github actions 
# prefect is simply run by running th script what of airflow 


