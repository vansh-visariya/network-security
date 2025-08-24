from datetime import datetime
import os
from network_security.constant.training_pipeline import *

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp:str = timestamp
        self.pipeline_name = PIPELINE_NAME
        self.artifact_dir = os.path.join(ARTIFACT_DIR,timestamp)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        """
        This class is used to create the data ingestion config
        """
        ## data ingestion directory
        self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
        ## feature store file path
        self.feature_store_file_path:str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
        ## ingested train and test file path
        self.training_file_path:str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
        self.testing_file_path:str = os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
        ## train test split ratio
        self.train_test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        ## mongodb info
        self.collection_name:str = DATA_INGESTION_COLLECTION_NAME
        self.database_name:str = DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.data_validation_dir,DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir,TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir,TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir,TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir,TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(self.data_validation_dir,DATA_VALIDATION_DRIFT_REPORT_DIR,DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)