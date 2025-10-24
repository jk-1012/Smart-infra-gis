#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4