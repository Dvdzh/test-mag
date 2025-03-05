# Utiliser une image Python officielle
FROM python:3.9-slim

# Installer unzip
RUN apt-get update && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY setup.sh .
COPY src/ src/
COPY data/Archive.zip data/

# Donner les permissions d'exécution au script setup.sh
RUN chmod +x setup.sh

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8050
EXPOSE 8050
EXPOSE 8060

# Exécuter setup.sh puis lancer l'application
CMD ["bash", "-c", "./setup.sh"]
