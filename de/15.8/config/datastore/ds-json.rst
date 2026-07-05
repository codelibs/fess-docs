==============
JSON-Konnektor
==============

Ubersicht
=========

Der JSON-Konnektor bietet die Funktionalitat, Daten aus lokalen JSONL-Dateien
(JSON-Lines-Format) abzurufen und im |Fess|-Index zu registrieren.

Fur diese Funktion ist das Plugin ``fess-ds-json`` erforderlich.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Lesezugriff auf die JSON-Dateien ist erforderlich
3. Die Struktur der JSON-Daten muss bekannt sein

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

Methode 2: Uber die Administrationsoberflache installieren

1. Offnen Sie "System" -> "Plugins"
2. Laden Sie die JAR-Datei hoch
3. Starten Sie |Fess| neu

Konfiguration
=============

Konfigurieren Sie uber die Administrationsoberflache unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

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
   :widths: 20 10 70

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``files``
     - Nein
     - Pfad zur zu verarbeitenden JSON-Datei (mehrere Angaben moglich: kommagetrennt). Nur Dateien mit der Erweiterung ``.json`` oder ``.jsonl`` werden verarbeitet.
   * - ``directories``
     - Nein
     - Pfad zum Verzeichnis mit JSON-Dateien (mehrere Angaben moglich: kommagetrennt)
   * - ``fileEncoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)

.. warning::
   Es muss entweder ``files`` oder ``directories`` angegeben werden.
   Wenn keiner der beiden Parameter angegeben ist (leer), wird eine ``DataStoreException`` ausgelost.
   Wenn beide angegeben sind, hat ``files`` Vorrang und ``directories`` wird ignoriert.

.. note::
   Der Parametername lautet im camelCase ``fileEncoding`` (nicht ``file_encoding`` in snake_case).

Verhalten bei Verzeichnisangabe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wenn ``directories`` angegeben ist, werden die Dateien direkt im jeweiligen Verzeichnis nach folgenden Regeln verarbeitet:

- **Unterverzeichnisse werden nicht durchsucht** (keine rekursive Suche).
- Nur Dateien mit der Erweiterung ``.json`` oder ``.jsonl`` werden berucksichtigt (Gro-/Kleinschreibung wird nicht unterschieden).
- Die Dateien werden in aufsteigender Reihenfolge nach Anderungsdatum (letzter Anderungszeitpunkt) verarbeitet.

.. note::
   Dieser Konnektor unterstutzt ausschlie?lich JSON-Dateien im lokalen Dateisystem. HTTP-Zugriff und API-Authentifizierung werden nicht unterstutzt.

Skript-Einstellungen
--------------------

Die Werte der einzelnen Felder werden aus den Feldern des jeweiligen JSON-Objekts zusammengesetzt.
Felder auf der obersten Ebene des JSON-Objekts konnen im Skript als **Variablen ohne Prafix**
direkt referenziert werden (kein Prafix wie ``data.``).

Einfaches JSON-Objekt:

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

Verschachteltes JSON-Objekt (verschachtelte Objekte werden als Map referenziert):

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

Verarbeitung von Array-Elementen:

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

Verfugbare Felder
~~~~~~~~~~~~~~~~~

- ``<Feldname>`` - Felder auf der obersten Ebene des JSON-Objekts werden direkt beim Namen referenziert
- ``<Elternteil>.<Kind>`` - Felder eines verschachtelten Objekts
- ``<Array>[<Index>]`` - Array-Element
- ``<Array>.<Methode>`` - Array-Methoden (``join``, ``collect``, ``size`` usw.)

.. note::

   Enthalt ein Feldname Leerzeichen, Bindestriche oder andere Zeichen, die als Groovy-Bezeichner
   ungultig sind, kann dieses Feld nicht direkt als Variablenname referenziert werden.

JSON-Format-Details
===================

JSON-Dateiformat
----------------

Der JSON-Konnektor liest Dateien im JSONL-Format (JSON Lines).
Dabei wird pro Zeile ein JSON-Objekt geschrieben. Die Datei wird zeilenweise eingelesen,
und jede Zeile wird als eigenstandiges JSON-Objekt verarbeitet.

