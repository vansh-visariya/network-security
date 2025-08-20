from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_ALAS_PASS")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config ## made object of data ingestion config
        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        """
        This function is used to export the collection from mongodb as dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            collection = self.mongo_client[database_name][collection_name]  ## get the collection
            df = pd.DataFrame(list(collection.find()))  ## convert the collection to dataframe
            if "_id" in df.columns:
                df = df.drop("_id",axis=1)
            df.replace({"na":np.nan},inplace=True)  ## replace na with nan
            return df
        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def export_data_into_feature_store(self,df:pd.DataFrame):
        """
        This function is used to export the dataframe to feature store
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def split_data_as_train_test(self,df:pd.DataFrame):
        """ 
        This function is used to split the data into train and test
        """
        try:
            train_set, test_set = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()  ## export the collection as dataframe
            dataframe = self.export_data_into_feature_store(dataframe)  ## export the dataframe to feature store
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)