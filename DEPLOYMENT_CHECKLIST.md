# ✅ DEPLOYMENT CHECKLIST

## Phase 1: Local Setup & Configuration
- [ ] Virtual environment dibuat (`python -m venv env`)
- [ ] Virtual environment activated
- [ ] `pip install -r requirements.txt` berhasil
- [ ] File `.env` dibuat dari `.env.example`
- [ ] Folder `data/` ada dengan file `data_clean.csv`
- [ ] Folder `models/` dibuat

## Phase 2: Model Training & Testing

### Local Training
- [ ] `python modelling.py` berhasil dijalankan
- [ ] Model tersimpan di `models/model.pkl`
- [ ] MLflow UI aktif (`python -m mlflow ui`)
- [ ] MLflow experiments dan runs terlihat di http://localhost:5000
- [ ] Model metrics (Accuracy, Precision, Recall, F1) tercatat

### MLflow Integration (Optional - DagsHub)
- [ ] DagsHub account dibuat
- [ ] Repository DagsHub dibuat untuk project
- [ ] `.env` diupdate dengan MLflow URI DagsHub
- [ ] `.env` diupdate dengan DAGSHUB_USERNAME & DAGSHUB_TOKEN
- [ ] `python modelling.py` dijalankan ke DagsHub
- [ ] Results muncul di DagsHub Experiments dashboard

## Phase 3: Flask Application Testing

### Home Page & Navigation
- [ ] `python app.py` berhasil dijalankan
- [ ] Home page accessible di http://localhost:8000/
- [ ] Navigation bar menampilkan semua links
- [ ] Links berfungsi dengan baik

### Dashboard Integration
- [ ] Dashboard page accessible di http://localhost:8000/dashboard
- [ ] Google Sheet dengan data attrition sudah disiapkan
- [ ] Google Looker Studio dashboard dibuat
- [ ] Looker iframe code di-copy
- [ ] Iframe code di-paste ke `templates/dashboard_view.html`
- [ ] Dashboard muncul dengan benar

### Prediction Form
- [ ] Prediction form page accessible di http://localhost:8000/predict
- [ ] Semua input fields terlihat dengan benar
- [ ] Form submission bekerja
- [ ] Prediction result ditampilkan
- [ ] Error handling berfungsi (jika input invalid)

### Health Check
- [ ] Health endpoint accessible di http://localhost:8000/health
- [ ] Returns `{"status": "healthy"}` JSON response

## Phase 4: Containerization (Docker)

### Docker Setup
- [ ] Docker sudah terinstall
- [ ] Docker Hub account sudah dibuat & authenticated
- [ ] `docker login` berhasil di-execute

### Docker Build
- [ ] `Dockerfile` sudah di-review dan benar
- [ ] `.dockerignore` sudah di-review
- [ ] Docker image build berhasil: `docker buildx build --platform linux/amd64 -t <username>/attrition-app:latest .`
- [ ] Docker image muncul di `docker images`

### Docker Local Testing
- [ ] Docker container bisa di-run: `docker run -p 8000:8000 <username>/attrition-app:latest`
- [ ] Container logs tidak menunjukkan error
- [ ] http://localhost:8000 accessible via docker container
- [ ] Semua pages (Home, Dashboard, Predict) berfungsi di container
- [ ] Container bisa di-stop tanpa error

### Docker Hub Upload
- [ ] `docker push <username>/attrition-app:latest` berhasil
- [ ] Image muncul di Docker Hub repository
- [ ] Docker Hub image name documented untuk Railway deployment

## Phase 5: Cloud Deployment (Railway)

### Railway Setup
- [ ] Railway account dibuat
- [ ] Railway project dibuat
- [ ] Railway connected ke Git (opsional - jika menggunakan GitHub)

### Railway Docker Deployment
- [ ] Docker image registry source di-select (Docker Hub)
- [ ] Docker image name di-input: `<username>/attrition-app:latest`
- [ ] Railway memulai deployment
- [ ] Deployment status menjadi "Running" (bukan "Failed")
- [ ] Railway memberikan URL deployment (misal: `https://xxx-yyy.railway.app`)

