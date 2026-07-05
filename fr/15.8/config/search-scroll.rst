================================================
Récupération en masse des résultats de recherche
================================================

Aperçu
======

La recherche normale de |Fess| affiche uniquement un nombre limité de résultats de recherche grâce à la fonction de pagination.
Si vous souhaitez récupérer tous les résultats de recherche en une seule fois, utilisez la fonction de recherche par défilement (Scroll Search).

Cette fonction est utile lorsque vous devez traiter tous les résultats de recherche,
par exemple pour l'export de données en masse, les sauvegardes ou l'analyse de grandes quantités de données.

Cas d'utilisation
=================

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
========================

Activation de la recherche par défilement
------------------------------------------

Par défaut, la recherche par défilement est désactivée pour des raisons de sécurité et de performances.
Pour l'activer, modifiez le paramètre suivant dans ``app/WEB-INF/classes/fess_config.properties``
(ou ``/etc/fess/fess_config.properties`` pour les packages RPM/DEB).

::

    api.search.scroll=true

.. note::
   Après avoir modifié les paramètres, vous devez redémarrer |Fess|.

Durée de vie du contexte de défilement
---------------------------------------

La durée de vie du contexte de défilement est fixée en interne à ``1m`` (1 minute) dans |Fess|.
Cette valeur ne peut pas être modifiée via ``fess_config.properties``.

.. note::
   Le paramètre ``index.scroll.search.timeout`` existe, mais il est utilisé pour les traitements
   internes impliquant la mise à jour ou la suppression d'index (update by query / delete by query).
   Il n'a aucun effet sur le délai d'expiration de la présente fonctionnalité (défilement de recherche).

Configuration des champs de réponse
-------------------------------------

Vous pouvez personnaliser les champs inclus dans la réponse des résultats de recherche.
Par défaut, de nombreux champs sont renvoyés, mais vous pouvez spécifier des champs supplémentaires.

::

    query.additional.scroll.response.fields=content

Pour spécifier plusieurs champs, énumérez-les séparés par des virgules.

.. note::
   Le champ ``content`` n'est pas inclus par défaut dans la réponse.
   Ajoutez-le via le paramètre ci-dessus si vous souhaitez récupérer le texte intégral.

Méthode d'utilisation
=====================

Utilisation de base
--------------------

L'accès à la recherche par défilement s'effectue via l'URL suivante.

::

    http://localhost:8080/api/v2/documents/all?q=mot-clé

Les résultats de recherche sont renvoyés au format NDJSON (Newline Delimited JSON).
Chaque ligne contient un document au format JSON.

**Exemple :**

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess"

Paramètres de requête
----------------------

Les paramètres suivants peuvent être utilisés pour la recherche par défilement.

.. note::
   La recherche par défilement ne prend en charge que la méthode GET. Si vous accédez avec
   une méthode autre que GET, ``405 Method Not Allowed`` est renvoyé.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nom du paramètre
     - Description
   * - ``q``
     - Requête de recherche (obligatoire)
   * - ``num``
     - Nombre d'éléments à récupérer par défilement (par défaut : 10, maximum : 100)
   * - ``fields.label``
     - Filtrage par étiquette

.. note::
   La valeur maximale de ``num`` est contrôlée par ``paging.search.page.max.size`` (par défaut : 100).
   Si une valeur supérieure au maximum est spécifiée, elle est automatiquement ramenée au maximum.
   La valeur par défaut est celle de ``paging.search.page.size`` (par défaut : 10).
   Si une valeur inférieure ou égale à 0 est spécifiée pour ``num``, une erreur (``INVALID_REQUEST``) est renvoyée.

Spécification de la requête de recherche
-----------------------------------------

Vous pouvez spécifier une requête de recherche comme dans une recherche normale.

**Exemple : Recherche par mot-clé**

::

    curl "http://localhost:8080/api/v2/documents/all?q=moteur de recherche"

**Exemple : Recherche par champ spécifique**

::

    curl "http://localhost:8080/api/v2/documents/all?q=title:Fess"

**Exemple : Récupération de tous les éléments (sans condition de recherche)**

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*"

Spécification du nombre d'éléments à récupérer
------------------------------------------------

Vous pouvez modifier le nombre d'éléments récupérés par défilement.

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess&num=100"

