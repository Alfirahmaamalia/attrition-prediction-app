# 📋 PANDUAN LENGKAP DEPLOYMENT MODEL ATTRITION PREDICTION

## 🎯 Status Implementasi

Semua file dan struktur project telah disiapkan sesuai dengan instruksi deployment tahap lanjut. Berikut adalah overview lengkapnya:

---

## ✅ Yang Sudah Dikerjakan

### 1. **App Configuration & Main Files**
- ✅ `app.py` - Updated dengan port management sesuai Railway/Heroku
- ✅ `modelling.py` - Model training dengan MLflow logging dan DagsHub integration
- ✅ `model_util.py` - Utility functions untuk loading model dari lokal/MLflow

### 2. **HTML Templates**
- ✅ `base.html` - Base template dengan navigation
- ✅ `home.html` - Home page dengan informasi & fitur aplikasi
- ✅ `dashboard_view.html` - Dashboard dengan placeholder iframe Looker
- ✅ `form_prediction.html` - Form prediksi attrition yang comprehensive
- ✅ `404.html` - Error page 404
- ✅ `500.html` - Error page 500

### 3. **Deployment Files**
- ✅ `Dockerfile` - Docker configuration untuk Railway
- ✅ `.dockerignore` - Docker ignore patterns
- ✅ `Procfile` - Process file untuk Heroku/Railway
- ✅ `.gitignore` - Git ignore patterns
- ✅ `.env.example` - Environment variables template

### 4. **Configuration**
- ✅ `requirements.txt` - Updated dengan gunicorn, MLflow, scikit-learn
- ✅ `static/style.css` - Comprehensive styling untuk aplikasi
- ✅ `README.md` - Dokumentasi lengkap

---

## 📱 Next Steps - Yang Perlu Dilakukan

### **BAGIAN 1: Persiapan & Testing Lokal**

#### Step 1: Setup Environment

```bash
# 1. Buat virtual environment (jika belum)
python -m venv env

# 2. Activate environment
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

#### Step 2: Prepare Data

```bash
# Pastikan data sudah ada:
# - mkdir data (jika folder belum ada)
# - Letakkan file CSV di: data/data_clean.csv
# - File harus memiliki kolom 'Attrition' sebagai target

# Create model folder
mkdir models
```

#### Step 3: Train Model (Lokal)

```bash
# Terminal 1: Start MLflow UI
python -m mlflow ui
# Akses: http://localhost:5000

# Terminal 2: Train model
python modelling.py

# Model akan disimpan di: models/model.pkl
```

#### Step 4: Setup Google Looker Dashboard

1. **Export Prediction Data ke Google Sheet:**
   - Buat script Python untuk generate sample predictions dan export ke CSV
   - Upload ke Google Sheet
   - Beri nama spesifik: "Data Attrition HR [Company Name]"

2. **Buat Looker Dashboard:**
   - Buka https://lookerstudio.google.com
   - Create → Report (Blank)
   - Add Data → Google Sheets → Select sheet Anda
   - Buat visualisasi (bar chart, pie chart, dll)
   - Share → Embed Report → Copy iframe code

3. **Update dashboard_view.html:**
   - Buka `templates/dashboard_view.html`
   - Replace komentar dengan iframe code dari Looker

#### Step 5: Test Aplikasi Lokal

```bash
# Jalankan Flask app
python app.py

# Akses di browser:
# - http://localhost:8000              (Home)
# - http://localhost:8000/dashboard   (Dashboard)
# - http://localhost:8000/predict     (Form Prediksi)

# Test health check:
# - http://localhost:8000/health
```

---

### **BAGIAN 2: Integration dengan MLflow & DagsHub**

#### Step 1: Setup DagsHub Account

```text
1. Go to https://dagshub.com
2. Create new account (bisa pakai GitHub login)
3. Create new repository untuk project ini
4. Copy MLflow URI dari: Remote → Experiments → MLFlow Tracking remote
5. Generate token dari: Profile → Settings → Tokens
```

#### Step 2: Konfigurasi Environment Variables

```bash
# 1. Buat .env di root project
cp .env.example .env

# 2. Edit .env dan isi dengan DagsHub credentials:
# MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
# DAGSHUB_USERNAME=<your_username>
# DAGSHUB_TOKEN=<your_token>
# MLFLOW_EXPERIMENT_NAME=attrition-prediction
# DATA_PATH=data/data_clean.csv
# MODEL_PATH=models/model.pkl
```

#### Step 3: Train & Log ke DagsHub

```bash
# Pastikan .env sudah dikonfigurasi
python modelling.py

# Cek hasil di: https://dagshub.com/<username>/<repo>/experiments
# Lihat metrics, parameters, dan artifacts
```

---

### **BAGIAN 3: Containerization dengan Docker**

#### Step 1: Test Docker Lokal

```bash
# 1. Deactivate venv
deactivate

# 2. Build Docker image
docker buildx build --platform linux/amd64 -t <docker_username>/attrition-app:latest .

# 3. Test menjalankan container lokal
docker run -p 8000:8000 <docker_username>/attrition-app:latest

# 4. Test di browser: http://localhost:8000
```

#### Step 2: Push ke Docker Hub

```bash
# 1. Login ke Docker Hub di terminal
docker login

# 2. Push image
docker push <docker_username>/attrition-app:latest

