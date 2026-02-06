=========================
Démarrage rapide de l'API
=========================

Cette page fournit un guide pratique pour commencer rapidement à utiliser l'API |Fess|.

Démarrez en 5 minutes
======================

Prérequis
---------

- |Fess| est en cours d'exécution (accessible à http://localhost:8080/)
- La réponse JSON est activée dans Panneau d'administration > Système > Général

Essayez l'API de recherche
--------------------------

**Exemples de commandes curl :**

.. code-block:: bash

    # Recherche simple
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # Obtenir 20 résultats de recherche
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # Obtenir la page 2 (à partir du résultat 21)
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # Recherche avec filtre par étiquette
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # Recherche avec facettes (agrégations)
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # Recherche avec caractères spéciaux (encodés en URL)
    curl "http://localhost:8080/api/v1/documents?q=search%20engine"

**Exemple de réponse (formatée) :**

.. code-block:: json

    {
      "q": "fess",
      "exec_time": 0.15,
      "record_count": 125,
      "page_size": 20,
      "page_number": 1,
      "data": [
        {
          "title": "Fess - Open Source Enterprise Search Server",
          "url": "https://fess.codelibs.org/",
          "content_description": "<strong>Fess</strong> is an easy to deploy...",
          "host": "fess.codelibs.org",
          "mimetype": "text/html"
        }
      ]
    }

Essayez l'API de suggestion
----------------------------

.. code-block:: bash

    # Obtenir des suggestions
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # Exemple de réponse
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

Essayez l'API d'étiquettes
----------------------------

.. code-block:: bash

    # Obtenir les étiquettes disponibles
    curl "http://localhost:8080/api/v1/labels"

Essayez l'API de vérification de santé
----------------------------------------

.. code-block:: bash

    # Vérifier l'état du serveur
    curl "http://localhost:8080/api/v1/health"

    # Exemple de réponse
    # {"data":{"status":"green","cluster_name":"fess"}}

Utilisation avec Postman
=========================

L'API |Fess| peut être facilement utilisée avec Postman.

Configuration de la collection
-------------------------------

1. Ouvrez Postman et créez une nouvelle collection
2. Ajoutez les requêtes suivantes :

**API de recherche :**

- Méthode : ``GET``
- URL : ``http://localhost:8080/api/v1/documents``
- Paramètres de requête :
  - ``q`` : Mot-clé de recherche
  - ``num`` : Nombre de résultats (optionnel)
  - ``start`` : Position de départ (optionnel)

**API de suggestion :**

- Méthode : ``GET``
- URL : ``http://localhost:8080/api/v1/suggest``
- Paramètres de requête :
  - ``q`` : Chaîne de caractères saisie

**API d'étiquettes :**

- Méthode : ``GET``
- URL : ``http://localhost:8080/api/v1/labels``

Variables d'environnement
--------------------------

Nous recommandons d'utiliser les variables d'environnement Postman pour gérer les URL des serveurs.

1. Créez un nouvel environnement dans « Environnements »
2. Ajoutez la variable : ``fess_url`` = ``http://localhost:8080``
3. Modifiez l'URL de la requête en ``{{fess_url}}/api/v1/documents``

Exemples de code par langage de programmation
==============================================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # URL du serveur Fess
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Appeler l'API de recherche Fess"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # Exemple d'utilisation
    results = search("enterprise search")
    print(f"Nombre total de résultats : {results['record_count']}")
    for doc in results['data']:
        print(f"- {doc['title']}")
        print(f"  URL : {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v1/documents?${params}`);
      return response.json();
    }

    // Exemple d'utilisation
    search('enterprise search').then(results => {
      console.log(`Nombre total de résultats : ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL : ${doc.url}`);
      });
    });

JavaScript (Navigateur)
------------------------

.. code-block:: javascript

    // Utilisation de JSONP
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // Fonction de rappel
    function handleResults(results) {
      console.log(`Nombre total de résultats : ${results.record_count}`);
    }

    // Exemple d'utilisation
    search('Fess', 'handleResults');

Java
----

.. code-block:: java

    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.net.URLEncoder;
    import java.nio.charset.StandardCharsets;

    public class FessApiClient {
        private static final String FESS_URL = "http://localhost:8080";
        private final HttpClient client = HttpClient.newHttpClient();

        public String search(String query) throws Exception {
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(FESS_URL + "/api/v1/documents?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("enterprise search");
            System.out.println(result);
        }
    }

Compatibilité des versions de l'API
=====================================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Version de Fess
     - Version de l'API
     - Notes
   * - 15.x
     - v1
     - Dernière version. Support complet des fonctionnalités
   * - 14.x
     - v1
     - API similaire. Quelques différences de paramètres possibles
   * - 13.x
     - v1
     - Support basique de l'API

.. note::

   La compatibilité de l'API est maintenue, mais les nouvelles fonctionnalités ne sont disponibles que dans la dernière version.
   Pour les différences détaillées entre les versions, consultez les `Notes de version <https://github.com/codelibs/fess/releases>`__.

Dépannage
==========

L'API ne fonctionne pas
------------------------

1. **Vérifier que la réponse JSON est activée**

   Vérifiez que « Réponse JSON » est activé dans Panneau d'administration > Système > Général.

2. **Erreurs CORS depuis le navigateur**

   Si vous obtenez des erreurs CORS lors de l'accès depuis un navigateur, utilisez JSONP ou
   configurez les paramètres CORS sur le serveur.

   Exemple JSONP :

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **Authentification requise**

   Si des jetons d'accès sont configurés, incluez-les dans l'en-tête de la requête :

   .. code-block:: bash

       curl -H "Authorization: Bearer VOTRE_JETON_ACCES" \
            "http://localhost:8080/api/v1/documents?q=fess"

Prochaines étapes
==================

- :doc:`api-search` - Détails de l'API de recherche
- :doc:`api-suggest` - Détails de l'API de suggestion
- :doc:`admin/index` - Utilisation de l'API d'administration
