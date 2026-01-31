==================================
Architecture des plugins
==================================

Vue d'ensemble
==============

Le systeme de plugins de |Fess| permet d'etendre les fonctionnalites de base.
Les plugins sont distribues sous forme de fichiers JAR et charges dynamiquement.

Types de plugins
================

|Fess| supporte les types de plugins suivants:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Type
     - Description
   * - DataStore
     - Recuperation de contenu depuis de nouvelles sources de donnees (Box, Slack, etc.)
   * - Script Engine
     - Support de nouveaux langages de script
   * - WebApp
     - Extension de l'interface web
   * - Ingest
     - Traitement des donnees lors de l'indexation

Structure d'un plugin
=====================

Structure de base
-----------------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # Implementation du DataStore
        └── ExampleDataStoreHandler.java # Handler (optionnel)

Exemple de pom.xml
------------------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.5.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.5.0</fess.version>
            <java.version>21</java.version>
        </properties>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <version>${fess.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

Enregistrement du plugin
========================

Enregistrement dans le conteneur DI
-----------------------------------

Les plugins sont enregistres dans des fichiers de configuration comme ``fess_ds.xml``:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

Enregistrement automatique
--------------------------

De nombreux plugins s'enregistrent automatiquement avec l'annotation ``@PostConstruct``:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

Cycle de vie du plugin
======================

Initialisation
--------------

1. Le fichier JAR est charge
2. Le conteneur DI initialise les composants
3. Les methodes ``@PostConstruct`` sont appelees
4. Le plugin est enregistre dans le gestionnaire

Terminaison
-----------

1. Les methodes ``@PreDestroy`` sont appelees (si definies)
2. Nettoyage des ressources

Dependances
===========

Dependance avec Fess
--------------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
        <scope>provided</scope>
    </dependency>

Bibliotheques externes
----------------------

Les plugins peuvent inclure leurs propres dependances:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Les bibliotheques dependantes peuvent etre distribuees avec le JAR du plugin,
ou vous pouvez creer un fat JAR avec Maven Shade Plugin.

Recuperation de la configuration
================================

Recuperation depuis FessConfig
------------------------------

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(DataConfig dataConfig, IndexUpdateCallback callback,
                Map<String, String> paramMap, Map<String, String> scriptMap,
                Map<String, Object> defaultDataMap) {

            // Recuperation des parametres
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // Recuperation de FessConfig
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Build et installation
=====================

Build
-----

::

    mvn clean package

Installation
------------

1. **Depuis l'interface d'administration**:

   - "Systeme" -> "Plugins" -> "Installer"
   - Entrer le nom du plugin et installer

2. **Ligne de commande**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **Manuellement**:

   - Copier le fichier JAR dans le repertoire ``plugins/``
   - Redemarrer |Fess|

Debogage
========

Sortie de logs
--------------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

Mode developpement
------------------

En developpement, vous pouvez lancer |Fess| depuis l'IDE pour deboguer:

1. Executer la classe ``FessBoot`` en mode debug
2. Inclure les sources du plugin dans le projet
3. Definir des points d'arret

Liste des plugins publies
=========================

Principaux plugins publies par le projet |Fess|:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Description
   * - fess-ds-box
     - Connecteur Box.com
   * - fess-ds-dropbox
     - Connecteur Dropbox
   * - fess-ds-slack
     - Connecteur Slack
   * - fess-ds-atlassian
     - Connecteur Confluence/Jira
   * - fess-ds-git
     - Connecteur de depot Git
   * - fess-theme-*
     - Themes personnalises

Ces plugins sont publies sur `GitHub <https://github.com/codelibs>`__ comme reference de developpement.

Informations complementaires
============================

- :doc:`datastore-plugin` - Developpement de plugins DataStore
- :doc:`script-engine-plugin` - Plugins Script Engine
- :doc:`webapp-plugin` - Plugins WebApp
- :doc:`ingest-plugin` - Plugins Ingest
