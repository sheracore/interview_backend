#!/bin/bash

# Apply database migrations
python manage.py migrate
python manage.py wait_for_db

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000