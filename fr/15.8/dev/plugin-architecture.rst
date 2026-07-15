=========================
Architecture des plugins
=========================

Aperçu
======

Le système de plugins de |Fess| permet d'étendre les fonctionnalités du cœur.
Les plugins sont distribués sous forme de fichiers JAR ; lorsqu'ils sont
ajoutés au classpath, leurs composants sont chargés par le conteneur DI
(Lasta Di) puis enregistrés auprès de la fabrique ou du gestionnaire
correspondant.

Types de plugins
=================

|Fess| détermine le type d'un plugin à partir du préfixe du nom de
l'artefact (``PluginHelper.ArtifactType``). Les principaux types sont les
suivants :

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Type
     - Préfixe
     - Description
   * - DataStore
     - ``fess-ds-*``
     - Récupération de contenu depuis de nouvelles sources de données (Box, Slack, Git, etc.)
   * - Application Web
     - ``fess-webapp-*``
     - Extension de l'interface Web ou des fonctionnalités de recherche
   * - Moteur de script
     - ``fess-script-*``
     - Prise en charge de nouveaux langages de script
   * - Ingest
     - ``fess-ingest-*``
     - Traitement des documents lors de leur enregistrement dans l'index
   * - Thème
     - ``fess-theme-*``
     - Personnalisation du design de l'écran de recherche
   * - Miniature
     - ``fess-thumbnail-*``
     - Ajout de méthodes de génération de miniatures
   * - LLM
     - ``fess-llm-*``
     - Ajout de fournisseurs LLM utilisés pour le RAG/chat
   * - Crawler
     - ``fess-crawler-*``
     - Extension des clients du crawler

Structure d'un plugin
======================

Structure de base
-----------------

