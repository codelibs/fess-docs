=========
Such-API
=========

Dieses Dokument beschreibt die v2-Such-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope, zum Fehlermodell und zu CSRF finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

Dokumente suchen
================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/search``
==================  ====================================================

Sucht nach Dokumenten, die der Abfrage entsprechen, und gibt die Ergebnisse im gemeinsamen Envelope zurück.
Alle Feldnamen im Payload verwenden ``snake_case``.

Anfrageparameter
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``q``
     - Suchbegriff (URL-kodiert).
   * - ``start``
     - Startposition (0-basiert; integer, ``>=0``, Standardwert ``0``).
   * - ``offset``
     - Offset von ``start`` (integer, ``>=0``, Standardwert ``0``).
   * - ``num``
     - Seitengröße (integer, ``>=1``, Standardwert ``20``). ``<= 0`` ergibt ``invalid_request``. Werte über dem konfigurierten Maximum werden stillschweigend begrenzt. Ob eine Begrenzung stattfand, lässt sich durch Vergleich von ``num`` im Request und ``page_size`` im Response feststellen.
   * - ``sort``
     - Sortierung (z. B. ``score``).
   * - ``lang``
     - Suchsprache. Kann mehrfach angegeben werden (Array). Beispiel: ``en``.
   * - ``ex_q``
     - Zusätzlicher Abfrageausdruck. Kann mehrfach angegeben werden.
   * - ``sdh``
     - Ähnlichkeits-Dokument-Hash (similar-document hash).
   * - ``fields.label``
     - Filtert nach Label-Name. Kann mehrfach angegeben werden. Dies ist der häufigste Anwendungsfall der allgemeinen ``fields.<name>``-Familie; beliebige ``fields.<name>``-Abfrageparameter schränken die Ergebnisse auf Dokumente ein, deren Feld ``<name>`` mit dem angegebenen Wert übereinstimmt.
   * - ``as.*``
     - Erweiterte Suchbedingungen. Beliebige ``as.<name>``-Parameter (z. B. ``as.q``, ``as.filetype``) werden an den erweiterten Suchbedingungsgenerator übergeben. Pro Name können mehrere Werte angegeben werden.
   * - ``track_total_hits``
     - Wird an die Suchmaschine weitergeleitet und steuert die genaue Trefferanzahl (z. B. ``true`` oder ein ganzzahliger Schwellenwert). Beeinflusst, ob ``record_count_relation`` ``eq`` oder ``gte`` ist.
   * - ``facet.field``
     - Facettenfeld. Kann mehrfach angegeben werden (Array).
   * - ``facet.query``
     - Facettenabfrage. Kann mehrfach angegeben werden (Array).
   * - ``facet.size``
     - Maximale Anzahl zurückgegebener Facettenbegriffe (integer).
   * - ``facet.minDocCount``
     - Minimale Dokumentanzahl für einen Facettenbegriff (integer).
   * - ``facet.sort``
     - Sortierung der Facetten.
   * - ``facet.missing``
     - Behandlung von Facetten für Dokumente ohne Wert.
   * - ``geo.location.point``
     - Mittelpunkt der Geokoordinate (z. B. ``35.0,139.0``).
   * - ``geo.location.distance``
     - Entfernung vom Mittelpunkt (z. B. ``10km``).

