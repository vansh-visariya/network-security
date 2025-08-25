from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging
import sys,os
from network_security.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class NetworkModel:
    def __init__(self,preprocessor,model,param):
        try:
            self.preprocessor = preprocessor
            self.model = model
            self.param = param
        except Exception as e:
            raise networkseacurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            model = self.model.set_params(**self.param)
            return self.model.predict(x_transform)
        except Exception as e:
            raise networkseacurityException(e,sys)