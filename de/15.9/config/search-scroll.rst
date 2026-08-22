================================
Massen-Abruf von Suchergebnissen
================================

Übersicht
=========

Bei der normalen Suche in |Fess| wird durch die Paging-Funktion nur eine bestimmte Anzahl von
Suchergebnissen angezeigt.
Wenn Sie alle Suchergebnisse auf einmal abrufen möchten, verwenden Sie die Scroll-Search-Funktion
(Scroll-Suche).

Diese Funktion ist nützlich, wenn alle Suchergebnisse verarbeitet werden müssen,
z. B. für den Massen-Datenexport, Backup oder die Analyse großer Datenmengen.

Anwendungsfälle
===============

Scroll-Suche eignet sich für folgende Zwecke:

- Vollständiger Export von Suchergebnissen
- Abruf großer Datenmengen für die Datenanalyse
- Datenabruf in der Batch-Verarbeitung
- Datensynchronisation mit externen Systemen
- Datenerfassung für die Berichtsgenerierung

.. warning::
   Scroll-Suche gibt große Datenmengen zurück und verbraucht daher im Vergleich zur normalen
   Suche mehr Serverressourcen. Aktivieren Sie diese Funktion nur bei Bedarf.

Konfiguration
=============

Aktivierung der Scroll-Suche
-----------------------------

Standardmäßig ist die Scroll-Suche aus Sicherheits- und Leistungsgründen deaktiviert.
Zur Aktivierung ändern Sie folgende Einstellung in
``app/WEB-INF/classes/fess_config.properties`` (bei RPM/DEB-Paketen in
``/etc/fess/fess_config.properties``):

::

    api.search.scroll=true

.. note::
   Nach einer Konfigurationsänderung muss |Fess| neu gestartet werden.

Gültigkeitsdauer des Scroll-Kontexts
--------------------------------------

Die Gültigkeitsdauer des Scroll-Kontexts ist in |Fess| intern auf ``1m`` (1 Minute) festgelegt.
Dieser Wert kann über ``fess_config.properties`` nicht geändert werden.

.. note::
   Die Einstellung ``index.scroll.search.timeout`` ist vorhanden, wird jedoch für interne
   Operationen (update by query / delete by query) verwendet, die mit Indexaktualisierungen oder
   -löschungen verbunden sind. Sie hat keinen Einfluss auf den Timeout dieser Funktion
   (Scroll-Suche).

Konfiguration der Response-Felder
-----------------------------------

Sie können die Felder anpassen, die in den Suchergebnissen enthalten sind.
Standardmäßig werden zahlreiche Felder zurückgegeben; Sie können jedoch zusätzliche Felder
angeben.

::

    query.additional.scroll.response.fields=content

Mehrere Felder werden durch Komma getrennt aufgelistet.

.. note::
   Das Feld ``content`` ist standardmäßig nicht in den Response-Feldern enthalten.
   Fügen Sie es mit der obigen Einstellung hinzu, wenn Sie den vollständigen Text abrufen
   möchten.

Verwendung
==========

Grundlegende Verwendung
------------------------

Der Zugriff auf die Scroll-Suche erfolgt über folgende URL:

::

    http://localhost:8080/api/v2/documents/all?q=Suchbegriff

Die Suchergebnisse werden im NDJSON-Format (Newline Delimited JSON) zurückgegeben.
Pro Zeile wird ein Dokument im JSON-Format ausgegeben.

**Beispiel:**

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess"

Request-Parameter
------------------

Für die Scroll-Suche können folgende Parameter verwendet werden:

.. note::
   Die Scroll-Suche unterstützt nur die GET-Methode. Bei Verwendung einer anderen HTTP-Methode
   wird ``405 Method Not Allowed`` zurückgegeben.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Parametername
     - Beschreibung
   * - ``q``
     - Suchabfrage (erforderlich)
   * - ``num``
     - Anzahl der Treffer pro Scroll-Abruf (Standard: 10, Maximum: 100)
   * - ``fields.label``
     - Filterung nach Label

.. note::
   Der maximale Wert von ``num`` wird durch ``paging.search.page.max.size`` (Standard: 100)
   gesteuert. Wird ein Wert angegeben, der das Maximum überschreitet, wird er automatisch auf
   den Maximalwert begrenzt. Als Standardwert wird ``paging.search.page.size`` (Standard: 10)
   verwendet. Wird für ``num`` ein Wert von 0 oder kleiner angegeben, wird ein Fehler
   (``INVALID_REQUEST``) zurückgegeben.

Angabe von Suchabfragen
------------------------

Sie können Suchabfragen wie bei der normalen Suche angeben.

**Beispiel: Schlüsselwortsuche**

::

    curl "http://localhost:8080/api/v2/documents/all?q=Suchmaschine"

**Beispiel: Feldspezifische Suche**

