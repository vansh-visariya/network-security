from network_security.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
from network_security.exception.expection import networkseacurityException
import sys

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true,y_pred)
        precision = precision_score(y_true,y_pred)
        recall = recall_score(y_true,y_pred)
        return ClassificationMetricArtifact(f1_score=f1,
                                            precision_score=precision,
                                            recall_score=recall)
    except Exception as e:
        raise networkseacurityException(e,sys)