# 🏗️ ARCHITECTURE & SYSTEM DESIGN

## Application Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER LAYER (Browser)                       │
│  http://localhost:8000  or  https://railway-url.app/           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                             │
│                   (Flask Templates)                              │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Home Page  │  │  Dashboard   │  │ Predict Form │          │
│  │  (home.html) │  │(dashboard)   │  │(form_pred)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↑                 ↑                   ↑                  │
│         └─────────────────┴───────────────────┘                 │
│                    base.html + style.css                        │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                              │
│                      (Flask - app.py)                            │
│                                                                  │
│  @app.route('/')              → home()                          │
│  @app.route('/dashboard')     → dashboard()                     │
│  @app.route('/predict')       → predict_view()                  │
│  @app.route('/health')        → health()                        │
└──────────────┬───────────────────────────────────────────────────┘
               │
        ┌──────┼──────┬──────────────┐
        ↓      ↓      ↓              ↓
┌──────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
│                                                                  │
│  ┌────────────────────┐  ┌──────────────────────┐              │
│  │ modelling.py       │  │ model_util.py        │              │
│  │                    │  │                      │              │
│  │ • load_data()      │  │ • setup_mlflow()     │              │
│  │ • preprocess()     │  │ • load_model()       │              │
│  │ • train_model()    │  │ • save_model()       │              │
│  │ • predict()        │  │ • get_model()        │              │
│  │                    │  │ • get_features()     │              │
│  └────────────────────┘  └──────────────────────┘              │
└──────────┬──────────────────────────────────────┬────────────────┘
           │                                      │
           ↓                                      ↓
┌────────────────────────┐        ┌───────────────────────────────┐
│    DATA LAYER          │        │   ML MODEL & TRACKING         │
│                        │        │                               │
│  data/                 │        │  MLflow Local/Remote:         │
│  ├── data_clean.csv    │        │  • http://localhost:5000      │
│  │   (Input Data)      │        │  • DagsHub (Optional)         │
│  │                     │        │                               │
│  models/               │        │  Models:                      │
│  ├── model.pkl         │        │  • models/model.pkl           │
│  └── model_scaler.pkl  │        │  • MLflow registry            │
│                        │        │                               │
│  .env                  │        │  Config:                      │
│  (Environment Vars)    │        │  • MLFLOW_TRACKING_URI       │
│                        │        │  • DAGSHUB credentials       │
└────────────────────────┘        └───────────────────────────────┘
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT MACHINE                           │
│                                                                  │
│  Python Project                                                 │
│  ├── app.py                                                     │
│  ├── modelling.py                                               │
│  ├── requirements.txt                                           │
│  ├── Dockerfile                                                 │
│  └── templates/                                                 │
│      ├── home.html, dashboard.html, etc                        │
│      └── static/style.css                                       │
│                                                                  │
│  ┌─────────────────────┐         ┌────────────────────┐        │
│  │  Virtual Env        │         │  MLflow Tracking   │        │
│  │  (Local Testing)    │         │  (Local/DagsHub)   │        │
│  └─────────────────────┘         └────────────────────┘        │
└──────────────┬───────────────────────────────────────────────────┘
               │
               │ docker build
               ↓
┌──────────────────────────────────────────────────────────────────┐
│                   DOCKER IMAGE                                   │
│                   (Container Layer)                              │
│                                                                  │
│  Dockerfile → Image: <username>/attrition-app:latest            │
│  - Python 3.12-slim                                             │
│  - gunicorn + Flask                                             │
│  - All dependencies from requirements.txt                       │
│  - EXPOSE 8000                                                  │
│  - CMD: gunicorn -b 0.0.0.0:8000 app:app                      │
└──────────────┬───────────────────────────────────────────────────┘
               │
               │ docker push
               ↓
┌──────────────────────────────────────────────────────────────────┐
│              DOCKER HUB REGISTRY                                 │
│              (Image Storage)                                     │
│                                                                  │
│  Registry: <username>/attrition-app                            │
│  - Image ID: <username>/attrition-app:latest                   │
│  - Size: ~300-500MB                                             │
│  - Accessible publicly                                          │
└──────────────┬───────────────────────────────────────────────────┘
               │
               │ railway deploy
               ↓
