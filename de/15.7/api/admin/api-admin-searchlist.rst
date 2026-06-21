==========================
SearchList API
==========================

Übersicht
=========

Die SearchList API ist eine Admin API zum Suchen und Verwalten von Dokumenten im |Fess|-Index.
Sie ermöglicht das Suchen, Abrufen, Erstellen, Aktualisieren und Löschen von Dokumenten.

Alle Feldnamen in der Antwort verwenden ``snake_case``. Felder mit dem Wert ``null`` werden in der Antwort weggelassen.

Basis-URL
=========

::

    /api/admin/searchlist

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
     - Dokumente löschen (per Query)

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
     - Suchanfrage (max. 1000 Zeichen). Wenn nicht angegeben, werden alle Dokumente berücksichtigt.
   * - ``sort``
     - String
     - Nein
     - Sortierfeld und -richtung (z. B. ``last_modified.desc``).
   * - ``start``
     - Integer
     - Nein
     - Nullbasierte Startposition (Standard ``0``).
   * - ``offset``
     - Integer
     - Nein
     - Offset ab ``start`` (Standard ``0``).
   * - ``pn``
     - Integer
     - Nein
     - Seitennummer.
   * - ``num``
     - Integer
     - Nein
     - Anzahl der abzurufenden Einträge (Standard ``10``). Werte, die das konfigurierte Maximum (Standard ``100``) überschreiten, sowie Werte von ``0`` oder kleiner werden auf das Maximum begrenzt.
   * - ``size``
     - Integer
     - Nein
     - Anzahl der abzurufenden Einträge (Alias für ``num``, zur Kompatibilität mit anderen Admin APIs).
   * - ``lang``
     - String[]
     - Nein
     - Suchsprache. Kann mehrfach angegeben werden (Array). z. B. ``en``.
   * - ``ex_q``
     - String[]
     - Nein
     - Zusätzliche Abfrageausdrücke. Kann mehrfach angegeben werden (Array).
   * - ``fields.<name>``
     - String[]
     - Nein
     - Filtert nach Feldwert. Der häufigste Fall ist ``fields.label`` (Filtern nach Label-Name); jedes ``fields.<name>`` schränkt die Ergebnisse auf Dokumente ein, deren Feld ``<name>`` mit dem angegebenen Wert übereinstimmt. Kann mehrfach angegeben werden.
   * - ``as.<name>``
     - String[]
     - Nein
     - Erweiterte Suchbedingungen. Beliebige ``as.<name>``-Parameter (z. B. ``as.q``) werden an den erweiterten Suchbedingungsgenerator übergeben. Pro Name können mehrere Werte angegeben werden.
   * - ``sdh``
     - String
     - Nein
     - Ähnlichkeits-Dokument-Hash (similar-document hash).

.. note::

   Dieser Endpunkt unterstützt kein Faceting, keine Hervorhebung und keine Geo-Suche. Entsprechende Parameter werden ignoriert, wenn sie angegeben werden.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
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
   * - ``version``
     - Die Version des laufenden |Fess| (der Beispielwert ist illustrativ).
   * - ``status``
     - Statuscode (``0`` für Erfolg; siehe „Statuscodes").
   * - ``query_id``
     - Such-Query-ID.
   * - ``docs``
     - Array der Suchergebnis-Dokumente. Jedes Dokument ist eine Map aus Feldnamen und Werten, wobei die Index-Feldnamen unverändert verwendet werden (``doc_id``, ``url``, ``title``, ``content_description`` usw.).
   * - ``exec_time``
     - Ausführungszeit der Suche (Sekunden, Zeichenkette).
   * - ``query_time``
     - Abfragezeit der Suchmaschine (Millisekunden).
   * - ``page_size``
     - Anzahl der Einträge pro Seite.
   * - ``page_number``
     - Aktuelle Seitennummer.
   * - ``record_count``
     - Anzahl der Treffer.
   * - ``record_count_relation``
     - Beziehung der Trefferanzahl. ``eq`` bedeutet eine exakte Anzahl, ``gte`` bedeutet, dass nur eine Untergrenze bekannt ist.
   * - ``page_count``
     - Gesamtanzahl der Seiten.
   * - ``next_page``
     - Gibt an, ob eine nächste Seite vorhanden ist (bool).
   * - ``prev_page``
     - Gibt an, ob eine vorherige Seite vorhanden ist (bool).
   * - ``start_record_number``
     - Startdatensatznummer dieser Seite.
   * - ``end_record_number``
     - Enddatensatznummer dieser Seite.
   * - ``page_numbers``
     - Array der im Pager angezeigten Seitennummern (Zeichenketten).
   * - ``partial``
     - Gibt an, ob die Ergebnisse unvollständig sind (bool).
   * - ``search_query``
     - Die tatsächlich ausgeführte Suchabfrage.
   * - ``requested_time``
     - Zeitpunkt der Anfrage (Epoch-Millisekunden).
   * - ``highlight_params``
     - Abfrageparameter-Zeichenkette für die Hervorhebung (für diese Admin API in der Regel leer).

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
     - Dokument-ID (der Wert von ``doc_id``, Pfadparameter).

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
          "title": "Sample Page 1"
        }
      }
    }

