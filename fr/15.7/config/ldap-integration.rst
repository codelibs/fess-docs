=====================================
Guide d'intégration LDAP
=====================================

Aperçu
======

|Fess| prend en charge l'intégration avec les serveurs LDAP (Lightweight Directory Access Protocol),
permettant l'authentification et la gestion des utilisateurs dans les environnements d'entreprise.

L'intégration LDAP permet :

- L'authentification des utilisateurs via Active Directory ou OpenLDAP (connexion)
- Le contrôle d'accès basé sur les groupes et les rôles
- La gestion des utilisateurs/rôles/groupes LDAP depuis la console d'administration (optionnel)

Serveurs LDAP pris en charge
=============================

|Fess| prend en charge l'intégration avec les serveurs LDAP suivants :

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Autres serveurs compatibles LDAP v3

Prérequis
=========

- Accès réseau au serveur LDAP
- Compte de service pour les recherches LDAP (Bind DN)
- Compréhension de la structure LDAP (Base DN, noms d'attributs, etc.)

Vue d'ensemble de la configuration
====================================

La configuration LDAP de |Fess| est gérée à deux endroits distincts selon l'usage.

Paramètres de connexion et d'authentification (console d'administration / ``system.properties``)
   Ces paramètres concernent la connexion au serveur LDAP et l'authentification lors de la connexion.
   Ils peuvent être configurés depuis la section « LDAP » de la page **« Système > Général »** de la
   console d'administration et sont enregistrés dans ``app/WEB-INF/conf/system.properties``.

Paramètres de gestion LDAP et de comportement (``fess_config.properties``)
   Ces paramètres concernent les fonctionnalités de gestion des utilisateurs/rôles/groupes LDAP
   depuis la console d'administration, ainsi que les comportements tels que la résolution des rôles.
   Ils sont définis dans ``app/WEB-INF/classes/fess_config.properties`` ; pour les modifier,
   éditez ce fichier directement.

.. note::

   Si vous utilisez uniquement l'authentification lors de la connexion, les « Paramètres de connexion
   et d'authentification » suffisent. La « Gestion LDAP » (``ldap.admin.enabled``) n'est nécessaire
   que si vous souhaitez créer, mettre à jour ou supprimer des utilisateurs/rôles/groupes LDAP
   depuis la console d'administration.

Paramètres de connexion et d'authentification
==============================================

Ces paramètres peuvent être configurés depuis la section LDAP de la console d'administration
« Système > Général » et sont enregistrés dans ``app/WEB-INF/conf/system.properties``.
Vous pouvez également modifier ce fichier directement.

.. list-table:: Propriétés de connexion et d'authentification
   :header-rows: 1
   :widths: 30 15 55

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``ldap.provider.url``
     - (aucune)
     - URL du serveur LDAP. Exemple : ``ldap://ldap.example.com:389``. Pour LDAPS : ``ldaps://ldap.example.com:636``. Plusieurs URL séparées par des espaces permettent le basculement (failover).
   * - ``ldap.base.dn``
     - (aucune)
     - Base DN pour les recherches LDAP. Exemple : ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - (aucune)
     - Modèle de DN de liaison pour l'authentification des utilisateurs. ``%s`` est remplacé par le nom d'utilisateur. Exemple : ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - Méthode d'authentification LDAP (``java.naming.security.authentication`` de JNDI). Généralement ``simple``.
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - Classe de fabrique de contexte initial JNDI. Généralement aucune modification requise.
   * - ``ldap.admin.security.principal``
     - (aucune)
     - Bind DN du compte de service pour les recherches LDAP. Exemple : ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - (aucune)
     - Mot de passe du compte de service ci-dessus.
   * - ``ldap.account.filter``
     - (aucune)
     - Filtre utilisé pour rechercher l'entrée de l'utilisateur lors de la résolution de ses rôles. ``%s`` est remplacé par le nom d'utilisateur. Exemple : ``uid=%s``
   * - ``ldap.group.filter``
     - (vide)
     - Filtre de recherche utilisé lors de la résolution des groupes. ``%s`` est remplacé par le DN de l'utilisateur, etc. Exemple : ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - Nom de l'attribut représentant l'appartenance à un groupe. Utilisé pour résoudre les rôles sur Active Directory et les serveurs disposant de cet attribut.

