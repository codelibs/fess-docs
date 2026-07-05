==========================
Documents API
==========================

Übersicht
=========

Die Documents API dient zur Verwaltung von Dokumenten im Index von |Fess|.
Sie können Operationen wie Massenlöschung, Aktualisierung und Suche von Dokumenten durchführen.

Basis-URL
=========

::

    /api/admin/documents

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - DELETE
     - /
     - Dokumente löschen (Query-basiert)
   * - DELETE
     - /{id}
     - Dokument löschen (ID-basiert)

Dokumente per Query löschen
===========================

Löscht alle Dokumente, die der Suchabfrage entsprechen.

Request
-------

::

    DELETE /api/admin/documents

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
     - Suchabfrage für zu löschende Dokumente

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

Beispiele
~~~~~~~~~

.. code-block:: bash

    # Dokumente einer bestimmten Website löschen
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Alte Dokumente löschen
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Dokumente mit bestimmtem Label löschen
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

Dokument per ID löschen
=======================

Löscht ein Dokument anhand seiner ID.

Request
-------

::

    DELETE /api/admin/documents/{id}

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
     - Dokument-ID (Pfadparameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Beispiel
~~~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

Query-Syntax
============

Für Löschabfragen kann die Standard-Suchsyntax von |Fess| verwendet werden.

Grundlegende Abfragen
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Abfragebeispiel
     - Beschreibung
   * - ``url:example.com``
     - Dokumente mit "example.com" in der URL
   * - ``url:https://example.com/*``
     - URLs mit bestimmtem Präfix
   * - ``host:example.com``
     - Dokumente eines bestimmten Hosts
   * - ``title:keyword``
     - Dokumente mit Schlüsselwort im Titel
   * - ``content:keyword``
     - Dokumente mit Schlüsselwort im Inhalt
   * - ``label:mylabel``
     - Dokumente mit bestimmtem Label

Datumsbereichsabfragen
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Abfragebeispiel
     - Beschreibung
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - Im angegebenen Zeitraum aktualisierte Dokumente
   * - ``lastModified:[* TO 2023-01-01]``
     - Vor dem angegebenen Datum aktualisierte Dokumente
   * - ``created:[2024-01-01 TO *]``
     - Nach dem angegebenen Datum erstellte Dokumente

Kombinierte Abfragen
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Abfragebeispiel
     - Beschreibung
   * - ``url:example.com AND label:blog``
     - UND-Bedingung
   * - ``url:example.com OR url:sample.com``
     - ODER-Bedingung
   * - ``NOT url:example.com``
     - NICHT-Bedingung
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - Gruppierung

Hinweise
========

Vorsichtsmaßnahmen bei Löschoperationen
---------------------------------------

.. warning::
   Löschoperationen können nicht rückgängig gemacht werden. Testen Sie vor der Ausführung in einer Produktionsumgebung unbedingt in einer Testumgebung.

- Bei der Löschung großer Dokumentmengen kann die Verarbeitung einige Zeit in Anspruch nehmen
- Während der Löschung kann die Index-Performance beeinträchtigt werden
- Nach der Löschung kann es etwas dauern, bis die Suchergebnisse aktualisiert sind

Empfohlene Praktiken
--------------------

1. **Vor dem Löschen bestätigen**: Verwenden Sie dieselbe Abfrage mit der Such-API, um die Löschziele zu überprüfen
2. **Schrittweises Löschen**: Führen Sie Massenlöschungen in mehreren Schritten durch
3. **Backup**: Sichern Sie wichtige Daten vorher

Verwendungsbeispiele
====================

Vorbereitung für Neuindexierung einer Website
---------------------------------------------

.. code-block:: bash

    # Alte Dokumente einer bestimmten Website löschen
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Crawl-Job starten
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Bereinigung alter Dokumente
---------------------------

.. code-block:: bash

    # Dokumente löschen, die seit über einem Jahr nicht aktualisiert wurden
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`../../admin/searchlist-guide` - Suchlistenverwaltungsanleitung
