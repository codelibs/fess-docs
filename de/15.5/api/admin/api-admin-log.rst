==========================
Log API
==========================

Übersicht
=========

Die Log API dient zum Abrufen von Systemprotokollen in |Fess|.
Sie können Anwendungsprotokolle und Crawl-Protokolle einsehen.

Basis-URL
=========

::

    /api/admin/log

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
     - Protokolldateien auflisten
   * - GET
     - /{filename}
     - Protokolldatei-Inhalt abrufen

Protokolldateien auflisten
==========================

Request
-------

::

    GET /api/admin/log

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "files": [
          {
            "name": "fess.log",
            "size": 1048576,
            "lastModified": "2025-01-29T10:00:00Z"
          },
          {
            "name": "fess-crawler.log",
            "size": 524288,
            "lastModified": "2025-01-29T09:30:00Z"
          }
        ]
      }
    }

Protokolldatei-Inhalt abrufen
=============================

Request
-------

::

    GET /api/admin/log/{filename}

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``lines``
     - Integer
     - Nein
     - Anzahl der letzten Zeilen (Standard: 100)

Response
--------

Text-Inhalt der Protokolldatei.

Verwendungsbeispiele
====================

Protokolldateien auflisten
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log" \
         -H "Authorization: Bearer YOUR_TOKEN"

Protokolldatei lesen
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/fess.log?lines=500" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/log-guide` - Protokoll Verwaltungsanleitung
