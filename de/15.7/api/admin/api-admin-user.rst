==========================
User API
==========================

Übersicht
=========

Die User API ist eine REST API zur Verwaltung von |Fess|-Benutzerkonten.
Sie können Benutzer erstellen, abrufen, aktualisieren und löschen sowie Rollen und Gruppen zuweisen.

Dies ist eine Admin-API; der Zugriff erfordert eine Authentifizierung mit einem Admin-Zugriffstoken.
Informationen zur Authentifizierungsmethode und zu den gemeinsamen Spezifikationen finden Sie unter :doc:`api-admin-overview`.

Jede Antwort ist in ein ``response``-Objekt eingebettet und enthält die folgenden gemeinsamen Felder:

- ``version`` : Der |Fess|-Produktversionsstring.
- ``status`` : Der Ergebnisstatuscode (``0`` =Erfolg, ``1`` =Ungültige Anfrage, ``2`` =Systemfehler, ``3`` =Nicht autorisiert, ``9`` =Fehlgeschlagen).

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

Anfrage
-------

::

    GET /api/admin/user/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite. Der Standardwert ist der konfigurierte Wert ``paging.page.size`` (Standard: 25).
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1). Der Standardwert ist 1.

.. note::

   In der aktuellen Implementierung berücksichtigt der Endpunkt für die Benutzerliste die Parameter ``size`` und ``page`` nicht.
   Es wird immer die erste Seite zurückgegeben, mit der durch die Servereinstellung ``paging.page.size`` (Standard: 25) festgelegten Anzahl von Einträgen, sortiert nach Benutzername (``name``) in aufsteigender Reihenfolge.
   Die Gesamtanzahl der übereinstimmenden Benutzer ist in ``response.total`` verfügbar.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : Das Array der Benutzer auf der aktuellen Seite.
- ``total`` : Die Gesamtanzahl der übereinstimmenden Benutzer.

Benutzer abrufen
================

Anfrage
-------

::

    GET /api/admin/user/setting/{id}

Geben Sie in ``{id}`` die Dokument-ID des Zielbenutzers an.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
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
          "groups": [],
          "versionNo": 1
        }
      }
    }

.. note::

   ``attributes`` enthält alle für den Benutzer gespeicherten Attribute, mit Ausnahme von ``name``, ``password``, ``roles`` und ``groups``.
   ``password`` ist nicht in der Antwort enthalten.

Benutzer erstellen
==================

Anfrage
-------

::

    POST /api/admin/user/setting
    Content-Type: application/json

Anfrage-Body
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
   :widths: 20 10 70

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
     - Bestätigungspasswort
   * - ``attributes``
     - Nein
     - Attribut-Map (siehe unten)
   * - ``roles``
     - Nein
     - Array von Rollen-IDs
   * - ``groups``
     - Nein
     - Array von Gruppen-IDs

.. note::

   Die REST API führt keine Pflichtprüfung für das Passwort, keinen Abgleich zwischen ``password`` und ``confirmPassword`` und keine Passwortrichtlinienvalidierung durch (diese werden nur in der Admin-Oberfläche angewendet).
   In der Praxis wird empfohlen, ein gültiges ``password`` anzugeben, dessen Wert mit ``confirmPassword`` übereinstimmt.

Die Schlüssel von ``attributes`` sind die Attributnamen der Benutzerentität (die aus LDAP abgeleiteten Schemaelementnamen).
Die häufigsten Schlüssel sind:

- ``surname``, ``givenName``, ``displayName``, ``mail``
- ``telephoneNumber``, ``mobile``, ``homePhone``
- ``employeeNumber``, ``title``, ``description``, ``homeDirectory``
- ``uidNumber``, ``gidNumber``

``uidNumber`` und ``gidNumber`` müssen numerische Werte sein (der Typ wird bei der Aktualisierung validiert).
Viele weitere LDAP-Attributschlüssel können ebenfalls angegeben werden.

.. note::

   Bei der Erstellung wird die Benutzer-ID (Dokument-ID) automatisch als Base64-URL-kodierter Wert des Benutzernamens generiert
   (zum Beispiel wird der Benutzername ``admin`` zu ``YWRtaW4=``).

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` : Die Dokument-ID des erstellten Benutzers.
- ``created`` : ``true`` bei erfolgreicher Erstellung.

Benutzer aktualisieren
======================

Anfrage
-------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

Anfrage-Body
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

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``id``
     - Ja
     - Die Dokument-ID des zu aktualisierenden Benutzers.
   * - ``name``
     - Ja
     - Benutzername (Login-ID)
   * - ``versionNo``
     - Ja
     - Versionsnummer (für optimistisches Sperren)
   * - ``password``
     - Nein
     - Neues Passwort (wird nur aktualisiert, wenn angegeben)
   * - ``confirmPassword``
     - Nein
     - Bestätigungspasswort
   * - ``attributes``
     - Nein
     - Attribut-Map (siehe „Benutzer erstellen")
   * - ``roles``
     - Nein
     - Array von Rollen-IDs
   * - ``groups``
     - Nein
     - Array von Gruppen-IDs

.. note::

   Bei der Aktualisierung sind ``id``, ``name`` und ``versionNo`` erforderlich.
   ``versionNo`` ist der Wert, der beim Abrufen des Zielbenutzers (GET) zurückgegeben wird, und entspricht der OpenSearch-Dokumentversion.
   Stimmt er nicht mit der aktuellen Version überein, wird die Anfrage als Konflikt behandelt und die Aktualisierung abgelehnt.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : ``false`` bei einer Aktualisierung.

Benutzer löschen
================

Anfrage
-------

::

    DELETE /api/admin/user/setting/{id}

Geben Sie in ``{id}`` die Dokument-ID des zu löschenden Benutzers an.

.. note::

   Der aktuell angemeldete Benutzer kann nicht gelöscht werden.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` : Die Dokument-ID des gelöschten Benutzers.

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
