==================================================
Protéger la recherche avec SSO et contrôle d'accès
==================================================

Introduction
============

Une plateforme de recherche interne rassemble des documents protégés par des autorisations.
Plutôt que de distribuer des mots de passe propres à Fess, la plupart des déploiements souhaitent que les utilisateurs se connectent via le fournisseur d'identité (IdP) de l'organisation et que les résultats de recherche soient filtrés selon leurs groupes.

Dans cet article, nous configurons les éléments suivants dans Fess 15.9, jusqu'à vérifier qu'ils fonctionnent.

- Authentification unique (SSO) avec Entra ID, OpenID Connect, SAML ou SPNEGO
- Empêcher les utilisateurs non connectés de rechercher grâce à « Connexion requise »
- Faire reconnaître correctement HTTPS par Fess derrière un proxy inverse qui termine TLS
- Revoir les jetons d'accès et les durées de conservation du journal d'audit et du journal de recherche

La conception des rôles et des groupes, et la manière de les indiquer dans les autorisations des configurations d'exploration, sont traitées dans :doc:`guide-05`.

Le SSO est fourni par des plugins
=================================

Dans Fess 15.9, le traitement de l'authentification SSO a été séparé du cœur en quatre plugins.

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - Méthode
     - Plugin
     - « SSO Type » (``sso.type``)
     - Origine du nom d'utilisateur
     - Origine des groupes et des rôles
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID (``entraid``)
     - Nom d'utilisateur du compte connecté (généralement l'UPN)
     - Groupes et rôles obtenus via Microsoft Graph
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect (``oic``)
     - Claim ``email`` de l'ID Token
     - Claim ``groups`` de l'ID Token. Les rôles proviennent uniquement de « Rôles par défaut »
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML (``saml``)
     - NameID de l'assertion
     - Valeurs des attributs désignés par « Nom de l'attribut de groupe » (par défaut ``memberOf``) et « Nom de l'attribut de rôle »
   * - SPNEGO (Kerberos)
     - ``fess-sso-spnego``
     - SPNEGO (``spnego``)
     - Partie du principal Kerberos située avant ``@``
     - Groupes obtenus via les paramètres LDAP de [Général]

Seul OpenID Connect a un nom de plugin (``oidc``) différent de la valeur de ``sso.type`` (``oic``).

La procédure est la même pour toutes les méthodes.

1. Installer le plugin et redémarrer Fess
2. Enregistrer Fess auprès de l'IdP. L'adresse de retour (URI de redirection ou URL ACS) est ``https://<hôte Fess>/sso/``
3. Dans la console d'administration, sous [Système] > [Général], saisir les informations de l'IdP dans la section de la méthode, choisir « SSO Type », puis mettre à jour
4. Ouvrir ``https://<hôte Fess>/sso/`` dans un navigateur et vérifier que la connexion via l'IdP fonctionne

Installer le plugin
-------------------

L'image Docker (``ghcr.io/codelibs/fess:15.9.0``) contient les quatre plugins SSO (les images dont le nom comporte ``-slim`` ne les contiennent pas).
Ils ne sont pas fournis avec les paquets ZIP, DEB et RPM ; installez-les depuis [Installer] dans [Système] > [Plugin], ou avec la commande suivante.

::

    $ bin/fess-setup install plugin fess-sso-entraid

Redémarrez Fess après une installation ou une suppression.
Utilisez des plugins de la même version mineure que Fess (15.9.x).

Si vous choisissez un « SSO Type » sans que le plugin soit installé, ``/sso/`` ne fait que revenir à l'écran de connexion, et un WARN ``No SSO authenticator is registered as ...`` est écrit une fois dans ``fess.log``.

Où les paramètres sont enregistrés
----------------------------------

Les valeurs saisies dans [Général] sont enregistrées dans ``system.properties`` (``app/WEB-INF/conf/`` pour le paquet ZIP, ``/etc/fess/`` pour DEB et RPM).
Les paramètres OpenID Connect, SAML et Entra ID sont lus à chaque connexion : ils s'appliquent dès l'enregistrement, sans redémarrage.
Les paramètres SPNEGO sont partagés par l'ensemble du processus ; un redémarrage est donc nécessaire après leur modification.

Le conteneur ``fess01`` de Docker n'a pas de volume : si vous exécutez ``docker compose down`` puis ``up``, les paramètres de [Général] sont perdus.
Avant de recréer le conteneur, téléchargez ``system.properties`` depuis [Informations système] > [Sauvegarde], puis, après l'avoir recréé, téléversez-le depuis le même écran pour restaurer les paramètres.

