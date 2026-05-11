import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import pandas as pd
import boto3
from dotenv import load_dotenv
from datetime import datetime
import logging


# Logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()


def save_raw_csv(customers, products, orders):
  """Save raw extracted data to S3/R2 as CSV files """

  endpoint = os.getenv("endpoint_url")
  access_key_id = os.getenv("access_key_id")
  secret_access_key = os.getenv("secret_key")

  bucket = "nathan-elt-buck"

  s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name="auto"
    )

  datasets = {
        "customers": customers,
        "products": products,
        "orders": orders
    }

  for name, data in datasets.items():

    if not data:
      logging.warning(f"{name} dataset is empty")
      continue

    try:
      df = pd.DataFrame(data)

            # Convert directly to CSV string (no StringIO)
      csv_data = df.to_csv(index=False)

      now = datetime.utcnow()

      key = (
                f"sqlite/csv/"
                f"{now:%Y/%m/%d/%H}/"
                f"{name}_data.csv"
            )

      s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=csv_data,
                ContentType="text/csv"
            )

      logging.info(f"{name} CSV staged to Data Lake")

    except Exception as e:
      logging.error(f"Failed to upload {name}: {e}")