# ADR 005 — Packaging Python et gestion des ressources

- **Statut :** accepté
- **Contexte :** Atelier 6 — industrialisation de LogiAI

## Contexte

Le code de prédiction doit être réutilisable depuis l'API et depuis une commande en ligne. Une installation dépendant uniquement du répertoire source serait moins adaptée à une distribution et à un déploiement reproductibles.

Le modèle, les données et les paramètres locaux sont des ressources qui ne doivent pas être confondues avec le code Python distribuable.

## Décisions

### 1. Utiliser `pyproject.toml`

Les métadonnées du projet, les dépendances, les options facultatives et le point d'entrée `logiai-predict` sont déclarés dans `pyproject.toml`.

Les dépendances sont déclarées avec des versions minimales. Pour une reproductibilité stricte, les versions réellement déployées doivent également être contrôlées dans le processus de construction.

### 2. Distribuer le code comme package Python

Le package est construit avec setuptools. Les formats wheel et source permettent de distribuer le code indépendamment de son environnement d'exécution.

La commande `logiai-predict` est déclarée comme point d'entrée console et utilise le composant de prédiction existant.

### 3. Séparer le code et les ressources

Le wheel contient le code du package, mais ne doit pas embarquer les fichiers de données, le modèle entraîné ni les secrets contenus dans `.env`.

La variable `LOGIAI_HOME` permet de configurer le répertoire racine des ressources nécessaires à l'exécution. Les ressources doivent être disponibles à cet emplacement.

### 4. Installer le package dans Docker

L'image Docker installe le package depuis un répertoire temporaire de construction, puis supprime ce répertoire. Les données et le modèle sont copiés séparément dans `/app`.

La variable `LOGIAI_HOME=/app` permet à l'application de retrouver ces ressources dans le conteneur.

## Conséquences

- Le code peut être installé et appelé depuis la CLI ou l'API.
- La construction du package peut être vérifiée indépendamment du démarrage de l'API.
- Le modèle et les données doivent être fournis séparément.
- Une installation isolée doit configurer `LOGIAI_HOME` si les ressources ne se trouvent pas dans le répertoire courant.
- Les fichiers de construction et les secrets ne doivent pas être ajoutés au dépôt Git.

## Vérifications

Les vérifications comprennent l'installation éditable, l'existence du point d'entrée, la construction du wheel et de l'archive source, l'exécution de la CLI et le chargement du package installé dans Docker.
