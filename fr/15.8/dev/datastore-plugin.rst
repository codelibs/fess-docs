==================================
Développement de plugins DataStore
==================================

Aperçu
======

En développant un plugin DataStore, vous pouvez ajouter à |Fess| la capacité
de récupérer du contenu depuis de nouvelles sources de données. Un DataStore
récupère des enregistrements depuis un système externe (base de données, API,
fichiers, etc.), les convertit en champs d'index selon le script de mapping
défini dans l'écran d'administration, puis les enregistre dans l'index de
|Fess|.

Les connecteurs publics tels que CSV, JSON, base de données, Git et divers
services cloud (``fess-ds-*``) sont tous implémentés selon ce mécanisme.
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ est publié
comme modèle d'implémentation ; pour créer un nouveau connecteur, il est donc
plus simple de partir en copiant ce projet.

Structure de base
=================

Un plugin DataStore se compose des trois éléments suivants.

- créer une classe héritant de ``AbstractDataStore``
- implémenter les deux méthodes ``getName()`` et ``storeData()``
- l'enregistrer comme composant dans ``fess_ds++.xml``

Implémentation minimale
------------------------

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
            // Utilisé comme nom de handler. Il est d'usage de retourner le nom simple de la classe
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Implémenter ici la récupération et le traitement des données
        }
    }

.. note::

   ``getName()`` et ``storeData()`` sont tous deux des méthodes abstraites
   ``protected``. Notez que le package de ``DataConfig`` dans |Fess| 15.x est
   ``org.codelibs.fess.opensearch.config.exentity`` (l'ancien
   ``org.codelibs.fess.es.config.exentity`` a été supprimé).

Enregistrement du composant
----------------------------

