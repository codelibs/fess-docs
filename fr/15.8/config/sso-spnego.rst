===================================================
Configuration SSO avec Auth Intégrée Windows
===================================================

Aperçu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) en utilisant l'authentification intégrée Windows (SPNEGO/Kerberos).
En utilisant l'authentification intégrée Windows, les utilisateurs connectés à un ordinateur membre d'un domaine Windows peuvent accéder à |Fess| sans opérations de connexion supplémentaires.

Fonctionnement de l'authentification intégrée Windows
-----------------------------------------------------

Dans l'authentification intégrée Windows, |Fess| utilise le protocole SPNEGO (Simple and Protected GSSAPI Negotiation Mechanism) pour l'authentification Kerberos.

1. L'utilisateur se connecte au domaine Windows
2. L'utilisateur accède à |Fess|
3. |Fess| envoie un défi SPNEGO
4. Le navigateur obtient un ticket Kerberos et l'envoie au serveur
5. |Fess| valide le ticket et récupère le nom d'utilisateur
6. Les informations de groupe de l'utilisateur sont récupérées via LDAP
7. L'utilisateur est connecté et les informations de groupe sont appliquées à la recherche basée sur les rôles

Pour l'intégration avec la recherche basée sur les rôles, consultez :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification intégrée Windows, vérifiez les prérequis suivants :

- |Fess| 15.8 ou supérieur est installé
- Un serveur Active Directory (AD) est disponible
- Le serveur |Fess| est accessible depuis le domaine AD
- Vous avez la permission de configurer les noms de principal de service (SPN) dans AD
- Un compte pour récupérer les informations utilisateur via LDAP est disponible

Configuration côté Active Directory
===================================

Enregistrement du nom de principal de service (SPN)
---------------------------------------------------

Vous devez enregistrer un SPN pour |Fess| dans Active Directory.
Ouvrez une invite de commandes sur un ordinateur Windows membre du domaine AD et exécutez la commande ``setspn``.

::

    setspn -S HTTP/<nom d'hôte du serveur Fess> <utilisateur d'accès AD>

Exemple :

::

    setspn -S HTTP/fess-server.example.local svc_fess

Pour vérifier l'enregistrement :

::

    setspn -L <utilisateur d'accès AD>

.. note::
   Après l'enregistrement du SPN, si vous avez exécuté la commande sur le serveur Fess, déconnectez-vous de Windows et reconnectez-vous.

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification intégrée Windows, ajoutez le paramètre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=spnego

Fichier de configuration Kerberos
---------------------------------

Créez ``app/WEB-INF/classes/krb5.conf`` avec la configuration Kerberos.

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   Remplacez ``EXAMPLE.LOCAL`` par votre nom de domaine AD (en majuscules) et ``AD-SERVER.EXAMPLE.LOCAL`` par le nom d'hôte de votre serveur AD.

.. warning::
   Un ticket de service chiffré avec un type absent de ``permitted_enctypes`` est rejeté par
   l'accepteur Kerberos avec ``encryption type not in permitted_enctypes list``.
   Active Directory émet normalement des tickets de service AES256 : AES256 doit donc figurer dans la liste.

.. note::
   RC4 (``rc4-hmac``), 3DES et DES sont désactivés par défaut à partir de Java 17 ; les mentionner n'a
   donc aucun effet et l'exemple ci-dessus ne spécifie que AES.
   ``aes256-cts-hmac-sha384-192`` et ``aes128-cts-hmac-sha256-128`` sont les types AES-SHA2 (RFC 8009)
   pris en charge par Windows Server 2025.
   Un compte de service ne disposant que d'une clé RC4 ne peut pas servir à l'authentification Kerberos :
   réinitialisez son mot de passe afin que des clés AES soient générées.

Fichier de configuration de connexion
-------------------------------------

Créez ``app/WEB-INF/classes/auth_login.conf`` avec la configuration de connexion JAAS.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

.. note::
   Les noms de fichier par défaut de ``krb5.conf`` et ``auth_login.conf`` sont définis respectivement par ``spnego.krb5.conf`` et ``spnego.login.conf``, mais ces fichiers doivent impérativement être créés.
   SPNEGO est initialisé lors de la première connexion : |Fess| démarre donc même si ces fichiers sont absents, mais la connexion SSO échoue.

Paramètres requis
-----------------

Ajoutez les paramètres suivants à ``app/WEB-INF/conf/system.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``spnego.preauth.username``
     - Nom d'utilisateur de connexion AD
     - (Requis)
   * - ``spnego.preauth.password``
     - Mot de passe de connexion AD
     - (Requis)
   * - ``spnego.krb5.conf``
     - Chemin du fichier de configuration Kerberos
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Chemin du fichier de configuration de connexion
     - ``auth_login.conf``

.. note::
   Si ``spnego.preauth.username`` et ``spnego.preauth.password`` sont tous deux vides, le module de
   connexion serveur utilise un keytab.
   Si vous ne souhaitez pas stocker le mot de passe du compte de service AD dans un fichier de
   configuration |Fess|, créez un keytab et configurez ``spnego-server`` dans ``auth_login.conf``
   comme suit.

   ::

       spnego-server {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/var/lib/fess/fess.keytab"
           principal="HTTP/fess-server.example.local@EXAMPLE.LOCAL"
           storeKey=true
           isInitiator=false;
       };

