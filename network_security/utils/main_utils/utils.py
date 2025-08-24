import yaml
import os,sys
from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging
import numpy as np
import pickle

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise networkseacurityException(e,sys)

def write_yaml_file(file_path:str, data:object, replace:bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise networkseacurityException(e,sys)

