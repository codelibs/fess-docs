=======================================
Configuration SSO avec Entra ID
=======================================

Apercu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) en utilisant Microsoft Entra ID (anciennement Azure AD).
En utilisant l'authentification Entra ID, vous pouvez integrer les informations utilisateur et les informations de groupe de votre environnement Microsoft 365 avec la recherche basee sur les roles de |Fess|.

Fonctionnement de l'authentification Entra ID
---------------------------------------------

Dans l'authentification Entra ID, |Fess| opere en tant que client OAuth 2.0/OpenID Connect et collabore avec Microsoft Entra ID pour l'authentification.

1. L'utilisateur accede au point de terminaison SSO de |Fess| (``/sso/``)
2. |Fess| redirige vers le point de terminaison d'autorisation d'Entra ID
3. L'utilisateur s'authentifie aupres d'Entra ID (connexion Microsoft)
4. Entra ID redirige le code d'autorisation vers |Fess|
5. |Fess| utilise le code d'autorisation pour obtenir un jeton d'acces
6. |Fess| utilise l'API Microsoft Graph pour recuperer les informations de groupe et de role de l'utilisateur
7. L'utilisateur est connecte et les informations de groupe sont appliquees a la recherche basee sur les roles

Pour l'integration avec la recherche basee sur les roles, consultez :doc:`security-role`.

Prerequis
=========

Avant de configurer l'authentification Entra ID, verifiez les prerequis suivants :

- |Fess| 15.4 ou superieur est installe
- Un tenant Microsoft Entra ID (Azure AD) est disponible
- |Fess| est accessible via HTTPS (requis pour les environnements de production)
- Vous avez la permission d'enregistrer des applications dans Entra ID

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification Entra ID, ajoutez le parametre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=entraid

Parametres requis
-----------------

Configurez les informations obtenues d'Entra ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
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
     - Utilise l'URL de la requete

.. note::
   Au lieu du prefixe ``entraid.*``, vous pouvez egalement utiliser le prefixe legacy ``aad.*`` pour la retrocompatibilite.

Parametres optionnels
---------------------

Les parametres suivants peuvent etre ajoutes si necessaire.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``entraid.authority``
     - URL du serveur d'authentification
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - Duree de vie du state (secondes)
     - ``3600``
   * - ``entraid.default.groups``
     - Groupes par defaut (separes par des virgules)
     - (Aucun)
   * - ``entraid.default.roles``
     - Roles par defaut (separes par des virgules)
     - (Aucun)

Configuration cote Entra ID
===========================

Enregistrement de l'application dans le portail Azure
-----------------------------------------------------

1. Connectez-vous au `Portail Azure <https://portal.azure.com/>`_

2. Selectionnez **Microsoft Entra ID**

3. Allez dans **Gerer** → **Inscriptions d'applications** → **Nouvelle inscription**

4. Enregistrez l'application :

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Parametre
        - Valeur
      * - Nom
        - Tout nom (ex: Fess SSO)
      * - Types de comptes pris en charge
        - "Comptes de cet annuaire d'organisation uniquement"
      * - Plateforme
        - Web
      * - URI de redirection
        - ``https://<hote Fess>/sso/``

5. Cliquez sur **Inscrire**

Creation d'un secret client
---------------------------

1. Sur la page de details de l'application, cliquez sur **Certificats et secrets**

2. Cliquez sur **Nouveau secret client**

3. Definissez une description et une date d'expiration, puis cliquez sur **Ajouter**

4. Copiez et sauvegardez la **Valeur** generee (cette valeur ne sera plus affichee)

.. warning::
   La valeur du secret client n'est affichee qu'immediatement apres la creation.
   Assurez-vous de l'enregistrer avant de quitter la page.

Configuration des autorisations d'API
-------------------------------------

1. Cliquez sur **Autorisations d'API** dans le menu de gauche

2. Cliquez sur **Ajouter une autorisation**

3. Selectionnez **Microsoft Graph**

4. Selectionnez **Autorisations deleguees**

5. Ajoutez l'autorisation suivante :

   - ``Group.Read.All`` - Requis pour recuperer les informations de groupe de l'utilisateur

6. Cliquez sur **Ajouter des autorisations**

7. Cliquez sur **Accorder le consentement administrateur pour <nom du tenant>**

.. note::
   Le consentement administrateur necessite des privileges d'administrateur de tenant.

Informations a obtenir
----------------------

Les informations suivantes sont utilisees pour la configuration de Fess :

- **ID d'application (Client)** : Sur la page Vue d'ensemble, sous "ID d'application (client)"
- **ID du tenant** : Sur la page Vue d'ensemble, sous "ID de repertoire (tenant)" ou au format ``xxx.onmicrosoft.com``
- **Valeur du secret client** : La valeur creee dans Certificats et secrets

Mappage des groupes et roles
============================

Avec l'authentification Entra ID, |Fess| recupere automatiquement les groupes et roles auxquels un utilisateur appartient en utilisant l'API Microsoft Graph.
Les ID de groupe et noms de groupe recuperes peuvent etre utilises pour la recherche basee sur les roles de |Fess|.

Groupes imbriques
-----------------

|Fess| recupere non seulement les groupes auxquels les utilisateurs appartiennent directement, mais aussi les groupes parents (groupes imbriques) de maniere recursive.
Ce traitement est execute de maniere asynchrone apres la connexion pour minimiser l'impact sur le temps de connexion.

Parametres de groupe par defaut
-------------------------------

Pour attribuer des groupes communs a tous les utilisateurs Entra ID :

::

    entraid.default.groups=authenticated_users,entra_users

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour verification dans un environnement de test.

::

    # Activer SSO
    sso.type=entraid

    # Parametres Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Configuration recommandee (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandee pour les environnements de production.

::

    # Activer SSO
    sso.type=entraid

    # Parametres Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Groupes par defaut (optionnel)
    entraid.default.groups=authenticated_users

Configuration legacy (retrocompatibilite)
-----------------------------------------

Pour la compatibilite avec les versions anterieures, le prefixe ``aad.*`` peut egalement etre utilise.

::

    # Activer SSO
    sso.type=entraid

    # Cles de configuration legacy
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Depannage
=========

Problemes courants et solutions
-------------------------------

Impossible de revenir a Fess apres l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifiez que l'URI de redirection est correctement configuree dans l'inscription de l'application du portail Azure
- Assurez-vous que la valeur de ``entraid.reply.url`` correspond exactement a la configuration du portail Azure
- Verifiez que le protocole (HTTP/HTTPS) correspond
- Verifiez que l'URI de redirection se termine par ``/``

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifiez que l'ID du tenant, l'ID client et le secret client sont correctement configures
- Verifiez que le secret client n'a pas expire
- Verifiez que le consentement administrateur a ete accorde pour les autorisations d'API

Impossible de recuperer les informations de groupe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifiez que l'autorisation ``Group.Read.All`` a ete accordee
- Verifiez que le consentement administrateur a ete accorde
- Verifiez que l'utilisateur appartient a des groupes dans Entra ID

Parametres de debogage
----------------------

Pour investiguer les problemes, vous pouvez afficher des logs detailles lies a Entra ID en ajustant le niveau de log de |Fess|.

Dans ``app/WEB-INF/classes/log4j2.xml``, vous pouvez ajouter le logger suivant pour changer le niveau de log :

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Reference
=========

- :doc:`security-role` - Configuration de la recherche basee sur les roles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-oidc` - Configuration SSO avec authentification OpenID Connect