Paramètres optionnels
---------------------

Les paramètres suivants peuvent être ajoutés si nécessaire.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``spnego.login.client.module``
     - Nom du module client
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - Nom du module serveur
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Autoriser l'authentification Basic
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - Autoriser l'authentification Basic non sécurisée
     - ``false``
   * - ``spnego.prompt.ntlm``
     - Revenir à l'authentification Basic lors de la réception d'un jeton NTLM
     - ``true``
   * - ``spnego.allow.localhost``
     - Autoriser l'accès depuis localhost
     - ``false``
   * - ``spnego.allow.delegation``
     - Autoriser la délégation
     - ``false``
   * - ``spnego.allowed.realms``
     - Domaines Kerberos acceptés en plus du domaine du serveur (séparés par des virgules)
     - (Aucun)
   * - ``spnego.logger.level``
     - Niveau de log interne de la bibliothèque SPNEGO (``1`` =FINEST, ``2`` =FINER, ``3`` =FINE, ``4`` =CONFIG, ``6`` =WARNING, ``7`` =SEVERE ; toute autre valeur, y compris ``0`` et ``5``, est traitée comme INFO)
     - (Automatique)

.. warning::
   ``spnego.allow.unsecure.basic=true`` peut envoyer des identifiants encodés en Base64 sur des connexions non chiffrées.
   Pour les environnements de production, il est fortement recommandé de définir cette valeur sur ``false`` et d'utiliser HTTPS.

.. note::
   Avec ``spnego.allow.unsecure.basic=false`` (valeur par défaut), l'authentification Basic n'est
   proposée que pour les requêtes dont ``HttpServletRequest#isSecure()`` renvoie ``true``.
   Lorsque TLS est terminé par un proxy inverse et que la requête est transmise à |Fess| en HTTP,
   cette valeur est ``false`` : un client qui ne peut pas obtenir de ticket Kerberos et bascule
   vers NTLM ne peut donc pas se connecter. Définissez ``tomcat.secure=true`` dans
   ``tomcat_config.properties`` pour indiquer à |Fess| que la requête est arrivée en HTTPS.

.. warning::
   Dans |Fess| 15.8, une connexion est refusée par défaut lorsque le domaine Kerberos du principal
   client diffère de celui du serveur. Si des utilisateurs se connectent depuis un domaine enfant
   d'une arborescence de domaines AD ou depuis une forêt approuvée, indiquez ces domaines dans
   ``spnego.allowed.realms``, séparés par des virgules. Sinon, les utilisateurs qui pouvaient se
   connecter jusqu'à la version 15.7 sont refusés avec ``Kerberos realm is not allowed``.

.. warning::
   |Fess| identifie un utilisateur par la partie du principal située avant ``@`` ; le domaine
   Kerberos ne fait donc pas partie du nom d'utilisateur. Lorsque vous indiquez des domaines
   supplémentaires dans ``spnego.allowed.realms``, les utilisateurs qui partagent un nom de compte
   entre domaines — par exemple ``alice@CORP.EXAMPLE.COM`` et ``alice@PARTNER.EXAMPLE.COM`` —
   deviennent le même utilisateur |Fess| et partagent ses groupes, ses rôles et ses autorisations
   sur les documents. N'ajoutez un domaine que si le nom de compte identifie exactement une
   personne dans tous les domaines que vous indiquez.

.. note::
   La liste d'autorisation s'applique également au repli sur l'authentification Basic. Si un
   utilisateur saisit un nom de la forme ``user@REALM``, ce domaine est comparé à
   ``spnego.allowed.realms`` et la connexion est refusée lorsqu'il n'est pas autorisé. Un simple
   nom de compte, ou la forme ``DOMAIN\user``, n'indique aucun domaine et est authentifié dans le
   domaine par défaut de ``krb5.conf``. Comme une connexion Basic est authentifiée directement
   auprès du domaine saisi par l'utilisateur, gardez la liste d'autorisation aussi réduite que
   possible et envisagez de définir ``spnego.allow.basic`` à ``false`` si vous vous en servez comme
   limite de sécurité.

.. note::
   Lorsque ``spnego.prompt.ntlm=true`` (valeur par défaut), ``spnego.allow.basic`` doit également être ``true``.
   Si vous définissez ``spnego.allow.basic=false``, vous devez également définir ``spnego.prompt.ntlm=false``.
   Si cette condition n'est pas respectée, une erreur se produit lors de l'initialisation de SPNEGO.

.. note::
   ``spnego.logger.level`` contrôle le niveau de log du logger interne de la bibliothèque SPNEGO (le logger ``java.util.logging`` nommé ``Spnego``).
   Si ce paramètre n'est pas défini, le niveau est déterminé automatiquement en fonction du niveau de log de |Fess|.

Configuration LDAP
==================