Exemple de configuration (édition directe de ``system.properties``) :

::

    # URL du serveur LDAP
    ldap.provider.url=ldap://ldap.example.com:389

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Modèle de DN de liaison pour l'authentification utilisateur (%s est remplacé par le nom d'utilisateur)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Bind DN et mot de passe du compte de service pour les recherches
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtres pour la résolution des rôles
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   Le paramètre fictif ``%s`` est traité par ``String.format()`` de Java.
   ``ldap.security.principal``, ``ldap.account.filter``, ``ldap.group.filter`` et
   les filtres d'administration utilisent tous le format ``%s`` (et non le format ``{0}``).
   Le nom d'utilisateur transmis aux filtres est automatiquement échappé en interne par
   |Fess| pour se prémunir contre les injections LDAP.

Paramètres de gestion LDAP et de comportement
===============================================

Les propriétés suivantes sont définies dans ``app/WEB-INF/classes/fess_config.properties``.
Pour les modifier, éditez ce fichier.

Activation des fonctionnalités d'administration
------------------------------------------------

.. list-table:: Propriétés des fonctionnalités d'administration
   :header-rows: 1
   :widths: 35 15 50

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``ldap.admin.enabled``
     - ``false``
     - Active la fonctionnalité de création, mise à jour et suppression des utilisateurs/rôles/groupes LDAP depuis la console d'administration. **Non requis pour l'authentification lors de la connexion** ; la connexion via LDAP fonctionne même sans activer cette option.
   * - ``ldap.admin.sync.password``
     - ``true``
     - Synchronise le mot de passe côté |Fess| avec LDAP lors de la mise à jour d'un utilisateur depuis la console d'administration.
   * - ``ldap.auth.validation``
     - ``true``
     - Effectue la validation de l'authentification LDAP lors de la connexion.

Filtres et Base DN pour la gestion des utilisateurs/rôles/groupes
------------------------------------------------------------------

Utilisés pour manipuler les entrées LDAP depuis la console d'administration lorsque
``ldap.admin.enabled=true``.

