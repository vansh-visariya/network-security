from dataclasses import dataclass ## this removve the need of __init__ method


## artifact is the output of the component, this is for data ingestion
@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str

## artifact is the output of the component, this is for data validation
@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str