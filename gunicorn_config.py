import os

# Ambil binding port otomatis dari environment Railway, default fallback 8000
port = int(os.environ.get("PORT", 8000))
bind = f"0.0.0.0:{port}"
workers = 2
