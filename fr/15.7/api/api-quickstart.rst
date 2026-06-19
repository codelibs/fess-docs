==========================
Démarrage rapide de l'API
==========================

Cette page fournit un guide pratique pour commencer rapidement à utiliser l'API |Fess| (v2).

Commencer en 5 minutes
=======================

Prérequis
---------

- |Fess| est en cours d'exécution (accessible à http://localhost:8080/)

Essayer l'API de recherche
---------------------------

Le point de terminaison de recherche v2 est ``GET /api/v2/search``.

**Exemples de commandes curl :**

.. code-block:: bash

    # Recherche simple
    curl "http://localhost:8080/api/v2/search?q=fess"

    # Obtenir 20 résultats de recherche (num est la taille de page ; la valeur par défaut est 10)
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # Ignorer les 20 premiers résultats (start est la position de départ, indexée à partir de 0)
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # Recherche avec filtre par étiquette
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # Recherche avec facettes (agrégations)
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # Recherche en japonais (encodé en URL)
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**Exemple de réponse (formatée) :**

Les réponses v2 sont encapsulées dans l'enveloppe ``response``.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fess",
        "record_count": 125,
        "page_size": 10,
        "page_number": 1,
        "data": [
          {
            "title": "Fess - オープンソース全文検索サーバー",
            "url": "https://fess.codelibs.org/ja/",
            "content_description": "<strong>Fess</strong>は簡単に構築できる...",
            "host": "fess.codelibs.org",
            "mimetype": "text/html"
          }
        ]
      }
    }

.. note::

   L'exemple ci-dessus est représentatif. Les champs de document inclus dans ``data`` dépendent
   de la configuration du serveur (la liste d'autorisation des champs de réponse). Pour la liste
   complète des paramètres de requête et des champs de réponse disponibles, voir :doc:`api-search`.
   Pour l'enveloppe de réponse commune, le modèle d'erreur et le CSRF, voir :doc:`api-overview`.

Essayer l'API de suggestions
------------------------------

Le point de terminaison de suggestions est ``GET /api/v2/suggest-words``.

.. code-block:: bash

    # Obtenir des suggestions
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**Exemple de réponse (formatée) :**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fes",
        "suggest_words": [
          { "text": "fess", "types": ["document"] }
        ]
      }
    }

Essayer l'API des étiquettes
------------------------------

.. code-block:: bash

    # Obtenir la liste des étiquettes disponibles
    curl "http://localhost:8080/api/v2/labels"

Essayer l'API de contrôle de santé
------------------------------------

Le point de terminaison de contrôle de santé est ``GET /api/v2/health``.

.. code-block:: bash

    # Vérifier l'état du serveur (cluster du moteur de recherche)
    curl "http://localhost:8080/api/v2/health"

**Exemple de réponse (formatée) :**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess",
          "status": "green",
          "ping_status": 200
        }
      }
    }

Utilisation avec Postman
=========================

L'API |Fess| peut être facilement utilisée avec Postman.

Configuration de la collection
-------------------------------

1. Ouvrez Postman et créez une nouvelle collection
2. Ajoutez les requêtes suivantes :

**API de recherche :**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query Parameters:
  - ``q`` : Mot-clé de recherche
  - ``num`` : Nombre de résultats (optionnel)
  - ``start`` : Position de départ (optionnel)

**API de suggestions :**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query Parameters:
  - ``q`` : Chaîne de caractères saisie

**API des étiquettes :**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

Variables d'environnement
--------------------------

Nous recommandons d'utiliser les variables d'environnement Postman pour gérer les URL des serveurs.

1. Créez un nouvel environnement dans « Environments »
2. Ajoutez la variable : ``fess_url`` = ``http://localhost:8080``
3. Modifiez l'URL de la requête en ``{{fess_url}}/api/v2/search``

Exemples de code par langage de programmation
==============================================

Tous les exemples ci-dessous appellent ``GET /api/v2/search`` et référencent l'enveloppe ``response``.

Python
------

.. code-block:: python

    import requests

    # Fess サーバーのURL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess検索APIを呼び出す"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # 使用例
    results = search("Fess 検索")
    print(f"ヒット件数: {results['response']['record_count']}")
    for doc in results["response"]["data"]:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v2/search?${params}`);
      return response.json();
    }

    // 使用例
    search('Fess 検索').then(results => {
      console.log(`ヒット件数: ${results.response.record_count}`);
      results.response.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

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
                .uri(URI.create(FESS_URL + "/api/v2/search?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("Fess 検索");
            System.out.println(result);
        }
    }

Tableau de compatibilité des versions d'API
=============================================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Version de Fess
     - Version d'API
     - Notes
   * - 15.x
     - v2
     - Dernière version. Support de toutes les fonctionnalités
   * - 14.x
     - v1
     - Ancienne API uniquement
   * - 13.x
     - v1
     - Support des fonctionnalités de base

.. note::

   Dans |Fess| 15.7, l'ancienne API de recherche JSON ``/api/v1`` et l'API de chat ont été supprimées.
   Les clients utilisant ``/api/v1`` doivent migrer vers ``/api/v2``.
   Pour les différences détaillées entre les versions, consultez les `notes de version <https://github.com/codelibs/fess/releases>`__.

Dépannage
==========

L'API ne fonctionne pas
------------------------

1. **Vérifier que |Fess| est en cours d'exécution**

   Vérifiez que http://localhost:8080/ est accessible.

2. **Vérifier que le point de terminaison est en v2**

   Vérifiez que le chemin de la requête commence par ``/api/v2/...``.
   L'ancien point de terminaison ``/api/v1`` a été supprimé.

3. **Si une authentification est requise**

   Pour les points de terminaison nécessitant une authentification, voir :doc:`api-auth`.

Prochaines étapes
==================

- :doc:`api-overview` - Spécifications communes de l'API (enveloppe de réponse, modèle d'erreur, authentification/CSRF)
- :doc:`api-search` - Détails de l'API de recherche
- :doc:`api-suggest` - Détails de l'API de suggestions
- :doc:`api-label` - Détails de l'API des étiquettes
- :doc:`api-health` - Détails de l'API de contrôle de santé
- :doc:`admin/index` - Utilisation de l'API d'administration
