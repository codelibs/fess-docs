========
Général
=======

Présentation
============

Cette page d'administration vous permet de gérer les paramètres de |Fess|.
Vous pouvez modifier divers paramètres de |Fess| sans redémarrer |Fess|.

|image0|

Contenu de la configuration
===========================

Système
-------

Réponse JSON
::::::::::::

Spécifie s'il faut activer l'API JSON.

Connexion requise
:::::::::::::::::

Spécifie si la connexion est requise pour la fonction de recherche.

Afficher le lien de connexion
::::::::::::::::::::::::::::::

Configure l'affichage du lien vers la page de connexion sur l'écran de recherche.

Réduire les résultats en double
::::::::::::::::::::::::::::::::

Configure l'activation de la réduction des résultats en double.

Afficher la miniature
:::::::::::::::::::::

Configure l'activation de l'affichage des vignettes.

Valeur d'étiquette par défaut
::::::::::::::::::::::::::::::

Décrit la valeur d'étiquette à ajouter aux critères de recherche par défaut.
Pour spécifier par rôle ou groupe, ajoutez « role: » ou « group: » comme « role:admin=label1 ».

Valeur de tri par défaut
:::::::::::::::::::::::::

Décrit la valeur de tri à ajouter aux critères de recherche par défaut.
Pour spécifier par rôle ou groupe, ajoutez « role: » ou « group: » comme « role:admin=content_length.desc ».

Hôte virtuel
::::::::::::

Configure l'hôte virtuel.
Pour plus de détails, consultez :doc:`Configuration de l'hôte virtuel dans le guide de configuration <../config/security-virtual-host>`.

Réponse de mot populaire
::::::::::::::::::::::::

Spécifie s'il faut activer l'API des mots populaires.

Encodage du fichier CSV
::::::::::::::::::::::::

Spécifie l'encodage des fichiers CSV à télécharger.

Ajouter des paramètres de recherche
::::::::::::::::::::::::::::::::::::

Active le passage de paramètres à l'affichage des résultats de recherche.

Proxy de fichier de recherche
:::::::::::::::::::::::::::::

Spécifie s'il faut activer le proxy de fichier pour les résultats de recherche.

Utiliser les paramètres régionaux du navigateur
::::::::::::::::::::::::::::::::::::::::::::::::

Spécifie s'il faut utiliser les paramètres régionaux du navigateur pour la recherche.

Type de SSO
:::::::::::

Spécifie le type d'authentification unique (Single Sign-On).

- **Aucun** : Ne pas utiliser le SSO
- **OpenID Connect** : Utiliser OpenID Connect
- **SAML** : Utiliser SAML
- **SPNEGO** : Utiliser SPNEGO
- **Entra ID** : Utiliser Microsoft Entra ID

Robot d'exploration
-------------------

Vérifier la dernière modification
::::::::::::::::::::::::::::::::::

Active le crawl différentiel.

Configuration du robot d'exploration simultané
:::::::::::::::::::::::::::::::::::::::::::::::

Spécifie le nombre de configurations de crawl à exécuter simultanément.

Agent utilisateur
:::::::::::::::::

Spécifie le nom de l'agent utilisateur utilisé par le robot d'exploration.

Supprimer les anciens documents
::::::::::::::::::::::::::::::::

Spécifie le nombre de jours de la période de validité après l'indexation.

Ignorer les types d'échec
:::::::::::::::::::::::::

Les URL en échec qui dépassent le seuil sont exclues des cibles de crawl, mais les noms d'exception spécifiés ici seront des cibles de crawl même si elles dépassent le seuil.

Seuil de nombre d'échecs
::::::::::::::::::::::::

Si le document cible de crawl est enregistré dans les URL en échec plus que le nombre de fois spécifié ici, il sera exclu du prochain crawl.

Journalisation
--------------

Journal de recherche
::::::::::::::::::::

Spécifie s'il faut activer l'enregistrement du journal de recherche.

