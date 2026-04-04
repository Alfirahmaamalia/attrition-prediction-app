# 🚀 QUICK REFERENCE - Common Commands

## Virtual Environment

```bash
# Create
python -m venv env

# Activate (Windows)
env\Scripts\activate

# Activate (Linux/Mac)
source env/bin/activate

# Deactivate
deactivate

# Install requirements
pip install -r requirements.txt

# Update requirements
pip freeze > requirements.txt
```

## Flask Development

```bash
# Run locally
python app.py

# Run with specific port
python app.py --port 5000

# Debug mode (development)
FLASK_ENV=development FLASK_DEBUG=1 python app.py
```

## Model Training

```bash
# Train model
python modelling.py

# MLflow UI
python -m mlflow ui

# MLflow URL: http://localhost:5000
```

## Docker Commands

```bash
# Build image
docker buildx build --platform linux/amd64 -t <docker_username>/attrition-app:latest .

# Build without cache
docker buildx build --platform linux/amd64 -t <docker_username>/attrition-app:latest --no-cache .

# List images
docker images

# Run container locally
docker run -p 8000:8000 <docker_username>/attrition-app:latest

# Run with environment variables
docker run -p 8000:8000 -e PORT=8000 <docker_username>/attrition-app:latest

# Stop container
docker stop <container_id>

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push <docker_username>/attrition-app:latest

# Remove image
docker rmi <image_id>

# View logs
docker logs <container_id>
```

## Git Commands (for version control)

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Your message"

# Push to remote
git push origin main

# Check status
git status

# Stash changes
git stash
```

## File Management

```bash
# Create directories
mkdir data
mkdir models

# Create file
touch .env
touch .gitignore

# Copy file
cp .env.example .env

# List files
ls -la (Linux/Mac)
dir (Windows)
```

## Environment Variables (Windows)

```powershell
# Set temporary environment variable
$env:PORT = 8000

# Or in .env file
MLFLOW_TRACKING_URI=http://localhost:5000
DAGSHUB_USERNAME=your_username
DAGSHUB_TOKEN=your_token
```

## Environment Variables (Linux/Mac)

```bash
# Set temporary
export PORT=8000
export MLFLOW_TRACKING_URI=http://localhost:5000

# Or create .env file and use python-dotenv
```

## Port Management

```bash
# Check which process uses port 8000
# Windows
netstat -ano | findstr :8000

# Linux
lsof -i :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Kill process (Linux)
kill -9 <PID>
```

## Useful URLs

```
Local Flask: http://localhost:8000
MLflow UI: http://localhost:5000
DagsHub: https://dagshub.com
Railway: https://railway.app
Docker Hub: https://hub.docker.com
Google Looker: https://lookerstudio.google.com
```

## Database Queries (if applicable)

```bash
# Create/Check database exists
sqlite3 app.db "SELECT 1;"

# Or use PostgreSQL
psql -U user -d database

# Backup database
sqlite3 app.db ".dump" > backup.sql
```

## Testing Endpoints

```bash
# Using curl to test endpoints
curl http://localhost:8000/

curl http://localhost:8000/health

# With POST data
curl -X POST http://localhost:8000/predict \
  -d "age=30&monthlyIncome=5000&..."
```

## Pip Package Management

```bash
# Install specific version
pip install Flask==3.1.3

# Install from requirements
pip install -r requirements.txt

# Update package
pip install --upgrade Flask

# Uninstall package
pip uninstall Flask

# List installed packages
pip list

# Search for package
pip search gunicorn

# Show package info
pip show Flask
```

## Debugging

```bash
# Python debugging with pdb
python -m pdb app.py

# Flask debug shell
flask shell

# Check Python version
python --version

# Check installed modules
python -c "import flask; print(flask.__version__)"

# Print working directory
pwd (Linux/Mac)
cd (Windows)
```

## Performance

```bash
# Time execution
time python modelling.py

# Profile code
python -m cProfile modelling.py

# Memory usage
pip install memory-profiler
python -m memory_profiler modelling.py
```

## Common Issues & Solutions

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
python -Bc -m compileall .

# Verify installations
python -c "import flask; import sklearn; import mlflow; print('OK')"

# Force pip to use specific Python
python -m pip install -r requirements.txt

# Upgrade pip
python -m pip install --upgrade pip
```

---

**Pro Tips:**
- 💡 Gunakan `--no-cache-dir` saat pip install untuk image Docker lebih kecil
- 💡 Set `debug=False` untuk production deployment
- 💡 Gunakan environment variables untuk sensitive data (credentials)
- 💡 Test lokal terlebih dahulu sebelum deploy
- 💡 Keep requirements.txt updated dengan `pip freeze`
- 💡 Monitor Railway logs untuk debugging
- 💡 Use `.env` file dan add ke `.gitignore` untuk security

---

**Last Updated**: Maret 2026
