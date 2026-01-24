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

- |Fess| 15.5 ou supérieur est installé
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
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

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
     - ``true``
   * - ``spnego.prompt.ntlm``
     - Afficher l'invite NTLM
     - ``true``
   * - ``spnego.allow.localhost``
     - Autoriser l'accès localhost
     - ``true``
   * - ``spnego.allow.delegation``
     - Autoriser la délégation
     - ``false``
   * - ``spnego.exclude.dirs``
     - Répertoires exclus de l'authentification (séparés par des virgules)
     - (Aucun)
   * - ``spnego.logger.level``
     - Niveau de log (0-7)
     - (Auto)

.. warning::
   ``spnego.allow.unsecure.basic=true`` peut envoyer des identifiants encodés en Base64 sur des connexions non chiffrées.
   Pour les environnements de production, il est fortement recommandé de définir cette valeur sur ``false`` et d'utiliser HTTPS.

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
3. Définir l'URL ou le domaine du serveur Fess (ex: ``https://fess-server.example.local``)

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
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

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
    spnego.allow.localhost=false

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

Paramètres de débogage
----------------------

Pour investiguer les problèmes, vous pouvez afficher des logs détaillés liés à SPNEGO en ajustant le niveau de log de |Fess|.

Ajoutez ce qui suit à ``app/WEB-INF/conf/system.properties`` :

::

    spnego.logger.level=1

Ou ajoutez les loggers suivants à ``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>
    <Logger name="org.codelibs.spnego" level="DEBUG"/>

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-oidc` - Configuration SSO avec authentification OpenID Connect
- :doc:`sso-entraid` - Configuration SSO avec Microsoft Entra ID

