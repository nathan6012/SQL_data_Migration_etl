import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from pydantic import BaseModel,ConfigDict,EmailStr
from typing import Optional 
from decimal import Decimal
from datetime import datetime




class CustomerData(BaseModel):
  
  model_config = ConfigDict(extra="forbid")
  id: int
  name: str
  email: Optional[EmailStr] = None
  city: str
  
  
  
  
class ProductData(BaseModel):
  
  model_config = ConfigDict(extra="forbid")
  id: int
  name: str 
  category: str
  price: Decimal
  
  
  

class OrdersData(BaseModel):
  
  model_config = ConfigDict(extra="forbid")
  id: int 
  customer_id: int
  product_id: int 
  quantity: int 
  total_price: Decimal
  order_date: datetime
  
  
  
  