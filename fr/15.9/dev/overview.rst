====================================================
Aperçu de la documentation pour les développeurs
====================================================

Vue d'ensemble
==============

Cette section décrit le développement d'extensions pour |Fess|.
Elle fournit des informations pour étendre |Fess|, telles que le développement
de plugins, la création de connecteurs personnalisés et la personnalisation
de thèmes.

Public cible
============

- Développeurs souhaitant développer des fonctionnalités personnalisées pour |Fess|
- Développeurs souhaitant créer des plugins
- Développeurs souhaitant comprendre le code source de |Fess|

Connaissances préalables
-------------------------

- Connaissances de base de Java 21
- Bases de Maven (système de build)
- Expérience en développement d'applications web
- Connaissances de base d'OpenSearch (|Fess| utilise OpenSearch comme moteur de recherche)

Environnement de développement
===============================

Environnement recommandé
--------------------------

- **JDK** : OpenJDK 21 ou supérieur
- **IDE** : IntelliJ IDEA / Eclipse / VS Code
- **Outil de build** : Maven (le build n'impose pas de version minimale, mais une version 3.x récente prenant en charge Java 21 est recommandée)
- **Git** : gestion de versions
- **OpenSearch** : moteur de recherche backend (si vous démarrez depuis l'IDE, les modules et plugins nécessaires sont téléchargés lors du build)

Installation
-------------

|Fess| se construit comme un projet Maven. Lors du développement, il est plus
simple de le démarrer depuis l'IDE.

1. Récupération du code source :

   ::

       git clone https://github.com/codelibs/fess.git

2. Importation dans l'IDE :

   Importez le répertoire récupéré dans l'IDE en tant que projet Maven.

3. Téléchargement des modules et plugins pour OpenSearch :

   Uniquement lors de la première exécution, récupérez les modules et plugins
   du moteur de recherche dans le répertoire ``plugins`` avec la commande
   suivante :

   ::

       mvn antrun:run

4. Démarrage du serveur de développement (depuis l'IDE) :

   Exécutez ou déboguez ``org.codelibs.fess.FessBoot`` dans l'IDE, puis ouvrez
   http://localhost:8080/ dans votre navigateur.
   L'écran d'administration se trouve à l'adresse http://localhost:8080/admin/
   (compte initial : ``admin`` / ``admin``).

5. Construction du package (création de la distribution) :

   Si vous avez besoin d'un package de distribution, exécutez le goal
   ``package``. Le résultat est généré dans ``target/releases`` (ajoutez
   ``-DskipTests`` pour ignorer les tests unitaires).

   ::

       mvn package

   Une fois la distribution générée décompressée, le script de démarrage
   ``bin/fess`` est disponible.

   ::

       unzip target/releases/fess-*.zip
       ./fess-*/bin/fess

.. note::

    Le script de démarrage ``bin/fess`` est inclus dans le package de
    distribution (zip/rpm/deb).
    Le simple fait d'exécuter ``mvn package`` dans l'arborescence source ne
    génère pas ``bin/fess`` à la racine du dépôt.
    Pour développer à partir des sources, exécutez ``FessBoot`` dans l'IDE
    comme indiqué ci-dessus, ou utilisez le ``bin/fess`` de la distribution
    décompressée.

Aperçu de l'architecture
=========================

|Fess| est composé des composants principaux suivants :

Structure des composants
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - Couche Web
     - Implémentation MVC avec le framework LastaFlute
   * - Couche Service
     - Logique métier
   * - Couche d'accès aux données
     - Accès type-safe à OpenSearch via DBFlute (ESFlute/FreeGen)
   * - Crawler
     - Collecte de contenu via la bibliothèque fess-crawler
   * - Moteur de recherche
     - Recherche plein texte avec OpenSearch

Frameworks principaux
-----------------------

- **LastaFlute** : framework web (actions, formulaires, validation)
- **DBFlute** : framework d'accès aux données. Les classes d'accès type-safe
  pour OpenSearch (``Bhv`` / ``ConditionBean``) sont générées par la
  fonctionnalité FreeGen de DBFlute et les templates ESFlute (régénération
  via ``mvn dbflute:freegen``)
- **Lasta Di** : conteneur d'injection de dépendances

Structure des répertoires
===========================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Contrôleurs (Action)
    │   │   ├── service/     # Services
    │   │   ├── logic/       # Logique
    │   │   └── pager/       # Pagination
    │   ├── api/             # API REST (api/v2, etc.)
    │   ├── helper/          # Classes utilitaires
    │   ├── crawler/         # Fonctionnalités liées au crawler
    │   ├── indexer/         # Traitement d'indexation
    │   ├── opensearch/      # Accès OpenSearch (généré par ESFlute/FreeGen)
    │   ├── llm/             # Intégration LLM
    │   ├── ds/              # Connecteurs de datastore
    │   ├── ingest/          # Ingest (traitement des données lors de l'indexation)
    │   ├── script/          # Moteur de script
    │   ├── entity/          # Entités
    │   └── mylasta/         # Configuration LastaFlute (DI, messages, configuration type-safe)
    ├── src/main/resources/
    │   ├── fess_config.properties  # Configuration
    │   └── fess_*.xml              # Configuration DI (app.xml, fess_ds.xml, etc.)
    └── src/main/webapp/
        └── WEB-INF/view/    # Templates JSP

Points d'extension
====================

|Fess| fournit les points d'extension suivants :

Plugins
--------

Vous pouvez ajouter des fonctionnalités à l'aide de plugins.

- **Plugin DataStore** : exploration depuis de nouvelles sources de données (hérite de ``AbstractDataStore``)
- **Plugin de moteur de script** : prise en charge de nouveaux langages de script (implémente ``ScriptEngine``)
- **Plugin d'application Web** : extension de l'interface web (surcharge de composants Lasta Di et fusion de ressources)
- **Plugin Ingest** : traitement des données lors de l'indexation (hérite de ``Ingester``)

Détails : :doc:`plugin-architecture`

.. note::

    |Fess| lui-même est empaqueté sous forme de ``war``. Si vous ne parvenez
    pas à résoudre |Fess| comme dépendance lors de la construction locale
    d'un plugin, modifiez temporairement ``<packaging>`` dans ``pom.xml`` en
    ``jar``, exécutez ``mvn clean install -DskipTests``, puis revenez à
    ``war``.

Thèmes
-------

Vous pouvez personnaliser le design de l'écran de recherche.

Détails : :doc:`theme-development`

Configuration
---------------

``fess_config.properties`` permet de personnaliser de nombreux comportements.

Détails : :doc:`../config/intro`

Développement de plugins
==========================

Pour plus de détails sur le développement de plugins, consultez :

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`datastore-plugin` - Développement de plugins DataStore
- :doc:`script-engine-plugin` - Plugin de moteur de script
- :doc:`webapp-plugin` - Plugin d'application Web
- :doc:`ingest-plugin` - Plugin Ingest

Développement de thèmes
=========================

- :doc:`theme-development` - Personnalisation des thèmes

Bonnes pratiques
==================

Conventions de codage
-----------------------

- Suivre le style de code existant de |Fess|
- Formater le code avec ``mvn formatter:format``
- Ajouter les en-têtes de licence avec ``mvn license:format``

Tests
------

- Tests unitaires (``*Test.java``) : exécutés via ``mvn test`` dans le profil ``build`` par défaut
- Tests d'intégration (``*Tests.java``) : exécutés via ``mvn test -P integrationTests``.
  L'exécution des tests d'intégration nécessite un serveur |Fess| et une instance OpenSearch en cours de fonctionnement

Journalisation
---------------

- Utilise Log4j2
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- Ne pas journaliser d'informations sensibles

Ressources
===========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
