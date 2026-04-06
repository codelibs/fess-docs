==============
Bauen und Testen
==============

Diese Seite erklärt, wie |Fess| gebaut wird, wie getestet wird
und wie Verteilungspakete erstellt werden.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Übersicht über das Build-System
==================

|Fess| verwendet Maven als Build-Tool.
Maven automatisiert die Verwaltung von Abhängigkeiten, Kompilierung, Tests und Paketierung.

pom.xml
-------

Dies ist die Maven-Konfigurationsdatei. Sie befindet sich im Stammverzeichnis des Projekts.

Hauptkonfiguration:

- Projektinformationen (groupId, artifactId, version)
- Abhängigkeitsbibliotheken
- Build-Plugins
- Profile

Grundlegende Build-Befehle
==================

Clean Build
------------

Löscht Build-Artefakte und baut dann neu:

.. code-block:: bash

    mvn clean compile

Erstellen von Paketen
--------------

Erstellt eine WAR-Datei und ein Distributions-Zip-Paket:

.. code-block:: bash

    mvn package

Die Artefakte werden im Verzeichnis ``target/`` generiert:

.. code-block:: text

    target/
    ├── fess.war
    └── releases/
        └── fess-{version}.zip

Vollständiger Build
--------

Führt Clean, Kompilierung, Tests und Paketierung vollständig aus:

.. code-block:: bash

    mvn clean package

Herunterladen von Abhängigkeiten
--------------------

Lädt Abhängigkeitsbibliotheken herunter:

.. code-block:: bash

    mvn dependency:resolve

Herunterladen der OpenSearch-Plugins
---------------------------------

Lädt OpenSearch und erforderliche Plugins herunter:

.. code-block:: bash

    mvn antrun:run

.. note::

   Führen Sie diesen Befehl beim Einrichten der Entwicklungsumgebung oder
   beim Aktualisieren von Plugins aus.

Tests
====

|Fess| implementiert Tests mit JUnit.

Ausführen von Unit-Tests
--------------

Alle Unit-Tests ausführen
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

Bestimmte Testklasse ausführen
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

Bestimmte Testmethode ausführen
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

Mehrere Testklassen ausführen
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

Tests überspringen
--------------

Wenn Sie beim Bauen Tests überspringen möchten:

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   Überspringen Sie während der Entwicklung keine Tests, sondern führen Sie sie immer aus.
   Stellen Sie vor dem Erstellen eines PR sicher, dass alle Tests bestehen.

Ausführen von Integrationstests
--------------

Für Integrationstests wird das Profil ``integrationTests`` verwendet.
Ein laufender |Fess|-Server und OpenSearch sind erforderlich:

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

.. note::

   Integrationstestklassen verwenden das Namensmuster ``*Tests.java`` (Unit-Tests verwenden ``*Test.java``).

Schreiben von Tests
============

Erstellen von Unit-Tests
--------------

Platzierung von Testklassen
~~~~~~~~~~~~~~~~

Platzieren Sie Testklassen unter ``src/test/java/``.
Die Paketstruktur sollte mit dem Hauptcode übereinstimmen.

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

Grundstruktur einer Testklasse
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: Testvoraussetzungen
            SearchService service = new SearchService();
            String query = "test";

            // When: Ausführung des Testobjekts
            SearchResponse response = service.search(query);

            // Then: Überprüfung der Ergebnisse
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

Test-Lebenszyklus
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // Einmal vor allen Tests ausführen
        }

        @BeforeEach
        void setUp() {
            // Vor jedem Test ausführen
        }

        @Test
        void testSomething() {
            // Test
        }

        @AfterEach
        void tearDown() {
            // Nach jedem Test ausführen
        }

        @AfterAll
        static void tearDownClass() {
            // Einmal nach allen Tests ausführen
        }
    }

Assertions
~~~~~~~~~~

Verwenden Sie JUnit 5-Assertions:

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // Gleichheit
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // Null-Prüfung
    assertNull(obj);
    assertNotNull(obj);

    // Boolean-Werte
    assertTrue(condition);
    assertFalse(condition);

    // Ausnahmen
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // Collections
    assertIterableEquals(expectedList, actualList);

Test-Coverage
--------------

Messen Sie die Test-Coverage mit JaCoCo:

.. code-block:: bash

    mvn clean test jacoco:report

Der Bericht wird unter ``target/site/jacoco/index.html`` generiert.

Code-Formatierung
================

|Fess| verwendet die folgenden Tools, um die Codequalität aufrechtzuerhalten.

Code-Formatter
------------------

Einheitlichen Codierungsstil sicherstellen:

.. code-block:: bash

    mvn formatter:format

Lizenz-Header
----------------

Lizenz-Header zu Quelldateien hinzufügen:

.. code-block:: bash

    mvn license:format

Prüfungen vor dem Commit
------------------

Führen Sie beide vor dem Commit aus:

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Erstellen von Verteilungspaketen
==================

Erstellen von Zip-Paketen
------------------

Erstellt ein Zip-Paket zur Verteilung:

