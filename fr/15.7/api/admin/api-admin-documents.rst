==========================
Documents API
==========================

Vue d'ensemble
==============

L'API Documents est une API d'administration de |Fess| permettant d'enregistrer en masse des documents dans l'index.
Elle permet aux systemes externes d'ajouter directement des documents a l'index sans passer par le moteur de crawl.
Plusieurs documents peuvent etre enregistres en une seule requete.

URL de base
===========

::

    /api/admin/documents

Authentification
================

Pour appeler cette API, une authentification par jeton d'acces est requise, comme explique dans :doc:`api-admin-overview`.
Le jeton doit disposer des permissions d'acces a l'API d'administration (par defaut ``Radmin-api``).
Cette permission peut etre modifiee via la cle de configuration ``api.admin.access.permissions``.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - PUT
     - /bulk
     - Enregistrement en masse de documents

.. note::

   Cet endpoint accepte uniquement la methode ``PUT``.

Enregistrement en masse de documents
=====================================

Enregistre plusieurs documents dans l'index en une seule fois.

Requete
-------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

Corps de la requete
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
     - Tableau des documents a enregistrer. Chaque document est specifie sous forme de correspondance entre nom de champ et valeur. Si la valeur est ``null`` ou un tableau vide, une erreur est retournee (``status`` = ``1``).

Champs du document
~~~~~~~~~~~~~~~~~~

Chaque document peut specifier librement les champs de l'index sous forme de correspondance entre nom et valeur.
Au minimum, ``url`` et ``title`` doivent etre specifies (conformement au parametre
``index.admin.required.fields``. La valeur par defaut est ``url,title,role,boost`` ;
``role`` et ``boost`` etant completes automatiquement comme indique ci-apres, seuls ``url`` et ``title`` sont en pratique obligatoires).

Les champs suivants sont completes automatiquement lorsqu'ils sont omis :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur par defaut en cas d'omission
   * - ``content_length``
     - Somme du nombre de caracteres de ``title`` et de ``content``
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - Role de recherche invite (role de recherche configure pour les utilisateurs invites)
   * - ``last_modified``
     - Heure actuelle
   * - ``timestamp``
     - Heure actuelle

De plus, les champs suivants sont generes automatiquement lors de l'enregistrement :

- ``id`` - Genere de facon deterministe a partir de l'``url`` du document (ainsi que de ``role`` et ``virtual_host``),
  et utilise comme identifiant de document OpenSearch (``_id``). Cette valeur est retournee dans ``items[].id`` de la reponse.
- ``doc_id`` - Un UUID aleatoire est genere a chaque enregistrement et stocke comme champ du document.

.. note::

   Comme ``id`` est genere de facon deterministe a partir de l'``url``, l'enregistrement d'un document
   avec le meme ``url`` mettra a jour le document existant
   (``items[].result`` aura la valeur ``OK``).

Remarques
~~~~~~~~~

- Si le champ ``lang`` contient ``"auto"``, la langue est detectee automatiquement a partir du contenu.
- Si ``config_id`` est specifie, le pipeline d'ingestion (ingest pipeline) de la configuration de crawl correspondante est applique.
- Si la generation de miniatures est activee (``thumbnail.crawler.enabled``), une tentative de generation de miniature est effectuee lors de l'enregistrement.
- La valeur de chaque champ est validee en fonction du type de champ configure (``index.admin.array.fields``,
  ``index.admin.date.fields``, ``index.admin.long.fields``, etc.).
  Si le type ne correspond pas, une erreur est retournee (``status`` = ``1``).

Reponse
-------

La reponse retourne le resultat du traitement de chaque document enregistre dans un tableau ``items``.
Les elements traites avec succes contiennent ``result`` et ``id`` ; les elements en echec contiennent ``result`` et ``message``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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

Si ``status`` est ``0``, cela indique que tous les documents ont ete enregistres avec succes.
``items[].result`` est ``CREATED`` lors d'une creation, et ``OK`` lors de la mise a jour d'un document existant.

Si l'enregistrement echoue pour l'un des elements, ``status`` devient ``9`` (FAILED) et
l'element concerne contient un champ ``message`` (``result`` est alors un nom de statut d'erreur tel que ``CONFLICT`` ou
``BAD_REQUEST``). Les elements traites avec succes retournent leur ``id`` normalement.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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

   Si la requete elle-meme est invalide (``documents`` absent ou vide, champ obligatoire manquant,
   type de champ incorrect, etc.), le traitement d'enregistrement des documents n'est pas execute et
   une reponse d'erreur contenant ``status`` = ``1`` (BAD_REQUEST) et ``message`` est retournee.
   Dans ce cas, le tableau ``items`` n'est pas retourne.

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``items``
     - Tableau des resultats de traitement de chaque document
   * - ``items[].result``
     - Nom du statut du resultat de traitement. ``CREATED`` lors d'une creation, ``OK`` lors d'une mise a jour, ou un nom de statut d'erreur tel que ``BAD_REQUEST`` en cas d'echec
   * - ``items[].id``
     - ID du document enregistre (en cas de succes uniquement)
   * - ``items[].message``
     - Message indiquant la raison de l'echec (en cas d'echec uniquement)

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

Informations complementaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-searchlist` - API de recherche et de gestion des documents
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