::

    curl "http://localhost:8080/api/v2/documents/all?q=title:Fess"

**Beispiel: Vollständiger Abruf (ohne Suchbedingung)**

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*"

Angabe der Abrufanzahl
-----------------------

Sie können die Anzahl der Treffer pro Scroll-Abruf ändern.

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess&num=100"

.. note::
   Ein zu großer ``num``-Parameter erhöht die Speichernutzung. Der Standardmaximalwert ist 100.
   Falls ein größerer Wert benötigt wird, ändern Sie die Einstellung
   ``paging.search.page.max.size``.

Filterung nach Label
---------------------

Sie können nur Dokumente bestimmter Labels abrufen.

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*&fields.label=public"

Zugriffskontrolle
------------------

.. note::
   Bei der Scroll-Suche wird wie bei der normalen Suche die rollenbasierte Zugriffskontrolle
   (RBAC) angewendet. Es werden nur Dokumente zurückgegeben, auf die der anfragende Benutzer
   gemäß seinen Rolleninformationen Zugriff hat. Dokumente ohne Leseberechtigung sind nicht
   im Ergebnis enthalten.

.. warning::
   Der Endpunkt der Scroll-Suche erfordert standardmäßig keine Authentifizierung (er ist für
   jeden zugänglich). Die zurückgegebenen Dokumente werden jedoch durch die oben beschriebene
   rollenbasierte Zugriffskontrolle gefiltert. Falls der Zugriff auf den Endpunkt selbst
   eingeschränkt werden soll, konfigurieren Sie eine IP-Adressen-Beschränkung oder
   Authentifizierung über einen Reverse-Proxy.

Response-Format
===============

NDJSON-Format
--------------

Die Response der Scroll-Suche wird im NDJSON-Format (Newline Delimited JSON) zurückgegeben.
Der Content-Type ist ``application/x-ndjson; charset=UTF-8``.
Jede Zeile repräsentiert ein Dokument, das in der Form ``{"data": {...}}`` eingeschlossen ist.

**Beispiel:**

::

    {"data":{"url":"http://example.com/page1","title":"Page 1","digest":"..."}}
    {"data":{"url":"http://example.com/page2","title":"Page 2","digest":"..."}}
    {"data":{"url":"http://example.com/page3","title":"Page 3","digest":"..."}}

.. note::
   Jedes Dokument wird unter dem Schlüssel ``data`` gespeichert. Auf Client-Seite ist nach dem
   Parsen jeder Zeile der Wert unter dem Schlüssel ``data`` zu lesen.

Verhalten im Fehlerfall
------------------------

Tritt auf der Serverseite ein Fehler auf, nachdem die Übertragung des Streams begonnen hat,
wird in der letzten Zeile der Response folgende Fehler-Abschlusszeile ausgegeben:

::

    {"error":{"code":"internal_error","message":"stream error"}}

.. note::
   Auf Client-Seite kann durch Prüfen, ob die letzte Zeile den Schlüssel ``error`` enthält,
   unterschieden werden, ob der Stream normal abgeschlossen wurde oder ob auf der Serverseite
   ein Fehler aufgetreten ist. Falls das Schreiben der Fehler-Abschlusszeile selbst fehlschlägt,
   wird keine Abschlusszeile ausgegeben und der Stream endet vorzeitig. Behandeln Sie daher auch
   unerwartete Verbindungsabbrüche als Fehler.

Response-Felder
----------------

Standardmäßig enthaltene Felder:

- ``score``: Suchscore
- ``_id``: Dokument-ID (OpenSearch-Dokument-ID)
- ``doc_id``: Dokument-ID (intern in |Fess|)
- ``boost``: Boost-Wert
- ``content_length``: Inhaltslänge
- ``host``: Hostname
- ``site``: Site
- ``last_modified``: Letztes Änderungsdatum
- ``timestamp``: Zeitstempel
- ``mimetype``: MIME-Typ
- ``filetype``: Dateityp
- ``filename``: Dateiname
- ``created``: Erstellungsdatum
- ``title``: Titel
- ``digest``: Textauszug
- ``url``: Dokument-URL
- ``thumbnail``: Vorschaubild
- ``click_count``: Klickanzahl
- ``favorite_count``: Favoritenanzahl
- ``has_cache``: Cache vorhanden
- ``content_title``: Anzeige-Titel
- ``content_description``: Textauszug für die Anzeige
- ``url_link``: Anzeige-Link-URL
- ``site_path``: Site-Pfad

.. note::
   Die tatsächlich ausgegebenen Felder sind auf die für die API-Response zugelassenen Felder
   beschränkt. Felder ohne Wert werden nicht ausgegeben.

.. note::
   ``content`` (Volltext) ist standardmäßig nicht enthalten.
   Er kann über ``query.additional.scroll.response.fields`` hinzugefügt werden.

Datenverarbeitungsbeispiele
============================

