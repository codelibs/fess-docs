==================================
Guide d'integration LDAP
==================================

Apercu
====

|Fess| prend en charge l'integration avec les serveurs LDAP (Lightweight Directory Access Protocol),
permettant l'authentification et la gestion des utilisateurs dans les environnements d'entreprise.

L'integration LDAP permet :

- L'authentification des utilisateurs via Active Directory ou OpenLDAP
- Le controle d'acces base sur les groupes
- La synchronisation automatique des informations utilisateur

Serveurs LDAP pris en charge
================

|Fess| prend en charge l'integration avec les serveurs LDAP suivants :

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Autres serveurs compatibles LDAP v3

Prerequis
========

- Acces reseau au serveur LDAP
- Compte de service pour les recherches LDAP (Bind DN)
- Comprehension de la structure LDAP (Base DN, noms d'attributs, etc.)

Configuration de base
========

Ajoutez les parametres suivants dans ``app/WEB-INF/conf/system.properties``.

Configuration de connexion LDAP
------------

::

    # Activer l'authentification LDAP
    ldap.admin.enabled=true

    # URL du serveur LDAP
    ldap.provider.url=ldap://ldap.example.com:389

    # Pour une connexion securisee (LDAPS)
    # ldap.provider.url=ldaps://ldap.example.com:636

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Bind DN (compte de service)
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # Mot de passe de bind
    ldap.admin.security.credentials=your_password

Configuration de recherche d'utilisateurs
----------------

::

    # Base DN pour la recherche d'utilisateurs
    ldap.user.search.base=ou=users,dc=example,dc=com

    # Filtre de recherche d'utilisateurs
    ldap.user.search.filter=(uid={0})

    # Attribut du nom d'utilisateur
    ldap.user.name.attribute=uid

Configuration de recherche de groupes
----------------

::

    # Base DN pour la recherche de groupes
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # Filtre de recherche de groupes
    ldap.group.search.filter=(member={0})

    # Attribut du nom de groupe
    ldap.group.name.attribute=cn

Configuration Active Directory
====================

Exemple de configuration pour Microsoft Active Directory.

Configuration de base
--------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Compte de service (format UPN)
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # Recherche d'utilisateurs
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # Recherche de groupes
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Configuration specifique a Active Directory
--------------------------

::

    # Resolution des groupes imbriques
    ldap.memberof.enabled=true

    # Utiliser l'attribut memberOf
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

Configuration OpenLDAP
============

Exemple de configuration pour OpenLDAP.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Compte de service
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Recherche d'utilisateurs
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # Recherche de groupes
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
    ldap.group.name.attribute=cn

Configuration de securite
================

LDAPS (SSL/TLS)
----------------

Utiliser une connexion chiffree :

::

    # Utiliser LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

    # Utiliser StartTLS
    ldap.start.tls=true

Pour les certificats auto-signes, importez le certificat dans le truststore Java :

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Protection du mot de passe
----------------

Configurer le mot de passe via une variable d'environnement :

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

Mappage des roles
================

Vous pouvez mapper les groupes LDAP aux roles de |Fess|.

Mappage automatique
--------------

Les noms de groupes sont utilises directement comme noms de roles :

::

    # Groupe LDAP "fess-users" -> Role Fess "fess-users"
    ldap.group.role.mapping.enabled=true

Mappage personnalise
------------------

::

    # Mapper les noms de groupes aux roles
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

Synchronisation des informations utilisateur
==================

Vous pouvez synchroniser les informations utilisateur depuis LDAP vers |Fess|.

Synchronisation automatique
--------

Synchroniser automatiquement les informations utilisateur lors de la connexion :

::

    ldap.user.sync.enabled=true

Attributs a synchroniser
------------

::

    # Adresse email
    ldap.user.email.attribute=mail

    # Nom d'affichage
    ldap.user.displayname.attribute=displayName

Pool de connexions
==============

Configuration du pool de connexions pour ameliorer les performances :

::

    # Activer le pool de connexions
    ldap.connection.pool.enabled=true

    # Nombre minimum de connexions
    ldap.connection.pool.min=1

    # Nombre maximum de connexions
    ldap.connection.pool.max=10

    # Timeout de connexion (millisecondes)
    ldap.connection.timeout=5000

Basculement
================

Basculement vers plusieurs serveurs LDAP :

::

    # Specifier plusieurs URL separees par des espaces
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Depannage
======================

Erreur de connexion
----------

**Symptome** : Echec de connexion au serveur LDAP

**Points a verifier** :

1. Verifier si le serveur LDAP est en cours d'execution
2. Verifier si le port est ouvert dans le pare-feu (389 ou 636)
3. Verifier si l'URL est correcte (``ldap://`` ou ``ldaps://``)
4. Verifier si le Bind DN et le mot de passe sont corrects

Erreur d'authentification
----------

**Symptome** : Echec de l'authentification utilisateur

**Points a verifier** :

1. Verifier si le filtre de recherche d'utilisateurs est correct
2. Verifier si l'utilisateur existe dans le Base DN de recherche
3. Verifier si l'attribut du nom d'utilisateur est correct

Les groupes ne sont pas recuperes
----------------------

**Symptome** : Les groupes de l'utilisateur ne sont pas recuperes

**Points a verifier** :

1. Verifier si le filtre de recherche de groupes est correct
2. Verifier si l'attribut d'appartenance au groupe est correct
3. Verifier si les groupes existent dans le Base DN de recherche

Configuration de debogage
------------

Afficher des logs detailles :

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Informations de reference
========

- :doc:`security-role` - Controle d'acces base sur les roles
- :doc:`sso-spnego` - Authentification SPNEGO (Kerberos)
- :doc:`../admin/user-guide` - Guide de gestion des utilisateurs
