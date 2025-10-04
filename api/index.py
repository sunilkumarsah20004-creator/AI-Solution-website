"""
Vercel Serverless Function Entry Point for Django Application
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI application
from config.wsgi import app

# Vercel handler
def handler(request, response):
    return app(request, response)

# Export the application
application = app

