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
     - ``true`` pour le plan Basic (defaut : ``false``)

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

Pour Dropbox Paper
~~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

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

Configuration pour le plan Basic
================================

Limitations du plan Dropbox Basic
---------------------------------

Si vous utilisez le plan Dropbox Basic, les limitations API sont differentes.
Definissez le parametre ``basic_plan`` sur ``true`` :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

Cela permet un traitement adapte aux limitations de debit API.

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

Informations de reference
=========================

- :doc:`ds-overview` - Apercu des connecteurs DataStore
- :doc:`ds-box` - Connecteur Box
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
