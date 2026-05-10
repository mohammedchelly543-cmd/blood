import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Si un superuser existe déjà → rien (sécurité : création unique)
if User.objects.filter(is_superuser=True).exists():
    print("✅ Superuser existe déjà — création désactivée.")
else:
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email    = os.environ.get('DJANGO_SUPERUSER_EMAIL',    'admin@bloodconnect.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin1234!')

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' créé avec succès.")
    print("🔒 Création désactivée automatiquement pour les prochains déploiements.")
