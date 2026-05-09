release: python manage.py migrate --no-input && python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || true
web: gunicorn bloodconnect.wsgi --bind 0.0.0.0:$PORT --workers 2
