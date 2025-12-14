==========================================
Configuration SSO avec authentification SAML
==========================================

Aperçu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) utilisant SAML (Security Assertion Markup Language) 2.0.
En utilisant l'authentification SAML, les informations utilisateur authentifiées par un IdP (Identity Provider) peuvent être intégrées à |Fess|, permettant l'affichage de résultats de recherche basés sur les permissions utilisateur lorsqu'elle est combinée avec la recherche basée sur les rôles.

Fonctionnement de l'authentification SAML
-----------------------------------------

Dans l'authentification SAML, |Fess| fonctionne comme un SP (Service Provider) et collabore avec un IdP externe pour l'authentification.

1. L'utilisateur accède au point d'accès SSO de |Fess| (``/sso/``)
2. |Fess| redirige la demande d'authentification vers l'IdP
3. L'utilisateur s'authentifie auprès de l'IdP
4. L'IdP envoie l'assertion SAML à |Fess|
5. |Fess| valide l'assertion et connecte l'utilisateur

Pour l'intégration avec la recherche basée sur les rôles, voir :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification SAML, vérifiez les prérequis suivants :

- |Fess| 15.4 ou supérieur est installé
- Un IdP (Identity Provider) compatible SAML 2.0 est disponible
- |Fess| est accessible via HTTPS (requis pour les environnements de production)
- Vous avez la permission d'enregistrer |Fess| comme SP côté IdP

Exemples d'IdP pris en charge :

- Microsoft Entra ID (Azure AD)
- Okta
- Google Workspace
- Keycloak
- OneLogin
- Autres IdP compatibles SAML 2.0

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification SAML, ajoutez le paramètre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=saml

Configuration du SP (Service Provider)
--------------------------------------

Pour configurer |Fess| comme SP, spécifiez l'URL de base du SP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.sp.base.url``
     - URL de base du SP
     - (Requis)

Ce paramètre configure automatiquement les points d'accès suivants :

- **Entity ID** : ``{base_url}/sso/metadata``
- **ACS URL** : ``{base_url}/sso/``
- **SLO URL** : ``{base_url}/sso/logout``

Exemple ::

    saml.sp.base.url=https://fess.example.com

Configuration d'URL individuelle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également spécifier les URL individuellement au lieu d'utiliser l'URL de base.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.sp.entityid``
     - Entity ID du SP
     - (Requis pour config individuelle)
   * - ``saml.sp.assertion_consumer_service.url``
     - URL du service Assertion Consumer
     - (Requis pour config individuelle)
   * - ``saml.sp.single_logout_service.url``
     - URL du service Single Logout
     - (Optionnel)

Configuration de l'IdP (Identity Provider)
------------------------------------------

Configurez les informations obtenues de votre IdP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.idp.entityid``
     - Entity ID de l'IdP
     - (Requis)
   * - ``saml.idp.single_sign_on_service.url``
     - URL du service SSO de l'IdP
     - (Requis)
   * - ``saml.idp.x509cert``
     - Certificat X.509 de signature de l'IdP (encodé en Base64, sans sauts de ligne)
     - (Requis)
   * - ``saml.idp.single_logout_service.url``
     - URL du service SLO de l'IdP
     - (Optionnel)

.. note::
   Pour ``saml.idp.x509cert``, spécifiez uniquement le contenu encodé en Base64 du certificat sur une seule ligne sans sauts de ligne.
   N'incluez pas les lignes ``-----BEGIN CERTIFICATE-----`` et ``-----END CERTIFICATE-----``.

Récupération des métadonnées SP
-------------------------------

Après le démarrage de |Fess|, vous pouvez récupérer les métadonnées SP au format XML depuis le point d'accès ``/sso/metadata``.

::

    https://fess.example.com/sso/metadata

Importez ces métadonnées dans votre IdP, ou enregistrez manuellement le SP côté IdP en utilisant le contenu des métadonnées.

.. note::
   Pour récupérer les métadonnées, vous devez d'abord compléter la configuration SAML de base (``sso.type=saml`` et ``saml.sp.base.url``) et démarrer |Fess|.

Configuration côté IdP
======================

Lors de l'enregistrement de |Fess| comme SP côté IdP, configurez les informations suivantes :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Valeur
   * - ACS URL / Reply URL
     - ``https://<Hôte Fess>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Hôte Fess>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` (Recommandé)

