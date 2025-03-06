## Table des matières
1. [Installation locale](#installation-locale)
2. [Utilisation avec Docker](#utilisation-avec-docker)

## Installation locale

### Étapes d'installation

1. Clonez le dépôt:
```bash
git clone git@github.com:Dvdzh/test-mag.git
cd test-mag
```

2. Créez un environnement virtuel (recommandé):
```bash
python -m venv venv
```

3. Activez l'environnement virtuel:
   - Sur Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Sur macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Installez les dépendances:
```bash
pip install -r requirements.txt
```

5. Lancez l'application:
```bash
python src/dashboard_1/main.py
python src/dashboard_2/main.py
```

6. Accédez à l'application dans votre navigateur:
```
http://localhost:8050
http://localhost:8060
```

## Utilisation avec Docker

### Utilisation de l'image précompilée

1. Téléchargez l'image Docker:
```bash
docker pull davidgpuless/dash-app
```

2. Lancez le conteneur:
```bash
docker run -p 8050:8050 davidgpuless/dash-app
```

3. Accédez à l'application dans votre navigateur:
```
http://localhost:8050
```

### Options de configuration Docker

Vous pouvez personnaliser le déploiement Docker avec ces options:

- **Changer le port exposé**:
```bash
docker run -p 8080:8050 davidgpuless/dash-app
```
(L'application sera accessible sur http://localhost:8080)

- **Exécution en arrière-plan**:
```bash
docker run -d -p 8050:8050 davidgpuless/dash-app
```

- **Montage des données locales**:
```bash
docker run -p 8050:8050 -v /chemin/local/vers/donnees:/app/data davidgpuless/dash-app
```
---


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
