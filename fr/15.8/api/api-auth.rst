=====================================
API d'authentification et de session
=====================================

Vue d'ensemble
==============

L'API v2 utilise une authentification basée sur les sessions.
La connexion s'effectue via ``POST /auth/login`` ; en cas de succès, une session est établie et un jeton CSRF est émis.

Les requêtes modifiant l'état (``POST``) nécessitent l'en-tête ``X-Fess-CSRF-Token``.
Pour les détails sur l'obtention et le renouvellement du jeton CSRF, ainsi que pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

Cette page décrit les quatre points de terminaison suivants.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Liste des points de terminaison
   :header-rows: 1
   :widths: 25 15 60

   * - Point de terminaison
     - Méthode
     - Description
   * - ``/auth/me``
     - GET
     - Récupère l'utilisateur authentifié courant.
   * - ``/auth/login``
     - POST
     - Se connecte avec un nom d'utilisateur et un mot de passe.
   * - ``/auth/logout``
     - POST
     - Se déconnecte (idempotent).
   * - ``/auth/password``
     - POST
     - Modifie le mot de passe de l'utilisateur courant.

.. _api-auth-userpayload:

Informations utilisateur communes (UserPayload)
================================================

Les informations utilisateur incluses dans les réponses de ``GET /auth/me`` et ``POST /auth/login`` sont retournées dans la structure commune ``UserPayload``.
Tous les champs de type tableau sont non-nuls ; un tableau vide est retourné s'il n'y a pas de valeur.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Description
   * - ``user_id``
     - string
     - Identifiant de l'utilisateur. (Obligatoire)
   * - ``username``
     - string
     - Nom d'utilisateur affiché dans le menu de compte de la SPA. Actuellement identique à ``user_id``, mais peut être fourni indépendamment par le backend à l'avenir. (Obligatoire)
   * - ``name``
     - string
     - Nom d'affichage pour le menu de compte de la SPA. Actuellement identique à ``user_id``. (Obligatoire)
   * - ``roles``
     - string[]
     - Tableau des rôles de l'utilisateur. (Obligatoire)
   * - ``groups``
     - string[]
     - Tableau des groupes de l'utilisateur. (Obligatoire)
   * - ``permissions``
     - string[]
     - Tableau des permissions de l'utilisateur. (Obligatoire)
   * - ``editable``
     - boolean
     - Indique si les informations utilisateur sont modifiables. (Obligatoire)
   * - ``admin``
     - boolean
     - Vaut ``true`` lorsque l'utilisateur possède l'un des rôles configurés dans ``authentication.admin.roles``. Contrôle l'affichage de l'élément « Administration » dans la SPA. (Obligatoire)

Récupération de l'état d'authentification
==========================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/auth/me``
====================  ====================================================

Récupère l'utilisateur authentifié courant.
Pour les appels anonymes, aucune erreur n'est retournée : ``authenticated: false`` est renvoyé.
Lorsque l'utilisateur est authentifié, ``user`` contient un :ref:`UserPayload <api-auth-userpayload>`.

Réponse
-------

En cas de succès (HTTP 200), une réponse au format d'enveloppe commune est retournée (exemple d'utilisateur authentifié).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "authenticated": true,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        }
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Informations de réponse
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Description
   * - ``authenticated``
     - boolean
     - Indique si l'utilisateur est authentifié. (Obligatoire)
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`. Présent uniquement si ``authenticated`` vaut ``true``.

Réponse d'erreur
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur
   :header-rows: 1
   :widths: 25 75

   * - Code de statut
     - Description
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Connexion
=========

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/auth/login``
====================  ====================================================

Se connecte avec un nom d'utilisateur et un mot de passe.
En cas de succès, l'identifiant de session du servlet est renouvelé, un nouveau jeton CSRF est émis, et les buckets de limite de débit de l'IP appelante et de l'utilisateur cible sont réinitialisés.

La limitation de débit est appliquée selon deux axes : par IP appelante et par utilisateur. Lorsque la limite par IP est dépassée, ``429 Too Many Requests`` est retourné accompagné d'un en-tête ``Retry-After`` (en secondes). Lorsque la limite par utilisateur est dépassée, le même ``401 Unauthorized`` que pour des informations d'identification invalides est retourné (sans en-tête ``Retry-After``), afin que l'état du compteur ne puisse pas être déduit de l'extérieur.

Même pour une session déjà authentifiée, aucun court-circuit n'est appliqué : les informations d'authentification transmises sont toujours vérifiées.

``return_to`` doit être un chemin relatif correspondant à ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$``.
De plus, les chemins relatifs aux protocoles (commençant par ``//``) et les chemins contenant des caractères de contrôle ASCII sont rejetés et silencieusement supprimés de la réponse.

.. note::

   Ce point de terminaison est **exclu de la vérification CSRF** (car aucun jeton n'existe avant la connexion).

.. note::

   Contrairement aux autres points de terminaison de modification d'état, ce point de terminaison regroupe les corps de requête trop grands et les ``Content-Type`` non pris en charge dans ``400 invalid_request`` (les autres points de terminaison retournent ``413`` / ``415``).

.. note::

   Les limites de débit pour la connexion et le changement de mot de passe peuvent être configurées avec les propriétés suivantes (valeurs par défaut entre parenthèses) :

   - ``theme.api.login.rate.limit.per.ip.per.minute`` (``10``) : Nombre maximal de tentatives par minute par adresse IP. S'applique uniquement à ``/auth/login``.
   - ``theme.api.login.rate.limit.per.user.per.minute`` (``5``) : Nombre maximal de tentatives par minute par utilisateur. S'applique à la fois à ``/auth/login`` et à ``/auth/password``.
   - ``theme.api.login.lockout.seconds`` (``900``) : Durée de verrouillage (en secondes) après dépassement de la limite. Retournée comme valeur de l'en-tête ``Retry-After``.

Corps de la requête (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le Content-Type est ``application/json`` (charset UTF-8). La taille maximale du corps de la requête est de 4 KiB.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - Champ
     - Type
     - Obligatoire
     - Description
   * - ``username``
     - string
     - Oui
     - Nom d'utilisateur. ``minLength`` : 1.
   * - ``password``
     - string
     - Oui
     - Mot de passe. ``minLength`` : 1.
   * - ``return_to``
     - string
     - Non
     - Chemin de redirection après connexion. Doit être un chemin relatif correspondant au motif ci-dessus.

Exemple de requête :

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

Réponse
-------

En cas de succès (HTTP 200, LoginResponse), une réponse au format d'enveloppe commune est retournée.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Informations de réponse
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Description
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`.
   * - ``csrf_token``
     - string
     - Nouveau jeton CSRF associé à la nouvelle session. (Obligatoire)
   * - ``return_to``
     - string
     - Renvoyé uniquement si la valeur de la requête a passé la liste d'autorisation.

