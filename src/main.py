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
# DEFAULT ARGS
# ----------------------------
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

# ----------------------------
# DAG
# ----------------------------
with DAG(
    dag_id="etl_sqlite_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["etl", "sqlite", "postgres"],
) as dag:

    # ----------------------------
    # 1. EXTRACT
    # ----------------------------
  @task(multiple_outputs=True)
  def extract_task():
    customers, products, orders = asyncio.run(fetch_from_database())
    return {
        "customers": customers,
        "products": products,
        "orders": orders,
    }
    # ----------------------------
    # 2. SAVE RAW
    # ----------------------------
  @task
  def save_raw_task(customers, products, orders):
    save_raw_csv(customers, products, orders)
    return "raw_saved"

    # ----------------------------
    # 3. VALIDATION
    # ----------------------------
  @task(multiple_outputs=True)
  def validate_customers_task(customers):
    valid, invalid = validate_customers_data(customers, CustomerData)
    return {"valid": valid, "invalid": invalid}

  @task(multiple_outputs=True)
  def validate_products_task(products):
    valid, invalid = validate_products_data(products, ProductData)
    return {"valid": valid, "invalid": invalid}

  @task(multiple_outputs=True)
  def validate_orders_task(orders):
    valid, invalid = validate_orders_data(orders, OrdersData)
    return {"valid": valid, "invalid": invalid}

    # ----------------------------
    # 4. TRANSFORM
    # ----------------------------
  @task(multiple_outputs=True)
  def transform_task(c_valid, c_invalid, p_valid, p_invalid, o_valid, o_invalid):
    cus_l, pro_l, ords_l = transform_data(
            c_valid, c_invalid,
            p_valid, p_invalid,
            o_valid, o_invalid
        )

    return {
            "customers": cus_l,
            "products": pro_l,
            "orders": ords_l,
        }

    # ----------------------------
    # 5. LOAD
    # ----------------------------
  @task
  def load_task(customers, products, orders):
    asyncio.run(load_to_postgres(customers, products, orders))
    return "loaded"

    # ----------------------------
    # DAG FLOW
    # ----------------------------

    # Extract
  raw = extract_task()

    # Save raw
  save_raw_task(
        raw["customers"],
        raw["products"],
        raw["orders"]
    )

    # Validate
  v_cust = validate_customers_task(raw["customers"])
  v_prod = validate_products_task(raw["products"])
  v_ord  = validate_orders_task(raw["orders"])

    # Transform
  transformed = transform_task(
        v_cust["valid"], v_cust["invalid"],
        v_prod["valid"], v_prod["invalid"],
        v_ord["valid"], v_ord["invalid"]
    )

    # Load
  load_task(
        transformed["customers"],
        transformed["products"],
        transformed["orders"]
    )