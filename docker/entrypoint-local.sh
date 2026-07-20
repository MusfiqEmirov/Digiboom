#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=digiboom.settings_local

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

echo "Running migrations..."
python digiboom/manage.py migrate --noinput

echo "Collecting static files..."
python digiboom/manage.py collectstatic --noinput

exec "$@"