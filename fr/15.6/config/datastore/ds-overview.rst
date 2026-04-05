==================================
Apercu des connecteurs DataStore
==================================

Apercu
======

Les connecteurs DataStore de |Fess| fournissent une fonctionnalite permettant de recuperer
et d'indexer du contenu depuis des sources de donnees autres que les sites web ou les systemes de fichiers.

En utilisant les connecteurs DataStore, vous pouvez rendre recherchables les donnees provenant des sources suivantes :

- Stockage cloud (Box, Dropbox, Google Drive, OneDrive)
- Outils de collaboration (Confluence, Jira, Slack)
- Bases de donnees (MySQL, PostgreSQL, Oracle, etc.)
- Autres systemes (Git, Salesforce, Elasticsearch, etc.)

Connecteurs disponibles
=======================

|Fess| fournit des connecteurs pour diverses sources de donnees.
La plupart des connecteurs sont fournis sous forme de plugins et peuvent etre installes selon les besoins.

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
     - Exploration de Google Drive, Gmail, etc.
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

Outils de developpement et operations
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connecteur
     - Plugin
     - Description
   * - :doc:`ds-git`
     - fess-ds-git
     - Exploration du code source des depots Git
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Recuperation de donnees depuis Elasticsearch/OpenSearch
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Exploration des objets Salesforce

Bases de donnees et fichiers
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connecteur
     - Plugin
     - Description
   * - :doc:`ds-database`
     - fess-ds-db
     - Recuperation de donnees depuis les bases de donnees compatibles JDBC
   * - :doc:`ds-csv`
     - fess-ds-csv
     - Recuperation de donnees depuis les fichiers CSV
   * - :doc:`ds-json`
     - fess-ds-json
     - Recuperation de donnees depuis les fichiers JSON

Installation des connecteurs
============================

Installation des plugins
------------------------

Les plugins de connecteurs DataStore peuvent etre installes depuis l'interface d'administration.

Depuis l'interface d'administration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Connectez-vous a l'interface d'administration
2. Naviguez vers "Systeme" -> "Plugins"
3. Dans l'onglet "Disponibles", recherchez le plugin souhaite
4. Cliquez sur "Installer"
5. Redemarrez |Fess|

Configuration de base des DataStores
====================================

La configuration des connecteurs DataStore s'effectue dans l'interface d'administration sous "Crawler" -> "DataStore".

Elements de configuration communs
---------------------------------

Elements de configuration communs a tous les connecteurs DataStore :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Description
   * - Nom
     - Nom d'identification de la configuration
   * - Description
     - Description de la configuration
   * - Nom du handler
     - Nom du handler du connecteur a utiliser (ex: ``BoxDataStore``)
   * - Parametres
     - Parametres de configuration specifiques au connecteur (format key=value)
   * - Script
     - Script de mapping des champs d'index
   * - Boost
     - Priorite dans les resultats de recherche
   * - Autorisations
     - Autorisations d'acces aux documents recuperes par ce connecteur
   * - Hotes virtuels
     - Hote virtuel auquel cette configuration s'applique
   * - Ordre d'affichage
     - Ordre d'affichage dans la liste des configurations
   * - Actif
     - Activer ou non cette configuration

Configuration des parametres
----------------------------

Les parametres sont specifies au format ``key=value`` separes par des retours a la ligne :

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

Configuration du script
-----------------------

Le script permet de mapper les donnees recuperees vers les champs d'index de |Fess|.

Voici un exemple utilisant le prefixe ``data.*`` pour les connecteurs CSV/JSON :

::

    url=data.url
    title=data.name
    content=data.content
    mimetype=data.mimetype
    filetype=data.filetype
    filename=data.filename
    created=data.created
    lastModified=data.lastModified
    contentLength=data.contentLength

.. note::

   Le prefixe des champs dans le script varie selon le connecteur.
   Par exemple, Box/Dropbox/Google Drive/OneDrive utilisent ``file.*``, Slack utilise ``message.*``,
   Jira utilise ``issue.*``.
   Consultez la documentation de chaque connecteur pour plus de details.

Configuration de l'authentification
===================================

La plupart des connecteurs DataStore necessitent une authentification (OAuth 2.0, cle API, compte de service, etc.).

Les parametres d'authentification varient selon le connecteur.
Consultez la documentation de chaque connecteur pour les details de configuration de l'authentification.

Parametres communs
==================

Parametres communs a tous les connecteurs DataStore :

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Defaut
     - Description
   * - ``readInterval``
     - ``0``
     - Delai d'attente entre le traitement de chaque enregistrement (en millisecondes). Utilisez ce parametre pour reduire la charge du serveur lors du traitement de grandes quantites de donnees.

Depannage
=========

Le connecteur n'apparait pas
----------------------------

1. Verifiez que le plugin est correctement installe
2. Redemarrez |Fess|
3. Verifiez les erreurs dans les logs

Erreur d'authentification
-------------------------

1. Verifiez que les informations d'authentification sont correctes
2. Verifiez la date d'expiration du token
3. Verifiez que les autorisations necessaires sont accordees
4. Verifiez que l'acces API est autorise cote service

Impossible de recuperer les donnees
-----------------------------------

1. Verifiez le format des parametres
2. Verifiez les droits d'acces aux dossiers/fichiers cibles
3. Verifiez les parametres de filtre
4. Verifiez les messages d'erreur detailles dans les logs

Configuration de debogage
-------------------------

Pour investiguer les problemes, ajustez le niveau de log :

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Informations de reference
=========================

- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
- :doc:`../../api/admin/api-admin-dataconfig` - API de configuration DataStore
