==================================
Connecteur Dropbox
==================================

Apercu
======

Le connecteur Dropbox fournit une fonctionnalite pour recuperer des fichiers depuis le stockage cloud Dropbox et les enregistrer dans l'index de |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-dropbox``.

Services pris en charge
=======================

- Dropbox (stockage de fichiers)
- Dropbox Paper (documents)

Prerequis
=========

1. L'installation du plugin est requise
2. Un compte developpeur Dropbox et la creation d'une application sont necessaires
3. L'obtention d'un token d'acces est requise

Installation du plugin
----------------------

Installez depuis l'interface d'administration sous "Systeme" -> "Plugins" :

1. Telechargez ``fess-ds-dropbox-X.X.X.jar`` depuis Maven Central
2. Uploadez et installez depuis l'interface de gestion des plugins
3. Redemarrez |Fess|

Ou consultez :doc:`../../admin/plugin-guide` pour plus de details.

Methode de configuration
========================

Configurez depuis l'interface d'administration : "Crawler" -> "DataStore" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple de configuration
   * - Nom
     - Company Dropbox
   * - Nom du handler
     - DropboxDataStore ou DropboxPaperDataStore
   * - Actif
     - Oui

Configuration des parametres
----------------------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Liste des parametres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``access_token``
     - Oui
     - Token d'acces Dropbox (genere dans App Console)
   * - ``basic_plan``
     - Non
     - ``true`` pour les comptes individuels, ``false`` pour les comptes d'equipe (defaut : ``false``)
   * - ``max_size``
     - Non
     - Taille maximale des fichiers pour l'indexation en octets (defaut : ``10000000``)
   * - ``number_of_threads``
     - Non
     - Nombre de threads pour l'exploration (defaut : ``1``)
   * - ``ignore_folder``
     - Non
     - Ignorer les metadonnees des dossiers (defaut : ``true``)
   * - ``ignore_error``
     - Non
     - Ignorer les erreurs lors de l'extraction de contenu (defaut : ``true``)
   * - ``supported_mimetypes``
     - Non
     - Motifs regex pour les types MIME autorises, separes par des virgules (defaut : ``.*``)
   * - ``include_pattern``
     - Non
     - Motif d'URL a inclure dans l'exploration
   * - ``exclude_pattern``
     - Non
     - Motif d'URL a exclure de l'exploration
   * - ``default_permissions``
     - Non
     - Permissions par defaut pour les documents indexes, separees par des virgules
   * - ``max_cached_content_size``
     - Non
     - Taille maximale du contenu en cache en memoire en octets (defaut : ``1048576``)

Configuration du script
-----------------------

Pour les fichiers Dropbox
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Champs disponibles :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``file.url``
     - Lien de previsualisation du fichier
   * - ``file.contents``
     - Contenu texte du fichier
   * - ``file.mimetype``
     - Type MIME du fichier
   * - ``file.filetype``
     - Type de fichier
   * - ``file.name``
     - Nom du fichier
   * - ``file.path_display``
     - Chemin du fichier
   * - ``file.size``
     - Taille du fichier (octets)
   * - ``file.client_modified``
     - Date de derniere modification cote client
   * - ``file.server_modified``
     - Date de derniere modification cote serveur
   * - ``file.roles``
     - Autorisations d'acces au fichier
   * - ``file.id``
     - Identifiant du fichier Dropbox
   * - ``file.path_lower``
     - Chemin du fichier en minuscules
   * - ``file.parent_shared_folder_id``
     - ID du dossier partage parent
   * - ``file.content_hash``
     - Hash du contenu
   * - ``file.rev``
     - Revision du fichier

Pour Dropbox Paper
~~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Champs disponibles :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``paper.url``
     - Lien de previsualisation du document Paper
   * - ``paper.contents``
     - Contenu texte du document Paper
   * - ``paper.mimetype``
     - Type MIME
   * - ``paper.filetype``
     - Type de fichier
   * - ``paper.title``
     - Titre du document Paper
   * - ``paper.owner``
     - Proprietaire du document Paper
   * - ``paper.roles``
     - Autorisations d'acces au document
   * - ``paper.revision``
     - Revision du document Paper

Configuration de l'authentification Dropbox
===========================================

Procedure d'obtention du token d'acces
--------------------------------------

1. Creer une application dans Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accedez a https://www.dropbox.com/developers/apps :

1. Cliquez sur "Create app"
2. Selectionnez "Scoped access" pour le type d'API
3. Selectionnez "Full Dropbox" ou "App folder" pour le type d'acces
4. Entrez le nom de l'application et creez

