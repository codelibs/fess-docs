============================================
Configuration SSO avec authentification SAML
============================================

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

- |Fess| 15.8 ou supérieur est installé
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
   En particulier, ``saml.security.*``, ``saml.strict`` et ``saml.debug`` n'ont pas non plus de champ dans l'interface d'administration :
   les écrire directement dans ``system.properties`` est le seul moyen de les définir.

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

Configuration de sécurité
=========================

Pour les environnements de production, il est recommandé d'activer les paramètres de sécurité suivants.

.. note::
   Si des paramètres déconseillés subsistent, un avertissement ``Insecure SAML settings: ...`` est
   écrit dans le journal lors du chargement des paramètres SAML.

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
   * - ``saml.security.reject_deprecated_alg``
     - Rejeter les algorithmes de signature obsolètes tels que SHA-1
     - ``false``

.. warning::
   Les fonctionnalités de sécurité sont désactivées par défaut.
   Pour les environnements de production, il est fortement recommandé de définir au moins ``saml.security.want_assertions_signed=true``.

.. note::
   Tant que ``saml.security.reject_deprecated_alg`` vaut ``false``, les assertions et messages signés
   avec SHA-1 (``rsa-sha1`` et ``dsa-sha1``) sont également acceptés. Ce paramètre n'est pas activé par
   défaut, car son activation entraîne le rejet des IdP qui signent encore avec SHA-1.
   Vérifiez que votre IdP signe avec SHA-256 ou plus fort, puis définissez
   ``saml.security.reject_deprecated_alg=true``.

