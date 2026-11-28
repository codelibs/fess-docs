===========================
Extending Fess with Plugins
===========================

Introduction
============

When no ``fess-ds-*`` plugin fits your in-house system, or when you want to process every document before it is indexed, you write your own plugin.
This article is for Java developers. It explains how to create a plugin that runs on Fess 15.9 from an official template, install it, and confirm that it works.

By following the steps in this article, you will be able to:

- Understand the types of plugins and how Fess tells them apart
- Build a data store plugin based on ``fess-ds-example``, add it to Fess, and index documents with it
- Create an Ingester that processes documents before indexing, based on ``fess-ingest-example``

We assume that Java 21 or later and Maven 3 are available, and that Fess 15.9 is running (:doc:`guide-02`).
How to use the data store configuration screen is explained in :doc:`datastore-basics`; reading it first makes the steps easier to follow.

Types of Plugins
================

A plugin is a jar file placed in ``app/WEB-INF/plugin/`` under the Fess installation directory.
Fess determines the type of a plugin from the beginning (prefix) of the jar file name (``PluginHelper.ArtifactType``).
The types in 15.9 are as follows.

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - Prefix
     - Role
     - Reference repository
   * - ``fess-ds``
     - Data store. Fetches records from an external system and indexes them
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester. Processes documents before indexing
     - ``fess-ingest-example``
   * - ``fess-script``
     - Script engine
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - Web application extension (adding APIs or endpoints)
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - Thumbnail generation
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - Crawler client
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - LLM provider used by AI search mode
     - ``fess-llm-openai``
   * - ``fess-storage``
     - Object storage (S3 / GCS)
     - ``fess-storage-s3``
   * - ``fess-sso``
     - Single sign-on authentication method
     - ``fess-sso-oidc``

All of these repositories are published at https://github.com/codelibs.

The design of the search page is not changed with plugins.
The ``fess-theme-*`` JAR theme plugins, which replaced JSPs, were removed in 15.9; the search page is now a ZIP theme consisting of ``theme.yml``, ``index.html`` and ``assets/``.
Themes are uploaded under [System] > [Theme].
For how to create one, see the `Theme Development Guide <https://fess.codelibs.org/stable/dev/theme-development.html>`__; for embedding search into an existing site, see :doc:`guide-03`.

Creating a Data Store Plugin
============================

Getting the Template
--------------------

``fess-ds-example`` is a repository published as a skeleton for data store plugins.
Its default branch tracks the version under development (15.10.0-SNAPSHOT), so to build for 15.9, use the commit aligned with 15.9.0.

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

The only difference between this commit and the default branch is two lines in ``pom.xml`` (the project version and the parent POM version).
You get the same result by staying on the default branch and changing those two places, described in the next section, for 15.9.

pom.xml
-------

The key parts of ``pom.xml`` are the following.

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

