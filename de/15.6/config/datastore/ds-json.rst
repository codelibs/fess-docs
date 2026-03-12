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

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

HTTP-Datei:

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

REST-API (mit Authentifizierung):

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

Mehrere Dateien:

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``file_path``
     - Ja
     - Pfad zur JSON-Datei oder API-URL (mehrere kommagetrennt)
   * - ``encoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)
   * - ``json_path``
     - Nein
     - JSONPath für Datenextraktion (Standard: ``$``)
   * - ``http_method``
     - Nein
     - HTTP-Methode (GET, POST usw., Standard: GET)
   * - ``auth_type``
     - Nein
     - Authentifizierungstyp (bearer, basic)
   * - ``auth_token``
     - Nein
     - Authentifizierungstoken (bei Bearer-Authentifizierung)
   * - ``auth_username``
     - Nein
     - Authentifizierungs-Benutzername (bei Basic-Authentifizierung)
   * - ``auth_password``
     - Nein
     - Authentifizierungs-Passwort (bei Basic-Authentifizierung)
   * - ``http_headers``
     - Nein
     - Benutzerdefinierte HTTP-Header (JSON-Format)

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

    json_path=$

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

    json_path=$.data.products

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

    json_path=$.articles

Skript:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

JSONPath verwenden
==================

Was ist JSONPath
----------------

JSONPath ist eine Abfragesprache zur Angabe von Elementen innerhalb von JSON.
Es entspricht XPath für XML.

Grundlegende Syntax
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Syntax
     - Beschreibung
   * - ``$``
     - Wurzelelement
   * - ``$.field``
     - Feld auf oberster Ebene
   * - ``$.parent.child``
     - Verschachteltes Feld
   * - ``$.array[0]``
     - Erstes Element des Arrays
   * - ``$.array[*]``
     - Alle Elemente des Arrays
   * - ``$..field``
     - Rekursive Suche

JSONPath-Beispiele
------------------

Alle Elemente (Wurzel):

::

    json_path=$

Bestimmtes Array:

::

    json_path=$.data.items

Verschachteltes Array:

::

    json_path=$.response.results.products

Rekursive Suche:

::

    json_path=$..products

Anwendungsbeispiele
===================

Produktkatalog-API
------------------

API-Antwort:

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "Notebook PC",
            "description": "Hochleistungs-Notebook",
            "price": 1200,
            "category": "Computer",
            "in_stock": true
          }
        ]
      }
    }

Parameter:

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

Skript:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Preis: " + data.price + " EUR"
    digest=data.category
    price=data.price

Blog-Artikel-API
----------------

API-Antwort:

::

    {
      "posts": [
        {
          "id": 1,
          "title": "Artikeltitel",
          "body": "Artikelinhalt...",
          "author": {
            "name": "Max Mustermann",
            "email": "mustermann@example.com"
          },
          "tags": ["Technik", "Programmierung"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

Parameter:

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

Skript:

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

API mit Bearer-Authentifizierung
--------------------------------

Parameter:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Skript:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

API mit Basic-Authentifizierung
-------------------------------

Parameter:

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

Skript:

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

Benutzerdefinierte Header verwenden
-----------------------------------

Parameter:

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

Skript:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Mehrere JSON-Dateien zusammenführen
-----------------------------------

Parameter:

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

Skript:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

POST-Anfrage
------------

Parameter:

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

Skript:

::

    url="https://example.com/result/" + data.id
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

JSONPath-Fehler
---------------

**Symptom**: Keine Daten abrufbar oder leeres Ergebnis

**Zu überprüfen**:

1. Überprüfen Sie die JSONPath-Syntax
2. Überprüfen Sie, ob das Zielelement existiert
3. Validieren Sie JSONPath mit einem Test-Tool:

   ::

       # Überprüfung mit jq
       cat data.json | jq '$.data.products'

4. Überprüfen Sie, ob der Pfad auf die richtige Hierarchie zeigt

Authentifizierungsfehler
------------------------

**Symptom**: ``401 Unauthorized`` oder ``403 Forbidden``

**Zu überprüfen**:

1. Überprüfen Sie, ob der Authentifizierungstyp korrekt ist (bearer, basic)
2. Überprüfen Sie das Authentifizierungstoken oder Benutzername/Passwort
3. Überprüfen Sie das Ablaufdatum des Tokens
4. Überprüfen Sie die Berechtigungseinstellungen der API

Keine Daten abrufbar
--------------------

**Symptom**: Crawling erfolgreich, aber 0 Einträge

**Zu überprüfen**:

1. Überprüfen Sie, ob JSONPath auf die richtigen Elemente zeigt
2. Überprüfen Sie die JSON-Struktur
3. Überprüfen Sie die Skript-Einstellungen
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

    json_path=$

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

    json_path=$.items

Große JSON-Dateien
------------------

**Symptom**: Speicherüberlauf oder Timeout

**Lösung**:

1. Teilen Sie die JSON-Datei in mehrere auf
2. Extrahieren Sie mit JSONPath nur benötigte Teile
3. Bei APIs Paginierung verwenden
4. Erhöhen Sie die Heap-Größe von |Fess|

API-Ratenbegrenzung
-------------------

**Symptom**: ``429 Too Many Requests``

**Lösung**:

1. Verlängern Sie das Crawl-Intervall
2. Überprüfen Sie die Ratenbegrenzung der API
3. Verwenden Sie mehrere API-Schlüssel zur Lastverteilung

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
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