Journal utilisateur
:::::::::::::::::::

Spécifie s'il faut activer l'enregistrement du journal utilisateur.

Journal des favoris
:::::::::::::::::::

Spécifie s'il faut activer l'enregistrement du journal des favoris.

Supprimer les anciens journaux de recherche
:::::::::::::::::::::::::::::::::::::::::::

Supprime les journaux de recherche antérieurs au nombre de jours spécifié.

Supprimer les anciens journaux de tâches
::::::::::::::::::::::::::::::::::::::::

Supprime les journaux de tâches antérieurs au nombre de jours spécifié.

Supprimer les anciens journaux utilisateur
::::::::::::::::::::::::::::::::::::::::::

Supprime les journaux utilisateur antérieurs au nombre de jours spécifié.

Noms de robots pour supprimer les journaux
:::::::::::::::::::::::::::::::::::::::::::

Spécifie le nom du bot à exclure des journaux de recherche.

Niveau de journalisation
:::::::::::::::::::::::::

Spécifie le niveau de journalisation de fess.log.

Notification des journaux
:::::::::::::::::::::::::

Spécifie s'il faut activer la fonction de notification des journaux qui capture automatiquement les événements de niveau ERROR et WARN et envoie des notifications.
Pour plus de détails, consultez :doc:`Configuration des notifications de journaux <../config/admin-log-notification>`.

Niveau de notification des journaux
::::::::::::::::::::::::::::::::::::

Spécifie le niveau de journalisation pour les notifications.
Les événements de journalisation au niveau sélectionné et au-dessus seront notifiés.

- **ERROR** : Notifier uniquement les erreurs (par défaut)
- **WARN** : Notifier les avertissements et au-dessus
- **INFO** : Notifier les informations et au-dessus
- **DEBUG** : Notifier le débogage et au-dessus
- **TRACE** : Notifier tous les journaux

Suggérer
--------

Suggérer à partir des termes de recherche
::::::::::::::::::::::::::::::::::::::::::

Spécifie s'il faut générer des candidats de suggestion à partir des journaux de recherche.

Suggérer à partir des documents
::::::::::::::::::::::::::::::::

Spécifie s'il faut générer des candidats de suggestion à partir des documents indexés.

Supprimer les anciennes informations de suggestion
:::::::::::::::::::::::::::::::::::::::::::::::::::

Supprime les données de suggestion antérieures au nombre de jours spécifié.

LDAP
----

URL LDAP
::::::::

Spécifie l'URL du serveur LDAP.

DN de base
::::::::::

Spécifie le nom distinctif de base pour se connecter à l'écran de recherche.

DN de liaison
:::::::::::::

Spécifie le DN de liaison de l'administrateur.

Mot de passe
::::::::::::

Spécifie le mot de passe du DN de liaison.

DN de l'utilisateur
:::::::::::::::::::

Spécifie le nom distinctif de l'utilisateur.

Filtre de compte
::::::::::::::::

Spécifie le nom commun de l'utilisateur, l'uid, etc.

Filtre de groupe
::::::::::::::::

Spécifie les conditions de filtre pour les groupes à récupérer.

Attribut memberOf
:::::::::::::::::

Spécifie le nom de l'attribut memberOf disponible sur le serveur LDAP.
Pour Active Directory, c'est memberOf.
Pour d'autres serveurs LDAP, cela peut être isMemberOf.

Authentification de sécurité
::::::::::::::::::::::::::::

Spécifie la méthode d'authentification de sécurité LDAP (ex. : simple).

Fabrique de contexte initial
:::::::::::::::::::::::::::::

Spécifie la classe de fabrique de contexte initial LDAP (ex. : com.sun.jndi.ldap.LdapCtxFactory).

OpenID Connect
--------------

ID client
:::::::::

Spécifie l'ID client du fournisseur OpenID Connect.

Secret client
:::::::::::::

Spécifie le secret client du fournisseur OpenID Connect.

