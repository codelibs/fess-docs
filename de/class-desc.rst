==================================
Fess-Architektur und Hauptfunktionen
==================================

Übersicht
=========

Diese Seite beschreibt die Hauptfunktionen und die Architektur von Fess aus Komponentensicht.
Fess verwendet ein modularisiertes Design, um den Aufbau von Suchsystemen zu erleichtern.

Gesamtarchitektur
=================

Fess besteht aus folgenden Hauptkomponenten:

.. figure:: ../resources/images/en/architecture-overview.png
   :scale: 100%
   :alt: Fess-Architekturübersicht
   :align: center

   Fess-Architekturübersicht

Hauptkomponenten
================

1. Crawler-Subsystem
---------------------

Das Crawler-Subsystem ist für das Sammeln von Dokumenten aus verschiedenen Datenquellen zuständig.

**Hauptklassen und -funktionen:**

Crawler
~~~~~~~

- **Rolle**: Zentrale Klasse für die Crawl-Verarbeitung
- **Hauptfunktionen**:

  - Sammeln von Dokumenten von Websites, Dateisystemen und Datenspeichern
  - Auswahl der Ziele basierend auf Crawl-Konfiguration
  - Verwaltung der Crawl-Job-Ausführung
  - Sitzungsverwaltung für Crawl-Ergebnisse

- **Ausführungsmodi**:

  - Regelmäßige Ausführung durch Scheduler
  - Manuelle Ausführung über die Admin-Oberfläche
  - Ausführung über die Befehlszeile

WebCrawler
~~~~~~~~~~

- **Rolle**: Crawling von Websites
- **Hauptfunktionen**:

  - Abrufen und Parsen von HTML-Seiten
  - Extrahieren und Verfolgen von Links
  - Unterstützung für JavaScript-basierte Websites
  - Unterstützung für authentifizierte Websites (BASIC/DIGEST/NTLM/FORM)
  - Einhaltung von robots.txt

FileCrawler
~~~~~~~~~~~

- **Rolle**: Crawling von Dateisystemen
- **Hauptfunktionen**:

  - Durchlaufen lokaler Dateisysteme
  - Zugriff auf Netzlaufwerke (SMB/CIFS)
  - Erkennung von Dateiformaten und Auswahl geeigneter Parser
  - Berechtigungsbasierte Zugriffskontrolle

DataStoreCrawler
~~~~~~~~~~~~~~~~

- **Rolle**: Crawling externer Datenspeicher
- **Hauptfunktionen**:

  - Abrufen von Daten aus Datenbanken
  - Integration mit Cloud-Speicher (Google Drive, Dropbox, Box usw.)
  - Integration mit Groupware (Office 365, Slack, Confluence usw.)
  - Erweiterbarkeit durch Plugins

CrawlConfig
~~~~~~~~~~~

- **Rolle**: Verwaltung der Crawl-Konfiguration
- **Hauptfunktionen**:

  - Definition von Ziel-URLs oder -Pfaden für das Crawling
  - Begrenzung der Crawl-Tiefe
  - Einstellung des Crawl-Intervalls
  - Festlegung von Ausschlussmustern
  - Zuweisung von Labels

2. Indexierungs-Subsystem
--------------------------

Das Indexierungs-Subsystem konvertiert gesammelte Dokumente in eine durchsuchbare Form.

DocumentParser
~~~~~~~~~~~~~~

- **Rolle**: Dokumentanalyse und Textextraktion
- **Hauptfunktionen**:

  - Unterstützung verschiedener Dateiformate mit Apache Tika
  - Extraktion von Metadaten
  - Automatische Erkennung der Zeichenkodierung
  - Automatische Spracherkennung

Indexer
~~~~~~~

- **Rolle**: Indexregistrierung in OpenSearch/Elasticsearch
- **Hauptfunktionen**:

  - Erstellung von Dokumentindizes
  - Beschleunigung durch Bulk-Indexierung
  - Indexoptimierung
  - Löschen alter Dokumente

FieldMapper
~~~~~~~~~~~

- **Rolle**: Definition von Feld-Mappings
- **Hauptfunktionen**:

  - Definition von Dokumentfeldern
  - Hinzufügen benutzerdefinierter Felder
  - Festlegung von Feldtypen (text, keyword, date usw.)
  - Konfiguration mehrsprachiger Analyzer

3. Such-Subsystem
------------------

Das Such-Subsystem verarbeitet Suchanfragen von Benutzern und gibt Ergebnisse zurück.

SearchService
~~~~~~~~~~~~~

- **Rolle**: Zentrum der Suchverarbeitung
- **Hauptfunktionen**:

  - Analyse und Optimierung von Abfragen
  - Ausführung von Abfragen an OpenSearch/Elasticsearch
  - Ranking der Suchergebnisse
  - Unterstützung von Facetten-Suche
  - Hervorhebung

QueryProcessor
~~~~~~~~~~~~~~

- **Rolle**: Vorverarbeitung von Suchanfragen
- **Hauptfunktionen**:

  - Normalisierung von Abfragen
  - Synonymerweiterung
  - Verarbeitung von Stoppwörtern
  - Abfragekorrektur

SuggestService
~~~~~~~~~~~~~~

- **Rolle**: Bereitstellung von Vorschlagsfunktionen
- **Hauptfunktionen**:

  - Generierung von Eingabevervollständigungsvorschlägen
  - Bereitstellung beliebter Suchbegriffe
  - Verwendung benutzerdefinierter Wörterbücher

RankingService
~~~~~~~~~~~~~~

- **Rolle**: Anpassung des Rankings der Suchergebnisse
- **Hauptfunktionen**:

  - Dokument-Boosting
  - Feld-Boosting
  - Benutzerdefiniertes Scoring
  - Anpassung der Relevanz

