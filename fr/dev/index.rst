====================================
Serveur de recherche plein texte open source - Guide de développement |Fess|
====================================

Ce guide fournit les informations nécessaires pour participer au développement de |Fess|.
Il s'adresse à un large public, des personnes qui découvrent le développement de |Fess| aux développeurs expérimentés.

.. contents:: Table des matières
   :local:
   :depth: 2

Public cible
========

Ce guide s'adresse aux personnes suivantes :

- Développeurs souhaitant contribuer à l'ajout de fonctionnalités ou à l'amélioration de |Fess|
- Ingénieurs souhaitant comprendre le code de |Fess|
- Personnes souhaitant personnaliser et utiliser |Fess|
- Personnes intéressées par la participation à des projets open source

Connaissances préalables requises
============

Pour participer au développement de |Fess|, les connaissances suivantes sont utiles :

**Obligatoire**

- Connaissances de base en programmation Java (Java 21 ou supérieur)
- Utilisation de base de Git et GitHub
- Utilisation de base de Maven

**Recommandé**

- Connaissance du framework LastaFlute
- Connaissance de DBFlute
- Connaissance d'OpenSearch/Elasticsearch
- Expérience en développement d'applications Web

Structure du guide de développement
==============

Ce guide est composé des sections suivantes.

:doc:`getting-started`
    Explique l'aperçu du développement |Fess| et les premières étapes pour commencer le développement.
    Vous pourrez comprendre la pile technologique nécessaire au développement et la vue d'ensemble du projet.

:doc:`setup`
    Explique en détail les procédures de configuration de l'environnement de développement.
    Explique étape par étape de l'installation des outils nécessaires tels que Java, IDE, OpenSearch,
    à l'obtention et à l'exécution du code source de |Fess|.

:doc:`architecture`
    Explique l'architecture et la structure du code de |Fess|.
    En comprenant les principaux packages, modules et modèles de conception,
    vous pouvez développer efficacement.

:doc:`workflow`
    Explique le flux de travail standard du développement |Fess|.
    Vous apprendrez comment procéder aux travaux de développement tels que l'ajout de fonctionnalités, la correction de bugs, la revue de code et les tests.

:doc:`building`
    Explique comment compiler et tester |Fess|.
    Explique comment utiliser les outils de compilation, exécuter les tests unitaires,
    et créer des packages de distribution.

:doc:`contributing`
    Explique comment contribuer au projet |Fess|.
    Vous apprendrez à créer des pull requests, à suivre les conventions de codage,
    et à communiquer avec la communauté.

Démarrage rapide
==============

Si vous souhaitez commencer à développer |Fess| immédiatement, suivez ces étapes :

1. **Vérification de la configuration système**

   Les outils suivants sont nécessaires pour le développement :

   - Java 21 ou supérieur
   - Maven 3.x ou supérieur
   - Git
   - IDE (Eclipse, IntelliJ IDEA, etc.)

2. **Obtention du code source**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **Téléchargement des plugins OpenSearch**

   .. code-block:: bash

       mvn antrun:run

4. **Exécution**

   Exécutez ``org.codelibs.fess.FessBoot`` depuis votre IDE,
   ou exécutez depuis Maven :

   .. code-block:: bash

       mvn compile exec:java

Consultez :doc:`setup` pour plus de détails.

Options d'environnement de développement
==============

Le développement de |Fess| peut être effectué dans l'un des environnements suivants :

Environnement de développement local
--------------

Il s'agit de l'environnement de développement le plus courant. Installez les outils de développement sur votre machine,
et développez en utilisant un IDE.

**Avantages:**

- Compilation et exécution rapides
- Utilisation complète des fonctionnalités de l'IDE
- Travail possible hors ligne

**Inconvénients:**

- La configuration initiale prend du temps
- Des problèmes peuvent survenir en raison de différences d'environnement

Environnement de développement avec Docker
------------------------

Vous pouvez créer un environnement de développement cohérent en utilisant des conteneurs Docker.

**Avantages:**

- Cohérence de l'environnement maintenue
- Configuration facile
- Facile de revenir à un état propre

**Inconvénients:**

- Connaissance de Docker nécessaire
- Les performances peuvent être légèrement réduites dans certains cas

Consultez :doc:`setup` pour plus de détails.

Questions fréquentes
==========

Q: Quelles sont les spécifications minimales requises pour le développement ?
--------------------------------

R: Nous recommandons ce qui suit :

- CPU: 4 cœurs ou plus
- Mémoire: 8 Go ou plus
- Disque: 20 Go ou plus d'espace libre

Q: Quel IDE dois-je utiliser ?
---------------------------------

R: Vous pouvez utiliser l'IDE de votre choix, tel qu'Eclipse, IntelliJ IDEA, VS Code, etc.
Ce guide explique principalement en utilisant Eclipse comme exemple,
mais vous pouvez développer de la même manière avec d'autres IDE.

Q: La connaissance de LastaFlute ou DBFlute est-elle obligatoire ?
------------------------------------------

R: Ce n'est pas obligatoire, mais cela facilitera le développement.
L'utilisation de base est également expliquée dans ce guide,
mais consultez la documentation officielle de chaque framework pour plus de détails.

Q: Par où dois-je commencer pour ma première contribution ?
------------------------------------------------------

R: Nous vous recommandons de commencer par des tâches relativement simples telles que :

- Amélioration de la documentation
- Ajout de tests
- Correction de bugs
- Petites améliorations de fonctionnalités existantes

Consultez :doc:`contributing` pour plus de détails.

Ressources connexes
==========

Ressources officielles
----------

- `Site officiel de Fess <https://fess.codelibs.org/ja/>`__
- `Dépôt GitHub <https://github.com/codelibs/fess>`__
- `Suivi des problèmes <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

Documentation technique
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Communauté
----------

- `Forum de la communauté Fess <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

Étapes suivantes
==========

Pour commencer le développement, nous vous recommandons de commencer par lire :doc:`getting-started`.

.. toctree::
   :maxdepth: 2
   :caption: Table des matières:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
