==========================
Role API
==========================

Übersicht
=========

Die Role API dient zur Verwaltung von Rollen in |Fess|.
Sie können Rollen erstellen, aktualisieren und löschen.

Basis-URL
=========

::

    /api/admin/role

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET/PUT
     - /settings
     - Rollenliste abrufen
   * - GET
     - /setting/{id}
     - Rolle abrufen
   * - POST
     - /setting
     - Rolle erstellen
   * - PUT
     - /setting
     - Rolle aktualisieren
   * - DELETE
     - /setting/{id}
     - Rolle löschen

Rollenliste abrufen
===================

Request
-------

::

    GET /api/admin/role/settings
    PUT /api/admin/role/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite (Standard: 20)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 0)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "role_id_1",
            "name": "admin"
          },
          {
            "id": "role_id_2",
            "name": "user"
          }
        ],
        "total": 5
      }
    }

Rolle abrufen
=============

Request
-------

::

    GET /api/admin/role/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin"
        }
      }
    }

Rolle erstellen
===============

Request
-------

::

    POST /api/admin/role/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Rollenname

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

Rolle aktualisieren
===================

Request
-------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

Rolle löschen
=============

Request
-------

::

    DELETE /api/admin/role/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

Verwendungsbeispiele
====================

Neue Rolle erstellen
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

Rollenliste abrufen
-------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-user` - Benutzerverwaltung API
- :doc:`api-admin-group` - Gruppenverwaltung API
- :doc:`../../admin/role-guide` - Rollenverwaltungsanleitung
