==========================
RelatedQuery API
==========================

Übersicht
=========

Die RelatedQuery API dient zur Verwaltung von verwandten Suchabfragen in |Fess|.
Zu einem vom Benutzer eingegebenen Suchbegriff (``term``) können verwandte Suchbegriffskandidaten
(``queries``) registriert und verwaltet werden. Die registrierten verwandten Abfragen werden
auf der Suchoberfläche als verwandte Suchvorschläge angezeigt.

Informationen zur Authentifizierung, zum gemeinsamen Antwortformat (``version``-Feld und ``status``-Codes),
zur Paginierung sowie zu Fehler-Responses finden Sie unter :doc:`api-admin-overview`.

Basis-URL
=========

::

    /api/admin/relatedquery

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
     - Verwandte Abfragen Liste abrufen
   * - GET
     - /setting/{id}
     - Verwandte Abfrage abrufen
   * - POST
     - /setting
     - Verwandte Abfrage erstellen
   * - PUT
     - /setting
     - Verwandte Abfrage aktualisieren
   * - DELETE
     - /setting/{id}
     - Verwandte Abfrage löschen

Verwandte Abfragen Liste abrufen
=================================

Request
-------

::

    GET /api/admin/relatedquery/settings

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
     - Seitennummer (beginnt bei 1; Standard: 1)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Jede Einstellung enthält ``versionNo`` (Versionsnummer für optimistisches Sperren). ``virtualHost``
   und Audit-Felder (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``) werden nur dann
   aufgenommen, wenn ein Wert gesetzt ist. Ein leerer ``virtualHost`` wird nicht in die Response aufgenommen.

Verwandte Abfrage abrufen
==========================

Request
-------

::

    GET /api/admin/relatedquery/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

Verwandte Abfrage erstellen
============================

Request
-------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``term``
     - Ja
     - Suchbegriff (maximal 10000 Zeichen)
   * - ``queries``
     - Ja
     - Verwandte Abfragen. Zeilenumbruch-getrennte Zeichenkette mit einem Eintrag pro Zeile (Leerzeilen werden ignoriert; maximal 10000 Zeichen)
   * - ``virtualHost``
     - Nein
     - Virtueller Host (maximal 1000 Zeichen)

.. note::

   ``crudMode`` wird serverseitig automatisch gesetzt und muss nicht im Request-Body angegeben werden.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Verwandte Abfrage aktualisieren
================================

Request
-------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
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
     - ID der zu aktualisierenden verwandten Abfrage (maximal 1000 Zeichen)
   * - ``term``
     - Ja
     - Suchbegriff (maximal 10000 Zeichen)
   * - ``queries``
     - Ja
     - Verwandte Abfragen. Zeilenumbruch-getrennte Zeichenkette mit einem Eintrag pro Zeile (Leerzeilen werden ignoriert; maximal 10000 Zeichen)
   * - ``virtualHost``
     - Nein
     - Virtueller Host (maximal 1000 Zeichen)
   * - ``versionNo``
     - Ja
     - Versionsnummer für optimistisches Sperren. Geben Sie den beim Abrufen in der Response enthaltenen Wert an.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Verwandte Abfrage löschen
==========================

Request
-------

::

    DELETE /api/admin/relatedquery/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Fehler-Response
===============

Schlägt ein Request fehl, wird in ``status`` ein von 0 verschiedener Wert gesetzt und ``message`` enthält
eine Fehlerbeschreibung. Bei Validierungsfehlern, z. B. fehlenden Pflichtfeldern, wird ``status`` auf ``1`` gesetzt.
Eine Übersicht der Statuscodes finden Sie unter :doc:`api-admin-overview`.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "..."
      }
    }

Verwendungsbeispiele
====================

Produktbezogene Abfragen
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

Hilfebezogene Abfragen
-----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-relatedcontent` - Verwandte Inhalte API
- :doc:`api-admin-suggest` - Suggest-Verwaltung API
- :doc:`../../admin/relatedquery-guide` - Verwandte Abfragen Verwaltungsanleitung
