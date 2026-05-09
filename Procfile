release: python manage.py migrate --no-input
web: python create_superuser.py && gunicorn bloodconnect.wsgi --bind 0.0.0.0:$PORT --workers 2
