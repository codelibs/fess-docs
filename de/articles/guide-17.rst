==========================
Fess mit Plugins erweitern
==========================

Einleitung
==========

Wenn es kein ``fess-ds-*``-Plugin gibt, das zu Ihrem internen System passt, oder wenn Sie alle Dokumente vor der Indexierung bearbeiten möchten, schreiben Sie ein eigenes Plugin.
Dieser Artikel richtet sich an Java-Entwickler. Er zeigt, wie Sie aus einer offiziellen Vorlage ein Plugin für Fess 15.9 erstellen, es installieren und seine Funktion prüfen.

Wenn Sie die Schritte dieses Artikels nachvollziehen, können Sie anschließend:

- die Plugin-Typen verstehen und wie Fess sie voneinander unterscheidet
- auf Basis von ``fess-ds-example`` ein Datenspeicher-Plugin bauen, in Fess einbinden und damit Dokumente indexieren
- auf Basis von ``fess-ingest-example`` einen Ingester erstellen, der Dokumente vor der Indexierung bearbeitet

Vorausgesetzt werden Java 21 oder neuer, Maven 3 und ein laufendes Fess 15.9 (:doc:`guide-02`).
Die Bedienung des Bildschirms für Datenspeicher-Konfigurationen wird in :doc:`datastore-basics` erklärt; wenn Sie ihn zuerst lesen, lassen sich die Schritte leichter nachvollziehen.

Plugin-Typen
============

Ein Plugin ist eine jar-Datei, die im Fess-Installationsverzeichnis unter ``app/WEB-INF/plugin/`` liegt.
Fess bestimmt den Typ eines Plugins anhand des Anfangs (Präfix) des jar-Dateinamens (``PluginHelper.ArtifactType``).
In 15.9 gibt es folgende Typen.

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - Präfix
     - Aufgabe
     - Referenz-Repository
   * - ``fess-ds``
     - Datenspeicher. Holt Datensätze aus einem externen System und indexiert sie
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester. Bearbeitet Dokumente vor der Indexierung
     - ``fess-ingest-example``
   * - ``fess-script``
     - Skript-Engine
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - Erweiterung der Webanwendung (zusätzliche APIs oder Endpunkte)
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - Erzeugung von Vorschaubildern
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - Crawler-Client
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - LLM-Anbieter für den KI-Suchmodus
     - ``fess-llm-openai``
   * - ``fess-storage``
     - Objektspeicher (S3 / GCS)
     - ``fess-storage-s3``
   * - ``fess-sso``
     - Authentifizierungsverfahren für Single Sign-on
     - ``fess-sso-oidc``

Alle diese Repositorys sind unter https://github.com/codelibs veröffentlicht.

Das Design der Suchseite wird nicht über Plugins geändert.
Die JAR-Theme-Plugins ``fess-theme-*``, die JSPs ersetzten, wurden in 15.9 entfernt; die Suchseite ist jetzt ein ZIP-Theme aus ``theme.yml``, ``index.html`` und ``assets/``.
Themes werden unter [System] > [Theme] hochgeladen.
Wie Sie ein Theme erstellen, beschreibt der `Theme-Entwicklungsleitfaden <https://fess.codelibs.org/de/stable/dev/theme-development.html>`__; zum Einbinden der Suche in eine bestehende Website siehe :doc:`guide-03`.

Ein Datenspeicher-Plugin erstellen
==================================

Die Vorlage beschaffen
----------------------

``fess-ds-example`` ist ein Repository, das als Gerüst für Datenspeicher-Plugins veröffentlicht wird.
Sein Standard-Branch folgt der Version in Entwicklung (15.10.0-SNAPSHOT); um für 15.9 zu bauen, verwenden Sie den auf 15.9.0 abgestimmten Commit.

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

Dieser Commit unterscheidet sich vom Standard-Branch nur in zwei Zeilen der ``pom.xml`` (Projektversion und Version des Parent-POM).
Sie erhalten dasselbe Ergebnis, wenn Sie auf dem Standard-Branch bleiben und die beiden im nächsten Abschnitt genannten Stellen für 15.9 ändern.

pom.xml
-------

Die wesentlichen Teile der ``pom.xml`` sind die folgenden.

