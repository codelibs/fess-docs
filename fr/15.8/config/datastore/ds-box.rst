==================================
Connecteur Box
==================================

Aperçu
======

Le connecteur Box fournit une fonctionnalité pour récupérer des fichiers depuis
le stockage cloud Box.com et les enregistrer dans l'index de |Fess|.

Ce connecteur s'authentifie auprès de l'entreprise via JWT (Server Authentication)
et explore récursivement les fichiers accessibles à chaque utilisateur de l'entreprise
en les empruntant (impersonation). Les utilisateurs à explorer peuvent être restreints
avec le paramètre ``filter_term``.

Cette fonctionnalité nécessite le plugin ``fess-ds-box``.

Prérequis
=========

1. L'installation du plugin est requise
2. Un compte développeur Box et la création d'une application sont nécessaires
3. La configuration de l'authentification JWT (JSON Web Token) est requise

Installation du plugin
----------------------

Méthode 1 : Placement direct du fichier JAR

::

    # Télécharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Placement
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Installation depuis l'interface d'administration

1. Ouvrez « Système » → « Plugins »
2. Uploadez le fichier JAR
3. Redémarrez |Fess|

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
     - Company Box Storage
   * - Nom du handler
     - BoxDataStore
   * - Actif
     - Oui

Configuration des paramètres
----------------------------

Exemple d'authentification JWT :

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

Paramètres d'authentification (obligatoires)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``client_id``
     - Oui
     - ID client de l'application Box
   * - ``client_secret``
     - Oui
     - Secret client de l'application Box
   * - ``public_key_id``
     - Oui
     - ID de la clé publique
   * - ``private_key``
     - Oui
     - Clé privée (format PEM, les retours à la ligne sont représentés par ``\n``)
   * - ``passphrase``
     - Oui
     - Phrase de passe de la clé privée
   * - ``enterprise_id``
     - Oui
     - ID Box Enterprise

Paramètres d'exploration (optionnels)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Paramètre
     - Valeur par défaut
     - Description
   * - ``max_size``
     - ``10000000``
     - Taille maximale des fichiers à explorer (en octets). Par défaut 10 Mo.
   * - ``supported_mimetypes``
     - ``.*``
     - Types MIME des fichiers à explorer (expression régulière). Plusieurs valeurs séparées par des virgules.
   * - ``include_pattern``
     - (aucun)
     - Modèle d'URL à inclure dans l'exploration
   * - ``exclude_pattern``
     - (aucun)
     - Modèle d'URL à exclure de l'exploration
   * - ``number_of_threads``
     - ``1``
     - Nombre de threads pour le traitement de l'exploration
   * - ``ignore_folder``
     - ``true``
     - Indique si les dossiers doivent être exclus de l'indexation. Dans l'implémentation actuelle, les dossiers ne sont pas indexés (seuls les fichiers sont ciblés), donc ce paramètre n'a aucun effet.
   * - ``ignore_error``
     - ``true``
     - Indique si le traitement doit continuer en cas d'erreur
   * - ``filter_term``
     - (aucun)
     - Condition de filtrage pour restreindre les utilisateurs de l'entreprise à explorer. Si ce paramètre n'est pas spécifié, tous les utilisateurs de l'entreprise sont ciblés.
   * - ``fields``
     - (tous les champs)
     - Spécification des champs à récupérer depuis l'API Box

Paramètres de connexion (optionnels)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Paramètre
     - Valeur par défaut
     - Description
   * - ``base_url``
     - ``https://app.box.com``
     - URL de base utilisée pour construire l'URL permettant d'ouvrir un fichier dans un navigateur (``file.url``). Elle n'affecte pas les points de terminaison de l'API utilisés par le SDK Box.
   * - ``max_retry_count``
     - ``10``
     - Nombre maximum de tentatives pour les appels API
   * - ``proxy_host``
     - (aucun)
     - Nom d'hôte du proxy HTTP
   * - ``proxy_port``
     - (aucun)
     - Numéro de port du proxy HTTP
   * - ``refresh_token_interval``
     - ``3540``
     - Intervalle de renouvellement du token (en secondes). Par défaut 59 minutes.

Configuration du script
-----------------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Champs disponibles
~~~~~~~~~~~~~~~~~~

Champs principaux
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``file.url``
     - Lien pour ouvrir le fichier dans le navigateur
   * - ``file.contents``
     - Contenu texte du fichier
   * - ``file.mimetype``
     - Type MIME du fichier
   * - ``file.filetype``
     - Type de fichier
   * - ``file.name``
     - Nom du fichier
   * - ``file.size``
     - Taille du fichier (en octets)
   * - ``file.created_at``
     - Date de création
   * - ``file.modified_at``
     - Date de dernière modification
   * - ``file.download_url``
     - URL de téléchargement direct Box
   * - ``file.id``
     - ID de l'élément Box
   * - ``file.description``
     - Description du fichier
   * - ``file.extension``
     - Extension du fichier
   * - ``file.sha1``
     - Hachage SHA1 du fichier
   * - ``file.path_collection``
     - Liste des chemins de dossiers

