import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from pydantic import BaseModel,ValidationError
import json 
from models import ProductData
from datetime import datetime



def validate_products_data(data2,Model):
  """Validate product Data """ 
  
  valid = []
  invalid = [] 
  
  for idx,records in enumerate(data2):
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
 
