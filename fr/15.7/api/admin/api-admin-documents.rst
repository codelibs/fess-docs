==========================
API Documents
==========================

Vue d'ensemble
==============

L'API Documents est une API permettant d'enregistrer en masse des documents dans l'index de |Fess|.
Vous pouvez ajouter plusieurs documents a l'index en une seule fois.

URL de base
===========

::

    /api/admin/documents

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

Enregistrement en masse de documents
====================================

Enregistre plusieurs documents dans l'index en une seule fois.

Requete
-------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "サンプルページ1",
          "content": "ページ1の本文テキストです。"
        },
        {
          "url": "https://example.com/page2",
          "title": "サンプルページ2",
          "content": "ページ2の本文テキストです。"
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
     - Tableau des documents a enregistrer. Chaque document est specifie sous forme de correspondance entre nom de champ et valeur. Un tableau vide n'est pas autorise.

Chaque document peut specifier librement des champs d'index tels que ``url`` , ``title`` , ``content`` .
Lorsque ``content_length`` , ``favorite_count`` , ``click_count`` , ``boost`` , ``role`` , ``last_modified`` , ``timestamp`` , etc. sont omis, des valeurs par defaut sont automatiquement renseignees.
De plus, ``doc_id`` et ID sont generes automatiquement lors de l'enregistrement.

Reponse
-------

La reponse renvoie le resultat du traitement de chaque document enregistre dans un tableau ``items`` .
Les elements reussis contiennent ``result`` et ``id`` , les elements en echec contiennent ``result`` et ``message`` .

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

Si l'enregistrement echoue pour l'un des elements, ``status`` devient ``9`` (FAILED) et l'element concerne contient un champ ``message`` .

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
     - Statut du resultat du traitement (ex. : ``CREATED``)
   * - ``items[].id``
     - ID du document enregistre (en cas de succes)
   * - ``items[].message``
     - Message indiquant la raison de l'echec (en cas d'echec)

Exemples d'utilisation
======================

Enregistrement en masse de documents
------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "サンプルページ1",
               "content": "ページ1の本文テキストです。"
             }
           ]
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-searchlist` - API de recherche et de gestion des documents
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
