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

<img width="317" height="291" alt="Screenshot from 2025-10-21 17-30-59" src="https://github.com/user-attachments/assets/a591b728-70cd-4f4d-a2f4-b44b6e8773e9" />


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

