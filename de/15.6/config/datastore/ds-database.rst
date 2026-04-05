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

1. Ein JDBC-Treiber ist erforderlich
2. Lesezugriff auf die Datenbank ist erforderlich
3. Bei großen Datenmengen ist ein geeignetes Query-Design wichtig

Installation des JDBC-Treibers
------------------------------

Platzieren Sie den JDBC-Treiber im ``lib/``-Verzeichnis:

::

    # Beispiel: MySQL-Treiber
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

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
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``driver``
     - Ja
     - Klassenname des JDBC-Treibers
   * - ``url``
     - Ja
     - JDBC-Verbindungs-URL
   * - ``username``
     - Nein
     - Datenbank-Benutzername
   * - ``password``
     - Nein
     - Datenbank-Passwort
   * - ``sql``
     - Ja
     - SQL-Query zum Abrufen der Daten
   * - ``fetch_size``
     - Nein
     - Fetch-Größe (Standard: 100). Für MySQL-Streaming kann der Wert ``MIN_VALUE`` als String angegeben werden.
   * - ``column_label.*``
     - Nein
     - Spaltenbezeichnung-Zuordnung. Bei BLOB-Spalten wird der MIME-Typ über die Dateierweiterung ermittelt und für die Inhaltsextraktion verwendet.
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

- ``<column_name>`` - Ergebnisspalten der SQL-Query (direkt über den Spaltennamen zugänglich)

SQL-Query-Design
================

Effiziente Queries
------------------

Bei großen Datenmengen ist die Query-Performance wichtig:

::

    # Effiziente Query mit Index-Nutzung
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

Bei der Verarbeitung von Daten mit Multibyte-Zeichen wie Deutsch oder Japanisch:

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
---------------------------------

.. warning::
   Das direkte Speichern von Passwörtern in Konfigurationsdateien stellt ein Sicherheitsrisiko dar.

Empfohlene Methoden:

1. Umgebungsvariablen verwenden
2. Verschlüsselungsfunktion von |Fess| verwenden
3. Nur-Lese-Benutzer verwenden

Prinzip der minimalen Rechte
----------------------------

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
---------------------------

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