.. code-block:: xml

    <artifactId>fess-ds-example</artifactId>
    <packaging>jar</packaging>
    <version>15.9.0-SNAPSHOT</version>

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.9.0</version>
        <relativePath />
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.opensearch</groupId>
            <artifactId>opensearch</artifactId>
            <version>${opensearch.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

Die Version von ``fess-parent`` richtet sich nach der Fess-Version, in die das Plugin installiert wird.
In ``fess-parent`` 15.9.0 ist ``fess.version`` gleich ``15.9.0``, daher wird gegen die API von Fess 15.9.0 kompiliert.
Fess selbst und die OpenSearch-Klassen stellt Fess zur Laufzeit bereit, deshalb sind sie ``provided``.
Die tatsächliche ``pom.xml`` enthält noch weitere Abhängigkeiten und Build-Einstellungen; verwenden Sie sie zunächst unverändert.
Das ``fess``-jar wird nicht aus Maven Central geladen, sondern aus dem von ``fess-parent`` deklarierten CodeLibs-Repository (``https://maven.codelibs.org/release/``).
In Umgebungen mit Proxy oder Mirror muss dieses Repository erreichbar sein.

Wenn Sie daraus Ihr eigenes Plugin machen, beginnen Sie die ``artifactId`` immer mit ``fess-ds-``.
Wie später erklärt, werden die Kandidaten für „Handler-Name“ in der Administrationsoberfläche nur aus jars gesammelt, deren Dateiname mit ``fess-ds`` beginnt.

Datenspeicher-Klasse
--------------------

Ein Datenspeicher erbt von ``org.codelibs.fess.ds.AbstractDataStore`` und implementiert ``getName()`` und ``storeData(...)``.
Das Folgende ist ``ExampleDataStore``, reduziert auf das Gerüst der Verarbeitung.
Es dient nur zum Verständnis der Funktionsweise; für den Build verwenden Sie ``ExampleDataStore`` aus dem Repository unverändert (die Tests verwenden Methoden, die im Gerüst fehlen, sodass beim Ersetzen die Kompilierung der Tests fehlschlägt).

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.HashMap;
    import java.util.LinkedHashMap;
    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback, final DataStoreParams paramMap,
                final Map<String, String> scriptMap, final Map<String, Object> defaultDataMap) {
            final String scriptType = getScriptType(paramMap);
            final int dataSize = Integer.parseInt(paramMap.getAsString("data.size", "10"));

            for (int i = 0; i < dataSize && alive; i++) {
                // Ein aus dem externen System geholter Datensatz (hier feste Werte)
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // Skripte werden auf „Parameter + Datensatz“ ausgewertet
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(source);

                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }
                callback.store(paramMap, dataMap);
            }
        }
    }

Die einzelnen Teile haben folgende Aufgaben.

- Der Rückgabewert von ``getName()`` wird als Name dieses Datenspeichers in ``DataStoreFactory`` registriert. Üblicherweise wird der einfache Klassenname zurückgegeben
- ``paramMap`` enthält die Werte aus dem Feld „Parameter“ der Datenspeicher-Konfiguration. Sie lesen sie mit ``getAsString(Schlüssel, Standardwert)`` aus
- ``scriptMap`` enthält die Zeilen des Felds „Skript“ in der Form ``Feldname=Ausdruck``. ``convertValue()`` wertet den Ausdruck aus, und das Ergebnis landet im entsprechenden Indexfeld
- ``defaultDataMap`` enthält Werte, die sich aus der Datenspeicher-Konfiguration ergeben, etwa Konfigurations-ID, Berechtigungen (Rollen), Boost-Wert und virtuelle Hosts. Kopieren Sie sie zuerst und fügen Sie dann die einzelnen Felder hinzu
- ``callback.store()`` indexiert die Datensätze einzeln. ``alive`` wird ``false``, sobald der Job gestoppt wird; nehmen Sie es deshalb in die Schleifenbedingung auf

Welcher Wert eines Datensatzes in welches Feld kommt, steht also nicht im Plugin, sondern wird vom Administrator im Feld „Skript“ festgelegt.
Die Aufgabe des Plugins ist es, Datensätze zu holen und in ``resultMap`` bereitzustellen.

Das tatsächliche ``ExampleDataStore`` implementiert zusätzlich eine Ausnahmebehandlung pro Datensatz (Eintrag unter [Fehler-URL]) und Crawl-Statistiken (``CrawlerStatsHelper``).
Wenn Sie Ihr eigenes Plugin erstellen, kopieren Sie nicht dieses Gerüst, sondern ``ExampleDataStore``, und schreiben Sie die mit ``// CUSTOMIZE:`` markierten Stellen (das Holen der Datensätze) um.

DI-Konfigurationsdatei
----------------------

