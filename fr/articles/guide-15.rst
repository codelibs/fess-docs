============================================================
Partie 15 : Infrastructure de recherche securisee -- Integration SSO et controle d'acces a la recherche dans un environnement Zero Trust
============================================================

Introduction
=============

Les exigences en matiere de securite de l'information dans les entreprises deviennent chaque annee plus strictes.
Etant donne que les systemes de recherche agregent un grand volume de documents confidentiels, des mecanismes d'authentification et d'autorisation adequats sont indispensables.

Dans cet article, nous approfondissons la recherche basee sur les roles presentee dans la Partie 5 et concevons une architecture de securite centree sur l'integration SSO (authentification unique).

Public cible
=============

- Personnes exploitant Fess dans un environnement d'entreprise
- Personnes concevant l'integration SSO (OIDC, SAML)
- Personnes comprenant les concepts de securite Zero Trust

Organisation des exigences de securite
=========================================

Nous organisons ci-dessous les exigences de securite typiques des entreprises.

.. list-table:: Exigences de securite
   :header-rows: 1
   :widths: 30 70

   * - Exigence
     - Description
   * - Authentification unique
     - S'integrer a un IdP existant pour supprimer les operations de connexion supplementaires
   * - Acces base sur les roles
     - Controler les resultats de recherche en fonction de l'affiliation et des permissions de l'utilisateur
   * - Chiffrement des communications
     - Chiffrer toutes les communications via HTTPS
   * - Controle d'acces a l'API
     - Authentification API basee sur des jetons et gestion des permissions
   * - Journaux d'audit
     - Enregistrer qui a recherche quoi

Options d'integration SSO
============================

Nous presentons ci-dessous les protocoles SSO pris en charge par Fess et les scenarios dans lesquels chacun est applicable.

.. list-table:: Comparaison des protocoles SSO
   :header-rows: 1
   :widths: 20 30 50

   * - Protocole
     - IdPs representatifs
     - Scenarios d'application
   * - OpenID Connect
     - Entra ID, Keycloak, Google
     - Environnements cloud, infrastructure d'authentification moderne
   * - SAML 2.0
     - Entra ID, Okta, OneLogin
     - Environnements d'entreprise, lorsqu'un IdP SAML existant est disponible
   * - SPNEGO/Kerberos
     - Active Directory
     - Environnements d'authentification integree Windows

Integration SSO via OpenID Connect / Entra ID
================================================

Il s'agit de l'approche la plus moderne et recommandee.
En plus de l'integration generique OpenID Connect, Fess fournit egalement une fonctionnalite d'integration dediee pour Entra ID (Azure AD).
Nous expliquons ici l'integration en prenant Entra ID comme exemple.

Apercu du flux d'authentification
-----------------------------------

1. Un utilisateur accede a Fess
2. Fess redirige l'utilisateur vers l'ecran d'authentification d'Entra ID
3. L'utilisateur s'authentifie aupres d'Entra ID (y compris la MFA)
4. Entra ID renvoie un jeton d'authentification a Fess
5. Fess recupere les informations utilisateur et les informations de groupe a partir du jeton
6. Les roles sont attribues en fonction des informations de groupe
7. Les resultats de recherche sont fournis en fonction des roles

Configuration cote Entra ID
-----------------------------

1. Enregistrez une application dans Entra ID
2. Configurez l'URI de redirection (URL de callback OIDC de Fess)
3. Accordez les permissions API requises (User.Read, GroupMember.Read.All, etc.)
4. Obtenez l'ID client et le secret

Configuration cote Fess
-------------------------

Configurez les informations de connexion SSO sur la page [Systeme] > [General] de la console d'administration.
Les principaux elements de configuration sont les suivants :

- URL du fournisseur OpenID Connect (point de terminaison Entra ID)
- ID client
- Secret client
- Portees (openid, profile, email, etc.)
- Parametres des revendications de groupe

Correspondance entre groupes et roles
----------------------------------------

Associez les groupes Entra ID aux roles Fess.
Cela permet a la gestion des groupes dans Entra ID d'etre directement refletee dans le controle des resultats de recherche.

Exemple : Groupe Entra ID « Engineering » -> Role Fess « engineering_role »

Integration SSO via SAML
==========================

L'integration SAML est adaptee aux environnements disposant d'un IdP SAML existant.

Apercu du flux d'authentification
-----------------------------------

