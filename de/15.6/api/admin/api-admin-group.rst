==========================
Group API
==========================

Übersicht
=========

Die Group API dient zur Verwaltung von Gruppen in |Fess|.
Sie können Gruppen erstellen, aktualisieren und löschen.

Basis-URL
=========

::

    /api/admin/group

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
     - Gruppenliste abrufen
   * - GET
     - /setting/{id}
     - Gruppe abrufen
   * - POST
     - /setting
     - Gruppe erstellen
   * - PUT
     - /setting
     - Gruppe aktualisieren
   * - DELETE
     - /setting/{id}
     - Gruppe löschen

Gruppenliste abrufen
====================

Request
-------

::

    GET /api/admin/group/settings
    PUT /api/admin/group/settings

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
            "id": "group_id_1",
            "name": "Engineering",
            "gidNumber": 1000
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "gidNumber": 1001
          }
        ],
        "total": 5
      }
    }

Gruppe abrufen
==============

Request
-------

::

    GET /api/admin/group/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "gidNumber": 1000
        }
      }
    }

Gruppe erstellen
================

Request
-------

::

    POST /api/admin/group/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "gidNumber": 1002
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
     - Gruppenname
   * - ``gidNumber``
     - Nein
     - Gruppen-ID-Nummer

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

Gruppe aktualisieren
====================

Request
-------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "gidNumber": 1002,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

Gruppe löschen
==============

Request
-------

::

    DELETE /api/admin/group/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

Verwendungsbeispiele
====================

Neue Gruppe erstellen
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "gidNumber": 2000
         }'

Gruppenliste abrufen
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-user` - Benutzerverwaltung API
- :doc:`api-admin-role` - Rollenverwaltung API
- :doc:`../../admin/group-guide` - Gruppenverwaltungsanleitung
