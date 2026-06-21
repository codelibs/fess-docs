==========================
RelatedContent API
==========================

Übersicht
=========

Die RelatedContent API dient zur Verwaltung von verwandten Inhalten in |Fess|.
Sie können benutzerdefinierte Inhalte definieren, die bei bestimmten Suchbegriffen angezeigt werden.

Basis-URL
=========

::

    /api/admin/relatedcontent

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
     - Verwandte Inhalte auflisten
   * - GET
     - /setting/{id}
     - Verwandten Inhalt abrufen
   * - POST
     - /setting
     - Verwandten Inhalt erstellen
   * - PUT
     - /setting
     - Verwandten Inhalt aktualisieren
   * - DELETE
     - /setting/{id}
     - Verwandten Inhalt löschen

Verwandte Inhalte auflisten
============================

Request
-------

::

    GET /api/admin/relatedcontent/settings

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
     - Anzahl der Einträge pro Seite (Standard: 25; änderbar über ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1; Werte von 0 oder kleiner werden als 1 behandelt)
   * - ``term``
     - String
     - Nein
     - Filterung nach Suchbegriff (Platzhaltersuche)
   * - ``content``
     - String
     - Nein
     - Filterung nach Inhaltstext (Platzhaltersuche)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
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

   Jedes Element von ``settings`` sowie das ``setting``-Objekt des Einzelabruf-Endpunkts enthält
   die Felder der gespeicherten Entität unverändert. Neben ``term``, ``content``, ``sortOrder``
   und ``virtualHost`` werden auch die Audit-Felder ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` sowie das Feld ``versionNo`` zur optimistischen Sperrung zurückgegeben.
   ``createdTime`` und ``updatedTime`` werden als Millisekunden seit dem Epoch-Zeitpunkt (Zahlen)
   angegeben. Felder, die nicht gesetzt sind (null), werden in der Antwort weggelassen. Außerdem
   enthält das ``response``-Objekt jeder Antwort stets ``version``, das die Produktversion angibt
   (Details siehe :doc:`api-admin-overview`).

Verwandten Inhalt abrufen
==========================

Request
-------

::

    GET /api/admin/relatedcontent/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
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

.. note::

   Der ``versionNo``-Wert, der beim Aktualisieren (PUT) benötigt wird, ist der in dieser
   Abrufantwort enthaltene Wert.

Verwandten Inhalt erstellen
============================

Request
-------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``term``
     - Ja
     - Suchbegriff (max. 10000 Zeichen)
   * - ``content``
     - Ja
     - Anzuzeigender HTML-Inhalt (max. 10000 Zeichen)
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge (ganze Zahl zwischen 0 und 2147483647)
   * - ``virtualHost``
     - Nein
     - Virtueller Host (max. 1000 Zeichen)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Verwandten Inhalt aktualisieren
================================

Request
-------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``id``
     - Ja
     - ID des zu aktualisierenden verwandten Inhalts (max. 1000 Zeichen)
   * - ``term``
     - Ja
     - Suchbegriff (max. 10000 Zeichen)
   * - ``content``
     - Ja
     - Anzuzeigender HTML-Inhalt (max. 10000 Zeichen)
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge (ganze Zahl zwischen 0 und 2147483647)
   * - ``virtualHost``
     - Nein
     - Virtueller Host (max. 1000 Zeichen)
   * - ``versionNo``
     - Ja
     - Versionsnummer zur optimistischen Sperrung. Geben Sie den in der Antwort von ``setting/{id}`` enthaltenen Wert an.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   Audit-Felder wie ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` sowie
   ``crudMode`` werden ignoriert, auch wenn sie im Request-Body enthalten sind, da sie
   serverseitig automatisch gesetzt werden. Sie müssen diese beim Erstellen oder Aktualisieren
   nicht angeben.

Verwandten Inhalt löschen
==========================

Request
-------

::

    DELETE /api/admin/relatedcontent/setting/{id}

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

Verwandter Inhalt für Produktinformationen
-------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

Verwandter Inhalt für Support-Informationen
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-relatedquery` - Verwandte Abfragen API
- :doc:`../../admin/relatedcontent-guide` - Verwandte Inhalte Verwaltungsanleitung
