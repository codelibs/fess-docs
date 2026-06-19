==========================
AccessToken API
==========================

Übersicht
=========

Die AccessToken API dient zur Verwaltung von API-Zugriffstoken in |Fess|.
Sie können Token erstellen, abrufen, aktualisieren und löschen.

Zugriffstoken werden zur Authentifizierung beim programmatischen Aufruf der Such-API oder der Admin API von |Fess| verwendet.
Die gemeinsamen Spezifikationen der Admin API (Authentifizierungsmethode, Response-Format, ``status``-Werte, Fehler-Response,
HTTP-Statuscodes) einschließlich dieser API finden Sie unter :doc:`api-admin-overview`.

.. note::

   Für den Zugriff auf diese API benötigt der verwendete Zugriffstoken eine Berechtigung,
   die ``api.admin.access.permissions`` (Standardwert ``{role}admin-api`` ) entspricht.

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
   * - GET
     - /settings
     - Zugriffstoken-Liste abrufen
   * - GET
     - /setting/{id}
     - Zugriffstoken abrufen
   * - POST
     - /setting
     - Zugriffstoken erstellen
   * - PUT
     - /setting
     - Zugriffstoken aktualisieren
   * - DELETE
     - /setting/{id}
     - Zugriffstoken löschen

Zugriffstoken-Liste abrufen
============================

Request
-------

::

    GET /api/admin/accesstoken/settings

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
     - Anzahl der Einträge pro Seite (Standard: 25; änderbar über ``paging.page.size``)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1; Standard: 1)
   * - ``id``
     - String
     - Nein
     - Filter, um nur den Token mit der angegebenen ID abzurufen

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Jedes Token-Objekt enthält außerdem Audit- und Versionsinformationen wie ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` und ``versionNo``.
   ``createdTime`` und ``updatedTime`` werden als Millisekunden seit der Epoche (numerisch) angegeben.
   Felder mit dem Wert ``null`` werden aus der Response ausgeschlossen.
   ``permissions`` wird als durch Zeilenumbrüche ( ``\n`` ) getrennte Zeichenkette zurückgegeben.

Zugriffstoken abrufen
======================

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
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
        }
      }
    }

Zugriffstoken erstellen
========================

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
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
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
     - Token-Name (maximal 1000 Zeichen)
   * - ``permissions``
     - Nein
     - Dem Token zugewiesene Berechtigungen. Mehrere Berechtigungen können durch Zeilenumbrüche ( ``\n`` ) getrennt angegeben werden (Beispiel: ``{role}admin-api`` ). Token, die die Admin API aufrufen sollen, benötigen eine Berechtigung, die ``api.admin.access.permissions`` (Standardwert ``{role}admin-api`` ) entspricht.
   * - ``parameterName``
     - Nein
     - Name des Request-Parameters zur Übergabe zusätzlicher Berechtigungen. Enthält eine mit diesem Token authentifizierte Anfrage einen Parameter mit dem hier angegebenen Namen, wird dessen Wert zu ``permissions`` hinzugefügt. Wird dieses Feld weggelassen, wird kein Parameter konfiguriert.
   * - ``expires``
     - Nein
     - Ablaufzeitpunkt. Als Zeichenkette im Format ``YYYY-MM-DDTHH:MM:SS`` angeben (Beispiel: ``2026-01-01T00:00:00`` ). Wird das Feld weggelassen, läuft der Token nie ab.

.. note::

   Der Token-String ( ``token`` ) wird serverseitig automatisch generiert. Ein im Request-Body
   angegebenes ``token``-Feld wird ignoriert. Da die Erstellungs-Response keinen Token-String enthält,
   rufen Sie den generierten Token-String über "Zugriffstoken abrufen" ( ``GET /setting/{id}`` ) ab.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "created": true
      }
    }

Zugriffstoken aktualisieren
============================

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
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

Bei der Aktualisierung werden zusätzlich zu den Feldern der Erstellung folgende Felder verwendet.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``id``
     - Ja
     - ID des zu aktualisierenden Tokens
   * - ``versionNo``
     - Ja
     - Versionsnummer für optimistisches Sperren. Geben Sie die ``versionNo`` des zuvor abgerufenen Tokens an.

.. note::

   Der Token-String ( ``token`` ) kann nicht aktualisiert werden. Ein im Request-Body angegebenes
   ``token``-Feld wird ignoriert und der vorhandene Wert bleibt erhalten.

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

Zugriffstoken löschen
======================

Request
-------

::

    DELETE /api/admin/accesstoken/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
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
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

API-Aufruf mit Token
--------------------

Der erstellte Token wird zur Authentifizierung beim Aufruf der Such-API und anderer APIs verwendet.

.. code-block:: bash

    # Token als Authorization-Header verwenden
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # Token als Query-Parameter verwenden (Konfiguration von api.access.token.request.parameter erforderlich)
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht (Authentifizierung, Response-Format, Fehler)
- :doc:`../api-search` - Such-API
- :doc:`../../admin/accesstoken-guide` - Zugriffstoken-Verwaltungsanleitung
