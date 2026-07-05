=======================
Vue d'ensemble de l'API
=======================


API fournies par |Fess|
=======================

Ce document décrit les API Web (v2) fournies par |Fess|.
En utilisant ces API, vous pouvez intégrer |Fess| comme serveur de recherche dans vos systèmes Web existants ou dans des applications monopage (SPA).

.. note::

   Dans |Fess| 15.8, l'API a été remaniée en **v2**. L'ancienne API de recherche JSON
   ``/api/v1`` et l'API de chat ont été supprimées et fusionnées dans ``/api/v2``.
   Les clients utilisant ``/api/v1`` doivent migrer vers ``/api/v2``.

URL de base
===========

Les points de terminaison de l'API v2 de |Fess| sont fournis à l'URL de base suivante.

::

    http://<Server Name>/api/v2/

Par exemple, dans un environnement local :

::

    http://localhost:8080/api/v2/

Enveloppe de réponse
====================

Toutes les réponses JSON de la v2 sont retournées dans une structure d'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` indique le résultat du traitement, en reprenant la convention de la v1.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Valeurs de status

   * - 0
     - Succès
   * - 1
     - Erreur client
   * - 9
     - Erreur système

Tableau : Valeurs de status

Notez que ``response.status >= 1`` correspond toujours à un code de statut HTTP ``400`` ou supérieur.

Noms des champs
---------------

Toutes les clés JSON — corps de requête, corps de réponse et données d'événements SSE inclus — utilisent le format ``snake_case``.

Réponse d'erreur
================

En cas d'erreur, un objet ``error`` est ajouté à l'enveloppe.

::

    {
      "response": {
        "status": 1,
        "error": {
          "code": "invalid_request",
          "message": "..."
        }
      }
    }

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Éléments de error

   * - code
     - Code d'erreur stable (``snake_case``). Il est recommandé que les clients localisent les messages en se basant sur cette valeur.
   * - message
     - Message d'erreur lisible par l'utilisateur (en anglais). Pour l'affichage, veuillez localiser côté client en vous basant sur ``code``.
   * - details
     - Objet facultatif contenant des informations structurées supplémentaires (peut être absent). Seuls certains points de terminaison l'incluent. Par exemple, :doc:`api-health` intègre un instantané du cluster du moteur de recherche sous ``error.details.engine``.

Tableau : Éléments de error

Codes d'erreur et codes de statut HTTP
---------------------------------------

Le code de statut HTTP par défaut est déterminé en fonction de ``error.code``.

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: Liste des codes d'erreur

   * - error.code
     - Statut HTTP
     - Description
   * - ``invalid_request``
     - 400
     - La requête est incorrecte.
   * - ``auth_required``
     - 401
     - Authentification requise ou informations d'authentification incorrectes.
   * - ``forbidden``
     - 403
     - Non autorisé (jeton CSRF manquant ou expiré, etc.).
   * - ``not_found``
     - 404
     - Ressource introuvable.
   * - ``method_not_allowed``
     - 405
     - Méthode HTTP non autorisée. Les méthodes acceptées sont listées dans l'en-tête ``Allow``.
   * - ``not_acceptable``
     - 406
     - Requête non acceptable.
   * - ``conflict``
     - 409
     - Conflit de ressource détecté.
   * - ``payload_too_large``
     - 413
     - Le corps de la requête dépasse la limite de taille.
   * - ``unsupported_media_type``
     - 415
     - ``Content-Type`` non pris en charge (la plupart des points de terminaison requièrent ``application/json``).
   * - ``rate_limited``
     - 429
     - Limite de débit dépassée. L'en-tête ``Retry-After`` indique le nombre de secondes d'attente.
   * - ``internal_error``
     - 500
     - Une erreur interne s'est produite sur le serveur.
   * - ``service_unavailable``
     - 503
     - Le service est temporairement indisponible.

Tableau : Liste des codes d'erreur

.. note::

   La réponse ``method_not_allowed`` est accompagnée d'un en-tête ``Allow``
   listant les méthodes HTTP acceptées.

