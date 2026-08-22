==================================
Connecteur Salesforce
==================================

Aperçu
====

Le connecteur Salesforce fournit la fonctionnalité permettant de récupérer des données
depuis les objets Salesforce (objets standard, objets personnalisés) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-salesforce``.

Objets pris en charge
================

- **Objets standard** : objets standard prédéfinis (Account, Contact, Lead, Opportunity, Case, Solution, etc.). L'ensemble des objets standard est fixe et la totalité d'entre eux est récupérée à chaque crawl.
- **Objets personnalisés** : objets définis par l'utilisateur, spécifiés via le paramètre ``custom`` (objets dont le nom API se termine par ``__c``).

.. note::

   Les objets standard sont toujours crawlés intégralement (il n'est pas possible de sélectionner individuellement les objets standard à crawler). Pour exclure des objets indésirables, utilisez le filtrage par URL via ``include_pattern`` / ``exclude_pattern``.

Liste des objets standard
-------------------------

Les objets standard suivants sont crawlés. La colonne "Nom de l'objet" est l'identifiant utilisé dans le mapping des champs (par exemple ``<NomObjet>.title``) ; ``object.type`` est la valeur du type d'objet que vous pouvez référencer dans les scripts.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Nom de l'objet
     - ``object.type``
     - Description
   * - ``ACCOUNT``
     - ``Account``
     - Account
   * - ``CONTACT``
     - ``Contact``
     - Contact
   * - ``LEAD``
     - ``Lead``
     - Lead
   * - ``OPPORTUNITY``
     - ``Opportunity``
     - Opportunity
   * - ``CASE``
     - ``Case``
     - Case
   * - ``SOLUTION``
     - ``Solution``
     - Solution
   * - ``CONTRACT``
     - ``Contract``
     - Contract
   * - ``ORDER``
     - ``Order``
     - Order
   * - ``CAMPAIGN``
     - ``Campaign``
     - Campaign
   * - ``PRODUCT2``
     - ``Product2``
     - Product
   * - ``PRICEBOOK2``
     - ``Pricebook2``
     - Price Book
   * - ``ASSET``
     - ``Asset``
     - Asset
   * - ``ASSET_RELATIONSHIP``
     - ``AssetRelationship``
     - Asset Relationship
   * - ``TASK``
     - ``Task``
     - Task
   * - ``USER``
     - ``User``
     - User
   * - ``COLLABORATION_GROUP``
     - ``CollaborationGroup``
     - Chatter Group
   * - ``IDEA``
     - ``Idea``
     - Idea
   * - ``RECOMMENDATION``
     - ``Recommendation``
     - Recommendation
   * - ``QUICK_TEXT``
     - ``QuickText``
     - Quick Text
   * - ``MACRO``
     - ``Macro``
     - Macro
   * - ``LIST_EMAIL``
     - ``ListEmail``
     - List Email
   * - ``IMAGE``
     - ``Image``
     - Image
   * - ``DAND_B_COMPANY``
     - ``DandBCompany``
     - D&B Company

Prérequis
========

1. L'installation du plugin est requise
2. La création d'une application connectée (Connected App) Salesforce est nécessaire
3. La configuration de l'authentification OAuth est nécessaire
4. L'accès en lecture aux objets est requis

Installation du plugin
------------------------

Installez depuis l'interface d'administration via "Système" -> "Plugins".

Ou consultez :doc:`../../admin/plugin-guide` pour plus de détails.

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
     - Salesforce CRM
   * - Nom du gestionnaire
     - SalesforceDataStore
   * - Active
     - Oui

Configuration des paramètres
----------------

Authentification OAuth Token (recommandée) :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignore_error=true
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
    password=YourPassword
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignore_error=true

Liste des paramètres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``base_url``
     - Non
     - URL Salesforce (par défaut : ``https://login.salesforce.com``, Sandbox : ``https://test.salesforce.com``)
   * - ``auth_type``
     - Oui
     - Type d'authentification (``oauth_token`` ou ``oauth_password``)
   * - ``username``
     - Oui
     - Nom d'utilisateur Salesforce
   * - ``password``
     - Pour oauth_password
     - Mot de passe Salesforce
   * - ``client_id``
     - Oui
     - Consumer Key de l'application connectée
   * - ``private_key``
     - Pour oauth_token
     - Clé privée (format PEM, sauts de ligne en ``\n``)
   * - ``client_secret``
     - Pour oauth_password
     - Consumer Secret de l'application connectée
   * - ``security_token``
     - Pour oauth_password
     - Token de sécurité de l'utilisateur
   * - ``number_of_threads``
     - Non
     - Nombre de threads de traitement parallèle (par défaut : 1)
   * - ``ignore_error``
     - Non
     - Continuer le traitement en cas d'erreur (par défaut : true)
   * - ``custom``
     - Non
     - Noms des objets personnalisés (séparés par des virgules)
   * - ``<objet>.title``
     - Non
     - Nom du champ à utiliser pour le titre
   * - ``<objet>.contents``
     - Non
     - Noms des champs à utiliser pour le contenu (séparés par des virgules)
   * - ``<objet>.descriptions``
     - Non
     - Noms de champs pour la description (séparés par des virgules)
   * - ``<objet>.thumbnail``
     - Non
     - Nom du champ pour la miniature
   * - ``include_pattern``
     - Non
     - Modèle d'inclusion du filtre URL (regex)
   * - ``exclude_pattern``
     - Non
     - Modèle d'exclusion du filtre URL (regex)
   * - ``refresh_token_interval``
     - Non
     - Intervalle d'actualisation du jeton en secondes (par défaut : 3540)
   * - ``proxy_host``
     - Non
     - Nom d'hôte du proxy HTTP
   * - ``proxy_port``
     - Si proxy_host est défini
     - Numéro de port du proxy HTTP

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
     - Date de création
   * - ``object.last_modified``
     - Date de dernière modification
   * - ``object.url``
     - URL de l'objet
   * - ``object.thumbnail``
     - URL de la miniature

Configuration de l'application connectée Salesforce
====================================

1. Création de l'application connectée
-----------------------------

Dans Salesforce Setup :

1. Ouvrez "Gestionnaire d'applications"
2. Cliquez sur "Nouvelle application connectée"
3. Entrez les informations de base :

   - Nom de l'application connectée : Fess Crawler
   - Nom de l'API : Fess_Crawler
   - Email de contact : your-email@example.com

4. Cochez "Activer les paramètres OAuth (Activer OAuth)"

2. Configuration de l'authentification OAuth Token (recommandée)
--------------------------------

Dans les paramètres OAuth :

1. Cochez "Utiliser les signatures numériques"
2. Téléchargez un certificat (créé selon les étapes ci-dessous)
3. Scopes OAuth sélectionnés :

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. Cliquez sur "Enregistrer"
5. Copiez la Consumer Key

Création du certificat :

::

    # Generation de la cle privee
    openssl genrsa -out private_key.pem 2048

    # Generation du certificat
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # Verification de la cle privee
    cat private_key.pem

Téléchargez le certificat (certificate.crt) sur Salesforce et
configurez le contenu de la clé privée (private_key.pem) dans les paramètres.

3. Configuration de l'authentification OAuth Password
---------------------------

Dans les paramètres OAuth :

1. URL de callback : ``https://localhost`` (non utilisée mais requise)
2. Scopes OAuth sélectionnés :

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. Cliquez sur "Enregistrer"
4. Copiez la Consumer Key et le Consumer Secret

Obtention du token de sécurité :

1. Ouvrez les paramètres personnels dans Salesforce
2. Cliquez sur "Réinitialiser mon token de sécurité"
3. Copiez le token envoyé par email

4. Autorisation de l'application connectée
-----------------------------

Dans "Administration" -> "Gérer les applications connectées" :

1. Sélectionnez l'application connectée créée
2. Cliquez sur "Modifier"
3. Changez "Utilisateurs autorisés" en "Les utilisateurs approuvés par l'administrateur sont préautorisés"
4. Attribuez des profils ou des ensembles de permissions

Configuration des objets personnalisés
==========================

Crawl des objets personnalisés
------------------------------

Spécifiez les noms des objets personnalisés avec le paramètre ``custom`` :

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

Règles de mapping des champs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``<nom_objet>.title`` - Champ à utiliser pour le titre (champ unique)
- ``<nom_objet>.contents`` - Champs à utiliser pour le contenu (plusieurs séparés par des virgules)
- ``<nom_objet>.descriptions`` - Champs à utiliser pour la description (plusieurs séparés par des virgules)
- ``<nom_objet>.thumbnail`` - Champ à utiliser pour la miniature (champ unique)

.. note::

   Pour le mapping des champs des objets standard, le nom de l'objet utilise la notation UPPER_SNAKE_CASE
   (la valeur de la colonne "Nom de l'objet" dans la section `Liste des objets standard`_)
   (ex. : ``ACCOUNT.title=Name``, ``DAND_B_COMPANY.title=Name``).
   Pour les objets personnalisés, le nom de référence API est utilisé tel quel (ex. : ``Product__c.title=Name``).

Exemples d'utilisation
======

Crawl des objets standard
--------------------------

Paramètres :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignore_error=true

Script :

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl des objets personnalisés
------------------------------

Paramètres :

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignore_error=true
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

Paramètres :

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    password=YourPassword
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignore_error=true

Script :

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

Dépannage
======================

Erreur d'authentification
----------

**Symptôme** : ``Authentication failed`` ou ``invalid_grant``

**Points à vérifier** :

1. Pour l'authentification OAuth Token :

   - Vérifier si la Consumer Key est correcte
   - Vérifier si la clé privée est correctement copiée (sauts de ligne en ``\n``)
   - Vérifier si le certificat a été téléchargé sur Salesforce
   - Vérifier si le nom d'utilisateur est correct

2. Pour l'authentification OAuth Password :

   - Vérifier si la Consumer Key et le Consumer Secret sont corrects
   - Vérifier si le token de sécurité est correct
   - Vérifier que le mot de passe et le token de sécurité ne sont pas concaténés (configurer séparément)

3. Commun :

   - Vérifier si base_url est correct (environnement de production ou Sandbox)
   - Vérifier si l'application connectée est autorisée

Impossible de récupérer les objets
--------------------------

**Symptôme** : Le crawl réussit mais 0 objets

**Points à vérifier** :

1. Vérifier si l'utilisateur a les droits de lecture sur l'objet
2. Pour les objets personnalisés, vérifier si le nom de l'objet est correct (nom de référence API)
3. Vérifier si le mapping des champs est correct
4. Vérifier les messages d'erreur dans les logs

Nom des objets personnalisés
--------------------------

Vérifier le nom de référence API de l'objet personnalisé :

1. Ouvrez "Gestionnaire d'objets" dans Salesforce Setup
2. Sélectionnez l'objet personnalisé
3. Copiez le "Nom de l'API" (se termine généralement par ``__c``)

Exemple :

- Label d'affichage : Product
- Nom de l'API : Product__c (utilisez celui-ci)

Vérification des noms de champs
------------------

Vérifier le nom de référence API des champs personnalisés :

1. Ouvrez "Champs et relations" de l'objet
2. Sélectionnez le champ personnalisé
3. Copiez le "Nom du champ" (se termine généralement par ``__c``)

Exemple :

- Label d'affichage du champ : Product Description
- Nom du champ : Product_Description__c (utilisez celui-ci)

Limitation de débit API
-------------

**Symptôme** : ``REQUEST_LIMIT_EXCEEDED``

**Solution** :

1. Réduire ``number_of_threads`` (définir à 1)
2. Augmenter l'intervalle de crawl
3. Vérifier l'utilisation de l'API Salesforce
4. Acheter des limites API supplémentaires si nécessaire

Cas de nombreuses données
----------------------

**Symptôme** : Le crawl prend du temps ou expire

**Solution** :

1. Diviser les objets en plusieurs data stores
2. Ajuster ``number_of_threads`` (environ 2-4)
3. Répartir le calendrier de crawl
4. Mapper uniquement les champs nécessaires

Erreur de format de clé privée
--------------------------

**Symptôme** : ``Invalid private key format``

**Solution** :

Vérifier si les sauts de ligne de la clé privée sont correctement en ``\n`` :

::

    # Format correct
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Format incorrect (contient des sauts de ligne reels)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Informations de référence
========

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de données
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
