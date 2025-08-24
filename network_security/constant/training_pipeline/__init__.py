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

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

""" DATA INGESTION related constant """
DATA_INGESTION_COLLECTION_NAME:str = "Network_Data"
DATA_INGESTION_DATABASE_NAME:str = "vansh"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

""" DATA VALIDATION related constant """
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

""" DATA TRANSFORMATION related constant """
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSED_OBJECT_FILE_NAME:str = "preprocessed_object.pkl"
# for knn imputer for replacing nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values" : np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}