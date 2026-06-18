==================================
Connecteur Microsoft 365
==================================

Aperçu
======

Le connecteur Microsoft 365 fournit la fonctionnalité permettant de récupérer des données
depuis les services Microsoft 365 (OneDrive, OneNote, Teams, SharePoint) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-microsoft365``.

Services pris en charge
=======================

- **OneDrive** : Drives utilisateurs, drives de groupe, documents partagés
- **OneNote** : Carnets (sites, utilisateurs, groupes)
- **Teams** : Canaux, messages, chats
- **SharePoint Document Libraries** : Métadonnées des bibliothèques de documents
- **SharePoint Lists** : Listes et éléments de liste
- **SharePoint Pages** : Pages de site, articles d'actualités

Prérequis
=========

1. L'installation du plugin est requise
2. L'enregistrement de l'application Azure AD est nécessaire
3. La configuration des permissions de l'API Microsoft Graph et le consentement administrateur sont requis
4. Java 21 ou supérieur, Fess 15.2.0 ou supérieur

Installation du plugin
----------------------

Méthode 1 : Placement direct du fichier JAR

::

    # Télécharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # Placement
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Build depuis les sources

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

Après l'installation, redémarrez |Fess|.

Configuration
=============

Configurez depuis l'interface d'administration via « Crawler » → « Data Store » → « Nouveau ».

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple de configuration
   * - Nom
     - Microsoft 365 OneDrive
   * - Nom du gestionnaire
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - Activé
     - Oui

Configuration des paramètres (communs)
--------------------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

Liste des paramètres communs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``tenant``
     - Oui
     - ID de locataire Azure AD
   * - ``client_id``
     - Oui
     - ID client de l'enregistrement d'application
   * - ``client_secret``
     - Oui
     - Secret client de l'enregistrement d'application
   * - ``number_of_threads``
     - Non
     - Nombre de threads de traitement parallèle (par défaut : 1)
   * - ``ignore_error``
     - Non
     - Continuer le traitement en cas d'erreur (par défaut : false)
   * - ``max_content_length``
     - Non
     - Taille maximale du contenu récupéré (par défaut : -1, illimité)
   * - ``cache_size``
     - Non
     - Taille du cache des informations utilisateur/groupe (par défaut : 10000)
   * - ``proxy_host``
     - Non
     - Hôte du proxy HTTP
   * - ``proxy_port``
     - Non
     - Port du proxy HTTP
   * - ``proxy_username``
     - Non
     - Nom d'utilisateur pour l'authentification proxy
   * - ``proxy_password``
     - Non
     - Mot de passe pour l'authentification proxy

Enregistrement d'application Azure AD
======================================

1. Enregistrer une application dans le portail Azure
-----------------------------------------------------

Ouvrez Azure Active Directory dans https://portal.azure.com :

1. Cliquez sur « Inscriptions d'applications » → « Nouvelle inscription »
2. Entrez le nom de l'application
3. Sélectionnez les types de comptes pris en charge
4. Cliquez sur « Inscrire »

2. Création du secret client
-----------------------------

Dans « Certificats et secrets » :

1. Cliquez sur « Nouveau secret client »
2. Définissez une description et une date d'expiration
3. Copiez la valeur du secret (attention : elle ne sera plus visible après)

3. Ajout des permissions API
-----------------------------

Dans « Autorisations des API » :

1. Cliquez sur « Ajouter une autorisation »
2. Sélectionnez « Microsoft Graph »
3. Sélectionnez « Autorisations d'application »
4. Ajoutez les permissions nécessaires (voir ci-dessous)
5. Cliquez sur « Accorder un consentement d'administrateur »

Permissions requises par Data Store
=====================================

OneDriveDataStore
-----------------

Permissions requises :

- ``Files.Read.All``

Permissions conditionnelles :

- ``User.Read.All`` - si user_drive_crawler=true
- ``Group.Read.All`` - si group_drive_crawler=true
- ``Sites.Read.All`` - si shared_documents_drive_crawler=true

OneNoteDataStore
----------------

