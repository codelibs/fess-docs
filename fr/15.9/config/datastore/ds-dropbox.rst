==================================
Connecteur Dropbox
==================================

Aperçu
======

Le connecteur Dropbox fournit une fonctionnalité pour récupérer des fichiers depuis le
stockage cloud Dropbox et les enregistrer dans l'index de |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-dropbox``.

Services pris en charge
=======================

- Dropbox (stockage de fichiers)
- Dropbox Paper (documents)

Prérequis
=========

1. L'installation du plugin est requise
2. Un compte développeur Dropbox et la création d'une application sont nécessaires
3. L'obtention d'un token d'accès est requise

Installation du plugin
----------------------

Installez depuis l'interface d'administration sous « Système » → « Plugins » :

1. Téléchargez ``fess-ds-dropbox-X.X.X.jar`` depuis Maven Central
2. Uploadez et installez depuis l'interface de gestion des plugins
3. Redémarrez |Fess|

Ou consultez :doc:`../../admin/plugin-guide` pour plus de détails.

Méthode de configuration
========================

Configurez depuis l'interface d'administration : « Crawler » → « DataStore » → « Nouveau ».

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple de configuration
   * - Nom
     - Company Dropbox
   * - Nom du handler
     - DropboxDataStore ou DropboxPaperDataStore
   * - Actif
     - Oui

Configuration des paramètres
-----------------------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``access_token``
     - Oui
     - Token d'accès Dropbox (généré dans App Console)
   * - ``basic_plan``
     - Non
     - ``true`` pour les comptes individuels, ``false`` pour les comptes d'équipe (défaut : ``false``)
   * - ``max_size``
     - Non
     - Taille maximale des fichiers pour l'indexation en octets (défaut : ``10000000``)
   * - ``number_of_threads``
     - Non
     - Nombre de threads pour l'exploration (défaut : ``1``)
   * - ``ignore_folder``
     - Non
     - Ignorer les métadonnées des dossiers (défaut : ``true``)
   * - ``ignore_error``
     - Non
     - Ignorer les erreurs lors de l'extraction de contenu (défaut : ``true``)
   * - ``supported_mimetypes``
     - Non
     - Motifs regex pour les types MIME autorisés, séparés par des virgules (défaut : ``.*``)
   * - ``include_pattern``
     - Non
     - Motif d'URL à inclure dans l'exploration
   * - ``exclude_pattern``
     - Non
     - Motif d'URL à exclure de l'exploration
   * - ``default_permissions``
     - Non
     - Permissions par défaut pour les documents indexés, séparées par des virgules
   * - ``max_cached_content_size``
     - Non
     - Taille maximale du contenu mis en cache en mémoire en octets. Le contenu dépassant cette taille est écrit dans un fichier temporaire (défaut : ``1048576``)
   * - ``readInterval``
     - Non
     - Temps d'attente inséré entre le traitement de chaque enregistrement (en millisecondes) (défaut : ``0``)

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
     - Lien de prévisualisation du fichier
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
     - Date de dernière modification côté client
   * - ``file.server_modified``
     - Date de dernière modification côté serveur
   * - ``file.roles``
     - Autorisations d'accès au fichier
   * - ``file.id``
     - Identifiant du fichier Dropbox
   * - ``file.path_lower``
     - Chemin du fichier en minuscules
   * - ``file.parent_shared_folder_id``
     - ID du dossier partagé parent
   * - ``file.content_hash``
     - Hash du contenu
   * - ``file.rev``
     - Révision du fichier

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
     - Lien de prévisualisation du document Paper
   * - ``paper.contents``
     - Contenu texte du document Paper
   * - ``paper.mimetype``
     - Type MIME
   * - ``paper.filetype``
     - Type de fichier
   * - ``paper.title``
     - Titre du document Paper
   * - ``paper.owner``
     - Propriétaire du document Paper
   * - ``paper.roles``
     - Autorisations d'accès au document
   * - ``paper.revision``
     - Révision du document Paper

Configuration de l'authentification Dropbox
============================================

Type de compte et token d'accès
---------------------------------

Ce connecteur bascule entre deux modes de fonctionnement via le paramètre ``basic_plan``.
Le type d'application et de token d'accès à créer diffère selon le mode ; vérifiez ce point en premier.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Mode
     - ``basic_plan``
     - Description
   * - Compte d'équipe (défaut)
     - ``false``
     - Pour les comptes Dropbox Business (équipe). Un token d'accès disposant des droits d'administrateur d'équipe est requis ; il explore les fichiers des membres de l'équipe et les dossiers d'équipe de manière transversale.
   * - Compte individuel
     - ``true``
     - Pour les comptes personnels (hors équipe). Utilise un token d'accès étendu standard et explore directement les fichiers du compte.

.. note::
   Par défaut (``basic_plan=false``), le connecteur utilise les API de gestion d'équipe (liste des membres, accès aux fichiers par membre, dossiers d'équipe) ;
   un compte Dropbox Business et un token disposant des droits d'administrateur d'équipe sont donc obligatoires. Si vous utilisez un compte individuel, définissez impérativement ``basic_plan=true``.

Procédure d'obtention du token d'accès
---------------------------------------

1. Créer une application dans Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accédez à https://www.dropbox.com/developers/apps :

1. Cliquez sur « Create app »
2. Sélectionnez « Scoped access » pour le type d'API
3. Sélectionnez le type d'accès (« Full Dropbox » recommandé pour explorer l'intégralité d'un compte d'équipe)
4. Saisissez le nom de l'application et créez-la

