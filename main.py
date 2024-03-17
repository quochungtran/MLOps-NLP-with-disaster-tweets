import joblib
import os
import pandas as pd
from loguru import logger
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# Creating a FAST API instance
app = FastAPI()

class DisasterReponse(BaseModel):
    disater_score: float
    is_toxic: bool

tfidf_model = joblib.load(
    os.environ.get('TFIDF_PATH')
)

clf = joblib.load(
    os.environ.get('MODEL_PATH')
)


@app.get('/')
def index():
    return {'message': 'Prediction Disaster Tweets'}

# creating an endpoint to receive the data
# to make prediction on
@app.post('/predict')
def predict(sentence: str):
    # Predict the result
    logger.info("Make prediction ...")

    sentence_transform = tfidf_model.transform([sentence])  # Pass sentence as a list
    res = clf.predict(sentence_transform)
    proba = clf.predict_proba(sentence_transform)

    return {
        'IsDisaster': int(res),
        'confidence score': float(proba[0][1])
    }