Permissions requises :

- ``Notes.Read.All``

Permissions conditionnelles :

- ``User.Read.All`` - si user_note_crawler=true
- ``Group.Read.All`` - si group_note_crawler=true
- ``Sites.Read.All`` - si site_note_crawler=true

TeamsDataStore
--------------

Permissions requises :

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

Permissions conditionnelles :

- ``Chat.Read.All`` - si chat_id est spécifié
- ``Files.Read.All`` - si append_attachment=true

SharePointDocLibDataStore
-------------------------

Permissions requises :

- ``Files.Read.All``
- ``Sites.Read.All``

Ou ``Sites.Selected`` (lorsque site_id est spécifié, configuration requise par site)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Permissions requises :

- ``Sites.Read.All``

Ou ``Sites.Selected`` (lorsque site_id est spécifié, configuration requise par site)

Configuration du script
========================

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Champs disponibles :

- ``file.name`` - Nom du fichier
- ``file.description`` - Description du fichier
- ``file.contents`` - Contenu textuel
- ``file.mimetype`` - Type MIME
- ``file.filetype`` - Type de fichier
- ``file.created`` - Date de création
- ``file.last_modified`` - Date de dernière modification
- ``file.size`` - Taille du fichier
- ``file.web_url`` - URL pour ouvrir dans le navigateur
- ``file.url`` - URL du fichier
- ``file.id`` - ID de l'élément du drive
- ``file.ctag`` - Tag de modification (cTag)
- ``file.etag`` - Tag d'entité (eTag)
- ``file.webdav_url`` - URL WebDAV
- ``file.parent_id`` - ID du dossier parent
- ``file.parent_name`` - Nom du dossier parent
- ``file.parent_path`` - Chemin du dossier parent
- ``file.roles`` - Permissions d'accès

.. note::

   En plus des champs ci-dessus, d'autres champs de métadonnées Microsoft Graph sont disponibles, notamment ``file.createdby_user``, ``file.last_modifiedby_user``, ``file.image``,
   ``file.video``, ``file.special_folder``, etc.

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

Champs disponibles :

- ``notebook.name`` - Nom du carnet
- ``notebook.contents`` - Contenu intégré des sections et pages
- ``notebook.size`` - Taille du contenu (nombre de caractères)
- ``notebook.created`` - Date de création
- ``notebook.last_modified`` - Date de dernière modification
- ``notebook.web_url`` - URL pour ouvrir dans le navigateur
- ``notebook.roles`` - Permissions d'accès

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

Champs disponibles :

