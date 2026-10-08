======================================
Configuration SSO avec OpenID Connect
======================================

Vue d'ensemble
==============

|Fess| prend en charge l'authentification Single Sign-On (SSO) utilisant OpenID Connect (OIDC).
OpenID Connect est un protocole d'authentification basé sur OAuth 2.0 qui utilise des ID Tokens (JWT) pour l'authentification des utilisateurs.
En utilisant l'authentification OpenID Connect, les informations utilisateur authentifiées par un OpenID Provider (OP) peuvent être intégrées avec |Fess|.

.. note::
   La prise en charge de l'authentification OpenID Connect provient du plugin
   ``fess-sso-oidc``, qui ne fait pas partie de la distribution. Installez-le depuis la page
   **Système > Plugin** de l'écran d'administration ou avec
   ``bin/fess-setup install plugin fess-sso-oidc``. Le plugin s'appelle ``fess-sso-oidc`` alors
   que la valeur de ``sso.type`` reste ``oic``.
   Jusque-là, avec ``sso.type=oic``, toute requête vers ``/sso/`` est simplement redirigée vers
   la page de connexion.

Fonctionnement de l'authentification OpenID Connect
----------------------------------------------------

Dans l'authentification OpenID Connect, |Fess| fonctionne comme une Relying Party (RP) et collabore avec un OpenID Provider (OP) externe pour l'authentification.

1. L'utilisateur accède au endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige vers le endpoint d'autorisation de l'OP
3. L'utilisateur s'authentifie auprès de l'OP
4. L'OP redirige le code d'autorisation vers |Fess|
5. |Fess| utilise le code d'autorisation pour obtenir un ID Token depuis le endpoint de token
6. |Fess| vérifie les claims de l'ID Token (JWT), en extrait les informations utilisateur et connecte l'utilisateur

.. note::
   |Fess| utilise le flux de code d'autorisation (Authorization Code Flow). L'ID Token est obtenu directement depuis le endpoint de token via un canal arrière (communication serveur à serveur) entre |Fess| et l'OP, sans passer par le navigateur.
   |Fess| décode l'ID Token pour extraire les claims (``email``, ``groups``, etc.) et constituer les informations utilisateur, mais ne procède pas à la vérification cryptographique de la signature JWT. OpenID Connect Core l'autorise, car le token est reçu directement depuis le endpoint de token via TLS ; l'URL du endpoint de token (``oic.token.server.url``) doit donc être en HTTPS. ``http`` n'est accepté que pour ``localhost``, ``127.x.x.x`` et ``::1``.
   |Fess| vérifie en revanche les claims : ``aud`` doit contenir ``oic.client.id`` (et ``azp``, lorsqu'il est présent, doit lui être égal), ``exp`` doit être présent et ne pas être dépassé (un décalage d'horloge pouvant atteindre 300 secondes est toléré), et ``iss`` doit être égal à ``oic.issuer`` lorsque cette clé est définie. Sans ``oic.issuer``, ``iss`` n'est pas vérifié et un avertissement est journalisé lors de la première connexion après chaque démarrage. ``nonce`` et PKCE ne sont pas utilisés.

Pour l'intégration avec la recherche basée sur les rôles, voir :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification OpenID Connect, vérifiez les prérequis suivants :

- |Fess| 15.9 ou supérieur est installé
- Un fournisseur compatible OpenID Connect (OP) est disponible
- |Fess| est accessible via HTTPS (requis pour les environnements de production)
- Vous avez la permission d'enregistrer |Fess| comme client (RP) côté OP

Exemples de fournisseurs pris en charge :

- Microsoft Entra ID (Azure AD)
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- Autres fournisseurs compatibles OpenID Connect

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification OpenID Connect, ajoutez le paramètre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=oic

.. note::
   ``sso.type`` ainsi que les paramètres ``oic.*`` décrits ci-après, à l'exception de ``oic.issuer``, peuvent également être configurés et modifiés depuis la page « Système > Général » de l'interface d'administration.
   Les paramètres modifiés dans l'interface d'administration sont enregistrés dans ``system.properties`` et sont conservés après redémarrage.
   ``oic.issuer`` ne peut être défini que dans ``system.properties``.

Configuration du fournisseur
----------------------------

