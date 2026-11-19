============================================
Configuration SSO avec authentification SAML
============================================

Aperçu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) utilisant SAML (Security Assertion Markup Language) 2.0.
En utilisant l'authentification SAML, les informations utilisateur authentifiées par un IdP (Identity Provider) peuvent être intégrées à |Fess|, permettant l'affichage de résultats de recherche basés sur les permissions utilisateur lorsqu'elle est combinée avec la recherche basée sur les rôles.

.. note::
   La prise en charge de l'authentification SAML provient du plugin ``fess-sso-saml``, qui ne
   fait pas partie de la distribution. Installez-le depuis la page **Système > Plugin** de
   l'écran d'administration ou avec ``bin/fess-setup install plugin fess-sso-saml``.
   Le plugin traite les messages SAML avec la bibliothèque SAML `saml4j <https://github.com/codelibs/saml4j>`__.
   Jusque-là, avec ``sso.type=saml``, toute requête vers ``/sso/`` est simplement redirigée
   vers la page de connexion.

Fonctionnement de l'authentification SAML
-----------------------------------------

Dans l'authentification SAML, |Fess| fonctionne comme un SP (Service Provider) et collabore avec un IdP externe pour l'authentification.

1. L'utilisateur accède au point d'accès SSO de |Fess| (``/sso/``)
2. |Fess| redirige la demande d'authentification vers l'IdP
3. L'utilisateur s'authentifie auprès de l'IdP
4. L'IdP envoie l'assertion SAML à |Fess|
5. |Fess| valide l'assertion et connecte l'utilisateur

.. note::
   Seule la connexion initiée par le SP, qui démarre au point d'accès SSO de |Fess| (``/sso/``) comme
   décrit ci-dessus, est prise en charge. |Fess| associe chaque réponse SAML à l'identifiant de
   l'AuthnRequest qu'il a émise ; une réponse initiée par l'IdP (non sollicitée), par exemple depuis
   une vignette |Fess| dans le tableau de bord Okta ou dans le portail « Mes applications » de
   Microsoft Entra ID, n'a donc aucune AuthnRequest correspondante et est rejetée. Si vous placez une
   vignette côté IdP, faites-la pointer vers le point d'accès ``/sso/`` de |Fess|.

   Notez qu'en 15.7, une connexion initiée par l'IdP fonctionnait incidemment lorsque
   ``tomcat.sameSiteCookies=none`` était défini : |Fess| renvoyait à l'IdP la réponse qu'il ne pouvait
   pas associer, et l'IdP retournait immédiatement une assertion sollicitée. En 15.8, ce renvoi n'a
   plus lieu, si bien que la connexion initiée par l'IdP ne fonctionne pas.

Pour l'intégration avec la recherche basée sur les rôles, voir :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification SAML, vérifiez les prérequis suivants :

- |Fess| 15.10 ou supérieur est installé
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

.. note::
   ``sso.type`` ainsi que les paramètres SAML de base (informations IdP, informations SP, mappage des attributs utilisateur) peuvent également être configurés depuis la page « Système > Général » de l'interface d'administration.
   Les paramètres modifiés dans l'interface d'administration sont enregistrés dans ``system.properties`` et persistent après redémarrage.
   Cependant, les paramètres de sécurité tels que la signature/le chiffrement ainsi que le certificat SP et la clé privée ne peuvent pas être configurés dans l'interface d'administration ; écrivez-les directement dans ``system.properties``.

.. note::
   Les paramètres commençant par ``saml.`` sont lus uniquement depuis ``system.properties``.
   Les propriétés système de la JVM telles que ``-Dsaml.security....`` ou ``-Dfess.saml.security....`` ne sont pas consultées.
   En particulier, ``saml.security.*`` n'a pas non plus de champ dans l'interface d'administration :
   l'écrire directement dans ``system.properties`` est le seul moyen de le définir.

Configuration du cookie de session
----------------------------------

