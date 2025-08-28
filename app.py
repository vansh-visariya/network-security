import sys,os
import pymongo
import certifi
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("MONGO_ALAS_PASS")

from network_security.exception.expection import networkseacurityException
from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File ,UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from network_security.utils.main_utils.utils import load_object
from network_security.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

ca = certifi.where()  ##It ensures that your Python application uses a trusted and up-to-date certificate authority (CA) bundle, rather than relying on potentially outdated or missing system certificates.
client = pymongo.MongoClient(url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    
if __name__ == "__main__":
    app_run(app, host="localhost", port=8080)