================================================
Open-Source-Volltextsuche-Server - |Fess| Entwicklungsübersicht
================================================

Diese Seite bietet einen Überblick über die |Fess|-Entwicklung und grundlegende Informationen für den Einstieg.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Übersicht
====

|Fess| ist ein in Java entwickelter Open-Source-Volltextsuche-Server.
Ziel ist es, Enterprise-Suche einfach aufzubauen zu können,
und bietet leistungsstarke Suchfunktionen und eine benutzerfreundliche Verwaltungsoberfläche.

Merkmale von |Fess|
-------------

- **Einfaches Setup**: Kann sofort gestartet werden, wenn eine Java-Umgebung vorhanden ist
- **Leistungsstarker Crawler**: Unterstützt verschiedene Datenquellen wie Websites, Dateisysteme, Datenbanken
- **Japanische Unterstützung**: Optimiert für japanische Volltextsuche
- **Erweiterbarkeit**: Funktionserweiterung durch Plugins möglich
- **REST-API**: Suchfunktionen können von anderen Anwendungen genutzt werden

Technologie-Stack
==========

|Fess| wird unter Verwendung folgender Technologien entwickelt.

Zielversion
------------

Diese Dokumentation richtet sich an folgende Versionen:

- **Fess**: 15.3.0
- **Java**: 21 oder höher
- **OpenSearch**: 3.3.0
- **Maven**: 3.x

Haupttechnologien und Frameworks
----------------------

Java 21
~~~~~~~

|Fess| ist eine Anwendung, die mit Java 21 oder höher läuft.
Sie nutzt die neuesten Java-Funktionen und verbessert Performance und Wartbarkeit.

- **Empfohlen**: Eclipse Temurin 21 (ehemals AdoptOpenJDK)
- **Mindestversion**: Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ ist ein Framework,
das in der Webanwendungsschicht von |Fess| verwendet wird.

**Hauptfunktionen:**

- DI (Dependency Injection)-Container
- Action-basiertes Web-Framework
- Validierung
- Nachrichtenverwaltung
- Konfigurationsverwaltung

**Lernressourcen:**

- `Offizielle LastaFlute-Dokumentation <https://github.com/lastaflute/lastaflute>`__
- Praktische Verwendung durch Lesen des Fess-Codes

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ ist ein O/R-Mapping-Tool
für den Datenbankzugriff.
|Fess| verwendet es, um Java-Code automatisch aus dem OpenSearch-Schema zu generieren.

**Hauptfunktionen:**

- Typsicherer SQL-Builder
- Automatische Code-Generierung aus Schema
- Automatische Generierung von Datenbankdokumentation

**Lernressourcen:**

- `Offizielle DBFlute-Website <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ ist eine verteilte Such- und Analyse-Engine,
die als Suchmaschine für |Fess| verwendet wird.

**Unterstützte Version**: OpenSearch 3.3.0

**Erforderliche Plugins:**

- opensearch-analysis-fess: Fess-spezifisches morphologisches Analyse-Plugin
- opensearch-analysis-extension: Zusätzliche Sprachanalysefunktionen
- opensearch-minhash: Erkennung ähnlicher Dokumente
- opensearch-configsync: Synchronisation der Konfiguration

**Lernressourcen:**

- `OpenSearch-Dokumentation <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven wird als Build-Tool für |Fess| verwendet.

**Hauptverwendung:**

- Verwaltung von Abhängigkeitsbibliotheken
- Ausführung von Build-Verarbeitung
- Ausführung von Tests
- Erstellung von Paketen

Entwicklungstools
========

Empfohlene Entwicklungsumgebung
----------------

Eclipse
~~~~~~~

Die offizielle Dokumentation erklärt die Entwicklungsmethode mit Eclipse.

**Empfohlene Version**: Eclipse 2023-09 oder höher

**Erforderliche Plugins:**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

Entwicklung ist auch mit IntelliJ IDEA möglich.

**Empfohlene Edition**: Community Edition oder Ultimate Edition

**Erforderliche Funktionen:**

- Maven-Unterstützung (standardmäßig enthalten)
- Java-Unterstützung

