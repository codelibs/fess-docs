==================================
JSON-Konnektor
==================================

Übersicht
=========

Der JSON-Konnektor bietet die Funktionalität, Daten aus lokalen JSON- oder JSONL-Dateien abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-json`` erforderlich.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Zugriff auf die JSON-Dateien ist erforderlich
3. Die JSON-Struktur muss bekannt sein

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Platzieren
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2: Über die Administrationsoberfläche installieren

1. Öffnen Sie "System" -> "Plugins"
2. Laden Sie die JAR-Datei hoch
3. Starten Sie |Fess| neu

Konfiguration
=============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - Products JSON
   * - Handler-Name
     - JsonDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Lokale Datei:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

Mehrere Dateien:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

Verzeichnisangabe:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``files``
     - Nein
     - Pfad zur JSON-Datei (mehrere kommagetrennt)
   * - ``directories``
     - Nein
     - Pfad zum Verzeichnis mit JSON-Dateien
   * - ``fileEncoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)

.. warning::
   Es muss entweder ``files`` oder ``directories`` angegeben werden.
   Wenn keiner von beiden angegeben ist, wird eine ``DataStoreException`` ausgelöst.
   Wenn beide angegeben sind, hat ``files`` Vorrang und ``directories`` wird ignoriert.

.. note::
   Dieser Konnektor unterstützt ausschließlich JSON-Dateien im lokalen Dateisystem. HTTP-Zugriff oder API-Authentifizierung werden nicht unterstützt.

Skript-Einstellungen
--------------------

Einfaches JSON-Objekt:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

Verschachteltes JSON-Objekt:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

Verarbeitung von Array-Elementen:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

Verfügbare Felder
~~~~~~~~~~~~~~~~~

- ``data.<Feldname>`` - Felder des JSON-Objekts
- ``data.<Eltern>.<Kind>`` - Verschachtelte Objekte
- ``data.<Array>[<Index>]`` - Array-Elemente
- ``data.<Array>.<Methode>`` - Array-Methoden (join, length usw.)

JSON-Format-Details
===================

JSON-Dateiformat
----------------

Der JSON-Konnektor liest Dateien im JSONL-Format (JSON Lines).
Dabei wird pro Zeile ein JSON-Objekt geschrieben.

.. note::
   JSON-Dateien im Array-Format ( ``[{...}, {...}]`` ) können nicht direkt gelesen werden.
   Bitte konvertieren Sie diese in das JSONL-Format.

JSONL-Datei:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

Anwendungsbeispiele
===================

Produktkatalog
--------------

Parameter:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

Skript:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Preis: " + data.price + " EUR"
    digest=data.category
    price=data.price

Integration mehrerer JSON-Dateien
---------------------------------

Parameter:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Skript:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Fehlerbehebung
==============

Datei nicht gefunden
--------------------

**Symptom**: ``FileNotFoundException``

**Prüfpunkte**:

1. Überprüfen Sie, ob der Dateipfad korrekt ist
2. Überprüfen Sie, ob die Datei existiert
3. Überprüfen Sie, ob Leserechte vorhanden sind

JSON-Analysefehler
------------------

**Symptom**: ``JsonParseException`` oder ``Unexpected character``

**Prüfpunkte**:

1. Überprüfen Sie, ob die JSON-Datei im korrekten Format ist:

   ::

       # JSON-Validierung
       cat data.json | jq .

2. Überprüfen Sie die Zeichenkodierung
3. Überprüfen Sie, ob ungültige Zeichen oder Zeilenumbrüche vorhanden sind
4. Überprüfen Sie, ob Kommentare enthalten sind (im JSON-Standard sind Kommentare nicht erlaubt)

Keine Daten abgerufen
---------------------

**Symptom**: Der Crawl ist erfolgreich, aber die Anzahl der Ergebnisse ist 0

**Prüfpunkte**:

1. Überprüfen Sie die JSON-Struktur
2. Überprüfen Sie die Skript-Einstellungen
3. Überprüfen Sie die Feldnamen (einschließlich Groß-/Kleinschreibung)
4. Überprüfen Sie die Protokolldateien auf Fehlermeldungen

Große JSON-Dateien
------------------

**Symptom**: Speichermangel oder Zeitüberschreitung

**Lösung**:

1. Teilen Sie die JSON-Datei in mehrere Dateien auf
2. Erhöhen Sie die Heap-Größe von |Fess|

Erweiterte Skript-Beispiele
============================

Bedingte Verarbeitung
---------------------

Jedes Feld wird als eigenständiger Ausdruck ausgewertet. Für bedingte Werte verwenden Sie den ternären Operator:

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

Array-Verknüpfung
-----------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

Standardwerte festlegen
-----------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "Ohne Titel"
    content=data.description ?: (data.summary ?: "Keine Beschreibung")
    price=data.price ?: 0

Datumsformatierung
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Numerische Verarbeitung
-----------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price as Float
    stock=data.stock_quantity as Integer

Referenzen
==========

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-csv` - CSV-Konnektor
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Datenspeicher-Konfigurationsleitfaden
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
