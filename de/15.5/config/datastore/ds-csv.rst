==================================
CSV-Konnektor
==================================

Übersicht
=========

Der CSV-Konnektor bietet die Funktionalität, Daten aus CSV-Dateien abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-csv`` erforderlich.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Zugriff auf die CSV-Datei ist erforderlich
3. Die Zeichenkodierung der CSV-Datei muss bekannt sein

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # Platzieren
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products CSV
   * - Handler-Name
     - CsvDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Lokale Datei:

::

    file_path=/path/to/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

HTTP-Datei:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Mehrere Dateien:

::

    file_path=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

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
     - Pfad zur CSV-Datei (lokal, HTTP, mehrere kommagetrennt)
   * - ``encoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)
   * - ``has_header``
     - Nein
     - Vorhandensein einer Kopfzeile (Standard: true)
   * - ``separator``
     - Nein
     - Trennzeichen (Standard: Komma ``,``)
   * - ``quote``
     - Nein
     - Anführungszeichen (Standard: Doppeltes Anführungszeichen ``"``)

Skript-Einstellungen
--------------------

Mit Kopfzeile:

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

Ohne Kopfzeile (Spaltenindex):

::

    url="https://example.com/product/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Verfügbare Felder
~~~~~~~~~~~~~~~~~

- ``data.<Spaltenname>`` - Spaltenname der Kopfzeile (bei has_header=true)
- ``data.col<N>`` - Spaltenindex (bei has_header=false, beginnend bei 0)

CSV-Format-Details
==================

Standard-CSV (RFC 4180-konform)
-------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

Trennzeichen ändern
-------------------

Tab-getrennt (TSV):

::

    # Parameter
    separator=\t

Semikolon-getrennt:

::

    # Parameter
    separator=;

Benutzerdefinierte Anführungszeichen
------------------------------------

Einfache Anführungszeichen:

::

    # Parameter
    quote='

Zeichenkodierung
----------------

Japanische Datei (Shift_JIS):

::

    encoding=Shift_JIS

Deutsche Datei (ISO-8859-1):

::

    encoding=ISO-8859-1

Anwendungsbeispiele
===================

Produktkatalog-CSV
------------------

CSV-Datei (products.csv):

::

    product_id,name,description,price,category,in_stock
    1001,Notebook PC,Hochleistungs-Notebook,1200,Computer,true
    1002,Maus,Kabellose Maus,25,Peripherie,true
    1003,Tastatur,Mechanische Tastatur,85,Peripherie,false

Parameter:

::

    file_path=/var/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Skript:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Kategorie: " + data.category + " Preis: " + data.price + " EUR"
    digest=data.category
    price=data.price

Filterung nach Lagerbestand:

::

    if (data.in_stock == "true") {
        url="https://shop.example.com/product/" + data.product_id
        title=data.name
        content=data.description
        price=data.price
    }

Mitarbeiterverzeichnis-CSV
--------------------------

CSV-Datei (employees.csv):

::

    emp_id,name,department,email,phone,position
    E001,Max Mustermann,Vertrieb,mustermann@example.com,030-1234-5678,Abteilungsleiter
    E002,Erika Musterfrau,Entwicklung,musterfrau@example.com,030-2345-6789,Manager
    E003,Hans Schmidt,Verwaltung,schmidt@example.com,030-3456-7890,Sachbearbeiter

Parameter:

::

    file_path=/var/data/employees.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Skript:

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="Abteilung: " + data.department + "\nPosition: " + data.position + "\nE-Mail: " + data.email + "\nTelefon: " + data.phone
    digest=data.department

CSV ohne Kopfzeile
------------------

CSV-Datei (data.csv):

::

    1,Produkt A,Dies ist Produkt A,1000
    2,Produkt B,Dies ist Produkt B,2000
    3,Produkt C,Dies ist Produkt C,3000

Parameter:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=false
    separator=,
    quote="

Skript:

::

    url="https://example.com/item/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Mehrere CSV-Dateien zusammenführen
----------------------------------

Parameter:

::

    file_path=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Skript:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

CSV über HTTP abrufen
---------------------

Parameter:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Skript:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description

Tab-getrennte Datei (TSV)
-------------------------

TSV-Datei (data.tsv):

::

    id	title	content	category
    1	Artikel 1	Dies ist der Inhalt von Artikel 1	Nachrichten
    2	Artikel 2	Dies ist der Inhalt von Artikel 2	Blog

Parameter:

::

    file_path=/var/data/data.tsv
    encoding=UTF-8
    has_header=true
    separator=\t
    quote="

Skript:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

Fehlerbehebung
==============

Datei nicht gefunden
--------------------

**Symptom**: ``FileNotFoundException`` oder ``No such file``

**Zu überprüfen**:

1. Überprüfen Sie, ob der Dateipfad korrekt ist (absoluter Pfad empfohlen)
2. Überprüfen Sie, ob die Datei existiert
3. Überprüfen Sie die Leseberechtigungen der Datei
4. Überprüfen Sie, ob der |Fess|-Ausführungsbenutzer Zugriff hat

Zeichenkodierungsprobleme
-------------------------

**Symptom**: Umlaute oder Sonderzeichen werden nicht korrekt angezeigt

**Lösung**:

Geben Sie die richtige Zeichenkodierung an:

::

    # UTF-8
    encoding=UTF-8

    # ISO-8859-1 (Westeuropäisch)
    encoding=ISO-8859-1

    # Windows-1252
    encoding=Windows-1252

Zeichenkodierung der Datei ermitteln:

::

    file -i data.csv

Spalten werden nicht korrekt erkannt
------------------------------------

**Symptom**: Spaltentrennzeichen wird nicht korrekt erkannt

**Zu überprüfen**:

1. Überprüfen Sie, ob das Trennzeichen korrekt ist:

   ::

       # Komma
       separator=,

       # Tab
       separator=\t

       # Semikolon
       separator=;

2. Überprüfen Sie die Anführungszeichen-Einstellung
3. Überprüfen Sie das CSV-Dateiformat (RFC 4180-konform?)

Kopfzeilen-Behandlung
---------------------

**Symptom**: Erste Zeile wird als Daten erkannt

**Lösung**:

Bei vorhandener Kopfzeile:

::

    has_header=true

Ohne Kopfzeile:

::

    has_header=false

Keine Daten abrufbar
--------------------

**Symptom**: Crawling erfolgreich, aber 0 Einträge

**Zu überprüfen**:

1. Überprüfen Sie, ob die CSV-Datei nicht leer ist
2. Überprüfen Sie die Skript-Einstellungen
3. Überprüfen Sie die Spaltennamen (bei has_header=true)
4. Überprüfen Sie die Logs auf Fehlermeldungen

Große CSV-Dateien
-----------------

**Symptom**: Speicherüberlauf oder Timeout

**Lösung**:

1. Teilen Sie die CSV-Datei in mehrere auf
2. Verwenden Sie nur benötigte Spalten im Skript
3. Erhöhen Sie die Heap-Größe von |Fess|
4. Filtern Sie nicht benötigte Zeilen

Felder mit Zeilenumbrüchen
--------------------------

Im RFC 4180-Format können Felder mit Anführungszeichen umschlossen Zeilenumbrüche enthalten:

::

    id,title,description
    1,"Produkt A","Dies ist
    eine mehrzeilige
    Beschreibung"
    2,"Produkt B","Einzeilige Beschreibung"

Parameter:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Erweiterte Skript-Beispiele
===========================

Datenverarbeitung
-----------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseInt(data.price)
    category=data.category.toLowerCase()

Bedingte Indizierung
--------------------

::

    # Nur Produkte mit Preis über 10000
    if (parseInt(data.price) >= 10000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Mehrere Spalten kombinieren
---------------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\nSpezifikationen:\n" + data.specs + "\n\nHinweise:\n" + data.notes
    category=data.category

Datumsformatierung
------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # Bei Bedarf zusätzliche Datumsformatierung

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-json` - JSON-Konnektor
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `RFC 4180 - CSV-Format <https://datatracker.ietf.org/doc/html/rfc4180>`_
