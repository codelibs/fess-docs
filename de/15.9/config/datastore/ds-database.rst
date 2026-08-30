=======================================
Datenbank-Konnektor (Datenbank-Suche)
=======================================

Übersicht
=========

Der Datenbank-Konnektor ist eine Funktion, mit der Datensätze aus JDBC-kompatiblen relationalen Datenbanken (MySQL, PostgreSQL, Oracle, SQL Server usw.) in den Index von |Fess| aufgenommen werden und damit eine Datenbank-Suche (Volltextsuche über Datenbankinhalte) realisiert wird. Die per SELECT-Anweisung abgerufenen Spalten werden dabei auf Suchfelder gemappt.

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

Methode 1: Installation über die Administrationsoberfläche

1. "System" -> "Plugins" öffnen
2. JAR-Datei hochladen
3. |Fess| neu starten

Methode 2: JAR-Datei direkt platzieren

::

    # Herunterladen aus dem CodeLibs-Repository
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Platzieren (dasselbe Verzeichnis, in das auch über die Administrationsoberfläche installiert wird)
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # oder
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

JDBC-Treiber-Installation
--------------------------

Der JDBC-Treiber ist nicht im Plugin enthalten. Beschaffen Sie den Treiber für Ihre Datenbank separat und platzieren Sie ihn selbst.

Das Datenspeicher-Crawling läuft im Crawler-Prozess, daher muss der Treiber im **Classpath des Crawler-Prozesses** liegen. Eines der folgenden Verzeichnisse ist geeignet:

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # Beispiel: MySQL-Treiber
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Starten Sie |Fess| neu, um den Treiber zu laden.

.. note::
   Fehlt der Treiber, schlägt das Crawling mit der Meldung
   ``The JDBC driver ... is not on the crawler classpath.`` fehl.

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
     - JDBC-Fetch-Größe. ``MIN_VALUE`` weist MySQL an, das Resultset zeilenweise zu lesen; andere Treiber lehnen negative Werte ab, und das Crawling wird nach einer Warnung mit dem Standardwert des Treibers fortgesetzt. Negative oder nicht numerische Werte werden gemeldet und ignoriert
   * - ``query_timeout``
     - Nein
     - Query-Timeout in Sekunden. ``0`` bedeutet keine Begrenzung (JDBC-Standard). Ohne Angabe des Parameters wird kein Timeout gesetzt
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

.. note::
   Hängt eine Query, gibt das Stoppen des Jobs den Crawler-Thread nicht frei.
   Die Stopp-Anforderung wird nur zwischen den Zeilen geprüft und kann daher einen
   Aufruf, der im Treiber blockiert, nicht unterbrechen. Setzen Sie ``query_timeout``
   für Queries, die lange laufen können.

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
- ``crawlingConfig`` - die Datenspeicher-Konfiguration
- ``crawlingContext`` - der Crawling-Kontext; ``crawlingContext.doc`` enthält das gerade erzeugte Dokument

.. note::
   Die Spaltennamen müssen mit den Spaltenbezeichnern (Aliasnamen) in der ``SELECT``-Klausel übereinstimmen.
   Bei Aggregatfunktionen oder Ausdrücken vergeben Sie mit ``AS`` einen expliziten Aliasnamen
   (Beispiel: ``COUNT(*) AS total``).

.. note::
   Die Groß-/Kleinschreibung der Spaltenbezeichner unterscheidet sich je nach Datenbank.
   PostgreSQL wandelt nicht in Anführungszeichen gesetzte Bezeichner in Kleinbuchstaben um,
   H2 in Großbuchstaben, und MySQL liefert sie wie deklariert. Ein Name, der nicht aufgelöst
   werden kann, lässt das Feld unbesetzt, statt einen Fehler auszulösen - vergeben Sie daher
   mit ``AS`` einen expliziten Aliasnamen, wenn Portabilität wichtig ist.

.. warning::
   Skripte können auf die **gesamte Parameterzuordnung des Datenspeichers** zugreifen, nicht
   nur auf die Ergebnisspalten der SQL-Query. ``driver``, ``url``, ``username``, ``password``
   und ``sql`` sind alle als gleichnamige Variablen sichtbar, sodass eine Spalte unbeabsichtigt
   überdeckt werden kann oder ein Parameterwert dort erscheint, wo eine fehlende Spalte
   erwartet wurde. Existieren beide, gewinnt der Wert der Spalte.

Laden von BLOB- und Binärdaten
==============================

Binärspalten (BLOB, ``BYTEA``, Byte-Array, Binär-Stream) werden einer Inhaltsextraktion
unterzogen - derselbe Extraktor wie beim Datei-Crawling - und als Text indiziert.

CLOB, NCLOB und Zeichen-Streams durchlaufen **keinen** Extraktor. Sie werden unverändert als
Text gelesen; die unten beschriebenen MIME-Typ-Hinweise gelten für sie nicht.

Spalten vom Array-Typ werden zu ihren mit Leerzeichen verbundenen Elementen. NULL-Werte
werden zu leeren Zeichenketten.

.. note::
   Ob eine BLOB-Spalte als ``java.sql.Blob`` oder als Byte-Array ankommt, entscheidet der
   JDBC-Treiber - MySQL und PostgreSQL liefern ein Byte-Array. Beide werden auf dieselbe
   Weise extrahiert.

