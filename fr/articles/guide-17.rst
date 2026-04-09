============================================================
Partie 17 : Etendre la recherche avec des plugins -- Implementation de sources de donnees personnalisees et de pipelines Ingest
============================================================

Introduction
============

Fess prend en charge de nombreuses sources de donnees par defaut, mais il peut etre necessaire de l'etendre via des plugins pour s'adapter aux systemes et formats de donnees specifiques a l'entreprise.

Cet article explique l'architecture des plugins de Fess et presente comment implementer des plugins de sources de donnees personnalisees et des plugins Ingest.

Public cible
============

- Personnes souhaitant connecter Fess a des sources de donnees personnalisees
- Developpeurs Java interesses par le developpement de plugins
- Personnes souhaitant comprendre l'architecture interne de Fess

Architecture des plugins
=========================

Fess propose les types de plugins suivants.

.. list-table:: Types de plugins
   :header-rows: 1
   :widths: 25 35 40

   * - Type
     - Role
     - Exemples
   * - Data Store (fess-ds-*)
     - Recuperation de donnees depuis des sources externes
     - Slack, Salesforce, DB
   * - Ingest (fess-ingest-*)
     - Traitement et transformation des donnees collectees
     - Example
   * - Theme (fess-theme-*)
     - Design de l'interface de recherche
     - Simple, Code Search
   * - Script (fess-script-*)
     - Prise en charge des langages de script
     - OGNL
   * - Web App (fess-webapp-*)
     - Extensions d'applications web
     - MCP Server

Deploiement des plugins
-----------------------

Les plugins sont fournis sous forme de fichiers JAR et places dans le repertoire de plugins de Fess.
Ils peuvent etre installes et geres depuis [Systeme] > [Plugins] dans la console d'administration.

Developpement d'un plugin de source de donnees personnalisee
=============================================================

Cette section explique le processus de developpement d'un plugin de source de donnees, en supposant l'existence d'un systeme de gestion documentaire interne proprietaire.

Structure du projet
-------------------

Creez un projet Maven en vous referant a un plugin Data Store existant (par exemple, fess-ds-git).

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

Specifiez fess-parent comme POM parent et configurez les dependances requises.

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

Implementation de la classe Data Store
----------------------------------------

Le coeur d'un plugin Data Store est la classe qui recupere les donnees et enregistre les documents dans Fess.

Les points cles de l'implementation sont les suivants :

1. Connexion et authentification avec le systeme externe
2. Recuperation des donnees (appels API, lecture de fichiers, etc.)
3. Conversion des donnees recuperees au format de document Fess
4. Enregistrement des documents

**Mappage des champs**

Mappez les donnees recuperees aux champs de Fess.
Les principaux champs sont les suivants :

- ``title`` : Titre du document
- ``url`` : URL du document (destination du lien dans les resultats de recherche)
- ``content`` : Corps du document (cible de recherche)
- ``mimetype`` : Type MIME
- ``last_modified`` : Date et heure de derniere modification

Compilation et deploiement
--------------------------

::

    $ mvn clean package

Placez le fichier JAR genere dans le repertoire de plugins de Fess et redemarrez Fess.

Developpement d'un plugin Ingest
==================================

Un plugin Ingest est un mecanisme permettant de traiter et de transformer les documents obtenus par collecte avant leur enregistrement dans l'index.

Cas d'utilisation
-----------------

- Ajout de champs supplementaires aux documents collectes
- Nettoyage du texte du corps (suppression de caracteres inutiles)
- Enrichissement via des API externes (traduction, classification, etc.)
- Sortie de logs (pour le debogage)

Points d'implementation
-----------------------

Dans un plugin Ingest, vous accedez aux donnees du document juste avant son enregistrement dans l'index et effectuez le traitement de transformation.

Par exemple, vous pouvez implementer un traitement qui ajoute des metadonnees de nom d'organisation a tous les documents, ou un traitement qui supprime des motifs specifiques du texte du corps.

Developpement d'un plugin de theme
====================================

Si vous souhaitez personnaliser entierement le design de l'interface de recherche, developpez un plugin de theme.

Structure du theme
------------------

Un plugin de theme est compose de fichiers JSP, CSS, JavaScript et de fichiers image.

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

Personnalisez le design en modifiant les fichiers JSP et CSS en vous referant aux themes existants.

Bonnes pratiques de developpement
==================================

Reference aux plugins existants
-------------------------------

Lors du developpement d'un nouveau plugin, il est fortement recommande de consulter le code source des plugins existants.
Le code source de tous les plugins est disponible sur le depot GitHub de CodeLibs.

Par exemple, ``fess-ds-git`` et ``fess-ds-slack`` constituent de bonnes references pour le developpement de plugins Data Store.

Tests
-----

Testez les plugins selon les perspectives suivantes :

- Tests de connexion avec les systemes externes
- Precision de la transformation des donnees
- Gestion des erreurs (echecs de connexion, donnees invalides, etc.)
- Performance (temps de traitement pour de grands volumes de donnees)

Compatibilite des versions
--------------------------

Verifiez la compatibilite des plugins lors de la mise a jour de Fess.
Des modifications de l'API peuvent survenir lors des mises a jour de version majeure de Fess.

Resume
======

Cet article a presente le developpement de plugins pour Fess.

- Vue d'ensemble de l'architecture des plugins (Data Store, Ingest, theme, script)
- Processus de developpement de plugins de sources de donnees personnalisees
- Traitement de documents avec les plugins Ingest
- Personnalisation de l'interface avec les plugins de theme
- Bonnes pratiques de developpement

Les plugins permettent d'etendre Fess pour repondre aux exigences specifiques de l'organisation.
Ceci conclut la serie Architecture et Mise a l'echelle. A partir du prochain article, la serie IA et Recherche de nouvelle generation abordera les fondamentaux de la recherche semantique.

References
==========

- `Gestion des plugins Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