Informations à obtenir de l'IdP
-------------------------------

Obtenez les informations suivantes depuis l'écran de configuration ou les métadonnées de votre IdP pour la configuration de |Fess| :

- **Entity ID de l'IdP** : URI identifiant l'IdP
- **URL SSO (HTTP-Redirect)** : URL du point d'accès Single Sign-On
- **Certificat X.509** : Certificat de clé publique utilisé pour la vérification de signature de l'assertion SAML

Mappage des attributs utilisateur
=================================

Vous pouvez mapper les attributs utilisateur obtenus des assertions SAML aux groupes et rôles |Fess|.

Configuration des attributs de groupe
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.attribute.group.name``
     - Nom de l'attribut contenant les informations de groupe
     - ``memberOf``
   * - ``saml.default.groups``
     - Groupes par défaut (séparés par des virgules)
     - (Aucun)

Exemple ::

    saml.attribute.group.name=groups
    saml.default.groups=user

Configuration des attributs de rôle
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.attribute.role.name``
     - Nom de l'attribut contenant les informations de rôle
     - (Aucun)
   * - ``saml.default.roles``
     - Rôles par défaut (séparés par des virgules)
     - (Aucun)

Exemple ::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   Si les attributs ne peuvent pas être obtenus de l'IdP, les valeurs par défaut seront utilisées.
   Lors de l'utilisation de la recherche basée sur les rôles, configurez les groupes ou rôles appropriés.

Configuration de sécurité
=========================

Pour les environnements de production, il est recommandé d'activer les paramètres de sécurité suivants.

Paramètres de signature
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.security.authnrequest_signed``
     - Signer les demandes d'authentification
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Exiger les signatures de messages
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Exiger les signatures d'assertions
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - Signer les demandes de déconnexion
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - Signer les réponses de déconnexion
     - ``false``

.. warning::
   Les fonctionnalités de sécurité sont désactivées par défaut.
   Pour les environnements de production, il est fortement recommandé de définir au moins ``saml.security.want_assertions_signed=true``.

Paramètres de chiffrement
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.security.want_assertions_encrypted``
     - Exiger le chiffrement des assertions
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - Exiger le chiffrement du NameID
     - ``false``

Autres paramètres de sécurité
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.security.strict``
     - Mode strict (effectuer une validation stricte)
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Algorithme de signature
     - ``http://www.w3.org/2000/09/xmldsig#rsa-sha1``
   * - ``saml.sp.nameidformat``
     - Format du NameID
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour la vérification dans un environnement de test.

::

    # Activer SSO
    sso.type=saml

    # Configuration SP
    saml.sp.base.url=https://fess.example.com

    # Configuration IdP (définir les valeurs obtenues de la console d'administration IdP)
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(certificat encodé en Base64)

    # Groupes par défaut
    saml.default.groups=user

Configuration recommandée (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandée pour les environnements de production.

::

    # Activer SSO
    sso.type=saml

    # Configuration SP
    saml.sp.base.url=https://fess.example.com

    # Configuration IdP
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(certificat encodé en Base64)

    # Mappage des attributs utilisateur
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # Paramètres de sécurité (recommandés pour la production)
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

Dépannage
=========

Problèmes courants et solutions
-------------------------------

Impossible de retourner à Fess après l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'URL ACS est correctement configurée côté IdP
- Assurez-vous que la valeur de ``saml.sp.base.url`` correspond à la configuration de l'IdP

Erreur de vérification de signature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le certificat IdP est correctement configuré
- Assurez-vous que le certificat n'a pas expiré
- Le certificat doit être spécifié uniquement comme contenu encodé en Base64, sans sauts de ligne

Groupes/rôles utilisateur non reflétés
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que les attributs sont correctement configurés côté IdP
- Assurez-vous que la valeur de ``saml.attribute.group.name`` correspond au nom d'attribut envoyé par l'IdP
- Activez le mode débogage pour inspecter le contenu de l'assertion SAML

Paramètres de débogage
----------------------

Pour investiguer les problèmes, vous pouvez activer le mode débogage avec le paramètre suivant :

::

    saml.security.debug=true

Vous pouvez également ajuster les niveaux de journalisation de |Fess| pour afficher des logs SAML détaillés.

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
