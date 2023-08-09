#!/bin/sh
python manage.py collectstatic --no-input --clear
python manage.py migrate --no-input

gunicorn reminder_service.wsgi:application --bind 0.0.0.0:8000
