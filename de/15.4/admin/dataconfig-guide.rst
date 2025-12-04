====================
Datenspeicher-Crawl
====================

Übersicht
=========

Mit |Fess| können Sie Datenquellen wie Datenbanken oder CSV als Crawl-Ziele festlegen.
Hier wird die erforderliche Datenspeicherkonfiguration dafür erläutert.

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite für die Datenspeicherkonfiguration zu öffnen, klicken Sie im linken Menü auf [Crawler > Datenspeicher].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Datenspeicherkonfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Geben Sie den Namen der Crawl-Konfiguration an.

Handler-Name
::::::::::::

Der Handler-Name zur Verarbeitung des Datenspeichers.

* DatabaseDataStore: Crawlt eine Datenbank
* CsvDataStore: Crawlt CSV/TSV-Dateien
* CsvListDataStore: Crawlt eine CSV-Datei, die Dateipfade zu indizierenden Dateien beschreibt

Parameter
:::::::::

Geben Sie Parameter für den Datenspeicher an.

Skript
::::::

Geben Sie an, in welchen Feldern die vom Datenspeicher abgerufenen Werte festgelegt werden sollen.
Ausdrücke können in Groovy geschrieben werden.

Boost-Wert
::::::::::

Geben Sie den Boost-Wert für Dokumente an, die mit dieser Konfiguration gecrawlt werden.

Berechtigung
::::::::::::

Geben Sie die Berechtigung für diese Konfiguration an.
Um beispielsweise Suchergebnisse für Benutzer anzuzeigen, die zur Gruppe „developer" gehören, geben Sie {group}developer an.
Für Benutzerebene geben Sie {user}Benutzername an, für Rollenebene {role}Rollenname und für Gruppenebene {group}Gruppenname.

Virtueller Host
:::::::::::::::

Geben Sie den Hostnamen des virtuellen Hosts an.
Weitere Details finden Sie unter :doc:`Virtueller Host im Konfigurationshandbuch <../config/virtual-host>`.

Status
::::::

Geben Sie an, ob diese Crawl-Konfiguration verwendet werden soll.

Beschreibung
::::::::::::

Sie können eine Beschreibung eingeben.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Beispiele
=========

DatabaseDataStore
-----------------

Datenbank-Crawling wird erklärt.

Als Beispiel wird eine Tabelle in der MySQL-Datenbank testdb wie folgt angenommen, auf die mit Benutzername hoge und Passwort fuga zugegriffen werden kann.

::

    CREATE TABLE doc (
        id BIGINT NOT NULL AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        content VARCHAR(255) NOT NULL,
        latitude VARCHAR(20),
        longitude VARCHAR(20),
        versionNo INTEGER NOT NULL,
        PRIMARY KEY (id)
    );

Hier fügen wir folgende Daten ein:

::

    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 1', 'コンテンツ 1 です．', '37.77493', ' -122.419416', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 2', 'コンテンツ 2 です．', '34.701909', '135.494977', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 3', 'コンテンツ 3 です．', '-33.868901', '151.207091', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 4', 'コンテンツ 4 です．', '51.500152', '-0.113736', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 5', 'コンテンツ 5 です．', '35.681137', '139.766084', 1);

Parameter
:::::::::

Ein Beispiel für die Parameterkonfiguration ist wie folgt:

::

    driver=com.mysql.jdbc.Driver
    url=jdbc:mysql://localhost:3306/testdb?useUnicode=true&characterEncoding=UTF-8
    username=hoge
    password=fuga
    sql=select * from doc

Parameter haben das Format „Schlüssel=Wert". Die Schlüsselerklärungen sind wie folgt:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - driver
     - Treiberklassenname
   * - url
     - URL
   * - username
     - Benutzername für die Datenbankverbindung
   * - password
     - Passwort für die Datenbankverbindung
   * - sql
     - SQL-Anweisung zum Abrufen von Crawl-Zielen

Tabelle: Beispiel für DB-Konfigurationsparameter


Skript
::::::

Ein Beispiel für die Skriptkonfiguration ist wie folgt:

::

    url="http://SERVERNAME/" + id
    host="SERVERNAME"
    site="SERVERNAME"
    title=title
    content=content
    cache=content
    digest=content
    anchor=
    content_length=content.length()
    last_modified=new java.util.Date()
    location=latitude + "," + longitude
    latitude=latitude
    longitude=longitude

Parameter haben das Format „Schlüssel=Wert". Die Schlüsselerklärungen sind wie folgt:

Die Werte werden in Groovy geschrieben.
Schließen Sie Zeichenketten in doppelte Anführungszeichen ein. Durch Zugriff auf den Datenbank-Spaltennamen wird der entsprechende Wert abgerufen.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - url
     - URL (Passen Sie sie an Ihre Umgebung an, um eine URL zu konfigurieren, über die auf die Daten zugegriffen werden kann)
   * - host
     - Hostname
   * - site
     - Site-Pfad
   * - title
     - Titel
   * - content
     - Dokumentinhalt (zu indizierender Text)
   * - cache
     - Dokument-Cache (nicht zu indizieren)
   * - digest
     - In Suchergebnissen angezeigter Digest-Teil
   * - anchor
     - Im Dokument enthaltene Links (normalerweise nicht erforderlich)
   * - content_length
     - Dokumentlänge
   * - last_modified
     - Letztes Änderungsdatum des Dokuments

Tabelle: Skriptkonfigurationsinhalt


Treiber
:::::::

Zum Verbinden mit der Datenbank ist ein Treiber erforderlich. Platzieren Sie die JAR-Datei in app/WEB-INF/lib.

CsvDataStore
------------

CSV-Datei-Crawling wird erklärt.

