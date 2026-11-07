=================================================
Partie 15 : Infrastructure de recherche sécurisée
=================================================

Introduction
=============

Les exigences en matière de sécurité de l'information dans les entreprises deviennent chaque année plus strictes.
Étant donné que les systèmes de recherche agrègent un grand volume de documents confidentiels, des mécanismes d'authentification et d'autorisation adéquats sont indispensables.

Dans cet article, nous approfondissons la recherche basée sur les rôles présentée dans la Partie 5 et concevons une architecture de sécurité centrée sur l'intégration SSO (authentification unique).

Public cible
=============

- Personnes exploitant Fess dans un environnement d'entreprise
- Personnes concevant l'intégration SSO (OIDC, SAML)
- Personnes comprenant les concepts de sécurité Zero Trust

Organisation des exigences de sécurité
=========================================

Nous organisons ci-dessous les exigences de sécurité typiques des entreprises.

.. list-table:: Exigences de sécurité
   :header-rows: 1
   :widths: 30 70

   * - Exigence
     - Description
   * - Authentification unique
     - S'intégrer à un IdP existant pour supprimer les opérations de connexion supplémentaires
   * - Accès basé sur les rôles
     - Contrôler les résultats de recherche en fonction de l'affiliation et des permissions de l'utilisateur
   * - Chiffrement des communications
     - Chiffrer toutes les communications via HTTPS
   * - Contrôle d'accès à l'API
     - Authentification API basée sur des jetons et gestion des permissions
   * - Journaux d'audit
     - Enregistrer qui a recherché quoi

Options d'intégration SSO
============================

Nous présentons ci-dessous les protocoles SSO pris en charge par Fess et les scénarios dans lesquels chacun est applicable.

.. list-table:: Comparaison des protocoles SSO
   :header-rows: 1
   :widths: 20 30 50

   * - Protocole
     - IdPs représentatifs
     - Scénarios d'application
   * - OpenID Connect
     - Entra ID, Keycloak, Google
     - Environnements cloud, infrastructure d'authentification moderne
   * - SAML 2.0
     - Entra ID, Okta, OneLogin
     - Environnements d'entreprise, lorsqu'un IdP SAML existant est disponible
   * - SPNEGO/Kerberos
     - Active Directory
     - Environnements d'authentification intégrée Windows

Intégration SSO via OpenID Connect / Entra ID
================================================

Il s'agit de l'approche la plus moderne et recommandée.
En plus de l'intégration générique OpenID Connect, Fess fournit également une fonctionnalité d'intégration dédiée pour Entra ID (Azure AD).
Nous expliquons ici l'intégration en prenant Entra ID comme exemple.

Aperçu du flux d'authentification
-----------------------------------

1. Un utilisateur accède à Fess
2. Fess redirige l'utilisateur vers l'écran d'authentification d'Entra ID
3. L'utilisateur s'authentifie auprès d'Entra ID (y compris la MFA)
4. Entra ID renvoie un jeton d'authentification à Fess
5. Fess récupère les informations utilisateur et les informations de groupe à partir du jeton
6. Les rôles sont attribués en fonction des informations de groupe
7. Les résultats de recherche sont fournis en fonction des rôles

Configuration côté Entra ID
-----------------------------

1. Enregistrez une application dans Entra ID
2. Configurez l'URI de redirection (URL de callback OIDC de Fess)
3. Accordez les permissions API requises (User.Read, GroupMember.Read.All, etc.)
4. Obtenez l'ID client et le secret

Configuration côté Fess
-------------------------

Configurez les informations de connexion SSO sur la page [Système] > [Général] de la console d'administration.
Les principaux éléments de configuration sont les suivants :

- URL du fournisseur OpenID Connect (point de terminaison Entra ID)
- ID client
- Secret client
- Portées (openid, profile, email, etc.)
- Paramètres des revendications de groupe

Correspondance entre groupes et rôles
----------------------------------------

Associez les groupes Entra ID aux rôles Fess.
Cela permet à la gestion des groupes dans Entra ID d'être directement reflétée dans le contrôle des résultats de recherche.

Exemple : Groupe Entra ID « Engineering » -> Rôle Fess « engineering_role »

Intégration SSO via SAML
==========================

L'intégration SAML est adaptée aux environnements disposant d'un IdP SAML existant.

Aperçu du flux d'authentification
-----------------------------------

Avec SAML, des SAML Assertions sont échangées entre le SP (Service Provider = Fess) et l'IdP.

