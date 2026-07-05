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

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

Mehrere Dateien:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   Die Anführungszeichen- (Quote-) Verarbeitung und die Escape-Verarbeitung sind standardmäßig **deaktiviert**.
   Wenn Sie CSV-Dateien verarbeiten, bei denen Felder in Anführungszeichen eingeschlossen sind und Trennzeichen oder
   Zeilenumbrüche enthalten (RFC 4180-konform), geben Sie explizit ``quote_disabled=false`` an, um die
   Anführungszeichenverarbeitung zu aktivieren.
   Weitere Details finden Sie im Abschnitt "Aktivierung der Anführungszeichen- und Escape-Verarbeitung" weiter unten.

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``files``
     - Nein
     - Pfad zur CSV-Datei (lokaler Pfad, mehrere kommagetrennt möglich). Entweder ``files`` oder ``directories`` muss angegeben werden. Werden beide angegeben, hat ``files`` Vorrang. Die angegebenen Dateien müssen die Endung ``.csv`` oder ``.tsv`` haben; Dateien mit anderen Endungen werden übersprungen.
   * - ``directories``
     - Nein
     - Pfad zu Verzeichnissen, die CSV-Dateien enthalten (mehrere kommagetrennt möglich). Es werden nur ``.csv``- und ``.tsv``-Dateien im Verzeichnis verarbeitet. Wird verwendet, wenn ``files`` nicht angegeben ist.
   * - ``file_encoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)
   * - ``has_header_line``
     - Nein
     - Vorhandensein einer Kopfzeile (Standard: false)
   * - ``separator_character``
     - Nein
     - Trennzeichen (Standard: Komma ``,``). Escape-Sequenzen wie ``\t`` können angegeben werden (für Tab-Trennung).
   * - ``quote_character``
     - Nein
     - Anführungszeichen (Standard: doppeltes Anführungszeichen ``"``). Die Anführungszeichenverarbeitung ist jedoch standardmäßig deaktiviert (siehe ``quote_disabled``).
   * - ``escape_character``
     - Nein
     - Escape-Zeichen (Standard: Backslash ``\``). Die Escape-Verarbeitung ist jedoch standardmäßig deaktiviert (siehe ``escape_disabled``).

.. note::

   Wenn sowohl ``files`` als auch ``directories`` leer sind, tritt ein Fehler (``DataStoreException``) auf.
   Geben Sie mindestens einen der beiden Parameter an.

Erweiterte Parameter
~~~~~~~~~~~~~~~~~~~~

Die folgenden Parameter steuern das CSV-Parsing-Verhalten im Detail:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Beschreibung
   * - ``quote_disabled``
     - Gibt an, ob die Anführungszeichenverarbeitung deaktiviert ist (Standard: true). Geben Sie ``false`` an, um RFC 4180-konforme Felder mit Anführungszeichen zu verarbeiten.
   * - ``escape_disabled``
     - Gibt an, ob die Escape-Verarbeitung deaktiviert ist (Standard: true). Geben Sie ``false`` an, um das Escaping mit ``escape_character`` zu aktivieren.
   * - ``skip_lines``
     - Anzahl der zu überspringenden Kopfzeilen (Standard: 0)
   * - ``ignore_line_patterns``
     - Reguläres Ausdrucksmuster für zu ignorierende Zeilen (z. B. ``^#.*`` zum Ignorieren von Kommentarzeilen)
   * - ``ignore_empty_lines``
     - Gibt an, ob leere Zeilen ignoriert werden sollen (Standard: false)
   * - ``ignore_trailing_whitespaces``
     - Gibt an, ob nachgestellte Leerzeichen ignoriert werden sollen (Standard: false)
   * - ``ignore_leading_whitespaces``
     - Gibt an, ob führende Leerzeichen ignoriert werden sollen (Standard: false)
   * - ``null_string``
     - Zeichenkette, die als Null-Wert behandelt wird
   * - ``break_string``
     - Zeichenkette, durch die Zeilenumbrüche in Feldwerten ersetzt werden
   * - ``readInterval``
     - Wartezeit in Millisekunden zwischen der Verarbeitung einzelner Datensätze (Standard: 0)

Skript-Einstellungen
--------------------

Die Werte der einzelnen Felder werden unter Bezugnahme auf die Spaltenwerte der CSV-Datei zusammengestellt.
Auf die Spalten der CSV-Datei kann im Skript direkt als **Variablen ohne Präfix** zugegriffen werden
(es wird kein Präfix wie ``data.`` verwendet).

Mit Kopfzeile (Referenz über Spaltenname):

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

Ohne Kopfzeile (Referenz über Spaltenindex):

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

Verfügbare Felder
~~~~~~~~~~~~~~~~~

- ``<Spaltenname>`` - Direkter Zugriff über den Spaltennamen der Kopfzeile (nur bei ``has_header_line=true``; gültig, wenn der Spaltenname nicht leer ist)
- ``cell<N>`` - Zugriff über den Spaltenindex (``cell1``, ``cell2`` ... beginnend bei 1; unabhängig vom Vorhandensein einer Kopfzeile verfügbar)
- ``csvfile`` - Vollständiger Pfad der aktuell verarbeiteten CSV-Datei
- ``csvfilename`` - Dateiname der aktuell verarbeiteten CSV-Datei

.. note::

   Enthält ein Spaltenname Leerzeichen, Bindestriche oder andere Zeichen, die als Groovy-Bezeichner ungültig sind,
   kann nicht über den Spaltennamen zugegriffen werden. Verwenden Sie in diesem Fall ``cell<N>``.

CSV-Format-Details
==================

Standard-CSV (RFC 4180-konform)
-------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

.. note::

   Um wie im obigen Beispiel bei ``"Book, Programming"`` Trennzeichen innerhalb eines Feldes durch
   Einschließen in Anführungszeichen zu verwenden, muss die Anführungszeichenverarbeitung mit
   ``quote_disabled=false`` aktiviert werden.
   Ist die Anführungszeichenverarbeitung deaktiviert (Standard), werden Anführungszeichen als
   normale Zeichen behandelt und Felder am Trennzeichen aufgeteilt.

Aktivierung der Anführungszeichen- und Escape-Verarbeitung
-----------------------------------------------------------

Die Anführungszeichen- und Escape-Verarbeitung ist standardmäßig deaktiviert. Aktivieren Sie sie wie folgt explizit.

Anführungszeichenverarbeitung aktivieren:

::

    # Parameter
    quote_disabled=false
    quote_character="

Escape-Verarbeitung aktivieren:

::

    # Parameter
    escape_disabled=false
    escape_character=\

Trennzeichen ändern
-------------------

Tab-getrennt (TSV):

::

    # Parameter
    separator_character=\t

Semikolon-getrennt:

::

    # Parameter
    separator_character=;

Benutzerdefinierte Anführungszeichen
-------------------------------------

Einfache Anführungszeichen (Anführungszeichenverarbeitung muss aktiviert sein):

::

    # Parameter
    quote_disabled=false
    quote_character='

Zeichenkodierung
----------------

Japanische Datei (Shift_JIS):

::

    file_encoding=Shift_JIS

Japanische Datei (EUC-JP):

::

    file_encoding=EUC-JP

Anwendungsbeispiele
===================

Produktkatalog-CSV
------------------

CSV-Datei (products.csv):

::

    product_id,name,description,price,category,in_stock
    1001,Laptop,Hochleistungs-Notebook,120000,Computer,true
    1002,Maus,Kabellose Maus,2500,Peripherie,true
    1003,Tastatur,Mechanische Tastatur,8500,Peripherie,false

Parameter:

::

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Skript:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Kategorie: " + category + " Preis: " + price + " EUR"
    digest=category
    price=price

Filterung nach Lagerbestand:

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

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

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Skript:

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="Abteilung: " + department + "\nPosition: " + position + "\nE-Mail: " + email + "\nTelefon: " + phone
    digest=department

CSV ohne Kopfzeile
------------------

CSV-Datei (data.csv):

::

    1,Produkt A,Dies ist Produkt A,1000
    2,Produkt B,Dies ist Produkt B,2000
    3,Produkt C,Dies ist Produkt C,3000

Parameter:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,

Skript:

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

Mehrere CSV-Dateien zusammenführen
----------------------------------

Parameter:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Skript:

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

Tab-getrennte Datei (TSV)
--------------------------

TSV-Datei (data.tsv):

::

    id	title	content	category
    1	Artikel 1	Dies ist der Inhalt von Artikel 1	Nachrichten
    2	Artikel 2	Dies ist der Inhalt von Artikel 2	Blog

Parameter:

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t

Skript:

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

Fehlerbehebung
==============

Datei nicht gefunden
--------------------

**Symptom**: Das Crawling wird ausgeführt, aber die Datei wird nicht verarbeitet; im Log erscheint ``is not found``

**Zu überprüfen**:

1. Überprüfen Sie, ob der Dateipfad korrekt ist (absoluter Pfad empfohlen)
2. Überprüfen Sie, ob die Datei existiert
3. Überprüfen Sie, ob die Dateiendung ``.csv`` oder ``.tsv`` ist (Dateien mit anderen Endungen werden übersprungen)
4. Überprüfen Sie die Leseberechtigungen der Datei
5. Überprüfen Sie, ob der |Fess|-Ausführungsbenutzer Zugriff hat

Zeichenkodierungsprobleme
--------------------------

**Symptom**: Umlaute oder Sonderzeichen werden nicht korrekt angezeigt

**Lösung**:

Geben Sie die richtige Zeichenkodierung an:

::

    # UTF-8
    file_encoding=UTF-8

    # Shift_JIS
    file_encoding=Shift_JIS

    # EUC-JP
    file_encoding=EUC-JP

    # Windows-Standard (CP932)
    file_encoding=Windows-31J

Zeichenkodierung der Datei ermitteln:

::

    file -i data.csv
    # oder
    nkf -g data.csv

Spalten werden nicht korrekt erkannt
-------------------------------------

**Symptom**: Das Spaltentrennzeichen wird nicht korrekt erkannt, oder in Anführungszeichen eingeschlossene Felder werden aufgeteilt

**Zu überprüfen**:

1. Überprüfen Sie, ob das Trennzeichen korrekt ist:

   ::

       # Komma
       separator_character=,

       # Tab
       separator_character=\t

       # Semikolon
       separator_character=;

2. Wenn Felder mit Anführungszeichen verarbeitet werden sollen (Felder, die Trennzeichen enthalten), aktivieren Sie die Anführungszeichenverarbeitung:

   ::

       quote_disabled=false

3. Überprüfen Sie das CSV-Dateiformat (RFC 4180-konform?)

Kopfzeilen-Behandlung
---------------------

**Symptom**: Erste Zeile wird als Daten erkannt

**Lösung**:

Bei vorhandener Kopfzeile:

::

    has_header_line=true

Ohne Kopfzeile:

::

    has_header_line=false

Keine Daten abrufbar
--------------------

**Symptom**: Crawling erfolgreich, aber 0 Einträge

**Zu überprüfen**:

1. Überprüfen Sie, ob die CSV-Datei nicht leer ist
2. Überprüfen Sie die Skript-Einstellungen (ob Spaltenname- oder ``cell<N>``-Referenzen ohne ``data.``-Präfix angegeben sind)
3. Überprüfen Sie die Spaltennamen (bei has_header_line=true)
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
---------------------------

Im RFC 4180-Format können Felder durch Einschließen in Anführungszeichen Zeilenumbrüche enthalten.
Da die Anführungszeichenverarbeitung standardmäßig deaktiviert ist, muss ``quote_disabled=false`` angegeben werden:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Parameter:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_disabled=false
    quote_character="

CsvListDataStore
================

Das Plugin ``fess-ds-csv`` enthält neben ``CsvDataStore`` auch den Handler ``CsvListDataStore``.

``CsvListDataStore`` erweitert ``CsvDataStore`` und bietet folgende zusätzliche Funktionen:

- Multithread-Verarbeitung (gesteuert über den Parameter ``numOfThreads``)
- Automatisches Löschen verarbeiteter CSV-Dateien
- Zeitstempelbasierte Dateifilterung (überspringt Dateien, die noch beschrieben werden)

Alle Parameter und Skript-Einstellungen von ``CsvDataStore`` können unverändert verwendet werden.

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Handler-Name
     - CsvListDataStore

Zusätzliche Parameter
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``timestamp_margin``
     - Nein
     - Vergangene Zeit seit der letzten Änderungszeit der Datei in Millisekunden. Dateien, bei denen diese Zeit noch nicht verstrichen ist, werden als noch im Schreibvorgang befindlich betrachtet und übersprungen (Standard: 10000)
   * - ``numOfThreads``
     - Nein
     - Anzahl der Verarbeitungs-Threads (Standard: 1)

.. note::

   ``CsvListDataStore`` löscht CSV-Dateien nach der Verarbeitung automatisch. Tritt während der Verarbeitung ein Fehler auf, wird die Datei in ``.txt`` umbenannt (schlägt die Umbenennung fehl, wird die Datei gelöscht).

Erweiterte Skript-Beispiele
============================

Datenverarbeitung
-----------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

Bedingte Indizierung
--------------------

::

    // Nur Produkte mit einem Preis von 10000 oder mehr indizieren
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

Mehrere Spalten kombinieren
---------------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\nSpezifikationen:\n" + specs + "\n\nHinweise:\n" + notes
    category=category

Datumsformatierung
------------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // Bei Bedarf zusätzliche Datumsformatkonvertierung

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-json` - JSON-Konnektor
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `RFC 4180 - CSV-Format <https://datatracker.ietf.org/doc/html/rfc4180>`_