### Railway Environment Variables
- [ ] Railway environment variables di-setup (jika diperlukan)
- [ ] MLFLOW_TRACKING_URI di-set (jika menggunakan DagsHub)
- [ ] DAGSHUB_USERNAME di-set (jika applicable)
- [ ] DAGSHUB_TOKEN di-set (jika applicable)

### Railway Testing
- [ ] Railway URL accessible di browser
- [ ] Home page muncul dengan benar
- [ ] Dashboard page accessible
- [ ] Prediction form page accessible
- [ ] Prediction functionality bekerja
- [ ] Error pages (404, 500) berfungsi with benar
- [ ] Health check endpoint returns success

## Phase 6: Production Validation

### Functionality Checks
- [ ] Semua links di navigation berfungsi
- [ ] Home page layout responsive (mobile, tablet, desktop)
- [ ] Dashboard visualization terlihat jelas
- [ ] Form inputs sesuai dengan model features
- [ ] Prediction results akurat dan informatif
- [ ] Styling konsisten di semua halaman

### Performance Checks
- [ ] Pages load dengan cepat (< 3 detik)
- [ ] Form submission tidak lag
- [ ] Dashboard tidak crash meski besar

### Security Checks
- [ ] Tidak ada credentials di-hardcode di code
- [ ] Environment variables digunakan untuk secrets
- [ ] `.env` di-add ke `.gitignore`
- [ ] `.dockerignore` include sensitive files
- [ ] Debug mode OFF untuk production

### Monitoring & Logging
- [ ] Railway logs dapat di-akses
- [ ] MLflow UI monitoring setup
- [ ] DagsHub monitoring setup (jika applicable)
- [ ] Error notifications framework ready

## Phase 7: Documentation & Version Control

### Git Repository
- [ ] Git repository di-initialize (jika belum)
- [ ] `.gitignore` properly configured
- [ ] Semua project files di-add ke git
- [ ] Initial commit di-push ke GitHub (optional but recommended)
- [ ] README.md di-push dengan dokumentasi lengkap

### Documentation
- [ ] README.md lengkap dengan setup instructions
- [ ] DEPLOYMENT_GUIDE.md comprehensive
- [ ] QUICK_REFERENCE.md ter-document
- [ ] Code comments sufficient untuk maintenance
- [ ] API documentation clear (jika ada custom endpoints)

## Phase 8: Post-Deployment

### Monitoring
- [ ] Railway dashboard di-check daily untuk errors
- [ ] MLflow metrics di-monitor untuk model performance
- [ ] User feedback collected untuk improvements

### Maintenance
- [ ] Model retraining schedule di-tentukan
- [ ] Update plan untuk dependencies
- [ ] Backup strategy untuk data
- [ ] Disaster recovery plan documented

### Optimization (Optional)
- [ ] Performance optimization applied
- [ ] Caching strategy implemented
- [ ] Database optimization (jika applicable)
- [ ] API rate limiting (jika applicable)

## 🎉 Final Checklist

- [ ] Project fully deployed dan accessible
- [ ] Semua features berfungsi dengan baik
- [ ] Documentation lengkap dan up-to-date
- [ ] Team training selesai (jika applicable)
- [ ] Backup & monitoring system ready
- [ ] Go-live approval received
- [ ] Production monitoring active

---

## 📊 Progress Tracking

**Start Date**: _______________  
**Deployment Date**: _______________  
**Current Phase**: _______________  
**Overall Progress %**: _____ %

### Notes:
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

### Issues Encountered:
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

### Solutions Applied:
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

**Last Updated**: Maret 2026  
**Project**: HR Attrition Prediction - Semester 6 DSP

---

## Legend:
- ✅ = Completed
- 🔄 = In Progress  
- ❌ = Failed (needs attention)
- ⏳ = Waiting for external dependency