Pour que |Fess| reconnaisse le DataStore créé, enregistrez le composant dans
``src/main/resources/fess_ds++.xml``.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Grâce à ``<postConstruct name="register">``, la méthode ``register()`` fournie
par ``AbstractDataStore`` est appelée automatiquement après la création du
composant, ce qui enregistre celui-ci auprès de ``DataStoreFactory``. Le nom
enregistré à ce moment est la valeur de retour de ``getName()`` (``ExampleDataStore``
dans l'exemple ci-dessus), qui devient le « nom de handler » sélectionnable dans
la configuration du DataStore de l'écran d'administration.

AbstractDataStore
=================

Méthodes principales
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Méthode
     - Catégorie
     - Description
   * - ``getName()``
     - Implémentation (obligatoire)
     - Méthode abstraite retournant le nom de handler du DataStore. Il est d'usage de retourner ``getClass().getSimpleName()``
   * - ``storeData()``
     - Implémentation (obligatoire)
     - Méthode abstraite effectuant la récupération, la conversion et l'enregistrement des données dans l'index
   * - ``register()``
     - Héritée (généralement inchangée)
     - Appelée automatiquement depuis le ``postConstruct`` de ``fess_ds++.xml`` ; enregistre le composant auprès de ``DataStoreFactory``
   * - ``store()``
     - Héritée (appelée par le framework)
     - Point d'entrée appelé par le framework. Prépare notamment ``defaultDataMap`` puis appelle ``storeData()``
   * - ``convertValue()``
     - Héritée (méthode d'aide)
     - Évalue la valeur (le gabarit) de ``scriptMap`` à l'aide du moteur de script
   * - ``getScriptType()``
     - Héritée (méthode d'aide)
     - Récupère le paramètre ``script_type`` (Groovy par défaut)
   * - ``getReadInterval()``
     - Héritée (méthode d'aide)
     - Récupère le paramètre ``readInterval`` (en millisecondes)
   * - ``sleep()``
     - Héritée (méthode d'aide)
     - Met en pause l'exécution pendant le nombre de millisecondes indiqué (utilisé pour patienter entre les enregistrements)

Paramètres de storeData
-------------------------

Paramètres passés à la méthode ``storeData()`` :

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Paramètre
     - Type
     - Description
   * - ``dataConfig``
     - ``DataConfig``
     - Configuration du DataStore (ID, nom de handler, paramètres, scripts, etc.)
   * - ``callback``
     - ``IndexUpdateCallback``
     - Callback permettant d'enregistrer le document généré dans l'index
   * - ``paramMap``
     - ``DataStoreParams``
     - Valeurs configurées dans le champ « Paramètres » de l'écran d'administration. Accessible via ``getAsString(key)`` / ``getAsString(key, default)`` / ``get(key)`` / ``asMap()`` / ``containsKey(key)``
   * - ``scriptMap``
     - ``Map<String, String>``
     - Configuration du champ « Script » de l'écran d'administration. La clé est le nom du champ d'index, la valeur est le gabarit de script à évaluer
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - Valeurs de champs par défaut de chaque document (ID de configuration, boost, rôle, mimetype, hôte virtuel, etc.). Préparé par le framework

.. warning::

   Le type de ``paramMap`` n'est pas ``Map<String, String>`` mais
   ``DataStoreParams``. ``DataStoreParams`` n'implémentant pas ``Map``,
   utilisez ``getAsString()``, qui retourne une chaîne, plutôt que ``get()``
   pour récupérer les valeurs.

Flux de traitement des données
--------------------------------

L'implémentation de ``storeData()`` traite les données selon le flux suivant.

#. Récupérer les enregistrements source depuis le système externe.
#. Construire ``resultMap`` en fusionnant les champs de l'enregistrement source
   dans ``paramMap.asMap()`` (le script est évalué sur ce ``resultMap``).
#. Évaluer chaque entrée de ``scriptMap`` avec ``convertValue(scriptType, template, resultMap)``
   et stocker le résultat dans ``dataMap``. Il est important que le mapping ne
   soit pas codé en dur dans le code, mais défini par l'administrateur dans le
   champ « Script ».
#. Appeler ``callback.store(paramMap, dataMap)`` pour enregistrer le document dans l'index.

Exemple d'implémentation
========================

DataStore simple
-----------------

Exemple récupérant des enregistrements depuis une API externe et les
enregistrant dans l'index.

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Récupération des paramètres (utiliser getAsString avec DataStoreParams)
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // Type d'évaluation du script (Groovy par défaut)
        final String scriptType = getScriptType(paramMap);
        // Délai d'attente entre les enregistrements (en millisecondes)
        final long readInterval = getReadInterval(paramMap);

        try {
            // Récupération des données depuis le système externe
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // Initialise dataMap en copiant les champs par défaut
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Construit resultMap en fusionnant les paramètres et l'enregistrement source
                // (le script est évalué sur ce resultMap)
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // Évalue chaque entrée de scriptMap pour générer les champs d'index
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // Enregistrement dans l'index
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` est une méthode propre au connecteur qui récupère la liste
des enregistrements depuis le système externe. Les noms de champs de chaque
enregistrement récupéré (``Map<String, Object>``) sont les noms auxquels les
scripts de ``scriptMap`` peuvent faire référence. ``DataStoreException`` est
une classe du package ``org.codelibs.fess.exception``.

Prise en charge de la pagination
-----------------------------------

Pour traiter de grands volumes de données, il convient de récupérer les
enregistrements page par page. Il est recommandé d'extraire le traitement par
enregistrement (construction de ``resultMap``, évaluation de ``scriptMap``,
appel de ``callback.store()``) dans une méthode telle que ``processRecord()``,
ce qui permet de séparer cette logique de celle de récupération.

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

Implémentation de l'authentification
=====================================

L'authentification auprès du système externe est implémentée côté connecteur.
Voici un exemple d'implémentation utilisant une bibliothèque cliente HTTP
courante ; il ne s'agit pas d'une API fournie par |Fess|. La bibliothèque
utilisée doit être incluse comme dépendance du plugin.

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // Exemple de récupération d'un jeton d'accès à l'aide d'un jeton de rafraîchissement
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

Authentification par clé API
------------------------------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Gestion des erreurs
====================

Pour les erreurs fatales devant interrompre le traitement, levez une exception
``DataStoreException``.

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Traitement
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // Logique de nouvelle tentative
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   Dans les connecteurs réels tels que ``fess-ds-example``, afin qu'une erreur
   sur un seul enregistrement n'interrompe pas l'ensemble de l'exploration, une
   ``CrawlingAccessException`` est capturée au niveau de chaque enregistrement
   et l'URL en erreur est enregistrée dans ``FailureUrlService``. Le drapeau
   d'interruption de ``DataStoreCrawlingException`` est également utilisé pour
   contrôler si l'ensemble de l'exploration doit être interrompu. Pour
   implémenter un connecteur robuste, référez-vous à l'implémentation de
   ``ExampleDataStore``.

Tests
=====

Tests unitaires
-----------------

Les plugins |Fess| sont testés à l'aide de la classe ``LastaDiTestCase`` d'UTFlute.
Les tests sont écrits avec JUnit 5 (Jupiter). En remplaçant ``IndexUpdateCallback``
par une implémentation qui collecte les ``dataMap`` enregistrés, il est possible
de vérifier le résultat du mapping sans recourir à une bibliothèque de mocks.

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

        // Callback de test collectant les dataMap enregistrés
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
                // Ne rien faire
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   Comme la classe de base annote déjà ``setUp`` avec ``@BeforeEach``, il n'est
   pas nécessaire de réajouter d'annotation de cycle de vie sur la méthode
   surchargée. Chaque méthode de test doit être annotée avec ``@Test``
   (``org.junit.jupiter.api.Test``).

Build et installation
========================

pom.xml
-------

Le plugin est construit comme un jar ayant ``fess-parent`` pour POM parent.
Les dépendances vers ``fess`` et ``opensearch`` étant fournies au moment de
l'exécution par |Fess| lui-même, elles doivent être déclarées en ``provided``.

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

Les tests utilisent JUnit 5 et ``org.dbflute.utflute:utflute-lastaflute``.

Build
-----

.. code-block:: bash

    mvn clean package

Le fichier ``fess-ds-example-15.8.0.jar`` est généré dans le répertoire ``target/``.

Installation
------------

Installez le fichier JAR généré dans |Fess| puis redémarrez |Fess|. Pour les
détails de la procédure d'installation, référez-vous à :doc:`../admin/plugin-guide`.
Après l'installation, créez une nouvelle configuration depuis « Crawler >
DataStore » dans l'écran d'administration, et indiquez dans « Nom de handler »
le nom retourné par ``getName()`` (``ExampleDataStore`` dans cet exemple).

Exemple de configuration
==========================

Exemple de configuration dans l'écran d'administration :

Paramètres
----------

Le champ « Paramètres » contient les clés et valeurs que le connecteur lit
depuis ``paramMap``.

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

Script
------

Le champ « Script » contient le mapping sous la forme ``membre gauche=membre droit``.
Le membre gauche est le nom du champ d'index, le membre droit est un script
(Groovy par défaut) référençant un champ de l'enregistrement source. Voici un
exemple pour un enregistrement source comportant les champs ``url`` / ``title``
/ ``content`` / ``updated_at`` / ``content_type``.

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   Les noms de champs référençables dans le membre droit dépendent des valeurs
   que le connecteur stocke dans ``resultMap`` (les valeurs de ``paramMap`` et
   les champs de l'enregistrement source). Dans les connecteurs existants tels
   que CSV ou JSON, un préfixe propre tel que ``data.*`` peut être utilisé ;
   référez-vous à la documentation de chaque connecteur.

Informations complémentaires
==============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`../admin/plugin-guide` - Installation des plugins
- :doc:`../config/datastore/ds-overview` - Vue d'ensemble des connecteurs DataStore
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ - Modèle d'implémentation de plugin DataStore
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Exemples de connecteurs publiés
