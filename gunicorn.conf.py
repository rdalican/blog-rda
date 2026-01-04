"""Gunicorn configuration file"""
import os
import sys

# Get PORT from environment
port = os.environ.get('PORT', '8080')
print(f"[GUNICORN CONFIG] PORT environment variable: {os.environ.get('PORT', 'NOT SET - using default 8080')}", file=sys.stderr, flush=True)

# Server socket
bind = f"0.0.0.0:{port}"

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
