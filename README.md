# LogiAI : prédiction des retards de livraison

Projet de TP consacré à la prédiction du risque de retard d’une livraison à l’aide du machine learning et à l’exposition du modèle via une API REST avec FastAPI. Une interface Streamlit permet de saisir les informations d’une livraison et d’afficher la prédiction.

## 1. Environnement et installation

Créer et activer l’environnement virtuel sous Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
python -m pip install streamlit requests
```

## 2. Génération des données et entraînement du modèle

Générer le dataset :

```powershell
python -m logiai.dataset
```

Cette commande génère le fichier `data/livraisons.csv`.

Entraîner le modèle :

```powershell
python -m logiai.train
```

Les fichiers du modèle sont enregistrés dans le dossier `models/`, notamment `model.joblib` et `model_info.json`.

## 3. Lancement de l’API FastAPI

Depuis la racine du projet, lancer :

```powershell
python -m uvicorn logiai.api.main:app --reload
```

La documentation interactive de l’API est accessible à l’adresse :

http://127.0.0.1:8000/docs

### Endpoint de prédiction

- **Méthode HTTP :** `POST`
- **Route :** `/v1/predict`
- **Rôle :** recevoir les informations d’une livraison et renvoyer une estimation du risque de retard.

Les données reçues sont validées à l’aide de Pydantic. Une requête invalide peut entraîner une réponse HTTP 422. Si le modèle n’est pas disponible au moment de la prédiction, l’API renvoie une réponse HTTP 503.

## 4. Lancement de l’interface Streamlit

Dans un deuxième terminal, activer l’environnement virtuel puis lancer :

```powershell
python -m streamlit run streamlit_app.py
```

L’interface est accessible à l’adresse :

http://localhost:8501

Le serveur FastAPI doit rester actif pendant l’utilisation de l’interface Streamlit.

## 5. Tests automatisés

Exécuter les tests avec :

```powershell
python -m pytest
```

Les tests permettent de vérifier le comportement de l’API, la validation des données et les réponses attendues.

**Résultat obtenu après correction : 13 tests réussis.**

## 6. Structure du projet

```text
Logiai_starter/
├── logiai/
│   ├── api/
│   │   ├── main.py
│   │   └── schemas.py
│   ├── dataset.py
│   └── train.py
├── data/
│   └── livraisons.csv
├── models/
│   ├── model.joblib
│   └── model_info.json
├── streamlit_app.py
├── requirements.txt
└── README.md
```

Les fichiers `data/` et `models/` sont générés par les commandes du projet. Leur présence dépend de l’exécution préalable du dataset et de l’entraînement.

## 7. Technologies utilisées

- Python
- FastAPI
- Pydantic
- Streamlit
- Scikit-learn et joblib
- Pytest

## 8. Dépôt GitHub

Branche de travail : `tp-api`

Dépôt : https://github.com/lolo952/Logiai_starter
