============================
Choix de la méthode d'installation
============================

Cette page décrit une vue d'ensemble des méthodes d'installation de |Fess|.
Veuillez sélectionner la méthode d'installation appropriée en fonction de votre environnement.

.. warning::

   **Note importante pour les environnements de production**

   Pour les environnements de production ou les tests de charge, nous ne recommandons pas l'utilisation d'OpenSearch intégré.
   Veuillez obligatoirement configurer un serveur OpenSearch externe.

Vérification des prérequis
===========================

Avant de commencer l'installation, veuillez vérifier la configuration requise.

Pour plus de détails, consultez :doc:`prerequisites`.

Comparaison des méthodes d'installation
========================================

|Fess| peut être installé selon les méthodes suivantes. Veuillez sélectionner en fonction de votre environnement et de votre utilisation.

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - Méthode
     - Système d'exploitation
     - Usage recommandé
     - Documentation détaillée
   * - Docker
     - Linux, Windows, macOS
     - Environnement de développement/évaluation, configuration rapide
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - Environnement nécessitant une personnalisation
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - Environnement de production (basé sur RPM)
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - Environnement de production (basé sur DEB)
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Développement/production sur environnement Windows
     - :doc:`install-windows`

Caractéristiques de chaque méthode d'installation
==================================================

Version Docker
--------------

**Avantages :**

- Configuration la plus rapide possible
- Gestion des dépendances non nécessaire
- Idéal pour la création d'environnements de développement
- Démarrage et arrêt faciles des conteneurs

**Inconvénients :**

- Connaissance de Docker requise

**Environnement recommandé :** Environnements de développement, d'évaluation, POC, production

Détails : :doc:`install-docker`

Packages Linux (TAR.GZ/RPM/DEB)
-------------------------------

**Avantages :**

- Hautes performances en environnement natif
- Gestion possible en tant que service système (RPM/DEB)
- Personnalisation fine possible

**Inconvénients :**

- Installation manuelle de Java et OpenSearch requise
- Configuration nécessitant un effort

**Environnement recommandé :** Environnement de production, environnement nécessitant une personnalisation

Détails : :doc:`install-linux`

Version Windows (ZIP)
---------------------

**Avantages :**

- Fonctionne en environnement Windows natif
- Aucun installateur nécessaire

**Inconvénients :**

- Installation manuelle de Java et OpenSearch requise
- Configuration nécessitant un effort

**Environnement recommandé :** Développement/évaluation sur environnement Windows, exploitation en production sur Windows Server

Détails : :doc:`install-windows`

Flux d'installation de base
===========================

Pour toutes les méthodes d'installation, le flux de base est le même.

1. **Vérification de la configuration requise**

   Consultez :doc:`prerequisites` pour confirmer que la configuration requise est satisfaite.

2. **Téléchargement du logiciel**

   Téléchargez |Fess| depuis le `site de téléchargement <https://fess.codelibs.org/ja/downloads.html>`__.

   Pour la version Docker, obtenez le fichier Docker Compose.

3. **Configuration d'OpenSearch**

   Pour les versions autres que Docker, vous devez configurer OpenSearch séparément.

   - Installation d'OpenSearch 3.3.2
   - Installation des plugins requis
   - Modification des fichiers de configuration

4. **Configuration de Fess**

   - Installation de Fess
   - Modification des fichiers de configuration (informations de connexion à OpenSearch, etc.)

5. **Démarrage et vérification**

   - Démarrage du service
   - Vérification du fonctionnement en accédant via un navigateur

   Pour plus de détails, consultez :doc:`run`.

Composants requis
=================

Pour exécuter |Fess|, les composants suivants sont nécessaires.

Application Fess
----------------

Il s'agit du système de recherche plein texte principal. Il fournit des fonctionnalités telles que l'interface Web, le crawler et l'indexeur.

OpenSearch
----------

OpenSearch est utilisé comme moteur de recherche.

- **Version compatible** : OpenSearch 3.3.2
- **Plugins requis** :

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   Les versions d'OpenSearch et des plugins doivent correspondre.
   Une incompatibilité de version peut causer des erreurs de démarrage ou des comportements inattendus.

Java (sauf version Docker)
--------------------------

Pour les versions TAR.GZ/ZIP/RPM/DEB, Java 21 ou ultérieur est requis.

- Recommandé : `Eclipse Temurin <https://adoptium.net/temurin>`__
- OpenJDK 21 ou ultérieur peut également être utilisé

.. note::

   Pour la version Docker, Java est inclus dans l'image Docker, donc aucune installation séparée n'est nécessaire.

Étapes suivantes
================

Après avoir vérifié la configuration requise, veuillez sélectionner la méthode d'installation appropriée.

1. :doc:`prerequisites` - Vérification de la configuration requise
2. Sélection de la méthode d'installation :

   - :doc:`install-docker` - Installation avec Docker
   - :doc:`install-linux` - Installation sur Linux
   - :doc:`install-windows` - Installation sur Windows

3. :doc:`run` - Démarrage de |Fess| et configuration initiale
4. :doc:`security` - Configuration de la sécurité (pour les environnements de production)

Questions fréquemment posées
=============================

Q : OpenSearch est-il obligatoire ?
------------------------------------

R : Oui, il est obligatoire. |Fess| utilise OpenSearch comme moteur de recherche.
Pour la version Docker, il est configuré automatiquement, mais pour les autres méthodes, vous devez l'installer manuellement.

Q : Peut-on effectuer une mise à niveau depuis une version antérieure ?
-----------------------------------------------------------------------

R : Oui, c'est possible. Pour plus de détails, consultez :doc:`upgrade`.

Q : Peut-on configurer avec plusieurs serveurs ?
-------------------------------------------------

R : Oui, c'est possible. Fess et OpenSearch peuvent être exécutés sur des serveurs séparés.
De plus, en configurant OpenSearch en cluster, vous pouvez améliorer la haute disponibilité et les performances.

Téléchargements
===============

|Fess| et les composants associés peuvent être téléchargés depuis :

- **Fess** : `Site de téléchargement <https://fess.codelibs.org/ja/downloads.html>`__
- **OpenSearch** : `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)** : `Adoptium <https://adoptium.net/>`__
- **Docker** : `Get Docker <https://docs.docker.com/get-docker/>`__

Informations de version
========================

Cette documentation concerne les versions suivantes :

- **Fess** : 15.5.0
- **OpenSearch** : 3.3.2
- **Java** : 21 ou ultérieur
- **Docker** : 20.10 ou ultérieur
- **Docker Compose** : 2.0 ou ultérieur

Pour la documentation des versions précédentes, veuillez consulter la documentation de chaque version.