La configuration LDAP est requise pour récupérer les informations de groupe des utilisateurs authentifiés via l'authentification intégrée Windows.
Configurez les paramètres LDAP dans le panneau d'administration de |Fess| sous "Système" -> "Général".

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Élément
     - Exemple
   * - URL LDAP
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - Mot de passe
     - Mot de passe de l'utilisateur d'accès AD
   * - User DN
     - ``%s@example.local``
   * - Filtre de compte
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - Attribut memberOf
     - ``memberOf``

Paramètres du navigateur
========================

Les paramètres du navigateur client sont nécessaires pour utiliser l'authentification intégrée Windows.

Internet Explorer / Microsoft Edge
----------------------------------

1. Ouvrir les Options Internet
2. Sélectionner l'onglet "Sécurité"
3. Cliquer sur "Sites" pour la zone "Intranet local"
4. Cliquer sur "Avancé" et ajouter l'URL de Fess
5. Cliquer sur "Personnaliser le niveau" pour la zone "Intranet local"
6. Sous "Authentification utilisateur" -> "Connexion", sélectionner "Connexion automatique uniquement dans la zone Intranet"
7. Dans l'onglet "Avancé", cocher "Activer l'authentification Windows intégrée"

Google Chrome
-------------

Chrome utilise généralement les paramètres des Options Internet de Windows.
Si une configuration supplémentaire est nécessaire, définissez ``AuthServerAllowlist`` via la stratégie de groupe ou le registre.

Mozilla Firefox
---------------

1. Entrer ``about:config`` dans la barre d'adresse
2. Rechercher ``network.negotiate-auth.trusted-uris``
3. Définir l'URL ou le domaine du serveur Fess (ex : ``https://fess-server.example.local``)

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour un environnement de test.

``app/WEB-INF/conf/system.properties`` :

::

    # Activer SSO
    sso.type=spnego

    # Paramètres SPNEGO
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf`` :

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf`` :

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Configuration recommandée (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandée pour les environnements de production.

``app/WEB-INF/conf/system.properties`` :

::

    # Activer SSO
    sso.type=spnego

    # Paramètres SPNEGO
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # Paramètres de sécurité (production)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.prompt.ntlm=false
    spnego.allow.localhost=false

.. note::
   Si vous définissez ``spnego.allow.basic=false``, vous devez également définir ``spnego.prompt.ntlm=false``.
   La valeur par défaut de ``spnego.prompt.ntlm`` est ``true`` ; omettre ce paramètre provoque une erreur lors de l'initialisation.

Dépannage
=========

Problèmes courants et solutions
-------------------------------

La boîte de dialogue d'authentification apparaît
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le serveur Fess est ajouté à la zone Intranet local dans les paramètres du navigateur
- Vérifiez que "Activer l'authentification Windows intégrée" est activé
- Vérifiez que le SPN est correctement enregistré (``setspn -L <nom d'utilisateur>``)

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le nom de domaine (majuscules) et le nom du serveur AD dans ``krb5.conf`` sont corrects
- Vérifiez que ``spnego.preauth.username`` et ``spnego.preauth.password`` sont corrects
- Vérifiez la connectivité réseau vers le serveur AD

Impossible de récupérer les informations de groupe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que les paramètres LDAP sont corrects
- Vérifiez que le Bind DN et le mot de passe sont corrects
- Vérifiez que l'utilisateur appartient à des groupes dans AD

La connexion renvoie HTTP 400
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour un utilisateur appartenant à de nombreux groupes, le ticket Kerberos (PAC) devient volumineux et
l'en-tête ``Authorization`` peut dépasser la limite par défaut de Tomcat (8 Ko), ce qui donne un 400.
La requête n'atteint jamais |Fess| : rien n'est écrit dans le journal.
Augmentez la limite dans ``tomcat_config.properties``.

::

    tomcat.maxHttpHeaderSize=65536

L'authentification échoue après le changement du mot de passe du compte de service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les informations d'identification du serveur sont obtenues une seule fois lors de la première
connexion, puis mises en cache pour toute la durée de vie du processus.
Redémarrez |Fess| après avoir changé le mot de passe du compte de service dans AD ou remplacé le
keytab. Un redémarrage est également requis après toute modification d'un paramètre ``spnego.*``.

Paramètres de débogage
----------------------

Pour investiguer les problèmes, vous pouvez afficher des logs détaillés liés à SPNEGO.

Pour afficher les logs détaillés internes de la bibliothèque SPNEGO, ajoutez ce qui suit à ``app/WEB-INF/conf/system.properties``.
``spnego.logger.level=1`` produit les logs les plus détaillés (FINEST).

::

    spnego.logger.level=1

Pour afficher les logs détaillés du traitement SPNEGO côté |Fess| (package ``org.codelibs.fess.sso.spnego``), ajoutez le logger suivant à ``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>

.. note::
   Les logs de la bibliothèque SPNEGO elle-même sont émis via ``java.util.logging`` et se contrôlent avec ``spnego.logger.level``, non via ``log4j2.xml``.
   Les logs du traitement d'intégration côté |Fess| se contrôlent via le logger ``log4j2.xml``.

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-oidc` - Configuration SSO avec authentification OpenID Connect
- :doc:`sso-entraid` - Configuration SSO avec Microsoft Entra ID
