================================================
Serveur de recherche plein texte open source - Aperçu du développement |Fess|
================================================

Cette page fournit une vue d'ensemble du développement |Fess| et des informations de base pour commencer le développement.

.. contents:: Table des matières
   :local:
   :depth: 2

Aperçu
====

|Fess| est un serveur de recherche plein texte open source développé en Java.
Il vise à faciliter la construction de recherches d'entreprise,
et fournit de puissantes fonctionnalités de recherche et un écran d'administration facile à utiliser.

Caractéristiques de |Fess|
-------------

- **Configuration facile** : Démarrage immédiat avec un environnement Java
- **Crawler puissant** : Prise en charge de diverses sources de données telles que les sites Web, les systèmes de fichiers et les bases de données
- **Support japonais** : Optimisé pour la recherche plein texte en japonais
- **Extensibilité** : Extension de fonctionnalités possible via des plugins
- **API REST** : Utilisation des fonctionnalités de recherche depuis d'autres applications

Pile technologique
==========

|Fess| est développé en utilisant les technologies suivantes.

Version cible
------------

Cette documentation cible les versions suivantes :

- **Fess** : 15.3.0
- **Java** : 21 ou supérieur
- **OpenSearch** : 3.3.0
- **Maven** : 3.x

Principales technologies et frameworks
----------------------

Java 21
~~~~~~~

|Fess| est une application qui fonctionne avec Java 21 ou supérieur.
Elle utilise les dernières fonctionnalités Java pour améliorer les performances et la maintenabilité.

- **Recommandé** : Eclipse Temurin 21 (anciennement AdoptOpenJDK)
- **Version minimale** : Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ est
le framework utilisé dans la couche application Web de |Fess|.

**Principales fonctionnalités :**

- Conteneur DI (injection de dépendances)
- Framework Web basé sur les actions
- Validation
- Gestion des messages
- Gestion de la configuration

**Ressources d'apprentissage :**

- `Documentation officielle LastaFlute <https://github.com/lastaflute/lastaflute>`__
- Vous pouvez apprendre l'utilisation pratique en lisant le code de Fess

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ est
un outil de mapping O/R pour l'accès aux bases de données.
|Fess| l'utilise pour générer automatiquement du code Java à partir du schéma OpenSearch.

**Principales fonctionnalités :**

- Constructeur SQL type-safe
- Génération automatique de code à partir du schéma
- Génération automatique de documentation de base de données

**Ressources d'apprentissage :**

- `Site officiel DBFlute <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ est
le moteur de recherche et d'analyse distribué utilisé comme moteur de recherche de |Fess|.

**Version prise en charge** : OpenSearch 3.3.0

**Plugins requis :**

- opensearch-analysis-fess : Plugin d'analyse morphologique dédié à Fess
- opensearch-analysis-extension : Fonctionnalités d'analyse linguistique supplémentaires
- opensearch-minhash : Détection de documents similaires
- opensearch-configsync : Synchronisation de la configuration

**Ressources d'apprentissage :**

- `Documentation OpenSearch <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven est utilisé comme outil de compilation de |Fess|.

**Principales utilisations :**

- Gestion des bibliothèques dépendantes
- Exécution du processus de compilation
- Exécution des tests
- Création de packages

Outils de développement
========

Environnement de développement recommandé
----------------

Eclipse
~~~~~~~

La documentation officielle explique les méthodes de développement en utilisant Eclipse.

**Version recommandée** : Eclipse 2023-09 ou supérieur

**Plugins nécessaires :**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

Le développement est également possible avec IntelliJ IDEA.

**Édition recommandée** : Community Edition ou Ultimate Edition

**Fonctionnalités nécessaires :**

- Support Maven (inclus par défaut)
- Support Java

VS Code
~~~~~~~

VS Code peut également être utilisé pour un développement léger.

**Extensions nécessaires :**

- Java Extension Pack
- Maven for Java

Gestion de version
~~~~~~~~~~~~

- **Git** : Gestion du code source
- **GitHub** : Hébergement de dépôt, gestion des problèmes, pull requests

Connaissances nécessaires
========

Connaissances de base
--------

Les connaissances suivantes sont nécessaires pour le développement de |Fess| :

**Obligatoire**

- **Programmation Java** : Classes, interfaces, génériques, expressions lambda, etc.
- **Orienté objet** : Héritage, polymorphisme, encapsulation
- **Maven** : Commandes de base et compréhension de pom.xml
- **Git** : clone, commit, push, pull, branch, merge, etc.

**Recommandé**

- **LastaFlute** : Concepts d'Action, Form, Service
- **DBFlute** : Utilisation de Behavior, ConditionBean
- **OpenSearch/Elasticsearch** : Bases des index, mappings, requêtes
- **Développement Web** : HTML, CSS, JavaScript (en particulier pour le développement frontend)
- **Commandes Linux** : Développement et débogage dans un environnement serveur

Ressources d'apprentissage
----------

Si vous abordez le développement de |Fess| pour la première fois, les ressources suivantes sont utiles :

Documentation officielle
~~~~~~~~~~~~~~

- `Manuel utilisateur Fess <https://fess.codelibs.org/ja/>`__
- `Guide administrateur Fess <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

Communauté
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__ : Questions et discussions
- `Suivi des problèmes <https://github.com/codelibs/fess/issues>`__ : Rapports de bugs et demandes de fonctionnalités
- `Forum Fess <https://discuss.codelibs.org/c/FessJA>`__ : Forum de la communauté japonaise

Code source
~~~~~~~~~~

