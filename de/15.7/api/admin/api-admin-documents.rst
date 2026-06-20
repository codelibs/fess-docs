==========================
Documents API
==========================

Übersicht
=========

Die Documents API ist eine Admin API von |Fess|, mit der Dokumente gesammelt im Index registriert werden können.
Externe Systeme können Dokumente direkt zum Index hinzufügen, ohne den Crawler zu verwenden.
Mit einer einzigen Anfrage können mehrere Dokumente auf einmal registriert werden.

Basis-URL
=========

::

    /api/admin/documents

Authentifizierung
=================

Um diese API aufzurufen, ist eine Authentifizierung mit einem Access Token erforderlich, wie in :doc:`api-admin-overview` beschrieben.
Der Token muss mit der Zugriffsberechtigung für die Admin API (standardmäßig ``Radmin-api``) ausgestattet sein.
Diese Berechtigung kann über den Konfigurationsschlüssel ``api.admin.access.permissions`` geändert werden.

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

.. note::

   Dieser Endpunkt akzeptiert ausschließlich die Methode ``PUT``.

Dokumente gesammelt registrieren
=================================

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
     - Array der zu registrierenden Dokumente. Jedes Dokument wird als Map aus Feldnamen und Werten angegeben. Bei ``null`` oder einem leeren Array wird ein Fehler zurückgegeben (``status`` = ``1``).

Dokumentenfelder
~~~~~~~~~~~~~~~~

Für jedes Dokument können die Felder des Index frei als Map aus Namen und Werten angegeben werden.
Mindestens ``url`` und ``title`` müssen angegeben werden (gemäß der Konfiguration der Pflichtfelder
``index.admin.required.fields``; der Standardwert ist ``url,title,role,boost``, wobei
``role`` und ``boost`` wie unten beschrieben automatisch ergänzt werden und daher praktisch nur
``url`` und ``title`` verpflichtend sind).

Die folgenden Felder werden automatisch ergänzt, wenn sie weggelassen werden:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Standardwert bei Weglassen
   * - ``content_length``
     - Summe der Zeichenanzahl von ``title`` und ``content``
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - Such-Gastrolle (die für Gastbenutzer konfigurierte Suchrolle)
   * - ``last_modified``
     - Aktueller Zeitstempel
   * - ``timestamp``
     - Aktueller Zeitstempel

Außerdem werden folgende Felder bei der Registrierung automatisch generiert:

- ``id`` - Wird deterministisch aus der ``url`` (sowie ``role`` und ``virtual_host``) des Dokuments
  generiert und als Dokument-ID (``_id``) in OpenSearch verwendet. Der Wert wird in
  ``items[].id`` der Antwort zurückgegeben.
- ``doc_id`` - Bei jeder Registrierung wird eine zufällige UUID generiert und als Dokumentfeld gespeichert.

.. note::

   Da ``id`` deterministisch aus der ``url`` generiert wird, wird ein Dokument mit derselben ``url``
   beim erneuten Registrieren aktualisiert (``items[].result`` ist dann ``OK``).

Ergänzende Hinweise
~~~~~~~~~~~~~~~~~~~

- Enthält das Feld ``lang`` den Wert ``"auto"``, wird die Sprache automatisch aus dem Fließtext erkannt.
- Wird ``config_id`` angegeben, wird die Ingest-Pipeline der entsprechenden Crawl-Konfiguration angewendet.
- Ist die Thumbnail-Generierung aktiviert (``thumbnail.crawler.enabled``), wird bei der Registrierung
  versucht, ein Thumbnail zu erstellen.
- Die Werte der einzelnen Felder werden gemäß den Typkonfigurationen (``index.admin.array.fields``,
  ``index.admin.date.fields``, ``index.admin.long.fields`` usw.) validiert.
  Bei Typinkonsistenz wird ein Fehler zurückgegeben (``status`` = ``1``).

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

Ein ``status`` von ``0`` zeigt an, dass alle Dokumente erfolgreich registriert wurden.
Bei ``items[].result`` wird ``CREATED`` für neu erstellte Dokumente und ``OK`` für aktualisierte
vorhandene Dokumente gesetzt.

Schlägt die Registrierung bei einem der Einträge fehl, wird ``status`` zu ``9`` (FAILED) und
der betreffende Eintrag enthält ein ``message``-Feld (``result`` enthält dann einen Fehlerstatusname
wie ``CONFLICT`` oder ``BAD_REQUEST``). Erfolgreiche Einträge geben weiterhin ihre ``id`` zurück.

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

.. note::

   Ist die Anfrage selbst ungültig (``documents`` nicht angegeben oder leer, fehlende Pflichtfelder,
   Typinkonsistenz bei Feldern usw.), wird die Dokumentregistrierung nicht ausgeführt und es wird
   eine Fehlerantwort mit ``status`` = ``1`` (BAD_REQUEST) und ``message`` zurückgegeben.
   In diesem Fall wird kein ``items``-Array zurückgegeben.

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
     - Statusname des Verarbeitungsergebnisses. ``CREATED`` bei Neuerstellung, ``OK`` bei Aktualisierung, bei Fehlschlag ein Fehlerstatusname wie ``BAD_REQUEST``
   * - ``items[].id``
     - ID des registrierten Dokuments (nur bei Erfolg)
   * - ``items[].message``
     - Meldung mit dem Fehlergrund (nur bei Fehlschlag)

Verwendungsbeispiele
====================

Dokumente gesammelt registrieren
---------------------------------

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
