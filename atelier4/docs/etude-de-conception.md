# Étude de conception — LogiAI

## 1. Besoin et objectifs

LogiAI est une application de prédiction des retards de livraison. Elle exploite les caractéristiques d'une livraison pour estimer sa probabilité de retard et déterminer si une alerte doit être déclenchée.

Les objectifs sont de proposer une prédiction accessible par API, une interface web et une commande en ligne, tout en facilitant l'installation et le déploiement.

## 2. Données

Le projet utilise un jeu de données de livraisons comprenant des caractéristiques numériques et catégorielles. Les données sont utilisées pour entraîner et évaluer le modèle.

Les entrées d'une prédiction doivent respecter le schéma défini par l'API. Les données sensibles et les informations d'authentification ne doivent pas être intégrées aux exemples ou aux journaux.

## 3. Modèle et métriques

Le projet utilise un modèle de machine learning entraîné pour estimer le risque de retard. Le modèle sauvegardé est chargé par le composant de prédiction.

L'évaluation du modèle s'appuie notamment sur des métriques adaptées à la classification, telles que l'accuracy et l'AUC. Les résultats obtenus doivent être interprétés en tenant compte de la répartition des classes et du coût des faux positifs et faux négatifs.

La probabilité estimée est comparée à un seuil configurable afin de déterminer si une alerte doit être déclenchée.

## 4. Critères d'acceptation

- Les tests automatisés doivent réussir.
- L'API doit accepter les entrées valides et rejeter les entrées invalides.
- La prédiction doit renvoyer une probabilité comprise entre 0 et 1.
- Le seuil d'alerte doit être appliqué de façon cohérente.
- La commande `logiai-predict` doit fonctionner avec un fichier JSON valide.
- Le package doit pouvoir être construit sous forme de wheel.
- L'application Docker doit charger le package installé et accéder au modèle.
- Les routes protégées doivent respecter les règles d'authentification du projet.

## 5. Cycle de vie

Le cycle de vie comprend la préparation des données, l'entraînement du modèle, son évaluation, sa sauvegarde, son intégration dans l'application, puis les tests et le déploiement.

Une modification du modèle doit être accompagnée de vérifications afin de s'assurer que le format sauvegardé reste compatible avec le code de prédiction.

## 6. Architecture

L'architecture repose sur plusieurs composants :

- **Données et modèle** : les fichiers de données et le modèle entraîné sont conservés comme ressources externes au package Python.
- **Package `logiai`** : regroupe le code réutilisable de configuration, de prédiction et d'exposition de l'API.
- **API FastAPI** : reçoit les requêtes, valide les entrées et expose les résultats de prédiction.
- **Interface web** : permet à l'utilisateur d'interagir avec l'application via le navigateur.
- **Nginx** : sert d'intermédiaire pour l'accès à l'interface web et les appels vers l'API selon la configuration du projet.
- **CLI `logiai-predict`** : permet de lancer une prédiction à partir d'un fichier JSON sans utiliser directement l'API.
- **Docker Compose** : orchestre les conteneurs de l'API et de l'interface.

La variable `LOGIAI_HOME` permet de préciser le répertoire contenant les ressources nécessaires, notamment le modèle et les données. Dans le conteneur API, cette variable est définie à `/app`.

## 7. Choix technologiques

Python est utilisé pour la logique métier et le machine learning. Scikit-learn et joblib servent respectivement au modèle et à sa sauvegarde. FastAPI expose les prédictions via HTTP.

Le fichier `pyproject.toml` définit les métadonnées du package, ses dépendances, ses options facultatives et le point d'entrée de la CLI. Setuptools construit la distribution Python.

Docker et Docker Compose permettent de reproduire l'environnement de déploiement. L'installation du package dans l'image évite de dépendre d'un import direct depuis le répertoire du code source.

## 8. Risques et éthique

Les prédictions restent des estimations et ne garantissent pas qu'une livraison sera en retard. Une mauvaise qualité des données ou une évolution des conditions de transport peut dégrader les performances.

Le seuil d'alerte doit être adapté au contexte métier. Il convient de surveiller les erreurs de prédiction, de protéger les clés d'API et de limiter l'exposition des données opérationnelles.

Les utilisateurs doivent comprendre que le résultat du modèle constitue une aide à la décision, et non une certitude.

## 9. Limites

Les performances dépendent des données d'entraînement et de leur représentativité. Les résultats peuvent varier lorsque les conditions réelles diffèrent de celles observées pendant l'entraînement.

Le package Python ne contient pas automatiquement les données, le modèle ou les secrets de configuration. Ces ressources doivent être fournies séparément et leur emplacement doit être configuré.

L'application ne remplace pas le suivi réel des livraisons ni une validation métier des alertes.
