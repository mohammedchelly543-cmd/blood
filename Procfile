release: python manage.py migrate --no-input && python create_superuser.py
web: gunicorn bloodconnect.wsgi --bind 0.0.0.0:$PORT --workers 2