L'IdP renvoie l'assertion à |Fess| via un **POST intersites**. Un cookie ``SameSite=Lax`` n'est pas envoyé sur une telle requête, si bien que la connexion SAML n'aboutit pas avec la valeur par défaut livrée avec |Fess|.

Remplacez ``tomcat.sameSiteCookies`` par ``none`` dans ``tomcat_config.properties``. Ce fichier se trouve dans ``lib/classes/`` pour le paquet ZIP et dans ``/etc/fess/`` pour les paquets DEB/RPM.

::

    tomcat.sameSiteCookies = none

.. warning::
   Les navigateurs n'acceptent ``none`` que sur un cookie portant également l'attribut ``Secure``. |Fess| doit donc être servi en HTTPS. En HTTP simple, ce réglage rend la connexion à |Fess| impossible.

.. note::
   La valeur par défaut ``lax`` est prévue pour les méthodes SSO dont le rappel revient sous forme de redirection (GET). La liaison HTTP-POST de SAML n'en fait pas partie, ce changement n'est donc nécessaire qu'avec SAML. |Fess| doit être redémarré après la modification.

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
     - ``http://localhost:8080``

.. note::
   La valeur par défaut de ``saml.sp.base.url`` est ``http://localhost:8080``.
   En dehors des environnements de test, définissez toujours l'URL utilisée pour accéder à |Fess| depuis l'extérieur (HTTPS en production).

Ce paramètre configure automatiquement les points d'accès suivants :

- **Entity ID** : ``{saml.sp.base.url}/sso/metadata``
- **ACS URL** : ``{saml.sp.base.url}/sso/``
- **SLO URL** : ``{saml.sp.base.url}/sso/logout``

Exemple ::

    saml.sp.base.url=https://fess.example.com

Configuration d'URL individuelle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En principe, la configuration de ``saml.sp.base.url`` permet de configurer automatiquement chaque URL de point d'accès, mais vous pouvez si nécessaire surcharger les URL individuelles explicitement avec les propriétés suivantes.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.sp.entityid``
     - Entity ID du SP
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - URL du service Assertion Consumer
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - URL du service Single Logout
     - ``{saml.sp.base.url}/sso/logout``

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
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - Certificats de signature supplémentaires de l'IdP (par exemple lors d'une rotation de clés)
     - (Optionnel)

.. note::
   Le certificat de l'IdP est la seule ancre de confiance pour les signatures ; un certificat contenu dans un message n'est jamais considéré comme fiable.
   Les certificats de l'IdP et du SP doivent être des clés RSA d'au moins 2048 bits.
   ``saml.idp.x509cert`` peut être omis lorsque ``saml.idp.x509certMulti.N`` est défini.

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