1. Un utilisateur accède à Fess
2. Fess envoie un SAML AuthnRequest à l'IdP
3. L'IdP authentifie l'utilisateur
4. L'IdP renvoie une SAML Response (contenant les attributs utilisateur) à Fess
5. Fess attribue des rôles en fonction des attributs utilisateur

Configuration côté Fess
-------------------------

Les paramètres suivants sont nécessaires pour l'intégration SAML :

- URL des métadonnées ou fichier XML de l'IdP
- ID d'entité du SP
- Assertion Consumer Service URL
- Correspondance des attributs (nom d'utilisateur, adresse e-mail, groupes)

Intégration SPNEGO / Kerberos
================================

Dans les environnements Windows Active Directory, l'authentification intégrée Windows via SPNEGO/Kerberos peut être utilisée.
Lors de l'accès via un navigateur depuis un PC membre du domaine, l'authentification s'effectue automatiquement sans opération de connexion supplémentaire.

Cette méthode est la plus transparente pour les utilisateurs, mais la configuration est la plus complexe.
Un environnement de domaine Active Directory est un prérequis.

Chiffrement des communications
=================================

Configuration SSL/TLS
----------------------

Dans les environnements de production, il est recommandé d'effectuer tous les accès à Fess via HTTPS.

**Méthode par proxy inverse (recommandée)**

Déployez Nginx ou Apache HTTP Server comme proxy inverse pour effectuer la terminaison SSL.
Fess lui-même fonctionne en HTTP, et le proxy inverse gère le HTTPS.

::

    [Client] --HTTPS--> [Nginx] --HTTP--> [Fess]

L'avantage de cette méthode est que la gestion des certificats est centralisée au niveau du proxy inverse.

**Méthode de configuration directe de Fess**

Il est également possible de configurer les certificats SSL directement dans le Tomcat de Fess.
Cette méthode est adaptée aux environnements de petite taille ou lorsqu'aucun proxy inverse n'est déployé.

Sécurité de l'accès à l'API
==============================

Nous renforçons ci-dessous la sécurité de l'intégration API présentée dans la Partie 11.

Conception des permissions des jetons
----------------------------------------

Configurez les permissions appropriées pour les jetons d'accès.

.. list-table:: Exemple de conception de jetons
   :header-rows: 1
   :widths: 25 25 50

   * - Utilisation
     - Permissions
     - Remarques
   * - Widget de recherche
     - Recherche uniquement (lecture seule)
     - Utilisé côté frontend
   * - Traitement par lots
     - Recherche + Indexation
     - Utilisé côté serveur
   * - Automatisation de l'administration
     - Accès à l'API d'administration
     - Utilisé dans les scripts d'exploitation

Gestion des jetons
-------------------

- Rotation régulière (tous les 3 à 6 mois)
- Révocation immédiate des jetons devenus inutiles
- Surveillance de l'utilisation des jetons

Audit et journaux
===================

Les journaux d'audit dans un système de recherche sont importants pour l'investigation des incidents de sécurité et la conformité réglementaire.

Journaux enregistrés par Fess
-------------------------------

- **Journaux de recherche** : Qui a recherché quoi (consultable dans [Informations système] > [Journal de recherche] de la console d'administration)
- **Journaux d'audit** (``audit.log``) : Les opérations telles que la connexion, la déconnexion, l'accès et les modifications de permissions sont enregistrées de manière unifiée

Conservation des journaux
---------------------------

Configurez la durée de conservation des journaux en fonction des exigences de sécurité.
Si des exigences de conformité existent, envisagez le transfert des journaux vers un système externe de gestion des journaux (SIEM).

Synthèse
=========

Dans cet article, nous avons conçu une architecture de sécurité pour Fess dans un environnement d'entreprise.

- Trois options d'intégration SSO (OIDC, SAML, SPNEGO) et leurs scénarios d'application
- Conception de l'intégration Entra ID via OpenID Connect
- Chiffrement des communications via SSL/TLS
- Conception des permissions pour les jetons d'accès à l'API
- Gestion des journaux d'audit

Construisez une infrastructure de recherche sécurisée tout en maintenant l'équilibre entre sécurité et ergonomie.

Le prochain article traitera de l'automatisation de l'infrastructure de recherche.

Références
===========

- `Configuration SSO de Fess <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Configuration de la sécurité de Fess <https://fess.codelibs.org/ja/15.5/config/security.html>`__