.. list-table:: Filtres et Base DN d'administration
   :header-rows: 1
   :widths: 38 47 15

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``ldap.admin.user.filter``
     - Filtre de recherche des utilisateurs (``%s`` est remplacé par le nom d'utilisateur)
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - Base DN de recherche des utilisateurs
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - objectClass lors de la création d'un utilisateur
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - Filtre de recherche des rôles
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - Base DN de recherche des rôles
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - objectClass lors de la création d'un rôle
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - Filtre de recherche des groupes
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - Base DN de recherche des groupes
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - objectClass lors de la création d'un groupe
     - ``groupOfNames``

Contrôle de la résolution des rôles et du comportement
-------------------------------------------------------

Contrôle le comportement de la résolution des rôles/groupes après la connexion.

.. list-table:: Propriétés de contrôle du comportement
   :header-rows: 1
   :widths: 40 15 45

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - Attribue des rôles basés sur le nom d'utilisateur.
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - Attribue des rôles basés sur les groupes.
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - Attribue des rôles basés sur les rôles.
   * - ``ldap.allow.empty.permission``
     - ``true``
     - Autorise la connexion des utilisateurs sans groupe ni rôle.
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - Supprime le nom NetBIOS (préfixe de la forme ``DOMAIN\``) des noms de groupes, etc.
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - Autorise les caractères de soulignement dans les noms de groupes.
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - Convertit les noms de permissions en minuscules.
   * - ``ldap.samaccountname.group``
     - ``false``
     - Utilise l'attribut ``sAMAccountName`` pour les noms de groupes (pour Active Directory).
   * - ``ldap.max.username.length``
     - ``-1``
     - Longueur maximale du nom d'utilisateur. ``-1`` signifie sans limite.

Correspondance des attributs
-----------------------------

La correspondance entre les attributs LDAP et les attributs utilisateur de |Fess| est définie
par les propriétés ``ldap.attr.*``. En général, aucune modification n'est nécessaire, mais
vous pouvez les ajuster si le schéma diffère. Exemples représentatifs :

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   Certaines propriétés ne correspondent pas au nom de l'attribut LDAP, par exemple
   ``ldap.attr.state`` est mappé sur ``st`` et ``ldap.attr.city`` sur ``l``.
   Pour la liste complète, consultez les lignes commençant par ``ldap.attr.``
   dans ``fess_config.properties``.

Configuration Active Directory
===============================

Exemple de configuration pour Microsoft Active Directory (``system.properties`` ou console d'administration).

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Modèle de DN de liaison pour l'authentification utilisateur (format UPN)
    ldap.security.principal=%s@example.com

    # Compte de service pour les recherches
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtre de compte
    ldap.account.filter=sAMAccountName=%s

    # Utilisation de l'attribut memberOf
    ldap.memberof.attribute=memberOf

    # Filtre de groupe
    ldap.group.filter=(member=%s)

Pour résoudre les groupes imbriqués, vous pouvez utiliser la règle de correspondance
``LDAP_MATCHING_RULE_IN_CHAIN`` spécifique à Active Directory.

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

Configuration OpenLDAP
=======================

Exemple de configuration pour OpenLDAP.

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Modèle de DN de liaison pour l'authentification utilisateur
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Compte de service pour les recherches
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtre de compte
    ldap.account.filter=uid=%s

    # Filtre de groupe (pour posixGroup)
    ldap.group.filter=(memberUid=%s)

.. note::

   OpenLDAP standard ne possède pas l'attribut ``memberOf`` ; les groupes sont donc
   résolus via ``ldap.group.filter``. Si l'overlay ``memberof`` est activé,
   ``ldap.memberof.attribute`` peut également être utilisé.

Paramètres de sécurité
=======================

LDAPS (SSL/TLS)
---------------

Utiliser une connexion chiffrée :

::

    # Utiliser LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

Pour les certificats auto-signés, importez le certificat dans le truststore Java.

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Protection du mot de passe
---------------------------

``ldap.admin.security.credentials`` est enregistré dans ``system.properties``.
Les informations d'identification configurées depuis la console d'administration
sont stockées chiffrées en interne. Veillez à restreindre les droits d'accès
au fichier de manière appropriée.

Basculement (Failover)
=======================

Pour basculer vers plusieurs serveurs LDAP, spécifiez plusieurs URL séparées par
des espaces dans ``ldap.provider.url``.

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Dépannage
==========

Erreur de connexion
--------------------

**Symptôme** : Échec de la connexion au serveur LDAP

**Points à vérifier** :

1. Le serveur LDAP est-il démarré ?
2. Le port est-il ouvert dans le pare-feu (389 ou 636) ?
3. ``ldap.provider.url`` est-il correct (``ldap://`` ou ``ldaps://``) ?
4. ``ldap.admin.security.principal`` et le mot de passe sont-ils corrects ?

Erreur d'authentification
--------------------------

**Symptôme** : Échec de l'authentification utilisateur

**Points à vérifier** :

1. Le modèle de ``ldap.security.principal`` est-il correct (contient-il ``%s``) ?
2. L'utilisateur existe-t-il dans le Base DN spécifié ?
3. ``ldap.account.filter`` est-il correct ?

Impossibilité de récupérer les groupes/rôles
---------------------------------------------

**Symptôme** : Les groupes et rôles de l'utilisateur ne peuvent pas être récupérés

**Points à vérifier** :

1. ``ldap.group.filter`` est-il correct ?
2. ``ldap.memberof.attribute`` est-il correct (pour Active Directory) ?
3. Les groupes existent-ils dans le Base DN de recherche ?
4. Les propriétés ``ldap.role.search.*.enabled`` sont-elles activées ?

Impossibilité de gérer les utilisateurs depuis la console d'administration
---------------------------------------------------------------------------

**Symptôme** : Impossible de créer, modifier ou supprimer des utilisateurs LDAP depuis la console d'administration

**Points à vérifier** :

1. ``ldap.admin.enabled`` est-il défini à ``true`` ?
2. Les Base DN d'administration tels que ``ldap.admin.user.base.dn`` sont-ils corrects ?
3. Le compte de service ``ldap.admin.security.principal`` dispose-t-il des droits en écriture ?

Configuration du débogage
--------------------------

Pour afficher des journaux détaillés, ajoutez un logger dans ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Informations de référence
==========================

- :doc:`security-role` - Contrôle d'accès basé sur les rôles
- :doc:`sso-spnego` - Authentification SPNEGO (Kerberos)
- :doc:`../admin/user-guide` - Guide de gestion des utilisateurs
