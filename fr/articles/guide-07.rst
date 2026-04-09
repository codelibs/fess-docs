============================================================
Partie 7 : Strategies de recherche a l'ere du stockage cloud -- Recherche transversale sur Google Drive, SharePoint et Box
============================================================

Introduction
============

Dans de nombreuses entreprises, l'utilisation du stockage cloud est devenue une evidence.
Cependant, il n'est pas rare que differents services cloud soient utilises selon les departements ou les usages.
Le temps passe a se demander "Ce fichier est-il sur Google Drive, SharePoint ou Box ?" nuit a la productivite.

Dans cet article, nous allons integrer plusieurs services de stockage cloud avec Fess et mettre en place un environnement permettant de rechercher tous les fichiers cloud de maniere transversale depuis une seule barre de recherche.

Public cible
============

- Administrateurs d'organisations utilisant plusieurs services de stockage cloud
- Personnes confrontees a des difficultes de recherche dans le stockage cloud
- Personnes ayant une comprehension des concepts de base de l'authentification OAuth

Scenario
========

Une entreprise utilise les services de stockage cloud suivants.

.. list-table:: Utilisation des services de stockage cloud
   :header-rows: 1
   :widths: 25 35 40

   * - Service
     - Departement utilisateur
     - Usage principal
   * - Google Drive
     - Service commercial et marketing
     - Propositions, rapports, feuilles de calcul
   * - SharePoint Online
     - Ensemble de l'entreprise
     - Portail interne, documents partages
   * - Box
     - Service juridique et comptabilite
     - Contrats, factures, documents confidentiels

Preparation de l'integration du stockage cloud
================================================

Installation des plugins de data store
--------------------------------------

Les plugins suivants sont utilises pour le crawl des services de stockage cloud.

- ``fess-ds-gsuite``: Crawl de Google Drive / Google Workspace
- ``fess-ds-microsoft365``: Crawl de SharePoint Online / OneDrive
- ``fess-ds-box``: Crawl de Box

L'installation s'effectue depuis l'ecran d'administration via [Systeme] > [Plugins].

Configuration de l'authentification OAuth
------------------------------------------

Pour acceder aux API des services de stockage cloud, la configuration de l'authentification OAuth est necessaire.
Dans la console d'administration de chaque service, enregistrez une application et obtenez l'identifiant client et le secret.

**Procedure commune**