Lire le code réel est la méthode d'apprentissage la plus efficace :

- Commencez par lire des petites fonctionnalités
- Suivez le comportement du code avec le débogueur
- Consultez le code de test existant

Flux de base du développement
==============

Le développement de |Fess| se déroule généralement comme suit :

1. **Vérification/création d'un problème**

   Vérifiez les problèmes GitHub et décidez sur quoi travailler.
   Pour une nouvelle fonctionnalité ou une correction de bug, créez un problème.

2. **Création d'une branche**

   Créez une branche de travail :

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **Codage**

   Implémentez la fonctionnalité ou corrigez le bug.

4. **Tests**

   Créez et exécutez des tests unitaires pour vérifier que les modifications fonctionnent correctement.

5. **Commit**

   Commitez les modifications :

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **Pull request**

   Poussez vers GitHub et créez une pull request :

   .. code-block:: bash

       git push origin feature/my-new-feature

Consultez :doc:`workflow` pour plus de détails.

Aperçu de la structure du projet
==================

Le code source de |Fess| a la structure suivante :

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # Couche application Web
    │   │   │       │   ├── web/       # Écran de recherche
    │   │   │       │   └── service/   # Couche service
    │   │   │       ├── crawler/       # Fonctionnalité crawler
    │   │   │       ├── es/            # Relatif à OpenSearch
    │   │   │       ├── helper/        # Classes d'aide
    │   │   │       ├── job/           # Traitement des jobs
    │   │   │       ├── util/          # Utilitaires
    │   │   │       └── FessBoot.java  # Classe de démarrage
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # Fichiers JSP
    │   └── test/
    │       └── java/                  # Code de test
    ├── pom.xml                        # Fichier de configuration Maven
    └── README.md

Principaux packages
--------------

app
~~~

Code de la couche application Web.
Contient les Actions, Forms, Services de l'écran d'administration et de recherche, etc.

crawler
~~~~~~~

Code de fonctionnalité de collecte de données.
Crawler Web, crawler de fichiers, crawler de magasin de données, etc.

es
~~

Code d'intégration avec OpenSearch.
Opérations sur les index, construction de requêtes de recherche, etc.

helper
~~~~~~

Classes d'aide utilisées dans toute l'application.

job
~~~

Code des jobs exécutés selon un calendrier.
Job de crawl, job d'optimisation d'index, etc.

Consultez :doc:`architecture` pour plus de détails.

Démarrage rapide de l'environnement de développement
=======================

Explique comment configurer l'environnement de développement avec les étapes minimales et exécuter |Fess|.

Prérequis
--------

- Java 21 ou supérieur installé
- Git installé
- Maven 3.x installé

Procédure
----

1. **Clonage du dépôt**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **Téléchargement des plugins OpenSearch**

   .. code-block:: bash

       mvn antrun:run

3. **Exécution**

   Exécutez depuis Maven :

   .. code-block:: bash

       mvn compile exec:java

   Ou exécutez la classe ``org.codelibs.fess.FessBoot`` depuis l'IDE (Eclipse, IntelliJ IDEA, etc.).

4. **Accès**

   Accédez aux URL suivantes dans le navigateur :

   - Écran de recherche : http://localhost:8080/
   - Écran d'administration : http://localhost:8080/admin/
     - Utilisateur par défaut : admin / admin

Consultez :doc:`setup` pour la procédure de configuration détaillée.

Conseils de développement
==========

Exécution en débogage
----------

Pour exécuter en débogage dans l'IDE, exécutez la classe ``FessBoot``.
En définissant des points d'arrêt, vous pouvez suivre en détail le comportement du code.

Hot deploy
------------

LastaFlute peut refléter certaines modifications sans redémarrage.
Cependant, les modifications de structure de classe, etc. nécessitent un redémarrage.

Vérification des journaux
--------

Les journaux sont enregistrés dans le répertoire ``target/fess/logs/``.
En cas de problème, vérifiez les fichiers journaux.

Manipulation d'OpenSearch
----------------

L'OpenSearch intégré est placé dans ``target/fess/es/``.
Il est également possible d'appeler directement l'API OpenSearch pour le débogage :

.. code-block:: bash

    # Vérification des index
    curl -X GET http://localhost:9201/_cat/indices?v

    # Recherche de documents
    curl -X GET http://localhost:9201/fess.search/_search?pretty

Communauté et support
==================

Questions et consultations
--------

Si vous avez des questions ou des consultations pendant le développement, utilisez les ressources suivantes :

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__ : Questions générales et discussions
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ : Rapports de bugs et demandes de fonctionnalités
- `Forum Fess <https://discuss.codelibs.org/c/FessJA>`__ : Forum en japonais

Méthodes de contribution
--------

Consultez :doc:`contributing` pour les méthodes de contribution à |Fess|.

Étapes suivantes
==========

Si vous êtes prêt à configurer l'environnement de développement, passez à :doc:`setup`.

Consultez également la documentation suivante pour des informations détaillées :

- :doc:`architecture` - Architecture et structure du code
- :doc:`workflow` - Flux de travail de développement
- :doc:`building` - Compilation et tests
- :doc:`contributing` - Guide de contribution

Ressources de référence
========

Ressources officielles
----------

- `Site officiel Fess <https://fess.codelibs.org/ja/>`__
- `Dépôt GitHub <https://github.com/codelibs/fess>`__
- `Page de téléchargements <https://fess.codelibs.org/ja/downloads.html>`__

Documentation technique
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Communauté
----------

- `Forum Fess <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