Réponse d'erreur
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur
   :header-rows: 1
   :widths: 25 75

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte (corps trop grand ou ``Content-Type`` non pris en charge inclus).
   * - 401 Unauthorized
     - Les informations d'authentification sont incorrectes.
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée.
   * - 429 Too Many Requests
     - Limite de débit dépassée. L'en-tête ``Retry-After`` indique le nombre de secondes d'attente.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Déconnexion
===========

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/auth/logout``
====================  ====================================================

Déconnecte l'utilisateur. Cette opération est idempotente : en l'absence de session active, elle ne fait rien et ne retourne pas d'erreur. Retourne toujours ``ok: true``.

L'en-tête ``X-Fess-CSRF-Token`` est requis.

Réponse
-------

En cas de succès (HTTP 200, OkResponse), une réponse au format d'enveloppe commune est retournée.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Informations de réponse
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Description
   * - ``ok``
     - boolean
     - Toujours ``true``. (Obligatoire)

Réponse d'erreur
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur
   :header-rows: 1
   :widths: 25 75

   * - Code de statut
     - Description
   * - 403 Forbidden
     - Jeton CSRF manquant ou expiré.
   * - 405 Method Not Allowed
     - Une méthode autre que POST a été spécifiée. Un en-tête ``Allow: POST`` est ajouté.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Changement de mot de passe
===========================

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/auth/password``
====================  ====================================================

Modifie le mot de passe de l'utilisateur courant.
Valide ``current_password``, applique la politique de mot de passe configurée à ``new_password``, invalide la session courante et invite la SPA à rediriger vers la page de connexion via ``re_login_required: true``.

Comme la session est détruite côté serveur, ``csrf_token`` n'est pas retourné. La SPA doit obtenir un nouveau jeton après une nouvelle authentification.

L'en-tête ``X-Fess-CSRF-Token`` est requis.

Une limite de débit par utilisateur est appliquée à ce point de terminaison ; lorsque la limite est dépassée, ``429 Too Many Requests`` est retourné accompagné d'un en-tête ``Retry-After`` (les paramètres sont partagés avec la connexion).

Corps de la requête (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le Content-Type est ``application/json`` (charset UTF-8). La taille maximale du corps de la requête est de 4 KiB.

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - Champ
     - Type
     - Obligatoire
     - Description
   * - ``current_password``
     - string
     - Oui
     - Mot de passe actuel. ``minLength`` : 1.
   * - ``new_password``
     - string
     - Oui
     - Nouveau mot de passe. Doit satisfaire la politique de mot de passe configurée (minimum 8 caractères par défaut). ``minLength`` : 1.
   * - ``confirm_password``
     - string
     - Oui
     - Mot de passe de confirmation. Doit être identique à ``new_password``. ``minLength`` : 1.

Réponse
-------

En cas de succès (HTTP 200), une réponse au format d'enveloppe commune est retournée.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Informations de réponse
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Description
   * - ``ok``
     - boolean
     - Toujours ``true``. (Obligatoire)
   * - ``re_login_required``
     - boolean
     - Toujours ``true``. La session courante a été invalidée côté serveur. La SPA doit rediriger vers la page de connexion pour obtenir une nouvelle session et un nouveau jeton CSRF. (Obligatoire)

Réponse d'erreur
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur
   :header-rows: 1
   :widths: 25 75

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte.
   * - 401 Unauthorized
     - Authentification requise ou ``current_password`` incorrect.
   * - 403 Forbidden
     - Jeton CSRF manquant ou expiré.
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée.
   * - 413 Payload Too Large
     - Le corps de la requête dépasse la limite de taille.
   * - 415 Unsupported Media Type
     - ``Content-Type`` non pris en charge.
   * - 429 Too Many Requests
     - Limite de débit dépassée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.
