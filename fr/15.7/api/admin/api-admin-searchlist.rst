==========================
API SearchList
==========================

Vue d'ensemble
==============

L'API SearchList est une API permettant de rechercher et de gerer les documents dans l'index de |Fess|.
Elle permet de rechercher, obtenir, creer, mettre a jour et supprimer des documents.

URL de base
===========

::

    /api/admin/searchlist

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
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
     - Creation d'un document
   * - PUT
     - /doc
     - Mise a jour d'un document
   * - DELETE
     - /doc/{id}
     - Suppression d'un document (par ID)
   * - DELETE
     - /query
     - Suppression de documents (par requete)

Recherche de documents
=======================

Recherche les documents correspondant aux criteres de recherche.

Requete
-------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Non
     - Requete de recherche. Si elle n'est pas specifiee, tous les elements sont concernes.
   * - ``sort``
     - String
     - Non
     - Champ et direction de tri
   * - ``start``
     - Integer
     - Non
     - Position de depart des resultats de recherche
   * - ``offset``
     - Integer
     - Non
     - Decalage de la pagination
   * - ``num``
     - Integer
     - Non
     - Nombre d'elements a obtenir
   * - ``size``
     - Integer
     - Non
     - Nombre d'elements a obtenir (alias de ``num``)
   * - ``lang``
     - String[]
     - Non
     - Langue

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "queryId": "...",
        "execTime": "0.05",
        "pageSize": 20,
        "pageNumber": 1,
        "recordCount": 234,
        "recordCountRelation": "EQUAL_TO",
        "pageCount": 12,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "サンプルページ1",
            "content_description": "..."
          }
        ]
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``queryId``
     - ID de la requete de recherche
   * - ``docs``
     - Tableau des documents resultats de la recherche
   * - ``execTime``
     - Temps d'execution de la recherche
   * - ``pageSize``
     - Nombre d'elements par page
   * - ``pageNumber``
     - Numero de la page courante
   * - ``recordCount``
     - Nombre d'elements correspondants
   * - ``recordCountRelation``
     - Relation du nombre d'elements correspondants (correspondance exacte ou valeur minimale)
   * - ``pageCount``
     - Nombre total de pages

Obtention d'un document
=======================

Obtient un seul document en specifiant son ID de document.

Requete
-------

::

    GET /api/admin/searchlist/doc/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (``doc_id``, parametre de chemin)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "サンプルページ1"
        }
      }
    }

Creation d'un document
======================

Cree un nouveau document dans l'index.

Requete
-------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "サンプルページ1",
        "content": "本文テキストです。"
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
     - Document a enregistrer. Specifie sous forme de carte de noms de champs et de valeurs.

Reponse
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

Mise a jour d'un document
=========================

Met a jour un document existant.

Requete
-------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "更新後のタイトル",
        "content": "更新後の本文テキストです。"
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
     - Document a mettre a jour. Specifie sous forme de carte de noms de champs et de valeurs.

Reponse
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

Suppression d'un document (par ID)
==================================

Supprime un document en specifiant son ID de document.

Requete
-------

::

    DELETE /api/admin/searchlist/doc/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (``doc_id``, parametre de chemin)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression de documents (par requete)
======================================

Supprime en masse les documents correspondant a une requete de recherche.

Requete
-------

::

    DELETE /api/admin/searchlist/query

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Oui
     - Requete de recherche des documents a supprimer

Reponse
-------

Retourne le nombre de documents supprimes dans ``count``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

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

Suppression de documents par requete
------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-documents` - API d'enregistrement groupe de documents
- :doc:`api-admin-crawlinginfo` - API d'informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
