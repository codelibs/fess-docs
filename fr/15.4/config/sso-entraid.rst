=======================================
Configuration SSO avec Entra ID
=======================================

Aperçu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) en utilisant Microsoft Entra ID (anciennement Azure AD).
En utilisant l'authentification Entra ID, vous pouvez intégrer les informations utilisateur et les informations de groupe de votre environnement Microsoft 365 avec la recherche basée sur les rôles de |Fess|.

Fonctionnement de l'authentification Entra ID
---------------------------------------------

Dans l'authentification Entra ID, |Fess| opère en tant que client OAuth 2.0/OpenID Connect et collabore avec Microsoft Entra ID pour l'authentification.

1. L'utilisateur accède au point de terminaison SSO de |Fess| (``/sso/``)
2. |Fess| redirige vers le point de terminaison d'autorisation d'Entra ID
3. L'utilisateur s'authentifie auprès d'Entra ID (connexion Microsoft)
4. Entra ID redirige le code d'autorisation vers |Fess|
5. |Fess| utilise le code d'autorisation pour obtenir un jeton d'accès
6. |Fess| utilise l'API Microsoft Graph pour récupérer les informations de groupe et de rôle de l'utilisateur
7. L'utilisateur est connecté et les informations de groupe sont appliquées à la recherche basée sur les rôles

Pour l'intégration avec la recherche basée sur les rôles, consultez :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification Entra ID, vérifiez les prérequis suivants :

- |Fess| 15.4 ou supérieur est installé
- Un tenant Microsoft Entra ID (Azure AD) est disponible
- |Fess| est accessible via HTTPS (requis pour les environnements de production)
- Vous avez la permission d'enregistrer des applications dans Entra ID

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification Entra ID, ajoutez le paramètre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=entraid

Paramètres requis
-----------------

Configurez les informations obtenues d'Entra ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``entraid.tenant``
     - ID du tenant (ex: ``xxx.onmicrosoft.com``)
     - (Requis)
   * - ``entraid.client.id``
     - ID d'application (Client)
     - (Requis)
   * - ``entraid.client.secret``
     - Valeur du secret client
     - (Requis)
   * - ``entraid.reply.url``
     - URI de redirection (URL de callback)
     - Utilise l'URL de la requête

.. note::
   Au lieu du préfixe ``entraid.*``, vous pouvez également utiliser le préfixe legacy ``aad.*`` pour la rétrocompatibilité.

Paramètres optionnels
---------------------

Les paramètres suivants peuvent être ajoutés si nécessaire.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``entraid.authority``
     - URL du serveur d'authentification
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - Durée de vie du state (secondes)
     - ``3600``
   * - ``entraid.default.groups``
     - Groupes par défaut (séparés par des virgules)
     - (Aucun)
   * - ``entraid.default.roles``
     - Rôles par défaut (séparés par des virgules)
     - (Aucun)

Configuration côté Entra ID
===========================

Enregistrement de l'application dans le portail Azure
-----------------------------------------------------

1. Connectez-vous au `Portail Azure <https://portal.azure.com/>`_

2. Sélectionnez **Microsoft Entra ID**

3. Allez dans **Gérer** → **Inscriptions d'applications** → **Nouvelle inscription**

4. Enregistrez l'application :

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Paramètre
        - Valeur
      * - Nom
        - Tout nom (ex: Fess SSO)
      * - Types de comptes pris en charge
        - "Comptes de cet annuaire d'organisation uniquement"
      * - Plateforme
        - Web
      * - URI de redirection
        - ``https://<hôte Fess>/sso/``

5. Cliquez sur **Inscrire**

Création d'un secret client
---------------------------

1. Sur la page de détails de l'application, cliquez sur **Certificats et secrets**

2. Cliquez sur **Nouveau secret client**

3. Définissez une description et une date d'expiration, puis cliquez sur **Ajouter**

4. Copiez et sauvegardez la **Valeur** générée (cette valeur ne sera plus affichée)

