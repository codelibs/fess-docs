============================================================
Teil 12: SaaS-Daten durchsuchbar machen -- Integrationsszenarien mit Salesforce und Datenbanken
============================================================

Einleitung
==========

Wichtige Unternehmensdaten sind nicht nur auf Dateiservern und in Cloud-Speichern abgelegt, sondern auch in SaaS-Anwendungen und Datenbanken.
Kundeninformationen in Salesforce, Produktstammdaten in internen Datenbanken, in CSV-Dateien verwaltete Listendaten -- diese Daten sind normalerweise nur innerhalb des jeweiligen Systems durchsuchbar.

Dieser Artikel behandelt Szenarien, in denen SaaS- und Datenbankdaten in den Fess-Index importiert werden, um sie zusammen mit anderen Dokumenten systemuebergreifend durchsuchen zu koennen.

Zielgruppe
==========

- Personen, die SaaS- und Datenbankinformationen in die Suche einbeziehen moechten
- Personen, die die Nutzung von Data-Store-Plugins erlernen moechten
- Personen, die eine Suchplattform ueber mehrere Datenquellen hinweg aufbauen moechten

Szenario
========

Eine Vertriebsorganisation hat ihre Daten auf folgende Systeme verteilt.

.. list-table:: Uebersicht der Datenquellen
   :header-rows: 1
   :widths: 20 35 45

   * - System
     - Gespeicherte Daten
     - Aktuelle Herausforderung
   * - Salesforce
     - Kundeninformationen, Geschaeftsabschluesse, Aktivitaetsverlauf
     - Nur innerhalb von Salesforce durchsuchbar
   * - Interne DB
     - Produktstamm, Preislisten, Bestandsinformationen
     - Nur ueber eine dedizierte Verwaltungsoberflaeche zugaenglich
   * - CSV-Dateien
     - Kundenlisten, Veranstaltungsteilnehmerlisten
     - Koennen nur in Excel geoeffnet und visuell durchsucht werden
   * - Dateiserver
     - Angebote, Kostenvoranschlaege, Vertraege
     - Bereits von Fess gecrawlt

Das Ziel ist es, all diese Daten mit Fess systemuebergreifend durchsuchbar zu machen, sodass die fuer Vertriebsaktivitaeten benoetigten Informationen ueber ein einziges Suchfeld gefunden werden koennen.

Salesforce-Datenintegration
=============================

Um Salesforce-Daten in Fess durchsuchbar zu machen, verwenden Sie das Salesforce-Data-Store-Plugin.

Plugin-Installation
--------------------

1. Navigieren Sie zu [System] > [Plugins] im Administrationsbereich
2. Installieren Sie ``fess-ds-salesforce``

Verbindungseinstellungen
-------------------------

Fuer die Integration mit Salesforce muss eine Connected App konfiguriert werden.

**Vorbereitung auf Salesforce-Seite**

1. Erstellen Sie eine Connected App in den Salesforce-Einstellungen
2. Aktivieren Sie die OAuth-Einstellungen
3. Erhalten Sie den Consumer Key und das Consumer Secret

**Konfiguration auf Fess-Seite**

1. Navigieren Sie zu [Crawler] > [Data Store] > [Neu erstellen]
2. Handler-Name: Waehlen Sie SalesforceDataStore
3. Konfigurieren Sie Parameter und Skripte
4. Label: Setzen Sie ``salesforce``

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**Beispiel fuer die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

Fuer ``auth_type`` geben Sie ``oauth_password`` (Benutzername/Passwort-Authentifizierung) oder ``oauth_token`` (JWT-Bearer-Token-Authentifizierung) an. Bei Verwendung der JWT-Authentifizierung setzen Sie den privaten RSA-Schluessel in ``private_key``.

Auswahl der Zieldaten
----------------------

Salesforce enthaelt viele Objekte, aber nicht alle muessen durchsuchbar sein.
Konzentrieren Sie sich auf die Objekte, nach denen das Vertriebsteam haeufig sucht.

.. list-table:: Beispiel fuer Zielobjekte
   :header-rows: 1
   :widths: 25 35 40

   * - Objekt
     - Durchsuchbare Felder
     - Zweck
   * - Account
     - Name, Branche, Adresse, Beschreibung
     - Suche nach grundlegenden Kontoinformationen
   * - Opportunity
     - Name, Phase, Beschreibung, Betrag
     - Suche nach laufenden Geschaeften
   * - Case
     - Betreff, Beschreibung, Status
     - Suche im Anfrageverlauf

Datenbankintegration
=====================

Um interne Datenbankdaten durchsuchbar zu machen, verwenden Sie das Datenbank-Data-Store-Plugin.

Plugin-Installation
--------------------

Installieren Sie das Plugin ``fess-ds-db``.
Dieses Plugin kann sich ueber JDBC mit verschiedenen Datenbanken verbinden (MySQL, PostgreSQL, Oracle, SQL Server usw.).

Konfiguration
--------------

1. Navigieren Sie zu [Crawler] > [Data Store] > [Neu erstellen]
2. Handler-Name: Waehlen Sie DatabaseDataStore
3. Konfigurieren Sie Parameter und Skripte
4. Label: Setzen Sie ``database``

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**Beispiel fuer die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=product_name
    content=description

Die Ergebnisse der in ``sql`` angegebenen SQL-Abfrage werden gecrawlt. In Skripten verwenden Sie SQL-Spaltennamen (oder Spaltenbezeichnungen), um sie den Fess-Indexfeldern zuzuordnen.