Eine Klasse allein wird von Fess nicht geladen.
Registrieren Sie sie in ``src/main/resources/fess_ds++.xml`` als Komponente.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Der DI-Container (Lasta Di) übernimmt jede ``fess_ds++.xml`` im Klassenpfad in die ``fess_ds.xml`` von Fess.
Durch ``<postConstruct name="register">`` wird nach der Erzeugung ``AbstractDataStore.register()`` aufgerufen und der Datenspeicher unter dem Namen aus ``getName()`` registriert.
Wenn Sie Klassennamen oder Paket ändern, passen Sie auch das Attribut ``class`` an.

Bauen
-----

::

    $ mvn clean package

In ``target/`` entstehen drei jars.
In Fess installiert wird ``fess-ds-example-15.9.0-SNAPSHOT.jar``, also das jar ohne ``-sources`` oder ``-javadoc``.
Mit ``unzip -l`` können Sie prüfen, dass es ``fess_ds++.xml`` und ``ExampleDataStore.class`` enthält.

Installieren
============

Am einfachsten installieren Sie das Plugin über die Administrationsoberfläche.

1. Klicken Sie unter [System] > [Plugin] auf [Installieren]
2. Lassen Sie die Auswahlliste auf dem Reiter [Remote] auf dem ersten Eintrag ``-``. Ist ein anderes Plugin ausgewählt, wird stattdessen dieses installiert
3. Wählen Sie auf dem Reiter [Lokal] unter „Jar-Datei“ das gebaute jar aus und klicken Sie auf [Installieren]
4. Starten Sie Fess neu

Das hochgeladene jar wird in ``app/WEB-INF/plugin/`` als ``<Name>-<Version>.jar`` gespeichert.
Name und Version werden aus dem Dateinamen gelesen; laden Sie das jar daher mit dem von Maven vergebenen Dateinamen hoch.
Statt der Administrationsoberfläche können Sie das jar auch direkt in dieses Verzeichnis kopieren und neu starten (im Docker-Image ``/usr/share/fess/app/WEB-INF/plugin/``).

Unter Docker holt ``FESS_PLUGINS`` Plugins, die in einem Repository veröffentlicht sind; für ein eigenes jar lässt es sich nicht verwenden.
Installieren Sie das jar über die Administrationsoberfläche und starten Sie anschließend mit ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01`` neu.
Das jar liegt im Container und verschwindet daher, wenn Sie den Container mit ``down`` und ``up`` neu erstellen.
Installieren Sie es in diesem Fall erneut.

Funktion prüfen
===============

Den Handler-Namen prüfen
------------------------

Öffnen Sie nach dem Neustart [Crawler] > [Datenspeicher] > [Neu erstellen] und prüfen Sie, ob ``ExampleDataStore`` in der Auswahlliste „Handler-Name“ erscheint.
Die Kandidaten werden aus den jars in ``app/WEB-INF/plugin/`` gebildet, deren Dateiname mit ``fess-ds`` beginnt.
Fess liest die ``fess_ds++.xml`` im jar und verwendet den einfachen Namen der Klasse aus dem Attribut ``class`` als Kandidaten (60 Sekunden lang zwischengespeichert).
Erscheint er nicht, prüfen Sie den jar-Dateinamen, die ``fess_ds++.xml`` im jar und ob Sie neu gestartet haben.

Die Datenspeicher-Konfiguration anlegen
---------------------------------------

Geben Sie auf demselben Bildschirm Folgendes ein und klicken Sie auf [Erstellen].

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Feld
     - Wert
   * - Name
     - ``Example``
   * - Handler-Name
     - ``ExampleDataStore``
   * - Parameter
     - ``data.size=5`` in der Zeile nach dem vorausgefüllten ``script_type=javascript`` ergänzen
   * - Skript
     - Drei Zeilen: ``title=title``, ``content=body`` und ``url=url``

Stimmt die rechte Seite einer Skriptzeile mit einem Schlüssel des Datensatzes überein (``title``, ``body``, ``url``), gibt ``convertValue()`` diesen Wert unverändert zurück, ohne eine Skript-Engine zu verwenden.
Ein Ausdruck wie ``content=title + " " + body`` wird mit der in ``script_type`` angegebenen Engine ausgewertet.
Wenn Sie ``script_type`` entfernen, wird ``groovy`` angenommen, und in Umgebungen ohne ``fess-script-groovy`` schlägt die Auswertung von Ausdrücken fehl; lassen Sie die Zeile daher stehen.

``url`` ist erforderlich.
``callback.store()`` akzeptiert kein Dokument ohne ``url`` und wirft eine Ausnahme.

Den Job ausführen
-----------------

