# 🌤 Weather Prediction MLops Project

## 🔹 Proje Hakkında
Bu proje, **hava tahmini (Temperature 3pm)** için basit bir **MLops pipeline** örneğidir.  
Proje, veri ön işleme, model eğitimi, API ile tahmin ve Docker tabanlı dağıtımı içerir.

**Özellikler:**
- CSV veri setinden veri yükleme ve ön işleme
- Basit regresyon modeli (örnek: RandomForest, XGBoost vs.)
- FastAPI ile REST API oluşturma
- Docker ile containerize edilmiş inference servisi
- DVC ile veri ve model yönetimi (opsiyonel)
- Test için örnek JSON input/output

---

## 🔹 Dosya Yapısı

weather-mlops/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml (opsiyonel)
├── src/
│ ├── app.py # FastAPI inference
│ ├── preprocess.py # veri hazırlama
│ ├── train.py # model eğitimi
│ ├── utils.py # helper fonksiyonlar
├── data/
│ ├── raw/ # raw dataset
│ └── processed/ # işlenmiş dataset
├── models/ # eğitilmiş model
└── leetcode_solutions/ # (opsiyonel)

## 🔹 Kurulum

# 1. Repo’yu klonla:

git clone git@github.com:huso987/Weather-Prediction-MLops-Project.git
cd weather-mlops

# 2.Virtual environment oluştur:

python3 -m venv env
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows

# 3.Gereksinimleri yükle:

pip install -r requirements.txt
