==================================
DataStore-Plugin-Entwicklung
==================================

Übersicht
=========

Durch die Entwicklung eines DataStore-Plugins können Sie |Fess| um die Fähigkeit
zur Inhaltserfassung aus neuen Datenquellen erweitern. Ein DataStore ruft
Datensätze aus externen Systemen wie Datenbanken, APIs oder Dateien ab, wandelt
sie gemäß dem in der Administrationsoberfläche konfigurierten Mapping-Skript in
Indexfelder um und registriert sie anschließend im Index von |Fess|.

Alle öffentlich verfügbaren Konnektoren (``fess-ds-*``) für CSV, JSON,
Datenbanken, Git und verschiedene Cloud-Dienste sind nach diesem Mechanismus
implementiert. Als Implementierungsvorlage steht
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ zur Verfügung.
Beim Erstellen eines neuen Konnektors ist es daher am einfachsten, dieses
Repository zu kopieren und darauf aufzubauen.

Grundstruktur
=============

Ein DataStore-Plugin besteht aus den folgenden drei Elementen:

- Erstellen einer Klasse, die von ``AbstractDataStore`` erbt
- Implementieren der beiden Methoden ``getName()`` und ``storeData()``
- Registrieren als Komponente in ``fess_ds++.xml``

Minimale Implementierung
-------------------------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // Wird als Handler-Name verwendet. Es ist üblich, den einfachen
            // Klassennamen zurückzugeben
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Datenabruf und -verarbeitung hier implementieren
        }
    }

.. note::

   ``getName()`` und ``storeData()`` sind beide ``protected`` deklarierte
   abstrakte Methoden. Beachten Sie, dass sich das Paket von ``DataConfig`` in
   |Fess| 15.x unter ``org.codelibs.fess.opensearch.config.exentity`` befindet
   (das frühere ``org.codelibs.fess.es.config.exentity`` wurde entfernt).

Komponenten-Registrierung
--------------------------

Damit |Fess| den erstellten DataStore erkennt, wird die Komponente in
``src/main/resources/fess_ds++.xml`` registriert.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Durch ``<postConstruct name="register">`` wird nach der Erzeugung der
Komponente automatisch die von ``AbstractDataStore`` bereitgestellte Methode
``register()`` aufgerufen, wodurch sich die Komponente selbst bei
``DataStoreFactory`` registriert. Der dabei registrierte Name ist der
Rückgabewert von ``getName()`` (im obigen Beispiel ``ExampleDataStore``) und
entspricht dem „Handler-Name", der in der Datenspeicher-Konfiguration der
Administrationsoberfläche ausgewählt wird.

AbstractDataStore
=================

Wichtige Methoden
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Methode
     - Kategorie
     - Beschreibung
   * - ``getName()``
     - Implementierung (erforderlich)
     - Abstrakte Methode, die den Handler-Namen des DataStore zurückgibt. Es ist üblich, ``getClass().getSimpleName()`` zurückzugeben
   * - ``storeData()``
     - Implementierung (erforderlich)
     - Abstrakte Methode, die Datenabruf, -umwandlung und Index-Registrierung durchführt
   * - ``register()``
     - Geerbt (in der Regel keine Änderung nötig)
     - Wird über ``postConstruct`` in ``fess_ds++.xml`` automatisch aufgerufen und registriert die Komponente bei ``DataStoreFactory``
   * - ``store()``
     - Geerbt (Framework-Aufruf)
     - Einstiegspunkt, der vom Framework aufgerufen wird. Bereitet u. a. ``defaultDataMap`` vor und ruft ``storeData()`` auf
   * - ``convertValue()``
     - Geerbt (Hilfsmethode)
     - Wertet den Wert (das Template) aus ``scriptMap`` mit der Skript-Engine aus
   * - ``getScriptType()``
     - Geerbt (Hilfsmethode)
     - Ruft den Parameter ``script_type`` ab (Standard ist Groovy)
   * - ``getReadInterval()``
     - Geerbt (Hilfsmethode)
     - Ruft den Parameter ``readInterval`` (in Millisekunden) ab
   * - ``sleep()``
     - Geerbt (Hilfsmethode)
     - Wartet die angegebene Anzahl an Millisekunden (wird zum Warten zwischen Datensätzen verwendet)

Parameter von storeData
-------------------------

An die Methode ``storeData()`` übergebene Parameter:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Parameter
     - Typ
     - Beschreibung
   * - ``dataConfig``
     - ``DataConfig``
     - Datenspeicher-Konfiguration (ID, Handler-Name, Parameter, Skript usw.)
   * - ``callback``
     - ``IndexUpdateCallback``
     - Callback zur Registrierung des erzeugten Dokuments im Index
   * - ``paramMap``
     - ``DataStoreParams``
     - Konfigurationswerte aus dem Feld „Parameter" der Administrationsoberfläche. Zugriff über ``getAsString(key)`` / ``getAsString(key, default)`` / ``get(key)`` / ``asMap()`` / ``containsKey(key)``
   * - ``scriptMap``
     - ``Map<String, String>``
     - Konfiguration aus dem Feld „Skript" der Administrationsoberfläche. Der Schlüssel ist der Indexfeldname, der Wert das auszuwertende Skript-Template
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - Standardfeldwerte jedes Dokuments (Konfigurations-ID, Boost, Rolle, MIME-Type, virtueller Host usw.), die vom Framework bereitgestellt werden

