==================================
Connecteur Box
==================================

Apercu
======

Le connecteur Box fournit une fonctionnalite pour recuperer des fichiers depuis le stockage cloud Box.com et les enregistrer dans l'index de |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-box``.

Prerequis
=========

1. L'installation du plugin est requise
2. Un compte developpeur Box et la creation d'une application sont necessaires
3. La configuration de l'authentification JWT (JSON Web Token) ou OAuth 2.0 est requise

Installation du plugin
----------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Placement
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2 : Installation depuis l'interface d'administration

1. Ouvrez "Systeme" -> "Plugins"
2. Uploadez le fichier JAR
3. Redemarrez |Fess|

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
     - Company Box Storage
   * - Nom du handler
     - BoxDataStore
   * - Actif
     - Oui

Configuration des parametres
----------------------------

Exemple d'authentification JWT (recommande) :

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Liste des parametres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
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
     - ID de la cle publique
   * - ``private_key``
     - Oui
     - Cle privee (format PEM, les retours a la ligne sont representes par ``\\n``)
   * - ``passphrase``
     - Oui
     - Phrase de passe de la cle privee
   * - ``enterprise_id``
     - Oui
     - ID Box Enterprise

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
     - Taille du fichier (octets)
   * - ``file.created_at``
     - Date de creation
   * - ``file.modified_at``
     - Date de derniere modification

Pour plus de details, consultez `Box File Object <https://developer.box.com/reference#file-object>`_.

Configuration de l'authentification Box
=======================================

Procedure de configuration de l'authentification JWT
----------------------------------------------------

1. Creer une application dans Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accedez a https://app.box.com/developers/console :

1. Cliquez sur "Create New App"
2. Selectionnez "Custom App"
3. Selectionnez "Server Authentication (with JWT)" comme methode d'authentification
4. Entrez le nom de l'application et creez

2. Configuration de l'application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurez dans l'onglet "Configuration" :

**Application Scopes** :

- Cochez "Read all files and folders stored in Box"

**Advanced Features** :

- Cliquez sur "Generate a Public/Private Keypair"
- Telechargez le fichier JSON genere (important !)

**App Access Level** :

- Selectionnez "App + Enterprise Access"

3. Autorisation dans l'entreprise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans la console d'administration Box :

1. Ouvrez "Apps" -> "Custom Apps"
2. Autorisez l'application creee

4. Obtention des informations d'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtenez les informations suivantes depuis le fichier JSON telecharge :

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

Format de la cle privee
~~~~~~~~~~~~~~~~~~~~~~~

Remplacez les retours a la ligne de ``private_key`` par ``\\n`` pour mettre sur une seule ligne :

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\\nMIIFDjBABgk...=\\n-----END ENCRYPTED PRIVATE KEY-----\\n

Exemples d'utilisation
======================

Explorer l'ensemble du stockage Box de l'entreprise
---------------------------------------------------

Parametres :

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\\n-----END ENCRYPTED PRIVATE KEY-----\\n
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

Explorer uniquement les fichiers PDF
------------------------------------

Filtrage par type MIME dans le script :

::

    if (file.mimetype == "application/pdf") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        created=file.created_at
        last_modified=file.modified_at
    }

Depannage
=========

Erreur d'authentification
-------------------------

**Symptome** : ``Authentication failed`` ou ``Invalid grant``

**Points a verifier** :

1. Verifiez que ``client_id`` et ``client_secret`` sont corrects
2. Verifiez que la cle privee est correctement copiee (les retours a la ligne sont-ils ``\\n`` ?)
3. Verifiez que la phrase de passe est correcte
4. Verifiez que l'application est autorisee dans la console d'administration Box
5. Verifiez que ``enterprise_id`` est correct

Erreur de format de cle privee
------------------------------

**Symptome** : ``Invalid private key format``

**Solution** :

Verifiez que les retours a la ligne sont correctement convertis en ``\\n`` :

::

    # Format correct
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\\nMIIFDj...\\n-----END ENCRYPTED PRIVATE KEY-----\\n

    # Format incorrect (contient des retours a la ligne reels)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

Impossible de recuperer les fichiers
------------------------------------

**Symptome** : L'exploration reussit mais 0 fichier

**Points a verifier** :

1. Verifiez que "Read all files and folders" est active dans Application Scopes
2. Verifiez que App Access Level est "App + Enterprise Access"
3. Verifiez que des fichiers existent reellement dans le stockage Box
4. Verifiez que le compte de service dispose des autorisations appropriees

Informations de reference
=========================

- :doc:`ds-overview` - Apercu des connecteurs DataStore
- :doc:`ds-dropbox` - Connecteur Dropbox
- :doc:`ds-gsuite` - Connecteur Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
