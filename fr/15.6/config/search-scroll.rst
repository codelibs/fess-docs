==================
Récupération en masse des résultats de recherche
==================

Aperçu
====

La recherche normale de |Fess| affiche uniquement un nombre limité de résultats de recherche grâce à la fonction de pagination.
Si vous souhaitez récupérer tous les résultats de recherche en une seule fois, utilisez la fonction de recherche par défilement (Scroll Search).

Cette fonction est utile lorsque vous devez traiter tous les résultats de recherche,
comme pour l'export de données en masse, les sauvegardes ou l'analyse de grandes quantités de données.

Cas d'utilisation
============

La recherche par défilement est adaptée aux utilisations suivantes :

- Export de tous les résultats de recherche
- Récupération de grandes quantités de données pour l'analyse de données
- Récupération de données dans des traitements par lots
- Synchronisation de données vers des systèmes externes
- Collecte de données pour la génération de rapports

.. warning::
   La recherche par défilement renvoie de grandes quantités de données et consomme donc
   plus de ressources serveur que la recherche normale. Activez-la uniquement si nécessaire.

Méthode de configuration
========

Activation de la recherche par défilement
----------------------

Par défaut, la recherche par défilement est désactivée pour des raisons de sécurité et de performances.
Pour l'activer, modifiez le paramètre suivant dans ``app/WEB-INF/classes/fess_config.properties`` ou ``/etc/fess/fess_config.properties``.

::

    api.search.scroll=true

.. note::
   Après avoir modifié les paramètres, vous devez redémarrer |Fess|.

Configuration des champs de réponse
--------------------------

Vous pouvez personnaliser les champs inclus dans la réponse des résultats de recherche.
Par défaut, seuls les champs de base sont renvoyés, mais vous pouvez spécifier des champs supplémentaires.

::

    query.additional.scroll.response.fields=content,mimetype,filename,created,last_modified

Pour spécifier plusieurs champs, énumérez-les séparés par des virgules.

Configuration du délai d'expiration du défilement
----------------------------

Vous pouvez configurer la durée de validité du contexte de défilement.
La valeur par défaut est de 1 minute.

::

    api.search.scroll.timeout=1m

Unités :
- ``s`` : secondes
- ``m`` : minutes
- ``h`` : heures

Méthode d'utilisation
========

Utilisation de base
----------------

L'accès à la recherche par défilement s'effectue via l'URL suivante.

::

    http://localhost:8080/json/scroll?q=mot-clé

Les résultats de recherche sont renvoyés au format NDJSON (Newline Delimited JSON).
Chaque ligne contient un document au format JSON.

**Exemple :**

::

    curl "http://localhost:8080/json/scroll?q=Fess"

Paramètres de requête
--------------------

Les paramètres suivants peuvent être utilisés pour la recherche par défilement.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nom du paramètre
     - Description
   * - ``q``
     - Requête de recherche (obligatoire)
   * - ``size``
     - Nombre d'éléments à récupérer par défilement (par défaut : 100)
   * - ``scroll``
     - Durée de validité du contexte de défilement (par défaut : 1m)
   * - ``fields.label``
     - Filtrage par étiquette

Spécification de la requête de recherche
----------------

Vous pouvez spécifier une requête de recherche comme dans une recherche normale.

**Exemple : Recherche par mot-clé**

::

    curl "http://localhost:8080/json/scroll?q=moteur de recherche"

**Exemple : Recherche par champ spécifique**

::

    curl "http://localhost:8080/json/scroll?q=title:Fess"

**Exemple : Récupération de tous les éléments (sans condition de recherche)**

::

    curl "http://localhost:8080/json/scroll?q=*:*"

Spécification du nombre d'éléments à récupérer
--------------

Vous pouvez modifier le nombre d'éléments récupérés par défilement.

::

    curl "http://localhost:8080/json/scroll?q=Fess&size=500"

.. note::
   Si le paramètre ``size`` est trop élevé, l'utilisation de la mémoire augmente.
   Il est généralement recommandé de le définir dans la plage de 100 à 1000.

Filtrage par étiquette
--------------------------

Vous pouvez récupérer uniquement les documents appartenant à une étiquette spécifique.

::

    curl "http://localhost:8080/json/scroll?q=*:*&fields.label=public"

En cas d'authentification requise
----------------

Si vous utilisez la recherche basée sur les rôles, vous devez inclure des informations d'authentification.

::

    curl -u username:password "http://localhost:8080/json/scroll?q=Fess"

Ou en utilisant un jeton API :

