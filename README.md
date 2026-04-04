# HR Attrition Prediction App

Aplikasi web interaktif untuk prediksi dan analisis attrition karyawan menggunakan Machine Learning dengan Flask, MLflow, dan Looker Studio.

## 📋 Fitur Utama

- **Dashboard Analitik**: Visualisasi insights attrition menggunakan Google Looker Studio
- **Form Prediksi**: Interface untuk prediksi attrition karyawan secara real-time
- **Model Management**: Model registry dan versioning menggunakan MLflow
- **Containerization**: Deployment dengan Docker
- **Remote Tracking**: Monitoring model dengan DagsHub

## 🗂️ Struktur Project

```
├── .dockerignore          # Docker ignore file
├── .gitignore            # Git ignore file
├── Dockerfile            # Docker configuration
├── Procfile              # Heroku/Railway process file
├── README.md             # Dokumentasi ini
├── app.py                # Flask application main
├── modelling.py          # Model training dan MLflow logging
├── model_util.py         # Utility untuk loading model
├── requirements.txt      # Python dependencies
├── data/
│   └── data_clean.csv    # Dataset untuk training
├── models/
│   └── model.pkl         # Trained model
├── static/
│   └── style.css         # Styling
└── templates/
    ├── base.html         # Base template
    ├── home.html         # Home page
    ├── dashboard_view.html    # Dashboard page
    └── form_prediction.html   # Prediction form page
```

## 🚀 Installation & Setup

### Prasyarat
- Python 3.12+
- pip
- virtualenv
- Docker (untuk containerization)
- Docker Hub account (untuk deployment)

### Langkah 1: Setup Virtual Environment

```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### Langkah 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Langkah 3: Setup Dataset

Pastikan file `data/data_clean.csv` sudah ada di folder project dengan struktur:
- Berisi kolom `Attrition` sebagai target
- Format CSV yang sudah ter-preprocessing

```bash
mkdir -p data
mkdir -p models
```

### Langkah 4: (Optional) Setup MLflow dengan DagsHub

1. Buat akun di [DagsHub](https://dagshub.com)
2. Buat repository baru untuk project
3. Copy `.env.example` ke `.env` dan isi dengan credentials:

```env
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
DAGSHUB_USERNAME=<your_username>
DAGSHUB_TOKEN=<your_token>
MLFLOW_EXPERIMENT_NAME=attrition-prediction
DATA_PATH=data/data_clean.csv
MODEL_PATH=models/model.pkl
```

## 🏋️ Model Training

### Training Lokal dengan MLflow

```bash
# Setup MLflow UI lokal (terminal 1)
python -m mlflow ui

# Training model (terminal 2)
python modelling.py

# Buka browser ke http://localhost:5000 untuk melihat metrics
```

### Training ke DagsHub

```bash
# Pastikan .env sudah dikonfigurasi dengan DagsHub credentials
python modelling.py

# Cek hasil di https://dagshub.com/<username>/<repo>/experiments
```

## 🌐 Menjalankan Aplikasi

### Development Mode

```bash
python app.py
```

Akses di: `http://localhost:8000`

### Production Mode (dengan Gunicorn)

```bash
gunicorn -b 0.0.0.0:8000 app:app
```

## 🎨 Integrasi Dashboard

### Setup Google Looker Dashboard

1. Export prediction results ke Google Sheet
2. Buka [Google Looker Studio](https://lookerstudio.google.com)
3. Create → Report → Add Data → Google Sheet
4. Bangun dashboard Anda dengan visualisasi
5. Share → Embed Report
6. Copy embedded iframe code

### Tambahkan Iframe ke Dashboard

1. Buka `templates/dashboard_view.html`
2. Replace komentar "PASTE POTONGAN KODE IFRAME LOOKER DISINI" dengan iframe code
3. Refresh halaman dashboard

Contoh:
```html
<iframe width="100%" height="600" 
    src="https://lookerstudio.google.com/embed/reporting/..." 
    frameborder="0" style="border:0" allowfullscreen>
</iframe>
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Deactivate virtual environment
deactivate

# Build image untuk Railway/Heroku
docker buildx build --platform linux/amd64 -t <docker_username>/attrition-app:latest .

# Test image lokal
docker run -p 8000:8000 <docker_username>/attrition-app:latest

# Push ke Docker Hub
docker push <docker_username>/attrition-app:latest
```

### Deploy ke Railway

1. Login ke [Railway.app](https://railway.app)
2. New Project → Deploy from Docker Image
3. Select Docker Image dari Docker Hub Repository
4. Configure environment variables (jika diperlukan)
5. Deploy
6. Copy provided URL

### Deploy ke Heroku

```bash
# Install Heroku CLI
# Login ke Heroku
heroku login

# Create aplikasi
heroku create <app-name>

# Push ke Heroku
git push heroku main
```

## 📊 API Routes

| Route | Method | Deskripsi |
|-------|--------|-----------|
| `/` | GET | Home page |
| `/dashboard` | GET | Dashboard Analitik |
| `/predict` | GET, POST | Form Prediksi Attrition |

## 🔧 Konfigurasi Environment Variables

Buat file `.env` di root project:

```env
# Flask
FLASK_ENV=production
PORT=8000

# MLflow (optional)
MLFLOW_TRACKING_URI=http://localhost:5000
DAGSHUB_USERNAME=
DAGSHUB_TOKEN=

# Model Configuration
DATA_PATH=data/data_clean.csv
MODEL_PATH=models/model.pkl
MLFLOW_EXPERIMENT_NAME=attrition-prediction
```

## 📈 Model Features

Model menggunakan fitur-fitur berikut untuk prediksi:

- **Age** - Usia karyawan
- **MonthlyIncome** - Penghasilan bulanan
- **YearsAtCompany** - Lama bekerja di perusahaan
- **YearsInCurrentRole** - Lama di posisi saat ini
- **YearsWithCurrManager** - Lama dengan manager saat ini
- **Department** - Departemen
- **JobRole** - Posisi pekerjaan
- **MaritalStatus** - Status pernikahan
- **OverTime** - Apakah sering lembur

## 🔍 Monitoring & Logging

### MLflow UI

```bash
python -m mlflow ui
```

Access: `http://localhost:5000`

Dapat melihat:
- Experiment dan Run history
- Metrics (Accuracy, Precision, Recall, F1-Score)
- Parameters yang digunakan
- Feature Importance
- Model Artifacts

### DagsHub Remote Tracking

- Buka repository di DagsHub
- Menu Experiments → Lihat results
- Model registry untuk versioning

## 🐛 Troubleshooting

### Model Not Found
```bash
# Pastikan file model sudah ada
ls models/model.pkl

# Atau train ulang
python modelling.py
```

### Port Already in Use
```bash
# Change port
python app.py --port 5000

# Atau kill process di port 8000
# Windows: netstat -ano | findstr :8000
# Linux: lsof -ti:8000 | xargs kill -9
```

### MLflow Connection Error
```bash
# Pastikan MLflow UI running
python -m mlflow ui

# Atau check DagsHub credentials di .env
```

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [Docker Documentation](https://docs.docker.com/)
- [Railway Deployment](https://railway.app/docs)
- [Google Looker Studio](https://support.google.com/looker-studio)

## 📝 License

This project is under [Your License Here]

## 👥 Contributors

- Your Name

---

**Dibuat untuk**: Semester 6 DSP (Digital Signal Processing / Data Science Project)
**Last Updated**: Maret 2026