.. note::
   CLOB und NCLOB werden vollständig und ohne Größenbegrenzung in den Speicher gelesen.
   Bei sehr großen Textspalten sollten Sie im SQL mit ``SUBSTRING`` oder Ähnlichem kürzen.
   Für den Weg über den Extraktor gilt die maximale Inhaltslänge des Crawlers.

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

.. warning::
   Die Query auf diese Weise einzuschränken macht aus dem Crawling noch kein
   inkrementelles Crawling. Wenn ein Crawl endet, löscht |Fess| die Dokumente dieser
   Datenspeicher-Konfiguration, die nicht Teil des soeben gelaufenen Crawls waren - eine
   gefilterte Query lässt also nur die passenden Zeilen im Index zurück.

   Fügen Sie ``delete_old_docs=false`` zu den Datenspeicher-Parametern hinzu, um die von
   früheren Crawls indexierten Dokumente zu behalten. Aus der Datenbank gelöschte Zeilen
   werden dann allerdings auch nicht mehr aus dem Index entfernt; führen Sie deshalb
   regelmäßig ein vollständiges Crawling durch.

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

.. warning::
   ``url=url`` tut nur dann das Erwartete, wenn das ``SELECT``-Ergebnis eine Spalte mit dem
   Bezeichner ``url`` enthält. Ohne eine solche Spalte wird der gleichnamige
   Datenspeicher-Parameter - also die **JDBC-Verbindungs-URL** - zur Dokument-URL. Vergeben
   Sie einen Aliasnamen für die Spalte, etwa ``SELECT page_url AS url``, oder benennen Sie sie
   im Skript, etwa ``url=page_url``.

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

1. Automatische Verschlüsselung nutzen

   Der Wert eines Parameters, dessen Name auf ``app.encrypt.property.pattern`` passt
   (Standard ``.*password|.*key|.*token|.*secret``), wird beim Speichern über die
   Administrationsoberfläche verschlüsselt und mit dem Präfix ``{cipher}`` abgelegt.
   ``password`` passt auf dieses Muster und wird daher nicht im Klartext gespeichert,
   wenn es über die Administrationsoberfläche gesetzt wird.

2. Umgebungsvariablen verwenden

   Eine Umgebungsvariable, deren Name mit ``FESS_ENV_`` beginnt, wird innerhalb eines
   Datenspeicher-Parameters als ``${Variablenname}`` expandiert:

   ::

       password=${FESS_ENV_DB_PASSWORD}

   Welche Namen expandiert werden, steuert ``crawler.data.env.param.key.pattern``
   (Standard ``^FESS_ENV_.*``).

3. Nur-Lese-Benutzer verwenden

.. note::
   Das Anheben von ``org.codelibs.fess.ds`` auf DEBUG legt keine Anmeldedaten offen: Die Werte
   von Parametern, die auf ``app.encrypt.property.pattern`` passen, sowie in der JDBC-URL
   eingebettete Anmeldedaten werden im Log maskiert.

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

Schlägt ein Crawling fehl, gibt die Meldung im Log an, welcher Schritt fehlgeschlagen ist.

JDBC-Treiber nicht gefunden
----------------------------

**Symptom**: ``The JDBC driver ... is not on the crawler classpath.``

**Lösung**:

1. Überprüfen Sie, ob der JDBC-Treiber in ``app/WEB-INF/lib/`` oder ``app/WEB-INF/env/crawler/lib/`` platziert ist
2. Überprüfen Sie, ob der in ``driver`` angegebene Klassenname korrekt ist
3. Starten Sie |Fess| neu

Verbindungsfehler
-----------------

**Symptom**: ``Failed to connect to <URL>.``

**Zu überprüfen**:

1. Ist die Datenbank gestartet?
2. Sind Hostname und Portnummer korrekt?
3. Sind Benutzername und Passwort korrekt?
4. Firewall-Einstellungen prüfen

Query-Fehler
------------

**Symptom**: ``Failed to execute the query.``

**Zu überprüfen**:

1. Testen Sie die SQL-Query direkt in der Datenbank
2. Überprüfen Sie, ob die Spaltennamen korrekt sind
3. Überprüfen Sie, ob die Tabellennamen korrekt sind

Fehlende Parameter
------------------

**Symptom**: ``The driver parameter is required.``, ``The url parameter is required.`` oder ``The sql parameter is required.``

Ein erforderlicher Parameter ist nicht gesetzt. Überprüfen Sie das Parameterfeld.

Nur einzelne Zeilen schlagen fehl
---------------------------------

Eine fehlgeschlagene Zeile bricht das Crawling nicht ab; sie wird unter "System" -> "Fehlerhafte URL"
protokolliert. Verwendet wird die Dokument-URL, sofern die Skripte eine erzeugt haben, und
``datastore://<ID der Datenspeicher-Konfiguration>/<Zeilennummer>``, wenn nicht.

Dokumente erscheinen nicht in den Suchergebnissen
-------------------------------------------------

1. Überprüfen Sie, ob die Skripte ``url``, ``title`` und ``content`` setzen
2. Überprüfen Sie, ob die Groß-/Kleinschreibung der Spaltenbezeichner mit der in den Skripten verwendeten übereinstimmt (siehe "Skript-Einstellungen")
3. Überprüfen Sie die Anzahl der Dokumente im Protokoll des Crawl-Jobs

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-csv` - CSV-Konnektor
- :doc:`ds-json` - JSON-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../crawler-basic` - Grundlegende Crawler-Konfiguration
- :doc:`../search-basic` - Suchfunktionen
