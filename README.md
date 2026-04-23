# IAM Platform

Projet de plateforme IAM sécurisée avec journalisation et analyse via Kibana.

## Technologies
- Django
- SQLite
- HTML/CSS/JS

## Structure
- accounts : authentification
- users_app : gestion utilisateurs
- roles : gestion des rôles
- logs_app : journalisation

## Lancer le projet

1. Cloner le projet
2. Créer un environnement virtuel
3. Installer les dépendances :
   pip install -r requirements.txt
4. Appliquer les migrations :
   python manage.py migrate
5. Lancer le serveur :
   python manage.py runserver
