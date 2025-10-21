from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

MODEL_PATH = "models/weather_model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Weather Prediction API")

class WeatherInput(BaseModel):
    MinTemp: float
    MaxTemp: float
    Rainfall: float
    Evaporation: float
    Sunshine: float
    WindGustSpeed: float
    Humidity9am: float
    Humidity3pm: float
    Pressure9am: float
    Pressure3pm: float
    Temp9am: float

@app.post("/predict/")
def predict(input: WeatherInput):
    df = pd.DataFrame([input.dict()])
    prediction = model.predict(df)[0]
    return {"PredictedTemp3pm": float(prediction)}