Verarbeitungsbeispiel mit Python
---------------------------------

.. code-block:: python

    import requests
    import json

    # Scroll-Suche ausführen
    url = "http://localhost:8080/api/v2/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # NDJSON-Response zeilenweise verarbeiten
    for line in response.iter_lines():
        if line:
            record = json.loads(line)
            if "error" in record:
                # Fehler mitten im Stream
                print("stream error:", record["error"])
                break
            doc = record["data"]
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Speichern in eine Datei
------------------------

Beispiel zum Speichern von Suchergebnissen in eine Datei:

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=*:*" > all_documents.ndjson

Konvertierung zu CSV
---------------------

Beispiel für die Konvertierung zu CSV mit dem jq-Befehl:

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=Fess" | \
        jq -r '.data | [.url, .title, .score] | @csv' > results.csv

Datenanalyse
-------------

Beispiel für die Analyse abgerufener Daten:

.. code-block:: python

    import json
    import pandas as pd

    # NDJSON-Datei einlesen (data-Schlüssel aus jeder Zeile entnehmen)
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            record = json.loads(line)
            if "data" in record:
                documents.append(record["data"])

    # In DataFrame konvertieren
    df = pd.DataFrame(documents)

    # Grundstatistik
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL-Domain-Analyse
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Leistung und Best Practices
============================

Effiziente Verwendung
----------------------

1. **Angemessene Einstellung des num-Parameters**

   - Zu klein erhöht den Kommunikations-Overhead
   - Zu groß erhöht die Speichernutzung
   - Standardmaximalwert: 100

2. **Optimierung der Suchbedingungen**

   - Suchbedingungen so angeben, dass nur benötigte Dokumente abgerufen werden
   - Vollständigen Abruf nur bei wirklichem Bedarf ausführen

3. **Nutzung von Nebenzeiten**

   - Abruf großer Datenmengen in Zeiten niedriger Systemlast ausführen

4. **Verwendung in der Batch-Verarbeitung**

   - Regelmäßige Datensynchronisation als Batch-Job ausführen

Optimierung der Speichernutzung
---------------------------------

Bei der Verarbeitung großer Datenmengen verwenden Sie Streaming-Verarbeitung, um die
Speichernutzung zu reduzieren.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v2/documents/all"
    params = {"q": "*:*", "num": 100}

    # Mit Streaming verarbeiten
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                record = json.loads(line)
                if "error" in record:
                    break
                # Dokument verarbeiten
                process_document(record["data"])

Sicherheitsüberlegungen
========================

Zugriffsbeschränkung
---------------------

Da die Scroll-Suche große Datenmengen zurückgibt, konfigurieren Sie angemessene
Zugriffsbeschränkungen. Da der Endpunkt selbst standardmäßig keine Authentifizierung erfordert,
erwägen Sie bei Bedarf folgende Maßnahmen:

1. **IP-Adressen-Beschränkung**

   Zugriff nur von bestimmten IP-Adressen erlauben

2. **API-Authentifizierung**

   API-Token oder Basic-Authentifizierung über einen Reverse-Proxy verwenden

3. **Rollenbasierte Zugriffskontrolle**

   Die zurückgegebenen Dokumente werden durch die rollenbasierte Zugriffskontrolle von |Fess|
   gefiltert

Rate-Limiting
--------------

Zur Vermeidung übermäßiger Zugriffe wird empfohlen, Rate-Limiting im Reverse-Proxy zu
konfigurieren.

Fehlerbehebung
==============

Scroll-Suche nicht verfügbar
------------------------------

1. Überprüfen Sie, ob ``api.search.scroll`` auf ``true`` gesetzt ist.
2. Überprüfen Sie, ob |Fess| neu gestartet wurde.
3. Überprüfen Sie die Fehlerprotokolle.

Timeout-Fehler tritt auf
-------------------------

1. Verkleinern Sie den ``num``-Parameter, um die Verarbeitung zu verteilen.
2. Grenzen Sie die Suchbedingungen ein, um die abzurufende Datenmenge zu reduzieren.

Speichermangel-Fehler
----------------------

1. Verkleinern Sie den ``num``-Parameter.
2. Erhöhen Sie den Heap-Speicher von |Fess|.
3. Überprüfen Sie den Heap-Speicher von OpenSearch.

Response ist leer
------------------

1. Überprüfen Sie, ob die Suchabfrage korrekt ist.
2. Überprüfen Sie, ob die angegebenen Labels oder Filterbedingungen korrekt sind.
3. Aufgrund der rollenbasierten Zugriffskontrolle sind Dokumente ohne Leseberechtigung nicht
   im Ergebnis enthalten. Überprüfen Sie die Rolleneinstellungen des Requests.

Referenzinformationen
=====================

- :doc:`search-basic` - Details zu Suchfunktionen
- :doc:`search-advanced` - Suchbezogene Konfigurationen
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