Champs de métadonnées
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``file.type``
     - Type d'élément (« file » ou « folder »)
   * - ``file.file_version``
     - Informations de version du fichier
   * - ``file.sequence_id``
     - ID de séquence
   * - ``file.etag``
     - Hachage ETag
   * - ``file.trashed_at``
     - Date de déplacement vers la corbeille
   * - ``file.purged_at``
     - Date de suppression définitive
   * - ``file.content_created_at``
     - Date de création du contenu
   * - ``file.content_modified_at``
     - Date de modification du contenu
   * - ``file.created_by``
     - Informations sur le créateur
   * - ``file.modified_by``
     - Informations sur le modificateur
   * - ``file.owned_by``
     - Informations sur le propriétaire
   * - ``file.shared_link``
     - Informations sur le lien partagé
   * - ``file.parent``
     - Informations sur le dossier parent
   * - ``file.item_status``
     - Statut de l'élément
   * - ``file.version_number``
     - Numéro de version
   * - ``file.comment_count``
     - Nombre de commentaires
   * - ``file.permissions``
     - Informations sur les permissions
   * - ``file.tags``
     - Informations sur les tags
   * - ``file.lock``
     - Informations sur le verrou
   * - ``file.is_package``
     - Indicateur de package
   * - ``file.is_watermark``
     - Indicateur de filigrane
   * - ``file.collections``
     - Informations sur les collections
   * - ``file.representations``
     - Informations sur les représentations
   * - ``file.api``
     - Objet BoxFileAPI (pour récupérer les informations de collaboration et de permissions)

Pour plus de détails, consultez `Box File Object <https://developer.box.com/reference#file-object>`_.

Configuration de l'authentification Box
=======================================

Procédure de configuration de l'authentification JWT
-----------------------------------------------------

1. Créer une application dans Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accédez à https://app.box.com/developers/console :

1. Cliquez sur « Create New App »
2. Sélectionnez « Custom App »
3. Sélectionnez « Server Authentication (with JWT) » comme méthode d'authentification
4. Entrez le nom de l'application et créez

2. Configuration de l'application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurez dans l'onglet « Configuration » :

**Application Scopes** :

- Cochez « Read all files and folders stored in Box »

**Advanced Features** :

- Cliquez sur « Generate a Public/Private Keypair »
- Téléchargez le fichier JSON généré (important !)

**App Access Level** :

- Sélectionnez « App + Enterprise Access »

3. Autorisation dans l'entreprise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans la console d'administration Box :

1. Ouvrez « Apps » → « Custom Apps »
2. Autorisez l'application créée

4. Obtention des informations d'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtenez les informations suivantes depuis le fichier JSON téléchargé :

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

Format de la clé privée
~~~~~~~~~~~~~~~~~~~~~~~

Remplacez les retours à la ligne de ``private_key`` par ``\n`` pour mettre sur une seule ligne :

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

Exemples d'utilisation
======================

Explorer l'ensemble du stockage Box de l'entreprise
----------------------------------------------------

Paramètres :

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

Script :

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Explorer uniquement un dossier spécifique
-----------------------------------------

Le filtrage par chemin de dossier est possible avec le paramètre ``include_pattern``.

Paramètres :

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    include_pattern=.*Documents/Projects/.*

Script :

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Explorer uniquement les fichiers PDF
-------------------------------------

Le filtrage par type MIME est possible avec le paramètre ``supported_mimetypes``.

Paramètres :

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    supported_mimetypes=application/pdf

Script :

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Dépannage
=========

Erreur d'authentification
--------------------------

**Symptôme** : ``Authentication failed`` ou ``Invalid grant``

**Points à vérifier** :

1. Vérifiez que ``client_id`` et ``client_secret`` sont corrects
2. Vérifiez que la clé privée est correctement copiée (les retours à la ligne sont-ils ``\n`` ?)
3. Vérifiez que la phrase de passe est correcte
4. Vérifiez que l'application est autorisée dans la console d'administration Box
5. Vérifiez que ``enterprise_id`` est correct

Erreur de format de clé privée
--------------------------------

**Symptôme** : ``Invalid private key format``

**Solution** :

Vérifiez que les retours à la ligne sont correctement convertis en ``\n`` :

::

    # Format correct
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # Format incorrect (contient des retours à la ligne réels)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

Impossible de récupérer les fichiers
--------------------------------------

**Symptôme** : L'exploration réussit mais 0 fichier

**Points à vérifier** :

1. Vérifiez que « Read all files and folders » est activé dans Application Scopes
2. Vérifiez que App Access Level est « App + Enterprise Access »
3. Vérifiez que des fichiers existent réellement dans le stockage Box
4. Vérifiez que le compte de service dispose des autorisations appropriées

Nombre de fichiers important
-----------------------------

**Symptôme** : L'exploration prend du temps ou expire

**Solution** :

Répartissez le traitement dans la configuration du DataStore :

1. Ajustez l'intervalle d'exploration
2. Répartissez sur plusieurs DataStores (par dossier, par exemple)
3. Augmentez le nombre de threads avec le paramètre ``number_of_threads``
4. Répartissez la charge avec la configuration des planifications

Droits et contrôle d'accès
===========================

Prise en compte des permissions de collaboration Box
-----------------------------------------------------

Grâce à l'objet ``BoxFileAPI`` fourni par le champ ``file.api``, vous pouvez
associer les informations de collaboration Box aux rôles de recherche de |Fess|.
``file.api.collaborationRoles`` retourne une liste de rôles de recherche correspondant
aux utilisateurs et groupes pouvant accéder au fichier.

Définissez les permissions dans le script :

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.api.collaborationRoles
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

.. note::
   ``file.api.collaborationRoles`` récupère les informations de collaboration pour
   chaque fichier, ce qui augmente le nombre d'appels à l'API Box et peut ralentir
   l'exploration.

Pour attribuer un rôle fixe à tous les fichiers, spécifiez-le comme suit :

::

    role="{role}box-users"

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs DataStore
- :doc:`ds-dropbox` - Connecteur Dropbox
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
