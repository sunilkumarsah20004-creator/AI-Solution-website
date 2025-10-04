#!/bin/bash

# Build script for Vercel deployment
echo "Starting build process..."

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Load demo data (optional - only for first deployment)
# echo "Loading demo data..."
# python manage.py loaddata demo_data.json

echo "Build completed successfully!"

