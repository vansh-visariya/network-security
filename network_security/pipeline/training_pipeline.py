import os, sys

from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import (TrainingPipelineConfig,
                                                   DataIngestionConfig,
                                                   DataValidationConfig,
                                                   DataTransformationConfig,
                                                   ModelTrainerConfig)

from network_security.entity.artifact_entity import (DataIngestionArtifact,
                                                     DataValidationArtifact,
                                                     DataTransformationArtifact,
                                                     ModelTrainerArtifact)

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data validation")

            data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                            data_ingestion_artifact=data_ingestion_artifact)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data transformation")

            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                    data_transformation_config=self.data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting model trainer")

            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,
                                        data_transformation_artifact=data_transformation_artifact)
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model trainer completed and artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            return model_trainer_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)