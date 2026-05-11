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
from io import StringIO


# Logging
logging.basicConfig(level=logging.INFO)
# Load environment variables
load_dotenv()


def save_raw_csv(customers, products, orders):
  """Save raw extracted data to S3/R2 as CSV """

  endpoint = os.getenv("endpoint_url")
  access_key_id = os.getenv("access_key_id")
  secret_access_key = os.getenv("secret_key")

  bucket = "nathan-elt-buck"

    # S3 / R2 client
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
            # Convert to DataFrame
      df = pd.DataFrame(data)

            # Convert DataFrame to CSV string
      csv_buffer = StringIO()
      df.to_csv(
                csv_buffer,
                index=False
            )

      now = datetime.utcnow()

            # File path in bucket
      key = (
                f"sqlite/csv/"
                f"{now:%Y/%m/%d/%H}/"
                f"{name}_data.csv"
            )

            # Upload CSV
      s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=csv_buffer.getvalue(),
                ContentType="text/csv"
            )

      logging.info(
                f"{name} CSV staged to Data Lake"
            )

    except Exception as e:
      logging.error(
                f"Failed to upload {name}: {e}"
            )