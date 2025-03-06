#!/bin/bash

echo "Démarrage de la configuration..."

# Création du dossier data si nécessaire
mkdir -p data

# Exécution des scripts de configuration Python
# choisir entre python ou python3
if command -v python3 &>/dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

$PYTHON src/setup.py
$PYTHON src/process_data.py
$PYTHON src/dashboard_1/main.py & $PYTHON src/dashboard_2/main.py

echo "Configuration terminée."