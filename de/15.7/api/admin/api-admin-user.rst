==========================
User API
==========================

Übersicht
=========

Die User API dient zur Verwaltung von Benutzerkonten in |Fess|.
Sie können Benutzer erstellen, aktualisieren, löschen und Berechtigungen konfigurieren.

Basis-URL
=========

::

    /api/admin/user

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /settings
     - Benutzerliste abrufen
   * - GET
     - /setting/{id}
     - Benutzer abrufen
   * - POST
     - /setting
     - Benutzer erstellen
   * - PUT
     - /setting
     - Benutzer aktualisieren
   * - DELETE
     - /setting/{id}
     - Benutzer löschen

Benutzerliste abrufen
=====================

Request
-------

::

    GET /api/admin/user/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "id": "user_id_1",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": []
          }
        ],
        "total": 10
      }
    }

Benutzer abrufen
================

Request
-------

::

    GET /api/admin/user/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "user_id_1",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["admin"],
          "groups": []
        }
      }
    }

Benutzer erstellen
==================

Request
-------

::

    POST /api/admin/user/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Benutzername (Login-ID)
   * - ``password``
     - Nein
     - Passwort
   * - ``confirmPassword``
     - Nein
     - Bestätigungspasswort (muss mit ``password`` übereinstimmen)
   * - ``attributes``
     - Nein
     - Attribut-Map (enthält LDAP-Attribute wie ``surname``, ``givenName``, ``mail``, ``telephoneNumber`` usw.)
   * - ``roles``
     - Nein
     - Array von Rollen-IDs
   * - ``groups``
     - Nein
     - Array von Gruppen-IDs

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

Benutzer aktualisieren
======================

Request
-------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

Benutzer löschen
================

Request
-------

::

    DELETE /api/admin/user/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

Verwendungsbeispiele
====================

Neuen Benutzer erstellen
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["user"],
           "groups": []
         }'

Benutzerrollen ändern
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-role` - Rollenverwaltung API
- :doc:`api-admin-group` - Gruppenverwaltung API
- :doc:`../../admin/user-guide` - Benutzerverwaltungsanleitung