.. note::
   Si le paramètre ``num`` est trop élevé, l'utilisation de la mémoire augmente.
   La valeur maximale par défaut est 100. Si vous avez besoin d'une valeur plus élevée,
   modifiez le paramètre ``paging.search.page.max.size``.

Filtrage par étiquette
-----------------------

Vous pouvez récupérer uniquement les documents appartenant à une étiquette spécifique.

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*&fields.label=public"

À propos du contrôle d'accès
------------------------------

.. note::
   La recherche par défilement applique également le contrôle d'accès basé sur les rôles (RBAC),
   comme la recherche normale. Seuls les documents accessibles selon les informations de rôle de la
   requête sont renvoyés ; les documents pour lesquels l'utilisateur ne dispose pas de droits de
   consultation ne sont pas inclus dans les résultats.

.. warning::
   Par défaut, l'endpoint de la recherche par défilement ne requiert pas d'authentification
   (tout le monde peut y accéder). Cependant, les documents renvoyés sont filtrés par le
   contrôle d'accès basé sur les rôles décrit ci-dessus. Si vous souhaitez restreindre l'accès
   à l'endpoint lui-même, configurez une restriction par adresse IP ou une authentification
   via un proxy inverse.

Format de réponse
=================

Format NDJSON
--------------

La réponse de la recherche par défilement est renvoyée au format NDJSON (Newline Delimited JSON).
Le Content-Type est ``application/x-ndjson; charset=UTF-8``.
Chaque ligne représente un document encapsulé dans le format ``{"data": {...}}``.

**Exemple :**

::

    {"data":{"url":"http://example.com/page1","title":"Page 1","digest":"..."}}
    {"data":{"url":"http://example.com/page2","title":"Page 2","digest":"..."}}
    {"data":{"url":"http://example.com/page3","title":"Page 3","digest":"..."}}

.. note::
   Chaque document est stocké sous la clé ``data``. Côté client, après avoir analysé chaque
   ligne, référencez la valeur de la clé ``data``.

Comportement en cas d'erreur
------------------------------

Si une erreur survient côté serveur après le début de l'envoi du flux, une ligne terminatrice
d'erreur est émise sur la dernière ligne de la réponse, comme suit :

::

    {"error":{"code":"internal_error","message":"stream error"}}

.. note::
   Côté client, vous pouvez déterminer si « le flux s'est terminé normalement » ou si
   « une erreur est survenue côté serveur en cours de traitement » en vérifiant si la
   dernière ligne contient la clé ``error``. Notez que si l'écriture de la ligne
   terminatrice d'erreur elle-même échoue, cette ligne ne sera pas émise et le flux
   se terminera en cours de route ; traitez donc également les déconnexions inattendues
   comme des erreurs.

Champs de réponse
------------------

Champs inclus par défaut :

- ``score`` : Score de recherche
- ``_id`` : Identifiant du document (identifiant de document OpenSearch)
- ``doc_id`` : Identifiant du document (interne à |Fess|)
- ``boost`` : Valeur de boost
- ``content_length`` : Taille du contenu
- ``host`` : Nom d'hôte
- ``site`` : Site
- ``last_modified`` : Date de dernière modification
- ``timestamp`` : Horodatage
- ``mimetype`` : Type MIME
- ``filetype`` : Type de fichier
- ``filename`` : Nom du fichier
- ``created`` : Date de création
- ``title`` : Titre
- ``digest`` : Extrait du corps du document
- ``url`` : URL du document
- ``thumbnail`` : Miniature
- ``click_count`` : Nombre de clics
- ``favorite_count`` : Nombre de favoris
- ``has_cache`` : Présence du cache
- ``content_title`` : Titre affiché
- ``content_description`` : Extrait affiché du corps du document
- ``url_link`` : URL du lien affiché
- ``site_path`` : Chemin du site

.. note::
   Les champs effectivement émis sont limités aux champs autorisés dans la réponse de l'API.
   Les champs sans valeur ne sont pas émis.

.. note::
   Le champ ``content`` (texte intégral) n'est pas inclus par défaut.
   Vous pouvez l'ajouter via ``query.additional.scroll.response.fields``.

Exemples de traitement de données
==================================

Exemple de traitement en Python
---------------------------------

