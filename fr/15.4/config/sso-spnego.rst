===================================================
Configuration SSO avec Auth Integree Windows
===================================================

Apercu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) en utilisant l'authentification integree Windows (SPNEGO/Kerberos).
En utilisant l'authentification integree Windows, les utilisateurs connectes a un ordinateur membre d'un domaine Windows peuvent acceder a |Fess| sans operations de connexion supplementaires.

Fonctionnement de l'authentification integree Windows
-----------------------------------------------------

Dans l'authentification integree Windows, |Fess| utilise le protocole SPNEGO (Simple and Protected GSSAPI Negotiation Mechanism) pour l'authentification Kerberos.

1. L'utilisateur se connecte au domaine Windows
2. L'utilisateur accede a |Fess|
3. |Fess| envoie un defi SPNEGO
4. Le navigateur obtient un ticket Kerberos et l'envoie au serveur
5. |Fess| valide le ticket et recupere le nom d'utilisateur
6. Les informations de groupe de l'utilisateur sont recuperees via LDAP
7. L'utilisateur est connecte et les informations de groupe sont appliquees a la recherche basee sur les roles

Pour l'integration avec la recherche basee sur les roles, consultez :doc:`security-role`.

Prerequis
=========

Avant de configurer l'authentification integree Windows, verifiez les prerequis suivants :

- |Fess| 15.4 ou superieur est installe
- Un serveur Active Directory (AD) est disponible
- Le serveur |Fess| est accessible depuis le domaine AD
- Vous avez la permission de configurer les noms de principal de service (SPN) dans AD
- Un compte pour recuperer les informations utilisateur via LDAP est disponible

Configuration cote Active Directory
===================================

Enregistrement du nom de principal de service (SPN)
---------------------------------------------------

Vous devez enregistrer un SPN pour |Fess| dans Active Directory.
Ouvrez une invite de commandes sur un ordinateur Windows membre du domaine AD et executez la commande ``setspn``.

::

    setspn -S HTTP/<nom d'hote du serveur Fess> <utilisateur d'acces AD>

Exemple :

::

    setspn -S HTTP/fess-server.example.local svc_fess

Pour verifier l'enregistrement :

::

    setspn -L <utilisateur d'acces AD>

.. note::
   Apres l'enregistrement du SPN, si vous avez execute la commande sur le serveur Fess, deconnectez-vous de Windows et reconnectez-vous.

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification integree Windows, ajoutez le parametre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=spnego

Fichier de configuration Kerberos
---------------------------------

Creez ``app/WEB-INF/classes/krb5.conf`` avec la configuration Kerberos.

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
   Remplacez ``EXAMPLE.LOCAL`` par votre nom de domaine AD (en majuscules) et ``AD-SERVER.EXAMPLE.LOCAL`` par le nom d'hote de votre serveur AD.

Fichier de configuration de connexion
-------------------------------------

Creez ``app/WEB-INF/classes/auth_login.conf`` avec la configuration de connexion JAAS.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Parametres requis
-----------------

Ajoutez les parametres suivants a ``app/WEB-INF/conf/system.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
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

Parametres optionnels
---------------------

Les parametres suivants peuvent etre ajoutes si necessaire.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
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
     - Autoriser l'authentification Basic non securisee
     - ``true``
   * - ``spnego.prompt.ntlm``
     - Afficher l'invite NTLM
     - ``true``
   * - ``spnego.allow.localhost``
     - Autoriser l'acces localhost
     - ``true``
   * - ``spnego.allow.delegation``
     - Autoriser la delegation
     - ``false``
   * - ``spnego.exclude.dirs``
     - Repertoires exclus de l'authentification (separes par des virgules)
     - (Aucun)
   * - ``spnego.logger.level``
     - Niveau de log (0-7)
     - (Auto)

.. warning::
   ``spnego.allow.unsecure.basic=true`` peut envoyer des identifiants encodes en Base64 sur des connexions non chiffrees.
   Pour les environnements de production, il est fortement recommande de definir cette valeur sur ``false`` et d'utiliser HTTPS.

Configuration LDAP
==================

La configuration LDAP est requise pour recuperer les informations de groupe des utilisateurs authentifies via l'authentification integree Windows.
Configurez les parametres LDAP dans le panneau d'administration de |Fess| sous "Systeme" -> "General".

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Element
     - Exemple
   * - URL LDAP
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - Mot de passe
     - Mot de passe de l'utilisateur d'acces AD
   * - User DN
     - ``%s@example.local``
   * - Filtre de compte
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - Attribut memberOf
     - ``memberOf``

Parametres du navigateur
========================

Les parametres du navigateur client sont necessaires pour utiliser l'authentification integree Windows.

Internet Explorer / Microsoft Edge
----------------------------------

1. Ouvrir les Options Internet
2. Selectionner l'onglet "Securite"
3. Cliquer sur "Sites" pour la zone "Intranet local"
4. Cliquer sur "Avance" et ajouter l'URL de Fess
5. Cliquer sur "Personnaliser le niveau" pour la zone "Intranet local"
6. Sous "Authentification utilisateur" -> "Connexion", selectionner "Connexion automatique uniquement dans la zone Intranet"
7. Dans l'onglet "Avance", cocher "Activer l'authentification Windows integree"

Google Chrome
-------------

Chrome utilise generalement les parametres des Options Internet de Windows.
Si une configuration supplementaire est necessaire, definissez ``AuthServerAllowlist`` via la strategie de groupe ou le registre.

Mozilla Firefox
---------------

1. Entrer ``about:config`` dans la barre d'adresse
2. Rechercher ``network.negotiate-auth.trusted-uris``
3. Definir l'URL ou le domaine du serveur Fess (ex: ``https://fess-server.example.local``)

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour un environnement de test.

``app/WEB-INF/conf/system.properties`` :

::

    # Activer SSO
    sso.type=spnego

    # Parametres SPNEGO
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

Configuration recommandee (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandee pour les environnements de production.

``app/WEB-INF/conf/system.properties`` :

::

    # Activer SSO
    sso.type=spnego

    # Parametres SPNEGO
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # Parametres de securite (production)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.allow.localhost=false

Depannage
=========

Problemes courants et solutions
-------------------------------

La boite de dialogue d'authentification apparait
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifiez que le serveur Fess est ajoute a la zone Intranet local dans les parametres du navigateur
- Verifiez que "Activer l'authentification Windows integree" est active
- Verifiez que le SPN est correctement enregistre (``setspn -L <nom d'utilisateur>``)

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifiez que le nom de domaine (majuscules) et le nom du serveur AD dans ``krb5.conf`` sont corrects
- Verifiez que ``spnego.preauth.username`` et ``spnego.preauth.password`` sont corrects
- Verifiez la connectivite reseau vers le serveur AD

Impossible de recuperer les informations de groupe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifiez que les parametres LDAP sont corrects
- Verifiez que le Bind DN et le mot de passe sont corrects
- Verifiez que l'utilisateur appartient a des groupes dans AD

Parametres de debogage
----------------------

Pour investiguer les problemes, vous pouvez afficher des logs detailles lies a SPNEGO en ajustant le niveau de log de |Fess|.

Ajoutez ce qui suit a ``app/WEB-INF/conf/system.properties`` :

::

    spnego.logger.level=1

Ou ajoutez les loggers suivants a ``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>
    <Logger name="org.codelibs.spnego" level="DEBUG"/>

Reference
=========

- :doc:`security-role` - Configuration de la recherche basee sur les roles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-oidc` - Configuration SSO avec authentification OpenID Connect
- :doc:`sso-entraid` - Configuration SSO avec Microsoft Entra ID

