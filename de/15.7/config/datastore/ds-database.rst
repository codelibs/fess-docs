==================================
Datenbank-Konnektor
==================================

Übersicht
=========

Der Datenbank-Konnektor bietet die Funktionalität, Daten aus JDBC-kompatiblen relationalen Datenbanken abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-db`` erforderlich.

Unterstützte Datenbanken
========================

Alle JDBC-kompatiblen Datenbanken werden unterstützt. Wichtige Beispiele:

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

Voraussetzungen
===============

1. Das Plugin ``fess-ds-db`` muss installiert sein
2. Ein JDBC-Treiber für die Zieldatenbank ist erforderlich
3. Lesezugriff auf die Datenbank ist erforderlich
4. Bei großen Datenmengen ist ein geeignetes Query-Design wichtig

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Herunterladen von Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Platzieren
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2: Installation über die Administrationsoberfläche

1. "System" -> "Plugins" öffnen
2. JAR-Datei hochladen
3. |Fess| neu starten

JDBC-Treiber-Installation
--------------------------

Platzieren Sie den JDBC-Treiber für die Zieldatenbank im Classpath von |Fess| (Verzeichnis ``app/WEB-INF/lib/``):

::

    # Beispiel: MySQL-Treiber
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Starten Sie |Fess| neu, um den Treiber zu laden.

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
     - Products Database
   * - Handler-Name
     - DatabaseDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Beispiel für MySQL/MariaDB:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

Beispiel für PostgreSQL:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``driver``
     - Ja
     - Klassenname des JDBC-Treibers (ohne Angabe wird eine ``DataStoreException`` ausgelöst)
   * - ``url``
     - Ja
     - JDBC-Verbindungs-URL (erforderlich für die Verbindung)
   * - ``sql``
     - Ja
     - SQL-Query zum Abrufen der Daten (ohne Angabe wird eine ``DataStoreException`` ausgelöst)
   * - ``username``
     - Nein
     - Datenbank-Benutzername
   * - ``password``
     - Nein
     - Datenbank-Passwort
   * - ``fetch_size``
     - Nein
     - JDBC-Fetch-Größe. Für MySQL-Streaming-Resultsets kann ``MIN_VALUE`` angegeben werden
   * - ``default_mimetype``
     - Nein
     - Standard-MIME-Typ für die Inhaltsextraktion aus BLOB- und Binärspalten
   * - ``column_label.mimetype``
     - Nein
     - Gibt den Spaltennamen an, der den MIME-Typ für die Extraktion aus BLOB- und Binärspalten enthält (Beispiel: ``column_label.mimetype=content_type``)
   * - ``column_label.filename``
     - Nein
     - Gibt den Spaltennamen an, der den Dateinamen für die Extraktion aus BLOB- und Binärspalten enthält (MIME-Typ wird aus der Dateiendung abgeleitet)
   * - ``info.*``
     - Nein
     - Zusätzliche JDBC-Verbindungseigenschaften (Beispiel: ``info.ssl=true``). Der Schlüssel ohne ``info.`` wird an den JDBC-Treiber übergeben
   * - ``readInterval``
     - Nein
     - Verzögerung in Millisekunden zwischen der Verarbeitung jeder Zeile. Standard: 0
   * - ``script_type``
     - Nein
     - Skript-Engine-Typ. Standard: groovy

Skript-Einstellungen
--------------------

Ordnen Sie die SQL-Spaltennamen den Index-Feldern zu:

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

Verfügbare Felder:

- ``<column_name>`` - Ergebnisspalten der SQL-Query (direkt über den Spaltenbezeichner zugänglich, ohne Präfix wie ``data.``)

.. note::
   Die Spaltennamen müssen mit den Spaltenbezeichnern (Aliasnamen) in der ``SELECT``-Klausel übereinstimmen.
   Bei Aggregatfunktionen oder Ausdrücken vergeben Sie mit ``AS`` einen expliziten Aliasnamen
   (Beispiel: ``COUNT(*) AS total``).

Laden von BLOB- und Binärdaten
==============================