Authentification et session
===========================

L'API v2 utilise une authentification basée sur les sessions.
La connexion s'effectue via ``POST /auth/login`` ; en cas de succès, une session est établie et un jeton CSRF est émis.
L'état d'authentification actuel peut être consulté via ``GET /auth/me``. Pour plus de détails, voir :doc:`api-auth`.

Les points de terminaison qui ne nécessitent pas de connexion, comme la recherche, peuvent être utilisés de manière anonyme (selon l'option « Connexion requise » des Paramètres système).

Jeton CSRF
----------

Les requêtes modifiant l'état (``POST`` / ``PUT`` / ``DELETE``) nécessitent l'en-tête ``X-Fess-CSRF-Token``.
Le jeton CSRF peut être obtenu de la manière suivante.

- Champ ``csrf_token`` dans la réponse de ``POST /auth/login``
- Réponse de ``GET /ui/config`` (champ ``csrf_token`` lorsque ``csrf_required=true``)

Le jeton est renouvelé à chaque connexion, déconnexion ou changement de mot de passe.

.. note::

   La vérification CSRF est effectuée **avant** l'authentification. Par conséquent,
   une requête de modification d'état sans session valide ni jeton CSRF valide recevra
   ``403 forbidden`` plutôt que ``401 auth_required``. ``/auth/login`` est exclu de la
   vérification CSRF car aucun jeton n'existe avant la connexion.

Format de streaming
===================

Certains points de terminaison retournent des réponses en format de streaming plutôt qu'en JSON ordinaire.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Formats de streaming

   * - Point de terminaison
     - Content-Type
     - Description
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events (SSE). Pour plus de détails, voir :doc:`api-chat`.
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON (chaque ligne est un document au format ``{"data":{...}}``. En cas d'échec en cours de stream, la dernière ligne sera ``{"error":{...}}``). Pour plus de détails, voir :doc:`api-search`.

Tableau : Formats de streaming

Types d'API
===========

|Fess| fournit les API v2 suivantes.

.. tabularcolumns:: |p{3cm}|p{4cm}|p{8cm}|
.. list-table::

   * - Type
     - Points de terminaison principaux
     - Description
   * - :doc:`search <api-search>`
     - ``/search`` , ``/documents/all``
     - API de recherche de documents et de récupération complète (défilement).
   * - :doc:`label <api-label>`
     - ``/labels``
     - API de récupération de la liste des étiquettes configurées.
   * - :doc:`suggest <api-suggest>`
     - ``/suggest-words``
     - API de récupération des mots suggérés.
   * - :doc:`popularword <api-popularword>`
     - ``/popular-words``
     - API de récupération des mots populaires.
   * - :doc:`related <api-related>`
     - ``/related-queries`` , ``/related-content``
     - API de récupération des requêtes associées et du contenu associé.
   * - :doc:`health <api-health>`
     - ``/health``
     - API de récupération de l'état du cluster du moteur de recherche.
   * - :doc:`auth <api-auth>`
     - ``/auth/login`` , ``/auth/logout`` , ``/auth/me`` , ``/auth/password``
     - API d'authentification et de gestion de session (connexion, déconnexion, récupération de l'état d'authentification, changement de mot de passe).
   * - :doc:`ui <api-uiconfig>`
     - ``/ui/config``
     - API de récupération de la configuration initiale (paramètres d'interface) pour les SPA.
   * - :doc:`favorite <api-favorite>`
     - ``/favorites`` , ``/documents/{docId}/favorite``
     - API de gestion des documents favoris.
   * - :doc:`click <api-click>`
     - ``/click``
     - API d'enregistrement des clics sur les résultats de recherche.
   * - :doc:`cache <api-cache>`
     - ``/cache/{docId}``
     - API de récupération du contenu en cache d'un document.
   * - :doc:`chat <api-chat>`
     - ``/chat`` , ``/chat/stream``
     - API d'accès à la fonctionnalité de mode de recherche IA (chat RAG).

Tableau : Types d'API
