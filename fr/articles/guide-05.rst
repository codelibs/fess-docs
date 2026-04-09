============================================================================================
Partie 5 : Adapter la recherche aux utilisateurs -- Contrôle des résultats par service et par droits d'accès
============================================================================================

Introduction
============

Dans l'article précédent, nous avons présenté comment intégrer plusieurs sources de données pour effectuer une recherche transversale.
Cependant, une fois la recherche transversale mise en place, un nouveau défi apparaît :
le contrôle des informations « autorisées à être consultées » et des informations « qui ne doivent pas être affichées ».

Il serait problématique que des documents confidentiels du service des ressources humaines apparaissent dans les résultats de recherche de tous les employés.
Dans cet article, nous allons concevoir et mettre en œuvre un contrôle des résultats de recherche en fonction de l'appartenance et des droits d'accès des utilisateurs, en exploitant la recherche par rôle de Fess.

Public visé
===========

- Personnes ayant besoin de contrôler l'accès aux résultats de recherche
- Personnes souhaitant construire une plateforme de recherche tenant compte de la sécurité de l'information en entreprise
- Personnes disposant de connaissances de base sur Active Directory et LDAP

Scénario
========

Une entreprise dispose de trois services.

- **Service commercial** : gère les informations clients, les devis et les propositions commerciales
- **Service développement** : gère les documents de conception, les spécifications du code source et les comptes rendus de réunion
- **Service ressources humaines** : gère les évaluations du personnel, les informations salariales et le règlement intérieur

Il existe également des documents communs accessibles à tous les services (règlement interne, guide des avantages sociaux, etc.).

L'objectif est de fournir l'expérience de recherche suivante :

- Les employés du service commercial peuvent rechercher uniquement les documents du service commercial et les documents communs
- Les employés du service développement peuvent rechercher uniquement les documents du service développement et les documents communs
- Les employés du service ressources humaines peuvent rechercher uniquement les documents du service ressources humaines et les documents communs
- La direction peut rechercher l'ensemble des documents

Fonctionnement de la recherche par rôle
========================================

La recherche par rôle de Fess fonctionne selon le processus suivant :

1. **Lors de l'exploration** : des informations de rôle sont attribuées aux documents (quels rôles peuvent y accéder)
2. **Lors de la connexion** : les informations de rôle de l'utilisateur sont récupérées (authentification interne Fess ou intégration avec un système d'authentification externe)
3. **Lors de la recherche** : seuls les documents correspondant aux rôles de l'utilisateur sont affichés dans les résultats

Ce mécanisme permet d'effectuer le contrôle d'accès au niveau du moteur de recherche.

Conception des rôles
====================

Conception des utilisateurs et des groupes
-------------------------------------------

Commençons par organiser la relation entre utilisateurs, groupes et rôles dans Fess.

.. list-table:: Conception des rôles
   :header-rows: 1
   :widths: 20 30 50

   * - Groupe
     - Rôle
     - Documents accessibles
   * - sales (service commercial)
     - sales_role
     - Documents du service commercial + documents communs
   * - engineering (service développement)
     - engineering_role
     - Documents du service développement + documents communs
   * - hr (service ressources humaines)
     - hr_role
     - Documents du service ressources humaines + documents communs
   * - management (direction)
     - management_role
     - Tous les documents

Configuration des groupes et rôles dans Fess
----------------------------------------------

**Création des rôles**

1. Dans l'écran d'administration, sélectionnez [Utilisateur] > [Rôle]
2. Créez les rôles suivants :

   - ``sales_role``
   - ``engineering_role``
   - ``hr_role``
   - ``management_role``

**Création des groupes**

1. Sélectionnez [Utilisateur] > [Groupe]
2. Créez les groupes suivants :

   - ``sales``
   - ``engineering``
   - ``hr``
   - ``management``

**Création des utilisateurs et attribution des rôles**

1. Sélectionnez [Utilisateur] > [Utilisateur]
2. Attribuez un groupe et un rôle à chaque utilisateur

Attribution des permissions dans la configuration d'exploration
================================================================

Pour attribuer des informations de contrôle d'accès aux documents, spécifiez les permissions dans la configuration d'exploration.
Les permissions s'expriment sous la forme ``{role}nom_du_rôle``, ``{group}nom_du_groupe``, ``{user}nom_utilisateur``, séparées par des retours à la ligne.

Configuration d'exploration par service
-----------------------------------------

**Serveur de fichiers du service commercial**

1. [Explorateur] > [Système de fichiers] > [Nouveau]
2. Configurez les éléments suivants :

   - Chemin : ``smb://fileserver/sales/``
   - Permissions : saisissez ``{role}sales_role`` et ``{role}management_role`` séparés par un retour à la ligne

Avec cette configuration, les documents explorés à partir du serveur de fichiers du service commercial ne seront visibles dans les résultats de recherche que par les utilisateurs possédant les rôles ``sales_role`` et ``management_role``.

**Serveur de fichiers du service développement**

1. [Explorateur] > [Système de fichiers] > [Nouveau]
2. Configurez les éléments suivants :

   - Chemin : ``smb://fileserver/engineering/``
   - Permissions : saisissez ``{role}engineering_role`` et ``{role}management_role`` séparés par un retour à la ligne

**Serveur de fichiers du service ressources humaines**

