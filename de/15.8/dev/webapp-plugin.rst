==================================
Webanwendungs-Plugin
==================================

Übersicht
=========

Webanwendungs-Plugins (``fess-webapp-*``) sind Plugins, die die Webanwendung
von |Fess| erweitern. Anders als andere Plugin-Typen fügen sie nicht direkt
Action-Klassen oder JSPs hinzu, sondern erweitern die Funktionalität, indem
sie dem DI-Container (Lasta Di) **Komponenten hinzufügen oder ersetzen**.
Typische Anwendungsfälle sind:

- Hinzufügen neuer Komponenten (z. B. Helper, Services)
- Ersetzen von Komponenten des |Fess|-Kerns (durch Unterklassenbildung)
- Hinzufügen von REST-API-Endpunkten (``WebApiManager``)
- Erweiterung des Suchverhaltens (Query-Commands, Rank-Fusion usw.)

.. note::

   Webanwendungs-Plugins werden als JAR-Datei ausgeliefert; ihre Klassen und
   DI-Konfigurationsdateien werden in den Klassenpfad der Webanwendung von
   |Fess| geladen. Sie fügen keine JSP-Views hinzu. Wenn Sie das Design der
   Suchoberfläche anpassen möchten, lesen Sie :doc:`theme-development`.

Grundstruktur
=============

Am Beispiel von
`fess-webapp-example <https://github.com/codelibs/fess-webapp-example>`__,
der Implementierungsvorlage für Webanwendungs-Plugins, besteht ein Plugin
aus einer „Implementierungsklasse" und einer „DI-Registrierungsdatei":

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # Hinzuzufügende Komponente
        │   └── CustomSystemHelper.java   # Ersetzen einer Kernkomponente
        └── resources/
            ├── app++.xml                 # Hinzufügen einer Komponente (Merge)
            └── fess+systemHelper.xml     # Ersetzen einer Komponente

.. note::

   Das Paket der Implementierungsklasse folgt dem Schema
   ``org.codelibs.fess.webapp.<Plugin-Name>``. Die DI-Konfigurationsdateien
   werden unter ``src/main/resources/`` abgelegt. Anders als bei
   DataStore-Plugins enthält das Projekt kein ``src/main/webapp/`` und
   keine JSPs.

pom.xml und Manifest
====================

Webanwendungs-Plugins werden als jar mit ``fess-parent`` als übergeordnetem
POM gebaut. Bibliotheken wie ``fess`` und ``opensearch``, die zur Laufzeit
vom |Fess|-Kern bereitgestellt werden, werden mit dem Scope ``provided``
deklariert. Zur Laufzeit benötigte Bibliotheken wie ``lastaflute``,
``dbflute-runtime`` und ``corelib`` werden mit dem normalen Scope
deklariert.

Das Wichtigste bei einem Webanwendungs-Plugin ist, dem JAR-Manifest den
Eintrag ``Fess-WebAppJar: true`` hinzuzufügen. Durch diese Deklaration
mountet |Fess| die Klassen und DI-Konfigurationsdateien des Plugins in den
Klassenlader der Webanwendung. Diese Einstellung wird über
``maven-jar-plugin`` vorgenommen:

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-jar-plugin</artifactId>
                <configuration>
                    <archive>
                        <manifestEntries>
                            <Fess-WebAppJar>true</Fess-WebAppJar>
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>

.. warning::

   Wird ``Fess-WebAppJar: true`` nicht gesetzt, werden die Klassen und
   DI-Konfigurationsdateien des Plugins nicht in den Klassenpfad der
   Webanwendung geladen, und das Hinzufügen bzw. Ersetzen von Komponenten
   wird nicht wirksam.

Den vollständigen Aufbau der pom.xml (übergeordnetes POM, Deklaration von
Abhängigkeiten usw.) finden Sie unter :doc:`plugin-architecture`.

Erweiterungsmuster
==================

Hinzufügen von Komponenten (app++.xml)
--------------------------------------

Die grundlegendste Erweiterungsmethode besteht darin, eigene Komponenten
hinzuzufügen. Lasta Di **merged** die ``app++.xml`` im Klassenpfad in den
``app``-Namensraum, der aus der ``app.xml`` des |Fess|-Kerns aufgebaut wird
(das ``++`` am Ende ist die Konvention für ein zusammenführendes Merge).
Da die hinzuzufügenden Komponenten Namen verwenden, die im |Fess|-Kern
nicht existieren, wird nichts überschrieben.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

