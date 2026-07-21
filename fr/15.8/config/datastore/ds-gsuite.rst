==================================
Connecteur Google Workspace
==================================

Aperçu
====

Le connecteur Google Workspace fournit la fonctionnalité permettant de récupérer les fichiers
depuis Google Drive (anciennement G Suite) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-gsuite``.

Services pris en charge
============

- Google Drive (Mon Drive, Drive partagés)
- Google Docs, Sheets, Slides, Forms, etc.

Prérequis
========

1. L'installation du plugin est requise
2. La création d'un projet Google Cloud Platform est nécessaire
3. La création d'un compte de service et l'obtention des identifiants sont nécessaires
4. La configuration de la délégation à l'échelle du domaine Google Workspace est nécessaire

Installation du plugin
------------------------

Méthode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Placement
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Système" -> "Plugins"
2. Télécharger le fichier JAR
3. Redémarrer |Fess|

Configuration
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - Company Google Drive
   * - Nom du gestionnaire
     - GoogleDriveDataStore
   * - Active
     - Oui

Configuration des paramètres
----------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

Liste des paramètres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``private_key``
     - Oui
     - Clé privée du compte de service (format PEM, sauts de ligne en ``\n``)
   * - ``private_key_id``
     - Oui
     - ID de la clé privée
   * - ``client_email``
     - Oui
     - Adresse email du compte de service
   * - ``max_size``
     - Non
     - Taille maximale des fichiers à indexer (en octets). Par défaut : ``10000000`` (environ 10 Mo)
   * - ``ignore_folder``
     - Non
     - Ignorer les dossiers ou non. Par défaut : ``true``
   * - ``ignore_error``
     - Non
     - Continuer le traitement en cas d'erreur. Par défaut : ``true``
   * - ``supported_mimetypes``
     - Non
     - Types MIME à indexer (expression régulière, séparés par des virgules). Par défaut : ``.*`` (tous les types)
   * - ``include_pattern``
     - Non
     - Expression régulière des URL à inclure dans l'indexation
   * - ``exclude_pattern``
     - Non
     - Expression régulière des URL à exclure de l'indexation
   * - ``default_permissions``
     - Non
     - Permissions par défaut (séparées par des virgules, ex : ``{role}drive-users``)
   * - ``number_of_threads``
     - Non
     - Nombre de threads de traitement parallèle. Par défaut : ``1``
   * - ``query``
     - Non
     - Chaîne de requête de recherche de l'API Google Drive
   * - ``corpora``
     - Non
     - Corpus à rechercher. Par défaut : ``allDrives``
   * - ``spaces``
     - Non
     - Espaces à rechercher (paramètre ``spaces`` de l'API Google Drive, par ex. ``drive``, ``appDataFolder``). Par défaut : non défini (valeur par défaut de l'API).
   * - ``fields``
     - Non
     - Champs de fichier à demander à l'API Google Drive. Par défaut : ``*`` (tous les champs).
   * - ``read_timeout``
     - Non
     - Délai de lecture HTTP (en millisecondes). Par défaut : ``20000``
   * - ``connect_timeout``
     - Non
     - Délai de connexion HTTP (en millisecondes). Par défaut : ``20000``
   * - ``refresh_token_interval``
     - Non
     - Intervalle (en secondes) pour renouveler le jeton d'accès OAuth. Par défaut : ``3540`` (59 minutes).
   * - ``max_cached_content_size``
     - Non
     - Taille maximale (en octets) du contenu conservé en mémoire ; un contenu plus volumineux est déchargé dans un fichier temporaire. Par défaut : ``1048576`` (1 Mo).
   * - ``proxy_host``
     - Non
     - Nom d'hôte du serveur proxy
   * - ``proxy_port``
     - Non
     - Numéro de port du serveur proxy

Configuration du script
--------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``file.name``
     - Nom du fichier
   * - ``file.description``
     - Description du fichier
   * - ``file.contents``
     - Contenu textuel du fichier
   * - ``file.mimetype``
     - Type MIME du fichier
   * - ``file.filetype``
     - Type de fichier
   * - ``file.created_time``
     - Date de création
   * - ``file.modified_time``
     - Date de dernière modification
   * - ``file.web_view_link``
     - Lien pour ouvrir dans le navigateur
   * - ``file.url``
     - URL du fichier
   * - ``file.thumbnail_link``
     - Lien vers la miniature (valide temporairement)
   * - ``file.size``
     - Taille du fichier (octets)
   * - ``file.roles``
     - Permissions d'accès

