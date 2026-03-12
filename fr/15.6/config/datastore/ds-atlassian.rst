==================================
Connecteur Atlassian
==================================

Apercu
======

Le connecteur Atlassian fournit une fonctionnalite pour recuperer des donnees depuis les produits Atlassian (Jira, Confluence) et les enregistrer dans l'index de |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-atlassian``.

Produits pris en charge
=======================

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

Prerequis
=========

1. L'installation du plugin est requise
2. Les informations d'authentification appropriees pour les produits Atlassian sont necessaires
3. Pour la version Cloud, OAuth 2.0 est disponible ; pour la version Server, OAuth 1.0a ou l'authentification basique sont disponibles

Installation du plugin
----------------------

Installez depuis l'interface d'administration sous "Systeme" -> "Plugins" :

1. Telechargez ``fess-ds-atlassian-X.X.X.jar`` depuis Maven Central
2. Uploadez et installez depuis l'interface de gestion des plugins
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
     - Company Jira/Confluence
   * - Nom du handler
     - JiraDataStore ou ConfluenceDataStore
   * - Actif
     - Oui

Configuration des parametres
----------------------------

Exemple version Cloud (OAuth 2.0) :

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Exemple version Server (authentification basique) :

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Exemple version Server (OAuth 1.0a) :

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\\nMIIE...=\\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

Liste des parametres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``home``
     - Oui
     - URL de l'instance Atlassian
   * - ``is_cloud``
     - Oui
     - ``true`` pour la version Cloud, ``false`` pour la version Server
   * - ``auth_type``
     - Oui
     - Type d'authentification : ``oauth``, ``oauth2``, ``basic``
   * - ``oauth.consumer_key``
     - Pour OAuth 1.0a
     - Cle consommateur (generalement ``OauthKey``)
   * - ``oauth.private_key``
     - Pour OAuth 1.0a
     - Cle privee RSA (format PEM)
   * - ``oauth.secret``
     - Pour OAuth 1.0a
     - Code de verification
   * - ``oauth.access_token``
     - Pour OAuth 1.0a
     - Token d'acces
   * - ``oauth2.client_id``
     - Pour OAuth 2.0
     - ID client
   * - ``oauth2.client_secret``
     - Pour OAuth 2.0
     - Secret client
   * - ``oauth2.access_token``
     - Pour OAuth 2.0
     - Token d'acces
   * - ``oauth2.refresh_token``
     - Non
     - Token de rafraichissement (OAuth 2.0)
   * - ``oauth2.token_url``
     - Non
     - URL du token (OAuth 2.0, valeur par defaut disponible)
   * - ``basic.username``
     - Pour auth basique
     - Nom d'utilisateur
   * - ``basic.password``
     - Pour auth basique
     - Mot de passe
   * - ``issue.jql``
     - Non
     - JQL (Jira uniquement, conditions de recherche avancees)

Configuration du script
-----------------------

Pour Jira
~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\\n\\n" + issue.comments
    last_modified=issue.last_modified

Champs disponibles :

- ``issue.view_url`` - URL du ticket
- ``issue.summary`` - Resume du ticket
- ``issue.description`` - Description du ticket
- ``issue.comments`` - Commentaires du ticket
- ``issue.last_modified`` - Date de derniere modification

Pour Confluence
~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\\n\\n" + content.comments
    last_modified=content.last_modified

Champs disponibles :

- ``content.view_url`` - URL de la page
- ``content.title`` - Titre de la page
- ``content.body`` - Corps de la page
- ``content.comments`` - Commentaires de la page
- ``content.last_modified`` - Date de derniere modification

Configuration de l'authentification OAuth 2.0
=============================================

Pour la version Cloud (recommande)
----------------------------------

1. Creez une application dans Atlassian Developer Console
2. Obtenez les informations d'authentification OAuth 2.0
3. Configurez les scopes necessaires :

   - Jira : ``read:jira-work``, ``read:jira-user``
   - Confluence : ``read:confluence-content.all``, ``read:confluence-user``

4. Obtenez le token d'acces et le token de rafraichissement

Configuration de l'authentification OAuth 1.0a
==============================================

Pour la version Server
----------------------

1. Creez un Application Link dans Jira ou Confluence
2. Generez une paire de cles RSA :

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. Enregistrez la cle publique dans l'Application Link
4. Configurez la cle privee dans les parametres

Configuration de l'authentification basique
===========================================

Configuration simple pour la version Server
-------------------------------------------

.. warning::
   L'authentification basique n'est pas recommandee pour des raisons de securite. Utilisez l'authentification OAuth autant que possible.

Pour utiliser l'authentification basique :

1. Preparez un compte utilisateur avec des privileges d'administration
2. Configurez le nom d'utilisateur et le mot de passe dans les parametres
3. Utilisez HTTPS pour assurer une connexion securisee

Recherche avancee avec JQL
==========================

Filtrer les tickets Jira avec JQL
---------------------------------

Explorer uniquement les tickets correspondant a des conditions specifiques :

::

    # Projet specifique uniquement
    issue.jql=project = "MYPROJECT"

    # Exclure certains statuts
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # Specifier une periode
    issue.jql=updated >= -30d

    # Combinaison de conditions multiples
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

Pour plus de details sur JQL, consultez la `documentation JQL Atlassian <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Exemples d'utilisation
======================

Exploration de Jira Cloud
-------------------------

Parametres :

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

Script :

::

    url=issue.view_url
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\\n\\nCommentaires:\\n" + issue.comments
    last_modified=issue.last_modified

Exploration de Confluence Server
--------------------------------

Parametres :

::

    home=https://wiki.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

Script :

::

    url=content.view_url
    title=content.title
    content=content.body + "\\n\\nCommentaires:\\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

Depannage
=========

Erreur d'authentification
-------------------------

**Symptome** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points a verifier** :

1. Verifiez que les informations d'authentification sont correctes
2. Pour la version Cloud, verifiez que les scopes appropries sont configures
3. Pour la version Server, verifiez que l'utilisateur dispose des autorisations appropriees
4. Pour OAuth 2.0, verifiez la date d'expiration du token

Erreur de connexion
-------------------

**Symptome** : ``Connection refused`` ou timeout de connexion

**Points a verifier** :

1. Verifiez que l'URL ``home`` est correcte
2. Verifiez les parametres du pare-feu
3. Verifiez que l'instance Atlassian est en cours d'execution
4. Verifiez que le parametre ``is_cloud`` est correctement configure

Impossible de recuperer les donnees
-----------------------------------

**Symptome** : L'exploration reussit mais 0 document

**Points a verifier** :

1. Verifiez que le JQL n'est pas trop restrictif
2. Verifiez que l'utilisateur a des droits de lecture sur les projets/espaces
3. Verifiez la configuration du script
4. Verifiez les erreurs dans les logs

Rafraichissement du token OAuth 2.0
-----------------------------------

**Symptome** : Des erreurs d'authentification se produisent apres un certain temps

**Solution** :

Les tokens d'acces OAuth 2.0 ont une date d'expiration. Configurez le token de rafraichissement pour permettre le renouvellement automatique :

::

    oauth2.refresh_token=your_refresh_token

Informations de reference
=========================

- :doc:`ds-overview` - Apercu des connecteurs DataStore
- :doc:`ds-database` - Connecteur base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Atlassian Developer <https://developer.atlassian.com/>`_
