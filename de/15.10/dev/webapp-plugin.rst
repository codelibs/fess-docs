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
   erneut angegeben werden (z. B. ``queryHelper`` in ``app.xml``). Diese
   müssen mit jedem |Fess|-Release synchronisiert werden. Ruft die Datei
   weiterhin eine Methode auf, die aus dem Kern entfernt wurde, schlägt die
   Initialisierung der Komponentendefinition mit einer
   ``BeanMethodNotFoundException`` fehl. So wurde in 15.9
   ``addDesignJspFileName`` aus ``systemHelper`` entfernt; eine
   Ersetzungsdatei, die sie noch aufruft, schlägt fehl. Dieser
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

.. _webapp-plugin-password-encoder:

Hinzufügen eines Passwort-Hash-Algorithmus (fess++.xml)
-------------------------------------------------------

Der Hash des Passworts eines lokalen Benutzers wird von einer Komponente erzeugt. Ein gespeichertes Passwort wird als ``{id}hash`` geschrieben. |Fess| nimmt die ``id`` des gespeicherten Werts und für ein neues Passwort den Wert von ``app.password.algorithm`` (standardmäßig ``bcrypt``) und sucht die DI-Komponente mit dem Namen ``<id>PasswordEncoder``, auf dieselbe Weise, wie ``<sso.type>Authenticator`` und ``<storage.type>StorageClient`` aufgelöst werden. |Fess| registriert ``bcryptPasswordEncoder`` selbst. Um einen Algorithmus hinzuzufügen, implementieren Sie ``org.codelibs.fess.crypto.password.PasswordEncoder`` und registrieren die Klasse in ``fess++.xml``, die Lasta Di in die ``fess.xml`` des |Fess|-Kerns einmischt:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="argon2PasswordEncoder"
            class="com.example.Argon2PasswordEncoder">
        </component>
    </components>

Das Interface hat die folgenden Methoden:

.. list-table:: Methoden von PasswordEncoder
   :header-rows: 1
   :widths: 35 65

   * - Methode
     - Beschreibung
   * - ``String encode(String rawPassword)``
     - Berechnet den Hash eines Passworts. Das Ergebnis wird hinter dem Präfix ``{id}`` gespeichert, das |Fess| ergänzt. Werfen Sie ``IllegalArgumentException`` für ein Passwort, das sich nicht originalgetreu hashen lässt; die Meldung darf das Passwort nicht enthalten.
   * - ``boolean matches(String rawPassword, String encodedPassword)``
     - Prüft ein Passwort gegen einen Hash, den dieser Encoder erzeugt hat. Geben Sie ``false`` für ein falsches Passwort und für einen fehlerhaften Hash zurück.
   * - ``boolean needsUpgrade(String encodedPassword)``
     - Optional (Standard ``false``). Gibt an, ob ein gespeicherter Hash schwächer ist als das, was ``encode`` jetzt erzeugt, sodass er bei der nächsten Anmeldung seines Benutzers neu berechnet wird. BCrypt gibt ``true`` zurück, wenn der Kostenfaktor unter ``app.password.bcrypt.cost`` liegt.
   * - ``int getMaxPasswordBytes()``
     - Optional (Standard ``0``, keine Begrenzung). Das längste Passwort in UTF-8-Bytes, das ``encode`` akzeptiert. BCrypt gibt ``72`` zurück.
   * - ``boolean isVerificationCostly()`` und ``void applyTimingPadding()``
     - Optional (Standard ``false`` und keine Aktion). Ein absichtlich langsamer Algorithmus gibt ``true`` zurück und verbraucht in ``applyTimingPadding()`` etwa die Zeit eines ``matches``. |Fess| ruft die Methode auf, wenn eine Anmeldung scheitert, ohne dass ein Hash geprüft wurde (zum Beispiel bei einem unbekannten Benutzer), damit die Antwortzeit nicht verrät, ob der Benutzer existiert.

