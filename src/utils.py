# src/utils.py
import pandas as pd
from typing import Tuple, Optional

# Önerilen hedef sütun isimleri (farklı dataset'lerde değişir)
POSSIBLE_TARGETS = [
    "Temp3pm", "Temp", "Temperature (C)", "Apparent Temperature (C)", "temperature", "temp"
]

# Önerilen tarih sütun isimleri
POSSIBLE_DATE_COLS = ["Date", "date", "Formatted Date", "formatted date", "Timestamp", "timestamp"]

def load_data(path: str) -> pd.DataFrame:
    """
    CSV'den oku
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {path}")
    return df

def detect_target_column(df: pd.DataFrame) -> Optional[str]:
    """
    DataFrame içinde yukarıdaki POSSIBLE_TARGETS listesinden birini bulup döndür.
    """
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in POSSIBLE_TARGETS:
        if cand in df.columns:
            return cand
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

def detect_date_column(df: pd.DataFrame) -> Optional[str]:
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in POSSIBLE_DATE_COLS:
        if cand in df.columns:
            return cand
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

def preprocess_data(df: pd.DataFrame, target: Optional[str]=None) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Esnek preprocess:
    - Eğer target sütunu verildi veya tespit edilebiliyorsa (Temp3pm, Temp, Temperature (C) vb.)
      o sütunu hedef alır.
    - Eğer dataset'te tarih sütunu varsa, tarihten day/month/year çıkarır.
    - Eğer sadece tek sıcaklık sütunu varsa (ör: Temperature (C)), lag (önceki gün) feature ekler.
    - Eksik numeric değerleri ortalama ile doldurur.
    """
    df = df.copy()

    # numeric missing doldur
    df = df.fillna(df.mean(numeric_only=True))

    # hedef kolonu belirle
    if target:
        if target not in df.columns:
            # küçük harf eşleşmesi
            lower_map = {c.lower(): c for c in df.columns}
            if target.lower() in lower_map:
                target = lower_map[target.lower()]
            else:
                raise ValueError(f"Hedef olarak verilen sütun bulunamadı: {target}")
    else:
        target = detect_target_column(df)

    date_col = detect_date_column(df)

    # Eğer hedef Temp3pm veya Temp gibi bulunduysa - zaman bazlı özellikler ekle
    if target:
        print(f"Detected target column: {target}")
        # Eğer zaman bilgisi varsa tarihten day/month/year alın
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                df['day'] = df[date_col].dt.day
                df['month'] = df[date_col].dt.month
                df['year'] = df[date_col].dt.year
            except Exception:
                print(f"Uyarı: Tarih sütunu '{date_col}' datetime'a çevrilemedi. Devam ediliyor.")
        # feature önerisi: sayısal sütunların bir kısmını al
        # filtre: hedef hariç tüm sayısal sütunlar feature olarak kullanılacak
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if target in numeric_cols:
            numeric_cols.remove(target)
        features = numeric_cols
        if len(features) == 0:
            raise ValueError("Veride sayısal feature bulunamadı.")
        X = df[features].copy()
        y = df[target].copy()
        # eksik feature var mı? -> zaten fillna uygulandı
        return X, y

    # Eğer target yoksa ama tarih+Temp sütunu(s) varsa fallback
    if date_col and ('temp' in " ".join([c.lower() for c in df.columns])):
        # örnek daily-min-temperatures
        print("Fallback: 'Date' + 'Temp' tipinde veri tespit edildi.")
        # normalize Temp kolonu
        lower_map = {c.lower(): c for c in df.columns}
        temp_col = None
        for cand in ["temp", "temperature (c)", "temperature", "temp (c)"]:
            if cand in lower_map:
                temp_col = lower_map[cand]
                break
        if not temp_col:
            raise ValueError("Temp benzeri kolon bulunamadı.")
        df[date_col] = pd.to_datetime(df[date_col])
        df['day'] = df[date_col].dt.day
        df['month'] = df[date_col].dt.month
        df['year'] = df[date_col].dt.year
        df['Temp_prev'] = df[temp_col].shift(1).fillna(method='bfill')
        X = df[['day','month','year','Temp_prev']]
        y = df[temp_col]
        return X, y

    # Eğer hiç uygun ise kullanıcıya mevcut sütunları göster
    raise ValueError(
        "Uygun hedef sütunu bulunamadı. Veri setinde 'Temp3pm' veya 'Temp' benzeri bir sütun ya da 'Date' bulunmalı.\n"
        f"Mevcut sütunlar: {list(df.columns)}"
    )