┌──────────────────────────────────────────────────────────────────┐
│                  RAILWAY.APP (Cloud)                            │
│                  (Production Environment)                        │
│                                                                  │
│  ┌────────────────────────────────────┐                        │
│  │  Railway Project                   │                        │
│  │ ├─ Service: attrition-app          │                        │
│  │ ├─ Image: <docker-username>/...    │                        │
│  │ ├─ Port: 8000                      │                        │
│  │ ├─ Domain: https://xxx-yyy.railway.app                     │
│  │ ├─ Environment: PORT, MLFLOW_*, etc│                        │
│  │ └─ Status: Running                 │                        │
│  └────────────────────────────────────┘                        │
│                                                                  │
│  ┌────────────────────────┐  ┌───────────────────┐             │
│  │ Gunicorn WSGI Server   │  │ Flask Application │             │
│  │ :8000                  │  │ Route Handling    │             │
│  └────────────────────────┘  └───────────────────┘             │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐│
│  │ Google Looker    │  │   MLflow / DagsHub   │  │   DB (Opt)  ││
│  │  (Dashboard)     │  │   (Model Tracking)   │  │              ││
│  └──────────────────┘  └──────────────────┘  └────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Prediction Flow

```
User Input                  Flask App                Model Processing
─────────────────────────────────────────────────────────────────────

User fills                  app.route('/predict')    model_util.py
form                        POST method              get_model()
    │                            │                         │
    │─────────────────────────→ predict_view() ────────→ load_model_from_local()
    │                            │                         │
    │                        Validate Input                │
    │                            │                    or load_model_from_mlflow()
    │                        Create input dict            │
    │                            │                         │
    │                    Call modelling.predict()         │
    │                            │←────────────────────────┤
    │                            │                    Return: Model object
    │                        Process prediction           │
    │                            │                    model.predict(X)
    │                        Format result                │
    │                            │
    │←──────── Return HTML ───────┤
    │        with prediction
    │
Display Result
with recommendations
```

### Model Training Flow

```
Raw Data (CSV)               Training Pipeline              MLflow
──────────────────────────────────────────────────────────────────

data_clean.csv               modelling.py
      │
      │─→ load_data()        Read ──→ DataFrame
      │
      │─→ preprocess_data()  Clean, encode, scale
      │
      │─→ train_model()
      │     │
      │     ├─ Split data (train/test)
      │     ├─ Scale features
      │     ├─ Train RandomForest
      │     │
      │     └─ MLflow.start_run()
      │         │
      │         ├─ log_params()  ──→ Save parameters
      │         ├─ log_metrics()  ──→ Save accuracy, precision, etc
      │         ├─ log_dict()  ───→ Save feature importance
      │         ├─ log_dict()  ───→ Save model artifacts
      │         └─ sklearn.log_model()  ──→ Save model
      │
      └─→ Save locally  ──→ models/model.pkl
                       ──→ models/model_scaler.pkl
                       ──→ MLflow remote (if DagsHub configured)
```

---

## File Dependency Graph

```
                    ┌─────────────────┐
                    │  requirements.txt│
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
         ┌────────┐  ┌──────────────┐  ┌──────────┐
         │Flask   │  │MLflow, sklearn   │joblib  │
         │Gunicorn│  │pandas, numpy     │dotenv  │
         └────┬───┘  └──────┬───────┘  └────┬───┘
              │             │             │
              └─────────────┬─────────────┘
                            ↓
              ┌─────────────────────────┐
              │     app.py              │
              │  (Flask Application)    │
              └────────────┬────────────┘
                    ┌──────┴────────┐
                    ↓               ↓
         ┌──────────────────┐  ┌──────────────────┐
         │  modelling.py    │  │  model_util.py   │
         │ (ML Training)    │  │ (Model Loading)  │
         └────────┬─────────┘  └────────┬─────────┘
                  │                      │
         ┌────────┴──────────────────────┴─────────┐
         ↓                                         ↓
    ┌─────────────┐                        ┌──────────────┐
    │ data/       │                        │ models/      │
    │ *.csv       │                        │ *.pkl        │
    └─────────────┘                        └──────────────┘
         ↓                                         ↓
         │                                    mlruns/ (MLflow)
         │                                    .mlflow/
         └────────────────────┬─────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  templates/         │
                    │  - base.html        │
                    │  - home.html        │
                    │  - dashboard.html   │
                    │  - form_pred.html   │
                    │  - 404.html, 500.html│
                    └─────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  static/            │
                    │  - style.css        │
                    └─────────────────────┘
```

---

## Environment Configuration

```
┌──────────────────────────────────────────────────────────────────┐
│                  ENVIRONMENT SETUP                               │
└──────────────────────────────────────────────────────────────────┘

├── Local Development (.env)
│   ├── FLASK_ENV=development
│   ├── PORT=8000
│   ├── MLFLOW_TRACKING_URI=http://localhost:5000
│   └── (Other optional vars)
│
├── Production Railway (.env via Railway UI)
│   ├── PORT=<auto-assigned>
│   ├── MLFLOW_TRACKING_URI=https://dagshub.com/...
│   ├── DAGSHUB_USERNAME=<username>
│   └── DAGSHUB_TOKEN=<token>
│
└── Docker Runtime (Dockerfile)
    ├── ENV PYTHONUNBUFFERED=1
    ├── EXPOSE 8000
    ├── FROM python:3.12-slim
    └── CMD gunicorn...
```