4. Verwaltungs-Subsystem
-------------------------

Das Verwaltungs-Subsystem verwaltet die Konfiguration und den Betrieb von Fess.

AdminConsole
~~~~~~~~~~~~

- **Rolle**: Webbasierte Verwaltungsoberfläche
- **Hauptfunktionen**:

  - Verwaltung der Crawl-Konfiguration
  - Scheduler-Einstellungen
  - Benutzer- und Rollenverwaltung
  - Systemeinstellungen
  - Log-Einsicht

Scheduler
~~~~~~~~~

- **Rolle**: Verwaltung von Job-Zeitplänen
- **Hauptfunktionen**:

  - Regelmäßige Ausführung von Crawl-Jobs
  - Regelmäßige Ausführung der Indexoptimierung
  - Log-Rotation
  - Zeitplaneinstellung mit Cron-Ausdrücken

BackupManager
~~~~~~~~~~~~~

- **Rolle**: Backup und Wiederherstellung
- **Hauptfunktionen**:

  - Backup von Konfigurationsdaten
  - Index-Snapshots
  - Wiederherstellungsfunktion
  - Planung automatischer Backups

5. Authentifizierungs- und Autorisierungs-Subsystem
----------------------------------------------------

Das Authentifizierungs- und Autorisierungs-Subsystem verwaltet Sicherheit und Zugriffskontrolle.

AuthenticationManager
~~~~~~~~~~~~~~~~~~~~~

- **Rolle**: Verwaltung der Benutzerauthentifizierung
- **Hauptfunktionen**:

  - Lokale Authentifizierung
  - LDAP/Active Directory-Integration
  - SAML-Integration
  - OpenID Connect-Integration
  - Rollenbasierte Zugriffskontrolle (RBAC)

RoleManager
~~~~~~~~~~~

- **Rolle**: Verwaltung von Rollen und Zugriffsrechten
- **Hauptfunktionen**:

  - Definition von Rollen
  - Zuweisung von Rollen an Benutzer
  - Zugriffskontrolle auf Dokumentebene
  - Filterung von Suchergebnissen

6. API-Schicht
--------------

Die API-Schicht bietet Integration mit externen Systemen.

SearchAPI
~~~~~~~~~

- **Rolle**: Bereitstellung der Such-API
- **Hauptfunktionen**:

  - Suche über REST-API
  - JSON-formatierte Antworten
  - OpenSearch-Kompatibilität
  - GSA (Google Search Appliance)-kompatible API

AdminAPI
~~~~~~~~

- **Rolle**: Bereitstellung der Verwaltungs-API
- **Hauptfunktionen**:

  - CRUD-Operationen für Crawl-Konfiguration
  - Indexverwaltung
  - Scheduler-Steuerung
  - Abrufen von Systeminformationen

7. Datenspeicher
-----------------

Der Datenspeicher ist für die Datenpersistenz von Fess zuständig.

ConfigStore
~~~~~~~~~~~

- **Rolle**: Speicherung von Konfigurationsdaten
- **Hauptfunktionen**:

  - Persistierung der Crawl-Konfiguration
  - Speicherung der Systemkonfiguration
  - Verwaltung von Benutzer- und Rolleninformationen
  - Verwendung von H2-Datenbank oder externer DB

SearchEngine
~~~~~~~~~~~~

- **Rolle**: Integration mit Suchmaschinen
- **Hauptfunktionen**:

  - Kommunikation mit OpenSearch/Elasticsearch
  - Indexverwaltung
  - Ausführung von Abfragen
  - Clustering-Unterstützung

Plugin-Architektur
==================

Fess kann durch Plugins erweitert werden.

DataStore-Plugins
-----------------

- **Rolle**: Verbindung zu externen Datenquellen
- **Verfügbare Plugins**:

  - Atlassian (Confluence/Jira)
  - Box
  - CSV
  - Database
  - Dropbox
  - Git/GitBucket
  - Google Drive
  - Office 365
  - S3
  - Slack
  - Weitere

Theme-Plugins
-------------

- **Rolle**: Anpassung der Suchoberfläche
- **Verfügbare Plugins**:

  - Simple Theme
  - Classic Theme

Ingester-Plugins
----------------

- **Rolle**: Vor- und Nachverarbeitung von Indexdaten
- **Verfügbare Plugins**:

  - Logger
  - NDJSON

Script-Plugins
--------------

- **Rolle**: Anpassung durch Skripte
- **Verfügbare Plugins**:

  - Groovy
  - OGNL

Konfigurationsverwaltung
========================

FessConfig
----------

- **Rolle**: Zentrale Verwaltung der Systemkonfiguration
- **Hauptkonfigurationselemente**:

  - Allgemeine Systemeinstellungen
  - Crawl-Einstellungen
  - Sucheinstellungen
  - Authentifizierungseinstellungen
  - Benachrichtigungseinstellungen
  - Leistungseinstellungen

DynamicProperties
-----------------

- **Rolle**: Verwaltung dynamischer Konfigurationen
- **Hauptfunktionen**:

  - Konfigurationsänderungen zur Laufzeit
  - Verwendung von Umgebungsvariablen
  - Profilspezifische Konfiguration

Zusammenfassung
===============

Fess realisiert ein leistungsstarkes Volltextsuchsystem durch die Zusammenarbeit dieser Komponenten.
Jede Komponente ist lose gekoppelt entworfen und kann bei Bedarf angepasst oder erweitert werden.

Für detailliertere Entwicklerinformationen siehe:

- `JavaDoc <https://fess.codelibs.org/apidocs/index.html>`__
- `XRef <https://fess.codelibs.org/xref/index.html>`__
- `Entwicklerhandbuch <dev/index.html>`__
- `GitHub-Repository <https://github.com/codelibs/fess>`__
