==================================
Connecteur Google Workspace
==================================

Apercu
====

Le connecteur Google Workspace fournit la fonctionnalite permettant de recuperer les fichiers
depuis Google Drive (anciennement G Suite) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-gsuite``.

Services pris en charge
============

- Google Drive (Mon Drive, Drive partages)
- Google Docs, Sheets, Slides, Forms, etc.

Prerequis
========

1. L'installation du plugin est requise
2. La creation d'un projet Google Cloud Platform est necessaire
3. La creation d'un compte de service et l'obtention des identifiants sont necessaires
4. La configuration de la delegation a l'echelle du domaine Google Workspace est necessaire

Installation du plugin
------------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Placement
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Systeme" -> "Plugins"
2. Telecharger le fichier JAR
3. Redemarrer |Fess|

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
     - Company Google Drive
   * - Nom du gestionnaire
     - GSuiteDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``private_key``
     - Oui
     - Cle privee du compte de service (format PEM, sauts de ligne en ``\n``)
   * - ``private_key_id``
     - Oui
     - ID de la cle privee
   * - ``client_email``
     - Oui
     - Adresse email du compte de service

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
     - Date de creation
   * - ``file.modified_time``
     - Date de derniere modification
   * - ``file.web_view_link``
     - Lien pour ouvrir dans le navigateur
   * - ``file.url``
     - URL du fichier
   * - ``file.thumbnail_link``
     - Lien vers la miniature (valide temporairement)
   * - ``file.size``
     - Taille du fichier (octets)
   * - ``file.roles``
     - Permissions d'acces

Pour plus de details, consultez `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Configuration Google Cloud Platform
=========================

1. Creation du projet
---------------------

Accedez a https://console.cloud.google.com/ :

1. Creez un nouveau projet
2. Entrez le nom du projet
3. Selectionnez l'organisation et l'emplacement

2. Activation de l'API Google Drive
---------------------------

Dans "APIs et services" -> "Bibliotheque" :

1. Recherchez "Google Drive API"
2. Cliquez sur "Activer"

3. Creation du compte de service
---------------------------

Dans "APIs et services" -> "Identifiants" :

1. Selectionnez "Creer des identifiants" -> "Compte de service"
2. Entrez le nom du compte de service (ex: fess-crawler)
3. Cliquez sur "Creer et continuer"
4. Les roles ne sont pas necessaires (ignorez)
5. Cliquez sur "Terminer"

4. Creation de la cle du compte de service
-------------------------------

Pour le compte de service cree :

1. Cliquez sur le compte de service
2. Ouvrez l'onglet "Cles"
3. "Ajouter une cle" -> "Creer une nouvelle cle"
4. Selectionnez le format JSON
5. Enregistrez le fichier JSON telecharge

5. Activation de la delegation a l'echelle du domaine
-----------------------------

Dans les parametres du compte de service :

1. Cochez "Activer la delegation a l'echelle du domaine"
2. Cliquez sur "Enregistrer"
3. Copiez "l'ID client OAuth 2"

6. Autorisation dans la console d'administration Google Workspace
---------------------------------------

Accedez a https://admin.google.com/ :

1. Ouvrez "Securite" -> "Acces et controle des donnees" -> "Controles d'API"
2. Selectionnez "Delegation a l'echelle du domaine"
3. Cliquez sur "Ajouter nouveau"
4. Entrez l'ID client
5. Entrez les scopes OAuth :

   ::

       https://www.googleapis.com/auth/drive.readonly

6. Cliquez sur "Autoriser"

Configuration des identifiants
==============

Obtention des informations depuis le fichier JSON
--------------------------

Fichier JSON telecharge :

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

Configurez les informations suivantes dans les parametres :

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (conservez les sauts de ligne en ``\n``)
- ``client_email`` -> ``client_email``

Format de la cle privee
~~~~~~~~~~~~

``private_key`` conserve les sauts de ligne en ``\n`` :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Exemples d'utilisation
======

Crawl de l'ensemble de Google Drive
--------------------------

Parametres :

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

Parametres :

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

Depannage
======================

Erreur d'authentification
----------

**Symptome** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points a verifier** :

1. Verifier si les identifiants du compte de service sont corrects :

   - Les sauts de ligne de ``private_key`` sont-ils en ``\n`` ?
   - ``private_key_id`` est-il correct ?
   - ``client_email`` est-il correct ?

2. Verifier si l'API Google Drive est activee
3. Verifier si la delegation a l'echelle du domaine est configuree
4. Verifier si l'autorisation a ete accordee dans la console d'administration Google Workspace
5. Verifier si le scope OAuth est correct (``https://www.googleapis.com/auth/drive.readonly``)

Erreur de delegation a l'echelle du domaine
------------------------

**Symptome** : ``Not Authorized to access this resource/api``

**Solution** :

1. Verifier l'autorisation dans la console d'administration Google Workspace :

   - L'ID client est-il correctement enregistre ?
   - Le scope OAuth est-il correct ? (``https://www.googleapis.com/auth/drive.readonly``)

2. Verifier si la delegation a l'echelle du domaine est activee sur le compte de service

Impossible de recuperer les fichiers
----------------------

**Symptome** : Le crawl reussit mais 0 fichiers

**Points a verifier** :

1. Verifier si des fichiers existent dans Google Drive
2. Verifier si le compte de service a les droits de lecture
3. Verifier si la delegation a l'echelle du domaine est correctement configuree
4. Verifier si le Drive de l'utilisateur cible est accessible

Erreur de quota API
-----------------

**Symptome** : ``403 Rate Limit Exceeded`` ou ``429 Too Many Requests``

**Solution** :

1. Verifier le quota dans Google Cloud Platform
2. Augmenter l'intervalle de crawl
3. Demander une augmentation de quota si necessaire

Erreur de format de cle privee
--------------------------

**Symptome** : ``Invalid private key format``

**Solution** :

Verifier si les sauts de ligne sont correctement en ``\n`` :

::

    # Correct
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Incorrect (contient des sauts de ligne reels)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Crawl des Drive partages
----------------------

.. note::
   Pour crawler les Drive partages avec un compte de service,
   vous devez ajouter le compte de service comme membre du Drive partage.

1. Ouvrez le Drive partage dans Google Drive
2. Cliquez sur "Gerer les membres"
3. Ajoutez l'adresse email du compte de service
4. Definissez le niveau de permission sur "Lecteur"

Cas de nombreux fichiers
------------------------

**Symptome** : Le crawl prend du temps ou expire

**Solution** :

1. Diviser en plusieurs data stores
2. Repartir la charge avec les parametres de planification
3. Ajuster l'intervalle de crawl
4. Crawler uniquement des dossiers specifiques

Permissions et controle d'acces
==================

Reflet des permissions de partage Google Drive
----------------------------

Reflet des parametres de partage Google Drive dans les permissions Fess :

Parametres :

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

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-microsoft365` - Connecteur Microsoft 365
- :doc:`ds-box` - Connecteur Box
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
