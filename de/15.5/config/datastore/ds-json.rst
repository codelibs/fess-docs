==================================
JSON-Konnektor
==================================

Übersicht
=========

Der JSON-Konnektor bietet die Funktionalität, Daten aus JSON-Dateien oder JSON-APIs abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-json`` erforderlich.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Zugriff auf die JSON-Datei oder API ist erforderlich
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

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``files``
     - Ja
     - Pfad zur JSON-Datei (mehrere kommagetrennt)
   * - ``fileEncoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)

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

Array-Elemente verarbeiten:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

Verfügbare Felder
~~~~~~~~~~~~~~~~~

- ``data.<Feldname>`` - Felder des JSON-Objekts
- ``data.<Parent>.<Child>`` - Verschachtelte Objekte
- ``data.<Array>[<Index>]`` - Array-Elemente
- ``data.<Array>.<Methode>`` - Array-Methoden (join, length usw.)

JSON-Format-Details
===================

Einfaches Array
---------------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

Parameter:

::


Verschachtelte Struktur
-----------------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

Parameter:

::


Skript:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

Komplexes Array
---------------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

Parameter:

::


Skript:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

Anwendungsbeispiele
===================

Mehrere JSON-Dateien zusammenführen
-----------------------------------

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

**Symptom**: ``FileNotFoundException`` oder ``404 Not Found``

**Zu überprüfen**:

1. Überprüfen Sie, ob der Dateipfad oder die URL korrekt ist
2. Überprüfen Sie, ob die Datei existiert
3. Bei URLs überprüfen Sie, ob die API verfügbar ist
4. Überprüfen Sie die Netzwerkverbindung

JSON-Parsing-Fehler
-------------------

**Symptom**: ``JsonParseException`` oder ``Unexpected character``

**Zu überprüfen**:

1. Überprüfen Sie, ob die JSON-Datei korrekt formatiert ist:

   ::

       # JSON validieren
       cat data.json | jq .

2. Überprüfen Sie die Zeichenkodierung
3. Überprüfen Sie auf ungültige Zeichen oder Zeilenumbrüche
4. Überprüfen Sie, ob Kommentare enthalten sind (im JSON-Standard sind Kommentare nicht erlaubt)

Keine Daten abrufbar
--------------------

**Symptom**: Crawling erfolgreich, aber 0 Einträge

**Zu überprüfen**:

1. Überprüfen Sie die JSON-Struktur
2. Überprüfen Sie die Skript-Einstellungen
4. Überprüfen Sie die Feldnamen (einschließlich Groß-/Kleinschreibung)
5. Überprüfen Sie die Logs auf Fehlermeldungen

Array-Verarbeitung
------------------

Wenn JSON ein Array ist:

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

Parameter:

::


Wenn JSON ein Objekt mit Array ist:

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

Parameter:

::


Große JSON-Dateien
------------------

**Symptom**: Speicherüberlauf oder Timeout

**Lösung**:

1. Teilen Sie die JSON-Datei in mehrere auf
2. Extrahieren Sie mit JSONPath nur benötigte Teile
3. Bei APIs Paginierung verwenden
4. Erhöhen Sie die Heap-Größe von |Fess|

Erweiterte Skript-Beispiele
===========================

Bedingte Verarbeitung
---------------------

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Arrays kombinieren
------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

Standardwerte setzen
--------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "Ohne Titel"
    content=data.description || data.summary || "Keine Beschreibung"
    price=data.price || 0

Datumsformatierung
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Zahlenverarbeitung
------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-csv` - CSV-Konnektor
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
