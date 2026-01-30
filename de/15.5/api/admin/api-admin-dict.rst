==========================
Dict API
==========================

Übersicht
=========

Die Dict API dient zur Verwaltung von Wörterbüchern in |Fess|.
Sie können Synonyme, Stoppwörter, Mappings und andere Wörterbuchdaten verwalten.

Basis-URL
=========

::

    /api/admin/dict

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /
     - Wörterbücher auflisten
   * - GET
     - /{dictId}/settings
     - Wörterbucheinträge auflisten
   * - GET
     - /{dictId}/setting/{id}
     - Wörterbucheintrag abrufen
   * - POST
     - /{dictId}/setting
     - Wörterbucheintrag erstellen
   * - PUT
     - /{dictId}/setting
     - Wörterbucheintrag aktualisieren
   * - DELETE
     - /{dictId}/setting/{id}
     - Wörterbucheintrag löschen

Wörterbücher auflisten
======================

Request
-------

::

    GET /api/admin/dict

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dictionaries": [
          {
            "id": "synonym",
            "name": "Synonym Dictionary",
            "type": "synonym"
          },
          {
            "id": "stopwords",
            "name": "Stop Words",
            "type": "stopwords"
          },
          {
            "id": "mapping",
            "name": "Character Mapping",
            "type": "mapping"
          }
        ]
      }
    }

Wörterbucheinträge auflisten
============================

Request
-------

::

    GET /api/admin/dict/{dictId}/settings

Response (Synonym-Beispiel)
---------------------------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "entry_1",
            "inputs": "auto, car, vehicle",
            "outputs": "automobile"
          }
        ],
        "total": 100
      }
    }

Wörterbucheintrag erstellen
===========================

Request (Synonym)
-----------------

::

    POST /api/admin/dict/synonym/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "laptop, notebook",
      "outputs": "computer"
    }

Request (Stoppwort)
-------------------

::

    POST /api/admin/dict/stopwords/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "input": "the"
    }

Verwendungsbeispiele
====================

Wörterbücher auflisten
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Synonyme auflisten
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Synonym hinzufügen
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "big, large, huge",
           "outputs": "big"
         }'

Stoppwort hinzufügen
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/stopwords/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "input": "and"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/dict-guide` - Wörterbuch Verwaltungsanleitung
- :doc:`../../admin/synonym-guide` - Synonym Verwaltungsanleitung