.. warning::
   Lorsque la déconnexion unique est configurée (``saml.idp.single_logout_service.url``), définissez
   impérativement aussi ``saml.security.want_messages_signed=true``.
   Tant que ce paramètre vaut ``false``, aucune signature n'est exigée sur une LogoutRequest reçue sur
   ``/sso/logout``. Les seules vérifications effectuées sont le schéma XML, ``NotOnOrAfter`` (s'il est
   présent), ``Destination`` (s'il est présent) et la correspondance de l'Issuer avec
   ``saml.idp.entityid`` (s'il est présent) ; le NameID de la LogoutRequest n'est jamais comparé à
   l'utilisateur connecté. L'élément Issuer est optionnel dans le schéma SAML, si bien qu'une
   LogoutRequest qui l'omet n'est jamais comparée à l'identifiant d'entité de l'IdP. Un attaquant peut
   donc, sans avoir besoin de connaître l'identifiant d'entité de l'IdP, forger une LogoutRequest non
   signée et mettre fin à la session d'un utilisateur authentifié en l'attirant vers cette URL.
   L'impact est une déconnexion forcée (déni de service), et non une prise de contrôle du compte.

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

Configuration du certificat SP et de la clé privée
---------------------------------------------------

Lorsque le SP signe les demandes d'authentification ou les messages de déconnexion (par ex. ``saml.security.authnrequest_signed``), ou demande le chiffrement des assertions ou du NameID (par ex. ``saml.security.want_assertions_encrypted``), vous devez configurer la clé privée et le certificat X.509 du SP.

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
   * - ``saml.strict``
     - Mode strict (effectuer une validation stricte)
     - ``true``
   * - ``saml.security.want_xml_validation``
     - Valider le schéma XML des messages
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Algorithme de signature
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - Contexte d'authentification demandé
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - Format du NameID
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| utilise en interne une bibliothèque SAML (java-saml), et les propriétés commençant par ``saml.`` sont mappées aux paramètres correspondants de la bibliothèque (préfixe ``onelogin.saml2.``).
   Ainsi, en plus de celles répertoriées ici, vous pouvez spécifier des paramètres détaillés dans ``system.properties`` tels que les liaisons (par ex. ``saml.sp.assertion_consumer_service.binding``), les informations d'organisation (``saml.organization.*``) et les informations de contact (``saml.contacts.*``).

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
Si aucune valeur n'est définie, 3600 secondes sont utilisées.
Si une valeur qui ne peut pas être interprétée comme un nombre est définie, 3600 secondes sont également utilisées et un avertissement commençant par ``Invalid saml.request.id.ttl`` est consigné.
Une valeur nulle ou négative écarterait l'identifiant de l'AuthnRequest avant qu'une connexion puisse revenir de l'IdP ; dans ce cas également, 3600 secondes sont utilisées et un avertissement est consigné.

.. note::
   Au maximum 10 AuthnRequest restées sans réponse sont conservées par session ; lorsque cette limite est dépassée, les plus anciennes sont écartées.
   Cela permet de démarrer des connexions depuis plusieurs onglets à la fois, et ne peut pas être modifié par un paramètre ``saml.``.
   Si la limite est remplacée par une valeur inférieure ou égale à zéro, la valeur 10 est utilisée à la place et un avertissement est consigné.

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

    # À activer après avoir vérifié que l'IdP signe avec SHA-256 ou plus fort
    saml.security.reject_deprecated_alg=true

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
  le navigateur n'envoie pas le cookie de session avec cette requête ; |Fess| ne trouve alors aucun
  identifiant d'AuthnRequest correspondant et fait échouer la connexion une seule fois, sur place. Le
  navigateur revient à la page de connexion en affichant « Le processus de connexion SSO a échoué. »,
  et un avertissement commençant par
  ``Received a SAML response with no matching AuthnRequest ID in the session`` est écrit dans le
  journal. Dans ce cas, définissez ``tomcat.sameSiteCookies = none`` (``SameSite=None`` nécessite HTTPS)
- Si la connexion a pris trop de temps chez l'IdP, l'identifiant d'AuthnRequest n'est plus présent
  lorsque l'assertion revient : la connexion échoue une seule fois et doit être recommencée.
  L'avertissement consigné indique ce qui a expiré : celui qui commence par
  ``Received a SAML response after the session it belongs to had expired`` signifie que le conteneur
  de servlets a supprimé la session entière, tandis que celui qui contient
  ``pending AuthnRequest ID(s) of the session had expired`` signifie que la session est toujours
  active et que seul ``saml.request.id.ttl`` a expiré. Les deux ne sont écrits que si le navigateur
  a bien envoyé son cookie de session, ce qui les distingue du cas SameSite ci-dessus
- |Fess| ne définit pas ``session-timeout`` dans ``app/WEB-INF/web.xml`` ; la valeur par défaut du
  conteneur de servlets, 30 minutes, s'applique donc, et elle est plus courte que les 3600 secondes
  de ``saml.request.id.ttl``. La session, et avec elle l'identifiant d'AuthnRequest qu'elle
  conserve, est écartée en premier : augmenter uniquement ``saml.request.id.ttl`` ne laisse pas plus
  de temps aux utilisateurs pour terminer la connexion chez l'IdP, il faut aussi allonger le délai
  d'expiration de session. L'avertissement relatif à ``saml.request.id.ttl`` n'apparaît donc que
  lorsque la TTL est réglée en dessous de ce délai

.. note::
   En 15.7, la même situation faisait rediriger |Fess| encore et encore vers l'IdP, mettant la connexion
   en boucle. En 15.8, elle échoue une seule fois au lieu de boucler. La solution de configuration reste
   la même.

La validation de Destination échoue derrière un proxy inverse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lorsque |Fess| s'exécute derrière un proxy inverse ou un répartiteur de charge qui termine TLS, la
validation de l'assertion peut échouer même si ``saml.sp.base.url`` est correctement défini.

La cause est que la bibliothèque SAML compare l'attribut ``Destination`` de l'assertion à l'URL de
requête reconstruite par le conteneur de servlets, et non à l'URL ACS configurée. Lorsque le proxy
termine HTTPS, l'URL de requête vue par |Fess| est une URL interne telle que
``http://<hôte-interne>:<port-interne>/sso/``, qui ne correspond pas à
``https://fess.example.com/sso/`` envoyée par l'IdP. ``saml.sp.base.url`` n'intervient pas dans cette
comparaison ; le définir seul ne résout donc pas le problème.

Définissez ``saml.debug=true`` pour que la raison soit écrite dans le journal :

::

    The response was received at http://... instead of https://fess.example.com/sso/

Alignez les paramètres du connecteur dans ``tomcat_config.properties`` sur le schéma et le port
visibles depuis l'extérieur. Ces paramètres sont livrés commentés :

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

Configurez également le proxy inverse pour qu'il transmette l'en-tête ``Host`` d'origine à |Fess|, car
la partie nom d'hôte de l'URL de requête est construite à partir de cet en-tête. |Fess| doit être
redémarré après modification de ``tomcat_config.properties``.

La même validation s'applique aux messages de déconnexion unique ; configurez-la également si vous
utilisez le SLO.

Erreur de vérification de signature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le certificat IdP est correctement configuré
- Assurez-vous que le certificat n'a pas expiré
- Le certificat doit être spécifié uniquement comme contenu encodé en Base64, sans sauts de ligne

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
- Activez le mode débogage pour inspecter le contenu de l'assertion SAML

Paramètres de débogage
----------------------

Pour investiguer les problèmes, vous pouvez activer le mode débogage avec le paramètre suivant :

::

    saml.debug=true

La configuration ``saml.debug=true`` enregistre dans le journal la raison détaillée lorsque l'authentification SAML échoue.

Vous pouvez également afficher des journaux détaillés liés à SAML en ajoutant le logger suivant dans ``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-oidc` - À propos de la configuration SSO avec OpenID Connect
- :doc:`sso-entraid` - À propos de la configuration SSO dédiée à Microsoft Entra ID
