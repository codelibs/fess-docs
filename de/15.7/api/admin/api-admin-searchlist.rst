==========================
SearchList API
==========================

Übersicht
=========

Die SearchList API ist eine API zum Suchen und Verwalten von Dokumenten im Index von |Fess|.
Sie können Dokumente suchen, abrufen, erstellen, aktualisieren und löschen.

Basis-URL
=========

::

    /api/admin/searchlist

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET / PUT
     - /docs
     - Dokumente suchen
   * - GET
     - /doc/{id}
     - Dokument abrufen
   * - POST
     - /doc
     - Dokument erstellen
   * - PUT
     - /doc
     - Dokument aktualisieren
   * - DELETE
     - /doc/{id}
     - Dokument löschen (per ID)
   * - DELETE
     - /query
     - Dokument löschen (per Query)

Dokumente suchen
================

Sucht nach Dokumenten, die den Suchbedingungen entsprechen.

Request
-------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``q``
     - String
     - Nein
     - Suchanfrage. Wenn nicht angegeben, werden alle Einträge berücksichtigt.
   * - ``sort``
     - String
     - Nein
     - Sortierfeld und -richtung
   * - ``start``
     - Integer
     - Nein
     - Startposition der Suchergebnisse
   * - ``offset``
     - Integer
     - Nein
     - Offset für die Paginierung
   * - ``num``
     - Integer
     - Nein
     - Anzahl der abzurufenden Einträge
   * - ``size``
     - Integer
     - Nein
     - Anzahl der abzurufenden Einträge (Alias für ``num``)
   * - ``lang``
     - String[]
     - Nein
     - Sprache

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "queryId": "...",
        "execTime": "0.05",
        "pageSize": 20,
        "pageNumber": 1,
        "recordCount": 234,
        "recordCountRelation": "EQUAL_TO",
        "pageCount": 12,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "サンプルページ1",
            "content_description": "..."
          }
        ]
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``queryId``
     - Such-Query-ID
   * - ``docs``
     - Array der Suchergebnis-Dokumente
   * - ``execTime``
     - Ausführungszeit der Suche
   * - ``pageSize``
     - Anzahl der Einträge pro Seite
   * - ``pageNumber``
     - Aktuelle Seitennummer
   * - ``recordCount``
     - Anzahl der Treffer
   * - ``recordCountRelation``
     - Beziehung der Trefferanzahl (exakte Übereinstimmung oder Untergrenze)
   * - ``pageCount``
     - Gesamtzahl der Seiten

Dokument abrufen
================

Ruft ein einzelnes Dokument anhand der Dokument-ID ab.

Request
-------

::

    GET /api/admin/searchlist/doc/{id}

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``id``
     - String
     - Ja
     - Dokument-ID (``doc_id``, Pfadparameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "サンプルページ1"
        }
      }
    }

Dokument erstellen
==================

Erstellt ein neues Dokument im Index.

Request
-------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "サンプルページ1",
        "content": "本文テキストです。"
      }
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``doc``
     - Ja
     - Zu registrierendes Dokument. Wird als Map aus Feldnamen und Werten angegeben.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

Dokument aktualisieren
======================

Aktualisiert ein vorhandenes Dokument.

Request
-------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "更新後のタイトル",
        "content": "更新後の本文テキストです。"
      }
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``doc``
     - Ja
     - Zu aktualisierendes Dokument. Wird als Map aus Feldnamen und Werten angegeben.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

Dokument löschen (per ID)
=========================

Löscht ein Dokument anhand der Dokument-ID.

Request
-------

::

    DELETE /api/admin/searchlist/doc/{id}

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``id``
     - String
     - Ja
     - Dokument-ID (``doc_id``, Pfadparameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Dokument löschen (per Query)
============================

Löscht alle Dokumente, die der Suchanfrage entsprechen, in einem Vorgang.

Request
-------

::

    DELETE /api/admin/searchlist/query

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``q``
     - String
     - Ja
     - Suchanfrage für die zu löschenden Dokumente

Response
--------

Gibt die Anzahl der gelöschten Dokumente in ``count`` zurück.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

Verwendungsbeispiele
====================

Dokumente suchen
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

Dokument abrufen
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

Dokument per Query löschen
--------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-documents` - API zur Massenregistrierung von Dokumenten
- :doc:`api-admin-crawlinginfo` - Crawl-Informations-API
- :doc:`../../admin/searchlist-guide` - Anleitung zur Verwaltung der Suchliste