2. Configuration des permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans l'onglet « Permissions », sélectionnez les permissions nécessaires :

**Permissions requises pour l'exploration des fichiers et de Paper** :

- ``files.metadata.read`` - Lecture des métadonnées des fichiers
- ``files.content.read`` - Lecture du contenu des fichiers et des documents Paper
- ``sharing.read`` - Lecture des informations de partage

**Permissions supplémentaires requises pour les comptes d'équipe (``basic_plan=false``)** :

- ``members.read`` - Lecture de la liste des membres de l'équipe
- Permissions d'accès aux données d'équipe / espaces d'équipe (nécessaires pour explorer les fichiers par membre et les dossiers d'équipe)

.. note::
   En mode compte d'équipe, le connecteur accède à chaque membre et dossier d'équipe en tant qu'administrateur d'équipe.
   Activez les permissions liées à l'équipe ci-dessus dans l'onglet Permissions, puis générez un token d'administrateur d'équipe.

3. Génération du token d'accès
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans l'onglet « Settings » :

1. Faites défiler jusqu'à la section « Generated access token »
2. Cliquez sur le bouton « Generate »
3. Copiez le token généré (ce token ne s'affiche qu'une seule fois)

.. warning::
   Conservez le token d'accès en sécurité. Ce token permet d'accéder à votre compte Dropbox.

4. Configuration du token
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurez le token obtenu dans les paramètres :

::

    access_token=sl.your-dropbox-token-here

Configuration pour compte individuel
======================================

Utilisation avec un compte individuel
---------------------------------------

Pour les comptes individuels (pas les comptes d'équipe),
définissez le paramètre ``basic_plan`` sur ``true`` :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

Quand ``false`` (défaut), le connecteur fonctionne comme un compte d'équipe et explore les fichiers des membres et des dossiers d'équipe.
Quand ``true``, il fonctionne comme un compte individuel et explore directement les fichiers du compte.

Exemples d'utilisation
=======================

Explorer l'ensemble des fichiers Dropbox
-----------------------------------------

Paramètres :

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
--------------------------------------

Paramètres :

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

Exploration avec permissions
------------------------------

Paramètres :

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

Explorer uniquement certains types de fichiers
-----------------------------------------------

Pour n'indexer que certains types MIME, spécifiez dans le paramètre ``supported_mimetypes``
les expressions régulières des types MIME autorisés, séparées par des virgules.

.. note::
   Les scripts de datastore évaluent chaque ligne comme une expression indépendante sous la forme ``champ=expression``.
   Il n'est donc pas possible d'affecter plusieurs champs à l'intérieur d'un bloc ``if`` multiligne.
   Le filtrage par type MIME doit être réalisé via le paramètre ``supported_mimetypes``, et non dans le script.

Paramètres (PDF et fichiers Word uniquement) :

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    supported_mimetypes=application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document

Script :

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

Dépannage
==========

Erreur d'authentification
--------------------------

**Symptôme** : ``Invalid access token`` ou ``401 Unauthorized``

**Points à vérifier** :

1. Vérifiez que le token d'accès est correctement copié
2. Vérifiez que le token n'a pas expiré (utilisez un token longue durée)
3. Vérifiez que les permissions nécessaires sont accordées dans Dropbox App Console
4. Vérifiez que l'application n'est pas désactivée

Impossible de récupérer les fichiers
--------------------------------------

**Symptôme** : L'exploration réussit mais 0 fichier

**Points à vérifier** :

1. Vérifiez le « Access type » de l'application :

   - « Full Dropbox » : Accès à l'ensemble de Dropbox
   - « App folder » : Accès à un dossier spécifique uniquement

2. Vérifiez que les permissions nécessaires sont accordées :

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Vérifiez que des fichiers existent dans le compte Dropbox

Erreur de limitation de débit API
-----------------------------------

**Symptôme** : Erreur ``429 Too Many Requests``

**Solution** :

1. Configurez ``readInterval`` pour espacer le traitement de chaque fichier
2. Réduisez ``number_of_threads`` pour diminuer le nombre de requêtes simultanées
3. Divisez le datastore en plusieurs parties (par dossier, etc.) et décalez les horaires d'exécution

.. note::
   ``basic_plan`` est un paramètre qui bascule entre le type de compte (équipe/individuel) et n'a pas d'effet sur la gestion des limites de débit. Configurez-le correctement selon votre compte.

Impossible de récupérer les documents Paper
--------------------------------------------

**Symptôme** : Les documents Paper ne sont pas explorés

**Points à vérifier** :

1. Vérifiez que le nom du handler est ``DropboxPaperDataStore``
2. Vérifiez que ``files.content.read`` est inclus dans les permissions
3. Vérifiez que des documents Paper existent réellement

En cas de grand nombre de fichiers
------------------------------------

**Symptôme** : L'exploration prend du temps ou expire

**Solution** :

1. Divisez les datastores en plusieurs parties (par dossier, etc.)
2. Répartissez la charge avec les paramètres de planification
3. Pour le plan Basic, faites attention aux limites de débit API

Permissions et contrôle d'accès
=================================

Reflet des permissions de partage Dropbox
------------------------------------------

Les paramètres de partage Dropbox peuvent être reflétés dans les permissions Fess :

Paramètres :

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

Informations de référence
==========================

- :doc:`ds-overview` - Aperçu des connecteurs DataStore
- :doc:`ds-box` - Connecteur Box
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
