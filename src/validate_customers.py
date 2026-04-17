import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from pydantic import BaseModel,ValidationError
import json 
from models import CustomerData
from datetime import datetime




def validate_customers_data(data,Model):
  """ Validates customer Data """
  
  
  valid = []
  invalid = [] 
  
  for idx,records in enumerate(data):
    try:
      clean = Model(**records)
      valid.append({ 
        "idx":idx,
        "data":clean.model_dump(mode="json")
      })
    except ValidationError as error:
      invalid.append({
        "idx":idx,
        "errors":error.errors()
      })
      
  return valid,invalid   
      

  


