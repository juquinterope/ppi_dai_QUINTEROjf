#!/bin/bash
set -e

# Ejecutar collectstatic
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 ExploreAntioquia.wsgi:application