---

## Request/Response Cycle

```
HTTP Request
    │
    ├─→ [1] Browser sends request to Flask
    │        └─ GET  / → load home page
    │        └─ GET  /dashboard → load dashboard
    │        └─ GET/POST /predict → predict page/submit form
    │        └─ GET  /health → health check
    │
    ├─→ [2] Flask app.py routes request
    │        └─ Matches URL to @app.route() decorator
    │        └─ Executes corresponding function
    │
    ├─→ [3] Function processes request
    │        └─ For GET: render template
    │        └─ For POST: process form, call model
    │
    ├─→ [4] Optional: Call modelling.predict()
    │        └─ Load model via model_util
    │        └─ Process input features
    │        └─ Return prediction result
    │
    ├─→ [5] Render response
    │        └─ Render template with variables
    │        └─ Include static files (CSS, JS)
    │
    └─→ [6] Send HTTP Response to Browser
             └─ HTML content (200 OK)
             └─ Or error page (404, 500)

Browser displays rendered HTML
User sees: Home / Dashboard / Prediction Result
```

---

## Scaling Considerations

```
Current Architecture (Single Instance)
┌──────────────────────┐
│   Railway App        │
│  (Single Container)  │
│   - gunicorn         │
│   - 4 workers        │
│   - ~2-5 concurrent  │
│     requests         │
└──────────────────────┘
```

If needed to scale:

```
Future Architecture (Multi-Instance)
┌──────────────────────┐
│  Load Balancer       │
│  (Railway auto)      │
└──────┬───────────────┘
       │
   ┌───┴────┬────┬─────┐
   ↓        ↓    ↓     ↓
┌────┐  ┌────┐ ┌──┐ ┌────┐
│Inst│  │Inst│ │In│ │Inst│  (Multiple instances)
│ 1  │  │ 2  │ │st│ │ 4  │
│    │  │    │ │3 │ │    │
└────┘  └────┘ └──┘ └────┘

+ Database Layer (PostgreSQL)
+ Redis Cache
+ CDN for static files
```

---

## Security Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                               │
└──────────────────────────────────────────────────────────────────┘

Layer 1: Source Code
├── .gitignore → Exclude .env, secrets
├── .dockerignore → Exclude sensitive files
└── No hardcoded credentials

Layer 2: Environment
├── .env file → Local secrets management
├── Railway Env Variables → Production secrets
├── No secrets in Docker image
└── DAGSHUB_TOKEN protected

Layer 3: Application
├── Flask debug=False (production)
├── Error handlers (don't leak stack traces)
├── Input validation
└── Request validation

Layer 4: Container
├── Python:3.12-slim → Minimal image
├── No root user
├── Read-only file system (optional)
└── Network isolation

Layer 5: Cloud
├── Railway HTTPS
├── Railway DDoS protection
├── Automatic security updates
└── Railway monitoring
```

---

## Technology Stack Summary

```
┌────────────────────────────────────────┐
│         TECHNOLOGY STACK               │
├────────────────────────────────────────┤
│ Language: Python 3.12                  │
│ Web Framework: Flask 3.1.3             │
│ WSGI Server: Gunicorn 22.0.0          │
│ ML Library: scikit-learn 1.6.1        │
│ Data: pandas 2.0.3, numpy 1.24.3     │
│ Model Tracking: MLflow 3.10.1         │
│ Containerization: Docker              │
│ Cloud Platform: Railway               │
│ Visualization: Google Looker Studio   │
│ Version Control: Git/GitHub           │
└────────────────────────────────────────┘
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE SUMMARY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input Layer:   → User Interface (Browser)                     │
│                                                                 │
│  App Layer:     → Flask Application (app.py)                   │
│                                                                 │
│  Logic Layer:   → ML Model (modelling.py, model_util.py)       │
│                                                                 │
│  Data Layer:    → CSV, Model Files, MLflow Registry            │
│                                                                 │
│  Deployment:    → Docker Container → Railway Cloud            │
│                                                                 │
│  Monitoring:    → MLflow UI → DagsHub (optional)               │
│                                                                 │
│  Integration:   → Google Looker Studio (Dashboard)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Simple, scalable, and production-ready! ✅

---

**Created**: Maret 2026  
**For**: HR Attrition Prediction - Semester 6 DSP
