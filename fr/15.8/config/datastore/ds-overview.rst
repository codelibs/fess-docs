==================================
Aperçu des connecteurs DataStore
==================================

Aperçu
======

Les connecteurs DataStore de |Fess| fournissent une fonctionnalité permettant de récupérer
et d'indexer du contenu depuis des sources de données autres que les sites web ou les systèmes de fichiers.

En utilisant les connecteurs DataStore, vous pouvez rendre recherchables les données provenant des sources suivantes :

- Stockage cloud (Box, Dropbox, Google Drive, OneDrive)
- Outils de collaboration (Confluence, Jira, Slack)
- Bases de données (MySQL, PostgreSQL, Oracle, etc.)
- Autres systèmes (Git, Salesforce, Elasticsearch, etc.)

Connecteurs disponibles
=======================

|Fess| fournit des connecteurs pour diverses sources de données.
La plupart des connecteurs sont fournis sous forme de plugins et peuvent être installés selon les besoins.

Stockage cloud
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connecteur
     - Plugin
     - Description
   * - :doc:`ds-box`
     - fess-ds-box
     - Exploration des fichiers et dossiers Box.com
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - Exploration des fichiers et dossiers Dropbox
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - Exploration de Google Drive
   * - :doc:`ds-microsoft365`
     - fess-ds-microsoft365
     - Exploration de OneDrive, SharePoint, etc.

Outils de collaboration
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connecteur
     - Plugin
     - Description
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - Exploration de Confluence et Jira
   * - :doc:`ds-slack`
     - fess-ds-slack
     - Exploration des messages et fichiers Slack

Outils de développement et opérations
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connecteur
     - Plugin
     - Description
   * - :doc:`ds-git`
     - fess-ds-git
     - Exploration du code source des dépôts Git
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Récupération de données depuis Elasticsearch/OpenSearch
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Exploration des objets Salesforce

Bases de données et fichiers
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connecteur
     - Plugin
     - Description
   * - :doc:`ds-database`
     - fess-ds-db
     - Récupération de données depuis les bases de données compatibles JDBC
   * - :doc:`ds-csv`
     - fess-ds-csv
     - Récupération de données depuis les fichiers CSV
   * - :doc:`ds-json`
     - fess-ds-json
     - Récupération de données depuis les fichiers JSON

Installation des connecteurs
============================

Installation des plugins
------------------------

Les plugins de connecteurs DataStore peuvent être installés depuis l'interface d'administration.

Depuis l'interface d'administration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Connectez-vous à l'interface d'administration
2. Naviguez vers "Système" -> "Plugin"
3. Cliquez sur le bouton "Installer"
4. Sélectionnez le plugin dans l'onglet "Distant" (ou téléchargez un fichier JAR depuis l'onglet "Local")
5. Cliquez sur "Installer"
6. Redémarrez |Fess|

Configuration de base des DataStores
====================================

La configuration des connecteurs DataStore s'effectue dans l'interface d'administration sous "Crawler" -> "DataStore".

Éléments de configuration communs
---------------------------------

Éléments de configuration communs à tous les connecteurs DataStore :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Description
   * - Nom
     - Nom d'identification de la configuration
   * - Description
     - Description de la configuration
   * - Nom du handler
     - Nom du handler du connecteur à utiliser (ex: ``CsvDataStore``)
   * - Paramètres
     - Paramètres de configuration spécifiques au connecteur (format key=value)
   * - Script
     - Script de mapping des champs d'index
   * - Boost
     - Priorité dans les résultats de recherche
   * - Autorisations
     - Autorisations d'accès aux documents récupérés par ce connecteur
   * - Hôtes virtuels
     - Hôte virtuel auquel cette configuration s'applique
   * - Ordre d'affichage
     - Ordre d'affichage dans la liste des configurations
   * - Actif
     - Activer ou non cette configuration

Configuration des paramètres
----------------------------

Les paramètres sont spécifiés au format ``key=value`` séparés par des retours à la ligne :

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

Configuration du script
-----------------------

Le script permet de mapper les données récupérées vers les champs d'index de |Fess|.
Chaque ligne du script associe un champ d'index |Fess| (membre gauche) au champ fourni par le connecteur (membre droit).

Voici un exemple pour le connecteur CSV avec les colonnes d'en-tête ``link``, ``subject`` et ``body`` :

::

    url=link
    title=subject
    content=body

.. note::

   Les noms de champs utilisables dans le script varient selon le connecteur.
   Box/Dropbox/Google Drive/OneDrive référencent l'objet récupéré avec le préfixe ``file.*`` ; Slack utilise ``message.*`` ; Jira utilise ``issue.*``.
   En revanche, les connecteurs CSV, JSON et Base de données n'utilisent aucun préfixe ; les champs sont référencés directement :

   - CSV : noms des colonnes d'en-tête (si ``has_header_line=true``), ou ``cell1``, ``cell2``, ... (index base 1) ; ainsi que ``csvfile`` et ``csvfilename``.
   - JSON : noms des champs de l'objet JSON.
   - Base de données : noms des colonnes (alias) du résultat SELECT.

   Consultez la documentation individuelle de chaque connecteur pour plus de détails.

Configuration de l'authentification
===================================

La plupart des connecteurs DataStore nécessitent une authentification (OAuth 2.0, clé API, compte de service, etc.).

Les paramètres d'authentification varient selon le connecteur.
Consultez la documentation de chaque connecteur pour les détails de configuration de l'authentification.

Paramètres communs
==================

Paramètres communs à tous les connecteurs DataStore :

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Paramètre
     - Défaut
     - Description
   * - ``readInterval``
     - ``0``
     - Délai d'attente entre le traitement de chaque enregistrement (en millisecondes). Utilisez ce paramètre pour réduire la charge du serveur lors du traitement de grandes quantités de données.
   * - ``script_type``
     - ``groovy``
     - Type de moteur de script utilisé pour le mappage des champs d'index. Par défaut, seul ``groovy`` est disponible.

Dépannage
=========

Le connecteur n'apparaît pas
----------------------------

1. Vérifiez que le plugin est correctement installé
2. Redémarrez |Fess|
3. Vérifiez les erreurs dans les logs

Erreur d'authentification
-------------------------

1. Vérifiez que les informations d'authentification sont correctes
2. Vérifiez la date d'expiration du token
3. Vérifiez que les autorisations nécessaires sont accordées
4. Vérifiez que l'accès API est autorisé côté service

Impossible de récupérer les données
-----------------------------------

1. Vérifiez le format des paramètres
2. Vérifiez les droits d'accès aux dossiers/fichiers cibles
3. Vérifiez les paramètres de filtre
4. Vérifiez les messages d'erreur détaillés dans les logs

Configuration de débogage
-------------------------

Pour investiguer les problèmes, ajustez le niveau de log. Le crawling des datastores s'exécute dans le processus crawler ; c'est donc le fichier de configuration des logs du crawler qu'il faut modifier :

``app/WEB-INF/env/crawler/resources/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Informations de référence
=========================

- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
- :doc:`../../api/admin/api-admin-dataconfig` - API de configuration DataStore