Match the ``fess-parent`` version to the version of Fess that the plugin will be installed into.
In ``fess-parent`` 15.9.0, ``fess.version`` is ``15.9.0``, so the plugin is compiled against the Fess 15.9.0 API.
Fess itself and the OpenSearch classes are supplied by Fess at runtime, so they are ``provided``.
The actual ``pom.xml`` also contains other dependencies and build settings, so start by using it as is.
The ``fess`` jar is not fetched from Maven Central but from the CodeLibs repository declared by ``fess-parent`` (``https://maven.codelibs.org/release/``).
In environments that use a proxy or a mirror, make sure this repository is reachable.

When you turn this into your own plugin, always start the ``artifactId`` with ``fess-ds-``.
As explained later, the candidates for "Handler Name" in the admin console are collected only from jars whose file names start with ``fess-ds``.

Data Store Class
----------------

A data store extends ``org.codelibs.fess.ds.AbstractDataStore`` and implements ``getName()`` and ``storeData(...)``.
The following is ``ExampleDataStore`` reduced to the skeleton of its processing.
It is meant for understanding how things work; for the build, use the repository's ``ExampleDataStore`` as is (the tests use methods that are not in the skeleton, so replacing the class makes the test compilation fail).

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
                // One record fetched from the external system (fixed values here)
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // Scripts are evaluated against "parameters + record"
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

Each part plays the following role.

- The return value of ``getName()`` is registered in ``DataStoreFactory`` as the name of this data store. By convention it returns the simple name of the class
- ``paramMap`` holds the values from the "Parameters" field of the data store configuration. Retrieve them with ``getAsString(key, defaultValue)``
- ``scriptMap`` holds the lines of the "Script" field, each in the form ``fieldName=expression``. ``convertValue()`` evaluates the expression and the result goes into the index field
- ``defaultDataMap`` holds values determined by the data store configuration, such as the configuration ID, permissions (roles), boost value and virtual hosts. Copy it first and then add each field
- ``callback.store()`` indexes the records one at a time. ``alive`` becomes ``false`` when the job is stopped, so include it in the loop condition

In other words, the plugin does not decide which record value goes into which field; the administrator decides that in the "Script" field.
The plugin's job is to fetch records and lay them out in ``resultMap``.

The actual ``ExampleDataStore`` additionally implements per-record exception handling (recording to [Failure URL]) and crawl statistics (``CrawlerStatsHelper``).
When you create your own plugin, copy ``ExampleDataStore`` rather than this skeleton, and rewrite the places marked ``// CUSTOMIZE:`` (the record retrieval part).

DI Configuration File
---------------------

Creating the class alone does not make Fess load it.
Register it as a component in ``src/main/resources/fess_ds++.xml``.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

The DI container (Lasta Di) merges any ``fess_ds++.xml`` on the class path into Fess's own ``fess_ds.xml``.
With ``<postConstruct name="register">``, ``AbstractDataStore.register()`` is called after the component is created, and the data store is registered under the name returned by ``getName()``.
If you change the class name or package, change the ``class`` attribute accordingly.

Building
--------

::

    $ mvn clean package

Three jars are created in ``target/``.
The one to install into Fess is ``fess-ds-example-15.9.0-SNAPSHOT.jar``, without ``-sources`` or ``-javadoc``.
You can check with ``unzip -l`` that it contains ``fess_ds++.xml`` and ``ExampleDataStore.class``.

Installing
==========

The easiest way is to install from the admin console.

1. Under [System] > [Plugin], click [Install]
2. Leave the drop-down on the [Remote] tab at the first entry, ``-``. If another plugin is selected, that plugin is installed instead
3. On the [Local] tab, select the jar you built in "Jar File" and click [Install]
4. Restart Fess

The uploaded jar is saved in ``app/WEB-INF/plugin/`` as ``<name>-<version>.jar``.
The name and version are read from the file name, so upload the jar without changing the file name Maven gave it.
Instead of using the admin console, you can also copy the jar directly into this directory and restart (``/usr/share/fess/app/WEB-INF/plugin/`` in the Docker image).

With Docker, ``FESS_PLUGINS`` fetches plugins published in a repository, so it cannot be used for your own jar.
Install the jar from the admin console and then restart with ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01``.
The jar is placed inside the container, so it disappears when you recreate the container with ``down`` and ``up``.
In that case, install it again.

Verifying the Plugin
====================

Checking the Handler Name
-------------------------

After the restart, open [Crawler] > [Data Store] > [Create New] and confirm that ``ExampleDataStore`` appears in the "Handler Name" drop-down.
The candidates are built from the jars in ``app/WEB-INF/plugin/`` whose file names start with ``fess-ds``.
Fess reads ``fess_ds++.xml`` inside each jar and uses the simple name of the class in the ``class`` attribute as a candidate (cached for 60 seconds).
If it does not appear, check the jar file name, the ``fess_ds++.xml`` inside the jar, and whether you restarted Fess.

Creating the Data Store Configuration
-------------------------------------

On the same screen, enter the following and click [Create].

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Value
   * - Name
     - ``Example``
   * - Handler Name
     - ``ExampleDataStore``
   * - Parameters
     - Add ``data.size=5`` on the line after the prefilled ``script_type=javascript``
   * - Script
     - Three lines: ``title=title``, ``content=body`` and ``url=url``

When the right-hand side of a script line matches a record key (``title``, ``body``, ``url``), ``convertValue()`` returns that value as is without using a script engine.
If you write an expression such as ``content=title + " " + body``, it is evaluated by the engine specified in ``script_type``.
If you remove ``script_type``, the script is treated as ``groovy``, and evaluating expressions fails in environments without ``fess-script-groovy``, so keep it.

``url`` is required.
``callback.store()`` does not accept a document without ``url`` and throws an exception.

Running the Job
---------------

1. In the [Crawler] > [Data Store] list, click ``Example`` and then click [Create New Job]
2. The scheduler creation screen opens; click [Create] without changing anything
3. Under [System] > [Scheduler], open the job you created and click [Start Now]

Checking the Results
--------------------

Check the following four points.

1. Under [System Info] > [Job Log], the job status is "OK"
2. Under [System Info] > [Crawling Info], "Index Size (Data Store)" for that session is ``5``
3. Nothing is recorded under [System Info] > [Failure URL]
4. Searching for ``Sample`` under [System Info] > [Search] shows five results, ``Sample 0`` to ``Sample 4``

A job status of "OK" does not necessarily mean that the data store processing succeeded.
For example, if you remove ``url=url`` from the script and run the job, ``callback.store()`` throws an exception for every record and nothing is indexed.
``ExampleDataStore`` catches exceptions per record, so ``record:0`` to ``record:4`` are recorded under [Failure URL] and WARN messages appear in ``fess-crawler.log``, but the job log still shows "OK".
With code that does not catch exceptions, like the skeleton, the whole configuration fails and only one entry is recorded under [Failure URL], in the form ``D<configId>:Example``.
The verification steps and log locations are summarized in the section on checking the results in :doc:`datastore-basics`.

Once you have confirmed all this, replace the record retrieval part, such as ``createSourceRecord()``, with code that reads your actual API or files.
Do not hard-code the connection target or credentials of the external system; receive them through ``paramMap`` from the "Parameters" field.

The template's ``src/test`` contains tests that use UTFlute's ``LastaDiTestCase``.
A test class that implements ``IndexUpdateCallback`` collects the ``dataMap`` passed to ``store()``, and the tests check the number of documents and the field values.
This lets you run ``mvn test`` without OpenSearch.
When you rewrite the record retrieval part, update these tests as well.

Processing Documents Before Indexing with an Ingester
=====================================================

An Ingester is called just before a document is sent to the index, in every kind of crawl: data store, web and file system.
It is used for processing such as adding a common field to every document or normalizing values.
There is no way to enable or disable it per configuration; once installed, it applies to all crawls.

Extend ``org.codelibs.fess.ingest.Ingester`` and override only the ``process`` methods you need.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Method
     - When it is called
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - Data store crawls (inside ``callback.store()``)
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - When web and file crawls index a document
   * - ``process(ResultData target, ResponseData responseData)``
     - When web and file crawls process a fetched response
   * - ``protected process(Map<String, Object> target)``
     - The method that the two ``Map`` versions above call by default. Override only this one when you want the processing to apply to both data store and web/file crawls

The following is ``ExampleIngester`` from ``fess-ingest-example``, reduced to the data store processing.

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

Registration is done in ``src/main/resources/fess_ingest++.xml``.
It has the same form as ``fess_ds++.xml``: a component named ``exampleIngester`` with ``<postConstruct name="register">``.
``Ingester.register()`` adds the Ingester itself to ``IngestFactory``.

Getting the template, building, installing and restarting follow the same steps as for the data store (the commit for 15.9 is ``8a1e45ddb63a118802287120effd3ce49fb60bfb`` and the jar is ``fess-ingest-example-15.9.0-SNAPSHOT.jar``).
For your own plugin, start the artifactId with ``fess-ingest-``.

Keep the following points in mind when implementing it.

- Always return ``target`` after modifying it. The return value is passed as is to the next Ingester and to the indexer, with no ``null`` check. Returning ``null`` does not exclude the document; it breaks the indexing process
- Multiple Ingesters run in ascending order of ``priority`` (default 99). Each Ingester receives the ``target`` modified by the previous one
- If ``process`` throws an exception, Fess logs a WARN and moves on to the next Ingester. Indexing of the document does not stop. Changes made to ``target`` before the exception remain

To verify it, run the job of the data store configuration created in "Verifying the Plugin" above once more.
Ingesters run in the crawler process, so if ``fess-crawler.log`` contains a ``DATASTORE CRAWL:`` line for each document, the Ingester is being called.
The repository's ``ExampleIngester`` also logs documents from web and file crawls one by one as ``WEB/FILE CRAWL:``.
Because it affects every crawl, delete it under [System] > [Plugin] once you have finished checking, and restart Fess.

Upgrading Fess
==============

Build a plugin with the ``fess-parent`` of the same minor version as the Fess it is installed into (15.9.x for Fess 15.9).
Published plugins are also released in a matching version for each Fess minor version.

When you upgrade Fess to 15.10, change the ``fess-parent`` version in ``pom.xml`` accordingly and rebuild.
In the [System] > [Plugin] list, delete the old jar, install the new one, and restart.
``bin/fess-setup upgrade plugins`` fetches new versions from the plugin repository, so it cannot update your own plugins that are not in the repository.

What to Read Next
=================

- To learn more about data store parameters, scripts, permissions and schedules: :doc:`datastore-basics`
- To see configuration examples for published data store plugins: :doc:`guide-06`, :doc:`guide-07` and :doc:`guide-12`
- To change the look of the search page: :doc:`guide-03`
- To enable AI search mode with an LLM plugin: :doc:`guide-19`
- To use a web application plugin (MCP server): :doc:`guide-20`

References
==========

- `Plugin Architecture <https://fess.codelibs.org/stable/dev/plugin-architecture.html>`__
- `Data Store Plugin Development <https://fess.codelibs.org/stable/dev/datastore-plugin.html>`__
- `Ingest Plugin <https://fess.codelibs.org/stable/dev/ingest-plugin.html>`__
- `Theme Development Guide <https://fess.codelibs.org/stable/dev/theme-development.html>`__
- `Plugin (admin console) <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `fess-ds-example (GitHub) <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example (GitHub) <https://github.com/codelibs/fess-ingest-example>`__
