#!/bin/sh

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.5
done
echo "Redis is up!"


python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

celery -A TomikoGroup worker -l info -P prefork &
celery -A TomikoGroup beat -l info &
celery -A TomikoGroup flower -l info &
gunicorn TomikoGroup.wsgi:application --bind 0.0.0.0:8000 &

wait