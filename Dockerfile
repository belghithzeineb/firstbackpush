# Utiliser l'image de base Python
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /back

# Copier les fichiers du projet Flask dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port 5000 pour le serveur Flask
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "a.py"]