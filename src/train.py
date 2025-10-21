import os
import joblib
from sklearn.linear_model import LinearRegression

PROCESSED_DATA = "data/processed/weather.pkl"
MODEL_PATH = "models/weather_model.pkl"

os.makedirs("models", exist_ok=True)

X, y = joblib.load(PROCESSED_DATA)

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")