URL du serveur d'autorisation
::::::::::::::::::::::::::::::

Spécifie l'URL du serveur d'autorisation pour OpenID Connect.

URL du serveur de jetons
::::::::::::::::::::::::

Spécifie l'URL du serveur de jetons pour OpenID Connect.

URL de redirection
::::::::::::::::::

Spécifie l'URL de redirection pour OpenID Connect.

Portée
::::::

Spécifie la portée pour OpenID Connect.

URL de base
:::::::::::

Spécifie l'URL de base pour OpenID Connect.

Groupes par défaut
::::::::::::::::::

Spécifie les groupes par défaut à attribuer aux utilisateurs lors de l'authentification OpenID Connect.

Rôles par défaut
::::::::::::::::

Spécifie les rôles par défaut à attribuer aux utilisateurs lors de l'authentification OpenID Connect.

SAML
----

URL de base du SP
:::::::::::::::::

Spécifie l'URL de base du fournisseur de services SAML.

Nom d'attribut de groupe
::::::::::::::::::::::::

Spécifie le nom d'attribut pour récupérer les groupes de la réponse SAML.

Nom d'attribut de rôle
::::::::::::::::::::::

Spécifie le nom d'attribut pour récupérer les rôles de la réponse SAML.

Groupes par défaut
::::::::::::::::::

Spécifie les groupes par défaut à attribuer aux utilisateurs lors de l'authentification SAML.

Rôles par défaut
::::::::::::::::

Spécifie les rôles par défaut à attribuer aux utilisateurs lors de l'authentification SAML.

SPNEGO
------

Configuration Krb5
:::::::::::::::::::

Spécifie le chemin vers le fichier de configuration Kerberos 5.

Configuration de connexion
::::::::::::::::::::::::::

Spécifie le chemin vers le fichier de configuration de connexion JAAS (Java Authentication and Authorization Service).

Module client de connexion
::::::::::::::::::::::::::

Spécifie le nom du module de connexion client JAAS.

Module serveur de connexion
:::::::::::::::::::::::::::

Spécifie le nom du module de connexion serveur JAAS.

Nom d'utilisateur de pré-authentification
::::::::::::::::::::::::::::::::::::::::::

Spécifie le nom d'utilisateur pour la pré-authentification SPNEGO.

Mot de passe de pré-authentification
:::::::::::::::::::::::::::::::::::::

Spécifie le mot de passe pour la pré-authentification SPNEGO.

Autoriser l'authentification Basic
:::::::::::::::::::::::::::::::::::

Spécifie s'il faut autoriser l'authentification Basic comme solution de repli.

Autoriser l'authentification Basic non sécurisée
:::::::::::::::::::::::::::::::::::::::::::::::::

Spécifie s'il faut autoriser l'authentification Basic sur les connexions non sécurisées (HTTP).

Invite NTLM
::::::::::::

Spécifie s'il faut activer l'invite NTLM.

Autoriser localhost
:::::::::::::::::::

Spécifie s'il faut autoriser l'accès depuis localhost.

Autoriser la délégation
:::::::::::::::::::::::

Spécifie s'il faut autoriser la délégation Kerberos.

Répertoires exclus
::::::::::::::::::

Spécifie les répertoires à exclure de l'authentification SPNEGO.

Entra ID
--------

ID client
:::::::::

Spécifie l'ID d'application (client) pour Microsoft Entra ID.

Secret client
:::::::::::::

Spécifie le secret client pour Microsoft Entra ID.

Locataire
:::::::::

Spécifie l'ID du locataire pour Microsoft Entra ID.

Autorité
::::::::

Spécifie l'URL de l'autorité pour Microsoft Entra ID.

URL de réponse
::::::::::::::

Spécifie l'URL de réponse (redirection) pour Microsoft Entra ID.

TTL de l'état
:::::::::::::

Spécifie la durée de vie (TTL) de l'état d'authentification.

Groupes par défaut
::::::::::::::::::