VS Code
~~~~~~~

VS Code kann auch für leichte Entwicklung verwendet werden.

**Erforderliche Erweiterungen:**

- Java Extension Pack
- Maven for Java

Versionskontrolle
~~~~~~~~~~~~

- **Git**: Quellcodeverwaltung
- **GitHub**: Repository-Hosting, Issue-Verwaltung, Pull Requests

Erforderliches Wissen
========

Grundkenntnisse
--------

Für die |Fess|-Entwicklung sind folgende Kenntnisse erforderlich:

**Erforderlich**

- **Java-Programmierung**: Klassen, Schnittstellen, Generics, Lambda-Ausdrücke usw.
- **Objektorientierung**: Vererbung, Polymorphismus, Kapselung
- **Maven**: Grundlegende Befehle und Verständnis von pom.xml
- **Git**: clone, commit, push, pull, branch, merge usw.

**Empfohlen**

- **LastaFlute**: Konzepte von Action, Form, Service
- **DBFlute**: Verwendung von Behavior, ConditionBean
- **OpenSearch/Elasticsearch**: Grundlagen von Index, Mapping, Query
- **Webentwicklung**: HTML, CSS, JavaScript (besonders bei Frontend-Entwicklung)
- **Linux-Befehle**: Entwicklung/Debugging in Server-Umgebung

Lernressourcen
----------

Für den ersten Einstieg in die |Fess|-Entwicklung sind folgende Ressourcen hilfreich:

Offizielle Dokumentation
~~~~~~~~~~~~~~

- `Fess-Benutzerhandbuch <https://fess.codelibs.org/ja/>`__
- `Fess-Administratorhandbuch <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

Community
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Fragen und Diskussionen
- `Issue-Tracker <https://github.com/codelibs/fess/issues>`__: Fehlerberichte und Feature-Anfragen
- `Fess-Forum <https://discuss.codelibs.org/c/FessJA>`__: Japanisches Community-Forum

Quellcode
~~~~~~~~~~

Das Lesen des tatsächlichen Codes ist die effektivste Lernmethode:

- Beginnen Sie zunächst mit dem Lesen kleiner Funktionen
- Verfolgen Sie das Verhalten des Codes mit dem Debugger
- Konsultieren Sie vorhandenen Testcode

Grundlegender Entwicklungsablauf
==============

Die |Fess|-Entwicklung folgt im Allgemeinen diesem Ablauf:

1. **Überprüfung/Erstellung von Issues**

   Überprüfen Sie Issues auf GitHub und entscheiden Sie, woran Sie arbeiten möchten.
   Erstellen Sie bei neuen Funktionen oder Fehlerbehebungen ein Issue.

2. **Erstellung eines Branches**

   Erstellen Sie einen Arbeits-Branch:

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **Codierung**

   Implementieren Sie Funktionen oder beheben Sie Fehler.

4. **Tests**

   Erstellen und führen Sie Unit-Tests aus und überprüfen Sie, dass Änderungen korrekt funktionieren.

5. **Commit**

   Committen Sie Änderungen:

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **Pull Request**

   Pushen Sie zu GitHub und erstellen Sie einen Pull Request:

   .. code-block:: bash

       git push origin feature/my-new-feature

Weitere Details finden Sie unter :doc:`workflow`.

Überblick über die Projektstruktur
==================

Der Quellcode von |Fess| hat folgende Struktur:

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # Webanwendungsschicht
    │   │   │       │   ├── web/       # Suchseite
    │   │   │       │   └── service/   # Service-Schicht
    │   │   │       ├── crawler/       # Crawler-Funktion
    │   │   │       ├── es/            # OpenSearch-bezogen
    │   │   │       ├── helper/        # Hilfsklassen
    │   │   │       ├── job/           # Job-Verarbeitung
    │   │   │       ├── util/          # Utilities
    │   │   │       └── FessBoot.java  # Startklasse
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # JSP-Dateien
    │   └── test/
    │       └── java/                  # Testcode
    ├── pom.xml                        # Maven-Konfigurationsdatei
    └── README.md

