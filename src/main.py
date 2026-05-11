import asyncio
import logging
from dagster import asset, Definitions
#import aiosqlite
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
# 1. EXTRACT
# ----------------------------
@asset
def raw_data():
    customers, products, orders = asyncio.run(fetch_from_database())
    return {
        "customers": customers,
        "products": products,
        "orders": orders,
    }


# ----------------------------
# 2. SAVE RAW to cloud 
# ----------------------------
@asset
def saved_raw_data(raw_data):
    save_raw_csv(
        raw_data["customers"],
        raw_data["products"],
        raw_data["orders"],
    )
    return "raw_saved"


# ----------------------------
# 3. VALIDATION
# ----------------------------
@asset
def validated_customers(raw_data):
    valid, invalid = validate_customers_data(
        raw_data["customers"], CustomerData
    )
    return {"valid": valid, "invalid": invalid}


@asset
def validated_products(raw_data):
    valid, invalid = validate_products_data(
        raw_data["products"], ProductData
    )
    return {"valid": valid, "invalid": invalid}


@asset
def validated_orders(raw_data):
    valid, invalid = validate_orders_data(
        raw_data["orders"], OrdersData
    )
    return {"valid": valid, "invalid": invalid}


# ----------------------------
# 4. TRANSFORM
# ----------------------------
@asset
def transformed_data(
    validated_customers,
    validated_products,
    validated_orders,
):
    cus_l, pro_l, ords_l = transform_data(
        validated_customers["valid"],
        validated_customers["invalid"],
        validated_products["valid"],
        validated_products["invalid"],
        validated_orders["valid"],
        validated_orders["invalid"],
    )

    return {
        "customers": cus_l,
        "products": pro_l,
        "orders": ords_l,
    }

# ----------------------------
# 5. LOAD
# ----------------------------
@asset
def loaded_data(transformed_data):
    asyncio.run(
        load_to_postgres(
            transformed_data["customers"],
            transformed_data["products"],
            transformed_data["orders"],
        )
    )
    return "loaded"

# ----------------------------
# DEFINITIONS (ENTRY POINT)
# ----------------------------
defs = Definitions(
    assets=[
        raw_data,
        saved_raw_data,
        validated_customers,
        validated_products,
        validated_orders,
        transformed_data,
        loaded_data,
    ]
)