- ``message.title`` - Titre du message
- ``message.content`` - Contenu du message
- ``message.body`` - Corps du message (données brutes incluant le HTML)
- ``message.subject`` - Objet du message
- ``message.summary`` - Résumé du message
- ``message.importance`` - Importance
- ``message.from`` - Informations sur l'expéditeur
- ``message.created_date_time`` - Date de création
- ``message.last_modified_date_time`` - Date de dernière modification
- ``message.last_edited_date_time`` - Date de dernière édition
- ``message.deleted_date_time`` - Date de suppression
- ``message.web_url`` - URL pour ouvrir dans le navigateur
- ``message.id`` - ID du message
- ``message.etag`` - Tag d'entité
- ``message.locale`` - Paramètre régional
- ``message.chat_id`` - ID du chat
- ``message.reply_to_id`` - ID du message d'origine de la réponse
- ``message.channel_identity`` - Identité du canal (ID d'équipe et ID de canal)
- ``message.mentions`` - Informations sur les mentions
- ``message.attachments`` - Informations sur les pièces jointes
- ``message.replies`` - Messages de réponse
- ``message.hosted_contents`` - Contenu inline (images, etc.)
- ``message.roles`` - Permissions d'accès

Champs de premier niveau (définis uniquement pour les messages de canal) :

- ``team`` - Équipe (objet ``Group`` de Microsoft Graph)
- ``channel`` - Canal (objet ``Channel`` de Microsoft Graph)
- ``parent`` - Message parent (défini pour les messages de réponse)

SharePoint Document Libraries
------------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

Champs disponibles :

- ``doclib.name`` - Nom de la bibliothèque de documents
- ``doclib.description`` - Description de la bibliothèque
- ``doclib.content`` - Contenu intégré pour la recherche
- ``doclib.created`` - Date de création
- ``doclib.modified`` - Date de dernière modification
- ``doclib.url`` - URL SharePoint
- ``doclib.web_url`` - URL pour ouvrir dans le navigateur
- ``doclib.id`` - ID de la bibliothèque de documents
- ``doclib.type`` - Type de document
- ``doclib.site_name`` - Nom du site
- ``doclib.site_url`` - URL du site
- ``doclib.roles`` - Permissions d'accès

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Champs disponibles :

- ``item.title`` - Titre de l'élément de liste
- ``item.content`` - Contenu textuel
- ``item.created`` - Date de création
- ``item.modified`` - Date de dernière modification
- ``item.url`` - URL SharePoint
- ``item.web_url`` - URL pour ouvrir dans le navigateur
- ``item.id`` - ID de l'élément de liste
- ``item.content_type`` - Type de contenu
- ``item.fields`` - Map de tous les champs
- ``item.roles`` - Permissions d'accès

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

Champs disponibles :

- ``page.title`` - Titre de la page
- ``page.content`` - Contenu de la page
- ``page.created`` - Date de création
- ``page.modified`` - Date de dernière modification
- ``page.url`` - URL SharePoint
- ``page.web_url`` - URL pour ouvrir dans le navigateur
- ``page.id`` - ID de la page
- ``page.description`` - Description de la page
- ``page.author`` - Auteur
- ``page.type`` - Type de page (news/article/page)
- ``page.site_name`` - Nom du site
- ``page.site_url`` - URL du site
- ``page.promotion_state`` - État de promotion
- ``page.roles`` - Permissions d'accès

Paramètres supplémentaires par Data Store
==========================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=
    url_filter=
    default_permissions=
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    default_permissions=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
-----------------------------

::

    site_id=
    exclude_site_id=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_pages=true
    page_type_filter=

Exemples d'utilisation
=======================

Crawl de tous les drives OneDrive
----------------------------------

Paramètres :

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Crawl des messages Teams d'une équipe spécifique
-------------------------------------------------

Paramètres :

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+09:00

Script :

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

Crawl des listes SharePoint
----------------------------

Paramètres :

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

Script :

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Dépannage
==========

Erreur d'authentification
--------------------------

**Symptôme** : ``Authentication failed`` ou ``Insufficient privileges``

**Points à vérifier** :

1. Vérifier si l'ID de locataire, l'ID client et le secret client sont corrects
2. Vérifier si les permissions API nécessaires sont accordées dans le portail Azure
3. Vérifier si le consentement administrateur a été accordé
4. Vérifier la date d'expiration du secret client

Erreur de limitation de débit API
-----------------------------------

**Symptôme** : ``429 Too Many Requests``

**Solution** :

1. Réduire ``number_of_threads`` (définir à 1 ou 2)
2. Augmenter l'intervalle de crawl
3. Définir ``ignore_error=true`` pour continuer le traitement

Impossible de récupérer les données
-------------------------------------

**Symptôme** : Le crawl réussit mais 0 documents

**Points à vérifier** :

1. Vérifier si les données cibles existent
2. Vérifier si les permissions API sont correctement configurées
3. Vérifier les paramètres du crawler de drive utilisateur/groupe
4. Vérifier les messages d'erreur dans les logs

Comment vérifier l'ID de site SharePoint
------------------------------------------

Vérifier avec PowerShell :

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

Ou avec l'API Microsoft Graph :

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

Crawl de données volumineuses
-------------------------------

**Solution** :

1. Diviser en plusieurs data stores (par site, par drive, etc.)
2. Répartir la charge avec les paramètres de planification
3. Ajuster ``number_of_threads`` pour le traitement parallèle
4. Crawler uniquement des dossiers/sites spécifiques

Informations de référence
===========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
