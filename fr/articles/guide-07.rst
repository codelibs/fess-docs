============================================================
Partie 7 : Stratégies de recherche à l'ère du stockage cloud
============================================================

Introduction
============

Dans de nombreuses entreprises, l'utilisation du stockage cloud est devenue une évidence.
Cependant, il n'est pas rare que différents services cloud soient utilisés selon les départements ou les usages.
Le temps passé à se demander "Ce fichier est-il sur Google Drive, SharePoint ou Box ?" nuit à la productivité.

Dans cet article, nous allons intégrer plusieurs services de stockage cloud avec Fess et mettre en place un environnement permettant de rechercher tous les fichiers cloud de manière transversale depuis une seule barre de recherche.

Public cible
============

- Administrateurs d'organisations utilisant plusieurs services de stockage cloud
- Personnes confrontées à des difficultés de recherche dans le stockage cloud
- Personnes ayant une compréhension des concepts de base de l'authentification OAuth

Scénario
========

Une entreprise utilise les services de stockage cloud suivants.

.. list-table:: Utilisation des services de stockage cloud
   :header-rows: 1
   :widths: 25 35 40

   * - Service
     - Département utilisateur
     - Usage principal
   * - Google Drive
     - Service commercial et marketing
     - Propositions, rapports, feuilles de calcul
   * - SharePoint Online
     - Ensemble de l'entreprise
     - Portail interne, documents partagés
   * - Box
     - Service juridique et comptabilité
     - Contrats, factures, documents confidentiels

Préparation de l'intégration du stockage cloud
================================================

Installation des plugins de data store
--------------------------------------

Les plugins suivants sont utilisés pour le crawl des services de stockage cloud.

- ``fess-ds-gsuite``: Crawl de Google Drive / Google Workspace
- ``fess-ds-microsoft365``: Crawl de SharePoint Online / OneDrive
- ``fess-ds-box``: Crawl de Box

L'installation s'effectue depuis l'écran d'administration via [Système] > [Plugins].

Configuration de l'authentification OAuth
------------------------------------------

Pour accéder aux API des services de stockage cloud, la configuration de l'authentification OAuth est nécessaire.
Dans la console d'administration de chaque service, enregistrez une application et obtenez l'identifiant client et le secret.

**Procédure commune**

