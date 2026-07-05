==========================
Chat API
==========================

Vue d'ensemble
==============

La Chat API est une API v2 permettant d'accéder par programmation à la fonctionnalité de mode de recherche IA (chat RAG) de |Fess|.
Vous pouvez obtenir des réponses générées par un LLM basées sur les résultats de recherche (complétion).

Cette API fournit les trois points de terminaison suivants.

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - Point de terminaison
     - Description
   * - ``POST /chat``
     - Complétion RAG en mode groupé (non-streaming).
   * - ``POST /chat/stream``
     - Complétion RAG en mode streaming (Server-Sent Events).
   * - ``DELETE /chat/sessions/{session_id}``
     - Effacement de l'historique de conversation d'une session de chat.

Pour l'URL de base ainsi que l'enveloppe de réponse commune et les codes d'erreur, voir :doc:`api-overview`.

::

    http://<Server Name>/api/v2/

Exemple en environnement local :

::

    http://localhost:8080/api/v2

Prérequis
=========

Pour utiliser la Chat API, les conditions suivantes doivent être réunies.

1. La fonctionnalité de mode de recherche IA (chat RAG) doit être activée (``rag.chat.enabled=true``)
2. Un fournisseur LLM doit être configuré

Si la fonctionnalité est désactivée (``rag.chat.enabled=false``), les requêtes retournent une erreur ``invalid_request``.

Pour les méthodes de configuration détaillées, voir :doc:`../config/rag-chat` et :doc:`../config/llm-overview`.

Authentification et CSRF
=========================

Tous les points de terminaison de la Chat API étant des requêtes modifiant l'état (``POST`` / ``DELETE``), l'en-tête ``X-Fess-CSRF-Token`` est requis.
Pour les détails sur l'obtention du jeton CSRF ainsi que sur l'authentification et la session, voir :doc:`api-overview`.

Limite de débit
===============

``POST /chat`` , ``POST /chat/stream`` et ``DELETE /chat/sessions/{session_id}`` sont soumis à une limite de débit par utilisateur.

- Valeur par défaut : 30 requêtes par minute (par utilisateur)
- Clé de configuration : ``api.v2.chat.rate.limit.per.user.per.minute``
- Définir la valeur à ``0`` ou moins désactive la limite de débit.

En cas de dépassement, une erreur ``rate_limited`` (HTTP 429) est retournée. L'en-tête ``Retry-After`` est défini à une valeur fixe de ``60`` (secondes).
Cette limite de débit est partagée entre ``POST /chat`` , ``POST /chat/stream`` , ``DELETE /chat/sessions/{session_id}``.

.. note::

   La limite de débit s'applique uniquement lorsque l'utilisateur peut être identifié. Pour les appels anonymes où aucune session n'est établie et où l'identifiant de l'utilisateur ne peut pas être résolu, la limite de débit est ignorée.

POST /chat
==========

Effectue une complétion de chat synchrone.
La session est identifiée par ``session_id``. Si ``session_id`` est omis, le serveur crée une session et la retourne dans ``session_id`` de la réponse.

Les valeurs incorrectes transmises dans ``fields.label`` ou ``extra_queries`` sont silencieusement supprimées de la requête résolue et ne se propagent pas dans l'enveloppe de réponse.

Point de terminaison
--------------------

::

    POST /api/v2/chat

Corps de la requête
-------------------

Corps JSON avec ``Content-Type: application/json``.

La taille du corps de la requête est limitée à 32 KiB. La dépasser entraîne une erreur ``payload_too_large`` (HTTP 413).

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - Champ
     - Type
     - Obligatoire
     - Description
   * - ``message``
     - string
     - Oui
     - Message de l'utilisateur (question). La longueur maximale est limitée par ``rag.chat.message.max.length`` (valeur par défaut 4000). La dépasser entraîne une erreur ``invalid_request`` (HTTP 400).
   * - ``session_id``
     - string
     - Non
     - Identifiant de session. Si omis, le serveur le crée et le retourne dans la réponse.
   * - ``fields``
     - object
     - Non
     - Champs de filtre optionnels pour l'étape de récupération.
   * - ``fields.label``
     - string / string[]
     - Non
     - Restreint la récupération aux étiquettes figurant dans la liste d'autorisation.
   * - ``extra_queries``
     - string / string[]
     - Non
     - Expressions de requêtes de facette figurant dans la liste d'autorisation.