Pour plus de détails, consultez `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Configuration Google Cloud Platform
=========================

1. Création du projet
---------------------

Accédez à https://console.cloud.google.com/ :

1. Créez un nouveau projet
2. Entrez le nom du projet
3. Sélectionnez l'organisation et l'emplacement

2. Activation de l'API Google Drive
---------------------------

Dans "APIs et services" -> "Bibliothèque" :

1. Recherchez "Google Drive API"
2. Cliquez sur "Activer"

3. Création du compte de service
---------------------------

Dans "APIs et services" -> "Identifiants" :

1. Sélectionnez "Créer des identifiants" -> "Compte de service"
2. Entrez le nom du compte de service (ex: fess-crawler)
3. Cliquez sur "Créer et continuer"
4. Les rôles ne sont pas nécessaires (ignorez)
5. Cliquez sur "Terminer"

4. Création de la clé du compte de service
-------------------------------

Pour le compte de service créé :

1. Cliquez sur le compte de service
2. Ouvrez l'onglet "Clés"
3. "Ajouter une clé" -> "Créer une nouvelle clé"
4. Sélectionnez le format JSON
5. Enregistrez le fichier JSON téléchargé

5. Activation de la délégation à l'échelle du domaine
-----------------------------

Dans les paramètres du compte de service :

1. Cochez "Activer la délégation à l'échelle du domaine"
2. Cliquez sur "Enregistrer"
3. Copiez "l'ID client OAuth 2"

6. Autorisation dans la console d'administration Google Workspace
---------------------------------------

Accédez à https://admin.google.com/ :

1. Ouvrez "Sécurité" -> "Accès et contrôle des données" -> "Contrôles d'API"
2. Sélectionnez "Délégation à l'échelle du domaine"
3. Cliquez sur "Ajouter nouveau"
4. Entrez l'ID client
5. Entrez les scopes OAuth :

   ::

       https://www.googleapis.com/auth/drive

6. Cliquez sur "Autoriser"

Configuration des identifiants
==============

Obtention des informations depuis le fichier JSON
--------------------------

Fichier JSON téléchargé :

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

Configurez les informations suivantes dans les paramètres :

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (conservez les sauts de ligne en ``\n``)
- ``client_email`` -> ``client_email``

Format de la clé privée
~~~~~~~~~~~~

``private_key`` conserve les sauts de ligne en ``\n`` :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Exemples d'utilisation
======

Crawl de l'ensemble de Google Drive
--------------------------

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    filename=file.name

Crawl avec permissions
----------------

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

Crawler uniquement certains types de fichiers
--------------------------------

Google Docs uniquement :

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

Dépannage
======================

Erreur d'authentification
----------

**Symptôme** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points à vérifier** :

1. Vérifier si les identifiants du compte de service sont corrects :

   - Les sauts de ligne de ``private_key`` sont-ils en ``\n`` ?
   - ``private_key_id`` est-il correct ?
   - ``client_email`` est-il correct ?

2. Vérifier si l'API Google Drive est activée
3. Vérifier si la délégation à l'échelle du domaine est configurée
4. Vérifier si l'autorisation a été accordée dans la console d'administration Google Workspace
5. Vérifier si le scope OAuth est correct (``https://www.googleapis.com/auth/drive``)

Erreur de délégation à l'échelle du domaine
------------------------

**Symptôme** : ``Not Authorized to access this resource/api``

**Solution** :

1. Vérifier l'autorisation dans la console d'administration Google Workspace :

   - L'ID client est-il correctement enregistré ?
   - Le scope OAuth est-il correct ? (``https://www.googleapis.com/auth/drive``)

2. Vérifier si la délégation à l'échelle du domaine est activée sur le compte de service

Impossible de récupérer les fichiers
----------------------

**Symptôme** : Le crawl réussit mais 0 fichiers

**Points à vérifier** :

1. Vérifier si des fichiers existent dans Google Drive
2. Vérifier si le compte de service a les droits de lecture
3. Vérifier si la délégation à l'échelle du domaine est correctement configurée
4. Vérifier si le Drive de l'utilisateur cible est accessible

Erreur de quota API
-----------------

**Symptôme** : ``403 Rate Limit Exceeded`` ou ``429 Too Many Requests``

**Solution** :

1. Vérifier le quota dans Google Cloud Platform
2. Augmenter l'intervalle de crawl
3. Demander une augmentation de quota si nécessaire

Erreur de format de clé privée
--------------------------

**Symptôme** : ``Invalid private key format``

**Solution** :

Vérifier si les sauts de ligne sont correctement en ``\n`` :

::

    # Correct
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Incorrect (contient des sauts de ligne reels)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Crawl des Drive partagés
----------------------

.. note::
   Pour crawler les Drive partagés avec un compte de service,
   vous devez ajouter le compte de service comme membre du Drive partagé.

1. Ouvrez le Drive partagé dans Google Drive
2. Cliquez sur "Gérer les membres"
3. Ajoutez l'adresse email du compte de service
4. Définissez le niveau de permission sur "Lecteur"

Cas de nombreux fichiers
------------------------

**Symptôme** : Le crawl prend du temps ou expire

**Solution** :

1. Diviser en plusieurs data stores
2. Répartir la charge avec les paramètres de planification
3. Ajuster l'intervalle de crawl
4. Crawler uniquement des dossiers spécifiques

Permissions et contrôle d'accès
==================

Reflet des permissions de partage Google Drive
----------------------------

Reflet des paramètres de partage Google Drive dans les permissions Fess :

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles`` contient les informations de partage Google Drive.

Informations de référence
========

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-microsoft365` - Connecteur Microsoft 365
- :doc:`ds-box` - Connecteur Box
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
