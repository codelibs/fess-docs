==================
Massen-Abruf von Suchergebnissen
==================

Übersicht
====

Bei normaler Suche in |Fess| wird durch Paging-Funktion nur eine bestimmte Anzahl von Suchergebnissen angezeigt.
Wenn Sie alle Suchergebnisse auf einmal abrufen möchten, verwenden Sie die Scroll-Search-Funktion.

Diese Funktion ist nützlich, wenn alle Suchergebnisse verarbeitet werden müssen,
z. B. für Massen-Datenexport, Backup oder Analyse großer Datenmengen.

Anwendungsfälle
============

Scroll-Suche eignet sich für folgende Zwecke:

- Vollständiger Export von Suchergebnissen
- Abruf großer Datenmengen für Datenanalyse
- Datenabruf in Batch-Verarbeitung
- Datensynchronisation mit externen Systemen
- Datenerfassung für Berichtsgenerierung

.. warning::
   Scroll-Suche gibt große Datenmengen zurück und verbraucht daher mehr
   Serverressourcen im Vergleich zur normalen Suche. Aktivieren Sie nur bei Bedarf.

Konfigurationsmethode
========

Aktivierung der Scroll-Suche
----------------------

Standardmäßig ist Scroll-Suche aus Sicherheits- und Leistungsgründen deaktiviert.
Zur Aktivierung ändern Sie in ``app/WEB-INF/classes/fess_config.properties`` oder ``/etc/fess/fess_config.properties``
folgende Einstellung:

::

    api.search.scroll=true

.. note::
   Nach Konfigurationsänderung muss |Fess| neu gestartet werden.

Konfiguration von Response-Feldern
--------------------------

Sie können Felder anpassen, die in Suchergebnissen enthalten sind.
Standardmäßig werden viele Felder zurückgegeben, Sie können jedoch zusätzliche Felder angeben.

::

    query.additional.scroll.response.fields=content

.. note::
   ``content`` ist standardmäßig nicht in den Response-Feldern enthalten.

Timeout-Einstellung für Scroll
----------------------------

Die Gültigkeitsdauer des Scroll-Kontexts wird serverseitig konfiguriert.
Standard ist ``3m`` (3 Minuten).

::

    index.scroll.search.timeout=3m

Verwendungsmethode
========

Grundlegende Verwendung
----------------

Zugriff auf Scroll-Suche erfolgt über folgende URL:

::

    http://localhost:8080/api/v1/documents/all?q=Suchschlüsselwort

Suchergebnisse werden im NDJSON-Format (Newline Delimited JSON) zurückgegeben.
Pro Zeile wird ein Dokument im JSON-Format ausgegeben.

**Beispiel:**

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess"

Request-Parameter
--------------------

Für Scroll-Suche können folgende Parameter verwendet werden:

.. note::
   Scroll-Suche unterstützt nur die GET-Methode.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Parametername
     - Beschreibung
   * - ``q``
     - Suchabfrage (erforderlich)
   * - ``num``
     - Anzahl pro Scroll-Abruf (Standard: 10, Maximum: 100)
   * - ``fields.label``
     - Filterung nach Label

.. note::
   Der maximale Wert von ``num`` wird durch ``paging.search.page.max.size`` gesteuert.

Angabe von Suchabfragen
----------------

Sie können Suchabfragen wie bei normaler Suche angeben.

**Beispiel: Schlüsselwortsuche**

::

    curl "http://localhost:8080/api/v1/documents/all?q=Suchmaschine"

**Beispiel: Feldspezifische Suche**

::

    curl "http://localhost:8080/api/v1/documents/all?q=title:Fess"

**Beispiel: Vollständiger Abruf (ohne Suchbedingung)**

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*"

Angabe der Abrufanzahl
--------------

Sie können die Anzahl pro Scroll-Abruf ändern.

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess&num=100"

.. note::
   Zu großer ``num``-Parameter erhöht Speichernutzung.
   Normalerweise wird ein Wert bis maximal 100 empfohlen.

Filterung nach Label
--------------------------

Sie können nur Dokumente bestimmter Labels abrufen.

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*&fields.label=public"

Hinweis zur Authentifizierung
-----------------------------

.. warning::
   Bei der Scroll-Suche wird die rollenbasierte Zugriffskontrolle (RBAC) von |Fess| nicht angewendet.
   Alle Dokumente, die den Suchkriterien entsprechen, werden unabhängig von den Benutzerberechtigungen zurückgegeben.
   Falls Zugriffsbeschränkungen erforderlich sind, konfigurieren Sie IP-Adressen-Beschränkung oder Authentifizierung über einen Reverse-Proxy.

Response-Format
==============

NDJSON-Format
----------

Scroll-Such-Response wird im NDJSON-Format (Newline Delimited JSON) zurückgegeben.
Jede Zeile repräsentiert ein Dokument.

**Beispiel:**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

Response-Felder
--------------------

Standardmäßig enthaltene Felder:

- ``url``: Dokument-URL
- ``doc_id``: Dokument-ID
- ``title``: Titel
- ``score``: Such-Score
- ``boost``: Boost-Wert
- ``content_length``: Inhaltslänge
- ``host``: Hostname
- ``site``: Site
- ``content_title``: Inhaltstitel
- ``content_description``: Inhaltsbeschreibung
- ``url_link``: URL-Link
- ``last_modified``: Letztes Änderungsdatum
- ``timestamp``: Zeitstempel
- ``created``: Erstellungsdatum
- ``mimetype``: MIME-Typ
- ``filetype``: Dateityp
- ``filename``: Dateiname
- ``favorite_count``: Favoritenanzahl
- ``click_count``: Klickanzahl
- ``config_id``: Konfiguration-ID
- ``_id``: Interne ID
- ``label``: Label

.. note::
   ``content`` ist standardmäßig nicht in den Response-Feldern enthalten.
   Um ``content`` zu erhalten, konfigurieren Sie ``query.additional.scroll.response.fields=content``.

Datenverarbeitungsbeispiele
============

Verarbeitungsbeispiel mit Python
----------------

.. code-block:: python

    import requests
    import json

    # Scroll-Suche ausführen
    url = "http://localhost:8080/api/v1/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # NDJSON-Response zeilenweise verarbeiten
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Speichern in Datei
----------------

Beispiel zum Speichern von Suchergebnissen in Datei:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=*:*" > all_documents.ndjson

Konvertierung zu CSV
-----------

Beispiel für Konvertierung zu CSV mit jq-Befehl:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

Datenanalyse
----------

Beispiel für Analyse abgerufener Daten:

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # NDJSON-Datei einlesen
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # In DataFrame konvertieren
    df = pd.DataFrame(documents)

    # Grundstatistik
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL-Domain-Analyse
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Leistung und Best Practices
==================================

Effiziente Verwendung
----------------

1. **Angemessene num-Parameter-Einstellung**

   - Zu klein erhöht Kommunikations-Overhead
   - Zu groß erhöht Speichernutzung
   - Standard-Maximum: 100

2. **Optimierung von Suchbedingungen**

   - Suchbedingungen so angeben, dass nur benötigte Dokumente abgerufen werden
   - Vollständigen Abruf nur bei wirklichem Bedarf ausführen

3. **Nutzung von Off-Peak-Zeiten**

   - Abruf großer Datenmengen in Zeiten niedriger Systemlast ausführen

4. **Verwendung in Batch-Verarbeitung**

   - Regelmäßige Datensynchronisation als Batch-Job ausführen

Optimierung der Speichernutzung
--------------------

Bei Verarbeitung großer Datenmengen verwenden Sie Streaming-Verarbeitung zur Reduzierung der Speichernutzung.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v1/documents/all"
    params = {"q": "*:*", "num": 100}

    # Mit Streaming verarbeiten
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # Dokumentverarbeitung
                process_document(doc)

Sicherheitsüberlegungen
====================

Zugriffsbeschränkung
------------

Da Scroll-Suche große Datenmengen zurückgibt, konfigurieren Sie angemessene Zugriffsbeschränkungen.

1. **IP-Adressen-Beschränkung**

   Zugriff nur von bestimmten IP-Adressen erlauben

2. **API-Authentifizierung**

   API-Token oder Basic-Authentifizierung verwenden

3. **Rollenbasierte Beschränkung**

   Zugriff nur für Benutzer mit bestimmten Rollen erlauben

Rate-Limiting
----------

Zur Vermeidung übermäßigen Zugriffs wird Konfiguration von Rate-Limiting im Reverse-Proxy empfohlen.

Fehlersuche
======================

Scroll-Suche nicht verfügbar
----------------------------

1. Überprüfen Sie, ob ``api.search.scroll`` auf ``true`` gesetzt ist.
2. Überprüfen Sie, ob |Fess| neu gestartet wurde.
3. Überprüfen Sie Fehlerprotokolle.

Timeout-Fehler tritt auf
----------------------------

1. Erhöhen Sie Wert von ``index.scroll.search.timeout``.
2. Verkleinern Sie ``num``-Parameter für verteilte Verarbeitung.
3. Grenzen Sie Suchbedingungen ein, um abzurufende Datenmenge zu reduzieren.

Speichermangel-Fehler
----------------

1. Verkleinern Sie ``num``-Parameter.
2. Erhöhen Sie Heap-Speichergröße von |Fess|.
3. Überprüfen Sie Heap-Speichergröße von OpenSearch.

Response ist leer
--------------------

1. Überprüfen Sie, ob Suchabfrage korrekt ist.
2. Überprüfen Sie, ob angegebene Labels oder Filterbedingungen korrekt sind.
3. Überprüfen Sie Berechtigungseinstellungen für rollenbasierte Suche.

Referenzinformationen
========

- :doc:`search-basic` - Details zu Suchfunktionen
- :doc:`search-advanced` - Suchbezogene Konfigurationen
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