Exemple de requête :

.. code-block:: json

    {
      "message": "Fessとは何ですか？",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

Réponse
-------

**En cas de succès (HTTP 200, ChatResponse)**

La réponse est encapsulée dans l'enveloppe commune ``response``. ``session_id`` est toujours présent.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Éléments de response
   :header-rows: 1

   * - Champ
     - Type
     - Description
   * - ``session_id``
     - string
     - Identifiant de session.
   * - ``content``
     - string (nullable)
     - Texte du message généré. Toujours présent, mais peut valoir ``null`` si le modèle n'a pas produit de contenu.
   * - ``sources``
     - array
     - Tableau des documents sources référencés. Chaque élément est un ChatSource.

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Éléments de ChatSource
   :header-rows: 1

   * - Champ
     - Type
     - Description
   * - ``rank``
     - integer
     - Position à base 1 dans l'ensemble récupéré.
   * - ``title``
     - string (nullable)
     - Titre du document.
   * - ``url``
     - string (nullable)
     - URL du document.
   * - ``doc_id``
     - string (nullable)
     - Identifiant du document.
   * - ``snippet``
     - string (nullable)
     - Extrait du document.
   * - ``url_link``
     - string (nullable)
     - Lien URL d'affichage.
   * - ``go_url``
     - string (nullable)
     - URL de redirection.

Exemple de réponse :

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "content": "Fessは全文検索サーバーです。主な特徴として...",
        "sources": [
          {
            "rank": 1,
            "title": "Fessの概要",
            "url": "https://fess.codelibs.org/ja/overview.html",
            "doc_id": "abcdef0123456789",
            "snippet": "Fessは...",
            "url_link": "https://fess.codelibs.org/ja/overview.html",
            "go_url": "/go/?docId=abcdef0123456789"
          }
        ]
      }
    }

Codes de statut HTTP
--------------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Description
   * - 200
     - Requête réussie.
   * - 400
     - Requête incorrecte (``message`` manquant, longueur maximale de ``message`` dépassée, ``rag.chat.enabled=false``, etc.).
   * - 403
     - Jeton CSRF manquant ou expiré, etc.
   * - 405
     - La méthode HTTP n'est pas autorisée.
   * - 413
     - Le corps de la requête dépasse la limite de taille (32 KiB).
   * - 415
     - ``Content-Type`` n'est pas ``application/json``, est absent, ou le ``charset`` n'est pas UTF-8.
   * - 429
     - Limite de débit dépassée.
   * - 500
     - Erreur interne du serveur.

Exemple cURL
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessとは何ですか？","session_id":"abc123def456"}'

POST /chat/stream
=================

Effectue une complétion de chat en mode streaming.
Le corps de la requête est identique à ``POST /chat`` (ChatRequest).

La réponse de succès est une séquence d'événements nommés au format ``text/event-stream`` (Server-Sent Events).
Chaque événement est composé de ``event: <nom>`` et ``data: <JSON>``.

