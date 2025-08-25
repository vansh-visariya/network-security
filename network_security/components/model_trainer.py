import sys,os
import numpy as np
import pandas as pd

from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import ModelTrainerConfig
from network_security.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact

from network_security.utils.main_utils.utils import load_numpy_array_data,save_object,load_object,evaluate_model
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import mlflow

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def track_model(self,model_name,model_score,metric):
        try:
            with mlflow.start_run():
                f1_score = metric.f1_score
                precision_score = metric.precision_score
                recall_score = metric.recall_score

                mlflow.log_param("model_name",model_name)
                mlflow.log_param("model_score",model_score)
                mlflow.log_param("f1_score",f1_score)
                mlflow.log_param("precision_score",precision_score)
                mlflow.log_param("recall_score",recall_score)

        except Exception as e:
            raise networkseacurityException(e,sys) 

    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            ## models to try of data and see which is best
            models = {
                "RandomForestClassifier":RandomForestClassifier(verbose=1),
                "GradientBoostingClassifier":GradientBoostingClassifier(verbose = 1),
                "AdaBoostClassifier":AdaBoostClassifier(),
                "LogisticRegression":LogisticRegression(verbose =1),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "KNeighborsClassifier":KNeighborsClassifier()
            }

            ## hyperparameter tuning params
            params = {
                "DecisionTreeClassifier":{'criterion':['gini','entropy','log_loss']},
                "RandomForestClassifier":{"n_estimators":[8,16,32,64,128,256]},
                "GradientBoostingClassifier":{'learning_rate':[0.1,0.01,0.05,0.001],
                                              'subsample':[0.6,0.7,0.8,0.9],
                                              'n_estimators':[8,16,32,64,128,256]},
                "LogisticRegression":{},
                "AdaBoostClassifier":{'learning_rate':[0.1,0.01,0.05,0.001],
                                      'n_estimators':[8,16,32,64,128,256]},
                "KNeighborsClassifier":{'n_neighbors':[3,5,7,9]}
            }
            
            model_report = evaluate_model(X_train, y_train, X_test, y_test, models, params)

            sorted_model_report = sorted(model_report.items(),key=lambda x:x[1]['score'], reverse=True)
            best_model = sorted_model_report[0][0]
            best_model_score = sorted_model_report[0][1]['score']
            best_model_params = sorted_model_report[0][1]['best_params']
            model = models[best_model].set_params(**best_model_params)
            model.fit(X_train,y_train)

            ## train metric
            y_train_pred = model.predict(X_train)
            classification_train_metric=get_classification_score(y_train,y_train_pred)
            ## tracking model in mlflow
            self.track_model(best_model,best_model_score,classification_train_metric)

            ## test metric
            y_test_pred = model.predict(X_test)
            classification_test_metric=get_classification_score(y_test,y_test_pred)

            ## tracking model in mlflow
            self.track_model(best_model,best_model_score,classification_test_metric)

            ##save the model
            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_dir)
            os.makedirs(model_dir_path,exist_ok=True)
            network_model = NetworkModel(preprocessor=preprocessor,model=model,param=best_model_params)
            save_object(self.model_trainer_config.model_path,network_model)

            ## save artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.model_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            return model_trainer_artifact
            
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            self.train_file_path = self.data_transformation_artifact.transformed_train_file_path
            self.test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(self.train_file_path)
            test_arr = load_numpy_array_data(self.test_file_path)

            ## split the data into X and y
            X_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            model_artifact = self.train_model(X_train,y_train,X_test,y_test)
            return model_artifact
        except Exception as e:
            raise networkseacurityException(e,sys)