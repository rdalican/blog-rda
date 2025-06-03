from flask import Flask
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def handler(request):
    """Handle a request to the Flask application."""
    with app.request_context(request):
        try:
            return app.dispatch_request()
        except Exception as e:
            return {
                "statusCode": 500,
                "body": str(e)
            } 