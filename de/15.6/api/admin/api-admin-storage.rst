==========================
Storage API
==========================

Übersicht
=========

Die Storage API dient zur Verwaltung des Dateispeichers in |Fess|.
Sie können Dateien hochladen, herunterladen und löschen.

Basis-URL
=========

::

    /api/admin/storage

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
     - Speicherinhalt auflisten
   * - GET
     - /{path}
     - Datei herunterladen
   * - POST
     - /
     - Datei hochladen
   * - DELETE
     - /{path}
     - Datei löschen

Speicherinhalt auflisten
========================

Request
-------

::

    GET /api/admin/storage

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``path``
     - String
     - Nein
     - Verzeichnispfad

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "items": [
          {
            "name": "documents",
            "type": "directory",
            "size": 0
          },
          {
            "name": "backup.zip",
            "type": "file",
            "size": 1048576,
            "lastModified": "2025-01-29T10:00:00Z"
          }
        ]
      }
    }

Datei hochladen
===============

Request
-------

::

    POST /api/admin/storage
    Content-Type: multipart/form-data

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "File uploaded successfully",
        "path": "/documents/uploaded-file.txt"
      }
    }

Verwendungsbeispiele
====================

Speicherinhalt auflisten
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage?path=/documents" \
         -H "Authorization: Bearer YOUR_TOKEN"

Datei hochladen
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@myfile.txt" \
         -F "path=/documents"

Datei löschen
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/documents/myfile.txt" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/storage-guide` - Speicher Verwaltungsanleitung
