==========================
Plugin API
==========================

Übersicht
=========

Die Plugin API dient zur Verwaltung von Plugins (Artefakten) in |Fess|.
Sie können installierte und installierbare Plugins auflisten sowie Plugins installieren und löschen.

Basis-URL
=========

::

    /api/admin/plugin

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /installed
     - Installierte Plugins auflisten
   * - GET
     - /available
     - Installierbare Plugins auflisten
   * - POST
     - /
     - Plugin installieren
   * - DELETE
     - /
     - Plugin löschen

Installierte Plugins auflisten
==============================

Gibt die Liste der installierten Plugins zurück.

Request
-------

::

    GET /api/admin/plugin/installed

Response
--------

In ``plugins`` wird ein Array von Objekten gespeichert, die die Plugin-Informationen darstellen.
Jedes Objekt ist eine Map aus Zeichenketten-Schlüsseln und -Werten und enthält ``name`` (Plugin-Name), ``version`` (Version) usw.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Installierbare Plugins auflisten
================================

Gibt die Liste der installierbaren Plugins zurück.

Request
-------

::

    GET /api/admin/plugin/available

Response
--------

In ``plugins`` wird ein Array von Objekten gespeichert, die die Informationen der installierbaren Plugins darstellen.
Wie bei ``installed`` ist jedes Objekt eine Map aus Zeichenketten-Schlüsseln und -Werten.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Plugin installieren
===================

Installiert das Plugin mit dem angegebenen Namen und der angegebenen Version.

Request
-------

::

    POST /api/admin/plugin
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Plugin-Name (maximal 100 Zeichen)
   * - ``version``
     - Ja
     - Plugin-Version (maximal 100 Zeichen)

Response
--------

Bei Erfolg wird nur ``status`` zurückgegeben.
Existiert kein Artefakt, das auf ``name`` oder ``version`` passt, wird ``status`` zu ``1`` (BAD_REQUEST) und in ``message`` wird ``invalid name or version`` gesetzt.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Plugin löschen
==============

Löscht das Plugin mit dem angegebenen Namen und der angegebenen Version.

Request
-------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Plugin-Name (maximal 100 Zeichen)
   * - ``version``
     - Nein
     - Plugin-Version (maximal 100 Zeichen)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Verwendungsbeispiele
====================

Installierte Plugins auflisten
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

Plugin installieren
-------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Plugin löschen
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