Wenn für die angegebene ID kein Dokument vorhanden ist, wird eine Fehlerantwort (``status`` = ``1``) zurückgegeben.

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
        "title": "Sample Page 1",
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
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
     - Das zu registrierende Dokument. Wird als Map aus Index-Feldnamen und Werten angegeben.

Von den in ``doc`` angegebenen Feldern müssen alle Pflichtfelder, die in ``index.admin.required.fields`` konfiguriert sind (Standard ``url,title,role,boost``), angegeben werden.
Im Gegensatz zur Massenregistrierung über die :doc:`Documents API <api-admin-documents>` vervollständigt dieser Endpunkt keine Standardwerte wie ``role`` oder ``boost`` automatisch, daher müssen die Pflichtfelder explizit in der Anfrage angegeben werden.
``doc_id`` wird serverseitig automatisch generiert und muss beim Erstellen nicht angegeben werden.

Die Werte der einzelnen Felder werden gemäß den Feldtypkonfigurationen validiert. Bei Typinkonsistenz wird ein Fehler (``status`` = ``1``) zurückgegeben.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Konfigurationsschlüssel
     - Standard
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - (leer)
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - (leer)

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

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``id``
     - Die ``doc_id`` des registrierten Dokuments.
   * - ``created``
     - ``true`` bei Neuerstellung.

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
        "title": "Updated Title",
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
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
     - Das zu aktualisierende Dokument. Wird als Map aus Index-Feldnamen und Werten angegeben.

Das zu aktualisierende Dokument wird über ``doc_id`` innerhalb von ``doc`` identifiziert. Wenn ``doc_id`` nicht angegeben ist oder kein passendes Dokument vorhanden ist, wird ein Fehler (``status`` = ``1``) zurückgegeben.
Wie beim Erstellen müssen alle Pflichtfelder, die in ``index.admin.required.fields`` konfiguriert sind (Standard ``url,title,role,boost``), angegeben werden, und die Feldwerte werden gemäß den Typkonfigurationen validiert.

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

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``id``
     - Die ``doc_id`` des aktualisierten Dokuments.
   * - ``created``
     - ``false`` bei Aktualisierung.

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
     - Dokument-ID (der Wert von ``doc_id``, Pfadparameter).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Dokumente löschen (per Query)
==============================

Löscht alle Dokumente, die einer Suchanfrage entsprechen, in einem Vorgang.

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
     - Suchanfrage für die zu löschenden Dokumente.

Das Löschziel wird mit derselben Abfrage wie bei „Dokumente suchen" erstellt, sodass Einschränkungsparameter wie ``fields.<name>`` und ``ex_q`` gemeinsam verwendet werden können. Wenn ``q`` nicht angegeben ist, wird ein Fehler (``status`` = ``1``) zurückgegeben.

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

Statuscodes
===========

Das Feld ``status`` in der Antwort wird auf einen der folgenden Werte gesetzt.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Wert
     - Name
     - Beschreibung
   * - ``0``
     - OK
     - Erfolg.
   * - ``1``
     - BAD_REQUEST
     - Die Anfrage ist ungültig (fehlendes Pflichtfeld, Typinkonsistenz, Zieldokument nicht gefunden, ungültige Abfrage usw.).
   * - ``2``
     - SYSTEM_ERROR
     - Systemfehler.
   * - ``3``
     - UNAUTHORIZED
     - Authentifizierungsfehler.
   * - ``9``
     - FAILED
     - Verarbeitung fehlgeschlagen.

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

Dokument erstellen
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

Dokumente per Query löschen
----------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-documents` - API zur Massenregistrierung von Dokumenten
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`../../admin/searchlist-guide` - Anleitung zur Verwaltung der Suchliste
