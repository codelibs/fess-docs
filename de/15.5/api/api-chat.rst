==========================
Chat API
==========================

Übersicht
=========

Die Chat API ist eine RESTful API für den programmatischen Zugriff auf die AI-Modus-Funktion von |Fess|.
Sie können KI-gestützte Antworten basierend auf Suchergebnissen erhalten.

Diese API bietet zwei Endpunkte:

- **Nicht-Streaming-API**: Vollständige Antwort auf einmal abrufen
- **Streaming-API**: Antworten in Echtzeit über Server-Sent Events (SSE)

Voraussetzungen
===============

Um die Chat API zu verwenden, sind folgende Einstellungen erforderlich:

1. AI-Modus-Funktion ist aktiviert (``rag.chat.enabled=true``)
2. LLM-Provider ist konfiguriert

Für detaillierte Konfiguration siehe :doc:`../config/rag-chat`.

Nicht-Streaming-API
===================

Endpunkt
--------

::

    POST /api/v1/chat

Request-Parameter
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``message``
     - String
     - Ja
     - Benutzernachricht (Frage)
   * - ``sessionId``
     - String
     - Nein
     - Sitzungs-ID für Gespräch fortsetzen
   * - ``clear``
     - String
     - Nein
     - ``"true"`` um Sitzung zu löschen

Response
--------

**Erfolg (HTTP 200)**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fess ist ein Volltextsuchserver. Hauptmerkmale sind...",
      "sources": [
        {
          "title": "Fess Übersicht",
          "url": "https://fess.codelibs.org/de/overview.html"
        },
        {
          "title": "Funktionsliste",
          "url": "https://fess.codelibs.org/de/features.html"
        }
      ]
    }

**Fehler**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

HTTP-Statuscodes
----------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Beschreibung
   * - 200
     - Request erfolgreich
   * - 400
     - Ungültige Request-Parameter (z.B. message leer)
   * - 404
     - Endpunkt nicht gefunden
   * - 405
     - HTTP-Methode nicht erlaubt (nur POST erlaubt)
   * - 500
     - Interner Serverfehler

Verwendungsbeispiele
--------------------

cURL
~~~~

.. code-block:: bash

    # Neuen Chat starten
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Was ist Fess?"

    # Gespräch fortsetzen
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Wie installiere ich es?" \
         -d "sessionId=abc123def456"

    # Sitzung löschen
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

    // Verwendung
    const result = await chat('Erzähle mir über Fess-Funktionen');
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

    # Verwendung
    result = chat('Wie installiere ich Fess?')
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

Streaming-API
=============

Endpunkt
--------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

Request-Parameter
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``message``
     - String
     - Ja
     - Benutzernachricht (Frage)
   * - ``sessionId``
     - String
     - Nein
     - Sitzungs-ID für Gespräch fortsetzen

Response-Format
---------------

Die Streaming-API gibt Antworten im ``text/event-stream`` Format (Server-Sent Events) zurück.

Jedes Ereignis hat folgendes Format:

::

    event: <Ereignisname>
    data: <JSON-Daten>

SSE-Ereignisse
--------------

**session**

Übermittelt Sitzungsinformationen. Wird zu Beginn des Streams gesendet.

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

Benachrichtigt über Start/Ende einer Verarbeitungsphase.

.. code-block:: json

    {
      "phase": "search",
      "status": "start",
      "message": "Searching documents...",
      "keywords": "Fess Installation"
    }

Phasentypen:

- ``intent_analysis`` - Absichtsanalyse
- ``search`` - Suchausführung
- ``evaluation`` - Ergebnisbewertung
- ``generation`` - Antwortgenerierung

**chunk**

Übermittelt generierte Textfragmente.

.. code-block:: json

    {
      "content": "Fess ist"
    }

**sources**

Übermittelt Quelldokument-Informationen.

.. code-block:: json

    {
      "sources": [
        {
          "title": "Installationsanleitung",
          "url": "https://fess.codelibs.org/de/install.html"
        }
      ]
    }

**done**

Benachrichtigt über Verarbeitungsabschluss.

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fess ist ein Volltextsuchserver...</p>"
    }

**error**

Benachrichtigt über Fehler.

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

Verwendungsbeispiele
--------------------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Erzähle mir über Fess-Funktionen" \
         -H "Accept: text/event-stream" \
         --no-buffer

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

    # Verwendung
    for event in stream_chat('Erzähle mir über Fess-Funktionen'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

Fehlerbehandlung
================

Bei der Verwendung der API sollten Sie eine geeignete Fehlerbehandlung implementieren.

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

Rate Limiting
=============

Für die Chat API gelten Rate Limits.

Standardeinstellungen:

- 10 Anfragen pro Minute

Bei Überschreitung des Rate Limits wird HTTP 429 zurückgegeben.

Für Rate-Limit-Konfiguration siehe :doc:`../config/rag-chat`.

Sicherheit
==========

Sicherheitshinweise bei Verwendung der Chat API:

1. **Authentifizierung**: In der aktuellen Version ist keine Authentifizierung erforderlich, aber erwägen Sie in Produktionsumgebungen eine angemessene Zugriffskontrolle
2. **Rate Limiting**: Aktivieren Sie Rate Limiting zum Schutz vor DoS-Angriffen
3. **Eingabevalidierung**: Führen Sie auch clientseitig eine Eingabevalidierung durch
4. **CORS**: Überprüfen Sie bei Bedarf die CORS-Einstellungen

Referenzinformationen
=====================

- :doc:`../config/rag-chat` - AI-Modus-Funktionskonfiguration
- :doc:`../config/llm-overview` - LLM-Integration Übersicht
- :doc:`../user/chat-search` - Endbenutzer-Chat-Suchanleitung
- :doc:`api-overview` - API-Übersicht
