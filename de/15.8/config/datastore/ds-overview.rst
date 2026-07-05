==================================
Übersicht der Datenspeicher-Konnektoren
==================================

Übersicht
=========

Die Datenspeicher-Konnektoren von |Fess| bieten die Funktionalität, Inhalte aus anderen Datenquellen als Webseiten oder Dateisystemen abzurufen und zu indizieren.

Mit Datenspeicher-Konnektoren können Sie Daten aus folgenden Quellen durchsuchbar machen:

- Cloud-Speicher (Box, Dropbox, Google Drive, OneDrive)
- Kollaborationstools (Confluence, Jira, Slack)
- Datenbanken (MySQL, PostgreSQL, Oracle usw.)
- Andere Systeme (Git, Salesforce, Elasticsearch usw.)

Verfügbare Konnektoren
======================

|Fess| bietet Konnektoren für verschiedene Datenquellen an.
Viele Konnektoren werden als Plugins bereitgestellt und können bei Bedarf installiert werden.

Cloud-Speicher
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Konnektor
     - Plugin
     - Beschreibung
   * - :doc:`ds-box`
     - fess-ds-box
     - Crawlt Dateien und Ordner von Box.com
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - Crawlt Dateien und Ordner von Dropbox
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - Crawlt Google Drive
   * - :doc:`ds-microsoft365`
     - fess-ds-microsoft365
     - Crawlt OneDrive, SharePoint usw.

Kollaborationstools
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Konnektor
     - Plugin
     - Beschreibung
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - Crawlt Confluence und Jira
   * - :doc:`ds-slack`
     - fess-ds-slack
     - Crawlt Slack-Nachrichten und -Dateien

Entwicklungs- und Betriebstools
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Konnektor
     - Plugin
     - Beschreibung
   * - :doc:`ds-git`
     - fess-ds-git
     - Crawlt Quellcode aus Git-Repositories
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Ruft Daten von Elasticsearch/OpenSearch ab
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Crawlt Salesforce-Objekte

Datenbank und Dateien
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Konnektor
     - Plugin
     - Beschreibung
   * - :doc:`ds-database`
     - fess-ds-db
     - Ruft Daten aus JDBC-kompatiblen Datenbanken ab
   * - :doc:`ds-csv`
     - fess-ds-csv
     - Ruft Daten aus CSV-Dateien ab
   * - :doc:`ds-json`
     - fess-ds-json
     - Ruft Daten aus JSON-Dateien ab

Installation von Konnektoren
============================

Plugin-Installation
-------------------

Datenspeicher-Konnektor-Plugins können über die Administrationsoberfläche installiert werden.

Über die Administrationsoberfläche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Bei der Administrationsoberfläche anmelden
2. Zu "System" → "Plugin" navigieren
3. Auf die Schaltfläche "Installieren" klicken
4. Das Plugin im Tab "Remote" auswählen (oder im Tab "Lokal" eine JAR-Datei hochladen)
5. Auf "Installieren" klicken
6. |Fess| neu starten


Grundlagen der Datenspeicher-Konfiguration
==========================================

Die Konfiguration der Datenspeicher-Konnektoren erfolgt in der Administrationsoberfläche unter "Crawler" -> "Datenspeicher".

Gemeinsame Einstellungen
------------------------

Einstellungen, die allen Datenspeicher-Konnektoren gemeinsam sind:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beschreibung
   * - Name
     - Identifikationsname der Konfiguration
   * - Handler-Name
     - Name des zu verwendenden Konnektor-Handlers (z.B. ``CsvDataStore``)
   * - Parameter
     - Konnektor-spezifische Konfigurationsparameter (Schlüssel=Wert-Format)
   * - Skript
     - Mapping-Skript für Index-Felder
   * - Boost
     - Priorität in den Suchergebnissen
   * - Berechtigungen
     - Zugriffsberechtigungen für die gecrawlten Dokumente
   * - Virtuelle Hosts
     - Virtuelle Hosts, denen diese Konfiguration zugeordnet ist
   * - Beschreibung
     - Optionale Beschreibung dieser Konfiguration
   * - Sortierreihenfolge
     - Reihenfolge zur Sortierung der Konfigurationen in der Verwaltungsliste
   * - Aktiviert
     - Ob diese Konfiguration aktiviert ist