1. [Explorateur] > [Système de fichiers] > [Nouveau]
2. Configurez les éléments suivants :

   - Chemin : ``smb://fileserver/hr/``
   - Permissions : saisissez ``{role}hr_role`` et ``{role}management_role`` séparés par un retour à la ligne

**Documents communs**

1. [Explorateur] > [Web] ou [Système de fichiers] > [Nouveau]
2. Permissions : laissez la valeur par défaut ``{role}guest``

Par défaut, ``{role}guest`` est automatiquement renseigné. Comme tous les utilisateurs, y compris les utilisateurs invités, possèdent le rôle ``guest``, tous les utilisateurs peuvent consulter ces résultats de recherche.

Intégration avec l'authentification externe
=============================================

Dans un environnement d'entreprise réel, il est courant de vouloir s'intégrer à un service d'annuaire existant plutôt que d'utiliser la gestion interne des utilisateurs de Fess.

Intégration Active Directory / LDAP
-------------------------------------

Fess prend en charge l'intégration LDAP et peut utiliser les informations utilisateur d'Active Directory pour l'authentification et l'attribution des rôles.

Pour activer l'intégration LDAP, configurez les informations de connexion LDAP dans le fichier de configuration de Fess.

Les principaux éléments de configuration sont les suivants :

- URL du serveur LDAP
- DN de liaison (compte de connexion)
- DN de base de recherche des utilisateurs
- DN de base de recherche des groupes
- Mappage des attributs utilisateur

Lorsque l'intégration LDAP est activée, les utilisateurs peuvent se connecter à Fess avec leur compte Active Directory.
Les informations d'appartenance aux groupes sont automatiquement reflétées en tant que rôles, ce qui évite de configurer manuellement les rôles pour chaque utilisateur dans Fess.

Intégration SSO
----------------

Pour une configuration plus avancée, l'intégration avec l'authentification unique (SSO) est également possible.
Fess prend en charge les protocoles SSO suivants :

- **OpenID Connect (OIDC)** : Entra ID (Azure AD), Keycloak, etc.
- **SAML** : intégration avec divers fournisseurs d'identité (IdP)
- **SPNEGO/Kerberos** : authentification intégrée Windows

Grâce à l'intégration SSO, les utilisateurs peuvent accéder automatiquement à Fess avec leurs identifiants habituels, et les informations de rôle sont également reflétées automatiquement.
Les détails de l'intégration SSO seront traités en profondeur dans la Partie 15 « Plateforme de recherche sécurisée ».

Vérification du fonctionnement
===============================

Une fois la configuration de la recherche par rôle terminée, vérifions son fonctionnement.

Procédure de vérification
--------------------------

1. Connectez-vous en tant qu'utilisateur du service commercial et recherchez « devis »
   → Vérifiez que seuls les documents du service commercial et les documents communs s'affichent

2. Connectez-vous en tant qu'utilisateur du service développement et effectuez la même recherche
   → Vérifiez que les documents du service commercial ne s'affichent pas

3. Connectez-vous en tant qu'utilisateur de la direction et effectuez la même recherche
   → Vérifiez que les documents de tous les services s'affichent

Points de vérification
-----------------------

- Les documents pour lesquels l'utilisateur n'a pas les droits ne doivent en aucun cas apparaître dans les résultats de recherche
- Les documents communs doivent s'afficher pour tous les utilisateurs
- Le comportement de la recherche lorsque l'utilisateur n'est pas connecté (périmètre de l'affichage invité)

Considérations de conception
==============================

Granularité des rôles
----------------------

La granularité des rôles est déterminée en fonction de la structure organisationnelle et des exigences de sécurité.

**Granularité large** : rôles définis par service (scénario de cet article)

- Avantage : configuration simple, gestion facile
- Inconvénient : impossible de contrôler finement l'accès au sein d'un service

**Granularité fine** : rôles définis par projet ou par équipe

- Avantage : contrôle d'accès détaillé possible
- Inconvénient : le nombre de rôles augmente et la gestion devient complexe

Il est recommandé de commencer avec une granularité large, puis d'affiner progressivement selon les besoins.

Intégration avec les ACL du serveur de fichiers
-------------------------------------------------

Lors de l'exploration d'un serveur de fichiers, il est également possible d'utiliser les informations ACL (liste de contrôle d'accès) des fichiers pour le contrôle des droits.
Dans ce cas, les paramètres de droits du système de fichiers sont directement reflétés dans le contrôle de l'affichage des résultats de recherche.

Pour exploiter les ACL du serveur de fichiers, vérifiez les éléments de configuration relatifs aux permissions dans la configuration d'exploration.

Conclusion
==========

Dans cet article, nous avons conçu et mis en œuvre un contrôle des résultats de recherche par service en utilisant la recherche par rôle de Fess.

- Conception et enregistrement des rôles, groupes et utilisateurs
- Attribution des rôles dans la configuration d'exploration
- Réflexion automatique des rôles via l'intégration Active Directory / LDAP
- Options d'intégration SSO (OIDC, SAML, SPNEGO)

La recherche par rôle permet de fournir la commodité de la recherche transversale tout en garantissant la sécurité de l'information.
Ceci conclut la section fondamentale. À partir du prochain article, nous aborderons la section solutions pratiques, en traitant de la construction d'un hub de connaissances pour les équipes de développement.

Ressources
==========

- `Configuration des rôles Fess <https://fess.codelibs.org/ja/15.5/admin/role.html>`__

- `Intégration LDAP Fess <https://fess.codelibs.org/ja/15.5/config/ldap.html>`__
