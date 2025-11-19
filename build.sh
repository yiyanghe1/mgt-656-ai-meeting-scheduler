#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate --no-input

# Create cache table (if using cache)
python manage.py createcachetable || true