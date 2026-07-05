==========================
AccessToken API
==========================

Übersicht
=========

Die AccessToken API dient zur Verwaltung von API-Zugriffstoken in |Fess|.
Sie können Token erstellen, aktualisieren und löschen.

Basis-URL
=========

::

    /api/admin/accesstoken

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
     - Access Token Liste abrufen
   * - GET
     - /setting/{id}
     - Access Token abrufen
   * - POST
     - /setting
     - Access Token erstellen
   * - PUT
     - /setting
     - Access Token aktualisieren
   * - DELETE
     - /setting/{id}
     - Access Token löschen

Access Token Liste abrufen
==========================

Request
-------

::

    GET /api/admin/accesstoken/settings
    PUT /api/admin/accesstoken/settings

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expiredTime": 1735689600000,
            "permissions": ["admin"]
          }
        ],
        "total": 5
      }
    }

Access Token abrufen
====================

Request
-------

::

    GET /api/admin/accesstoken/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "token",
          "expiredTime": 1735689600000,
          "permissions": ["admin"]
        }
      }
    }

Access Token erstellen
======================

Request
-------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "parameterName": "token",
      "permissions": ["user"]
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
     - Token-Name
   * - ``token``
     - Nein
     - Token-String (automatisch generiert, wenn nicht angegeben)
   * - ``parameterName``
     - Nein
     - Parametername (Standard: "token")
   * - ``expiredTime``
     - Nein
     - Ablaufzeit (Unix-Zeit in Millisekunden)
   * - ``permissions``
     - Nein
     - Erlaubte Rollen

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "token": "generated_token_string",
        "created": true
      }
    }

Access Token aktualisieren
==========================

Request
-------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "parameterName": "token",
      "expiredTime": 1767225600000,
      "permissions": ["user", "editor"],
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

Access Token löschen
====================

Request
-------

::

    DELETE /api/admin/accesstoken/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_token_id",
        "created": false
      }
    }

Verwendungsbeispiele
====================

API-Token erstellen
-------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "External App Token",
           "parameterName": "token",
           "permissions": ["guest"]
         }'

API-Aufruf mit Token
--------------------

.. code-block:: bash

    # Token als Parameter verwenden
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # Token im Authorization-Header verwenden
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../api-search` - Such-API
- :doc:`../../admin/accesstoken-guide` - Access Token Verwaltungsanleitung
