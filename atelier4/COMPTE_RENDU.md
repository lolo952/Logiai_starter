# Compte rendu : tester, sécuriser et appeler l'API LogiAI

**Nom :** Leila Souiri  **Groupe :** 3

## 1. Casser son API (activité 1)
| Cas | Requête (corps ou URL) | Prévu | Obtenu |
|---|---|---|---|
| champ manquant | VALID sans poids_kg | 422 | 422 |
| valeur absurde | poids_kg = 99999 | 422 | 422 |
| texte au lieu d'un nombre | distance_km = "abc" | 422 | 422 |
| champ en trop | Ajout de couleur = "rouge" | 422 | 422 |
| mauvaise route | POST /v1/inexistante | 404 | 404 |

- Une requête acceptée alors qu'elle devait être refusée ? Laquelle ?
Aucune parmi les cinq requêtes testées. Toutes les requêtes invalides ont été refusées avec le code HTTP attendu.

## 2. Les 2 bugs (activité 2)
| Bug | Test qui l'a révélé | Comportement avant | Correction |
|---|---|---|---|
| 1 | Test de la limite de pluie (pluie_mm = 500) | L'API acceptait une valeur de pluie supérieure à la limite autorisée. | Ajout de le=100 dans Field pour pluie_mm. |
| 2 | | | |

- Sortie de `python -m pytest` à la fin de l'activité 2 :
Nous avions relevé 24 passed, 1 warning après les corrections de sécurité et de validation.

## 3. La clé API (sprint 1)
- Ma fonction `verify_api_key()` (collez le code) :

def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """Authentification : renvoie le rôle ('user' ou 'admin') ou lève une 401."""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Clé API manquante",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if _egal(x_api_key, config.ADMIN_KEY):
        return "admin"

    if _egal(x_api_key, config.API_KEY):
        return "user"

    raise HTTPException(
        status_code=401,
        detail="Clé API invalide",
        headers={"WWW-Authenticate": "ApiKey"},
    )

| Requête | Code obtenu |
|---|---|
| `/v1/predict` sans clé | 401 |
| `/v1/predict` fausse clé | 401 |
| `/v1/predict` clé utilisateur | 200 |
| `/v1/model-info` clé utilisateur | 403 |
| `/v1/model-info` clé administrateur | 200 |
| `/health` sans clé | 200 |

- Preuve que `.env` n'est pas dans Git (sortie de `git status`) :

(.venv) PS C:\Users\USER\Logiai_starter\atelier4> git check-ignore -v .env
atelier4/.gitignore:5:.env      .env
(.venv) PS C:\Users\USER\Logiai_starter\atelier4> Test-Path .env
False

## 4. Le client web (sprint 2)
- Mon `fetch` (collez le code) :

async function appelerApi(livraison, cle) {
  const reponse = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": cle
    },
    body: JSON.stringify(livraison)
  });

  return {
    status: reponse.status,
    corps: await reponse.json()
  };
}

- Ce qui s'affiche : livraison normale / pluie de 500 mm / fausse clé :

Livraison normale : la probabilité de retard s'affiche en pourcentage avec un message indiquant si la livraison présente un risque de retard ou non.

Pluie de 500 mm : l'API renvoie une erreur HTTP 422, car la valeur dépasse la limite maximale autorisée de 100 mm.

Fausse clé : l'API renvoie une erreur HTTP 401, car la clé API est invalide.

- Expérience CORS (page servie sur le port 5501) : que disent la page et la console (F12) ? Pourquoi `curl` marche-t-il quand même ?

Lorsque la page est servie depuis le port 5501, le navigateur bloque la requête si cette origine n'est pas autorisée dans la configuration CORS de l'API. La console F12 affiche une erreur CORS et la page indique qu'il est impossible de contacter l'API. curl fonctionne quand même parce qu'il n'applique pas les restrictions CORS des navigateurs.

- Où voyez-vous la clé dans F12 ?

Dans l'onglet Network (Réseau), je sélectionne la requête /v1/predict, puis je consulte Headers (En-têtes), dans la section Request Headers. La clé apparaît dans l'en-tête X-API-Key

## 5. Questions de compréhension
1. Quelle différence entre 401, 403 et 422 ?
401 Unauthorized : la clé API est absente ou incorrecte. L'utilisateur n'est pas authentifié.
403 Forbidden : l'utilisateur est authentifié, mais il n'a pas les autorisations nécessaires.
422 Unprocessable Entity : les données envoyées ne respectent pas les règles de validation de l'API.
2. Pourquoi la clé n'est-elle ni dans le code ni dans Git ?
Pour protéger les informations sensibles et éviter que d'autres personnes puissent récupérer et utiliser la clé API. Elle est stockée dans un fichier .env local, qui est exclu de Git grâce au fichier .gitignore.
3. Pourquoi comparer avec `compare_digest` plutôt qu'avec `==` ?
compare_digest permet de comparer deux clés en limitant les fuites d'informations liées au temps d'exécution. Cela rend la comparaison plus sûre contre certaines attaques temporelles.
4. Pourquoi `curl` fonctionne-t-il alors que la page du port 5501 est bloquée ?
CORS est une politique de sécurité appliquée par les navigateurs web. curl n'applique pas cette politique et peut envoyer directement une requête HTTP à l'API, même si l'origine n'est pas autorisée par CORS.
5. Pourquoi la validation faite par le navigateur ne remplace-t-elle pas celle de l'API ?
Parce que la validation du navigateur peut être contournée ou désactivée. Un utilisateur peut envoyer directement des requêtes avec curl ou Postman. L'API doit donc vérifier elle-même toutes les données reçues pour garantir la sécurité et la fiabilité du système.

## 6. Lien de la pull request

https://github.com/lolo952/Logiai_starter/pull/3

## 7. Atelier 5 — Docker et déploiement

### 7.1 Conteneurisation

J’ai utilisé Docker pour lancer l’API LogiAI dans un conteneur et l’interface web dans un autre conteneur utilisant Nginx. Docker Compose permet de démarrer les deux services.

- API : port 8001 sur la machine hôte.
- Interface web : port 8080 sur la machine hôte.
- Nginx transmet les requêtes `/api/` à l’API.
- Les clés d’authentification sont configurées avec des variables d’environnement.

### 7.2 Tests effectués

| Test | Résultat obtenu |
|---|---|
| Démarrage avec Docker Compose | Les deux conteneurs démarrent |
| État du conteneur API | Healthy |
| Requête `/api/health` via Nginx | HTTP 200 |
| Prédiction sans clé API | HTTP 401 |
| Prédiction avec une clé valide | HTTP 200 |
| Tests automatisés avec pytest | 28 tests réussis |

### 7.3 Résultat de la prédiction

Pour un exemple de livraison, l’API a retourné les valeurs suivantes :

- Probabilité de retard : 0,732, soit 73,2 %.
- Seuil d’alerte : 0,4, soit 40 %.
- Alerte : `true`.
- Version du modèle : `1.0`.

La probabilité obtenue dépasse le seuil configuré, donc une alerte est déclenchée.

### 7.4 Conclusion

Cette activité m’a permis de conteneuriser l’API et l’interface web, de configurer Nginx comme reverse proxy et de vérifier le fonctionnement de l’authentification. Les tests confirment que l’application fonctionne dans l’environnement Docker utilisé pendant l’atelier.