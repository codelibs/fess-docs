==================================
Connecteur Atlassian
==================================

Aperçu
======

Le connecteur Atlassian fournit une fonctionnalité pour récupérer des données depuis les produits Atlassian (Jira, Confluence) et les enregistrer dans l'index de |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-atlassian``.

Produits pris en charge
=======================

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

Prérequis
=========

1. L'installation du plugin est requise
2. Les informations d'authentification appropriées pour les produits Atlassian sont nécessaires
3. Pour la version Cloud, OAuth 2.0 est disponible ; pour la version Server, OAuth 1.0a ou l'authentification basique sont disponibles

Installation du plugin
----------------------

Installez depuis l'interface d'administration sous "Système" -> "Plugins" :

1. Téléchargez ``fess-ds-atlassian-X.X.X.jar`` depuis Maven Central
2. Uploadez et installez depuis l'interface de gestion des plugins
3. Redémarrez |Fess|

Méthode de configuration
========================

Configurez depuis l'interface d'administration : "Crawler" -> "DataStore" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple de configuration
   * - Nom
     - Company Jira/Confluence
   * - Nom du handler
     - JiraDataStore ou ConfluenceDataStore
   * - Actif
     - Oui

Configuration des paramètres
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
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``home``
     - Oui
     - URL de l'instance Atlassian
   * - ``is_cloud``
     - Non
     - ``true`` pour la version Cloud, ``false`` pour la version Server (défaut : ``true``). Utilisé uniquement pour la sélection du point de terminaison lors de l'authentification OAuth 2.0 ; ignoré pour les authentifications basique et OAuth 1.0a.
   * - ``auth_type``
     - Oui
     - Type d'authentification : ``oauth``, ``oauth2``, ``basic``
   * - ``oauth.consumer_key``
     - Pour OAuth 1.0a
     - Clé consommateur (généralement ``OauthKey``)
   * - ``oauth.private_key``
     - Pour OAuth 1.0a
     - Clé privée RSA (format PEM)
   * - ``oauth.secret``
     - Pour OAuth 1.0a
     - Code de vérification
   * - ``oauth.access_token``
     - Pour OAuth 1.0a
     - Token d'accès
   * - ``oauth2.client_id``
     - Pour OAuth 2.0
     - ID client
   * - ``oauth2.client_secret``
     - Pour OAuth 2.0
     - Secret client
   * - ``oauth2.access_token``
     - Pour OAuth 2.0
     - Token d'accès
   * - ``oauth2.refresh_token``
     - Non
     - Token de rafraîchissement (OAuth 2.0)
   * - ``oauth2.token_url``
     - Non
     - URL du token (OAuth 2.0, défaut : ``https://auth.atlassian.com/oauth/token``)
   * - ``basic.username``
     - Pour auth basique
     - Nom d'utilisateur
   * - ``basic.password``
     - Pour auth basique
     - Mot de passe
   * - ``issue.jql``
     - Non
     - JQL (Jira uniquement, conditions de recherche avancées). Si non spécifié, tous les tickets (``created is not empty``) sont ciblés.
   * - ``issue_max_results``
     - Non
     - Nombre maximum de résultats par requête API Jira (défaut : ``50``, Jira uniquement)
   * - ``content_limit``
     - Non
     - Nombre maximum d'éléments par requête API Confluence (défaut : ``25``, Confluence uniquement)
   * - ``ignore_error``
     - Non
     - Continuer le traitement en cas d'erreur (défaut : ``true``)
   * - ``include_pattern``
     - Non
     - Modèle d'inclusion d'URL (regex)
   * - ``exclude_pattern``
     - Non
     - Modèle d'exclusion d'URL (regex)
   * - ``number_of_threads``
     - Non
     - Nombre de threads pour le traitement parallèle (défaut : ``1``)
   * - ``proxy_host``
     - Non
     - Nom d'hôte du proxy HTTP
   * - ``proxy_port``
     - Non
     - Numéro de port du proxy HTTP
   * - ``connection_timeout``
     - Non
     - Délai de connexion HTTP (millisecondes)
   * - ``read_timeout``
     - Non
     - Délai de lecture HTTP (millisecondes)
   * - ``readInterval``
     - Non
     - Intervalle entre le traitement de chaque document (en millisecondes, défaut : ``0``)

Configuration du script
-----------------------

Pour Jira
~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

Champs disponibles :

- ``issue.view_url`` - URL du ticket
- ``issue.summary`` - Résumé du ticket
- ``issue.description`` - Description du ticket
- ``issue.comments`` - Commentaires du ticket
- ``issue.last_modified`` - Date de dernière modification

Pour Confluence
~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

Champs disponibles :

- ``content.view_url`` - URL de la page
- ``content.title`` - Titre de la page
- ``content.body`` - Corps de la page
- ``content.comments`` - Commentaires de la page
- ``content.last_modified`` - Date de dernière modification

.. note::
   Le connecteur Confluence récupère à la fois les pages normales (page) et les articles de blog (blogpost).

Configuration de l'authentification OAuth 2.0
=============================================

Pour la version Cloud (recommandé)
----------------------------------

1. Créez une application dans Atlassian Developer Console
2. Obtenez les informations d'authentification OAuth 2.0
3. Configurez les scopes nécessaires :

   - Jira : ``read:jira-work``, ``read:jira-user``
   - Confluence : ``read:confluence-content.all``, ``read:confluence-user``

4. Obtenez le token d'accès et le token de rafraîchissement

Configuration de l'authentification OAuth 1.0a
==============================================

Pour la version Server
----------------------

1. Créez un Application Link dans Jira ou Confluence
2. Générez une paire de clés RSA :

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. Enregistrez la clé publique dans l'Application Link
4. Configurez la clé privée dans les paramètres

Configuration de l'authentification basique
===========================================

Configuration simple pour la version Server
-------------------------------------------

.. warning::
   L'authentification basique n'est pas recommandée pour des raisons de sécurité. Utilisez l'authentification OAuth autant que possible.

Pour utiliser l'authentification basique :

1. Préparez un compte utilisateur avec des privilèges d'administration
2. Configurez le nom d'utilisateur et le mot de passe dans les paramètres
3. Utilisez HTTPS pour assurer une connexion sécurisée

Recherche avancée avec JQL
==========================

Filtrer les tickets Jira avec JQL
---------------------------------

Explorer uniquement les tickets correspondant à des conditions spécifiques :

::

    # Projet specifique uniquement
    issue.jql=project = "MYPROJECT"

    # Exclure certains statuts
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # Specifier une periode
    issue.jql=updated >= -30d

    # Combinaison de conditions multiples
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

Pour plus de détails sur JQL, consultez la `documentation JQL Atlassian <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Exemples d'utilisation
======================

Exploration de Jira Cloud
-------------------------

Paramètres :

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
    title=issue.summary
    content=issue.description + "\n\nCommentaires:\n" + issue.comments
    last_modified=issue.last_modified

Exploration de Confluence Server
--------------------------------

Paramètres :

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
    content=content.body + "\n\nCommentaires:\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

Dépannage
=========

Erreur d'authentification
-------------------------

**Symptôme** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points à vérifier** :

1. Vérifiez que les informations d'authentification sont correctes
2. Pour la version Cloud, vérifiez que les scopes appropriés sont configurés
3. Pour la version Server, vérifiez que l'utilisateur dispose des autorisations appropriées
4. Pour OAuth 2.0, vérifiez la date d'expiration du token

Erreur de connexion
-------------------

**Symptôme** : ``Connection refused`` ou timeout de connexion

**Points à vérifier** :

1. Vérifiez que l'URL ``home`` est correcte
2. Vérifiez les paramètres du pare-feu
3. Vérifiez que l'instance Atlassian est en cours d'exécution
4. Vérifiez que le paramètre ``is_cloud`` est correctement configuré

Impossible de récupérer les données
-----------------------------------

**Symptôme** : L'exploration réussit mais 0 document

**Points à vérifier** :

1. Vérifiez que le JQL n'est pas trop restrictif
2. Vérifiez que l'utilisateur a des droits de lecture sur les projets/espaces
3. Vérifiez la configuration du script
4. Vérifiez les erreurs dans les logs

Rafraîchissement du token OAuth 2.0
-----------------------------------

**Symptôme** : Des erreurs d'authentification se produisent après un certain temps

**Solution** :

Les tokens d'accès OAuth 2.0 ont une date d'expiration. Configurez le token de rafraîchissement pour permettre le renouvellement automatique :

::

    oauth2.refresh_token=your_refresh_token

Lors du renouvellement des tokens, le nouveau token d'accès et le nouveau token de rafraîchissement sont automatiquement enregistrés dans la configuration du data store, de sorte que les explorations suivantes utilisent les tokens mis à jour (aucune mise à jour manuelle n'est nécessaire).

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs DataStore
- :doc:`ds-database` - Connecteur base de données
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- `Atlassian Developer <https://developer.atlassian.com/>`_