2. Configuration des permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans l'onglet "Permissions", selectionnez les permissions necessaires :

**Permissions requises pour l'exploration des fichiers** :

- ``files.metadata.read`` - Lecture des metadonnees des fichiers
- ``files.content.read`` - Lecture du contenu des fichiers
- ``sharing.read`` - Lecture des informations de partage

**Permissions supplementaires requises pour l'exploration Paper** :

- ``files.content.read`` - Lecture des documents Paper

3. Generation du token d'acces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans l'onglet "Settings" :

1. Faites defiler jusqu'a la section "Generated access token"
2. Cliquez sur le bouton "Generate"
3. Copiez le token genere (ce token ne s'affiche qu'une seule fois)

.. warning::
   Conservez le token d'acces en securite. Ce token permet d'acceder a votre compte Dropbox.

4. Configuration du token
~~~~~~~~~~~~~~~~~~~~~~~~~

Configurez le token obtenu dans les parametres :

::

    access_token=sl.your-dropbox-token-here

Configuration pour compte individuel
=====================================

Utilisation avec un compte individuel
-------------------------------------

Pour les comptes individuels (pas les comptes d'equipe),
definissez le parametre ``basic_plan`` sur ``true`` :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

Quand ``false`` (defaut), il fonctionne comme un compte d'equipe et explore les fichiers des membres et des dossiers d'equipe.
Quand ``true``, il fonctionne comme un compte individuel et explore les fichiers directement depuis le compte.

Exemples d'utilisation
======================

Explorer l'ensemble des fichiers Dropbox
----------------------------------------

Parametres :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Script :

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

Explorer les documents Dropbox Paper
------------------------------------

Parametres :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Script :

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

Explorer uniquement certains types de fichiers
----------------------------------------------

Filtrage dans le script :

::

    # Uniquement PDF et fichiers Word
    if (file.mimetype == "application/pdf" || file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        last_modified=file.client_modified
    }

Exploration avec permissions
----------------------------

Parametres :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    default_permissions={role}admin

Script (fichiers Dropbox) :

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Script (Dropbox Paper) :

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Depannage
=========

Erreur d'authentification
-------------------------

**Symptome** : ``Invalid access token`` ou ``401 Unauthorized``

**Points a verifier** :

1. Verifiez que le token d'acces est correctement copie
2. Verifiez que le token n'a pas expire (utilisez un token longue duree)
3. Verifiez que les permissions necessaires sont accordees dans Dropbox App Console
4. Verifiez que l'application n'est pas desactivee

Impossible de recuperer les fichiers
------------------------------------

**Symptome** : L'exploration reussit mais 0 fichier

**Points a verifier** :

1. Verifiez le "Access type" de l'application :

   - "Full Dropbox" : Acces a l'ensemble de Dropbox
   - "App folder" : Acces a un dossier specifique uniquement

2. Verifiez que les permissions necessaires sont accordees :

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Verifiez que des fichiers existent dans le compte Dropbox

Erreur de limitation de debit API
---------------------------------

**Symptome** : Erreur ``429 Too Many Requests``

**Solution** :

1. Pour le plan Basic, configurez ``basic_plan=true``
2. Augmentez l'intervalle d'exploration
3. Utilisez plusieurs tokens d'acces pour repartir la charge

Impossible de recuperer les documents Paper
-------------------------------------------

**Symptome** : Les documents Paper ne sont pas explores

**Points a verifier** :

1. Verifiez que le nom du handler est ``DropboxPaperDataStore``
2. Verifiez que ``files.content.read`` est inclus dans les permissions
3. Verifiez que des documents Paper existent reellement

En cas de grand nombre de fichiers
----------------------------------

**Symptome** : L'exploration prend du temps ou timeout

**Solution** :

1. Divisez les datastores en plusieurs (par dossier, etc.)
2. Repartissez la charge avec les parametres de planification
3. Pour le plan Basic, attention aux limites de debit API

Permissions et controle d'acces
===============================

Reflet des permissions de partage Dropbox
-----------------------------------------

Les parametres de partage Dropbox peuvent etre refletes dans les permissions Fess :

Parametres :

::

    access_token=sl.your-dropbox-token-here
    default_permissions={role}dropbox-users

Script :

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.roles
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

``file.roles`` ou ``paper.roles`` contiennent les informations de partage Dropbox.

Informations de reference
=========================

- :doc:`ds-overview` - Apercu des connecteurs DataStore
- :doc:`ds-box` - Connecteur Box
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
