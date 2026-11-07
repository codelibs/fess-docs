====================================
Teil 17: Suche mit Plugins erweitern
====================================

Einleitung
==========

Fess unterstützt standardmäßig viele Datenquellen. Um jedoch unternehmensspezifische Systeme und Datenformate zu unterstützen, kann eine Erweiterung durch Plugins erforderlich sein.

In diesem Artikel wird die Plugin-Architektur von Fess erläutert und die Implementierung von benutzerdefinierten Datenquellen-Plugins und Ingest-Plugins vorgestellt.

Zielgruppe
==========

- Personen, die Fess mit eigenen Datenquellen verbinden möchten
- Java-Entwickler, die sich für die Plugin-Entwicklung interessieren
- Personen, die die interne Architektur von Fess verstehen möchten

Plugin-Architektur
===================

Fess bietet die folgenden Arten von Plugins.

.. list-table:: Plugin-Typen
   :header-rows: 1
   :widths: 25 35 40

   * - Typ
     - Rolle
     - Beispiele
   * - Data Store (fess-ds-\*)
     - Daten aus externen Datenquellen abrufen
     - Slack, Salesforce, DB
   * - Ingest (fess-ingest-\*)
     - Gecrawlte Daten verarbeiten und transformieren
     - Example
   * - Theme (fess-theme-\*)
     - Design der Suchoberfläche
     - Simple, Code Search
   * - Script (fess-script-\*)
     - Unterstützung von Skriptsprachen
     - OGNL
   * - Web App (fess-webapp-\*)
     - Erweiterungen für Webanwendungen
     - MCP Server

Plugin-Bereitstellung
---------------------

Plugins werden als JAR-Dateien bereitgestellt und im Plugin-Verzeichnis von Fess abgelegt.
Sie können über [System] > [Plugins] in der Administrationsoberfläche installiert und verwaltet werden.

Entwicklung eines benutzerdefinierten Datenquellen-Plugins
===========================================================

In diesem Abschnitt wird der Entwicklungsprozess für ein Datenquellen-Plugin erläutert, wobei ein proprietäres internes Dokumentenmanagementsystem vorausgesetzt wird.

Projektstruktur
---------------

Erstellen Sie ein Maven-Projekt unter Bezugnahme auf ein bestehendes Data-Store-Plugin (z. B. fess-ds-git).

::

    fess-ds-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── java/
                └── org/codelibs/fess/ds/custom/
                    └── CustomDataStore.java

pom.xml-Konfiguration
----------------------

Geben Sie fess-parent als übergeordnetes POM an und konfigurieren Sie die erforderlichen Abhängigkeiten.

.. code-block:: xml

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.5.0</version>
    </parent>

    <artifactId>fess-ds-custom</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

Implementierung der Data-Store-Klasse
--------------------------------------

Der Kern eines Data-Store-Plugins ist die Klasse, die Daten abruft und Dokumente in Fess registriert.

Die wichtigsten Implementierungspunkte sind:

1. Verbindung und Authentifizierung mit dem externen System
2. Datenabruf (API-Aufrufe, Dateilesen usw.)
3. Konvertierung der abgerufenen Daten in das Fess-Dokumentformat
4. Registrierung der Dokumente

**Feld-Mapping**

Ordnen Sie die abgerufenen Daten den Fess-Feldern zu.
Die wichtigsten Felder sind:

- ``title``: Dokumenttitel
- ``url``: Dokument-URL (Linkziel in den Suchergebnissen)
- ``content``: Dokumentinhalt (Suchziel)
- ``mimetype``: MIME-Typ
- ``last_modified``: Datum und Uhrzeit der letzten Änderung

Build und Deployment
--------------------

::

    $ mvn clean package

Legen Sie die generierte JAR-Datei im Plugin-Verzeichnis von Fess ab und starten Sie Fess neu.

Entwicklung eines Ingest-Plugins
=================================

Ein Ingest-Plugin ist ein Mechanismus zur Verarbeitung und Transformation von Dokumenten, die durch Crawling gewonnen wurden, bevor sie im Index registriert werden.

Anwendungsfälle
-----------------

- Hinzufügen zusätzlicher Felder zu gecrawlten Dokumenten
- Bereinigung von Textinhalten (Entfernung unnötiger Zeichen)
- Anreicherung durch externe APIs (Übersetzung, Klassifizierung usw.)
- Log-Ausgabe (für Debugging)

Implementierungshinweise
-------------------------

In einem Ingest-Plugin greifen Sie auf die Dokumentdaten unmittelbar vor der Registrierung im Index zu und führen Transformationsverarbeitungen durch.

Beispielsweise können Sie eine Verarbeitung implementieren, die allen Dokumenten Organisationsnamen-Metadaten hinzufügt, oder eine Verarbeitung, die bestimmte Muster aus dem Textinhalt entfernt.

Entwicklung eines Theme-Plugins
=================================

Wenn Sie das Design der Suchoberfläche vollständig anpassen möchten, entwickeln Sie ein Theme-Plugin.

Theme-Struktur
--------------

Ein Theme-Plugin besteht aus JSP-Dateien, CSS, JavaScript und Bilddateien.

::

    fess-theme-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── resources/
                ├── css/
                ├── js/
                ├── images/
                └── view/
                    ├── index.jsp
                    ├── search.jsp
                    └── header.jsp

Passen Sie das Design an, indem Sie JSP und CSS unter Bezugnahme auf bestehende Themes ändern.

Best Practices für die Entwicklung
=====================================

Bestehende Plugins als Referenz
-------------------------------

Bei der Entwicklung eines neuen Plugins wird dringend empfohlen, den Quellcode bestehender Plugins als Referenz zu verwenden.
Der Quellcode aller Plugins ist im CodeLibs-GitHub-Repository verfügbar.

Beispielsweise sind ``fess-ds-git`` und ``fess-ds-slack`` gute Referenzen für die Entwicklung von Data-Store-Plugins.

Tests
-----

Testen Sie Plugins unter folgenden Gesichtspunkten:

- Verbindungstests mit externen Systemen
- Genauigkeit der Datentransformation
- Fehlerbehandlung (Verbindungsfehler, ungültige Daten usw.)
- Leistung (Verarbeitungszeit für große Datenmengen)

Versionskompatibilität
------------------------

Überprüfen Sie die Plugin-Kompatibilität beim Upgrade von Fess.
Bei einem Hauptversions-Upgrade von Fess kann es zu API-Änderungen kommen.

Zusammenfassung
===============

In diesem Artikel wurde die Plugin-Entwicklung für Fess erläutert.

- Überblick über die Plugin-Architektur (Data Store, Ingest, Theme, Script)
- Entwicklungsprozess für benutzerdefinierte Datenquellen-Plugins
- Dokumentverarbeitung mit Ingest-Plugins
- UI-Anpassung mit Theme-Plugins
- Best Practices für die Entwicklung

Durch Plugins können Sie Fess an organisationsspezifische Anforderungen anpassen.
Damit endet die Reihe zu Architektur und Skalierung. Ab dem nächsten Artikel befasst sich die Reihe KI und Suche der nächsten Generation mit den Grundlagen der semantischen Suche.

Referenzen
==========

- `Fess Plugin-Verwaltung <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