SSO avec Entra ID
=================

Pour les organisations qui utilisent Microsoft 365, ``fess-sso-entraid`` est la solution la plus simple.
Les groupes sont récupérés via Microsoft Graph après la connexion ; il n'est donc pas nécessaire de configurer des revendications de groupe côté IdP.

Paramètres côté Entra ID
------------------------

Dans le portail Azure, créez une nouvelle inscription dans « Inscriptions d'applications » et configurez-la comme suit.

- Types de comptes pris en charge : Comptes de cet annuaire d'organisation uniquement
- URI de redirection : ``https://fess.example.com/sso/`` avec la plateforme « Web » (elle doit correspondre exactement, ``/`` final compris)
- Dans « Certificats et secrets », créez un secret client et notez sa valeur (elle n'est affichée que juste après la création)
- Dans « Autorisations d'API », ajoutez les autorisations déléguées Microsoft Graph ``User.Read`` et ``GroupMember.Read.All``, puis accordez le consentement administrateur

Sans ``GroupMember.Read.All``, les groupes parents imbriqués ne peuvent pas être récupérés, et un avertissement ``Not allowed to read the parent groups of ...`` est écrit dans ``fess.log``.

Paramètres côté Fess
--------------------

Saisissez les valeurs dans la section « Entra ID » de [Système] > [Général].

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Champ
     - Clé
     - Valeur
   * - Locataire (ID ou domaine)
     - ``entraid.tenant``
     - ID de l'annuaire (locataire), ou ``yourcompany.onmicrosoft.com``
   * - ID client
     - ``entraid.client.id``
     - ID d'application (client)
   * - Clé secrète client
     - ``entraid.client.secret``
     - Valeur du secret créé
   * - URL de réponse
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

Enfin, choisissez « Entra ID » pour « SSO Type » dans la section « Système », puis cliquez sur [Mettre à jour].

Faire correspondre les groupes et les autorisations des documents
-----------------------------------------------------------------

Pour les groupes et rôles obtenus depuis Entra ID, leur ID (GUID) devient toujours une autorisation.
En outre, les valeurs des attributs listés dans « Champs d'autorisation » (``entraid.permission.fields``, par défaut ``mail``) deviennent elles aussi des autorisations.

Les groupes de sécurité ne sont pas à extension messagerie ; avec la valeur par défaut, seul leur GUID devient une autorisation.
Si les ACL de votre serveur de fichiers sont écrites avec des noms de groupe, réglez « Champs d'autorisation » sur ``mail,displayName``.
Cependant, ``displayName`` n'est pas unique : un groupe portant le même nom qu'un groupe intégré de Windows (comme ``Administrators``) correspond aussi aux documents de ce groupe intégré.

Dans les autorisations de la configuration d'exploration, écrivez la valeur obtenue telle quelle, préfixée de ``{group}`` (par exemple ``{group}sales@example.com``).

.. warning::

   Les « Rôles par défaut » (``entraid.default.roles``) sont attribués à tous les utilisateurs du locataire.
   Si vous y mettez ``admin``, tout le monde pourra accéder à la console d'administration.

SSO avec OpenID Connect, SAML ou SPNEGO
=======================================

OpenID Connect
--------------

L'intégration avec des fournisseurs OpenID Connect tels que Keycloak ou Okta se fait avec ``fess-sso-oidc``.
Côté fournisseur, enregistrez Fess comme application web (client) et définissez l'URI de redirection sur ``https://fess.example.com/sso/``.

Les principaux champs à saisir dans la section « OpenID Connect » de [Général] sont les suivants.

- URL du serveur d'autorisation (``oic.auth.server.url``) et URL du serveur de jetons (``oic.token.server.url``) : saisissez séparément les valeurs indiquées dans ``/.well-known/openid-configuration`` du fournisseur. L'URL du serveur de jetons doit utiliser ``https`` (``http`` n'est autorisé que pour ``localhost``, ``127.x.x.x`` et ``::1``)
- ID client et Clé secrète client
- Scope : ``openid email``. Le nom d'utilisateur est tiré du claim ``email`` ; ``email`` est donc obligatoire
- URL de base (``oic.base.url``) : ``https://fess.example.com``. Si l'URL de redirection est laissée vide, elle vaut ``{URL de base}/sso/``

Pour les groupes, les valeurs du claim ``groups`` de l'ID Token deviennent telles quelles des autorisations.
Contrairement à Entra ID, les groupes parents ne sont pas parcourus ; si vous avez besoin des groupes imbriqués, incluez-les dans le claim côté fournisseur.
Les rôles ne sont pas tirés des claims ; seules les valeurs de « Rôles par défaut » sont attribuées.

``oic.issuer``, qui vérifie l'émetteur (``iss``), n'a pas de champ dans [Général] ; écrivez-le directement dans ``system.properties``.

SAML
----

Avec ``fess-sso-saml``, Fess joue le rôle de SP.
L'IdP renvoie l'assertion par un POST intersite ; avec la valeur par défaut ``tomcat.sameSiteCookies = lax``, la connexion n'aboutit donc pas.
Modifiez-la comme suit dans ``tomcat_config.properties``, puis redémarrez Fess.

::

    tomcat.sameSiteCookies = none

``none`` ne fonctionne qu'en HTTPS.
En HTTP simple, la connexion deviendra impossible ; effectuez donc d'abord la configuration HTTPS décrite plus loin.

Saisissez les éléments suivants dans la section « SAML » de [Général].

- URL de base du SP (``saml.sp.base.url``) : ``https://fess.example.com``. Elle détermine l'Entity ID du SP (``{URL de base du SP}/sso/metadata``) et l'URL ACS (``{URL de base du SP}/sso/``)
- IdP Entity ID, IdP SSO URL et Certificat X.509 de l'IdP : recopiez-les depuis la console d'administration de l'IdP. Saisissez le certificat en Base64 sur une seule ligne, sans les lignes ``-----BEGIN CERTIFICATE-----``
- Nom de l'attribut de groupe (par défaut ``memberOf``) et Nom de l'attribut de rôle : alignez-les sur les noms d'attributs envoyés par l'IdP

Il n'existe pas de fonction permettant de charger l'URL des métadonnées de l'IdP.
À l'inverse, les métadonnées SP de Fess sont disponibles à ``https://fess.example.com/sso/metadata`` et peuvent être chargées dans l'IdP.
Le nom d'utilisateur est le NameID, dont le format est par défaut l'adresse e-mail.
Seule la connexion initiée par le SP, qui commence à ``/sso/`` de Fess, est prise en charge ; les connexions lancées depuis une tuile du portail de l'IdP sont refusées.

En production, ajoutez ``saml.security.want_assertions_signed=true`` à ``system.properties`` pour exiger des assertions signées.
Les paramètres de signature et de chiffrement n'ont pas de champ dans [Général] et ne peuvent pas non plus être indiqués comme propriétés système de la JVM ; écrivez-les directement dans le fichier.

.. warning::

   Lorsque « Nom de l'attribut de rôle » est défini, les valeurs envoyées par l'IdP deviennent telles quelles des rôles Fess.
   Le rôle administrateur est ``authentication.admin.roles=admin`` ; un utilisateur pour lequel l'IdP envoie ``admin`` devient donc administrateur.

SPNEGO (authentification intégrée Windows)
------------------------------------------

Pour permettre aux utilisateurs de postes Windows membres du domaine de se connecter sans saisir de mot de passe, utilisez ``fess-sso-spnego``.
Il faut enregistrer un SPN dans l'AD (``setspn -S HTTP/<nom d'hôte Fess> <compte de service>``), créer ``krb5.conf`` et ``auth_login.conf`` dans ``app/WEB-INF/classes/``, et configurer les paramètres intranet du navigateur.
Les groupes sont récupérés depuis l'AD selon les paramètres de la section « LDAP » de [Général].
Suivez la procédure de `Configuration SSO avec Auth Intégrée Windows <https://fess.codelibs.org/fr/stable/config/sso-spnego.html>`__, et redémarrez Fess après avoir modifié les champs SPNEGO de [Général].

Vérifier que le SSO fonctionne
==============================

Commencez par ouvrir ``https://fess.example.com/sso/`` en étant déconnecté, et vérifiez que vous êtes redirigé vers l'écran de connexion de l'IdP.

Une fois connecté, ouvrez ``https://fess.example.com/api/v2/auth/me`` dans le même navigateur.

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

Vérifiez que ``groups`` contient les groupes attendus et que ``admin`` est conforme à votre intention.
Avec Entra ID, les groupes sont récupérés après la connexion : juste après, ``permission_state`` vaut ``PENDING``, puis passe à ``RESOLVED`` une fois la récupération terminée.

Le journal d'audit ``audit.log`` enregistre également une ligne ``LOGIN`` avec le nom d'utilisateur et les autorisations.

En cas d'échec de la connexion, vous revenez à l'écran de connexion et le message « Le processus de connexion SSO a échoué. » s'affiche.
La cause apparaît dans un WARN de ``fess.log`` (par exemple ``Failed to process SSO login``).

Même si les paramètres SSO sont erronés, vous pouvez vous connecter avec l'utilisateur local ``admin`` depuis ``/login/`` et les corriger.

.. note::

   Les utilisateurs connectés ne reçoivent pas ``{role}guest``.
   Les documents des configurations d'exploration qui n'ont que la valeur par défaut ``{role}guest`` disparaissent des résultats de recherche des utilisateurs connectés par SSO.
   Pour savoir comment composer les autorisations, consultez :doc:`guide-05`.

Empêcher les utilisateurs non connectés de rechercher
=====================================================

Si vous activez « Connexion requise » dans [Système] > [Général], les utilisateurs non connectés ne peuvent plus rechercher.

- Si le SSO est disponible (plugin installé et « SSO Type » choisi), les utilisateurs qui ouvrent l'écran de recherche du thème fourni ``bootstrap`` sont automatiquement envoyés vers ``/sso/`` et, après s'être connectés auprès de l'IdP, reviennent à leur recherche d'origine
- Sans SSO, une boîte de dialogue de connexion s'affiche sur l'écran de recherche
- L'API de recherche sous ``/api/v2/`` n'est plus utilisable de façon anonyme non plus ; seuls les appels munis d'un jeton d'accès sont acceptés

Même sans activer « Connexion requise », si le SSO est disponible et que « Afficher le lien de connexion » est activé, le lien de connexion de l'écran de recherche pointe vers ``/sso/``.

Publier en HTTPS
================

Terminer TLS sur un proxy inverse
---------------------------------

Dans une configuration où Nginx ou un équivalent termine TLS et transmet les requêtes à Fess en HTTP, les requêtes reçues par Fess apparaissent en ``http://``.
En l'état, la validation des assertions SAML (comparaison de ``Destination``) échoue, et SPNEGO ne propose pas le repli sur l'authentification Basic.

Dans ``tomcat_config.properties``, indiquez à Fess le schéma et le port vus de l'extérieur.
Ce fichier se trouve dans ``lib/classes/`` pour le paquet ZIP, et dans ``/etc/fess/`` pour DEB, RPM et l'image Docker.

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

Côté proxy, transmettez l'en-tête ``Host`` d'origine tel quel à Fess (avec Nginx, ``proxy_set_header Host $host;``).
En effet, Fess construit le nom d'hôte de l'URL de la requête à partir de l'en-tête ``Host``.

Par ailleurs, définissez ``session.cookie.secure=true`` dans ``fess_config.properties`` pour ajouter l'attribut ``Secure`` au cookie de session.
Par défaut (vide), la décision est laissée à Tomcat, mais dans les environnements de production où un proxy termine TLS, indiquez explicitement ``true``.
Si vous utilisez ``tomcat.sameSiteCookies = none`` pour SAML, les cookies ``SameSite=None`` exigent aussi l'attribut ``Secure``.

Après modification de l'un ou l'autre fichier, Fess doit être redémarré.

Recevoir TLS directement dans Fess
----------------------------------

Sans proxy, définissez ``tomcat.SSLEnabled=true``, ``tomcat.certificateKeystoreFile``, ``tomcat.certificateKeystorePassword``, ``tomcat.certificateKeyAlias``, etc. dans ``tomcat_config.properties``.
Pour un exemple de configuration, consultez `Configuration de la sécurité <https://fess.codelibs.org/fr/stable/install/security.html>`__.

Fermer le port d'OpenSearch
---------------------------

Le fichier ``compose-opensearch3.yaml`` de docker-fess expose OpenSearch, avec son plugin de sécurité désactivé, sur le port 9200 de l'hôte.
Fess se connecte par le réseau entre conteneurs (``http://search01:9200``) ; sur un serveur partagé, vous pouvez donc retirer ``ports`` de ``search01``.

Gérer les jetons d'accès
========================

Les jetons permettant aux systèmes métier d'appeler l'API se créent dans [Système] > [Jeton d'accès].
L'appel de l'API est traité dans :doc:`guide-11` ; nous ne listons ici que les points pour une exploitation sûre.

- N'attribuez à un jeton de recherche que les autorisations des documents que ce système peut voir (par exemple ``{group}sales``)
- Un jeton doté de ``{role}admin-api`` peut utiliser non seulement l'enregistrement de documents, mais tous les points de terminaison de l'Admin API. Il n'existe pas d'autorisation plus restreinte du type « enregistrement uniquement »
- Définissez « Expire » et recréez le jeton à son expiration. Supprimez les jetons devenus inutiles
- Conservez les jetons côté serveur ; ne les intégrez pas dans du JavaScript exécuté dans le navigateur
- Laissez « Nom du paramètre » vide. S'il est défini, des autorisations peuvent être ajoutées via un paramètre d'URL
- Traitez le rôle ``admin-accesstoken``, qui peut émettre des jetons, et le rôle ``admin-accesstoken-view``, qui peut afficher leurs valeurs, comme l'équivalent d'administrateurs

Décider de la durée de conservation des journaux
================================================

L'emplacement des fichiers journaux et leur surveillance sont traités dans :doc:`guide-10`.
Ici, nous faisons le point sur les enregistrements utilisés pour les contrôles de sécurité et sur leur durée de conservation.

Le journal d'audit (``audit.log``) enregistre, une ligne par événement, les connexions (``LOGIN``), les échecs de connexion (``LOGIN_FAILURE``), les déconnexions (``LOGOUT``), les accès à la console d'administration et à l'Admin API (``ACCESS``), les refus pour droits insuffisants (``ACCESS_DENIED``), etc.
Le fichier est écrit dans ``logs/`` pour le paquet ZIP, et dans ``/var/log/fess/`` pour DEB, RPM et l'image Docker ; il peut aussi être téléchargé depuis [Informations système] > [Fichier journal].
Le format par défaut est LTSV ; dans l'image Docker, c'est du JSON au format ECS.
Les fichiers ayant subi une rotation sont supprimés au bout de 360 jours (``backup.audit.max.age`` dans ``log4j2.xml``).

Qui a recherché quoi est consigné dans le journal de recherche enregistré dans OpenSearch, consultable dans [Informations système] > [Journal de recherche].
La valeur par défaut de « Supprimer les anciens journaux de recherche » dans [Général] est ``-1`` : les journaux de recherche sont conservés sans être supprimés.
Ce nombre de jours s'applique aussi au journal des clics, au journal des favoris et au journal de chat.
Si vos règles internes fixent une durée de conservation, saisissez ce nombre de jours.

Fonctionnement sur plusieurs instances
======================================

Dans Fess 15.9, les sessions de connexion sont conservées dans la mémoire de chaque processus Fess.
Les valeurs utilisées pendant le SSO (``state`` d'OpenID Connect et ID de l'AuthnRequest SAML) sont aussi stockées dans la session ; si vous placez plusieurs instances derrière un répartiteur de charge, activez donc les sessions persistantes (sticky sessions) afin que le même utilisateur soit toujours dirigé vers le même Fess.
Pour la configuration multi-instances elle-même, consultez :doc:`guide-14`.

Notez que l'enregistrement des sessions dans OpenSearch pour les partager entre plusieurs instances, ainsi que la connexion par clé d'accès (passkey) des utilisateurs locaux, sont des fonctionnalités de la version 15.10 et ultérieures.

Articles suivants
=================

- Concevoir les rôles et les groupes, et indiquer les autorisations dans les configurations d'exploration : :doc:`guide-05`
- Intégration par API avec des jetons d'accès : :doc:`guide-11`
- Emplacement des journaux, surveillance et sauvegarde : :doc:`guide-10`
- Passage à une configuration multi-instances : :doc:`guide-14`
- Refléter les ACL du serveur de fichiers dans les résultats de recherche : :doc:`file-server-search`

Références
==========

- `Configuration SSO avec Entra ID <https://fess.codelibs.org/fr/stable/config/sso-entraid.html>`__
- `Configuration SSO avec OpenID Connect <https://fess.codelibs.org/fr/stable/config/sso-oidc.html>`__
- `Configuration SSO avec authentification SAML <https://fess.codelibs.org/fr/stable/config/sso-saml.html>`__
- `Configuration SSO avec Auth Intégrée Windows <https://fess.codelibs.org/fr/stable/config/sso-spnego.html>`__
- `Général <https://fess.codelibs.org/fr/stable/admin/general-guide.html>`__
- `Jeton d'accès <https://fess.codelibs.org/fr/stable/admin/accesstoken-guide.html>`__
- `Configuration de la sécurité <https://fess.codelibs.org/fr/stable/install/security.html>`__
- `Configuration des journaux <https://fess.codelibs.org/fr/stable/config/admin-logging.html>`__
