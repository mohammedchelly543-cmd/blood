# BloodConnect 🩸

Plateforme de gestion des dons de sang — Django 4.2

## Déploiement sur Railway

### 1. Créer le projet sur Railway

1. Aller sur [railway.app](https://railway.app) et créer un compte
2. Cliquer **New Project** → **Deploy from GitHub repo**
3. Connecter votre repo GitHub contenant ce projet

### 2. Ajouter une base de données PostgreSQL

Dans Railway, cliquer **+ Add Service** → **Database** → **PostgreSQL**  
Railway injecte automatiquement la variable `DATABASE_URL`.

### 3. Variables d'environnement à configurer

Dans Railway → votre service → **Variables** :

| Variable | Valeur |
|---|---|
| `SECRET_KEY` | Une clé aléatoire sécurisée (ex: `openssl rand -hex 32`) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `votre-app.railway.app` |

> `DATABASE_URL` est injecté automatiquement par Railway PostgreSQL.

### 4. Déploiement

Railway lance automatiquement :
- `python manage.py migrate` (via la commande `release` dans le Procfile)
- `gunicorn bloodconnect.wsgi ...` pour démarrer le serveur

### 5. Créer un super-utilisateur

Depuis Railway → votre service → **Shell** :
```bash
python manage.py createsuperuser
```

## Développement local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