Hauptpakete
--------------

app
~~~

Code der Webanwendungsschicht.
Enthält Actions, Forms, Services der Verwaltungs- und Suchseite.

crawler
~~~~~~~

Code der Datensammlungsfunktion.
Web-Crawler, File-Crawler, Datastore-Crawler usw.

es
~~

Code zur Integration mit OpenSearch.
Index-Operationen, Aufbau von Suchabfragen usw.

helper
~~~~~~

In der gesamten Anwendung verwendete Hilfsklassen.

job
~~~

Code für geplant ausgeführte Jobs.
Crawl-Job, Index-Optimierungs-Job usw.

Weitere Details finden Sie unter :doc:`architecture`.

Schnellstart der Entwicklungsumgebung
=======================

Erklärt, wie man mit minimalen Schritten eine Entwicklungsumgebung einrichtet und |Fess| ausführt.

Voraussetzungen
--------

- Java 21 oder höher ist installiert
- Git ist installiert
- Maven 3.x ist installiert

Schritte
----

1. **Repository klonen**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **OpenSearch-Plugins herunterladen**

   .. code-block:: bash

       mvn antrun:run

3. **Ausführen**

   Von Maven ausführen:

   .. code-block:: bash

       mvn compile exec:java

   Oder führen Sie die Klasse ``org.codelibs.fess.FessBoot`` von der IDE (Eclipse, IntelliJ IDEA usw.) aus.

4. **Zugriff**

   Greifen Sie im Browser auf Folgendes zu:

   - Suchseite: http://localhost:8080/
   - Verwaltungsseite: http://localhost:8080/admin/
     - Standardbenutzer: admin / admin

Detaillierte Setup-Schritte finden Sie unter :doc:`setup`.

Entwicklungstipps
==========

Debug-Ausführung
----------

Bei Debug-Ausführung in der IDE führen Sie die Klasse ``FessBoot`` aus.
Durch Setzen von Breakpoints können Sie das Verhalten des Codes im Detail verfolgen.

Hot Deploy
------------

LastaFlute kann einige Änderungen ohne Neustart widerspiegeln.
Allerdings erfordern Änderungen der Klassenstruktur usw. einen Neustart.

Überprüfung von Logs
--------

Logs werden im Verzeichnis ``target/fess/logs/`` ausgegeben.
Überprüfen Sie bei Problemen die Logdateien.

Betrieb von OpenSearch
----------------

Das eingebettete OpenSearch wird unter ``target/fess/es/`` platziert.
Sie können auch direkt die OpenSearch-API zum Debuggen aufrufen:

.. code-block:: bash

    # Indizes überprüfen
    curl -X GET http://localhost:9201/_cat/indices?v

    # Dokumente durchsuchen
    curl -X GET http://localhost:9201/fess.search/_search?pretty

Community und Support
==================

Fragen und Beratung
--------

Bei Fragen oder Beratungsbedarf während der Entwicklung nutzen Sie Folgendes:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Allgemeine Fragen und Diskussionen
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__: Fehlerberichte und Feature-Anfragen
- `Fess-Forum <https://discuss.codelibs.org/c/FessJA>`__: Japanisches Forum

Beitragsmethode
--------

Informationen zum Beitragen zu |Fess| finden Sie unter :doc:`contributing`.

Nächste Schritte
==========

Wenn Sie bereit sind, die Entwicklungsumgebung einzurichten, fahren Sie mit :doc:`setup` fort.

Weitere Informationen finden Sie auch in folgender Dokumentation:

- :doc:`architecture` - Architektur und Codestruktur
- :doc:`workflow` - Entwicklungsworkflow
- :doc:`building` - Build und Test
- :doc:`contributing` - Leitfaden für Beiträge

Referenzmaterialien
========

Offizielle Ressourcen
----------

- `Offizielle Fess-Website <https://fess.codelibs.org/ja/>`__
- `GitHub-Repository <https://github.com/codelibs/fess>`__
- `Download-Seite <https://fess.codelibs.org/ja/downloads.html>`__

Technische Dokumentation
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Community
----------

- `Fess-Forum <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
