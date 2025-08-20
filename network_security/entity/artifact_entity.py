from dataclasses import dataclass ## this removve the need of __init__ method


## artifact is the output of the component
@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str