1. Enregistrer une application dans la console d'administration de chaque service
2. Configurer les scopes API (permissions) necessaires (l'acces en lecture seule est suffisant)
3. Obtenir l'identifiant client et le secret client
4. Configurer ces informations dans les parametres de data store de Fess

Configuration de chaque service
================================

Configuration de Google Drive
------------------------------

Nous allons ajouter les fichiers Google Drive aux cibles de recherche.

**Preparation dans Google Cloud Console**

1. Creer un projet dans Google Cloud Console
2. Activer l'API Google Drive
3. Creer un compte de service et telecharger le fichier de cle JSON
4. Configurer le partage du compte de service sur les drives ou dossiers cibles

**Configuration dans Fess**

1. [Crawler] > [Data Store] > [Nouveau]
2. Nom du handler : selectionner GoogleDriveDataStore
3. Configuration des parametres et des scripts
4. Label : definir ``google-drive``

**Exemple de configuration des parametres**

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

Definissez les valeurs ``private_key``, ``private_key_id`` et ``client_email`` a partir du fichier de cle JSON du compte de service. Les formats proprietaires Google tels que Google Docs, Sheets et Slides peuvent egalement etre extraits et recherches sous forme de texte.

Configuration de SharePoint Online
------------------------------------

Nous allons ajouter les bibliotheques de documents SharePoint Online aux cibles de recherche.

**Preparation dans Entra ID (Azure AD)**

1. Enregistrer une application dans Entra ID
2. Configurer les permissions de l'API Microsoft Graph (Sites.Read.All, etc.)
3. Creer un secret client ou un certificat

**Configuration dans Fess**

1. [Crawler] > [Data Store] > [Nouveau]
2. Nom du handler : selectionner SharePointDocLibDataStore (pour les bibliotheques de documents. Selon l'usage, SharePointListDataStore, SharePointPageDataStore ou OneDriveDataStore sont egalement disponibles)
3. Configuration des parametres et des scripts
4. Label : definir ``sharepoint``

**Exemple de configuration des parametres**

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

Definissez ``tenant``, ``client_id`` et ``client_secret`` avec les valeurs obtenues lors de l'enregistrement de l'application dans Entra ID. En specifiant ``site_id``, seul un site particulier sera crawle. Si cette valeur est omise, tous les sites accessibles seront inclus.

Configuration de Box
---------------------

Nous allons ajouter les fichiers Box aux cibles de recherche.

**Preparation dans Box Developer Console**

1. Creer une application personnalisee dans Box Developer Console
2. Selectionner "Authentification serveur (avec identifiants client)" comme methode d'authentification
3. Demander l'approbation de l'application a un administrateur

**Configuration dans Fess**

1. [Crawler] > [Data Store] > [Nouveau]
2. Nom du handler : selectionner BoxDataStore
3. Configuration des parametres et des scripts
4. Label : definir ``box``

**Exemple de configuration des parametres**

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

Configurez les informations d'authentification de l'application personnalisee creee dans Box Developer Console. Le parametre ``supported_mimetypes`` permet de filtrer les types de fichiers a crawler a l'aide d'expressions regulieres.

Optimisation de la recherche transversale
==========================================

Utilisation du crawl differentiel
----------------------------------

Pour le crawl des services de stockage cloud, il est plus efficace d'utiliser le crawl differentiel, qui ne recupere que les fichiers mis a jour depuis le dernier crawl, plutot que de recuperer l'ensemble des fichiers a chaque fois.

Verifiez si l'option de crawl differentiel est disponible dans la configuration de chaque plugin.
Le crawl differentiel permet de reduire le nombre d'appels API et de raccourcir le temps de crawl.

URL des resultats de recherche
-------------------------------

Pour les documents crawles depuis le stockage cloud, un clic sur le lien dans les resultats de recherche ouvre le fichier dans l'interface Web du service correspondant.
Ce comportement est naturel pour les utilisateurs et ne necessite generalement aucune configuration particuliere.

Points d'attention operationnels
=================================

Renouvellement des tokens OAuth
--------------------------------

Lors de l'integration avec les services de stockage cloud, il est important de surveiller la validite des tokens OAuth.

- **Google Drive** : dans le cas d'un compte de service, les tokens sont renouveles automatiquement
- **SharePoint Online** : les secrets client ont une date d'expiration et doivent etre renouveles periodiquement
- **Box** : une re-approbation de l'application peut etre necessaire

Enregistrez les dates d'expiration des tokens dans un calendrier afin d'eviter l'arret du crawl en raison d'une expiration.

Surveillance de l'utilisation des API
--------------------------------------

Les API des services de stockage cloud sont soumises a des limites d'utilisation.
En particulier lors du crawl d'un grand nombre de fichiers, surveillez l'utilisation des API et ajustez les parametres de crawl pour ne pas depasser les limites.

Permissions et securite
------------------------

Le compte de service Fess pour le stockage cloud doit etre configure avec des permissions en lecture seule.
Les permissions en ecriture ne sont pas necessaires, conformement au principe de minimisation des risques de securite.

De plus, en combinant cette approche avec la recherche basee sur les roles abordee dans la Partie 5, il est possible de controler les resultats de recherche en fonction du systeme de permissions du stockage cloud.

Conclusion
==========

Dans cet article, nous avons integre trois services de stockage cloud -- Google Drive, SharePoint Online et Box -- avec Fess pour mettre en place un environnement de recherche transversale.

- Configuration des plugins de data store et de l'authentification OAuth pour chaque service de stockage cloud
- Distinction et filtrage des sources d'information par labels
- Optimisation de l'experience de recherche grace au crawl differentiel
- Gestion des tokens OAuth et surveillance de l'utilisation des API

Cela permet de trouver instantanement les fichiers necessaires sans avoir a se demander sur quel service cloud ils se trouvent.

Dans le prochain article, nous aborderons le cycle de tuning pour l'amelioration continue de la qualite de recherche.

References
==========

- `Configuration des data stores Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Liste des plugins Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