.. note::
   Dateien mit der Erweiterung ``.json`` werden ebenfalls verarbeitet, der Inhalt muss jedoch
   im JSONL-Format vorliegen (ein Objekt pro Zeile).
   JSON-Dateien im Array-Format (``[{...}, {...}]``) oder mehrzeilig formatierte
   (pretty-printed) JSON-Dateien konnen nicht direkt eingelesen werden. Bitte konvertieren Sie
   diese in das JSONL-Format.

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

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Preis: " + price + " Yen"
    digest=category
    price=price

Integration mehrerer JSON-Dateien
----------------------------------

Parameter:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Skript:

::

    url="https://example.com/item/" + id
    title=title
    content=content

Fehlerbehebung
==============

Datei nicht gefunden
--------------------

**Symptom**: Im Protokoll wird ``... is not found.`` oder ``Source file ... does not exist.`` ausgegeben

**Prufpunkte**:

1. Uberprfen Sie, ob der Dateipfad korrekt ist
2. Uberprfen Sie, ob die Datei vorhanden ist
3. Uberprfen Sie, ob die Dateiendung ``.json`` oder ``.jsonl`` ist
4. Uberprfen Sie, ob Leserechte fur die Datei vorhanden sind

JSON-Analysefehler
------------------

**Symptom**: Im Protokoll wird ``Crawling Access Exception`` zusammen mit ``JsonParseException`` o. a. ausgegeben

Enthalt eine Zeile ungultige Daten, wird nur diese Zeile ubersprungen und als fehlgeschlagene URL
erfasst; das Crawling selbst wird ab der nachsten Zeile fortgesetzt.

**Prufpunkte**:

1. Uberprfen Sie, ob die JSON-Datei im korrekten Format vorliegt (JSONL: ein Objekt pro Zeile):

   ::

       # Jede Zeile auf gultige JSON-Objekte prfen
       cat data.json | jq -c .

2. Uberprfen Sie die Zeichenkodierung
3. Uberprfen Sie, ob ein einzelnes Objekt uber mehrere Zeilen verteilt ist
4. Uberprfen Sie, ob Kommentare enthalten sind (Kommentare sind im JSON-Standard nicht erlaubt)

Keine Daten abgerufen
---------------------

**Symptom**: Das Crawling ist erfolgreich, aber die Trefferanzahl betragt 0

**Prufpunkte**:

1. Uberprfen Sie die JSON-Struktur
2. Uberprfen Sie die Skript-Einstellungen (Felder werden ohne ``data.``-Prafix referenziert)
3. Uberprfen Sie die Feldnamen (einschlie?lich Gro-/Kleinschreibung)
4. Uberprfen Sie die Protokolldateien auf Fehlermeldungen

Gro?e JSON-Dateien
------------------

**Symptom**: Speichermangel oder Zeituberschreitung

Da die Datei zeilenweise eingelesen wird, wirkt sich die Gesamtgro?e der Datei nicht direkt auf
den Speicherverbrauch aus. Probleme konnen jedoch auftreten, wenn eine einzelne Zeile
(ein einzelnes Objekt) extrem gro? ist oder die Last beim Indexieren sehr hoch ist.

**Losung**:

1. Teilen Sie die JSON-Datei in mehrere Dateien auf
2. Erhohen Sie die Heap-Gro?e von |Fess|

Erweiterte Skript-Beispiele
============================

Bedingte Verarbeitung
---------------------

Jedes Feld wird als eigenstandiger Ausdruck ausgewertet. Fur bedingte Werte verwenden Sie den
ternaren Operator:

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

Array-Verknupfung
-----------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

Standardwerte festlegen
-----------------------

::

    url="https://example.com/item/" + id
    title=title ?: "Ohne Titel"
    content=description ?: (summary ?: "Keine Beschreibung")
    price=price ?: 0

Datumsformatierung
------------------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

Numerische Verarbeitung
-----------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

Referenzen
==========

- :doc:`ds-overview` - Ubersicht der Datenspeicher-Konnektoren
- :doc:`ds-csv` - CSV-Konnektor
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Datenspeicher-Konfigurationsleitfaden
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
