=======================================
Teil 12: SaaS-Daten durchsuchbar machen
=======================================

Einleitung
==========

Wichtige Unternehmensdaten sind nicht nur auf Dateiservern und in Cloud-Speichern abgelegt, sondern auch in SaaS-Anwendungen und Datenbanken.
Kundeninformationen in Salesforce, Produktstammdaten in internen Datenbanken, in CSV-Dateien verwaltete Listendaten -- diese Daten sind normalerweise nur innerhalb des jeweiligen Systems durchsuchbar.

Dieser Artikel behandelt Szenarien, in denen SaaS- und Datenbankdaten in den Fess-Index importiert werden, um sie zusammen mit anderen Dokumenten systemübergreifend durchsuchen zu können.

Zielgruppe
==========

- Personen, die SaaS- und Datenbankinformationen in die Suche einbeziehen möchten
- Personen, die die Nutzung von Data-Store-Plugins erlernen möchten
- Personen, die eine Suchplattform über mehrere Datenquellen hinweg aufbauen möchten

Szenario
========

Eine Vertriebsorganisation hat ihre Daten auf folgende Systeme verteilt.

.. list-table:: Übersicht der Datenquellen
   :header-rows: 1
   :widths: 20 35 45

   * - System
     - Gespeicherte Daten
     - Aktuelle Herausforderung
   * - Salesforce
     - Kundeninformationen, Geschäftsabschlüsse, Aktivitätsverlauf
     - Nur innerhalb von Salesforce durchsuchbar
   * - Interne DB
     - Produktstamm, Preislisten, Bestandsinformationen
     - Nur über eine dedizierte Verwaltungsoberfläche zugänglich
   * - CSV-Dateien
     - Kundenlisten, Veranstaltungsteilnehmerlisten
     - Können nur in Excel geöffnet und visuell durchsucht werden
   * - Dateiserver
     - Angebote, Kostenvoranschläge, Verträge
     - Bereits von Fess gecrawlt

Das Ziel ist es, all diese Daten mit Fess systemübergreifend durchsuchbar zu machen, sodass die für Vertriebsaktivitäten benötigten Informationen über ein einziges Suchfeld gefunden werden können.

Salesforce-Datenintegration
=============================

Um Salesforce-Daten in Fess durchsuchbar zu machen, verwenden Sie das Salesforce-Data-Store-Plugin.

Plugin-Installation
--------------------

1. Navigieren Sie zu [System] > [Plugins] im Administrationsbereich
2. Installieren Sie ``fess-ds-salesforce``

Verbindungseinstellungen
-------------------------

Für die Integration mit Salesforce muss eine Connected App konfiguriert werden.

**Vorbereitung auf Salesforce-Seite**

1. Erstellen Sie eine Connected App in den Salesforce-Einstellungen
2. Aktivieren Sie die OAuth-Einstellungen
3. Erhalten Sie den Consumer Key und das Consumer Secret

**Konfiguration auf Fess-Seite**

1. Navigieren Sie zu [Crawler] > [Data Store] > [Neu erstellen]
2. Handler-Name: Wählen Sie SalesforceDataStore
3. Konfigurieren Sie Parameter und Skripte
4. Label: Setzen Sie ``salesforce``

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

Für ``auth_type`` geben Sie ``oauth_password`` (Benutzername/Passwort-Authentifizierung) oder ``oauth_token`` (JWT-Bearer-Token-Authentifizierung) an. Bei Verwendung der JWT-Authentifizierung setzen Sie den privaten RSA-Schlüssel in ``private_key``.

Auswahl der Zieldaten
----------------------

Salesforce enthält viele Objekte, aber nicht alle müssen durchsuchbar sein.
Konzentrieren Sie sich auf die Objekte, nach denen das Vertriebsteam häufig sucht.

.. list-table:: Beispiel für Zielobjekte
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
     - Suche nach laufenden Geschäften
   * - Case
     - Betreff, Beschreibung, Status
     - Suche im Anfrageverlauf

Datenbankintegration
=====================

Um interne Datenbankdaten durchsuchbar zu machen, verwenden Sie das Datenbank-Data-Store-Plugin.

Plugin-Installation
--------------------

Installieren Sie das Plugin ``fess-ds-db``.
Dieses Plugin kann sich über JDBC mit verschiedenen Datenbanken verbinden (MySQL, PostgreSQL, Oracle, SQL Server usw.).

Konfiguration
--------------

1. Navigieren Sie zu [Crawler] > [Data Store] > [Neu erstellen]
2. Handler-Name: Wählen Sie DatabaseDataStore
3. Konfigurieren Sie Parameter und Skripte
4. Label: Setzen Sie ``database``

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=product_name
    content=description

Die Ergebnisse der in ``sql`` angegebenen SQL-Abfrage werden gecrawlt. In Skripten verwenden Sie SQL-Spaltennamen (oder Spaltenbezeichnungen), um sie den Fess-Indexfeldern zuzuordnen.

SQL-Abfrage-Design
--------------------

Wichtige Punkte beim Entwerfen der SQL-Abfrage für den ``sql``-Parameter:

- Fügen Sie eine ``url``-Spalte hinzu, die als Linkziel in den Suchergebnissen dient (z.B. ``CONCAT('https://.../', id) AS url``)
- Fügen Sie Spalten hinzu, die als durchsuchbarer Textkörper dienen
- Verwenden Sie eine ``WHERE``-Klausel, um unnötige Daten auszuschließen (z.B. ``status = 'active'``)

In Skripten verwenden Sie die SQL-Spaltennamen direkt, um sie den Fess-Indexfeldern zuzuordnen.

CSV-Datei-Integration
======================

Auch CSV-Dateidaten können durchsuchbar gemacht werden.

Konfiguration
--------------

Verwenden Sie das Plugin ``fess-ds-csv`` oder die CSV-Data-Store-Funktionalität.

1. Navigieren Sie zu [Crawler] > [Data Store] > [Neu erstellen]
2. Handler-Name: Wählen Sie CsvDataStore
3. Konfigurieren Sie Parameter und Skripte
4. Label: Setzen Sie ``csv-data``

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Beispiel für die Skriptkonfiguration** (Spaltennamen verwenden, wenn eine Kopfzeile vorhanden ist)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

Bei ``has_header_line=true`` können die Spaltennamen der Kopfzeile in Skripten verwendet werden. Wenn keine Kopfzeile vorhanden ist, werden Spalten über Nummern referenziert, z.B. ``cell1``, ``cell2``, ``cell3``. Skripte können Groovy-Ausdrücke enthalten, einschließlich Zeichenkettenverkettung.

Wenn CSV-Dateien regelmäßig aktualisiert werden, legen Sie den Ablageort fest und konfigurieren Sie einen Crawl-Zeitplan, damit die neuesten Daten automatisch im Index aktualisiert werden.

Systemübergreifende Suche
============================

Sobald alle Datenquellenkonfigurationen abgeschlossen sind, können Sie die systemübergreifende Suche erleben.

Suchbeispiel
--------------

Eine Suche nach "ABC GmbH" liefert beispielsweise folgende Ergebnisse:

1. Salesforce-Kontoinformationen (Account)
2. Angebotsdokumente vom Dateiserver (PDF)
3. Produktkaufhistorie aus der Datenbank
4. Messeteilnehmerliste aus CSV

Benutzer können die benötigten Informationen finden, ohne sich Gedanken darüber machen zu müssen, wo diese gespeichert sind.

Filterung nach Label
---------------------

Wenn es viele Suchergebnisse gibt, grenzen Sie diese mithilfe von Labels ein.

- ``salesforce``: Nur Salesforce-Daten
- ``database``: Nur Datenbankdaten
- ``csv-data``: Nur CSV-Daten
- ``shared-files``: Nur Dateiserver-Dokumente

Betriebliche Überlegungen
===========================

Datenaktualität
-----------------

SaaS- und Datenbankdaten können häufig aktualisiert werden.
Stellen Sie die Crawl-Häufigkeit angemessen ein, um die Aktualität der Suchergebnisse zu gewährleisten.

.. list-table:: Empfohlene Crawl-Häufigkeit
   :header-rows: 1
   :widths: 25 25 50

   * - Datenquelle
     - Empfohlene Häufigkeit
     - Begründung
   * - Salesforce
     - Alle 4-6 Stunden
     - Geschäfts- und Kundeninformationen werden während der Geschäftszeiten aktualisiert
   * - Datenbank
     - Alle 2-4 Stunden
     - Daten mit hoher Volatilität, wie z.B. Bestandsinformationen
   * - CSV
     - Täglich
     - Wird normalerweise über Batch-Verarbeitung aktualisiert

Sicherheit der Datenbankverbindung
------------------------------------

Wenn Sie sich direkt mit einer Datenbank verbinden, achten Sie besonders auf die Sicherheit.

- Verwenden Sie einen Datenbankbenutzer mit Nur-Lese-Zugriff
- Beschränken Sie Verbindungen auf die IP-Adresse des Fess-Servers
- Gewähren Sie keinen Zugriff auf unnötige Tabellen
- Achten Sie auf eine sichere Passwortverwaltung

Zusammenfassung
================

Dieser Artikel behandelte Szenarien, um Salesforce-, Datenbank- und CSV-Dateidaten mit Fess durchsuchbar zu machen.

- CRM-Datenintegration mit dem Salesforce-Data-Store-Plugin
- Interne-DB-Integration mit dem Datenbank-Data-Store-Plugin
- Listendatenintegration mit dem CSV-Data-Store
- Feldzuordnung und SQL-Abfrage-Design
- Nutzung von Labels bei der systemübergreifenden Suche

Durch die Beseitigung von Datensilos können Sie eine Umgebung schaffen, in der alle Informationsquellen über eine einzige Plattform durchsuchbar sind.
Damit ist der Abschnitt "Praktische Lösungen" abgeschlossen. Ab dem nächsten Teil behandeln wir den Abschnitt "Architektur und Skalierung", beginnend mit dem Mehrmandanten-Design.

Referenzen
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