Spécifie les groupes par défaut à attribuer aux utilisateurs lors de l'authentification Entra ID.

Rôles par défaut
::::::::::::::::

Spécifie les rôles par défaut à attribuer aux utilisateurs lors de l'authentification Entra ID.

Champs de permissions
:::::::::::::::::::::

Spécifie les champs pour récupérer les informations de permissions depuis Entra ID.

Utiliser le service de domaine
:::::::::::::::::::::::::::::::

Spécifie s'il faut utiliser le service de domaine Entra ID.

Avis
----

Page de connexion
:::::::::::::::::

Décrit le message à afficher sur l'écran de connexion.

Page d'accueil de la recherche
::::::::::::::::::::::::::::::

Décrit le message à afficher sur l'écran d'accueil de recherche.

Page de recherche avancée
:::::::::::::::::::::::::

Décrit le message à afficher sur l'écran de recherche avancée.

Notification
------------

E-mail de notification
::::::::::::::::::::::

Spécifie l'adresse e-mail pour la notification à la fin du crawl.
Plusieurs adresses peuvent être spécifiées séparées par des virgules. Un serveur de messagerie est requis pour l'utilisation.

Slack Webhook URL
:::::::::::::::::

Spécifie l'URL du webhook pour les notifications Slack.

Google Chat Webhook URL
:::::::::::::::::::::::

Spécifie l'URL du webhook pour les notifications Google Chat.

Stockage
--------

Après avoir configuré chaque élément, un menu [Système > Stockage] apparaîtra dans le menu de gauche.
Pour la gestion des fichiers, consultez :doc:`Stockage <../admin/storage-guide>`.

Type
::::

Spécifie le type de stockage.
Lorsque « Automatique » est sélectionné, le type de stockage est automatiquement déterminé à partir du point de terminaison.

- **Automatique** : Détection automatique à partir du point de terminaison
- **S3** : Amazon S3
- **GCS** : Google Cloud Storage

Compartiment
::::::::::::

Spécifie le nom du compartiment à gérer.

Point de terminaison
::::::::::::::::::::

Spécifie l'URL du point de terminaison du serveur de stockage.

- S3 : Utilise le point de terminaison AWS par défaut si vide
- GCS : Utilise le point de terminaison Google Cloud par défaut si vide
- MinIO, etc. : L'URL du point de terminaison du serveur MinIO

Clé d'accès
:::::::::::

Spécifie la clé d'accès pour S3 ou le stockage compatible S3.

Clé secrète
:::::::::::

Spécifie la clé secrète pour S3 ou le stockage compatible S3.

Région
::::::

Spécifie la région S3 (ex. : ap-northeast-1).

ID de projet
::::::::::::

Spécifie l'ID de projet Google Cloud pour GCS.

Chemin des identifiants
:::::::::::::::::::::::

Spécifie le chemin vers le fichier JSON d'identifiants du compte de service pour GCS.

Exemples
========

Exemples de configuration LDAP
------------------------------

.. tabularcolumns:: |p{4cm}|p{4cm}|p{4cm}|
.. list-table:: Configuration LDAP/Active Directory
   :header-rows: 1

   * - Nom
     - Valeur (LDAP)
     - Valeur (Active Directory)
   * - URL LDAP
     - ldap://SERVERNAME:389
     - ldap://SERVERNAME:389
   * - DN de base
     - cn=Directory Manager
     - dc=fess,dc=codelibs,dc=org
   * - DN de liaison
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - manager@fess.codelibs.org
   * - DN de l'utilisateur
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - %s@fess.codelibs.org
   * - Filtre de compte
     - cn=%s ou uid=%s
     - (&(objectClass=user)(sAMAccountName=%s))
   * - Filtre de groupe
     -
     - (member:1.2.840.113556.1.4.1941:=%s)
   * - memberOf
     - isMemberOf
     - memberOf


.. |image0| image:: ../../../resources/images/en/15.6/admin/general-1.png
.. pdf            :height: 940 px
