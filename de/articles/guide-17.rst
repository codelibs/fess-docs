============================================================
Teil 17: Suche mit Plugins erweitern -- Implementierung benutzerdefinierter Datenquellen und Ingest-Pipelines
============================================================

Einleitung
==========

Fess unterstuetzt standardmaessig viele Datenquellen. Um jedoch unternehmensspezifische Systeme und Datenformate zu unterstuetzen, kann eine Erweiterung durch Plugins erforderlich sein.

In diesem Artikel wird die Plugin-Architektur von Fess erlaeutert und die Implementierung von benutzerdefinierten Datenquellen-Plugins und Ingest-Plugins vorgestellt.

Zielgruppe
==========

- Personen, die Fess mit eigenen Datenquellen verbinden moechten
- Java-Entwickler, die sich fuer die Plugin-Entwicklung interessieren
- Personen, die die interne Architektur von Fess verstehen moechten

Plugin-Architektur
===================

Fess bietet die folgenden Arten von Plugins.

.. list-table:: Plugin-Typen
   :header-rows: 1
   :widths: 25 35 40

   * - Typ
     - Rolle
     - Beispiele
   * - Data Store (fess-ds-*)
     - Daten aus externen Datenquellen abrufen
     - Slack, Salesforce, DB
   * - Ingest (fess-ingest-*)
     - Gecrawlte Daten verarbeiten und transformieren
     - Example
   * - Theme (fess-theme-*)
     - Design der Suchoberflaeche
     - Simple, Code Search
   * - Script (fess-script-*)
     - Unterstuetzung von Skriptsprachen
     - OGNL
   * - Web App (fess-webapp-*)
     - Erweiterungen fuer Webanwendungen
     - MCP Server

Plugin-Bereitstellung
---------------------

Plugins werden als JAR-Dateien bereitgestellt und im Plugin-Verzeichnis von Fess abgelegt.
Sie koennen ueber [System] > [Plugins] in der Administrationsoberflaeche installiert und verwaltet werden.

Entwicklung eines benutzerdefinierten Datenquellen-Plugins
===========================================================

In diesem Abschnitt wird der Entwicklungsprozess fuer ein Datenquellen-Plugin erlaeutert, wobei ein proprietaeres internes Dokumentenmanagementsystem vorausgesetzt wird.

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

Geben Sie fess-parent als uebergeordnetes POM an und konfigurieren Sie die erforderlichen Abhaengigkeiten.

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
- ``last_modified``: Datum und Uhrzeit der letzten Aenderung

Build und Deployment
--------------------

::

    $ mvn clean package

Legen Sie die generierte JAR-Datei im Plugin-Verzeichnis von Fess ab und starten Sie Fess neu.

Entwicklung eines Ingest-Plugins
=================================

Ein Ingest-Plugin ist ein Mechanismus zur Verarbeitung und Transformation von Dokumenten, die durch Crawling gewonnen wurden, bevor sie im Index registriert werden.

Anwendungsfaelle
-----------------

- Hinzufuegen zusaetzlicher Felder zu gecrawlten Dokumenten
- Bereinigung von Textinhalten (Entfernung unnoetiger Zeichen)
- Anreicherung durch externe APIs (Uebersetzung, Klassifizierung usw.)
- Log-Ausgabe (fuer Debugging)

Implementierungshinweise
-------------------------

In einem Ingest-Plugin greifen Sie auf die Dokumentdaten unmittelbar vor der Registrierung im Index zu und fuehren Transformationsverarbeitungen durch.

Beispielsweise koennen Sie eine Verarbeitung implementieren, die allen Dokumenten Organisationsnamen-Metadaten hinzufuegt, oder eine Verarbeitung, die bestimmte Muster aus dem Textinhalt entfernt.

Entwicklung eines Theme-Plugins
=================================

Wenn Sie das Design der Suchoberflaeche vollstaendig anpassen moechten, entwickeln Sie ein Theme-Plugin.

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

Passen Sie das Design an, indem Sie JSP und CSS unter Bezugnahme auf bestehende Themes aendern.

Best Practices fuer die Entwicklung
=====================================

Bestehende Plugins als Referenz
-------------------------------

Bei der Entwicklung eines neuen Plugins wird dringend empfohlen, den Quellcode bestehender Plugins als Referenz zu verwenden.
Der Quellcode aller Plugins ist im CodeLibs-GitHub-Repository verfuegbar.

Beispielsweise sind ``fess-ds-git`` und ``fess-ds-slack`` gute Referenzen fuer die Entwicklung von Data-Store-Plugins.

Tests
-----

Testen Sie Plugins unter folgenden Gesichtspunkten:

- Verbindungstests mit externen Systemen
- Genauigkeit der Datentransformation
- Fehlerbehandlung (Verbindungsfehler, ungueltige Daten usw.)
- Leistung (Verarbeitungszeit fuer grosse Datenmengen)

Versionskompatibilitaet
------------------------

Ueberpruefen Sie die Plugin-Kompatibilitaet beim Upgrade von Fess.
Bei einem Hauptversions-Upgrade von Fess kann es zu API-Aenderungen kommen.

Zusammenfassung
===============

In diesem Artikel wurde die Plugin-Entwicklung fuer Fess erlaeutert.

- Ueberblick ueber die Plugin-Architektur (Data Store, Ingest, Theme, Script)
- Entwicklungsprozess fuer benutzerdefinierte Datenquellen-Plugins
- Dokumentverarbeitung mit Ingest-Plugins
- UI-Anpassung mit Theme-Plugins
- Best Practices fuer die Entwicklung

Durch Plugins koennen Sie Fess an organisationsspezifische Anforderungen anpassen.
Damit endet die Reihe zu Architektur und Skalierung. Ab dem naechsten Artikel befasst sich die Reihe KI und Suche der naechsten Generation mit den Grundlagen der semantischen Suche.

Referenzen
==========

- `Fess Plugin-Verwaltung <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
