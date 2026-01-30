==================================
Datenbank-Konnektor
==================================

Übersicht
=========

Der Datenbank-Konnektor bietet die Funktionalität, Daten aus JDBC-kompatiblen relationalen Datenbanken abzurufen und im |Fess|-Index zu registrieren.

Diese Funktion ist in |Fess| integriert und erfordert kein zusätzliches Plugin.

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
     - Ja
     - Datenbank-Benutzername
   * - ``password``
     - Ja
     - Datenbank-Passwort
   * - ``sql``
     - Ja
     - SQL-Query zum Abrufen der Daten
   * - ``fetch.size``
     - Nein
     - Fetch-Größe (Standard: 100)

Skript-Einstellungen
--------------------

Ordnen Sie die SQL-Spaltennamen den Index-Feldern zu:

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

Verfügbare Felder:

- ``data.<column_name>`` - Ergebnisspalten der SQL-Query

SQL-Query-Design
================

Effiziente Queries
------------------

Bei großen Datenmengen ist die Query-Performance wichtig:

::

    # Effiziente Query mit Index-Nutzung
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
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
    url="https://example.com/article/" + data.id

    # Kombination mehrerer Felder
    url="https://example.com/" + data.category + "/" + data.slug

    # In der Datenbank gespeicherte URL verwenden
    url=data.url

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

Connection-Pooling
==================

Bei der Verarbeitung großer Datenmengen sollten Sie Connection-Pooling in Betracht ziehen:

::

    # Einstellungen bei Verwendung von HikariCP
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

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

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " Kategorie: " + data.category + " Preis: " + data.price + " EUR"
    lastModified=data.updated_at

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

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

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
