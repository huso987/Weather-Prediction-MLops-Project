# src/preprocess.py
import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
from src.utils import load_data, preprocess_data

parser = argparse.ArgumentParser()
parser.add_argument("--raw", default="data/raw/weather.csv", help="Raw CSV dosya yolu")
parser.add_argument("--out", default="data/processed/weather.pkl", help="İşlenmiş veri çıkış dosyası")
parser.add_argument("--target", default=None, help="Hedef sütun adı (opsiyonel)")
args = parser.parse_args()

RAW_DATA = args.raw
PROCESSED_DATA = args.out

os.makedirs(os.path.dirname(PROCESSED_DATA), exist_ok=True)

print("Loading data from:", RAW_DATA)
df = load_data(RAW_DATA)
print("Columns found in CSV:", list(df.columns))

try:
    X, y = preprocess_data(df, target=args.target)
except Exception as e:
    print("Error during preprocessing:", e)
    raise

print("Processed shapes -> X:", X.shape, " y:", y.shape)

joblib.dump((X, y), PROCESSED_DATA)
print(f"Processed data saved to {PROCESSED_DATA}")
