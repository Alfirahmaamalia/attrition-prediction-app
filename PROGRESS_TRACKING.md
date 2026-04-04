# 📈 Tracking Progres: Employee Attrition (Project I)

Berdasarkan pedoman project dan analisis pada workspace Anda saat ini, berikut adalah *checklist* untuk melacak langkah-langkah mana saja yang telah selesai dan yang masih perlu dikerjakan. 

Tandai dengan `[x]` untuk yang sudah selesai dan `[ ]` untuk yang belum.

## 1. Business Understanding
- [x] Memahami latar belakang masalah *attrition* di Jaya Jaya Maju
- [x] Menentukan tujuan penyelesaian masalah

## 2. Data Understanding
- [x] Mengunduh dan mengecek struktur format dataset tabular (1470 baris, 35 kolom)
- [x] Analisis tipe data & kelengkapan (identifikasi *missing value* ~28% pada target)
- [x] Melakukan Exploratory Data Analysis (EDA) univariate maupun multivariate

## 3. Data Preparation
- [x] Preprocessing: mengatasi *missing values* melalui imputasi/prediksi 
- [x] Feature selection & Balancing data jika diperlukan
- [x] Menyimpan hasil preprocessing ke dataset bersih (Terdapat file `attrition_final_fikss.csv` pada workspace)

## 4. Modeling & Evaluation
- [x] Melakukan eksperimentasi algoritma Machine Learning (`modelling.py` sudah ada)
- [x] Evaluasi dan penentuan model algoritma terbaik
- [x] *Export* hasil pemodelan ke dalam file (contoh: `.pkl`) dan disimpan di folder `model/`

## 5. Deployment Terintegrasi
### A. Dashboard Analitik
- [x] Ekspor hasil prediksi dataset (*file akhir csv*)
- [ ] Import data prediksi dari Google Sheet ke lingkungan **Google Looker Studio**
- [ ] Membuat / melengkapi visualisasi Dashboard Analitik di Google Looker
- [x] *Embed report* & mendapatkan link/kode iframe dari Looker untuk diintegrasikan ke Web App (Contoh Iframe sudah ada di `dashboard_view.html`)

### B. Web App & Dockerization
- [x] Setup struktur utama Flask Web App (`app.py`, `templates/`, `static/`, `requirements.txt`)
- [x] Pembuatan script `model_util.py` untuk mengolah dan *load* model
- [x] Menambahkan sistem routing Flask termasuk template `base.html`, `home.html`, dan `dashboard_view.html`
- [x] *Paste* kode iframe Looker ke dalam file view dashboard HTML Anda
- [x] Menyiapkan environment deployment (`Dockerfile`, `Procfile`, `.dockerignore`)
- [ ] Build & Uji coba *Image* Docker Flask App secara lokal
- [ ] Push *Image* Docker ke akun Docker Hub
- [ ] Menghubungkan Docker Hub ke platform Railway dan _Deploy_ aplikasi

## 6. Tracking / Monitoring (MLOps)
- [x] Setup virtual environment (*sukses diperbaiki/diinstal* `requirements.txt` untuk Python 3.13)
- [ ] Membuat Repository di **DagsHub**
- [x] Menyiapkan *script* untuk integrasi MLFlow di `modelling.py`
- [x] Logging & Tracking parameter, serta *metrics* model ke MLFlow Tracker UI lokal (port 5000)
- [ ] Push log MLFlow, artifacts & tracking ke Remote DagsHub (*Serving*)
- [ ] Fetching (mengambil) Model Registry terbaru via script `model_util.py` langsung dari MLFlow Dagshub uri.

---
> **Catatan AI**: Daftar di atas dibuat secara otomatis dari pengamatan awal workspace Anda (`app.py`, `modelling.py`, `attrition_final_fikss.csv`, dan Docker config sudah tercatat). Silakan sesuaikan (ubah `[ ]` menjadi `[x]`) apabila ada tahapan seperti setting Dagshub atau Setup Dashboard Looker yang sebenarnya sudah Anda selesaikan di luar workspace ini secara manual!