Parameter-Einstellungen
-----------------------

Parameter werden im Format ``Schlüssel=Wert`` mit Zeilenumbrüchen als Trennzeichen angegeben:

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

Skript-Einstellungen
--------------------

Im Skript werden die abgerufenen Daten auf die Index-Felder von |Fess| abgebildet.
Die linke Seite jeder Zeile ist das |Fess|-Indexfeld, die rechte Seite das vom Konnektor gelieferte Feld.

Das folgende Beispiel gilt für den CSV-Konnektor mit den Spaltenüberschriften ``link``, ``subject`` und ``body``:

::

    url=link
    title=subject
    content=body

.. note::

   Die im Skript referenzierbaren Feldnamen unterscheiden sich je nach Konnektor.
   Box/Dropbox/Google Drive/OneDrive referenzieren das abgerufene Objekt über das Präfix ``file.*``;
   Slack verwendet ``message.*``; Jira verwendet ``issue.*``.
   CSV-, JSON- und Datenbank-Konnektoren verwenden kein Präfix — die Felder werden direkt referenziert:

   - CSV: Spaltenüberschriften (bei ``has_header_line=true``), oder ``cell1``, ``cell2``, ... (1-basierter Spaltenindex); zusätzlich stehen ``csvfile`` und ``csvfilename`` zur Verfügung.
   - JSON: Feldnamen des JSON-Objekts.
   - Datenbank: Spaltennamen (Aliasse) aus dem SELECT-Ergebnis.

   Weitere Details finden Sie in der Dokumentation des jeweiligen Konnektors.

Authentifizierung
=================

Die Authentifizierungsparameter sind konnektorspezifisch.
Jeder Konnektor erfordert unterschiedliche Anmeldedaten und Konfigurationsschlüssel.
Weitere Informationen finden Sie in der Dokumentation des jeweiligen Konnektors.

Gemeinsame Parameter
====================

Der folgende Parameter wird von ``AbstractDataStore`` vererbt und steht in allen Konnektoren zur Verfügung:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Standardwert
     - Beschreibung
   * - ``readInterval``
     - ``0``
     - Wartezeit in Millisekunden zwischen der Verarbeitung einzelner Datensätze. Kann verwendet werden, um die Last auf die Datenquelle zu begrenzen.
   * - ``script_type``
     - ``groovy``
     - Typ der Skript-Engine für das Mapping der Indexfelder. Standardmäßig ist nur ``groovy`` verfügbar.

Fehlerbehebung
==============

Konnektor wird nicht angezeigt
------------------------------

1. Überprüfen Sie, ob das Plugin korrekt installiert ist
2. Starten Sie |Fess| neu
3. Prüfen Sie die Logs auf Fehler

Authentifizierungsfehler
------------------------

1. Überprüfen Sie die Richtigkeit der Anmeldedaten
2. Überprüfen Sie die Gültigkeit des Tokens
3. Überprüfen Sie, ob die erforderlichen Berechtigungen erteilt wurden
4. Überprüfen Sie, ob der API-Zugriff auf der Service-Seite erlaubt ist

Keine Daten abrufbar
--------------------

1. Überprüfen Sie das Format der Parameter
2. Überprüfen Sie die Zugriffsrechte auf die Ziel-Ordner/Dateien
3. Überprüfen Sie die Filtereinstellungen
4. Prüfen Sie detaillierte Fehlermeldungen in den Logs

Debug-Einstellungen
-------------------

Bei der Untersuchung von Problemen passen Sie das Log-Level an.
Das Crawlen von Datenspeichern läuft im Crawler-Prozess, daher muss die Log-Konfigurationsdatei des Crawlers bearbeitet werden:

``app/WEB-INF/env/crawler/resources/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Weiterführende Informationen
============================

- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../../admin/plugin-guide` - Leitfaden zur Plugin-Verwaltung
- :doc:`../../api/admin/api-admin-dataconfig` - Datenspeicher-Konfigurations-API