Erstellen Sie beispielsweise eine test.csv-Datei im Verzeichnis /home/taro/csv mit folgendem Inhalt.
Die Dateikodierung sollte Shift_JIS sein.

::

    1,タイトル 1,テスト1です。
    2,タイトル 2,テスト2です。
    3,タイトル 3,テスト3です。
    4,タイトル 4,テスト4です。
    5,タイトル 5,テスト5です。
    6,タイトル 6,テスト6です。
    7,タイトル 7,テスト7です。
    8,タイトル 8,テスト8です。
    9,タイトル 9,テスト9です。


Parameter
:::::::::

Ein Beispiel für die Parameterkonfiguration ist wie folgt:

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

Parameter haben das Format „Schlüssel=Wert". Die Schlüsselerklärungen sind wie folgt:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - directories
     - Verzeichnis mit CSV-Dateien (.csv oder .tsv)
   * - files
     - CSV-Dateien (bei direkter Angabe)
   * - fileEncoding
     - Kodierung der CSV-Datei
   * - separatorCharacter
     - Trennzeichen


Tabelle: Beispiel für CSV-Datei-Konfigurationsparameter


Skript
::::::

Ein Beispiel für die Skriptkonfiguration ist wie folgt:

::

    url="http://SERVERNAME/" + cell1
    host="SERVERNAME"
    site="SERVERNAME"
    title=cell2
    content=cell3
    cache=cell3
    digest=cell3
    anchor=
    content_length=cell3.length()
    last_modified=new java.util.Date()

Parameter haben das Format „Schlüssel=Wert".
Die Schlüssel sind dieselben wie beim Datenbank-Crawling.
Daten in CSV-Dateien werden in cell[Nummer] gespeichert (Nummern beginnen bei 1).
Wenn keine Daten in einer CSV-Zelle vorhanden sind, kann der Wert null sein.

EsDataStore
-----------

Die Datenquelle ist Elasticsearch, aber die grundlegende Verwendung ist dieselbe wie bei CsvDataStore.

Parameter
:::::::::

Ein Beispiel für die Parameterkonfiguration ist wie folgt:

::

    settings.cluster.name=elasticsearch
    hosts=SERVERNAME:9300
    index=logindex
    type=data

Parameter haben das Format „Schlüssel=Wert". Die Schlüsselerklärungen sind wie folgt:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - settings.*
     - Elasticsearch-Einstellungsinformationen
   * - hosts
     - Elasticsearch-Verbindungsziel
   * - index
     - Indexname
   * - type
     - Typname
   * - query
     - Abfrage für Abrufbedingungen

Tabelle: Beispiel für Elasticsearch-Konfigurationsparameter


Skript
::::::

Ein Beispiel für die Skriptkonfiguration ist wie folgt:

::

    url=source.url
    host="SERVERNAME"
    site="SERVERNAME"
    title=source.title
    content=source.content
    digest=
    anchor=
    content_length=source.size
    last_modified=new java.util.Date()

Parameter haben das Format „Schlüssel=Wert".
Die Schlüssel sind dieselben wie beim Datenbank-Crawling.
Sie können Werte mit source.* abrufen und festlegen.

CsvListDataStore
----------------

Wird zum Crawlen großer Dateimengen verwendet.
Durch Platzieren einer CSV-Datei mit Pfaden zu aktualisierten Dateien und Crawlen nur der angegebenen Pfade kann die Crawl-Ausführungszeit verkürzt werden.

Das Format zum Beschreiben von Pfaden ist wie folgt:

::

    [Aktion]<Trennzeichen>[Pfad]

Geben Sie eine der folgenden Aktionen an:

* create: Datei wurde erstellt
* modify: Datei wurde aktualisiert
* delete: Datei wurde gelöscht

Erstellen Sie beispielsweise eine test.csv-Datei im Verzeichnis /home/taro/csv mit folgendem Inhalt.
Die Dateikodierung sollte Shift_JIS sein.

Pfade werden in derselben Notation wie bei der Angabe von Crawl-Zielpfaden beim Datei-Crawling beschrieben.
Geben Sie wie folgt „file:/[Pfad]" oder „smb://[Pfad]" an:

::

    modify,smb://servername/data/testfile1.txt
    modify,smb://servername/data/testfile2.txt
    modify,smb://servername/data/testfile3.txt
    modify,smb://servername/data/testfile4.txt
    modify,smb://servername/data/testfile5.txt
    modify,smb://servername/data/testfile6.txt
    modify,smb://servername/data/testfile7.txt
    modify,smb://servername/data/testfile8.txt
    modify,smb://servername/data/testfile9.txt
    modify,smb://servername/data/testfile10.txt


Parameter
:::::::::

Ein Beispiel für die Parameterkonfiguration ist wie folgt:

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

Parameter haben das Format „Schlüssel=Wert". Die Schlüsselerklärungen sind wie folgt:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - directories
     - Verzeichnis mit CSV-Dateien (.csv oder .tsv)
   * - fileEncoding
     - Kodierung der CSV-Datei
   * - separatorCharacter
     - Trennzeichen


Tabelle: Beispiel für CSV-Datei-Konfigurationsparameter


Skript
::::::

Ein Beispiel für die Skriptkonfiguration ist wie folgt:

::

    event_type=cell1
    url=cell2

Parameter haben das Format „Schlüssel=Wert".
Die Schlüssel sind dieselben wie beim Datenbank-Crawling.

Wenn für das Crawl-Ziel eine Authentifizierung erforderlich ist, müssen auch folgende Einstellungen konfiguriert werden:

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

.. |image0| image:: ../../../resources/images/en/15.4/admin/dataconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/dataconfig-2.png
