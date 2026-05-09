import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME') or 'admin'
email = os.environ.get('DJANGO_SUPERUSER_EMAIL') or 'admin@admin.com'
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD') or 'Admin1234!'

if not username:
    print("DJANGO_SUPERUSER_USERNAME non défini, superuser non créé.")
elif User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' existe déjà.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' créé avec succès.")