.. warning::
   La valeur du secret client n'est affichée qu'immédiatement après la création.
   Assurez-vous de l'enregistrer avant de quitter la page.

Configuration des autorisations d'API
-------------------------------------

1. Cliquez sur **Autorisations d'API** dans le menu de gauche

2. Cliquez sur **Ajouter une autorisation**

3. Sélectionnez **Microsoft Graph**

4. Sélectionnez **Autorisations déléguées**

5. Ajoutez l'autorisation suivante :

   - ``Group.Read.All`` - Requis pour récupérer les informations de groupe de l'utilisateur

6. Cliquez sur **Ajouter des autorisations**

7. Cliquez sur **Accorder le consentement administrateur pour <nom du tenant>**

.. note::
   Le consentement administrateur nécessite des privilèges d'administrateur de tenant.

Informations à obtenir
----------------------

Les informations suivantes sont utilisées pour la configuration de Fess :

- **ID d'application (Client)** : Sur la page Vue d'ensemble, sous "ID d'application (client)"
- **ID du tenant** : Sur la page Vue d'ensemble, sous "ID de répertoire (tenant)" ou au format ``xxx.onmicrosoft.com``
- **Valeur du secret client** : La valeur créée dans Certificats et secrets

Mappage des groupes et rôles
============================

Avec l'authentification Entra ID, |Fess| récupère automatiquement les groupes et rôles auxquels un utilisateur appartient en utilisant l'API Microsoft Graph.
Les ID de groupe et noms de groupe récupérés peuvent être utilisés pour la recherche basée sur les rôles de |Fess|.

Groupes imbriqués
-----------------

|Fess| récupère non seulement les groupes auxquels les utilisateurs appartiennent directement, mais aussi les groupes parents (groupes imbriqués) de manière récursive.
Ce traitement est exécuté de manière asynchrone après la connexion pour minimiser l'impact sur le temps de connexion.

Paramètres de groupe par défaut
-------------------------------

Pour attribuer des groupes communs à tous les utilisateurs Entra ID :

::

    entraid.default.groups=authenticated_users,entra_users

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour vérification dans un environnement de test.

::

    # Activer SSO
    sso.type=entraid

    # Paramètres Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Configuration recommandée (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandée pour les environnements de production.

::

    # Activer SSO
    sso.type=entraid

    # Paramètres Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Groupes par défaut (optionnel)
    entraid.default.groups=authenticated_users

Configuration legacy (rétrocompatibilité)
-----------------------------------------

Pour la compatibilité avec les versions antérieures, le préfixe ``aad.*`` peut également être utilisé.

::

    # Activer SSO
    sso.type=entraid

    # Clés de configuration legacy
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Dépannage
=========

Problèmes courants et solutions
-------------------------------

Impossible de revenir à Fess après l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'URI de redirection est correctement configurée dans l'inscription de l'application du portail Azure
- Assurez-vous que la valeur de ``entraid.reply.url`` correspond exactement à la configuration du portail Azure
- Vérifiez que le protocole (HTTP/HTTPS) correspond
- Vérifiez que l'URI de redirection se termine par ``/``

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'ID du tenant, l'ID client et le secret client sont correctement configurés
- Vérifiez que le secret client n'a pas expiré
- Vérifiez que le consentement administrateur a été accordé pour les autorisations d'API

Impossible de récupérer les informations de groupe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'autorisation ``Group.Read.All`` a été accordée
- Vérifiez que le consentement administrateur a été accordé
- Vérifiez que l'utilisateur appartient à des groupes dans Entra ID

Paramètres de débogage
----------------------

Pour investiguer les problèmes, vous pouvez afficher des logs détaillés liés à Entra ID en ajustant le niveau de log de |Fess|.

Dans ``app/WEB-INF/classes/log4j2.xml``, vous pouvez ajouter le logger suivant pour changer le niveau de log :

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-oidc` - Configuration SSO avec authentification OpenID Connect