Configurez les informations obtenues de votre OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.auth.server.url``
     - URL du endpoint d'autorisation
     - ``https://accounts.google.com/o/oauth2/auth``
   * - ``oic.token.server.url``
     - URL du endpoint de token
     - ``https://accounts.google.com/o/oauth2/token``
   * - ``oic.issuer``
     - Identifiant de l'émetteur (optionnel). Lorsqu'il est défini, le claim ``iss`` de l'ID Token doit lui être strictement égal (une barre oblique finale compte)
     - (vide : ``iss`` n'est pas vérifié)

.. note::
   Ces URLs et l'émetteur peuvent être obtenus depuis le endpoint Discovery de l'OP (``/.well-known/openid-configuration``) ; l'émetteur correspond à sa valeur ``issuer``. L'URL du endpoint de token doit être en HTTPS.

Configuration du client
-----------------------

Configurez les informations client enregistrées auprès de l'OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.client.id``
     - ID client
     - (vide)
   * - ``oic.client.secret``
     - Secret client
     - (vide)
   * - ``oic.scope``
     - Scopes demandés
     - (vide)

.. note::
   Le scope doit inclure au moins ``openid``.
   Pour récupérer l'adresse e-mail de l'utilisateur, spécifiez ``openid email``.

Configuration de l'URL de redirection
--------------------------------------

Configurez l'URL de callback après l'authentification.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.redirect.url``
     - URL de redirection (URL de callback)
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - URL de base de |Fess|
     - ``http://localhost:8080``

.. note::
   Si ``oic.redirect.url`` est omis, il est automatiquement construit à partir de ``oic.base.url``.
   Pour les environnements de production, définissez ``oic.base.url`` sur une URL HTTPS.

Configuration des attributs utilisateur
----------------------------------------

Configurez les groupes et rôles par défaut à attribuer aux utilisateurs authentifiés via OIDC.
L'identifiant utilisateur, les groupes et les rôles sont déterminés comme suit :

- **Identifiant utilisateur** : extrait du claim ``email`` de l'ID Token (JWT). Pour cette raison, le scope doit en pratique inclure ``email`` (si le claim ``email`` ne peut pas être obtenu, la connexion ne s'effectuera pas correctement).
- **Groupes** : extraits du claim ``groups`` de l'ID Token. Si le claim ``groups`` est absent, la valeur de ``oic.default.groups`` est utilisée. Un tableau ``groups`` vide est considéré comme présent : ``oic.default.groups`` n'est alors pas utilisé et l'utilisateur est traité comme n'ayant aucun groupe.
- **Rôles** : la valeur de ``oic.default.roles`` est toujours utilisée (il n'existe pas de mécanisme permettant d'extraire les rôles depuis les claims de l'ID Token).

.. note::
   |Fess| utilise telles quelles les valeurs du claim ``groups`` : aucune interrogation de
   l'annuaire n'est effectuée et les groupes imbriqués (transitifs) ne sont pas développés.
   La présence des groupes parents dépend donc uniquement de la configuration des claims de l'OP,
   contrairement à :doc:`sso-entraid`, où |Fess| résout les groupes parents en utilisant l'API
   Microsoft Graph.
   La valeur du claim devient telle quelle la permission de recherche. Si l'OP est configuré pour
   émettre les chemins de groupe complets, il envoie des valeurs comme ``/parent/enfant``, qui ne
   correspondent pas aux documents étiquetés avec le seul nom du groupe.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``oic.default.groups``
     - Groupes par défaut (séparés par des virgules)
     - (vide)
   * - ``oic.default.roles``
     - Rôles par défaut (séparés par des virgules)
     - (vide)

.. note::
   Pour utiliser la recherche basée sur les rôles, vous devez attribuer des groupes ou des rôles appropriés aux utilisateurs.
   Pour plus de détails, voir :doc:`security-role`.

Configuration côté OP
=====================

Lors de l'enregistrement de |Fess| comme client (RP) côté OP, configurez les informations suivantes :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Valeur
   * - Type d'application
     - Application web
   * - URI de redirection / URL de callback
     - ``https://<Hôte Fess>/sso/``
   * - Scopes autorisés
     - ``openid`` et les scopes requis (``email``, ``profile``, etc.)

Informations à obtenir de l'OP
-------------------------------

Obtenez les informations suivantes depuis l'écran de configuration ou le endpoint Discovery de l'OP pour la configuration de |Fess| :

- **Endpoint d'autorisation (Authorization Endpoint)** : URL pour initier l'authentification utilisateur
- **Endpoint de token (Token Endpoint)** : URL pour obtenir les tokens
- **Issuer** (optionnel) : valeur ``issuer`` du document Discovery, utilisée pour ``oic.issuer``
- **ID client** : Identifiant client émis par l'OP
- **Secret client** : Clé secrète utilisée pour l'authentification du client

.. note::
   La plupart des OP vous permettent de vérifier les URLs des endpoints d'autorisation et de token depuis le
   endpoint Discovery (``https://<OP>/.well-known/openid-configuration``).

Exemples de configuration
=========================

Configuration minimale (pour les tests)
----------------------------------------

Voici un exemple de configuration minimale pour la vérification dans un environnement de test.

::

    # Activer SSO
    sso.type=oic

    # Configuration du fournisseur (définir les valeurs obtenues de l'OP)
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Configuration du client
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # URL de redirection (environnement de test)
    oic.redirect.url=http://localhost:8080/sso/

Configuration recommandée (pour la production)
-----------------------------------------------

Voici un exemple de configuration recommandée pour les environnements de production.

::

    # Activer SSO
    sso.type=oic

    # Configuration du fournisseur
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Issuer (la valeur « issuer » du document Discovery)
    oic.issuer=https://op.example.com

    # Configuration du client
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # URL de base (utiliser HTTPS pour la production)
    oic.base.url=https://fess.example.com

Dépannage
=========

Problèmes courants et solutions
--------------------------------

Impossible de retourner à |Fess| après l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'URI de redirection est correctement configurée côté OP
- Assurez-vous que la valeur de ``oic.redirect.url`` ou ``oic.base.url`` correspond à la configuration de l'OP
- Vérifiez que le protocole (HTTP/HTTPS) correspond

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'ID client et le secret client sont correctement configurés
- Assurez-vous que le scope inclut ``openid``
- Vérifiez que l'URL du endpoint d'autorisation et l'URL du endpoint de token sont correctes
- Si la connexion échoue, ``fess.log`` contient un avertissement ``Failed to process the OpenID Connect callback:`` suivi du motif
- ``The ID token was not issued for this client`` : le claim ``aud`` de l'ID Token n'est pas ``oic.client.id`` ; vérifiez l'ID client
- ``The ID token has expired`` : les horloges de l'hôte |Fess| et de l'OP diffèrent de plus de 300 secondes ; synchronisez l'heure (NTP)
- ``The ID token was not issued by the configured issuer`` : ``oic.issuer`` diffère du ``iss`` indiqué dans le message ; copiez exactement la valeur ``issuer`` du document Discovery
- ``oic.token.server.url must be https`` : utilisez une URL de endpoint de token en HTTPS (``http`` ne fonctionne que pour ``localhost``, ``127.x.x.x`` et ``::1``)

Impossible de récupérer les informations utilisateur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Assurez-vous que le scope inclut les permissions requises (``email``, ``profile``, etc.)
- Vérifiez que les scopes requis sont autorisés pour le client côté OP
- Avec Microsoft Entra ID, le claim ``groups`` contient les ``ObjectId`` (GUID) des groupes, sauf
  si un autre attribut source est sélectionné ; les valeurs ne correspondent donc pas aux noms de
  groupe
- Microsoft Entra ID omet entièrement le claim ``groups`` lorsque l'utilisateur appartient à plus
  de 200 groupes (les groupes imbriqués comptent dans cette limite) ; |Fess| se rabat alors sur
  ``oic.default.groups``

Configuration de débogage
--------------------------

Pour investiguer les problèmes, vous pouvez afficher des logs détaillés liés à OpenID Connect en ajustant le niveau de log de |Fess|.

Dans ``app/WEB-INF/classes/log4j2.xml``, vous pouvez ajouter le logger suivant pour changer le niveau de log :

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

.. warning::
   Avec ce logger en DEBUG, les claims de l'ID Token (``email``, ``groups``, etc.) sont écrits dans
   le fichier de log. Rétablissez le niveau de log une fois l'investigation terminée et traitez la
   sortie de log en conséquence.

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-entraid` - Configuration SSO dédiée à Microsoft Entra ID (si vous utilisez Entra ID, vous pouvez opter pour cette configuration dédiée plutôt que la configuration OpenID Connect générique)