.. note::
   |Fess| vérifie les points suivants pour chaque assertion. Les URL sont dérivées de ``saml.sp.base.url`` (ou des propriétés d'URL individuelles), et non de la requête entrante.

   - L'assertion contient un ``AudienceRestriction`` qui désigne l'entity ID du SP
   - Le ``Destination`` d'une Response signée et le ``Recipient`` du SubjectConfirmation correspondent à l'URL du service Assertion Consumer

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

.. note::
   |Fess| utilise telles quelles les valeurs de groupe de l'assertion : aucune interrogation de
   l'annuaire n'est effectuée et les groupes imbriqués (transitifs) ne sont pas développés.
   La présence des groupes parents dépend donc uniquement de la configuration des claims de l'IdP,
   contrairement à :doc:`sso-entraid`, où |Fess| résout les groupes parents en utilisant l'API
   Microsoft Graph.

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

.. warning::
   Lorsque ``saml.attribute.role.name`` est défini, les valeurs d'attribut envoyées par l'IdP
   deviennent telles quelles des rôles |Fess|. Comme ``authentication.admin.roles`` dans
   ``fess_config.properties`` vaut ``admin`` par défaut, tout utilisateur dont l'attribut de rôle
   contient ``admin`` obtient les privilèges d'administrateur de |Fess|. Vérifiez qui peut contrôler
   l'attribut de rôle côté IdP et, si nécessaire, remplacez ``authentication.admin.roles`` par un
   autre nom.

IdP qui répètent un nom d'attribut
----------------------------------

Si l'IdP répartit le même nom d'attribut sur plusieurs éléments ``<Attribute>``, |Fess| fusionne
leurs valeurs.

Keycloak envoie par défaut des assertions de cette forme : ses mappeurs de rôles et de groupes
émettent un élément ``<Attribute>`` par valeur tant que leur option ``single`` n'est pas activée, et
tout compte Keycloak possède plusieurs rôles de royaume par défaut. Aucun paramètre n'est nécessaire
dans |Fess| pour cela.

Configuration de sécurité
=========================

Les paramètres de sécurité suivants sont lus depuis ``system.properties``.

.. note::
   Si des paramètres qui affaiblissent les valeurs par défaut subsistent (``saml.security.want_logout_signed=false``
   avec la déconnexion unique configurée, ``saml.security.allow_deprecated_alg=true`` ou
   ``saml.security.allow_rsa_1_5=true``), un avertissement ``Insecure SAML settings: ...`` est écrit dans le
   journal lors du chargement des paramètres SAML.

Paramètres de signature
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.security.authnrequest_signed``
     - Signer les demandes d'authentification (nécessite ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Exiger que la Response soit signée
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Exiger que l'Assertion soit signée
     - ``false``
   * - ``saml.security.want_logout_signed``
     - Exiger que les messages de déconnexion de l'IdP soient signés
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - Accepter les signatures SHA-1
     - ``false``
   * - ``saml.security.signature_algorithm``
     - Algorithme des signatures sortantes : l'URI de ``rsa-sha256``, ``rsa-sha384`` ou ``rsa-sha512``
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   Quels que soient ces paramètres, soit la Response, soit l'Assertion doit être signée.
   Utilisez ``saml.security.want_messages_signed`` ou ``saml.security.want_assertions_signed`` pour exiger la signature sur l'élément que signe votre IdP.
   La signature doit référencer l'élément signé par son propre ID et utiliser ``rsa-sha256``, ``rsa-sha384`` ou ``rsa-sha512`` (ou les variantes ECDSA).
   Les signatures SHA-1 sont rejetées sauf si ``saml.security.allow_deprecated_alg=true`` ; vérifiez donc que votre IdP signe avec SHA-256 ou plus fort.

.. note::
   Lorsque la déconnexion unique est configurée (``saml.idp.single_logout_service.url``), la LogoutRequest et la
   LogoutResponse envoyées par l'IdP doivent être signées avec la clé de ``saml.idp.x509cert``
   (``saml.security.want_logout_signed=true`` est la valeur par défaut).
   Définissez ``saml.security.want_logout_signed=false`` uniquement pour un IdP qui ne peut pas les signer.
   Le service de déconnexion unique (``/sso/logout``) accepte la liaison par redirection (GET) et la liaison POST.
   Enregistrez aussi l'URL ``/sso/logout`` pour la liaison POST côté IdP ; une LogoutResponse que l'IdP
   envoie par POST au service Assertion Consumer n'est pas reconnue.

Paramètres de chiffrement
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.security.want_assertions_encrypted``
     - Exiger le chiffrement des assertions (nécessite ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - Accepter le transport de clé RSA 1.5 (nécessite ``saml.sp.privatekey``). Sinon, seul OAEP est accepté
     - ``false``

.. note::
   Laissez ``saml.security.allow_rsa_1_5`` à ``false`` sauf si votre IdP ne peut chiffrer qu'avec RSA 1.5.

Configuration du certificat SP et de la clé privée
---------------------------------------------------

Lorsque le SP signe les demandes d'authentification ou les messages de déconnexion (par ex. ``saml.security.authnrequest_signed``), ou demande le chiffrement des assertions ou du NameID (par ex. ``saml.security.want_assertions_encrypted``), vous devez configurer la clé privée (PKCS#8) et le certificat X.509 du SP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.sp.x509cert``
     - Certificat X.509 du SP (encodé en Base64, sans sauts de ligne)
     -
   * - ``saml.sp.privatekey``
     - Clé privée du SP (encodée en Base64, sans sauts de ligne)
     -

.. note::
   Pour ``saml.sp.x509cert`` et ``saml.sp.privatekey``, comme pour ``saml.idp.x509cert``, spécifiez le contenu encodé en Base64 sur une seule ligne sans sauts de ligne (n'incluez pas les lignes ``-----BEGIN ...-----`` et ``-----END ...-----``).
   Lorsque vous activez la signature/le chiffrement, enregistrez également le certificat SP côté IdP. Le certificat SP est publié dans les métadonnées SP à l'adresse ``/sso/metadata``.

Autres paramètres de sécurité
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.security.requested_authncontext``
     - Contexte d'authentification demandé (une valeur vide n'en demande aucun)
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - Comparaison pour le contexte d'authentification demandé (``exact``, ``minimum``, ``maximum`` ou ``better``)
     - ``exact``
   * - ``saml.security.clock_drift``
     - Décalage d'horloge toléré lors de la vérification des périodes de validité (secondes, 0 à 600)
     - ``120``
   * - ``saml.security.max_message_size``
     - Taille maximale d'un message décodé accepté (octets, 1024 à 16777216)
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - Format du NameID
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   L'audience, le destinataire, la destination, l'émetteur et la période de validité d'une assertion sont toujours vérifiés,
   et une réponse doit correspondre à une connexion démarrée par |Fess|.
   Une assertion sans Audience, ou dont l'Audience ne désigne pas l'entity ID du SP, est rejetée.
   La validation est toujours stricte : ``saml.strict=false`` est refusé.

Propriétés qui ne sont plus utilisées
-------------------------------------

Les propriétés suivantes sont ignorées. Un seul avertissement qui les nomme est écrit dans le journal.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Propriété
     - Désormais
   * - ``saml.security.reject_deprecated_alg``
     - Les signatures SHA-1 sont rejetées par défaut ; ``saml.security.allow_deprecated_alg=true`` les accepte
   * - ``saml.security.allowed_key_transport_algorithms``
     - Seul OAEP est accepté par défaut ; ``saml.security.allow_rsa_1_5=true`` accepte également RSA 1.5
   * - ``saml.security.allow_duplicated_attribute_name``
     - Les attributs répétés sont toujours fusionnés
   * - ``saml.security.reject_missing_audience``
     - Une assertion sans audience est toujours rejetée
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - Définissez ``saml.idp.x509cert`` ; une empreinte n'est pas une ancre de confiance
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``, les propriétés ``*.binding`` et ``*.response.url``
     - N'est plus utilisé

Toute autre propriété ``saml.`` inconnue de la bibliothèque interrompt les connexions SAML avec un message qui la nomme,
afin qu'un paramètre de sécurité mal orthographié ne passe pas inaperçu. ``saml.debug`` est accepté et n'a aucun effet.

Expiration de l'AuthnRequest
============================

|Fess| envoie une AuthnRequest à l'IdP à chaque accès à ``/sso/`` et enregistre son identifiant dans la session.
La réponse SAML renvoyée par l'IdP est validée par rapport à l'identifiant enregistré.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``saml.request.id.ttl``
     - Durée pendant laquelle l'identifiant d'une AuthnRequest restée sans réponse est conservé (secondes)
     - ``3600``

L'identifiant enregistré est écarté une fois ce délai écoulé.
S'il expire (par exemple parce que la page de connexion de l'IdP est restée ouverte), l'assertion renvoyée ne peut pas être associée et la connexion échoue une seule fois.

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
    # Exiger la signature sur l'élément que signe l'IdP
    # (saml.security.want_messages_signed=true pour la Response)
    saml.security.want_assertions_signed=true

Dépannage
=========

Problèmes courants et solutions
-------------------------------

Impossible de retourner à Fess après l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'URL ACS est correctement configurée côté IdP
- Assurez-vous que la valeur de ``saml.sp.base.url`` correspond à la configuration de l'IdP
- L'assertion SAML arrive sous forme de POST intersite depuis l'IdP. Lorsque
  ``tomcat.sameSiteCookies`` dans ``tomcat_config.properties`` vaut ``lax`` (la valeur par défaut),
  le navigateur n'envoie pas le cookie de session avec cette requête et la connexion échoue une seule
  fois. Dans ce cas, définissez ``tomcat.sameSiteCookies = none`` (``SameSite=None`` nécessite HTTPS)
- Si la connexion a pris trop de temps chez l'IdP, l'identifiant d'AuthnRequest n'est plus présent
  lorsque l'assertion revient : la connexion échoue une seule fois et doit être recommencée
- |Fess| ne définit pas ``session-timeout`` dans ``app/WEB-INF/web.xml`` ; la valeur par défaut du
  conteneur de servlets, 30 minutes, s'applique donc, et elle est plus courte que les 3600 secondes
  de ``saml.request.id.ttl``, si bien que la session est écartée en premier. Augmenter uniquement
  ``saml.request.id.ttl`` ne laisse pas plus de temps aux utilisateurs pour terminer la connexion
  chez l'IdP : allongez aussi le délai d'expiration de session

La validation de Destination ou de Recipient échoue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le ``Destination`` d'une Response signée et le ``Recipient`` du SubjectConfirmation doivent correspondre à
l'URL du service Assertion Consumer de |Fess|. Cette URL provient de ``saml.sp.base.url`` (ou de
``saml.sp.assertion_consumer_service.url``), et non de la requête qui parvient à |Fess| ; un proxy
inverse qui termine TLS n'affecte donc pas la comparaison.

