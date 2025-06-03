from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, 
           template_folder='../templates',  # Point to templates in parent directory
           static_folder='../static')       # Point to static in parent directory

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

def handler(request):
    """Handle a request to the Flask application."""
    return app(request) 