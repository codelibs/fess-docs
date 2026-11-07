=================================================
Partie 17 : Étendre la recherche avec des plugins
=================================================

Introduction
============

Fess prend en charge de nombreuses sources de données par défaut, mais il peut être nécessaire de l'étendre via des plugins pour s'adapter aux systèmes et formats de données spécifiques à l'entreprise.

Cet article explique l'architecture des plugins de Fess et présente comment implémenter des plugins de sources de données personnalisées et des plugins Ingest.

Public cible
============

- Personnes souhaitant connecter Fess à des sources de données personnalisées
- Développeurs Java intéressés par le développement de plugins
- Personnes souhaitant comprendre l'architecture interne de Fess

Architecture des plugins
=========================

Fess propose les types de plugins suivants.

.. list-table:: Types de plugins
   :header-rows: 1
   :widths: 25 35 40

   * - Type
     - Rôle
     - Exemples
   * - Data Store (fess-ds-\*)
     - Récupération de données depuis des sources externes
     - Slack, Salesforce, DB
   * - Ingest (fess-ingest-\*)
     - Traitement et transformation des données collectées
     - Example
   * - Theme (fess-theme-\*)
     - Design de l'interface de recherche
     - Simple, Code Search
   * - Script (fess-script-\*)
     - Prise en charge des langages de script
     - OGNL
   * - Web App (fess-webapp-\*)
     - Extensions d'applications web
     - MCP Server

Déploiement des plugins
-----------------------

Les plugins sont fournis sous forme de fichiers JAR et placés dans le répertoire de plugins de Fess.
Ils peuvent être installés et gérés depuis [Système] > [Plugins] dans la console d'administration.

Développement d'un plugin de source de données personnalisée
=============================================================

Cette section explique le processus de développement d'un plugin de source de données, en supposant l'existence d'un système de gestion documentaire interne propriétaire.

Structure du projet
-------------------

Créez un projet Maven en vous référant à un plugin Data Store existant (par exemple, fess-ds-git).

::

    fess-ds-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── java/
                └── org/codelibs/fess/ds/custom/
                    └── CustomDataStore.java

Configuration du pom.xml
------------------------

Spécifiez fess-parent comme POM parent et configurez les dépendances requises.

.. code-block:: xml

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.5.0</version>
    </parent>

    <artifactId>fess-ds-custom</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

Implémentation de la classe Data Store
----------------------------------------

Le cœur d'un plugin Data Store est la classe qui récupère les données et enregistre les documents dans Fess.

Les points clés de l'implémentation sont les suivants :

1. Connexion et authentification avec le système externe
2. Récupération des données (appels API, lecture de fichiers, etc.)
3. Conversion des données récupérées au format de document Fess
4. Enregistrement des documents

**Mappage des champs**

Mappez les données récupérées aux champs de Fess.
Les principaux champs sont les suivants :

- ``title`` : Titre du document
- ``url`` : URL du document (destination du lien dans les résultats de recherche)
- ``content`` : Corps du document (cible de recherche)
- ``mimetype`` : Type MIME
- ``last_modified`` : Date et heure de dernière modification

Compilation et déploiement
--------------------------

::

    $ mvn clean package

Placez le fichier JAR généré dans le répertoire de plugins de Fess et redémarrez Fess.

Développement d'un plugin Ingest
==================================

Un plugin Ingest est un mécanisme permettant de traiter et de transformer les documents obtenus par collecte avant leur enregistrement dans l'index.

Cas d'utilisation
-----------------

- Ajout de champs supplémentaires aux documents collectés
- Nettoyage du texte du corps (suppression de caractères inutiles)
- Enrichissement via des API externes (traduction, classification, etc.)
- Sortie de logs (pour le débogage)

Points d'implémentation
-----------------------

Dans un plugin Ingest, vous accédez aux données du document juste avant son enregistrement dans l'index et effectuez le traitement de transformation.

Par exemple, vous pouvez implémenter un traitement qui ajoute des métadonnées de nom d'organisation à tous les documents, ou un traitement qui supprime des motifs spécifiques du texte du corps.

Développement d'un plugin de thème
====================================

Si vous souhaitez personnaliser entièrement le design de l'interface de recherche, développez un plugin de thème.

Structure du thème
------------------

Un plugin de thème est composé de fichiers JSP, CSS, JavaScript et de fichiers image.

::

    fess-theme-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── resources/
                ├── css/
                ├── js/
                ├── images/
                └── view/
                    ├── index.jsp
                    ├── search.jsp
                    └── header.jsp

Personnalisez le design en modifiant les fichiers JSP et CSS en vous référant aux thèmes existants.

Bonnes pratiques de développement
==================================

Référence aux plugins existants
-------------------------------

Lors du développement d'un nouveau plugin, il est fortement recommandé de consulter le code source des plugins existants.
Le code source de tous les plugins est disponible sur le dépôt GitHub de CodeLibs.

Par exemple, ``fess-ds-git`` et ``fess-ds-slack`` constituent de bonnes références pour le développement de plugins Data Store.

Tests
-----

Testez les plugins selon les perspectives suivantes :

- Tests de connexion avec les systèmes externes
- Précision de la transformation des données
- Gestion des erreurs (échecs de connexion, données invalides, etc.)
- Performance (temps de traitement pour de grands volumes de données)

Compatibilité des versions
--------------------------

Vérifiez la compatibilité des plugins lors de la mise à jour de Fess.
Des modifications de l'API peuvent survenir lors des mises à jour de version majeure de Fess.

Résumé
======

Cet article a présenté le développement de plugins pour Fess.

- Vue d'ensemble de l'architecture des plugins (Data Store, Ingest, thème, script)
- Processus de développement de plugins de sources de données personnalisées
- Traitement de documents avec les plugins Ingest
- Personnalisation de l'interface avec les plugins de thème
- Bonnes pratiques de développement

Les plugins permettent d'étendre Fess pour répondre aux exigences spécifiques de l'organisation.
Ceci conclut la série Architecture et Mise à l'échelle. À partir du prochain article, la série IA et Recherche de nouvelle génération abordera les fondamentaux de la recherche sémantique.

Références
==========

- `Gestion des plugins Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