Spalten vom Typ BLOB, CLOB, NCLOB, Byte-Array oder Binär-Stream werden automatisch
einer Inhaltsextraktion unterzogen (derselbe Extraktor wie beim Datei-Crawling) und als
Text indiziert. Spalten vom Array-Typ werden in leerzeichengetrennte Zeichenketten
umgewandelt. NULL-Werte werden zu leeren Zeichenketten.

Damit Text aus BLOB- und Binär-Streams korrekt extrahiert werden kann, muss der Datentyp
(MIME-Typ) bestimmt werden. Die folgende Prioritätsreihenfolge wird verwendet:

1. ``column_label.mimetype=<Spaltenname>`` - Der Wert der angegebenen Spalte wird als MIME-Typ verwendet
2. ``column_label.filename=<Spaltenname>`` - Der Wert der angegebenen Spalte wird als Dateiname behandelt, der MIME-Typ wird aus der Dateiendung abgeleitet
3. ``default_mimetype`` - Standard-MIME-Typ, der verwendet wird, wenn die obigen Methoden keinen Typ ergeben

Beispiel (BLOB der Spalte ``file_data`` wird mit dem MIME-Typ aus Spalte ``content_type`` extrahiert):

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

SQL-Query-Design
================

Effiziente Queries
------------------

Bei großen Datenmengen ist die Query-Performance wichtig.
SQL-Abfragen werden unverändert an die Datenbank gesendet (kein Parameter-Binding):

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

Inkrementelles Crawling
-----------------------

Methode zum Abrufen nur der aktualisierten Datensätze:

::

    # Filterung nach Aktualisierungsdatum
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Bereichsangabe nach ID
    sql=SELECT * FROM articles WHERE id > 10000

URL-Generierung
---------------

Die Dokument-URL wird im Skript generiert:

::

    # Festes Muster
    url="https://example.com/article/" + id

    # Kombination mehrerer Felder
    url="https://example.com/" + category + "/" + slug

    # In der Datenbank gespeicherte URL verwenden
    url=url

Multibyte-Zeichenunterstützung
==============================

Bei der Verarbeitung von Daten mit Multibyte-Zeichen wie Japanisch:

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL verwendet standardmäßig UTF-8. Bei Bedarf:

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

Sicherheit
==========

Schutz der Datenbank-Anmeldedaten
----------------------------------

.. warning::
   Das direkte Speichern von Passwörtern in Konfigurationsdateien stellt ein Sicherheitsrisiko dar.

Empfohlene Methoden:

1. Umgebungsvariablen verwenden
2. Verschlüsselungsfunktion von |Fess| verwenden
3. Nur-Lese-Benutzer verwenden

Prinzip der minimalen Rechte
-----------------------------

Gewähren Sie dem Datenbankbenutzer nur die minimal erforderlichen Berechtigungen:

::

    -- MySQL-Beispiel
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Anwendungsbeispiele
===================

Produktkatalog-Suche
--------------------

Parameter:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

Skript:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " Kategorie: " + category + " Preis: " + price + " EUR"
    lastModified=updated_at

Wissensdatenbank-Artikel
------------------------

Parameter:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

Skript:

::

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

Fehlerbehebung
==============

JDBC-Treiber nicht gefunden
----------------------------

**Symptom**: ``ClassNotFoundException`` oder ``No suitable driver``

**Lösung**:

1. Überprüfen Sie, ob der JDBC-Treiber in ``lib/`` platziert ist
2. Überprüfen Sie, ob der Klassenname des Treibers korrekt ist
3. Starten Sie |Fess| neu

Verbindungsfehler
-----------------

**Symptom**: ``Connection refused`` oder Authentifizierungsfehler

**Zu überprüfen**:

1. Ist die Datenbank gestartet?
2. Sind Hostname und Portnummer korrekt?
3. Sind Benutzername und Passwort korrekt?
4. Firewall-Einstellungen prüfen

Query-Fehler
------------

**Symptom**: ``SQLException`` oder SQL-Syntaxfehler

**Zu überprüfen**:

1. Testen Sie die SQL-Query direkt in der Datenbank
2. Überprüfen Sie, ob die Spaltennamen korrekt sind
3. Überprüfen Sie, ob die Tabellennamen korrekt sind

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-csv` - CSV-Konnektor
- :doc:`ds-json` - JSON-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
