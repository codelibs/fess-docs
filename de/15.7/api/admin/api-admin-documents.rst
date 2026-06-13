==========================
Documents API
==========================

Übersicht
=========

Die Documents API dient zur gesammelten Registrierung von Dokumenten im Index von |Fess|.
Sie können mehrere Dokumente auf einmal zum Index hinzufügen.

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
   * - PUT
     - /bulk
     - Dokumente gesammelt registrieren

Dokumente gesammelt registrieren
================================

Registriert mehrere Dokumente gesammelt im Index.

Request
-------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "Beispielseite 1",
          "content": "Dies ist der Textinhalt von Seite 1."
        },
        {
          "url": "https://example.com/page2",
          "title": "Beispielseite 2",
          "content": "Dies ist der Textinhalt von Seite 2."
        }
      ]
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``documents``
     - Ja
     - Array der zu registrierenden Dokumente. Jedes Dokument wird als Map aus Feldnamen und Werten angegeben. Ein leeres Array ist nicht zulässig.

Für jedes Dokument können Index-Felder wie ``url``, ``title``, ``content`` usw. frei angegeben werden.
Werden ``content_length``, ``favorite_count``, ``click_count``, ``boost``, ``role``, ``last_modified``, ``timestamp`` usw. weggelassen, werden die Standardwerte automatisch ergänzt.
Außerdem werden ``doc_id`` und die ID bei der Registrierung automatisch generiert.

Response
--------

Die Antwort gibt das Verarbeitungsergebnis jedes registrierten Dokuments im Array ``items`` zurück.
Erfolgreiche Einträge enthalten ``result`` und ``id``, fehlgeschlagene Einträge enthalten ``result`` und ``message``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

Schlägt die Registrierung bei einem der Einträge fehl, wird ``status`` zu ``9`` (FAILED) und der betreffende Eintrag enthält ein ``message``-Feld.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
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
   * - ``items``
     - Array der Verarbeitungsergebnisse je Dokument
   * - ``items[].result``
     - Status des Verarbeitungsergebnisses (Beispiel: ``CREATED``)
   * - ``items[].id``
     - ID des registrierten Dokuments (bei Erfolg)
   * - ``items[].message``
     - Meldung mit dem Fehlergrund (bei Fehlschlag)

Verwendungsbeispiele
====================

Dokumente gesammelt registrieren
--------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "Beispielseite 1",
               "content": "Dies ist der Textinhalt von Seite 1."
             }
           ]
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-searchlist` - Dokumentsuche- und -verwaltungs-API
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`../../admin/searchlist-guide` - Suchlistenverwaltungsanleitung
