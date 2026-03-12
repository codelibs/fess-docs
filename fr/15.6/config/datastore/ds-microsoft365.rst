==================================
Connecteur Microsoft 365
==================================

Apercu
====

Le connecteur Microsoft 365 fournit la fonctionnalite permettant de recuperer des donnees
depuis les services Microsoft 365 (OneDrive, OneNote, Teams, SharePoint) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-microsoft365``.

Services pris en charge
============

- **OneDrive** : Drives utilisateurs, drives de groupe, documents partages
- **OneNote** : Carnets (sites, utilisateurs, groupes)
- **Teams** : Canaux, messages, chats
- **SharePoint Document Libraries** : Metadonnees des bibliotheques de documents
- **SharePoint Lists** : Listes et elements de liste
- **SharePoint Pages** : Pages de site, articles d'actualites

Prerequis
========

1. L'installation du plugin est requise
2. L'enregistrement de l'application Azure AD est necessaire
3. La configuration des permissions de l'API Microsoft Graph et le consentement administrateur sont requis
4. Java 21 ou superieur, Fess 15.2.0 ou superieur

Installation du plugin
------------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # Placement
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2 : Build depuis les sources

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

Apres l'installation, redemarrez |Fess|.

Configuration
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple
   * - Nom
     - Microsoft 365 OneDrive
   * - Nom du gestionnaire
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - Active
     - Oui

Configuration des parametres (communs)
------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

Liste des parametres communs
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
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
     - Nombre de threads de traitement parallele (par defaut : 1)
   * - ``ignore_error``
     - Non
     - Continuer le traitement en cas d'erreur (par defaut : false)
   * - ``include_pattern``
     - Non
     - Pattern regex pour le contenu a inclure
   * - ``exclude_pattern``
     - Non
     - Pattern regex pour le contenu a exclure
   * - ``default_permissions``
     - Non
     - Attribution de role par defaut

Enregistrement d'application Azure AD
============================

1. Enregistrer une application dans le portail Azure
---------------------------------------

Ouvrez Azure Active Directory dans https://portal.azure.com :

1. Cliquez sur "Inscriptions d'applications" -> "Nouvelle inscription"
2. Entrez le nom de l'application
3. Selectionnez les types de comptes pris en charge
4. Cliquez sur "Inscrire"

2. Creation du secret client
---------------------------------

Dans "Certificats et secrets" :

1. Cliquez sur "Nouveau secret client"
2. Definissez une description et une date d'expiration
3. Copiez la valeur du secret (attention : elle ne sera plus visible apres)

3. Ajout des permissions API
----------------

Dans "Permissions de l'API" :

1. Cliquez sur "Ajouter une autorisation"
2. Selectionnez "Microsoft Graph"
3. Selectionnez "Autorisations d'application"
4. Ajoutez les permissions necessaires (voir ci-dessous)
5. Cliquez sur "Accorder un consentement d'administrateur"

Permissions requises par Data Store
==========================

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

- ``Chat.Read.All`` - si chat_id est specifie
- ``Files.Read.All`` - si append_attachment=true

SharePointDocLibDataStore
-------------------------

Permissions requises :

- ``Files.Read.All``
- ``Sites.Read.All``

Ou ``Sites.Selected`` (lorsque site_id est specifie, configuration requise par site)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Permissions requises :

- ``Sites.Read.All``

Ou ``Sites.Selected`` (lorsque site_id est specifie, configuration requise par site)

Configuration du script
==============

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
- ``file.created`` - Date de creation
- ``file.last_modified`` - Date de derniere modification
- ``file.size`` - Taille du fichier
- ``file.web_url`` - URL pour ouvrir dans le navigateur
- ``file.roles`` - Permissions d'acces

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
- ``notebook.contents`` - Contenu integre des sections et pages
- ``notebook.size`` - Taille du contenu (caracteres)
- ``notebook.created`` - Date de creation
- ``notebook.last_modified`` - Date de derniere modification
- ``notebook.web_url`` - URL pour ouvrir dans le navigateur
- ``notebook.roles`` - Permissions d'acces

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
- ``message.created_date_time`` - Date de creation
- ``message.last_modified_date_time`` - Date de derniere modification
- ``message.web_url`` - URL pour ouvrir dans le navigateur
- ``message.roles`` - Permissions d'acces
- ``message.from`` - Informations sur l'expediteur

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

- ``doclib.name`` - Nom de la bibliotheque de documents
- ``doclib.description`` - Description de la bibliotheque
- ``doclib.content`` - Contenu integre pour la recherche
- ``doclib.created`` - Date de creation
- ``doclib.modified`` - Date de derniere modification
- ``doclib.url`` - URL SharePoint
- ``doclib.site_name`` - Nom du site

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

- ``item.title`` - Titre de l'element de liste
- ``item.content`` - Contenu textuel
- ``item.created`` - Date de creation
- ``item.modified`` - Date de derniere modification
- ``item.url`` - URL SharePoint
- ``item.fields`` - Map de tous les champs
- ``item.roles`` - Permissions d'acces

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
- ``page.created`` - Date de creation
- ``page.modified`` - Date de derniere modification
- ``page.url`` - URL SharePoint
- ``page.type`` - Type de page (news/article/page)
- ``page.roles`` - Permissions d'acces

Parametres supplementaires par Data Store
================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
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
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    ignore_system_pages=true
    page_type_filter=

Exemples d'utilisation
======

Crawl de tous les drives OneDrive
----------------------------

Parametres :

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

Crawl des messages Teams d'une equipe specifique
------------------------------------

Parametres :

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+01:00

Script :

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

Crawl des listes SharePoint
--------------------------

Parametres :

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

Depannage
======================

Erreur d'authentification
----------

**Symptome** : ``Authentication failed`` ou ``Insufficient privileges``

**Points a verifier** :

1. Verifier si l'ID de locataire, l'ID client et le secret client sont corrects
2. Verifier si les permissions API necessaires sont accordees dans le portail Azure
3. Verifier si le consentement administrateur a ete donne
4. Verifier la date d'expiration du secret client

Erreur de limitation de debit API
-------------------

**Symptome** : ``429 Too Many Requests``

**Solution** :

1. Reduire ``number_of_threads`` (definir a 1 ou 2)
2. Augmenter l'intervalle de crawl
3. Definir ``ignore_error=true`` pour continuer le traitement

Impossible de recuperer les donnees
--------------------

**Symptome** : Le crawl reussit mais 0 documents

**Points a verifier** :

1. Verifier si les donnees cibles existent
2. Verifier si les permissions API sont correctement configurees
3. Verifier les parametres du crawler de drive utilisateur/groupe
4. Verifier les messages d'erreur dans les logs

Comment verifier l'ID de site SharePoint
----------------------------

Verifier avec PowerShell :

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

Ou avec l'API Microsoft Graph :

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

Crawl de donnees volumineuses
--------------------

**Solution** :

1. Diviser en plusieurs data stores (par site, par drive, etc.)
2. Repartir la charge avec les parametres de planification
3. Ajuster ``number_of_threads`` pour le traitement parallele
4. Crawler uniquement des dossiers/sites specifiques

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
