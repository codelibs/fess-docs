==================================
Vue d'ensemble développeur
==================================

Vue d'ensemble
==============

Cette section décrit le développement d'extensions pour |Fess|.
Elle fournit des informations sur le développement de plugins, la création de connecteurs personnalisés,
la personnalisation de thèmes, etc.

Public cible
============

- Développeurs souhaitant créer des fonctionnalités personnalisées pour |Fess|
- Développeurs souhaitant créer des plugins
- Développeurs souhaitant comprendre le code source de |Fess|

Connaissances préalables
------------------------

- Connaissances de base de Java 21
- Bases de Maven (système de build)
- Expérience en développement d'applications web

Environnement de développement
==============================

Environnement recommandé
------------------------

- **JDK**: OpenJDK 21 ou supérieur
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Outil de build**: Maven 3.9 ou supérieur
- **Git**: Gestion de versions

Configuration
-------------

1. Récupération du code source:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. Build:

::

    mvn package -DskipTests

3. Démarrage du serveur de développement:

::

    ./bin/fess

Aperçu de l'architecture
========================

|Fess| est composé des composants principaux suivants:

Structure des composants
------------------------

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
     - Intégration OpenSearch via DBFlute
   * - Crawler
     - Collecte de contenu via la bibliothèque fess-crawler
   * - Moteur de recherche
     - Recherche plein texte avec OpenSearch

Frameworks principaux
---------------------

- **LastaFlute**: Framework web (actions, formulaires, validation)
- **DBFlute**: Framework d'accès aux données (intégration OpenSearch)
- **Lasta Di**: Conteneur d'injection de dépendances

Structure des répertoires
=========================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Controleurs (Action)
    │   │   ├── service/     # Services
    │   │   └── pager/       # Pagination
    │   ├── api/             # API REST
    │   ├── helper/          # Classes utilitaires
    │   ├── crawler/         # Fonctionnalites du crawler
    │   ├── opensearch/      # Integration OpenSearch (genere par DBFlute)
    │   ├── llm/             # Integration LLM
    │   └── ds/              # Connecteurs de datastore
    ├── src/main/resources/
    │   ├── fess_config.properties  # Configuration
    │   └── fess_*.xml              # Configuration DI
    └── src/main/webapp/
        └── WEB-INF/view/    # Templates JSP

Points d'extension
==================

|Fess| fournit les points d'extension suivants:

Plugins
-------

Vous pouvez ajouter des fonctionnalités via des plugins.

- **Plugins DataStore**: Crawl depuis de nouvelles sources de données
- **Plugins Script Engine**: Support de nouveaux langages de script
- **Plugins WebApp**: Extension de l'interface web
- **Plugins Ingest**: Traitement des données lors de l'indexation

Détails: :doc:`plugin-architecture`

Thèmes
------

Vous pouvez personnaliser le design de l'écran de recherche.

Détails: :doc:`theme-development`

Configuration
-------------

De nombreux comportements peuvent être personnalisés via ``fess_config.properties``.

Détails: :doc:`../config/intro`

Développement de plugins
========================

Pour plus de détails sur le développement de plugins, consultez:

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`datastore-plugin` - Développement de plugins DataStore
- :doc:`script-engine-plugin` - Plugins Script Engine
- :doc:`webapp-plugin` - Plugins WebApp
- :doc:`ingest-plugin` - Plugins Ingest

Développement de thèmes
=======================

- :doc:`theme-development` - Personnalisation des thèmes

Bonnes pratiques
================

Conventions de codage
---------------------

- Suivre le style de code existant de |Fess|
- Formater le code avec ``mvn formatter:format``
- Ajouter les en-têtes de licence avec ``mvn license:format``

Tests
-----

- Écrire des tests unitaires (``*Test.java``)
- Les tests d'intégration sont ``*Tests.java``

Journalisation
--------------

- Utiliser Log4j2
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- Ne pas journaliser d'informations sensibles

Ressources
==========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
