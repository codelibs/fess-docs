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
Zur Aktivierung ändern Sie in ``fess_config.properties`` oder ``/etc/fess/fess_config.properties``
folgende Einstellung:

::

    api.search.scroll=true

.. note::
   Nach Konfigurationsänderung muss |Fess| neu gestartet werden.

Konfiguration von Response-Feldern
--------------------------

Sie können Felder anpassen, die in Suchergebnissen enthalten sind.
Standardmäßig werden nur Grundfelder zurückgegeben, Sie können jedoch zusätzliche Felder angeben.

::

    query.additional.scroll.response.fields=content,mimetype,filename,created,last_modified

Bei Angabe mehrerer Felder trennen Sie diese durch Kommas.

Timeout-Einstellung für Scroll
----------------------------

Sie können die Gültigkeitsdauer des Scroll-Kontexts konfigurieren.
Standard ist 1 Minute.

::

    api.search.scroll.timeout=1m

Einheiten:
- ``s``: Sekunden
- ``m``: Minuten
- ``h``: Stunden

Verwendungsmethode
========

Grundlegende Verwendung
----------------

Zugriff auf Scroll-Suche erfolgt über folgende URL:

::

    http://localhost:8080/json/scroll?q=Suchschlüsselwort

Suchergebnisse werden im NDJSON-Format (Newline Delimited JSON) zurückgegeben.
Pro Zeile wird ein Dokument im JSON-Format ausgegeben.

**Beispiel:**

::

    curl "http://localhost:8080/json/scroll?q=Fess"

Request-Parameter
--------------------

Für Scroll-Suche können folgende Parameter verwendet werden:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Parametername
     - Beschreibung
   * - ``q``
     - Suchabfrage (erforderlich)
   * - ``size``
     - Anzahl pro Scroll-Abruf (Standard: 100)
   * - ``scroll``
     - Gültigkeitszeit des Scroll-Kontexts (Standard: 1m)
   * - ``fields.label``
     - Filterung nach Label

Angabe von Suchabfragen
----------------

Sie können Suchabfragen wie bei normaler Suche angeben.

**Beispiel: Schlüsselwortsuche**

::

    curl "http://localhost:8080/json/scroll?q=Suchmaschine"

**Beispiel: Feldspezifische Suche**

::

    curl "http://localhost:8080/json/scroll?q=title:Fess"

**Beispiel: Vollständiger Abruf (ohne Suchbedingung)**

::

    curl "http://localhost:8080/json/scroll?q=*:*"

Angabe der Abrufanzahl
--------------

Sie können die Anzahl pro Scroll-Abruf ändern.

::

    curl "http://localhost:8080/json/scroll?q=Fess&size=500"

.. note::
   Zu großer ``size``-Parameter erhöht Speichernutzung.
   Normalerweise wird Bereich von 100–1000 empfohlen.

Filterung nach Label
--------------------------

Sie können nur Dokumente bestimmter Labels abrufen.

::

    curl "http://localhost:8080/json/scroll?q=*:*&fields.label=public"

Bei erforderlicher Authentifizierung
----------------

Bei Verwendung rollenbasierter Suche müssen Sie Authentifizierungsinformationen einschließen.

::

    curl -u username:password "http://localhost:8080/json/scroll?q=Fess"

Oder mit API-Token:

::

    curl -H "Authorization: Bearer YOUR_API_TOKEN" \
         "http://localhost:8080/json/scroll?q=Fess"

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

Standardmäßig enthaltene Hauptfelder:

- ``url``: Dokument-URL
- ``title``: Titel
- ``content``: Haupttext (Auszug)
- ``score``: Such-Score
- ``boost``: Boost-Wert
- ``created``: Erstellungsdatum
- ``last_modified``: Letztes Änderungsdatum

Datenverarbeitungsbeispiele
============

Verarbeitungsbeispiel mit Python
----------------

.. code-block:: python

    import requests
    import json

    # Scroll-Suche ausführen
    url = "http://localhost:8080/json/scroll"
    params = {
        "q": "Fess",
        "size": 100
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

    curl "http://localhost:8080/json/scroll?q=*:*" > all_documents.ndjson

Konvertierung zu CSV
-----------

Beispiel für Konvertierung zu CSV mit jq-Befehl:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=Fess" | \
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

1. **Angemessene size-Parameter-Einstellung**

   - Zu klein erhöht Kommunikations-Overhead
   - Zu groß erhöht Speichernutzung
   - Empfohlen: 100–1000

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

    url = "http://localhost:8080/json/scroll"
    params = {"q": "*:*", "size": 100}

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

1. Erhöhen Sie Wert von ``api.search.scroll.timeout``.
2. Verkleinern Sie ``size``-Parameter für verteilte Verarbeitung.
3. Grenzen Sie Suchbedingungen ein, um abzurufende Datenmenge zu reduzieren.

Speichermangel-Fehler
----------------

1. Verkleinern Sie ``size``-Parameter.
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
