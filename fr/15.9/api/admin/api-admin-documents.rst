==========================
Documents API
==========================

Vue d'ensemble
==============

L'API Documents est une API d'administration de |Fess| permettant d'enregistrer en masse des documents dans l'index.
Elle permet aux systèmes externes d'ajouter directement des documents à l'index sans passer par le moteur de crawl.
Plusieurs documents peuvent être enregistrés en une seule requête.

URL de base
===========

::

    /api/admin/documents

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
   * - PUT
     - /bulk
     - Enregistrement en masse de documents

.. note::

   Cet endpoint accepte uniquement la méthode ``PUT``.

Enregistrement en masse de documents
=====================================

Enregistre plusieurs documents dans l'index en une seule fois.

Requête
-------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "Page d'exemple 1",
          "content": "Voici le texte du corps de la page 1."
        },
        {
          "url": "https://example.com/page2",
          "title": "Page d'exemple 2",
          "content": "Voici le texte du corps de la page 2."
        }
      ]
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``documents``
     - Oui
     - Tableau des documents à enregistrer. Chaque document est spécifié sous forme de correspondance entre nom de champ et valeur. Si la valeur est ``null`` ou un tableau vide, une erreur est retournée (``status`` = ``1``).

Champs du document
~~~~~~~~~~~~~~~~~~

Chaque document peut spécifier librement les champs de l'index sous forme de correspondance entre nom et valeur.
Au minimum, ``url`` et ``title`` doivent être spécifiés (conformément au paramètre
``index.admin.required.fields``. La valeur par défaut est ``url,title,role,boost`` ;
``role`` et ``boost`` étant complétés automatiquement comme indiqué ci-après, seuls ``url`` et ``title`` sont en pratique obligatoires).

Les champs suivants sont complétés automatiquement lorsqu'ils sont omis :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur par défaut en cas d'omission
   * - ``content_length``
     - Somme du nombre de caractères de ``title`` et de ``content``
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - Rôle de recherche invité (rôle de recherche configuré pour les utilisateurs invités)
   * - ``last_modified``
     - Heure actuelle
   * - ``timestamp``
     - Heure actuelle

De plus, les champs suivants sont générés automatiquement lors de l'enregistrement :

- ``id`` - Généré de façon déterministe à partir de l'``url`` du document (ainsi que de ``role`` et ``virtual_host``),
  et utilisé comme identifiant de document OpenSearch (``_id``). Cette valeur est retournée dans ``items[].id`` de la réponse.
- ``doc_id`` - Un UUID aléatoire est généré à chaque enregistrement et stocké comme champ du document.

.. note::

   Comme ``id`` est généré de façon déterministe à partir de l'``url``, l'enregistrement d'un document
   avec le même ``url`` mettra à jour le document existant
   (``items[].result`` aura la valeur ``OK``).

Remarques
~~~~~~~~~

- Si le champ ``lang`` contient ``"auto"``, la langue est détectée automatiquement à partir du contenu.
- Si ``config_id`` est spécifié, le pipeline d'ingestion (ingest pipeline) de la configuration de crawl correspondante est appliqué.
- Si la génération de miniatures est activée (``thumbnail.crawler.enabled``), une tentative de génération de miniature est effectuée lors de l'enregistrement.
- La valeur de chaque champ est validée en fonction du type de champ configuré (``index.admin.array.fields``,
  ``index.admin.date.fields``, ``index.admin.long.fields``, etc.).
  Si le type ne correspond pas, une erreur est retournée (``status`` = ``1``).

Réponse
-------

La réponse retourne le résultat du traitement de chaque document enregistré dans un tableau ``items``.
Les éléments traités avec succès contiennent ``result`` et ``id`` ; les éléments en échec contiennent ``result`` et ``message``.

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

Si ``status`` est ``0``, cela indique que tous les documents ont été enregistrés avec succès.
``items[].result`` est ``CREATED`` lors d'une création, et ``OK`` lors de la mise à jour d'un document existant.

Si l'enregistrement échoue pour l'un des éléments, ``status`` devient ``9`` (FAILED) et
l'élément concerné contient un champ ``message`` (``result`` est alors un nom de statut d'erreur tel que ``CONFLICT`` ou
``BAD_REQUEST``). Les éléments traités avec succès retournent leur ``id`` normalement.

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

.. note::

   Si la requête elle-même est invalide (``documents`` absent ou vide, champ obligatoire manquant,
   type de champ incorrect, etc.), le traitement d'enregistrement des documents n'est pas exécuté et
   une réponse d'erreur contenant ``status`` = ``1`` (BAD_REQUEST) et ``message`` est retournée.
   Dans ce cas, le tableau ``items`` n'est pas retourné.

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``items``
     - Tableau des résultats de traitement de chaque document
   * - ``items[].result``
     - Nom du statut du résultat de traitement. ``CREATED`` lors d'une création, ``OK`` lors d'une mise à jour, ou un nom de statut d'erreur tel que ``BAD_REQUEST`` en cas d'échec
   * - ``items[].id``
     - ID du document enregistré (en cas de succès uniquement)
   * - ``items[].message``
     - Message indiquant la raison de l'échec (en cas d'échec uniquement)

Exemples d'utilisation
======================

Enregistrement en masse de documents
-------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "Page d'\''exemple 1",
               "content": "Voici le texte du corps de la page 1."
             }
           ]
         }'

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-searchlist` - API de recherche et de gestion des documents
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
