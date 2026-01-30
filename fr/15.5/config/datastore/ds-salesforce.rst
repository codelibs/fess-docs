==================================
Connecteur Salesforce
==================================

Apercu
====

Le connecteur Salesforce fournit la fonctionnalite permettant de recuperer des donnees
depuis les objets Salesforce (objets standard, objets personnalises) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-salesforce``.

Objets pris en charge
================

- **Objets standard** : Account, Contact, Lead, Opportunity, Case, Solution, etc.
- **Objets personnalises** : Objets crees par l'utilisateur
- **Articles Knowledge** : Salesforce Knowledge

Prerequis
========

1. L'installation du plugin est requise
2. La creation d'une application connectee (Connected App) Salesforce est necessaire
3. La configuration de l'authentification OAuth est necessaire
4. L'acces en lecture aux objets est requis

Installation du plugin
------------------------

Installez depuis l'interface d'administration via "Systeme" -> "Plugins".

Ou consultez :doc:`../../admin/plugin-guide` pour plus de details.

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
     - Salesforce CRM
   * - Nom du gestionnaire
     - SalesforceDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

Authentification OAuth Token (recommandee) :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

Authentification OAuth Password :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``base_url``
     - Oui
     - URL Salesforce (Production : ``https://login.salesforce.com``, Sandbox : ``https://test.salesforce.com``)
   * - ``auth_type``
     - Oui
     - Type d'authentification (``oauth_token`` ou ``oauth_password``)
   * - ``username``
     - Oui
     - Nom d'utilisateur Salesforce
   * - ``client_id``
     - Oui
     - Consumer Key de l'application connectee
   * - ``private_key``
     - Pour oauth_token
     - Cle privee (format PEM, sauts de ligne en ``\n``)
   * - ``client_secret``
     - Pour oauth_password
     - Consumer Secret de l'application connectee
   * - ``security_token``
     - Pour oauth_password
     - Token de securite de l'utilisateur
   * - ``number_of_threads``
     - Non
     - Nombre de threads de traitement parallele (par defaut : 1)
   * - ``ignoreError``
     - Non
     - Continuer le traitement en cas d'erreur (par defaut : true)
   * - ``custom``
     - Non
     - Noms des objets personnalises (separes par des virgules)
   * - ``<objet>.title``
     - Non
     - Nom du champ a utiliser pour le titre
   * - ``<objet>.contents``
     - Non
     - Noms des champs a utiliser pour le contenu (separes par des virgules)

Configuration du script
--------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``object.type``
     - Type de l'objet (ex: Case, User, Solution)
   * - ``object.title``
     - Nom de l'objet
   * - ``object.description``
     - Description de l'objet
   * - ``object.content``
     - Contenu textuel de l'objet
   * - ``object.id``
     - ID de l'objet
   * - ``object.content_length``
     - Longueur du contenu
   * - ``object.created``
     - Date de creation
   * - ``object.last_modified``
     - Date de derniere modification
   * - ``object.url``
     - URL de l'objet
   * - ``object.thumbnail``
     - URL de la miniature

Configuration de l'application connectee Salesforce
====================================

1. Creation de l'application connectee
-----------------------------

Dans Salesforce Setup :

1. Ouvrez "Gestionnaire d'applications"
2. Cliquez sur "Nouvelle application connectee"
3. Entrez les informations de base :

   - Nom de l'application connectee : Fess Crawler
   - Nom de l'API : Fess_Crawler
   - Email de contact : your-email@example.com

4. Cochez "Activer les parametres OAuth (Activer OAuth)"

2. Configuration de l'authentification OAuth Token (recommandee)
--------------------------------

Dans les parametres OAuth :

1. Cochez "Utiliser les signatures numeriques"
2. Telechargez un certificat (cree selon les etapes ci-dessous)
3. Scopes OAuth selectionnes :

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. Cliquez sur "Enregistrer"
5. Copiez la Consumer Key

Creation du certificat :

::

    # Generation de la cle privee
    openssl genrsa -out private_key.pem 2048

    # Generation du certificat
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # Verification de la cle privee
    cat private_key.pem

Telechargez le certificat (certificate.crt) sur Salesforce et
configurez le contenu de la cle privee (private_key.pem) dans les parametres.

3. Configuration de l'authentification OAuth Password
---------------------------

Dans les parametres OAuth :

1. URL de callback : ``https://localhost`` (non utilisee mais requise)
2. Scopes OAuth selectionnes :

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. Cliquez sur "Enregistrer"
4. Copiez la Consumer Key et le Consumer Secret

Obtention du token de securite :

1. Ouvrez les parametres personnels dans Salesforce
2. Cliquez sur "Reinitialiser mon token de securite"
3. Copiez le token envoye par email

4. Autorisation de l'application connectee
-----------------------------

Dans "Administration" -> "Gerer les applications connectees" :

1. Selectionnez l'application connectee creee
2. Cliquez sur "Modifier"
3. Changez "Utilisateurs autorises" en "Les utilisateurs approuves par l'administrateur sont preautorises"
4. Attribuez des profils ou des ensembles de permissions

Configuration des objets personnalises
==========================

Crawl des objets personnalises
------------------------------

Specifiez les noms des objets personnalises avec le parametre ``custom`` :

::

    custom=FessObj,CustomProduct,ProjectTask

Mapping des champs pour chaque objet :

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

Regles de mapping des champs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``<nom_objet>.title`` - Champ a utiliser pour le titre (champ unique)
- ``<nom_objet>.contents`` - Champs a utiliser pour le contenu (plusieurs separes par des virgules)

Exemples d'utilisation
======

Crawl des objets standard
--------------------------

Parametres :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

Script :

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl des objets personnalises
------------------------------

Parametres :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

Script :

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl d'un environnement Sandbox
---------------------

Parametres :

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

Script :

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

Depannage
======================

Erreur d'authentification
----------

**Symptome** : ``Authentication failed`` ou ``invalid_grant``

**Points a verifier** :

1. Pour l'authentification OAuth Token :

   - Verifier si la Consumer Key est correcte
   - Verifier si la cle privee est correctement copiee (sauts de ligne en ``\n``)
   - Verifier si le certificat a ete telecharge sur Salesforce
   - Verifier si le nom d'utilisateur est correct

2. Pour l'authentification OAuth Password :

   - Verifier si la Consumer Key et le Consumer Secret sont corrects
   - Verifier si le token de securite est correct
   - Verifier que le mot de passe et le token de securite ne sont pas concatenes (configurer separement)

3. Commun :

   - Verifier si base_url est correct (environnement de production ou Sandbox)
   - Verifier si l'application connectee est autorisee

Impossible de recuperer les objets
--------------------------

**Symptome** : Le crawl reussit mais 0 objets

**Points a verifier** :

1. Verifier si l'utilisateur a les droits de lecture sur l'objet
2. Pour les objets personnalises, verifier si le nom de l'objet est correct (nom de reference API)
3. Verifier si le mapping des champs est correct
4. Verifier les messages d'erreur dans les logs

Nom des objets personnalises
--------------------------

Verifier le nom de reference API de l'objet personnalise :

1. Ouvrez "Gestionnaire d'objets" dans Salesforce Setup
2. Selectionnez l'objet personnalise
3. Copiez le "Nom de l'API" (se termine generalement par ``__c``)

Exemple :

- Label d'affichage : Product
- Nom de l'API : Product__c (utilisez celui-ci)

Verification des noms de champs
------------------

Verifier le nom de reference API des champs personnalises :

1. Ouvrez "Champs et relations" de l'objet
2. Selectionnez le champ personnalise
3. Copiez le "Nom du champ" (se termine generalement par ``__c``)

Exemple :

- Label d'affichage du champ : Product Description
- Nom du champ : Product_Description__c (utilisez celui-ci)

Limitation de debit API
-------------

**Symptome** : ``REQUEST_LIMIT_EXCEEDED``

**Solution** :

1. Reduire ``number_of_threads`` (definir a 1)
2. Augmenter l'intervalle de crawl
3. Verifier l'utilisation de l'API Salesforce
4. Acheter des limites API supplementaires si necessaire

Cas de nombreuses donnees
----------------------

**Symptome** : Le crawl prend du temps ou expire

**Solution** :

1. Diviser les objets en plusieurs data stores
2. Ajuster ``number_of_threads`` (environ 2-4)
3. Repartir le calendrier de crawl
4. Mapper uniquement les champs necessaires

Erreur de format de cle privee
--------------------------

**Symptome** : ``Invalid private key format``

**Solution** :

Verifier si les sauts de ligne de la cle privee sont correctement en ``\n`` :

::

    # Format correct
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Format incorrect (contient des sauts de ligne reels)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