.. warning::

   Der Typ von ``paramMap`` ist nicht ``Map<String, String>``, sondern
   ``DataStoreParams``. Da ``DataStoreParams`` das Interface ``Map`` nicht
   implementiert, verwenden Sie zum Abrufen von Werten nicht ``get()``, sondern
   ``getAsString()``, das einen String zurückgibt.

Ablauf der Datenverarbeitung
------------------------------

Die Implementierung von ``storeData()`` verarbeitet Daten in folgendem Ablauf.

#. Abrufen der Quelldatensätze aus dem externen System.
#. Erstellen von ``resultMap`` durch Zusammenführen der Felder des
   Quelldatensatzes mit ``paramMap.asMap()`` (das Skript wird gegen dieses
   ``resultMap`` ausgewertet).
#. Auswerten jedes Eintrags von ``scriptMap`` mit
   ``convertValue(scriptType, template, resultMap)`` und Speichern des
   Ergebnisses in ``dataMap``. Wichtig ist, dass das Mapping nicht im Code fest
   verdrahtet ist, sondern vom Administrator im Feld „Skript" definiert wird.
#. Aufrufen von ``callback.store(paramMap, dataMap)``, um das Dokument im Index
   zu registrieren.

Implementierungsbeispiel
==========================

Einfacher DataStore
---------------------