1. Enregistrer une application dans la console d'administration de chaque service
2. Configurer les scopes API (permissions) nécessaires (l'accès en lecture seule est suffisant)
3. Obtenir l'identifiant client et le secret client
4. Configurer ces informations dans les paramètres de data store de Fess

Configuration de chaque service
================================

Configuration de Google Drive
------------------------------

Nous allons ajouter les fichiers Google Drive aux cibles de recherche.

**Préparation dans Google Cloud Console**

1. Créer un projet dans Google Cloud Console
2. Activer l'API Google Drive
3. Créer un compte de service et télécharger le fichier de clé JSON
4. Configurer le partage du compte de service sur les drives ou dossiers cibles

**Configuration dans Fess**

1. [Crawler] > [Data Store] > [Nouveau]
2. Nom du handler : sélectionner GoogleDriveDataStore
3. Configuration des paramètres et des scripts
4. Label : définir ``google-drive``

**Exemple de configuration des paramètres**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**Exemple de configuration des scripts**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

Définissez les valeurs ``private_key``, ``private_key_id`` et ``client_email`` à partir du fichier de clé JSON du compte de service. Les formats propriétaires Google tels que Google Docs, Sheets et Slides peuvent également être extraits et recherchés sous forme de texte.

Configuration de SharePoint Online
------------------------------------

Nous allons ajouter les bibliothèques de documents SharePoint Online aux cibles de recherche.

**Préparation dans Entra ID (Azure AD)**

1. Enregistrer une application dans Entra ID
2. Configurer les permissions de l'API Microsoft Graph (Sites.Read.All, etc.)
3. Créer un secret client ou un certificat

**Configuration dans Fess**

1. [Crawler] > [Data Store] > [Nouveau]
2. Nom du handler : sélectionner SharePointDocLibDataStore (pour les bibliothèques de documents. Selon l'usage, SharePointListDataStore, SharePointPageDataStore ou OneDriveDataStore sont également disponibles)
3. Configuration des paramètres et des scripts
4. Label : définir ``sharepoint``

**Exemple de configuration des paramètres**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**Exemple de configuration des scripts**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

Définissez ``tenant``, ``client_id`` et ``client_secret`` avec les valeurs obtenues lors de l'enregistrement de l'application dans Entra ID. En spécifiant ``site_id``, seul un site particulier sera crawlé. Si cette valeur est omise, tous les sites accessibles seront inclus.

Configuration de Box
---------------------

Nous allons ajouter les fichiers Box aux cibles de recherche.

**Préparation dans Box Developer Console**

1. Créer une application personnalisée dans Box Developer Console
2. Sélectionner "Authentification serveur (avec identifiants client)" comme méthode d'authentification
3. Demander l'approbation de l'application à un administrateur

**Configuration dans Fess**

1. [Crawler] > [Data Store] > [Nouveau]
2. Nom du handler : sélectionner BoxDataStore
3. Configuration des paramètres et des scripts
4. Label : définir ``box``

**Exemple de configuration des paramètres**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**Exemple de configuration des scripts**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

Configurez les informations d'authentification de l'application personnalisée créée dans Box Developer Console. Le paramètre ``supported_mimetypes`` permet de filtrer les types de fichiers à crawler à l'aide d'expressions régulières.

Optimisation de la recherche transversale
==========================================

Utilisation du crawl différentiel
----------------------------------

Pour le crawl des services de stockage cloud, il est plus efficace d'utiliser le crawl différentiel, qui ne récupère que les fichiers mis à jour depuis le dernier crawl, plutôt que de récupérer l'ensemble des fichiers à chaque fois.

Vérifiez si l'option de crawl différentiel est disponible dans la configuration de chaque plugin.
Le crawl différentiel permet de réduire le nombre d'appels API et de raccourcir le temps de crawl.

URL des résultats de recherche
-------------------------------

Pour les documents crawlés depuis le stockage cloud, un clic sur le lien dans les résultats de recherche ouvre le fichier dans l'interface Web du service correspondant.
Ce comportement est naturel pour les utilisateurs et ne nécessite généralement aucune configuration particulière.

Points d'attention opérationnels
=================================

Renouvellement des tokens OAuth
--------------------------------

Lors de l'intégration avec les services de stockage cloud, il est important de surveiller la validité des tokens OAuth.

- **Google Drive** : dans le cas d'un compte de service, les tokens sont renouvelés automatiquement
- **SharePoint Online** : les secrets client ont une date d'expiration et doivent être renouvelés périodiquement
- **Box** : une re-approbation de l'application peut être nécessaire

Enregistrez les dates d'expiration des tokens dans un calendrier afin d'éviter l'arrêt du crawl en raison d'une expiration.

Surveillance de l'utilisation des API
--------------------------------------

Les API des services de stockage cloud sont soumises à des limites d'utilisation.
En particulier lors du crawl d'un grand nombre de fichiers, surveillez l'utilisation des API et ajustez les paramètres de crawl pour ne pas dépasser les limites.

Permissions et sécurité
------------------------

Le compte de service Fess pour le stockage cloud doit être configuré avec des permissions en lecture seule.
Les permissions en écriture ne sont pas nécessaires, conformément au principe de minimisation des risques de sécurité.

De plus, en combinant cette approche avec la recherche basée sur les rôles abordée dans la Partie 5, il est possible de contrôler les résultats de recherche en fonction du système de permissions du stockage cloud.

Conclusion
==========

Dans cet article, nous avons intégré trois services de stockage cloud -- Google Drive, SharePoint Online et Box -- avec Fess pour mettre en place un environnement de recherche transversale.

- Configuration des plugins de data store et de l'authentification OAuth pour chaque service de stockage cloud
- Distinction et filtrage des sources d'information par labels
- Optimisation de l'expérience de recherche grâce au crawl différentiel
- Gestion des tokens OAuth et surveillance de l'utilisation des API

Cela permet de trouver instantanément les fichiers nécessaires sans avoir à se demander sur quel service cloud ils se trouvent.

Dans le prochain article, nous aborderons le cycle de tuning pour l'amélioration continue de la qualité de recherche.

Références
==========

- `Configuration des data stores Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Liste des plugins Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