SQL-Abfrage-Design
--------------------

Wichtige Punkte beim Entwerfen der SQL-Abfrage fuer den ``sql``-Parameter:

- Fuegen Sie eine ``url``-Spalte hinzu, die als Linkziel in den Suchergebnissen dient (z.B. ``CONCAT('https://.../', id) AS url``)
- Fuegen Sie Spalten hinzu, die als durchsuchbarer Textkoerper dienen
- Verwenden Sie eine ``WHERE``-Klausel, um unnoetige Daten auszuschliessen (z.B. ``status = 'active'``)

In Skripten verwenden Sie die SQL-Spaltennamen direkt, um sie den Fess-Indexfeldern zuzuordnen.

CSV-Datei-Integration
======================

Auch CSV-Dateidaten koennen durchsuchbar gemacht werden.

Konfiguration
--------------

Verwenden Sie das Plugin ``fess-ds-csv`` oder die CSV-Data-Store-Funktionalitaet.

1. Navigieren Sie zu [Crawler] > [Data Store] > [Neu erstellen]
2. Handler-Name: Waehlen Sie CsvDataStore
3. Konfigurieren Sie Parameter und Skripte
4. Label: Setzen Sie ``csv-data``

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Beispiel fuer die Skriptkonfiguration** (Spaltennamen verwenden, wenn eine Kopfzeile vorhanden ist)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

Bei ``has_header_line=true`` koennen die Spaltennamen der Kopfzeile in Skripten verwendet werden. Wenn keine Kopfzeile vorhanden ist, werden Spalten ueber Nummern referenziert, z.B. ``cell1``, ``cell2``, ``cell3``. Skripte koennen Groovy-Ausdruecke enthalten, einschliesslich Zeichenkettenverkettung.

Wenn CSV-Dateien regelmaessig aktualisiert werden, legen Sie den Ablageort fest und konfigurieren Sie einen Crawl-Zeitplan, damit die neuesten Daten automatisch im Index aktualisiert werden.

Systemuebergreifende Suche
============================

Sobald alle Datenquellenkonfigurationen abgeschlossen sind, koennen Sie die systemuebergreifende Suche erleben.

Suchbeispiel
--------------

Eine Suche nach "ABC GmbH" liefert beispielsweise folgende Ergebnisse:

1. Salesforce-Kontoinformationen (Account)
2. Angebotsdokumente vom Dateiserver (PDF)
3. Produktkaufhistorie aus der Datenbank
4. Messeteilnehmerliste aus CSV

Benutzer koennen die benoetigten Informationen finden, ohne sich Gedanken darueber machen zu muessen, wo diese gespeichert sind.

Filterung nach Label
---------------------

Wenn es viele Suchergebnisse gibt, grenzen Sie diese mithilfe von Labels ein.

- ``salesforce``: Nur Salesforce-Daten
- ``database``: Nur Datenbankdaten
- ``csv-data``: Nur CSV-Daten
- ``shared-files``: Nur Dateiserver-Dokumente

Betriebliche Ueberlegungen
===========================

Datenaktualitaet
-----------------

SaaS- und Datenbankdaten koennen haeufig aktualisiert werden.
Stellen Sie die Crawl-Haeufigkeit angemessen ein, um die Aktualitaet der Suchergebnisse zu gewaehrleisten.

.. list-table:: Empfohlene Crawl-Haeufigkeit
   :header-rows: 1
   :widths: 25 25 50

   * - Datenquelle
     - Empfohlene Haeufigkeit
     - Begruendung
   * - Salesforce
     - Alle 4-6 Stunden
     - Geschaefts- und Kundeninformationen werden waehrend der Geschaeftszeiten aktualisiert
   * - Datenbank
     - Alle 2-4 Stunden
     - Daten mit hoher Volatilitaet, wie z.B. Bestandsinformationen
   * - CSV
     - Taeglich
     - Wird normalerweise ueber Batch-Verarbeitung aktualisiert

Sicherheit der Datenbankverbindung
------------------------------------

Wenn Sie sich direkt mit einer Datenbank verbinden, achten Sie besonders auf die Sicherheit.

- Verwenden Sie einen Datenbankbenutzer mit Nur-Lese-Zugriff
- Beschraenken Sie Verbindungen auf die IP-Adresse des Fess-Servers
- Gewaehren Sie keinen Zugriff auf unnoetige Tabellen
- Achten Sie auf eine sichere Passwortverwaltung

Zusammenfassung
================

Dieser Artikel behandelte Szenarien, um Salesforce-, Datenbank- und CSV-Dateidaten mit Fess durchsuchbar zu machen.

- CRM-Datenintegration mit dem Salesforce-Data-Store-Plugin
- Interne-DB-Integration mit dem Datenbank-Data-Store-Plugin
- Listendatenintegration mit dem CSV-Data-Store
- Feldzuordnung und SQL-Abfrage-Design
- Nutzung von Labels bei der systemuebergreifenden Suche

Durch die Beseitigung von Datensilos koennen Sie eine Umgebung schaffen, in der alle Informationsquellen ueber eine einzige Plattform durchsuchbar sind.
Damit ist der Abschnitt "Praktische Loesungen" abgeschlossen. Ab dem naechsten Teil behandeln wir den Abschnitt "Architektur und Skalierung", beginnend mit dem Mehrmandanten-Design.

Referenzen
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
