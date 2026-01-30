==========================
API Chat
==========================

Apercu
====

L'API Chat est une API RESTful permettant d'acceder par programmation a la fonctionnalite de chat RAG de |Fess|.
Vous pouvez obtenir des reponses assistees par IA basees sur les resultats de recherche.

Cette API fournit deux endpoints :

- **API non-streaming** : Obtient la reponse complete en une seule fois
- **API streaming** : Obtient la reponse en temps reel au format Server-Sent Events (SSE)

Prerequis
========

Pour utiliser l'API Chat, les configurations suivantes sont necessaires :

1. La fonctionnalite de chat RAG doit etre activee (``rag.chat.enabled=true``)
2. Un fournisseur LLM doit etre configure

Pour les methodes de configuration detaillees, consultez :doc:`../config/rag-chat`.

API non-streaming
===================

Endpoint
--------------

::

    POST /api/v1/chat

Parametres de requete
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``message``
     - String
     - Oui
     - Message de l'utilisateur (question)
   * - ``sessionId``
     - String
     - Non
     - ID de session. A specifier pour continuer une conversation
   * - ``clear``
     - String
     - Non
     - Specifier ``"true"`` pour effacer la session

Reponse
----------

**Succes (HTTP 200)**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fess est un serveur de recherche full-text. Ses principales caracteristiques sont...",
      "sources": [
        {
          "title": "Apercu de Fess",
          "url": "https://fess.codelibs.org/ja/overview.html"
        },
        {
          "title": "Liste des fonctionnalites",
          "url": "https://fess.codelibs.org/ja/features.html"
        }
      ]
    }

**Erreur**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

Codes de statut HTTP
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Requete reussie
   * - 400
     - Parametre de requete invalide (message vide, etc.)
   * - 404
     - Endpoint non trouve
   * - 405
     - Methode HTTP non autorisee (seul POST est autorise)
   * - 500
     - Erreur interne du serveur

Exemples d'utilisation
------

cURL
~~~~

.. code-block:: bash

    # Demarrer un nouveau chat
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Qu'est-ce que Fess ?"

    # Continuer la conversation
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Comment l'installer ?" \
         -d "sessionId=abc123def456"

    # Effacer la session
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "sessionId=abc123def456" \
         -d "clear=true"

JavaScript
~~~~~~~~~~

.. code-block:: javascript

    async function chat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        body: params
      });

      return await response.json();
    }

    // Exemple d'utilisation
    const result = await chat('Quelles sont les fonctionnalites de Fess ?');
    console.log(result.content);
    console.log('Session ID:', result.sessionId);

Python
~~~~~~

.. code-block:: python

    import requests

    def chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat',
            data=data
        )
        return response.json()

    # Exemple d'utilisation
    result = chat("Comment installer Fess ?")
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

API streaming
=================

Endpoint
--------------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

Parametres de requete
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``message``
     - String
     - Oui
     - Message de l'utilisateur (question)
   * - ``sessionId``
     - String
     - Non
     - ID de session. A specifier pour continuer une conversation

Format de reponse
--------------

L'API streaming retourne les reponses au format ``text/event-stream`` (Server-Sent Events).

Chaque evenement est dans le format suivant :

::

    event: <nom de l'evenement>
    data: <donnees JSON>

Evenements SSE
-----------

**session**

Notifie les informations de session. Envoye au debut du stream.

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

Notifie le debut/fin des phases de traitement.

.. code-block:: json

    {
      "phase": "intent_analysis",
      "status": "start",
      "message": "Analyzing user intent..."
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "start",
      "message": "Searching documents...",
      "keywords": "Fess installation"
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "complete"
    }

Types de phases :

- ``intent_analysis`` - Analyse d'intention
- ``search`` - Execution de la recherche
- ``evaluation`` - Evaluation des resultats
- ``generation`` - Generation de la reponse

**chunk**

Notifie les fragments de texte genere.

.. code-block:: json

    {
      "content": "Fess est"
    }

**sources**

Notifie les informations sur les documents sources.

.. code-block:: json

    {
      "sources": [
        {
          "title": "Guide d'installation",
          "url": "https://fess.codelibs.org/ja/install.html"
        }
      ]
    }

**done**

Notifie la fin du traitement.

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fess est un serveur de recherche full-text...</p>"
    }

**error**

Notifie une erreur.

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

Exemples d'utilisation
------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Quelles sont les caracteristiques de Fess ?" \
         -H "Accept: text/event-stream" \
         --no-buffer

JavaScript (EventSource)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    function streamChat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      // Utiliser fetch pour les requetes POST
      return fetch('/api/v1/chat/stream', {
        method: 'POST',
        body: params
      }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function read() {
          return reader.read().then(({ done, value }) => {
            if (done) return;

            const text = decoder.decode(value);
            const lines = text.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                handleEvent(data);
              }
            }

            return read();
          });
        }

        return read();
      });
    }

    function handleEvent(data) {
      if (data.content) {
        // Afficher le chunk
        document.getElementById('output').textContent += data.content;
      } else if (data.phase) {
        // Afficher les informations de phase
        console.log(`Phase: ${data.phase} - ${data.status}`);
      } else if (data.sources) {
        // Afficher les informations sources
        console.log('Sources:', data.sources);
      }
    }

Python
~~~~~~

.. code-block:: python

    import requests

    def stream_chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat/stream',
            data=data,
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    import json
                    data = json.loads(line[6:])
                    yield data

    # Exemple d'utilisation
    for event in stream_chat('Parlez-moi des fonctionnalites de Fess'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

Gestion des erreurs
==================

Lors de l'utilisation de l'API, implementez une gestion des erreurs appropriee.

.. code-block:: javascript

    async function chatWithErrorHandling(message, sessionId = null) {
      try {
        const params = new URLSearchParams();
        params.append('message', message);
        if (sessionId) {
          params.append('sessionId', sessionId);
        }

        const response = await fetch('/api/v1/chat', {
          method: 'POST',
          body: params
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'API request failed');
        }

        const result = await response.json();

        if (result.status === 'error') {
          throw new Error(result.message);
        }

        return result;

      } catch (error) {
        console.error('Chat API error:', error);
        throw error;
      }
    }

Limitation de debit
==========

L'API Chat est soumise a une limitation de debit.

Configuration par defaut :

- 10 requetes par minute

Lorsque la limite de debit est depassee, une erreur HTTP 429 est retournee.

Pour la configuration de la limitation de debit, consultez :doc:`../config/rag-chat`.

Securite
============

Points de securite a noter lors de l'utilisation de l'API Chat :

1. **Authentification** : La version actuelle ne necessite pas d'authentification pour l'API, mais envisagez un controle d'acces approprie pour les environnements de production
2. **Limitation de debit** : Activez la limitation de debit pour prevenir les attaques DoS
3. **Validation des entrees** : Validez egalement les entrees cote client
4. **CORS** : Verifiez les parametres CORS si necessaire

Informations de reference
========

- :doc:`../config/rag-chat` - Configuration de la fonctionnalite de chat RAG
- :doc:`../config/llm-overview` - Apercu de l'integration LLM
- :doc:`../user/chat-search` - Guide de recherche par chat pour les utilisateurs
- :doc:`api-overview` - Apercu des API
