import joblib
import os
import pytest
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to Python path

# local import 
import src.config as cfg

@pytest.fixture
def trained_model():
    return joblib.load(os.path.join(cfg.MODEL_PATH, "tfv_regression_model_fold_3.pkl"))

@pytest.fixture
def tfidf_model():
    return joblib.load(os.path.join(cfg.MODEL_PATH, "tfidf.pkl"))

def test_model_correctness(trained_model, tfidf_model):
    test_sentence = "13,000 people receive #wildfires evacuation orders in California"
    sentence_transform = tfidf_model.transform([test_sentence])
    prediction = trained_model.predict(sentence_transform)
    assert prediction == 1, "Expected prediction to be 1"