Les échecs de validation avant le démarrage du stream retournent toujours une enveloppe JSON (mêmes codes d'erreur que ``POST /chat``).
Les valeurs incorrectes dans ``fields.label`` ou ``extra_queries`` sont silencieusement supprimées et ne se propagent ni dans l'enveloppe de réponse ni dans les événements SSE.

Point de terminaison
--------------------

::

    POST /api/v2/chat/stream

Événements SSE
--------------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - Événement
     - Description (charge utile)
   * - ``phase``
     - Transition de phase du pipeline (``{ phase, status, message?, keywords?, hit_count?, ... }``). ``message`` et ``keywords`` sont émis lors de onPhaseStart. Les champs optionnels supplémentaires (ex. : ``hit_count``) proviennent de la charge utile de onPhaseComplete.
   * - ``chunk``
     - Fragment de texte généré (``{ content }``).
   * - ``sources``
     - Sources récupérées (``{ sources: [ChatSource] }``).
   * - ``retry``
     - Backoff d'échec temporaire (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``).
   * - ``waiting``
     - Progression d'une phase longue (``{ phase, reason, elapsed_ms, timeout_ms }``).
   * - ``fallback``
     - Réécriture de requête ou repli de stratégie (``{ phase, reason, original_query?, new_query? }``).
   * - ``warning``
     - Avertissement récupérable (``{ phase, code, detail? }``).
   * - ``done``
     - Fin du stream (``{ session_id, html_content? }``).
   * - ``error``
     - Échec terminal en cours de stream (``{ phase?, message, error_code }``). Le champ ``message`` contient la même chaîne que ``error_code``. Les clients doivent localiser en se basant sur ``error_code``.

Exemple de stream SSE :

::

    event: phase
    data: {"phase":"search","status":"start","message":"Searching documents...","keywords":"Fess インストール"}

    event: chunk
    data: {"content":"Fessは"}

    event: sources
    data: {"sources":[{"rank":1,"title":"インストールガイド","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

Codes de statut HTTP
--------------------

En cas d'échec de validation avant le démarrage du stream, les codes d'erreur suivants sont retournés dans une enveloppe JSON.

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Description
   * - 200
     - Démarrage du stream SSE (succès).
   * - 400
     - Requête incorrecte (``message`` manquant, ``rag.chat.enabled=false``, etc.).
   * - 403
     - Jeton CSRF manquant ou expiré, etc.
   * - 405
     - La méthode HTTP n'est pas autorisée.
   * - 413
     - Le corps de la requête dépasse la limite de taille (32 KiB).
   * - 415
     - ``Content-Type`` n'est pas ``application/json``, est absent, ou le ``charset`` n'est pas UTF-8.
   * - 429
     - Limite de débit dépassée.
   * - 500
     - Erreur interne du serveur.

Exemple cURL
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

DELETE /chat/sessions/{session_id}
===================================

Efface l'historique de conversation de la session de chat spécifiée.
La session est identifiée par ``session_id`` dans le chemin.

En cas de succès, ``cleared: true`` est retourné. Si aucune session active correspondante n'est trouvée, une erreur ``not_found`` (HTTP 404) est retournée.

Point de terminaison
--------------------

::

    DELETE /api/v2/chat/sessions/{session_id}

Paramètres de chemin
--------------------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - Paramètre
     - Type
     - Description
   * - ``session_id``
     - string
     - Identifiant de la session à effacer. minLength 1, maxLength 128, motif ``^[A-Za-z0-9._-]+$``.

Réponse
-------

**En cas de succès (HTTP 200, ChatClearResponse)**

La réponse est encapsulée dans l'enveloppe commune ``response``. ``session_id`` et ``cleared`` sont toujours présents.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Éléments de response
   :header-rows: 1

   * - Champ
     - Type
     - Description
   * - ``session_id``
     - string
     - Identifiant de session.
   * - ``cleared``
     - boolean
     - Toujours ``true`` (lorsque la session a été trouvée et effacée).

Exemple de réponse :

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

Codes de statut HTTP
--------------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Description
   * - 200
     - Session effacée avec succès.
   * - 400
     - La requête est incorrecte (par exemple, ``session_id`` ne correspond pas au motif ``^[A-Za-z0-9._-]+$`` ou à la limite de longueur de 1 à 128 caractères, ou ``rag.chat.enabled=false``).
   * - 403
     - Jeton CSRF manquant ou expiré, etc.
   * - 404
     - Aucune session active correspondante trouvée.
   * - 405
     - La méthode HTTP n'est pas autorisée.
   * - 429
     - Limite de débit dépassée.
   * - 500
     - Erreur interne du serveur.

Exemple cURL
------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

Sécurité
========

Points de sécurité à noter lors de l'utilisation de la Chat API :

1. **Authentification** : L'API v2 utilise une authentification basée sur les sessions. Pour plus de détails, voir :doc:`api-overview`.
2. **CSRF** : Les requêtes modifiant l'état nécessitent l'en-tête ``X-Fess-CSRF-Token``.
3. **Limite de débit** : Une limite de débit par utilisateur (30/minute par défaut) est appliquée pour prévenir les attaques DoS. La clé de configuration est ``api.v2.chat.rate.limit.per.user.per.minute``.

Informations de référence
=========================

- :doc:`../config/rag-chat` - Configuration de la fonctionnalité de mode de recherche IA
- :doc:`../config/llm-overview` - Vue d'ensemble de l'intégration LLM
- :doc:`../user/chat-search` - Guide de recherche par chat pour les utilisateurs
- :doc:`api-overview` - Vue d'ensemble de l'API