- Définissez ``saml.sp.base.url`` sur l'URL visible depuis l'extérieur, schéma et port compris
- Enregistrez la même URL ACS (``{saml.sp.base.url}/sso/``) côté IdP
- Si ``saml.sp.entityid`` est surchargé, l'IdP doit utiliser cette valeur comme Audience

Erreur de vérification de signature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le certificat IdP est correctement configuré
- Assurez-vous que le certificat n'a pas expiré
- Le certificat doit être spécifié uniquement comme contenu encodé en Base64, sans sauts de ligne
- Le certificat de l'IdP doit être une clé RSA d'au moins 2048 bits
- Soit la Response, soit l'Assertion doit être signée, et la signature doit utiliser SHA-256 ou plus fort
  (SHA-1 n'est accepté qu'avec ``saml.security.allow_deprecated_alg=true``)
- La raison du rejet d'une réponse est écrite dans le journal sous la forme ``Authentication failed: <reason> - <detail>``

Groupes/rôles utilisateur non reflétés
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que les attributs sont correctement configurés côté IdP
- Assurez-vous que la valeur de ``saml.attribute.group.name`` correspond au nom d'attribut envoyé par l'IdP
- Avec Microsoft Entra ID, le claim de groupes contient les ``ObjectId`` (GUID) des groupes, sauf
  si un autre attribut source est sélectionné ; les valeurs ne correspondent donc pas aux noms de
  groupe
- Microsoft Entra ID omet entièrement le claim de groupes lorsque l'utilisateur appartient à plus
  de 150 groupes (les groupes imbriqués comptent dans cette limite) ; |Fess| se rabat alors sur
  ``saml.default.groups``
- Comparez les noms d'attributs avec ceux de l'assertion réellement envoyée par l'IdP

Paramètres de journalisation
----------------------------

Lorsque l'authentification SAML échoue, la raison est toujours écrite dans le journal sous forme d'avertissement.
La propriété ``saml.debug`` n'a aucun effet.

Pour afficher des journaux détaillés liés à SAML, ajoutez le logger suivant dans ``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-oidc` - À propos de la configuration SSO avec OpenID Connect
- :doc:`sso-entraid` - À propos de la configuration SSO dédiée à Microsoft Entra ID
