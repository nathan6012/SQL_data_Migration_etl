import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pandas as pd 
import csv 
from pathlib import Path
from datetime import datetime 


def save_raw_csv(a,b,c):
  
  """ Data Saved to json back to dict """
  
    
  pwd = Path(__file__).resolve().parent
  root = pwd.parent
  sub_folder = root/"data"

  #file1 = sub_folder/"customers.csv"
  #file2 = sub_folder/"products.csv"
  #file3 = sub_folder/"orders.csv"
  
  ts = datetime.now().strftime("%Y%m%d_%H%M%S")
  file_data_1 = f"customers_{ts}.csv"
  
  file1 = sub_folder/ file_data_1
  
  
  ts = datetime.now().strftime("%Y%m%d_%H%M%S")
  file_data_2 = f"products_{ts}.csv"
  
  file2 = sub_folder/file_data_2
  
  
  ts = datetime.now().strftime("%Y%m%d_%H%M%S")
  file_data_3 = f"orders_{ts}.csv "
  
  file3 = sub_folder/file_data_3
  
  

  
  df = pd.DataFrame(a)
  df.to_csv(file1,index=False)
  
  df2 = pd.DataFrame(b)
  df2.to_csv(file2,index=False)
  
  df3 = pd.DataFrame(c)
  df3.to_csv(file3,index=False)
  
  
  
def main():
  save_raw_csv()
  
if __name__== "__main__":
  main()