Ein Beispiel, das Datensätze von einer externen API abruft und im Index
registriert.

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Parameter abrufen (bei DataStoreParams wird getAsString verwendet)
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // Auswertungstyp des Skripts (Standard ist Groovy)
        final String scriptType = getScriptType(paramMap);
        // Wartezeit zwischen Datensätzen (in Millisekunden)
        final long readInterval = getReadInterval(paramMap);

        try {
            // Daten vom externen System abrufen
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // dataMap durch Kopieren der Standardfelder initialisieren
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // resultMap durch Zusammenführen von Parametern und
                // Quelldatensatz erstellen
                // (das Skript wird gegen dieses resultMap ausgewertet)
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // Jeden Eintrag von scriptMap auswerten, um Indexfelder zu erzeugen
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // Im Index registrieren
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` ist eine eigene Methode, die die Liste der Datensätze vom
externen System abruft. Die Feldnamen der einzelnen abgerufenen Datensätze
(``Map<String, Object>``) sind die Namen, auf die im Skript von ``scriptMap``
verwiesen werden kann. ``DataStoreException`` ist eine Klasse aus dem Paket
``org.codelibs.fess.exception``.

Unterstützung für Paginierung
-------------------------------

Beim Umgang mit großen Datenmengen erfolgt die Verarbeitung seitenweise. Wenn
die Verarbeitung pro Datensatz (Erstellen von ``resultMap``, Auswerten von
``scriptMap``, Aufruf von ``callback.store()``) in eine Methode wie
``processRecord()`` ausgelagert wird, lässt sie sich von der Abruflogik
trennen.

.. code-block:: java

    int offset = 0;
    final int pageSize = 100;

    while (true) {
        final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey, offset, pageSize);

        if (records.isEmpty()) {
            break;
        }

        for (final Map<String, Object> record : records) {
            processRecord(record, callback, paramMap, scriptMap, defaultDataMap);
        }

        offset += pageSize;
    }

Implementierung der Authentifizierung
========================================

Die Authentifizierung gegenüber dem externen System wird auf Seiten des
Konnektors implementiert. Das folgende Beispiel verwendet eine gängige
HTTP-Client-Bibliothek und ist keine von |Fess| bereitgestellte API. Binden Sie
die verwendete Bibliothek als Abhängigkeit des Plugins ein.

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // Beispiel zum Abrufen eines Access-Tokens mittels Refresh-Token
        final OkHttpClient client = new OkHttpClient();

        final RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        final Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            final JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

API-Key-Authentifizierung
---------------------------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Fehlerbehandlung
==================

Bei fatalen Fehlern, die die Verarbeitung abbrechen sollen, wird
``DataStoreException`` geworfen.

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Verarbeitung
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // Retry-Logik
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   Bei tatsächlichen Konnektoren wie ``fess-ds-example`` wird
   ``CrawlingAccessException`` pro Datensatz abgefangen, damit ein Fehler bei
   einem einzelnen Datensatz nicht den gesamten Crawl-Vorgang stoppt; die
   fehlerhafte URL wird dabei bei ``FailureUrlService`` protokolliert. Außerdem
   wird über das Abbruch-Flag von ``DataStoreCrawlingException`` gesteuert, ob
   der gesamte Crawl-Vorgang abgebrochen werden soll. Wenn Sie einen robusten
   Konnektor implementieren möchten, orientieren Sie sich an der
   Implementierung von ``ExampleDataStore``.

Tests
=====

Unit-Tests
----------

|Fess|-Plugins werden mit ``LastaDiTestCase`` aus UTFlute getestet. Die Tests
werden mit JUnit 5 (Jupiter) geschrieben. Indem ``IndexUpdateCallback`` durch
eine Implementierung ersetzt wird, die die registrierten ``dataMap``-Werte
sammelt, lässt sich das Mapping-Ergebnis ohne Mock-Bibliothek überprüfen.

.. code-block:: java

    public class ExampleDataStoreTest extends LastaDiTestCase {

        public ExampleDataStore dataStore;

        @Override
        protected String prepareConfigFile() {
            return "test_app.xml";
        }

        @Override
        public void setUp(final TestInfo testInfo) throws Exception {
            super.setUp(testInfo);
            dataStore = new ExampleDataStore();
        }

        @Test
        public void test_getName() {
            assertEquals("ExampleDataStore", dataStore.getName());
        }

        @Test
        public void test_storeData() {
            final TestIndexUpdateCallback callback = new TestIndexUpdateCallback();
            final DataStoreParams paramMap = new DataStoreParams();

            final Map<String, String> scriptMap = new HashMap<>();
            scriptMap.put("title", "title");

            dataStore.storeData(new DataConfig(), callback, paramMap, scriptMap, new HashMap<>());

            assertFalse(callback.getDataMapList().isEmpty());
        }

        // Test-Callback, der die registrierten dataMap-Werte sammelt
        private static class TestIndexUpdateCallback implements IndexUpdateCallback {
            private final List<Map<String, Object>> dataMapList = new ArrayList<>();

            @Override
            public void store(final DataStoreParams paramMap, final Map<String, Object> dataMap) {
                dataMapList.add(new HashMap<>(dataMap));
            }

            @Override
            public long getExecuteTime() {
                return 0;
            }

            @Override
            public long getDocumentSize() {
                return dataMapList.size();
            }

            @Override
            public void commit() {
                // Keine Aktion
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   Da ``setUp`` in der Basisklasse bereits mit ``@BeforeEach`` versehen ist,
   muss beim Überschreiben keine Lifecycle-Annotation erneut hinzugefügt
   werden. Jeder Testmethode wird ``@Test`` (``org.junit.jupiter.api.Test``)
   hinzugefügt.

Build und Installation
========================

pom.xml
-------

Das Plugin wird als jar mit ``fess-parent`` als übergeordnetem POM gebaut. Die
Abhängigkeiten von ``fess`` und ``opensearch`` werden zur Laufzeit von |Fess|
selbst bereitgestellt und daher als ``provided`` deklariert.

.. code-block:: xml

    <project xmlns="http://maven.apache.org/POM/4.0.0" ...>
        <modelVersion>4.0.0</modelVersion>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

Für Tests werden JUnit 5 und ``org.dbflute.utflute:utflute-lastaflute``
verwendet.

Build
-----

.. code-block:: bash

    mvn clean package

Im Verzeichnis ``target/`` wird ``fess-ds-example-15.8.0.jar`` erzeugt.

Installation
------------

Installieren Sie das erzeugte JAR in |Fess| und starten Sie |Fess| neu.
Details zum Installationsvorgang finden Sie unter
:doc:`../admin/plugin-guide`. Erstellen Sie nach der Installation über
„Crawler > Datenspeicher" in der Administrationsoberfläche eine neue
Konfiguration und geben Sie als „Handler-Name" den von ``getName()``
zurückgegebenen Namen an (in diesem Beispiel ``ExampleDataStore``).

Konfigurationsbeispiel
========================

Konfigurationsbeispiel in der Administrationsoberfläche:

Parameter
---------

Im Feld „Parameter" werden die Schlüssel und Werte angegeben, die der
Konnektor aus ``paramMap`` ausliest.

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

Skript
------

Im Feld „Skript" wird das Mapping im Format ``linke Seite=rechte Seite``
angegeben. Die linke Seite ist der Indexfeldname, die rechte Seite ein Skript
(standardmäßig Groovy), das auf ein Feld des Quelldatensatzes verweist. Das
folgende Beispiel gilt für den Fall, dass der Quelldatensatz die Felder
``url`` / ``title`` / ``content`` / ``updated_at`` / ``content_type`` besitzt.

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   Welche Feldnamen auf der rechten Seite referenziert werden können, hängt
   von den Werten ab, die der Konnektor in ``resultMap`` ablegt (Werte aus
   ``paramMap`` und Felder des Quelldatensatzes). Bei bestehenden Konnektoren
   wie CSV oder JSON kann ein eigenes Präfix wie ``data.*`` vorangestellt
   sein; weitere Details finden Sie in der Dokumentation des jeweiligen
   Konnektors.

Referenzinformationen
======================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`../admin/plugin-guide` - Plugin-Installation
- :doc:`../config/datastore/ds-overview` - Übersicht der Datenspeicher-Konnektoren
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ - Implementierungsvorlage für DataStore-Plugins
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Beispiele veröffentlichter Konnektoren
