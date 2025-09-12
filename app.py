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
from network_security.utils.ml_utils.model.estimator import NetworkModel
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

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./template")

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
       raise networkseacurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        model = load_object("artifacts/08_28_2025_21_30_12/model_trainer/trained_model/model.pkl")
        preprocessor = load_object("artifacts/08_28_2025_21_30_12/data_transformation/transformed_object/preprocessed_object.pkl")
        network_model = NetworkModel(preprocessor=preprocessor,model=model.model,param=model.param)

        prediction = network_model.predict(df)
        df['predicted_column'] = prediction
        
        os.makedirs("prediction_output", exist_ok=True) 
        df.to_csv("prediction_output/output.csv")

        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table":table_html})
    except Exception as e:
        raise networkseacurityException(e,sys)
    
if __name__ == "__main__":
    app_run(app, host="localhost", port=8080)