Avec SAML, des SAML Assertions sont echangees entre le SP (Service Provider = Fess) et l'IdP.

1. Un utilisateur accede a Fess
2. Fess envoie un SAML AuthnRequest a l'IdP
3. L'IdP authentifie l'utilisateur
4. L'IdP renvoie une SAML Response (contenant les attributs utilisateur) a Fess
5. Fess attribue des roles en fonction des attributs utilisateur

Configuration cote Fess
-------------------------

Les parametres suivants sont necessaires pour l'integration SAML :

- URL des metadonnees ou fichier XML de l'IdP
- ID d'entite du SP
- Assertion Consumer Service URL
- Correspondance des attributs (nom d'utilisateur, adresse e-mail, groupes)

Integration SPNEGO / Kerberos
================================

Dans les environnements Windows Active Directory, l'authentification integree Windows via SPNEGO/Kerberos peut etre utilisee.
Lors de l'acces via un navigateur depuis un PC membre du domaine, l'authentification s'effectue automatiquement sans operation de connexion supplementaire.

Cette methode est la plus transparente pour les utilisateurs, mais la configuration est la plus complexe.
Un environnement de domaine Active Directory est un prerequis.

Chiffrement des communications
=================================

Configuration SSL/TLS
----------------------

Dans les environnements de production, il est recommande d'effectuer tous les acces a Fess via HTTPS.

**Methode par proxy inverse (recommandee)**

Deployez Nginx ou Apache HTTP Server comme proxy inverse pour effectuer la terminaison SSL.
Fess lui-meme fonctionne en HTTP, et le proxy inverse gere le HTTPS.

::

    [Client] --HTTPS--> [Nginx] --HTTP--> [Fess]

L'avantage de cette methode est que la gestion des certificats est centralisee au niveau du proxy inverse.

**Methode de configuration directe de Fess**

Il est egalement possible de configurer les certificats SSL directement dans le Tomcat de Fess.
Cette methode est adaptee aux environnements de petite taille ou lorsqu'aucun proxy inverse n'est deploye.

Securite de l'acces a l'API
==============================

Nous renforcons ci-dessous la securite de l'integration API presentee dans la Partie 11.

Conception des permissions des jetons
----------------------------------------

Configurez les permissions appropriees pour les jetons d'acces.

.. list-table:: Exemple de conception de jetons
   :header-rows: 1
   :widths: 25 25 50

   * - Utilisation
     - Permissions
     - Remarques
   * - Widget de recherche
     - Recherche uniquement (lecture seule)
     - Utilise cote frontend
   * - Traitement par lots
     - Recherche + Indexation
     - Utilise cote serveur
   * - Automatisation de l'administration
     - Acces a l'API d'administration
     - Utilise dans les scripts d'exploitation

Gestion des jetons
-------------------

- Rotation reguliere (tous les 3 a 6 mois)
- Revocation immediate des jetons devenus inutiles
- Surveillance de l'utilisation des jetons

Audit et journaux
===================

Les journaux d'audit dans un systeme de recherche sont importants pour l'investigation des incidents de securite et la conformite reglementaire.

Journaux enregistres par Fess
-------------------------------

- **Journaux de recherche** : Qui a recherche quoi (consultable dans [Informations systeme] > [Journal de recherche] de la console d'administration)
- **Journaux d'audit** (``audit.log``) : Les operations telles que la connexion, la deconnexion, l'acces et les modifications de permissions sont enregistrees de maniere unifiee

Conservation des journaux
---------------------------

Configurez la duree de conservation des journaux en fonction des exigences de securite.
Si des exigences de conformite existent, envisagez le transfert des journaux vers un systeme externe de gestion des journaux (SIEM).

Synthese
=========

Dans cet article, nous avons concu une architecture de securite pour Fess dans un environnement d'entreprise.

- Trois options d'integration SSO (OIDC, SAML, SPNEGO) et leurs scenarios d'application
- Conception de l'integration Entra ID via OpenID Connect
- Chiffrement des communications via SSL/TLS
- Conception des permissions pour les jetons d'acces a l'API
- Gestion des journaux d'audit

Construisez une infrastructure de recherche securisee tout en maintenant l'equilibre entre securite et ergonomie.

Le prochain article traitera de l'automatisation de l'infrastructure de recherche.

References
===========

- `Configuration SSO de Fess <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Configuration de la securite de Fess <https://fess.codelibs.org/ja/15.5/config/security.html>`__