::

    curl -H "Authorization: Bearer YOUR_API_TOKEN" \
         "http://localhost:8080/json/scroll?q=Fess"

Format de réponse
==============

Format NDJSON
----------

La réponse de la recherche par défilement est renvoyée au format NDJSON (Newline Delimited JSON).
Chaque ligne représente un document.

**Exemple :**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

Champs de réponse
--------------------

Principaux champs inclus par défaut :

- ``url`` : URL du document
- ``title`` : Titre
- ``content`` : Corps du texte (extrait)
- ``score`` : Score de recherche
- ``boost`` : Valeur de boost
- ``created`` : Date de création
- ``last_modified`` : Date de dernière modification

Exemples de traitement de données
============

Exemple de traitement en Python
----------------

.. code-block:: python

    import requests
    import json

    # Exécution de la recherche par défilement
    url = "http://localhost:8080/json/scroll"
    params = {
        "q": "Fess",
        "size": 100
    }

    response = requests.get(url, params=params, stream=True)

    # Traitement de la réponse NDJSON ligne par ligne
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Enregistrement dans un fichier
----------------

Exemple d'enregistrement des résultats de recherche dans un fichier :

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=*:*" > all_documents.ndjson

Conversion en CSV
-----------

Exemple de conversion en CSV à l'aide de la commande jq :

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

Analyse de données
----------

Exemple d'analyse des données récupérées :

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # Lecture du fichier NDJSON
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # Conversion en DataFrame
    df = pd.DataFrame(documents)

    # Statistiques de base
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # Analyse des domaines des URL
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Performances et meilleures pratiques
==================================

Méthodes d'utilisation efficaces
----------------

1. **Configuration appropriée du paramètre size**

   - Une valeur trop petite augmente la surcharge de communication
   - Une valeur trop grande augmente l'utilisation de la mémoire
   - Recommandé : 100 à 1000

2. **Optimisation des conditions de recherche**

   - Spécifiez des conditions de recherche pour ne récupérer que les documents nécessaires
   - N'effectuez la récupération complète que si vraiment nécessaire

3. **Utilisation en heures creuses**

   - Exécutez la récupération de grandes quantités de données pendant les périodes de faible charge système

4. **Utilisation dans des traitements par lots**

   - Exécutez la synchronisation régulière de données en tant que tâches par lots

Optimisation de l'utilisation de la mémoire
--------------------

Lors du traitement de grandes quantités de données, utilisez le traitement en streaming pour réduire l'utilisation de la mémoire.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/json/scroll"
    params = {"q": "*:*", "size": 100}

    # Traitement en streaming
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # Traitement du document
                process_document(doc)

Considérations de sécurité
====================

Restrictions d'accès
------------

Étant donné que la recherche par défilement renvoie de grandes quantités de données, veuillez configurer des restrictions d'accès appropriées.

1. **Restriction par adresse IP**

   Autoriser l'accès uniquement à partir d'adresses IP spécifiques

2. **Authentification API**

   Utiliser des jetons API ou l'authentification Basic

3. **Restriction basée sur les rôles**

   Autoriser l'accès uniquement aux utilisateurs ayant des rôles spécifiques

Limitation de débit
----------

Pour éviter les accès excessifs, il est recommandé de configurer une limitation de débit sur le proxy inverse.

Dépannage
======================

La recherche par défilement n'est pas disponible
----------------------------

1. Vérifiez que ``api.search.scroll`` est défini sur ``true``.
2. Vérifiez que vous avez redémarré |Fess|.
3. Consultez les journaux d'erreurs.

Une erreur de délai d'expiration se produit
----------------------------

1. Augmentez la valeur de ``api.search.scroll.timeout``.
2. Réduisez le paramètre ``size`` pour répartir le traitement.
3. Affinez les conditions de recherche pour réduire la quantité de données récupérées.

Erreur de mémoire insuffisante
----------------

1. Réduisez le paramètre ``size``.
2. Augmentez la taille de la mémoire heap de |Fess|.
3. Vérifiez la taille de la mémoire heap d'OpenSearch.

La réponse est vide
--------------------

1. Vérifiez que la requête de recherche est correcte.
2. Vérifiez que l'étiquette ou les conditions de filtre spécifiées sont correctes.
3. Vérifiez les paramètres de permission de recherche basée sur les rôles.

Informations de référence
========

- :doc:`search-basic` - Détails de la fonction de recherche
- :doc:`search-scroll` - Paramètres liés à la recherche
- `API Scroll d'OpenSearch <https://opensearch.org/docs/latest/api-reference/scroll/>`_
