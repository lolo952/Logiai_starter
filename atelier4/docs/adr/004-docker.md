# ADR 004 — Conteneurisation de LogiAI

- **Statut :** Accepté
- **Date :** 11 novembre 2026

## Contexte

L'application LogiAI possède une API FastAPI qui réalise les prédictions de retard des livraisons et une interface web. Nous souhaitons faciliter son lancement et séparer le serveur API du serveur web.

## Décision

Nous utilisons Docker pour exécuter l'API dans un conteneur et Nginx dans un second conteneur.

- L'API utilise FastAPI et Uvicorn sur le port 8000 dans le conteneur.
- Nginx sert l'interface web sur le port 80 dans son conteneur.
- Les ports 8001 et 8080 permettent respectivement d'accéder à l'API et à l'interface depuis la machine hôte.
- Nginx transmet les requêtes `/api/` au service `api`.
- Docker Compose démarre les deux services et attend que le contrôle de santé de l'API réussisse avant de démarrer le service web.
- Les clés d'authentification sont fournies par le fichier `.env`, qui ne doit pas être versionné.

## Conséquences

Cette architecture sépare l'interface web de l'API et permet de démarrer les deux services avec Docker Compose. Le reverse proxy permet au navigateur d'utiliser une même origine pour l'interface et les requêtes API.

Les clés d'authentification doivent être configurées dans l'environnement. Les ports publiés facilitent les tests locaux, mais ne constituent pas à eux seuls une configuration de déploiement sécurisé en production.

## Vérifications

- Contrôle de santé de l'API : HTTP 200.
- Reverse proxy `/api/health` : HTTP 200.
- Prédiction sans clé : HTTP 401.
- Prédiction avec une clé valide : HTTP 200.
- Tests automatisés : 28 tests réussis.