.. code-block:: python

    import requests
    import json

    # Exécution de la recherche par défilement
    url = "http://localhost:8080/api/v2/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # Traitement de la réponse NDJSON ligne par ligne
    for line in response.iter_lines():
        if line:
            record = json.loads(line)
            if "error" in record:
                # Une erreur est survenue en cours de flux
                print("stream error:", record["error"])
                break
            doc = record["data"]
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Enregistrement dans un fichier
--------------------------------

Exemple d'enregistrement des résultats de recherche dans un fichier :

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=*:*" > all_documents.ndjson

Conversion en CSV
------------------

Exemple de conversion en CSV à l'aide de la commande jq :

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=Fess" | \
        jq -r '.data | [.url, .title, .score] | @csv' > results.csv

Analyse de données
-------------------

Exemple d'analyse des données récupérées :

.. code-block:: python

    import json
    import pandas as pd

    # Lecture du fichier NDJSON (extraction de la clé data de chaque ligne)
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            record = json.loads(line)
            if "data" in record:
                documents.append(record["data"])

    # Conversion en DataFrame
    df = pd.DataFrame(documents)

    # Statistiques de base
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # Analyse des domaines des URL
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Performances et meilleures pratiques
=====================================

Méthodes d'utilisation efficaces
----------------------------------

1. **Configuration appropriée du paramètre num**

   - Une valeur trop petite augmente la surcharge de communication
   - Une valeur trop grande augmente l'utilisation de la mémoire
   - Maximum par défaut : 100

2. **Optimisation des conditions de recherche**

   - Spécifiez des conditions de recherche pour ne récupérer que les documents nécessaires
   - N'effectuez la récupération complète que si vraiment nécessaire

3. **Utilisation en heures creuses**

   - Exécutez la récupération de grandes quantités de données pendant les périodes de faible charge système

4. **Utilisation dans des traitements par lots**

   - Exécutez la synchronisation régulière de données en tant que tâches par lots

Optimisation de l'utilisation de la mémoire
---------------------------------------------

Lors du traitement de grandes quantités de données, utilisez le traitement en streaming pour réduire l'utilisation de la mémoire.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v2/documents/all"
    params = {"q": "*:*", "num": 100}

    # Traitement en streaming
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                record = json.loads(line)
                if "error" in record:
                    break
                # Traitement du document
                process_document(record["data"])

Considérations de sécurité
============================

Restrictions d'accès
----------------------

Étant donné que la recherche par défilement renvoie de grandes quantités de données, veuillez configurer des restrictions d'accès appropriées.
L'endpoint lui-même ne requiert pas d'authentification par défaut ; envisagez les mesures suivantes si nécessaire.

1. **Restriction par adresse IP**

   Autoriser l'accès uniquement à partir d'adresses IP spécifiques

2. **Authentification API**

   Utiliser des jetons API ou l'authentification Basic via un proxy inverse

3. **Contrôle d'accès basé sur les rôles**

   Les documents renvoyés sont filtrés par le contrôle d'accès basé sur les rôles de |Fess|

Limitation de débit
---------------------

Pour éviter les accès excessifs, il est recommandé de configurer une limitation de débit sur le proxy inverse.

Dépannage
==========

La recherche par défilement n'est pas disponible
-------------------------------------------------

1. Vérifiez que ``api.search.scroll`` est défini sur ``true``.
2. Vérifiez que vous avez redémarré |Fess|.
3. Consultez les journaux d'erreurs.

Une erreur de délai d'expiration se produit
---------------------------------------------

1. Réduisez le paramètre ``num`` pour répartir le traitement.
2. Affinez les conditions de recherche pour réduire la quantité de données récupérées.

Erreur de mémoire insuffisante
--------------------------------

1. Réduisez le paramètre ``num``.
2. Augmentez la taille de la mémoire heap de |Fess|.
3. Vérifiez la taille de la mémoire heap d'OpenSearch.

La réponse est vide
--------------------

1. Vérifiez que la requête de recherche est correcte.
2. Vérifiez que l'étiquette ou les conditions de filtre spécifiées sont correctes.
3. En raison du contrôle d'accès basé sur les rôles, les documents pour lesquels l'utilisateur ne dispose pas de droits de consultation ne sont pas inclus dans les résultats. Vérifiez les paramètres de rôle de la requête.

Informations de référence
==========================

- :doc:`search-basic` - Détails de la fonction de recherche
- :doc:`search-advanced` - Paramètres liés à la recherche
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