.. code-block:: bash

    mvn clean package

Generierte Artefakte:

.. code-block:: text

    target/releases/
    └── fess-{version}.zip

Erstellen von RPM-Paketen
------------------

.. code-block:: bash

    mvn rpm:rpm

Erstellen von DEB-Paketen
------------------

.. code-block:: bash

    mvn jdeb:jdeb

Profile
==========

Maven-Profile ermöglichen das Umschalten zwischen Test-Typen.

build (Standard)
-----------------

Das Standardprofil. Führt Unit-Tests (``*Test.java``) aus:

.. code-block:: bash

    mvn package

integrationTests
----------------

Profil zum Ausführen von Integrationstests (``*Tests.java``):

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

CI/CD
=====

|Fess| verwendet GitHub Actions für CI/CD.

GitHub Actions
-------------

Konfigurationsdateien befinden sich im Verzeichnis ``.github/workflows/``.

Automatisch ausgeführte Prüfungen:

- Build
- Unit-Tests
- Paketerstellung

Lokale CI-Prüfungen
-----------------------

Vor dem Erstellen eines PR können Sie lokal die gleichen Prüfungen wie in der CI ausführen:

.. code-block:: bash

    mvn clean package

Fehlerbehebung
====================

Build-Fehler
----------

**Fehler: Download von Abhängigkeiten fehlgeschlagen**

.. code-block:: bash

    # Maven-Lokal-Repository löschen
    rm -rf ~/.m2/repository
    mvn clean compile

**Fehler: Speicher nicht ausreichend**

.. code-block:: bash

    # Maven-Speicher erhöhen
    export MAVEN_OPTS="-Xmx2g"
    mvn clean package

**Fehler: Java-Version ist veraltet**

Verwenden Sie Java 21 oder höher:

.. code-block:: bash

    java -version

Test-Fehler
----------

**Test läuft in Timeout**

Verlängern Sie die Test-Timeout-Zeit:

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch startet nicht**

Überprüfen Sie den Port und ändern Sie ihn, wenn er verwendet wird:

.. code-block:: bash

    lsof -i :9201

Abhängigkeitsprobleme
------------

**Abhängigkeitskonflikte**

Überprüfen Sie den Abhängigkeitsbaum:

.. code-block:: bash

    mvn dependency:tree

Schließen Sie bestimmte Abhängigkeiten aus:

.. code-block:: xml

    <dependency>
        <groupId>org.example</groupId>
        <artifactId>example-lib</artifactId>
        <version>1.0</version>
        <exclusions>
            <exclusion>
                <groupId>conflicting-lib</groupId>
                <artifactId>conflicting-lib</artifactId>
            </exclusion>
        </exclusions>
    </dependency>

Best Practices für Builds
========================

Regelmäßige Clean Builds
--------------------

Führen Sie regelmäßig Clean Builds aus, um Probleme mit dem Build-Cache zu vermeiden:

.. code-block:: bash

    mvn clean package

Ausführen von Tests
----------

Führen Sie vor dem Commit immer Tests aus:

.. code-block:: bash

    mvn test

Code-Formatierung ausführen
------------------

Führen Sie die Code-Formatierung vor dem Erstellen eines PR aus:

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Aktualisieren von Abhängigkeiten
------------

Aktualisieren Sie Abhängigkeiten regelmäßig:

.. code-block:: bash

    mvn versions:display-dependency-updates

Nutzung des Build-Cache
--------------------

Nutzen Sie den Maven-Cache, um die Build-Zeit zu verkürzen:

.. code-block:: bash

    # Überspringen, wenn bereits kompiliert
    mvn compile

Maven-Befehlsreferenz
========================

Häufig verwendete Befehle
--------------

.. code-block:: bash

    # Clean
    mvn clean

    # Kompilieren
    mvn compile

    # Testen
    mvn test

    # Paketieren
    mvn package

    # Installieren (im lokalen Repository registrieren)
    mvn install

    # Überprüfen (einschließlich Integrationstests)
    mvn verify

    # Abhängigkeiten auflösen
    mvn dependency:resolve

    # Abhängigkeitsbaum anzeigen
    mvn dependency:tree

    # Projektinformationen anzeigen
    mvn help:effective-pom

    # Code-Formatierung
    mvn formatter:format

    # Lizenz-Header hinzufügen
    mvn license:format

Nächste Schritte
==========

Nachdem Sie verstanden haben, wie gebaut und getestet wird, lesen Sie folgende Dokumentation:

- :doc:`workflow` - Entwicklungsworkflow
- :doc:`contributing` - Richtlinien für Beiträge
- :doc:`architecture` - Verständnis der Codebasis

Referenzmaterialien
======

- `Offizielle Maven-Dokumentation <https://maven.apache.org/guides/>`__
- `JUnit 5-Benutzerhandbuch <https://junit.org/junit5/docs/current/user-guide/>`__
- `JaCoCo-Dokumentation <https://www.jacoco.org/jacoco/trunk/doc/>`__
