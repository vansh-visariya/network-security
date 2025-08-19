from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
import json
import sys
import certifi
import pandas as pd
import numpy as np
import pymongo
from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging

load_dotenv()
url = os.getenv("MONGO_ALAS_PASS")

ca = certifi.where()  ##It ensures that your Python application uses a trusted and up-to-date certificate authority (CA) bundle, rather than relying on potentially outdated or missing system certificates.

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records = df.to_json(orient='records')
            return json.loads(records)
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.mongo_client = MongoClient(url)
            self.database = self.mongo_client[database]  ## create database
            self.collection = self.database[collection]   ## create collection
            self.collection.insert_many(records)   ## insert data
            return(len(records))
        except Exception as e:
            raise networkseacurityException(e,sys)
        
if __name__ == "__main__":
    file_path = 'network_data/phisingData.csv'
    database = 'vansh'
    collection = 'Network_Data'
    obj = NetworkDataExtract()
    records = obj.csv_to_json(file_path=file_path)
    lenght = obj.insert_data_mongodb(records,database,collection)
    print(lenght)