So verwenden Sie den Encoder:

#. Legen Sie die JAR-Datei im Verzeichnis ``WEB-INF/plugin`` ab. Wie bei jedem Webanwendungs-Plugin benötigt das Manifest ``Fess-WebAppJar: true`` (siehe „pom.xml und Manifest"); ohne diesen Eintrag wird die Komponente nicht gefunden.
#. Setzen Sie ``app.password.algorithm`` in ``fess_config.properties`` auf die ID (``argon2`` für ``argon2PasswordEncoder``). Die ID muss in Kleinbuchstaben geschrieben sein und darf kein ``}`` enthalten. Neue und geänderte Passwörter werden danach mit diesem Encoder gehasht. Passwörter, die mit einer anderen ID oder als alter Hash ohne ID gespeichert sind, werden bei der nächsten erfolgreichen Anmeldung ihres Benutzers neu gehasht, solange ``app.password.upgrade.enabled`` den Wert ``true`` hat (Standard).

Beachten Sie Folgendes:

- Der Encoder ist ein Singleton, das von allen Threads gemeinsam genutzt wird, und muss daher threadsicher sein.
- Die Längenbegrenzung gehört zum Encoder. Wenn ein Passwort festgelegt wird (Benutzerverwaltung, erzwungene Passwortänderung, ``/api/v2/auth/password`` und Admin-API), lehnt |Fess| ein Passwort ab, das länger ist als ``getMaxPasswordBytes()`` des Algorithmus aus ``app.password.algorithm``, mit „Das Passwort darf höchstens N Bytes lang sein."; bei ``0`` oder weniger wird nur ``password.max.length`` geprüft. Beim Prüfen eines gespeicherten Hashes wendet |Fess| keine Längenbegrenzung an; ob ein längeres Passwort passen darf, entscheidet ``matches``.
- Lassen Sie das Plugin installiert, solange Passwörter mit seiner ID gespeichert sind. Ohne die Komponente passt ein Hash mit dieser ID nie: Diese Benutzer können sich nicht anmelden, und ihre Hashes werden nicht neu berechnet.
- Nennt ``app.password.algorithm`` eine ID ohne Komponente (zum Beispiel nach dem Entfernen der Plugin-JAR), startet |Fess| trotzdem, und Benutzer, deren Hash eine andere ID hat, können sich weiterhin anmelden, aber das Festlegen eines Passworts schlägt mit einem Fehler fehl, der ``app.password.algorithm`` nennt.

Anpassung der Suchoberfläche
============================

Webanwendungs-Plugins können keine JSP-Views hinzufügen. JSP-Views befinden
sich unter ``WEB-INF/view/`` im WAR des |Fess|-Kerns, während das
Plugin-JAR in den Klassenpfad (``WEB-INF/classes``) gemountet wird. Wenn
Sie das Design der Suchoberfläche ändern möchten, nutzen Sie ein Theme. Es passt das Design der Suchoberfläche (HTML/CSS/JavaScript) an.
Siehe :doc:`theme-development`.

Build und Installation
=======================

::

    mvn clean package

Im Verzeichnis ``target/`` wird eine JAR-Datei erzeugt (z. B.
``fess-webapp-example-15.10.0.jar``). Installieren Sie das erzeugte JAR
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
   * - ``fess-webapp-bangs``
     - Bangs im Stil von DuckDuckGo (``!g``), die eine Suche an eine andere Website senden
   * - ``fess-webapp-semantic-search``
     - Neuronale Suche/Vektorsuche (veraltet; abgelöst durch die Kernintegration in 15.8)
   * - ``fess-webapp-multimodal``
     - Multimodale Suche (Bild und Text)

Referenzinformationen
=====================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`theme-development` - Theme-Anpassung
- :doc:`../admin/plugin-guide` - Plugin-Installation
- :doc:`overview` - Entwicklerdokumentation Übersicht

