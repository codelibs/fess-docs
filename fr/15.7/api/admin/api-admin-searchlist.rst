==========================
SearchList API
==========================

Vue d'ensemble
==============

L'API SearchList est une API d'administration de |Fess| permettant de rechercher et de gérer les documents dans l'index.
Elle permet de rechercher, obtenir, créer, mettre à jour et supprimer des documents.

Tous les noms de champs dans la réponse sont en ``snake_case``. Les champs dont la valeur est ``null`` sont omis de la réponse.

URL de base
===========

::

    /api/admin/searchlist

Authentification
================

Pour appeler cette API, une authentification par jeton d'accès est requise, comme expliqué dans :doc:`api-admin-overview`.
Le jeton doit disposer des permissions d'accès à l'API d'administration (par défaut ``Radmin-api``).
Cette permission peut être modifiée via la clé de configuration ``api.admin.access.permissions``.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET / PUT
     - /docs
     - Recherche de documents
   * - GET
     - /doc/{id}
     - Obtention d'un document
   * - POST
     - /doc
     - Création d'un document
   * - PUT
     - /doc
     - Mise à jour d'un document
   * - DELETE
     - /doc/{id}
     - Suppression d'un document (par ID)
   * - DELETE
     - /query
     - Suppression de documents (par requête)

Recherche de documents
======================

Recherche les documents correspondant aux critères de recherche.

