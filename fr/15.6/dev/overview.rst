==================================
Vue d'ensemble developpeur
==================================

Vue d'ensemble
==============

Cette section decrit le developpement d'extensions pour |Fess|.
Elle fournit des informations sur le developpement de plugins, la creation de connecteurs personnalises,
la personnalisation de themes, etc.

Public cible
============

- Developpeurs souhaitant creer des fonctionnalites personnalisees pour |Fess|
- Developpeurs souhaitant creer des plugins
- Developpeurs souhaitant comprendre le code source de |Fess|

Connaissances prealables
------------------------

- Connaissances de base de Java 21
- Bases de Maven (systeme de build)
- Experience en developpement d'applications web

Environnement de developpement
==============================

Environnement recommande
------------------------

- **JDK**: OpenJDK 21 ou superieur
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Outil de build**: Maven 3.9 ou superieur
- **Git**: Gestion de versions

Configuration
-------------

1. Recuperation du code source:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. Build:

::

    mvn package -DskipTests

3. Demarrage du serveur de developpement:

::

    ./bin/fess

Apercu de l'architecture
========================

|Fess| est compose des composants principaux suivants:

Structure des composants
------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - Couche Web
     - Implementation MVC avec le framework LastaFlute
   * - Couche Service
     - Logique metier
   * - Couche d'acces aux donnees
     - Integration OpenSearch via DBFlute
   * - Crawler
     - Collecte de contenu via la bibliotheque fess-crawler
   * - Moteur de recherche
     - Recherche plein texte avec OpenSearch

Frameworks principaux
---------------------

- **LastaFlute**: Framework web (actions, formulaires, validation)
- **DBFlute**: Framework d'acces aux donnees (integration OpenSearch)
- **Lasta Di**: Conteneur d'injection de dependances

Structure des repertoires
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

Vous pouvez ajouter des fonctionnalites via des plugins.

- **Plugins DataStore**: Crawl depuis de nouvelles sources de donnees
- **Plugins Script Engine**: Support de nouveaux langages de script
- **Plugins WebApp**: Extension de l'interface web
- **Plugins Ingest**: Traitement des donnees lors de l'indexation

Details: :doc:`plugin-architecture`

Themes
------

Vous pouvez personnaliser le design de l'ecran de recherche.

Details: :doc:`theme-development`

Configuration
-------------

De nombreux comportements peuvent etre personnalises via ``fess_config.properties``.

Details: :doc:`../config/intro`

Developpement de plugins
========================

Pour plus de details sur le developpement de plugins, consultez:

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`datastore-plugin` - Developpement de plugins DataStore
- :doc:`script-engine-plugin` - Plugins Script Engine
- :doc:`webapp-plugin` - Plugins WebApp
- :doc:`ingest-plugin` - Plugins Ingest

Developpement de themes
=======================

- :doc:`theme-development` - Personnalisation des themes

Bonnes pratiques
================

Conventions de codage
---------------------

- Suivre le style de code existant de |Fess|
- Formater le code avec ``mvn formatter:format``
- Ajouter les en-tetes de licence avec ``mvn license:format``

Tests
-----

- Ecrire des tests unitaires (``*Test.java``)
- Les tests d'integration sont ``*Tests.java``

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
