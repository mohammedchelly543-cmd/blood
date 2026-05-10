import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Vérifie si un superuser existe déjà — si oui, on ne fait RIEN (sécurité)
if User.objects.filter(is_superuser=True).exists():
    print("✅ Un superuser existe déjà. Création désactivée automatiquement.")
else:
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email    = os.environ.get('DJANGO_SUPERUSER_EMAIL',    'admin@admin.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin1234!')

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' créé avec succès.")
    print("🔒 Cette page de création est maintenant désactivée automatiquement.")