En prenant comme exemple `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__,
le modèle d'implémentation d'un plugin DataStore, un plugin se compose d'une
« classe d'implémentation » et d'un « fichier d'enregistrement DI » :

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # Implémentation du DataStore
        └── resources/
            └── fess_ds++.xml             # Enregistrement du composant DI

Exemple de pom.xml
------------------

Le plugin est construit comme un jar ayant ``fess-parent`` pour POM parent.
Les bibliothèques telles que ``fess`` ou ``opensearch``, fournies à
l'exécution par |Fess| lui-même, doivent être déclarées avec la portée
``provided``. Le numéro de version et les paramètres de build (formateur,
en-têtes de licence, etc.) sont hérités du POM parent.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
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

.. note::

   Sur les branches en cours de développement, la version comporte le
   suffixe ``-SNAPSHOT``, par exemple ``15.8.0-SNAPSHOT``. Les bibliothèques
   dépendantes propres au plugin sont déclarées comme des dépendances Maven
   classiques. Comme elles ne sont pas incluses dans |Fess| lui-même, elles
   doivent être distribuées avec le plugin.

Enregistrement du plugin
=========================

Enregistrement dans le conteneur DI
------------------------------------

Un plugin enregistre ses composants dans un fichier de configuration DI dont
le nom se termine par ``++``, comme ``fess_ds++.xml``. Lasta Di fusionne
automatiquement tout fichier suffixé par ``++`` trouvé sur le classpath avec
le fichier de configuration correspondant de |Fess| lui-même (``fess_ds.xml``
dans cet exemple). Ce mécanisme permet à un plugin d'ajouter ses propres
composants sans modifier les fichiers de |Fess| lui-même.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Le fichier cible de la fusion diffère selon le type de plugin. Par exemple,
un moteur de script utilise ``fess_se++.xml``, un plugin Ingest utilise
``fess_ingest++.xml``, un fournisseur LLM utilise ``fess_llm++.xml``, et une
application Web utilise ``app++.xml``.

Initialisation du composant
----------------------------

``<postConstruct name="register">`` est un paramètre de cycle de vie de
Lasta Di indiquant la méthode à appeler après la création du composant. Dans
le cas d'un DataStore, la méthode ``register()`` fournie par
``AbstractDataStore`` est appelée et enregistre celui-ci auprès de
``DataStoreFactory`` :

.. code-block:: java

    // Implémentation fournie par AbstractDataStore (il n'est généralement pas nécessaire de la surcharger)
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   Il ne s'agit pas de l'annotation Java ``@PostConstruct``, mais d'une
   initialisation réalisée via l'élément ``<postConstruct>`` du fichier de
   configuration DI. Le nom enregistré correspond à la valeur de retour de
   ``getName()`` ; c'est ce nom qui sera utilisé pour sélectionner le plugin
   dans l'écran d'administration.

Cycle de vie du plugin
=======================

Initialisation
--------------

1. Le fichier JAR du plugin est ajouté au classpath.
2. Le conteneur DI fusionne les fichiers ``fess_*++.xml`` et génère les composants.
3. La méthode indiquée dans ``<postConstruct>`` (par exemple ``register``) est appelée.
4. Le plugin est enregistré auprès de la fabrique ou du gestionnaire correspondant.

Arrêt
-----

1. À l'arrêt du conteneur DI, la méthode indiquée dans ``<preDestroy>`` est
   appelée (si elle est définie).
2. Nettoyage des ressources.

.. note::

   Dans le cas d'un DataStore, ``AbstractDataStore.stop()`` positionne un
   indicateur d'arrêt sur l'exploration en cours, ce qui permet à la boucle
   de traitement des enregistrements de se terminer de manière sûre.

Dépendances
============

Dépendance envers le cœur de Fess
-----------------------------------

Les classes du cœur de |Fess| étant présentes sur le classpath du serveur au
moment de l'exécution, elles sont déclarées comme dépendance avec la portée
``provided`` (elles ne doivent pas être incluses dans le JAR du plugin).

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

Bibliothèques externes
-----------------------

Un plugin peut inclure ses propres bibliothèques dépendantes :

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Comme elles ne sont pas incluses dans |Fess| lui-même, elles doivent être
distribuées avec le plugin.

Récupération de la configuration
==================================

Récupération des paramètres et de FessConfig
----------------------------------------------

Dans la méthode ``storeData()`` d'un DataStore, les paramètres configurés
dans l'écran d'administration sont récupérés depuis ``DataStoreParams``.
Utilisez ``getAsString()`` pour récupérer les valeurs (``DataStoreParams``
n'implémentant pas ``Map``, ``get()`` ne retourne pas de chaîne de
caractères). Les valeurs de configuration de |Fess| peuvent également être
récupérées via ``ComponentUtil.getFessConfig()`` :

.. code-block:: java

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

            // Récupération des paramètres
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // Récupération de FessConfig
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Pour plus de détails sur l'implémentation de ``storeData()`` (récupération
des données, évaluation du script, enregistrement dans l'index), reportez-vous
à :doc:`datastore-plugin`.

Build et installation
======================

Build
-----

::

    mvn clean package

Le fichier JAR (par exemple ``fess-ds-example-15.8.0.jar``) est généré dans
le répertoire ``target/``.

Installation
------------

1. **Depuis l'écran d'administration** :

   - Ouvrez « Système » → « Plugin » → « Installer ».
   - Sélectionnez un plugin dans la liste du dépôt de plugins, ou téléversez
     le fichier JAR construit pour l'installer.

2. **Manuellement** :

   - Copiez le fichier JAR dans le répertoire ``app/WEB-INF/plugin/``.
   - Redémarrez |Fess|.

Pour plus de détails sur la procédure d'installation, reportez-vous à
:doc:`../admin/plugin-guide`.

Débogage
========

Journalisation
---------------

|Fess| utilise Log4j2. Le logger s'obtient avec ``LogManager.getLogger()`` :

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   N'écrivez pas d'informations sensibles telles que mots de passe ou
   jetons dans les journaux.

Mode de développement
-----------------------

Lors du développement, vous pouvez démarrer |Fess| depuis un IDE pour le
déboguer :

1. Exécutez la classe ``org.codelibs.fess.FessBoot`` en mode débogage.
2. Incluez les sources du plugin dans le projet.
3. Définissez des points d'arrêt.

Liste des plugins publiés
==========================

De nombreux plugins sont publiés par le projet |Fess|. Voici quelques
exemples représentatifs (cette liste n'est pas exhaustive) :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Description
   * - ``fess-ds-box``
     - Connecteur Box
   * - ``fess-ds-dropbox``
     - Connecteur Dropbox
   * - ``fess-ds-slack``
     - Connecteur Slack
   * - ``fess-ds-atlassian``
     - Connecteur JIRA / Confluence
   * - ``fess-ds-git``
     - Connecteur de dépôt Git
   * - ``fess-llm-openai``
     - Fournisseur LLM OpenAI
   * - ``fess-theme-*``
     - Thèmes personnalisés

D'autres connecteurs DataStore tels que ``fess-ds-csv`` / ``fess-ds-db`` /
``fess-ds-json`` / ``fess-ds-microsoft365`` / ``fess-ds-sharepoint``, ainsi
que des fournisseurs LLM tels que ``fess-llm-ollama`` / ``fess-llm-gemini``,
sont également publiés. Ces plugins sont disponibles sur
`GitHub <https://github.com/codelibs>`__ comme référence pour le
développement.

Informations complémentaires
=============================

- :doc:`datastore-plugin` - Développement de plugins DataStore
- :doc:`script-engine-plugin` - Plugin de moteur de script
- :doc:`webapp-plugin` - Plugin d'application Web
- :doc:`ingest-plugin` - Plugin Ingest
- :doc:`theme-development` - Personnalisation des thèmes
- :doc:`../admin/plugin-guide` - Installation des plugins