# 3. Verify di https://hub.docker.com
# Cek bahwa image sudah ter-push dengan tag :latest
```

---

### **BAGIAN 4: Deployment ke Railway**

#### Step 1: Setup Railway Account

```text
1. Go to https://railway.app
2. Login/Create account (bisa pakai GitHub)
3. Create new project
```

#### Step 2: Deploy Docker Image

```text
1. New Project → Deploy from Docker Image
2. Registy Source: select Docker Hub
3. Image: <docker_username>/attrition-app:latest
4. Railway akan otomatis pull dan deploy image
5. Tunggu hingga deployment complete (status: "Running")
```

#### Step 3: Konfigurasi Environment Variables di Railway

```text
1. Go ke Railway Project → Variables
2. Tambahkan (jika menggunakan DagsHub):
   - MLFLOW_TRACKING_URI=https://dagshub.com/...
   - DAGSHUB_USERNAME=...
   - DAGSHUB_TOKEN=...
3. Save
```

#### Step 4: Deploy & Test

```text
1. Railway akan auto-deploy setelah .env disave
2. Copy URL yang diberikan Railway
3. Test di browser dengan URL tersebut
4. Akses: https://[railway-url]/dashboard
```

---

### **BAGIAN 5: Monitoring & Maintenance**

#### MLflow Monitoring (Lokal)

```bash
# Lihat metrics & artifacts lokal
python -m mlflow ui
# http://localhost:5000
```

#### DagsHub Monitoring (Remote)

```text
1. Go ke https://dagshub.com/<username>/<repo>
2. Menu "Experiments" → lihat runs
3. Inspect: parameters, metrics, model artifacts
4. Model registry untuk production versioning
```

#### Railway Logs Monitoring

```text
1. Go ke Railway Project
2. View deployment logs
3. Debug jika ada error
```

---

## 🔧 Konfigurasi Model Features

Update `model_util.py` dan `modelling.py` dengan fitur yang sesuai dataset Anda:

```python
# Di model_util.py - get_feature_names()
features = [
    'Age',
    'MonthlyIncome',
    'YearsAtCompany',
    'YearsInCurrentRole',
    'YearsWithCurrManager',
    'Department',
    'JobRole',
    'MaritalStatus',
    'OverTime',
    # Tambahkan fitur lainnya sesuai dataset
]

# Di modelling.py - preprocess_data()
# Sesuaikan target_column dengan nama kolom di dataset:
target_column = 'Attrition'  # atau nama lain
```

---

## 📊 Testing Checklist

- [ ] Virtual environment setup berhasil
- [ ] `pip install -r requirements.txt` berhasil
- [ ] `python modelling.py` berhasil train & save model
- [ ] `python app.py` berjalan di localhost:8000
- [ ] Home page, Dashboard, Predict form bisa diakses
- [ ] Form prediksi bisa submit & get hasil
- [ ] Google Looker Dashboard embed di dashboard_view.html
- [ ] MLflow UI menampilkan experiment & runs
- [ ] DagsHub remote tracking menampilkan metrics (opsional)
- [ ] Docker image build & run berhasil lokal
- [ ] Docker image push ke Docker Hub berhasil
- [ ] Deployment di Railway berhasil
- [ ] URL Railway bisa diakses di browser
- [ ] Semua halaman bisa diakses via Railway URL

---

## 🐛 Troubleshooting

### Port 8000 sudah terpakai

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
lsof -ti:8000 | xargs kill -9
```

### Model tidak ditemukan

```bash
# Pastikan model sudah di-train
python modelling.py
# Cek file ada di: models/model.pkl
```

### Error import modelling di app.py

```bash
# Pastikan modelling.py ada dan tidak ada syntax error
# Test run modelling.py langsung:
python modelling.py
```

### Docker build gagal

```bash
# Clear Docker cache dan build ulang
docker builder prune
docker buildx build --platform linux/amd64 -t <docker_username>/attrition-app:latest --no-cache .
```

### Railway deployment gagal

```text
1. Check Railway logs untuk error message
2. Pastikan Dockerfile correct dan image bisa run lokal
3. Pastikan port environment variable sudah di-set
4. Try rebuild & redeploy dari Railway dashboard
```

---

## 📞 Reference & Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **MLflow Docs**: https://mlflow.org/docs/latest/
- **Docker Docs**: https://docs.docker.com/
- **Railway Docs**: https://railway.app/docs
- **Google Looker Studio**: https://support.google.com/looker-studio
- **DagsHub**: https://dagshub.com

---

## 📝 Catatan Tambahan

1. **Performance Optimization**: Jika model besar, pertimbangkan model compression atau caching
2. **Security**: Update `.env` dengan credentials yang aman, jangan commit ke git
3. **Scaling**: Jika traffic tinggi, gunakan Railway paid plan atau cloud provider lain
4. **Continuous Integration**: Pertimbangkan setup GitHub Actions untuk auto-deploy
5. **Monitoring Production**: Setup error tracking (Sentry) untuk production monitoring

---

## ✨ Summary

Project Anda sudah fully configured untuk deployment! Semua files dan infrastructure sudah siap. Sekarang tinggal:

1. ✅ Prepare data & train model lokal
2. ✅ Setup Google Looker dashboard
3. ✅ Configure Docker & test lokal
4. ✅ Push ke Docker Hub
5. ✅ Deploy ke Railway

Semua instruksi sudah lengkap di atas. Selamat berhasil dengan deployment! 🚀

---

**Created**: Maret 2026  
**For**: Semester 6 DSP Project - HR Attrition Prediction  
**Status**: Ready for Deployment ✅
