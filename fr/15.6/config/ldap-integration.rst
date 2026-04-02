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

    # Modele de DN de liaison pour l'authentification utilisateur (%s est remplace par le nom d'utilisateur)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # DN de liaison administrateur (compte de service pour les recherches LDAP)
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com

    # Mot de passe de liaison administrateur
    ldap.admin.security.credentials=your_password

Configuration de recherche d'utilisateurs
----------------

::

    # Base DN pour la recherche d'utilisateurs
    ldap.user.search.base=ou=users,dc=example,dc=com

    # Filtre de recherche d'utilisateurs
    ldap.account.filter=(uid={0})

    # Attribut du nom d'utilisateur
    ldap.user.name.attribute=uid

    # Filtre de recherche d'utilisateurs administrateur pour la console de gestion LDAP
    ldap.admin.user.filter=uid=%s

.. note::

   ``ldap.account.filter`` est le filtre de recherche pour l'authentification des utilisateurs,
   tandis que ``ldap.admin.user.filter`` est le filtre de recherche d'utilisateurs pour la
   console de gestion LDAP. Configurez chacun de maniere appropriee car ils ont des objectifs differents.

Configuration des DN de base d'administration LDAP
---------------------------------------------------

::

    # DN de base de recherche d'utilisateurs
    ldap.admin.user.base.dn=ou=People,dc=example,dc=com

    # DN de base de recherche de roles
    ldap.admin.role.base.dn=ou=Roles,dc=example,dc=com

    # DN de base de recherche de groupes
    ldap.admin.group.base.dn=ou=Groups,dc=example,dc=com

Configuration de recherche de groupes
----------------

::

    # Base DN pour la recherche de groupes
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # Filtre de recherche de groupes
    ldap.group.filter=(member={0})

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

    # Modele de DN de liaison pour l'authentification utilisateur (format UPN)
    ldap.security.principal=%s@example.com

    # DN de liaison administrateur (compte de service)
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Recherche d'utilisateurs
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.account.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # Recherche de groupes
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.filter=(member={0})
    ldap.group.name.attribute=cn


Configuration OpenLDAP
============

Exemple de configuration pour OpenLDAP.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Modele de DN de liaison pour l'authentification utilisateur
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # DN de liaison administrateur (compte de service)
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Recherche d'utilisateurs
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.account.filter=(uid={0})
    ldap.user.name.attribute=uid

    # Recherche de groupes
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.filter=(memberUid={0})
    ldap.group.name.attribute=cn

Configuration de securite
================

LDAPS (SSL/TLS)
----------------

Utiliser une connexion chiffree :

::

    # Utiliser LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636


Pour les certificats auto-signes, importez le certificat dans le truststore Java :

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Protection du mot de passe
----------------

Configurer le mot de passe via une variable d'environnement :

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

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
