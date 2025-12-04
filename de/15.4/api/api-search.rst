==========
Such-API
==========

Abrufen von Suchergebnissen
============================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v1/documents``
==================  ====================================================

Durch Senden einer Anfrage wie
``http://<Servername>/api/v1/documents?q=Suchbegriff``
an |Fess| können Sie die Suchergebnisse von |Fess| im JSON-Format erhalten.
Um die Such-API zu nutzen, muss die JSON-Antwort in der Administrationsoberfläche unter System > Allgemeine Einstellungen aktiviert sein.

Anfrageparameter
----------------

Durch Angabe von Anfrageparametern wie
``http://<Servername>/api/v1/documents?q=Suchbegriff&num=50&fields.label=fess``
können Sie erweiterte Suchfunktionen durchführen.
Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Suchbegriff. Wird URL-codiert übergeben.
   * - start
     - Startposition der Ergebnisse. Beginnt bei 0.
   * - num
     - Anzahl der Ergebnisse. Standard ist 20. Maximal können 100 Ergebnisse angezeigt werden.
   * - sort
     - Sortierung. Wird verwendet, um die Suchergebnisse zu sortieren.
   * - fields.label
     - Label-Wert. Wird verwendet, um ein Label anzugeben.
   * - facet.field
     - Angabe des Facettenfeldes. (Beispiel) ``facet.field=label``
   * - facet.query
     - Angabe der Facettenabfrage. (Beispiel) ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - Angabe der maximalen Anzahl der abzurufenden Facetten. Gilt, wenn facet.field angegeben ist.
   * - facet.minDocCount
     - Ruft Facetten ab, deren Anzahl größer oder gleich diesem Wert ist. Gilt, wenn facet.field angegeben ist.
   * - geo.location.point
     - Angabe von Breiten- und Längengrad. (Beispiel) ``geo.location.point=35.0,139.0``
   * - geo.location.distance
     - Angabe der Entfernung vom Mittelpunkt. (Beispiel) ``geo.location.distance=10km``
   * - lang
     - Angabe der Suchsprache. (Beispiel) ``lang=en``
   * - preference
     - Zeichenfolge zur Angabe des Shards bei der Suche. (Beispiel) ``preference=abc``
   * - callback
     - Callback-Name bei Verwendung von JSONP. Muss nicht angegeben werden, wenn JSONP nicht verwendet wird.

Tabelle: Anfrageparameter


Antwort
-------

| Es wird folgende Antwort zurückgegeben.
| (Formatiert dargestellt)

::

    {
      "q": "Fess",
      "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
      "exec_time": 0.21,
      "query_time": 0,
      "page_size": 20,
      "page_number": 1,
      "record_count": 31625,
      "page_count": 1,
      "highlight_params": "&hq=n2sm&hq=Fess",
      "next_page": true,
      "prev_page": false,
      "start_record_number": 1,
      "end_record_number": 20,
      "page_numbers": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "partial": false,
      "search_query": "(Fess OR n2sm)",
      "requested_time": 1507822131845,
      "related_query": [
        "aaa"
      ],
      "related_contents": [],
      "data": [
        {
          "filetype": "html",
          "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
          "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
          "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess ? Fess is very powerful and easily deployable Enterprise Search Server. ...",
          "host": "fess.codelibs.org",
          "last_modified": "2017-10-09T22:28:56.000Z",
          "content_length": "29624",
          "timestamp": "2017-10-09T22:28:56.000Z",
          "url_link": "https://fess.codelibs.org/",
          "created": "2017-10-10T15.40:48.609Z",
          "site_path": "fess.codelibs.org/",
          "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
          "url": "https://fess.codelibs.org/",
          "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is OpenSearch-based search",
          "site": "fess.codelibs.org/",
          "boost": "10.0",
          "mimetype": "text/html"
        }
      ]
    }

Die einzelnen Elemente sind wie folgt definiert:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Antwortinformationen

   * - q
     - Suchbegriff
   * - exec_time
     - Antwortzeit (Einheit: Sekunden)
   * - query_time
     - Abfrageverarbeitungszeit (Einheit: Millisekunden)
   * - page_size
     - Anzahl der Ergebnisse
   * - page_number
     - Seitennummer
   * - record_count
     - Anzahl der Treffer für den Suchbegriff
   * - page_count
     - Anzahl der Seiten der Treffer für den Suchbegriff
   * - highlight_params
     - Hervorhebungsparameter
   * - next_page
     - true: Nächste Seite existiert. false: Nächste Seite existiert nicht.
   * - prev_page
     - true: Vorherige Seite existiert. false: Vorherige Seite existiert nicht.
   * - start_record_number
     - Startposition der Datensatznummer
   * - end_record_number
     - Endposition der Datensatznummer
   * - page_numbers
     - Array der Seitennummern
   * - partial
     - Wird true, wenn das Suchergebnis abgebrochen wurde, z.B. bei Zeitüberschreitung.
   * - search_query
     - Suchabfrage
   * - requested_time
     - Anfragezeitpunkt (Einheit: Epoch-Millisekunden)
   * - related_query
     - Verwandte Abfragen
   * - related_contents
     - Abfragen für verwandte Inhalte
   * - facet_field
     - Informationen über Dokumente, die auf das angegebene Facettenfeld zutreffen (nur wenn ``facet.field`` im Anfrageparameter angegeben wurde)
   * - facet_query
     - Anzahl der Dokumente, die auf die angegebene Facettenabfrage zutreffen (nur wenn ``facet.query`` im Anfrageparameter angegeben wurde)
   * - result
     - Übergeordnetes Element der Suchergebnisse
   * - filetype
     - Dateityp
   * - created
     - Erstellungsdatum des Dokuments
   * - title
     - Titel des Dokuments
   * - doc_id
     - ID des Dokuments
   * - url
     - URL des Dokuments
   * - site
     - Site-Name
   * - content_description
     - Beschreibung des Inhalts
   * - host
     - Hostname
   * - digest
     - Zusammenfassung des Dokuments
   * - boost
     - Boost-Wert des Dokuments
   * - mimetype
     - MIME-Typ
   * - last_modified
     - Letztes Änderungsdatum
   * - content_length
     - Größe des Dokuments
   * - url_link
     - URL als Suchergebnis
   * - timestamp
     - Aktualisierungszeitpunkt des Dokuments


Suche in allen Dokumenten
==========================

Um alle Zieldokumente zu durchsuchen, senden Sie folgende Anfrage:
``http://<Servername>/api/v1/documents/all?q=Suchbegriff``

Um diese Funktion zu nutzen, muss in fess_config.properties die Einstellung api.search.scroll auf true gesetzt werden.

Anfrageparameter
----------------

Die verfügbaren Anfrageparameter sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Suchbegriff. Wird URL-codiert übergeben.
   * - num
     - Anzahl der Ergebnisse. Standard ist 20. Maximal können 100 Ergebnisse angezeigt werden.
   * - sort
     - Sortierung. Wird verwendet, um die Suchergebnisse zu sortieren.

Tabelle: Anfrageparameter

Fehlerantworten
===============

Wenn die Such-API fehlschlägt, wird folgende Fehlerantwort zurückgegeben:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantworten

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrageparameter ungültig sind
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler aufgetreten ist

Beispiel für eine Fehlerantwort:

::

    {
      "message": "Invalid request parameter",
      "status": 400
    }