Tabelle: Anfrageparameter

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` im gemeinsamen Envelope zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "q": "Fess",
        "query_id": "f8b1c2d3e4a5",
        "exec_time": 0.012,
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 42,
        "record_count_relation": "eq",
        "page_count": 3,
        "highlight_params": "&hq=Fess",
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "related_query": ["enterprise search"],
        "related_contents": [],
        "data": [
          {
            "doc_id": "a1b2c3d4e5f6",
            "url": "https://example.com/",
            "title": "Example",
            "content_description": "An example document about Fess.",
            "score": 1.2345
          }
        ],
        "facet_field": [
          {
            "name": "label",
            "result": [
              { "value": "news", "count": 12 }
            ]
          }
        ],
        "facet_query": [
          { "value": "filetype:html", "count": 30 }
        ]
      }
    }

Die einzelnen Felder sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``q``
     - Suchbegriff (nullable).
   * - ``query_id``
     - Bezeichner der Abfrage.
   * - ``exec_time``
     - Ausführungszeit (double, Sekunden).
   * - ``query_time``
     - Abfragezeit der Suchmaschine (int64, Millisekunden).
   * - ``page_size``
     - Seitengröße.
   * - ``page_number``
     - Aktuelle Seitennummer.
   * - ``record_count``
     - Anzahl der Treffer (int64).
   * - ``record_count_relation``
     - Bei ``eq`` ist die Anzahl exakt; bei ``gte`` ist nur eine Untergrenze bekannt.
   * - ``page_count``
     - Gesamtanzahl der Seiten.
   * - ``highlight_params``
     - Abfrageparameter-Zeichenkette für die Hervorhebung.
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
     - Gibt an, ob das Ergebnis unvollständig ist (bool).
   * - ``search_query``
     - Tatsächlich ausgeführte Suchabfrage.
   * - ``requested_time``
     - Zeitpunkt der Anfrage (int64, Epoch-Millisekunden).
   * - ``related_query``
     - Array verwandter Abfragen (Zeichenketten).
   * - ``related_contents``
     - Array verwandter Inhalte (Zeichenketten).
   * - ``data``
     - Array der Suchergebnisse. Ein Element pro Dokument. Nur Felder, die von ``QueryFieldConfig#isApiResponseField`` erlaubt werden, sind enthalten; null-Werte und leere Schlüssel werden ausgeschlossen.
   * - ``facet_field``
     - Array, das nur vorhanden ist, wenn Facettenfelder angefordert wurden. Jedes Element hat die Struktur ``{name, result:[{value, count}]}``.
   * - ``facet_query``
     - Array, das nur vorhanden ist, wenn Facettenabfragen angefordert wurden. Jedes Element hat die Struktur ``{value, count}``.

Tabelle: Antwortfelder

Fehlerantwort
~~~~~~~~~~~~~

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort

Alle Dokumente abrufen (Scroll-Suche / NDJSON)
===============================================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/documents/all``
==================  ====================================================

Überträgt alle zur Abfrage passenden Dokumente als NDJSON (``application/x-ndjson``).
Jede Zeile ist ein ``{"data":{...}}``-Objekt, das die von ``QueryFieldConfig#isApiResponseField`` erlaubten Felder enthält.

Wenn der Stream während der Übertragung fehlschlägt, wird als letzte Zeile folgendes ausgegeben und geflusht:

::

    {"error":{"code":"internal_error","message":"stream error"}}

Daher müssen Clients den ersten Schlüssel der letzten Zeile prüfen, um zwischen normalem Abschluss (``data``) und einem Serverfehler (``error``) zu unterscheiden.

Die Abfrage wird mit denselben Parametern wie ``GET /search`` erstellt (``q``, ``sort``, ``num``, ``lang``, ``ex_q``, ``sdh``, ``fields.*``, ``as.*``, ``track_total_hits``, ``facet.*``, ``geo.*``).
Wenn die Scroll-Suche durch ``api.search.scroll=false`` deaktiviert ist, wird ``invalid_request`` (400) zurückgegeben.

Anfrageparameter
~~~~~~~~~~~~~~~~

Folgende Parameter sind in der Spezifikation explizit aufgeführt:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrageparameter

   * - ``q``
     - Suchbegriff.
   * - ``sort``
     - Sortierung.
   * - ``num``
     - Größe einer Seite (Scroll-Batch) (integer, ``>=1``). ``<= 0`` ergibt ``invalid_request``.
   * - ``lang``
     - Suchsprache. Kann mehrfach angegeben werden (Array).
   * - ``ex_q``
     - Zusätzlicher Abfrageausdruck. Kann mehrfach angegeben werden (Array).
   * - ``fields.label``
     - Filtert nach Label-Name. Kann mehrfach angegeben werden (Array). Teil der allgemeinen ``fields.<name>``-Familie (siehe ``GET /search``).
   * - ``sdh``
     - Ähnlichkeits-Dokument-Hash (similar-document hash).

Tabelle: Anfrageparameter

Antwort
-------

Bei Erfolg (200) ist der Content-Type ``application/x-ndjson``, und die Ausgabe erfolgt zeilenweise, ein Dokument pro Zeile:

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

Fehlerantwort
~~~~~~~~~~~~~

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Ungültige Abfrage, ``num <= 0`` oder Scroll-Suche durch ``api.search.scroll=false`` deaktiviert.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
