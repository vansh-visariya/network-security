import os
import sys
import numpy as np
import pandas as pd

""" Training pipeline related constant """
TARGET_COLUMN = "Result"
PIPELINE_NAME:str = "network_security"
ARTIFACT_DIR:str = "artifacts"
FILE_NAME:str = "network_data.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


""" DATA INGESTION related constant """
DATA_INGESTION_COLLECTION_NAME:str = "Network_Data"
DATA_INGESTION_DATABASE_NAME:str = "vansh"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2