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

Erstellt eine ausführbare JAR-Datei:

.. code-block:: bash

    mvn package

Die Artefakte werden im Verzeichnis ``target/`` generiert:

.. code-block:: text

    target/
    ├── fess-15.3.x.jar
    └── fess-15.3.x/

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

Führt alle Tests einschließlich Integrationstests aus:

.. code-block:: bash

    mvn verify

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

Verwendung von Mocks
~~~~~~~~~~

Verwenden Sie Mockito zum Erstellen von Mocks:

.. code-block:: java

    import static org.mockito.Mockito.*;
    import org.mockito.Mock;
    import org.mockito.junit.jupiter.MockitoExtension;
    import org.junit.jupiter.api.extension.ExtendWith;

    @ExtendWith(MockitoExtension.class)
    public class SearchServiceTest {

        @Mock
        private SearchEngineClient searchEngineClient;

        @Test
        public void testSearch() {
            // Mock-Konfiguration
            when(searchEngineClient.search(anyString()))
                .thenReturn(new SearchResponse());

            // Test ausführen
            SearchService service = new SearchService();
            service.setSearchEngineClient(searchEngineClient);
            SearchResponse response = service.search("test");

            // Überprüfung
            assertNotNull(response);
            verify(searchEngineClient, times(1)).search("test");
        }
    }

Test-Coverage
--------------

Messen Sie die Test-Coverage mit JaCoCo:

.. code-block:: bash

    mvn clean test jacoco:report

Der Bericht wird unter ``target/site/jacoco/index.html`` generiert.

Code-Qualitätsprüfung
================

Checkstyle
----------

Überprüft den Codierungsstil:

.. code-block:: bash

    mvn checkstyle:check

Die Konfigurationsdatei befindet sich unter ``checkstyle.xml``.

SpotBugs
--------

Erkennt potenzielle Bugs:

.. code-block:: bash

    mvn spotbugs:check

PMD
---

Erkennt Code-Qualitätsprobleme:

.. code-block:: bash

    mvn pmd:check

Alle Prüfungen ausführen
--------------------

.. code-block:: bash

    mvn clean verify checkstyle:check spotbugs:check pmd:check

Erstellen von Verteilungspaketen
==================

Erstellen von Release-Paketen
--------------------

Erstellt Pakete für die Verteilung:

.. code-block:: bash

    mvn clean package

Generierte Artefakte:

.. code-block:: text

    target/releases/
    ├── fess-15.3.x.tar.gz      # Für Linux/macOS
    ├── fess-15.3.x.zip         # Für Windows
    ├── fess-15.3.x.rpm         # RPM-Paket
    └── fess-15.3.x.deb         # DEB-Paket

Erstellen von Docker-Images
-------------------

Erstellt ein Docker-Image:

.. code-block:: bash

    mvn package docker:build

Generiertes Image:

.. code-block:: bash

    docker images | grep fess

Profile
==========

Sie können Maven-Profile verwenden, um verschiedene Einstellungen pro Umgebung anzuwenden.

Entwicklungsprofil
--------------

Baut mit Entwicklungseinstellungen:

.. code-block:: bash

    mvn package -Pdev

Produktionsprofil
--------------

Baut mit Produktionseinstellungen:

.. code-block:: bash

    mvn package -Pprod

Schneller Build
--------

Überspringt Tests und Prüfungen für schnelles Bauen:

.. code-block:: bash

    mvn package -Pfast

.. warning::

   Schnelle Builds sind nur zur Überprüfung während der Entwicklung gedacht.
   Führen Sie vor dem Erstellen eines PR unbedingt einen vollständigen Build aus.

CI/CD
=====

|Fess| verwendet GitHub Actions für CI/CD.

GitHub Actions
-------------

Konfigurationsdateien befinden sich im Verzeichnis ``.github/workflows/``.

Automatisch ausgeführte Prüfungen:

- Build
- Unit-Tests
- Integrationstests
- Code-Stil-Prüfung
- Code-Qualitätsprüfung

Lokale CI-Prüfungen
-----------------------

Vor dem Erstellen eines PR können Sie lokal die gleichen Prüfungen wie in der CI ausführen:

.. code-block:: bash

    mvn clean verify checkstyle:check

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
    export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512m"
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

Code-Qualitätsprüfung
------------------

Überprüfen Sie die Code-Qualität vor dem Erstellen eines PR:

.. code-block:: bash

    mvn checkstyle:check spotbugs:check

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
- `Mockito-Dokumentation <https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html>`__
- `JaCoCo-Dokumentation <https://www.jacoco.org/jacoco/trunk/doc/>`__