1. Klicken Sie in der Liste unter [Crawler] > [Datenspeicher] auf ``Example`` und dann auf [Neuen Job erstellen]
2. Der Bildschirm zum Anlegen eines Scheduler-Jobs öffnet sich; klicken Sie ohne Änderungen auf [Erstellen]
3. Öffnen Sie unter [System] > [Scheduler] den angelegten Job und klicken Sie auf [Jetzt starten]

Ergebnisse prüfen
-----------------

Prüfen Sie die folgenden vier Punkte.

1. Unter [Systeminformationen] > [Jobprotokoll] hat der Job den Status „OK“
2. Unter [Systeminformationen] > [Crawling-Informationen] ist „Indexgröße (Datenspeicher)“ für diese Sitzung ``5``
3. Unter [Systeminformationen] > [Fehler-URL] ist nichts eingetragen
4. Eine Suche nach ``Sample`` unter [Systeminformationen] > [Suche] liefert fünf Treffer, ``Sample 0`` bis ``Sample 4``

Der Jobstatus „OK“ bedeutet nicht zwingend, dass die Verarbeitung des Datenspeichers erfolgreich war.
Entfernen Sie zum Beispiel ``url=url`` aus dem Skript und führen den Job aus, wirft ``callback.store()`` für jeden Datensatz eine Ausnahme, und es wird nichts indexiert.
``ExampleDataStore`` fängt Ausnahmen pro Datensatz ab; daher werden unter [Fehler-URL] ``record:0`` bis ``record:4`` eingetragen und in ``fess-crawler.log`` erscheinen WARN-Meldungen, das Jobprotokoll zeigt aber weiterhin „OK“.
Bei Code, der Ausnahmen nicht abfängt, wie dem Gerüst, schlägt die gesamte Konfiguration fehl, und unter [Fehler-URL] wird nur ein Eintrag in der Form ``D<Konfigurations-ID>:Example`` erfasst.
Die Prüfschritte und die Speicherorte der Logs sind im Abschnitt über das Prüfen der Ergebnisse in :doc:`datastore-basics` zusammengefasst.

Wenn all das bestätigt ist, ersetzen Sie das Holen der Datensätze, etwa ``createSourceRecord()``, durch Code, der Ihre tatsächliche API oder Ihre Dateien liest.
Verbindungsziel und Zugangsdaten des externen Systems gehören nicht in den Code; übergeben Sie sie über das Feld „Parameter“ per ``paramMap``.

``src/test`` der Vorlage enthält Tests mit ``LastaDiTestCase`` aus UTFlute.
Eine Testklasse, die ``IndexUpdateCallback`` implementiert, sammelt die an ``store()`` übergebenen ``dataMap``-Objekte, und die Tests prüfen Anzahl und Feldwerte.
Deshalb können Sie ``mvn test`` ohne OpenSearch ausführen.
Wenn Sie das Holen der Datensätze umschreiben, passen Sie auch diese Tests an.

Dokumente vor der Indexierung mit einem Ingester bearbeiten
===========================================================

Ein Ingester wird bei jeder Art von Crawl – Datenspeicher, Web und Dateisystem – unmittelbar aufgerufen, bevor ein Dokument an den Index gesendet wird.
Er dient etwa dazu, allen Dokumenten ein gemeinsames Feld hinzuzufügen oder Werte zu normalisieren.
Es gibt keine Möglichkeit, ihn pro Konfiguration zu aktivieren oder zu deaktivieren; nach der Installation gilt er für alle Crawls.

Erben Sie von ``org.codelibs.fess.ingest.Ingester`` und überschreiben Sie nur die ``process``-Methoden, die Sie benötigen.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Methode
     - Aufgerufen bei
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - Datenspeicher-Crawls (innerhalb von ``callback.store()``)
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - der Indexierung bei Web- und Datei-Crawls
   * - ``process(ResultData target, ResponseData responseData)``
     - der Verarbeitung der abgerufenen Antwort bei Web- und Datei-Crawls
   * - ``protected process(Map<String, Object> target)``
     - Methode, die die beiden ``Map``-Varianten oben standardmäßig aufrufen. Überschreiben Sie nur diese, wenn die Verarbeitung sowohl für Datenspeicher- als auch für Web- und Datei-Crawls gelten soll

Das Folgende ist ``ExampleIngester`` aus ``fess-ingest-example``, reduziert auf die Verarbeitung für Datenspeicher.

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {
        private static final Logger logger = LogManager.getLogger(ExampleIngester.class);

        public ExampleIngester() {
            setPriority(50);
        }

        @Override
        public Map<String, Object> process(final Map<String, Object> target, final DataStoreParams params) {
            target.put("ingested_by", ExampleIngester.class.getSimpleName());
            logger.info("DATASTORE CRAWL: {}", target);
            return target;
        }
    }