Requête
-------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Non
     - Requête de recherche (1000 caractères maximum). Si elle n'est pas spécifiée, tous les documents sont concernés.
   * - ``sort``
     - String
     - Non
     - Champ et direction de tri (ex. ``last_modified.desc``).
   * - ``start``
     - Integer
     - Non
     - Position de départ à base zéro (par défaut ``0``).
   * - ``offset``
     - Integer
     - Non
     - Décalage depuis ``start`` (par défaut ``0``).
   * - ``pn``
     - Integer
     - Non
     - Numéro de page.
   * - ``num``
     - Integer
     - Non
     - Nombre d'éléments à obtenir (par défaut ``10``). Les valeurs dépassant le maximum configuré (par défaut ``100``) ou les valeurs inférieures ou égales à ``0`` sont ramenées au maximum.
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments à obtenir (alias de ``num``, fourni pour compatibilité avec les autres API d'administration).
   * - ``lang``
     - String[]
     - Non
     - Langue de recherche. Peut être spécifié plusieurs fois (tableau). Ex. ``en``.
   * - ``ex_q``
     - String[]
     - Non
     - Expressions de requête supplémentaires. Peut être spécifié plusieurs fois (tableau).
   * - ``fields.<name>``
     - String[]
     - Non
     - Filtre par valeur de champ. Le cas le plus courant est ``fields.label`` (filtre par nom d'étiquette) ; tout ``fields.<name>`` restreint les résultats aux documents dont le champ ``<name>`` correspond à la valeur donnée. Peut être spécifié plusieurs fois.
   * - ``as.<name>``
     - String[]
     - Non
     - Conditions de recherche avancée. Tout ``as.<name>`` (ex. ``as.q``) est transmis au générateur de conditions de recherche avancée. Peut être spécifié plusieurs fois par nom.
   * - ``sdh``
     - String
     - Non
     - Hachage de document similaire (similar-document hash).

.. note::

   Cet endpoint ne prend pas en charge les facettes, la mise en évidence ou la recherche géographique. Ces paramètres sont ignorés s'ils sont spécifiés.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
            "content_description": "..."
          }
        ]
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``version``
     - Version de |Fess| en cours d'exécution (la valeur d'exemple est indicative).
   * - ``status``
     - Code de statut (``0`` en cas de succès ; voir "Codes de statut").
   * - ``query_id``
     - ID de la requête de recherche.
   * - ``docs``
     - Tableau des documents résultats de la recherche. Chaque document est une carte de noms de champs et de valeurs, utilisant les noms de champs de l'index tels quels (``doc_id``, ``url``, ``title``, ``content_description``, etc.).
   * - ``exec_time``
     - Temps d'exécution de la recherche (secondes, chaîne de caractères).
   * - ``query_time``
     - Temps de requête du moteur de recherche (millisecondes).
   * - ``page_size``
     - Nombre d'éléments par page.
   * - ``page_number``
     - Numéro de la page courante.
   * - ``record_count``
     - Nombre d'éléments correspondants.
   * - ``record_count_relation``
     - Relation du nombre d'éléments correspondants. ``eq`` indique un comptage exact, ``gte`` indique que seule la borne inférieure est connue.
   * - ``page_count``
     - Nombre total de pages.
   * - ``next_page``
     - Indique s'il existe une page suivante (bool).
   * - ``prev_page``
     - Indique s'il existe une page précédente (bool).
   * - ``start_record_number``
     - Numéro du premier enregistrement de cette page.
   * - ``end_record_number``
     - Numéro du dernier enregistrement de cette page.
   * - ``page_numbers``
     - Tableau des numéros de page à afficher dans le paginateur (chaînes de caractères).
   * - ``partial``
     - Indique si les résultats sont partiels (bool).
   * - ``search_query``
     - Requête de recherche réellement exécutée.
   * - ``requested_time``
     - Horodatage de la requête (epoch en millisecondes).
   * - ``highlight_params``
     - Chaîne de paramètres de requête pour la mise en évidence (généralement vide pour cette API d'administration).

Obtention d'un document
=======================

Obtient un seul document en spécifiant son ID de document.

Requête
-------

::

    GET /api/admin/searchlist/doc/{id}

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (valeur de ``doc_id``, paramètre de chemin).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

Si aucun document n'existe pour l'ID spécifié, une réponse d'erreur (``status`` = ``1``) est retournée.

Création d'un document
======================

Crée un nouveau document dans l'index.

Requête
-------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "Sample Page 1",
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``doc``
     - Oui
     - Document à enregistrer. Spécifié sous forme de carte de noms de champs d'index et de valeurs.

Parmi les champs spécifiés dans ``doc``, tous les champs obligatoires configurés dans ``index.admin.required.fields`` (par défaut ``url,title,role,boost``) doivent être fournis.
Contrairement à l'API :doc:`Documents API <api-admin-documents>` par lot, cet endpoint ne complète pas automatiquement les valeurs par défaut telles que ``role`` ou ``boost``, de sorte que les champs obligatoires doivent être spécifiés explicitement dans la requête.
``doc_id`` est généré automatiquement côté serveur et n'est pas spécifié lors de la création.

La valeur de chaque champ est validée en fonction de la configuration du type de champ. Si le type ne correspond pas, une erreur (``status`` = ``1``) est retournée.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Clé de configuration
     - Valeur par défaut
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - (vide)
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - (vide)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Le ``doc_id`` du document enregistré.
   * - ``created``
     - ``true`` lors de la création.

Mise à jour d'un document
=========================

Met à jour un document existant.

Requête
-------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "Updated Title",
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``doc``
     - Oui
     - Document à mettre à jour. Spécifié sous forme de carte de noms de champs d'index et de valeurs.

Le document à mettre à jour est identifié par ``doc_id`` dans ``doc``. Si ``doc_id`` n'est pas spécifié, ou si aucun document correspondant n'existe, une erreur (``status`` = ``1``) est retournée.
Comme pour la création, tous les champs obligatoires configurés dans ``index.admin.required.fields`` (par défaut ``url,title,role,boost``) doivent être fournis, et la valeur de chaque champ est validée en fonction de la configuration du type.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Le ``doc_id`` du document mis à jour.
   * - ``created``
     - ``false`` lors de la mise à jour.

Suppression d'un document (par ID)
===================================

Supprime un document en spécifiant son ID de document.

Requête
-------

::

    DELETE /api/admin/searchlist/doc/{id}

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (valeur de ``doc_id``, paramètre de chemin).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression de documents (par requête)
=======================================

Supprime en masse les documents correspondant à une requête de recherche.

Requête
-------

::

    DELETE /api/admin/searchlist/query

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Oui
     - Requête de recherche des documents à supprimer.

La cible de suppression est construite avec la même requête que "Recherche de documents", de sorte que les paramètres de filtrage tels que ``fields.<name>`` et ``ex_q`` peuvent être utilisés conjointement. Si ``q`` n'est pas spécifié, une erreur (``status`` = ``1``) est retournée.

Réponse
-------

Retourne le nombre de documents supprimés dans ``count``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

Codes de statut
===============

Le champ ``status`` dans la réponse prend l'une des valeurs suivantes.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Valeur
     - Nom
     - Description
   * - ``0``
     - OK
     - Succès.
   * - ``1``
     - BAD_REQUEST
     - La requête est invalide (champ obligatoire manquant, type incorrect, document cible introuvable, requête invalide, etc.).
   * - ``2``
     - SYSTEM_ERROR
     - Erreur système.
   * - ``3``
     - UNAUTHORIZED
     - Erreur d'authentification.
   * - ``9``
     - FAILED
     - Le traitement a échoué.

Exemples d'utilisation
======================

Recherche de documents
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention d'un document
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

Création d'un document
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

Suppression de documents par requête
-------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-documents` - API d'enregistrement en masse de documents
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
