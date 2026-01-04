"""Gunicorn configuration file"""
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Worker processes
workers = 1
worker_class = 'sync'  # Start with sync, we'll debug async later
timeout = 0  # Disable timeout

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'

print(f"[GUNICORN CONFIG] Loaded successfully")
print(f"[GUNICORN CONFIG] Bind: {bind}")
print(f"[GUNICORN CONFIG] Workers: {workers}")
print(f"[GUNICORN CONFIG] Worker class: {worker_class}")
print(f"[GUNICORN CONFIG] Timeout: {timeout}")
