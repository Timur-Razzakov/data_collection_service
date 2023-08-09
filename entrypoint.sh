#!/bin/sh
python manage.py collectstatic --no-input --clear
python manage.py migrate --no-input

gunicorn referal_system.wsgi:application --bind 0.0.0.0:8000
