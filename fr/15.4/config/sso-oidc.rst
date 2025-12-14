====================================
Configuration SSO avec OpenID Connect
====================================

Vue d'ensemble
==============

|Fess| prend en charge l'authentification Single Sign-On (SSO) utilisant OpenID Connect (OIDC).
OpenID Connect est un protocole d'authentification basé sur OAuth 2.0 qui utilise des ID Tokens (JWT) pour l'authentification des utilisateurs.
En utilisant l'authentification OpenID Connect, les informations utilisateur authentifiées par un OpenID Provider (OP) peuvent être intégrées avec |Fess|.

Fonctionnement de l'authentification OpenID Connect
----------------------------------------------------

Dans l'authentification OpenID Connect, |Fess| fonctionne comme une Relying Party (RP) et collabore avec un OpenID Provider (OP) externe pour l'authentification.

1. L'utilisateur accède au endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige vers le endpoint d'autorisation de l'OP
3. L'utilisateur s'authentifie auprès de l'OP
4. L'OP redirige le code d'autorisation vers |Fess|
5. |Fess| utilise le code d'autorisation pour obtenir un ID Token depuis le endpoint de token
6. |Fess| valide l'ID Token (JWT) et connecte l'utilisateur

Pour l'intégration avec la recherche basée sur les rôles, voir :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification OpenID Connect, vérifiez les prérequis suivants :

- |Fess| 15.4 ou supérieur est installé
- Un fournisseur compatible OpenID Connect (OP) est disponible
- |Fess| est accessible via HTTPS (requis pour les environnements de production)
- Vous avez la permission d'enregistrer |Fess| comme client (RP) côté OP

Exemples de fournisseurs pris en charge :

- Microsoft Entra ID (Azure AD)
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- Autres fournisseurs compatibles OpenID Connect

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification OpenID Connect, ajoutez le paramètre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=oic

Configuration du fournisseur
----------------------------

Configurez les informations obtenues de votre OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.auth.server.url``
     - URL du endpoint d'autorisation
     - (Requis)
   * - ``oic.token.server.url``
     - URL du endpoint de token
     - (Requis)

.. note::
   Ces URLs peuvent être obtenues depuis le endpoint Discovery de l'OP (``/.well-known/openid-configuration``).

Configuration du client
-----------------------

Configurez les informations client enregistrées auprès de l'OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.client.id``
     - ID client
     - (Requis)
   * - ``oic.client.secret``
     - Secret client
     - (Requis)
   * - ``oic.scope``
     - Scopes demandés
     - (Requis)

.. note::
   Le scope doit inclure au moins ``openid``.
   Pour récupérer l'adresse e-mail de l'utilisateur, spécifiez ``openid email``.

Configuration de l'URL de redirection
-------------------------------------

Configurez l'URL de callback après l'authentification.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.redirect.url``
     - URL de redirection (URL de callback)
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - URL de base de |Fess|
     - ``http://localhost:8080``

.. note::
   Si ``oic.redirect.url`` est omis, il est automatiquement construit à partir de ``oic.base.url``.
   Pour les environnements de production, définissez ``oic.base.url`` sur une URL HTTPS.

Configuration côté OP
=====================

Lors de l'enregistrement de |Fess| comme client (RP) côté OP, configurez les informations suivantes :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Valeur
   * - Type d'application
     - Application web
   * - URI de redirection / URL de callback
     - ``https://<Hôte Fess>/sso/``
   * - Scopes autorisés
     - ``openid`` et les scopes requis (``email``, ``profile``, etc.)

Informations à obtenir de l'OP
------------------------------

Obtenez les informations suivantes depuis l'écran de configuration ou le endpoint Discovery de l'OP pour la configuration de |Fess| :

- **Endpoint d'autorisation (Authorization Endpoint)** : URL pour initier l'authentification utilisateur
- **Endpoint de token (Token Endpoint)** : URL pour obtenir les tokens
- **ID client** : Identifiant client émis par l'OP
- **Secret client** : Clé secrète utilisée pour l'authentification du client

.. note::
   La plupart des OP vous permettent de vérifier les URLs des endpoints d'autorisation et de token depuis le
   endpoint Discovery (``https://<OP>/.well-known/openid-configuration``).

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour la vérification dans un environnement de test.

::

    # Activer SSO
    sso.type=oic

    # Configuration du fournisseur (définir les valeurs obtenues de l'OP)
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Configuration du client
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # URL de redirection (environnement de test)
    oic.redirect.url=http://localhost:8080/sso/

Configuration recommandée (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandée pour les environnements de production.

::

    # Activer SSO
    sso.type=oic

    # Configuration du fournisseur
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Configuration du client
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # URL de base (utiliser HTTPS pour la production)
    oic.base.url=https://fess.example.com

Dépannage
=========

Problèmes courants et solutions
-------------------------------

Impossible de retourner à Fess après l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'URI de redirection est correctement configurée côté OP
- Assurez-vous que la valeur de ``oic.redirect.url`` ou ``oic.base.url`` correspond à la configuration de l'OP
- Vérifiez que le protocole (HTTP/HTTPS) correspond

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'ID client et le secret client sont correctement configurés
- Assurez-vous que le scope inclut ``openid``
- Vérifiez que l'URL du endpoint d'autorisation et l'URL du endpoint de token sont correctes

Impossible de récupérer les informations utilisateur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Assurez-vous que le scope inclut les permissions requises (``email``, ``profile``, etc.)
- Vérifiez que les scopes requis sont autorisés pour le client côté OP

Configuration de débogage
-------------------------

Pour investiguer les problèmes, vous pouvez afficher des logs détaillés liés à OpenID Connect en ajustant le niveau de log de |Fess|.

Dans ``app/WEB-INF/classes/log4j2.xml``, vous pouvez ajouter le logger suivant pour changer le niveau de log :

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
