import sys,os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer

from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataTransformationConfig
from network_security.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from network_security.constant.training_pipeline import *
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
        data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def get_data_transformer_object(self)->Pipeline:
        """
        This function is used initialize knn imputer and return the pipeline object
        """
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline = Pipeline(steps=[("imputer",imputer)])
            return pipeline
        except Exception as e:
            raise networkseacurityException(e,sys)
        
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            ## get the train test data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ## testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            ## get the pipeline object
            preprocessing = self.get_data_transformer_object()
            transformed_input_train_feature = preprocessing.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessing.transform(input_feature_test_df)

            ## merge the input and target feature
            ## np.c_ is a utility in NumPy used for concatenating arrays along the second axis (columns)
            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path,preprocessing)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)