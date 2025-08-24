from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging

from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file
from network_security.constant.training_pipeline import SCHEMA_FILE_PATH

import pandas as pd
import os,sys
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    ## use staticmethod because we don't want to change the state of the object (No access to self or cls)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema["columns"])
            return number_of_columns == len(dataframe.columns)
        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self.schema["numerical_columns"]
            dataframe_columns = [col for col in dataframe.columns if dataframe[col].dtype == "int64"]
            return set(numerical_columns) == set(dataframe_columns)
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    ##Dataset drift happens when the distribution of data changes over time. 
    ## This can cause models trained on old data to perform poorly on new data.
    def detect_dataset_drift(self,base_df, current_df, threshold=0.05):
        try:
            status = True
            report = {}
            for col in base_df.columns:
                base_data, current_data = base_df[col], current_df[col]
                # Null hypothesis is that both samples are drawn from the same distribution
                # If p-value is less than the threshold, we reject the null hypothesis
                # and conclude that the two samples are not drawn from the same distribution
                p_value = ks_2samp(base_data, current_data).pvalue
                if p_value < threshold:
                    report.update({col:{"p_value":p_value,"drift_status":"drift detected"}})
                    status = False
                else:
                    report.update({col:{"p_value":p_value,"drift_status":"No drift detected"}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            write_yaml_file(file_path=drift_report_file_path,data=report)
            return status
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the train and test file
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            ## validate number of columns
            status = self.validate_number_of_columns(train_df)
            if not status:
                raise Exception("Number of columns are not matching with the schema")
            status = self.validate_number_of_columns(test_df)
            if not status:
                raise Exception("Number of columns are not matching with the schema")

            ## validate numerical columns
            status = self.is_numerical_column_exist(train_df)
            if not status:
                raise Exception("Numerical columns are not matching with the schema")
            status = self.is_numerical_column_exist(test_df)
            if not status:
                raise Exception("Numerical columns are not matching with the schema")
            
            ## lets check data drift
            status =self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            if not status:
                raise Exception("Data drift detected")
            
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)

            dir_path = os.path.dirname(self.data_validation_config.valid_test_file_path)
            os.makedirs(dir_path,exist_ok=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)

