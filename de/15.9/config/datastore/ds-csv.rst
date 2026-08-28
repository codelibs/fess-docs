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

Mehrere Dateien:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

.. note::

   Die Anführungszeichen- (Quote-) Verarbeitung und die Escape-Verarbeitung sind in |Fess| 15.9
   standardmäßig **aktiviert**. CSV-Dateien (RFC 4180-konform), bei denen Felder in
   Anführungszeichen eingeschlossen sind und Trennzeichen oder Zeilenumbrüche enthalten, werden
   ohne zusätzliche Parameter korrekt verarbeitet.
   Wie Sie zum bisherigen Verhalten (Anführungszeichenverarbeitung deaktivieren) zurückkehren
   und was dabei zu beachten ist, erfahren Sie im Abschnitt "Deaktivierung der Anführungszeichen-
   und Escape-Verarbeitung" weiter unten.

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
     - Anführungszeichen (Standard: doppeltes Anführungszeichen ``"``). Die Anführungszeichenverarbeitung ist standardmäßig aktiviert (siehe ``quote_disabled``).
   * - ``escape_character``
     - Nein
     - Escape-Zeichen (Standard: dasselbe Zeichen wie ``quote_character``; gemäß RFC 4180 werden Anführungszeichen durch Verdopplung escaped). Ob die Escape-Verarbeitung aktiv ist, richtet sich nach dem aufgelösten Wert von ``quote_disabled`` (siehe ``escape_disabled``).

.. note::

   Wenn sowohl ``files`` als auch ``directories`` leer sind, tritt ein Fehler (``DataStoreException``) auf.
   Geben Sie mindestens einen der beiden Parameter an.

Erweiterte Parameter
~~~~~~~~~~~~~~~~~~~~

Die folgenden Parameter steuern das CSV-Parsing-Verhalten sowie das Indexierungsverhalten im Detail:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Beschreibung
   * - ``quote_disabled``
     - Gibt an, ob die Anführungszeichenverarbeitung deaktiviert ist (Standard: false). RFC 4180-konforme Felder mit Anführungszeichen werden standardmäßig korrekt verarbeitet. Geben Sie ``true`` an, um zum bisherigen Verhalten (Anführungszeichen als normale Zeichen) zurückzukehren.
   * - ``escape_disabled``
     - Gibt an, ob die Escape-Verarbeitung deaktiviert ist (Standard: identisch mit dem aufgelösten Wert von ``quote_disabled``). Ein explizit angegebener Wert hat Vorrang.
   * - ``delete_old_docs``
     - Gibt an, ob nach Abschluss des Crawlings Dokumente gelöscht werden, die zu dieser Datenspeicher-Konfiguration gehören und in der aktuellen Crawling-Sitzung nicht erneut registriert wurden (Standard: true). Wenn Sie mehrere CSV-Dateien zu unterschiedlichen Zeitpunkten in dieselbe Datenspeicher-Konfiguration einspeisen, geben Sie ``false`` an -- sonst werden die zuvor eingespeisten Dokumente gelöscht (Details siehe Abschnitt zur Fehlerbehebung weiter unten).
   * - ``keep_expires_docs``
     - Gibt an, ob beim Löschen über ``delete_old_docs`` Dokumente ausgenommen werden, deren Ablaufzeitpunkt ("expires", z. B. über ``time_to_live`` gesetzt) noch nicht erreicht ist (Standard: true). Bei ``false`` werden nicht erneut registrierte Dokumente auch innerhalb ihrer Ablaufzeit gelöscht.
   * - ``time_to_live``
     - Nach wie vielen Minuten ab dem Registrierungszeitpunkt der Ablaufzeitpunkt eines Dokuments gesetzt wird (in Minuten; Standard: nicht gesetzt, d. h. unbegrenzt).
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

   Enthält ein Spaltenname Leerzeichen, Bindestriche oder andere Zeichen, die als Skript-Bezeichner ungültig sind,
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
   Einschließen in Anführungszeichen zu verwenden, wird das Feld mit den Standardeinstellungen
   (Anführungszeichenverarbeitung aktiviert) bereits korrekt als ein einziges Feld verarbeitet.
   Wie Sie zum bisherigen Verhalten (Anführungszeichen als normale Zeichen, Aufteilung der Felder
   am Trennzeichen) zurückkehren, erfahren Sie im Abschnitt "Deaktivierung der Anführungszeichen-
   und Escape-Verarbeitung" weiter unten.

Deaktivierung der Anführungszeichen- und Escape-Verarbeitung
-------------------------------------------------------------

Die Anführungszeichen- und Escape-Verarbeitung ist in |Fess| 15.9 standardmäßig aktiviert.
Als Anführungszeichen wird standardmäßig das doppelte Anführungszeichen ``"`` verwendet, als
Escape-Zeichen standardmäßig dasselbe Zeichen wie das Anführungszeichen (gemäß RFC 4180 durch
Verdopplung escaped); Standard-RFC-4180-CSV-Dateien lassen sich so ohne zusätzliche Parameter
verarbeiten.

.. warning::

   Enthält eine CSV-Datei bei aktivierter Anführungszeichenverarbeitung auch nur ein einziges
   ``"`` ohne passendes schließendes Anführungszeichen, wird der gesamte Rest der Datei ab diesem
   Anführungszeichen (einschließlich der folgenden Zeilen) als ein einziger Feldwert eingelesen,
   und für die übrigen Zeilen werden keine Dokumente mehr erzeugt. Da frühere Versionen jede Zeile
   unabhängig verarbeitet haben, kann dieses Verhalten erst nach einem Upgrade zutage treten.
   Da ``delete_old_docs`` (siehe oben) standardmäßig aktiviert ist, können dabei nicht nur die
   nicht erzeugten Dokumente, sondern auch bereits durch ein früheres Crawling registrierte
   Dokumente gelöscht werden.
   Prüfen Sie Ihre CSV-Dateien vor dem Upgrade auf nicht geschlossene Anführungszeichen, oder
   erwägen Sie, mit ``quote_disabled=true`` zur bisherigen Verarbeitungsweise zurückzukehren.

Anführungszeichenverarbeitung deaktivieren (bisheriges Verhalten wiederherstellen):

::

    # Parameter
    quote_disabled=true

Mit ``quote_disabled=true`` wird gleichzeitig auch die Escape-Verarbeitung deaktiviert (außer Sie
geben explizit ``escape_disabled=false`` an).

Nur die Escape-Verarbeitung deaktivieren:

::

    # Parameter
    escape_disabled=true

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

Einfache Anführungszeichen:

::

    # Parameter
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

2. Felder mit Anführungszeichen (Felder, die Trennzeichen enthalten) werden standardmäßig korrekt
   verarbeitet. Prüfen Sie, ob Sie nicht versehentlich ``quote_disabled=true`` gesetzt haben.
3. Überprüfen Sie das CSV-Dateiformat (RFC 4180-konform?). Enthält die Datei ein ``"`` ohne
   passendes schließendes Anführungszeichen, wird der gesamte Rest der Datei ab dieser Stelle als
   ein einziger Feldwert eingelesen.

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
5. Prüfen Sie, ob ein Parametername falsch geschrieben ist (ein nicht erkannter
   Parametername wird ohne Warnung ignoriert; ``has_headerline=true`` belässt
   ``has_header_line`` beispielsweise beim Standardwert ``false``)

Der Index aus einem vorherigen Crawling verschwindet nach einem zweiten CSV-Import
----------------------------------------------------------------------------------

**Symptom**: Nachdem eine erste CSV-Datei gecrawlt wurde, verschwinden nach dem Crawling einer
zweiten CSV-Datei mit derselben Datenspeicher-Konfiguration an einem späteren Tag die aus der
ersten CSV-Datei registrierten Dokumente aus den Suchergebnissen.

**Ursache**:

Nach Abschluss eines Crawlings löscht |Fess| aus dem Index alle Dokumente, die zu dieser
Datenspeicher-Konfiguration gehören und in der aktuellen Sitzung nicht erneut registriert wurden
(``delete_old_docs``, Standard: true). Wenn Sie mehrere CSV-Dateien zu unterschiedlichen
Zeitpunkten in dieselbe Datenspeicher-Konfiguration einspeisen, gelten beim Crawling der später
eingespeisten Datei die durch die frühere Datei registrierten Inhalte als "in der aktuellen
Sitzung nicht erneut registriert" und werden gelöscht.

**Lösung**:

Wenn Sie mehrere CSV-Dateien zu unterschiedlichen Zeitpunkten in dieselbe Datenspeicher-Konfiguration
einspeisen und deren Inhalte kumulieren möchten, geben Sie Folgendes an.

::

    delete_old_docs=false

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
Da die Anführungszeichenverarbeitung standardmäßig aktiviert ist, wird dies ohne zusätzliche Parameter korrekt verarbeitet:

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
   * - ``delete_processed_file``
     - Nein
     - Gibt an, ob die CSV-Datei nach Abschluss der Verarbeitung gelöscht wird (Standard: true)
   * - ``ignore_data_store_exception``
     - Nein
     - Gibt an, ob das gesamte Crawling fortgesetzt wird, wenn bei der Verarbeitung einer einzelnen CSV-Datei eine Ausnahme auftritt (Standard: true)

.. warning::

   ``CsvListDataStore`` **löscht** CSV-Dateien nach Abschluss der Verarbeitung automatisch (``delete_processed_file`` ist standardmäßig ``true``). Tritt während der Verarbeitung ein Fehler auf, wird die Datei stattdessen in ``.txt`` umbenannt (schlägt die Umbenennung fehl, wird die Datei gelöscht). Wenn Dateien nicht gelöscht werden sollen, geben Sie ``delete_processed_file=false`` an.

CSV-Zeilenformat (Ereignistyp)
-----------------------------------

CSV-Dateien, die an ``CsvListDataStore`` übergeben werden, benötigen pro Zeile mindestens zwei
Spalten: einen "Ereignistyp" und eine "URL". Weitere Spalten können hinzugefügt und als
``cell3``, ``cell4`` ... referenziert werden (z. B. um einen Wert an ``timestamp.overwrite`` zu übergeben).

::

    <Ereignistyp>,<URL>

Für den Ereignistyp stehen die folgenden drei Werte zur Verfügung.

- ``create`` - eine Datei wurde erstellt
- ``modify`` - eine Datei wurde geändert
- ``delete`` - eine Datei wurde gelöscht

``create`` und ``modify`` werden als derselbe Vorgang behandelt (Crawling und Indexierung der
Ziel-URL). Es gibt keinen Unterschied im Verhalten.

Der Spaltenname (bei vorhandener Kopfzeile) und der Wert für jeden Ereignistyp lassen sich über
die folgenden Parameter anpassen.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Beschreibung
   * - ``field.event_type``
     - Spaltenname, in dem der Ereignistyp gespeichert ist (Standard: ``event_type``)
   * - ``event.create``
     - Wert für "erstellt" (Standard: ``create``)
   * - ``event.modify``
     - Wert für "geändert" (Standard: ``modify``)
   * - ``event.delete``
     - Wert für "gelöscht" (Standard: ``delete``)

Beispiel für eine CSV-Datei:

::

    modify,smb://servername/data/testfile1.txt
    delete,smb://servername/data/testfile2.txt

Beispiel-Skript (ohne Kopfzeile):

::

    event_type=cell1
    url=cell2

Überschreiben von Feldwerten (.overwrite)
-------------------------------------------

Wird der Name eines im Skript zusammengestellten Indexfelds mit ``.overwrite`` versehen, wird der
Wert dieses Feldes nicht aus dem tatsächlichen Crawling-Ergebnis der Datei, sondern aus dem in der
CSV gesetzten Wert überschrieben.

::

    timestamp.overwrite=cell3

.. note::

   Das Datumsfacet in der Suchoberfläche filtert nicht über ``created``, sondern über das Feld
   ``timestamp``. Wenn Sie den Zeitstempel mit einem Wert aus der CSV überschreiben möchten,
   geben Sie ``timestamp.overwrite`` anstelle von ``created.overwrite`` an.

Übernahme von Authentifizierungs- und Proxy-Einstellungen
-----------------------------------------------------------

``CsvListDataStore`` crawlt tatsächlich die in der CSV enthaltenen URLs; Authentifizierungs- und
Proxy-Einstellungen, die in der Datenspeicher-Konfiguration des Datei- oder Web-Crawlings
konfiguriert sind, werden dabei jedoch nicht übernommen. Geben Sie benötigte Einstellungen
einzeln als Parameter dieser Datenspeicher-Konfiguration an.

Beispiel für SMB-Authentifizierung:

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

Beispiel für Proxy-Einstellungen:

::

    crawler.web.proxyHost=proxy.example.com
    crawler.web.proxyPort=8080

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

.. note::

   Wie oben gezeigt, wird eine Zeile, in der ``url`` den Wert ``null`` liefert, nicht als Fehler
   behandelt, sondern stillschweigend übersprungen. Die Anzahl der übersprungenen Zeilen wird pro
   CSV-Datei gezählt und jeweils nach Abschluss der Leseschleife dieser Datei als eine einzelne
   zusammenfassende WARN-Logzeile ausgegeben (es wird nicht jede fehlgeschlagene URL einzeln
   protokolliert; werden mehrere CSV-Dateien verarbeitet, erscheint pro Datei eine WARN-Zeile).

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
