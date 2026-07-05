==========================
LabelType API
==========================

Übersicht
=========

Die LabelType API dient zur Verwaltung von Label-Typen in |Fess|.
Label-Typen ermöglichen die Kategorisierung von Suchergebnissen anhand von gecrawlten Pfaden und
virtuellen Hosts und können für die Eingrenzung (Filterung) über Labels in der Suchoberfläche
verwendet werden.

Informationen zur Authentifizierung sowie zu den gemeinsamen Spezifikationen von Antworten
(``status``-Code, ``version``-Feld, Fehlerformat, HTTP-Statuscodes usw.) finden Sie unter
:doc:`api-admin-overview`.
Für den Zugriff auf diese API ist ein Access Token mit Admin-API-Berechtigung (``admin-api``)
im Header ``Authorization: Bearer <Access Token>`` erforderlich.

Basis-URL
=========

::

    /api/admin/labeltype

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
     - Label-Typ-Liste abrufen
   * - GET
     - /setting/{id}
     - Label-Typ abrufen
   * - POST
     - /setting
     - Label-Typ erstellen
   * - PUT
     - /setting
     - Label-Typ aktualisieren
   * - DELETE
     - /setting/{id}
     - Label-Typ löschen

Label-Typ-Liste abrufen
=======================

Anfrage
-------

::

    GET /api/admin/labeltype/settings

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
     - Anzahl der Einträge pro Seite. Standard ist der konfigurierte Wert von ``paging.page.size`` (normalerweise ``25``).
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1). Standard ist ``1``.
   * - ``name``
     - String
     - Nein
     - Eingrenzung nach Anzeigename (Wildcard-Suche).
   * - ``value``
     - String
     - Nein
     - Eingrenzung nach Label-Wert (Wildcard-Suche).

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Jedes Einstellungsobjekt enthält auch die Audit-Felder ``createdBy`` / ``createdTime`` / ``updatedBy`` /
   ``updatedTime`` sowie ``versionNo`` für optimistisches Sperren (Felder mit dem Wert ``null``
   werden weggelassen). Das ``response``-Objekt enthält stets ``version``, das die Produktversion
   angibt; in den folgenden Beispielen wird es der Übersichtlichkeit halber teilweise weggelassen.

Label-Typ abrufen
=================

Anfrage
-------

::

    GET /api/admin/labeltype/setting/{id}

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "permissions": "{role}admin",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

Label-Typ erstellen
===================

Anfrage
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Anfragetext
~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest"
    }

Feldbeschreibung
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Feld
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``name``
     - String
     - Ja
     - Anzeigename des Labels (maximal 100 Zeichen).
   * - ``value``
     - String
     - Ja
     - Label-Wert (wird bei der Suche als ``label``-Parameter verwendet). Nur alphanumerische Zeichen und Unterstriche (``_``) sind zulässig; der Wert muss dem regulären Ausdruck ``^[a-zA-Z0-9_]+$`` entsprechen (maximal 100 Zeichen).
   * - ``includedPaths``
     - String
     - Nein
     - Regulärer Ausdruck für Label-Zielpfade. Bei mehreren Angaben durch Zeilenumbruch (``\n``) trennen.
   * - ``excludedPaths``
     - String
     - Nein
     - Regulärer Ausdruck für ausgeschlossene Pfade. Bei mehreren Angaben durch Zeilenumbruch (``\n``) trennen.
   * - ``permissions``
     - String
     - Nein
     - Zugriffsberechtigte Rollen/Gruppen/Benutzer (Beispiel: ``{role}admin``). Bei mehreren Angaben durch Zeilenumbruch (``\n``) trennen.
   * - ``sortOrder``
     - Integer
     - Nein
     - Anzeigereihenfolge (ganze Zahl >= 0). Standardwert ist ``0``.
   * - ``virtualHost``
     - String
     - Nein
     - Virtueller Host (maximal 1000 Zeichen).

.. note::

   Audit-Felder wie ``createdBy`` / ``createdTime`` werden serverseitig automatisch gesetzt
   und müssen nicht in der Anfrage angegeben werden.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

Bei erfolgreicher Erstellung ist ``created`` gleich ``true``.

Label-Typ aktualisieren
=======================

Anfrage
-------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Anfragetext
~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest",
      "versionNo": 1
    }

Bei der Aktualisierung sind zusätzlich zu den Feldern beim Erstellen folgende Felder erforderlich.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Feld
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``id``
     - String
     - Ja
     - ID des zu aktualisierenden Label-Typs.
   * - ``versionNo``
     - Integer
     - Ja
     - Versionsnummer für optimistisches Sperren. Geben Sie den ``versionNo``-Wert aus der Abrufantwort an. Stimmt die angegebene Version nicht mit der aktuellen überein, schlägt die Aktualisierung fehl.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

Bei einer Aktualisierung ist ``created`` gleich ``false``.

Label-Typ löschen
=================

Anfrage
-------

::

    DELETE /api/admin/labeltype/setting/{id}

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Anwendungsbeispiele
===================

Dokumentations-Label erstellen
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Label-Typ-Liste abrufen
-----------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suche mit Label-Typ
-------------------

.. code-block:: bash

    # Mit Label filtern
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Siehe auch
==========

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../api-search` - Such-API
- :doc:`../../admin/labeltype-guide` - Label-Typ Verwaltungsanleitung