Bei der Implementierung der Komponente wird für die Initialisierung
``@PostConstruct`` verwendet; Komponenten des |Fess|-Kerns werden über
``ComponentUtil`` abgerufen und wiederverwendet (nicht kopiert oder
überschrieben):

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // Initialisierungslogik, die nach der Erzeugung durch DI einmalig aufgerufen wird
        }

        public String getPluginLabel() {
            // Wiederverwendung des Core-SystemHelper zum Ermitteln der laufenden Fess-Version
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   Ziehen Sie zunächst dieses „Hinzufügen von Komponenten" in Betracht.
   Solange keine Kernfunktionen geändert werden müssen, ist dies sicherer
   und besser wartbar als ein Ersetzen.

Ersetzen von Kernkomponenten (fess+componentName.xml)
------------------------------------------------------

Wenn Sie das Verhalten einer Komponente des |Fess|-Kerns ändern möchten,
bilden Sie eine Unterklasse der Zielklasse und registrieren diese in einer
DI-Konfigurationsdatei mit dem Namen ``<baseDicon>+<componentName>.xml``
**erneut unter demselben Komponentennamen**. Da ``systemHelper``
beispielsweise in der ``fess.xml`` des |Fess|-Kerns deklariert ist, lautet
die Ersetzungsdatei ``fess+systemHelper.xml`` (nicht
``app+systemHelper.xml``).

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import java.nio.file.Path;

    import org.codelibs.fess.helper.SystemHelper;

    public class CustomSystemHelper extends SystemHelper {

        @Override
        protected void parseProjectProperties(final Path propPath) {
            try {
                super.parseProjectProperties(propPath);
            } catch (final Exception e) {
                // eigene Verarbeitung
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   Das Ersetzen (einzelnes ``+``) ersetzt die Komponentendefinition
   **vollständig**. Aus diesem Grund müssen in der Ersetzungsdatei alle
   ``<postConstruct>``-Einträge, die in der Kerndefinition vorhanden sind,
   erneut angegeben werden. Wenn Sie beispielsweise ``systemHelper``
   ersetzen, müssen Sie die Zuordnung der Design-JSP-Namen
   (``addDesignJspFileName``) vollständig aus der ``fess.xml`` des Kerns
   kopieren und übernehmen. Diese müssen mit jedem |Fess|-Release
   synchronisiert werden; fehlt ein Eintrag, können bestimmte Bildschirme
   (z. B. ``chat`` / ``login``) nicht mehr aufgelöst werden. Dieser
   Wartungsaufwand ist der Grund, warum das Hinzufügen dem Ersetzen
   vorgezogen werden sollte.

Hinzufügen einer REST-API (fess_api++.xml)
-------------------------------------------

Um einen neuen REST-API-Endpunkt hinzuzufügen, implementieren Sie
``WebApiManager``. Erben Sie von ``BaseApiManager`` und registrieren Sie
sich selbst in ``@PostConstruct`` bei der ``WebApiManagerFactory``. Der
registrierte API-Manager wird bei jeder Anfrage von ``WebApiFilter``
aufgerufen. Registrieren Sie die Komponente in ``fess_api++.xml``:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleApiManager"
            class="org.codelibs.fess.webapp.example.api.ExampleApiManager">
        </component>
    </components>

.. code-block:: java

    package org.codelibs.fess.webapp.example.api;

    import java.io.IOException;

    import org.codelibs.fess.api.BaseApiManager;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;
    import jakarta.servlet.FilterChain;
    import jakarta.servlet.ServletException;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;

    public class ExampleApiManager extends BaseApiManager {

        public ExampleApiManager() {
            // Pfadpräfix, das von diesem Manager verarbeitet wird
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // Prüft, ob dieser Manager die Anfrage verarbeiten soll
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // Verarbeitung der Anfrage und Schreiben der Antwort
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // Setzen der Antwort-Header (bei Bedarf)
        }
    }

Als Implementierungsbeispiele bieten sich
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__,
das ``/api/v1`` bereitstellt, sowie
`fess-webapp-classic-api <https://github.com/codelibs/fess-webapp-classic-api>`__,
das ``/json`` / ``/suggest`` bereitstellt, als Referenz an.

Anpassung der Suchoberfläche
============================

Webanwendungs-Plugins können keine JSP-Views hinzufügen. JSP-Views befinden
sich unter ``WEB-INF/view/`` im WAR des |Fess|-Kerns, während das
Plugin-JAR in den Klassenpfad (``WEB-INF/classes``) gemountet wird. Wenn
Sie das Design der Suchoberfläche ändern möchten, nutzen Sie eine der
folgenden Möglichkeiten:

- **Theme**: Passt das Design der Suchoberfläche (HTML/CSS/JavaScript) an.
  Siehe :doc:`theme-development`.
- **Ersetzen von systemHelper**: Über das oben beschriebene „Ersetzen von
  Kernkomponenten" lässt sich die Zuordnung der Design-JSP-Namen ändern
  (die JSP-Dateien selbst werden jedoch weiterhin vom |Fess|-Kern
  bereitgestellt).

Build und Installation
=======================

::

    mvn clean package

Im Verzeichnis ``target/`` wird eine JAR-Datei erzeugt (z. B.
``fess-webapp-example-15.8.0.jar``). Installieren Sie das erzeugte JAR
entweder über die Administrationsoberfläche, oder legen Sie es im
Verzeichnis ``app/WEB-INF/plugin/`` ab und starten Sie |Fess| neu. Details
zum Installationsvorgang finden Sie unter :doc:`../admin/plugin-guide`.

Beispiele veröffentlichter Plugins
==================================

Im |Fess|-Projekt sind die folgenden Webanwendungs-Plugins veröffentlicht.
Sie sind als Referenz für die Entwicklung auf
`GitHub <https://github.com/codelibs>`__ verfügbar:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Plugin
     - Beschreibung
   * - ``fess-webapp-example``
     - Implementierungsvorlage für Plugins
   * - ``fess-webapp-v1-api``
     - ``/api/v1`` REST-API
   * - ``fess-webapp-classic-api``
     - ``/json`` / ``/suggest`` Legacy-REST-API
   * - ``fess-webapp-mcp``
     - MCP-Server (Model Context Protocol)
   * - ``fess-webapp-semantic-search``
     - Neuronale Suche/Vektorsuche
   * - ``fess-webapp-multimodal``
     - Multimodale Suche (Bild und Text)

Referenzinformationen
=====================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`theme-development` - Theme-Anpassung
- :doc:`../admin/plugin-guide` - Plugin-Installation
- :doc:`overview` - Entwicklerdokumentation Übersicht