Die Registrierung erfolgt in ``src/main/resources/fess_ingest++.xml``.
Der Aufbau entspricht ``fess_ds++.xml``: eine Komponente namens ``exampleIngester`` mit ``<postConstruct name="register">``.
``Ingester.register()`` fügt den Ingester selbst zu ``IngestFactory`` hinzu.

Vorlage beschaffen, bauen, installieren und neu starten funktionieren wie beim Datenspeicher (der Commit für 15.9 ist ``8a1e45ddb63a118802287120effd3ce49fb60bfb``, das jar heißt ``fess-ingest-example-15.9.0-SNAPSHOT.jar``).
Bei Ihrem eigenen Plugin beginnt die artifactId mit ``fess-ingest-``.

Beachten Sie bei der Implementierung folgende Punkte.

- Geben Sie ``target`` nach der Änderung immer zurück. Der Rückgabewert wird unverändert an den nächsten Ingester und an den Indexer weitergegeben, ohne Prüfung auf ``null``. Die Rückgabe von ``null`` schließt das Dokument nicht aus, sondern bringt die Indexierung durcheinander
- Mehrere Ingester laufen in aufsteigender Reihenfolge von ``priority`` (Standardwert 99). Jeder Ingester erhält das vom vorherigen geänderte ``target``
- Wirft ``process`` eine Ausnahme, protokolliert Fess eine WARN-Meldung und fährt mit dem nächsten Ingester fort. Die Indexierung des Dokuments wird nicht abgebrochen. Änderungen, die vor der Ausnahme an ``target`` vorgenommen wurden, bleiben erhalten

Zur Prüfung führen Sie den Job der in „Funktion prüfen“ oben angelegten Datenspeicher-Konfiguration noch einmal aus.
Ingester laufen im Crawler-Prozess; enthält ``fess-crawler.log`` für jedes Dokument eine Zeile ``DATASTORE CRAWL:``, wird der Ingester aufgerufen.
``ExampleIngester`` aus dem Repository protokolliert auch Dokumente aus Web- und Datei-Crawls einzeln als ``WEB/FILE CRAWL:``.
Da er auf alle Crawls wirkt, löschen Sie ihn nach der Prüfung unter [System] > [Plugin] und starten Fess neu.

Fess aktualisieren
==================

Bauen Sie ein Plugin mit dem ``fess-parent`` derselben Minor-Version wie das Fess, in das es installiert wird (für Fess 15.9 also 15.9.x).
Auch veröffentlichte Plugins erscheinen für jede Fess-Minor-Version in einer passenden Version.

Wenn Sie Fess auf 15.10 aktualisieren, passen Sie die ``fess-parent``-Version in der ``pom.xml`` an und bauen neu.
Löschen Sie in der Liste unter [System] > [Plugin] das alte jar, installieren Sie das neue und starten Sie neu.
``bin/fess-setup upgrade plugins`` holt neue Versionen aus dem Plugin-Repository; eigene Plugins, die dort nicht liegen, lassen sich damit nicht aktualisieren.

Weiterführende Artikel
======================

- Mehr über Parameter, Skripte, Berechtigungen und Zeitpläne von Datenspeichern: :doc:`datastore-basics`
- Konfigurationsbeispiele für veröffentlichte Datenspeicher-Plugins: :doc:`guide-06`, :doc:`guide-07` und :doc:`guide-12`
- Das Aussehen der Suchseite ändern: :doc:`guide-03`
- Den KI-Suchmodus mit einem LLM-Plugin aktivieren: :doc:`guide-19`
- Ein Webanwendungs-Plugin (MCP-Server) verwenden: :doc:`guide-20`

Referenzen
==========

- `Plugin-Architektur <https://fess.codelibs.org/de/stable/dev/plugin-architecture.html>`__
- `DataStore-Plugin-Entwicklung <https://fess.codelibs.org/de/stable/dev/datastore-plugin.html>`__
- `Ingest-Plugin <https://fess.codelibs.org/de/stable/dev/ingest-plugin.html>`__
- `Theme-Entwicklungsleitfaden <https://fess.codelibs.org/de/stable/dev/theme-development.html>`__
- `Plug-ins (Administrationsoberfläche) <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `fess-ds-example (GitHub) <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example (GitHub) <https://github.com/codelibs/fess-ingest-example>`__
