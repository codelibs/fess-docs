========
Chat-API
========

Übersicht
=========

Die Chat-API ist eine v2-API für den programmatischen Zugriff auf den KI-Suchmodus (RAG-Chat) von |Fess|.
Sie ermöglicht den Abruf von LLM-basierten Antworten (Vervollständigungen) auf Basis von Suchergebnissen.

Diese API stellt drei Endpunkte bereit:

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - Endpunkt
     - Beschreibung
   * - ``POST /chat``
     - Gebündelte (nicht-streaming) RAG-Chat-Vervollständigung.
   * - ``POST /chat/stream``
     - Streaming-RAG-Chat-Vervollständigung (Server-Sent Events).
   * - ``DELETE /chat/sessions/{session_id}``
     - Löscht den Gesprächsverlauf einer Chat-Sitzung.

Informationen zur Basis-URL sowie zum gemeinsamen Antwort-Envelope und zu Fehlercodes finden Sie unter :doc:`api-overview`.

::

    http://<Server Name>/api/v2/

Beispiel für eine lokale Umgebung:

::

    http://localhost:8080/api/v2

Voraussetzungen
===============

Für die Verwendung der Chat-API sind folgende Einstellungen erforderlich:

1. Der KI-Suchmodus (RAG-Chat) muss aktiviert sein (``rag.chat.enabled=true``).
2. Ein LLM-Anbieter muss konfiguriert sein.

Wenn die Funktion deaktiviert ist (``rag.chat.enabled=false``), wird die Anfrage mit einem ``invalid_request``-Fehler beantwortet.

Detaillierte Konfigurationsanweisungen finden Sie unter :doc:`../config/rag-chat` und :doc:`../config/llm-overview`.

Authentifizierung und CSRF
==========================

Da alle Endpunkte der Chat-API zustandsändernde Anfragen (``POST`` / ``DELETE``) sind, ist der ``X-Fess-CSRF-Token``-Header erforderlich.
Informationen zum Abrufen des CSRF-Tokens sowie zu Authentifizierung und Sitzungen finden Sie unter :doc:`api-overview`.

Rate-Limiting
=============

Für ``POST /chat`` , ``POST /chat/stream`` und ``DELETE /chat/sessions/{session_id}`` gilt ein benutzerspezifisches Rate-Limit.

- Standardwert: 30 Anfragen pro Minute (pro Benutzer)
- Konfigurationsschlüssel: ``api.v2.chat.rate.limit.per.user.per.minute``

Bei Überschreitung des Rate-Limits wird der Fehler ``rate_limited`` (HTTP 429) zurückgegeben. Der ``Retry-After``-Header gibt die Wartezeit in Sekunden an.
Dieses Rate-Limit wird zwischen ``POST /chat`` , ``POST /chat/stream`` , ``DELETE /chat/sessions/{session_id}`` geteilt.

POST /chat
==========

Führt eine synchrone Chat-Vervollständigung durch.
Sitzungen werden durch ``session_id`` identifiziert. Wenn ``session_id`` weggelassen wird, erstellt der Server eine Sitzung und gibt sie als ``session_id`` in der Antwort zurück.

Ungültige Werte in ``fields.label`` oder ``extra_queries`` werden stillschweigend aus der aufgelösten Anfrage entfernt und sind im Antwort-Envelope nicht sichtbar.

Endpunkt
--------

::

    POST /api/v2/chat

Anfrage-Body
------------

JSON-Body mit ``Content-Type: application/json``.

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - Feld
     - Typ
     - Pflicht
     - Beschreibung
   * - ``message``
     - string
     - Ja
     - Benutzernachricht (Frage).
   * - ``session_id``
     - string
     - Nein
     - Sitzungs-ID. Wenn weggelassen, erstellt der Server eine Sitzung und gibt sie in der Antwort zurück.
   * - ``fields``
     - object
     - Nein
     - Optionale Filterfelder für den Abrufschritt.
   * - ``fields.label``
     - string / string-Array
     - Nein
     - Schränkt den Abruf auf zugelassene Labels ein.
   * - ``extra_queries``
     - string / string-Array
     - Nein
     - Zugelassene Facettenabfrageausdrücke.

Anfrage-Beispiel:

.. code-block:: json

    {
      "message": "Fessとは何ですか？",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

Antwort
-------

**Bei Erfolg (HTTP 200, ChatResponse)**

Die Antwort ist im gemeinsamen Envelope ``response`` enthalten. ``session_id`` ist stets vorhanden.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elemente von response
   :header-rows: 1

   * - Feld
     - Typ
     - Beschreibung
   * - ``session_id``
     - string
     - Sitzungs-ID.
   * - ``content``
     - string (nullable)
     - Generierter Nachrichtentext. Stets vorhanden, kann aber ``null`` sein, wenn das Modell keinen Inhalt generiert hat.
   * - ``sources``
     - array
     - Array der Quelldokumente. Jedes Element ist ein ChatSource-Objekt.

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elemente von ChatSource
   :header-rows: 1

   * - Feld
     - Typ
     - Beschreibung
   * - ``rank``
     - integer
     - 1-basierte Position im Abruf-Set.
   * - ``title``
     - string (nullable)
     - Titel des Dokuments.
   * - ``url``
     - string (nullable)
     - URL des Dokuments.
   * - ``doc_id``
     - string (nullable)
     - Dokument-ID.
   * - ``snippet``
     - string (nullable)
     - Snippet.
   * - ``url_link``
     - string (nullable)
     - URL-Link zur Anzeige.
   * - ``go_url``
     - string (nullable)
     - URL für die Weiterleitung.

Antwort-Beispiel:

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

HTTP-Statuscodes
----------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Beschreibung
   * - 200
     - Anfrage erfolgreich.
   * - 400
     - Ungültige Anfrage (z. B. fehlendes ``message``-Feld, ``rag.chat.enabled=false``).
   * - 403
     - Fehlender oder abgelaufener CSRF-Token.
   * - 404
     - Ressource nicht gefunden.
   * - 405
     - HTTP-Methode nicht erlaubt.
   * - 413
     - Request-Body überschreitet die Größenbegrenzung.
   * - 415
     - Nicht unterstützter ``Content-Type``.
   * - 429
     - Rate-Limit überschritten.
   * - 500
     - Interner Serverfehler.

cURL-Beispiel
-------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessとは何ですか？","session_id":"abc123def456"}'

POST /chat/stream
=================

Führt eine Streaming-Chat-Vervollständigung durch.
Der Anfrage-Body ist identisch mit ``POST /chat`` (ChatRequest).

Die Erfolgsantwort ist im Format ``text/event-stream`` (Server-Sent Events) mit benannten Ereignissen.
Jedes Ereignis besteht aus ``event: <Name>`` und ``data: <JSON>``.

Validierungsfehler vor dem Stream werden weiterhin als JSON-Envelope zurückgegeben (gleiche Fehlercodes wie ``POST /chat``).
Ungültige Werte in ``fields.label`` oder ``extra_queries`` werden stillschweigend entfernt und sind weder im Antwort-Envelope noch in SSE-Ereignissen sichtbar.

Endpunkt
--------

::

    POST /api/v2/chat/stream

SSE-Ereignisse
--------------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - Ereignis
     - Beschreibung (Payload)
   * - ``phase``
     - Phasenübergang der Pipeline (``{ phase, status, message?, keywords?, hit_count?, ... }``). ``message`` und ``keywords`` werden bei onPhaseStart ausgegeben. Zusätzliche optionale Felder (z. B. ``hit_count``) stammen aus dem Payload von onPhaseComplete.
   * - ``chunk``
     - Fragment des generierten Textes (``{ content }``).
   * - ``sources``
     - Abgerufene Quellen (``{ sources: [ChatSource] }``).
   * - ``retry``
     - Backoff bei vorübergehendem Fehler (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``).
   * - ``waiting``
     - Fortschritt bei lang andauernden Phasen (``{ phase, reason, elapsed_ms, timeout_ms }``).
   * - ``fallback``
     - Umschreibung der Abfrage oder Strategie-Fallback (``{ phase, reason, original_query?, new_query? }``).
   * - ``warning``
     - Behebbarer Warnhinweis (``{ phase, code, detail? }``).
   * - ``done``
     - Stream-Ende (``{ session_id, html_content? }``).
   * - ``error``
     - Terminaler Stream-Fehler mitten im Stream (``{ phase?, message, error_code }``). Das Feld ``message`` enthält denselben Wert wie ``error_code``. Clients sollten ``error_code`` zur Lokalisierung verwenden.

SSE-Stream-Beispiel:

::

    event: phase
    data: {"phase":"search","status":"start","message":"Searching documents...","keywords":"Fess インストール"}

    event: chunk
    data: {"content":"Fessは"}

    event: sources
    data: {"sources":[{"rank":1,"title":"インストールガイド","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

HTTP-Statuscodes
----------------

Wenn die Validierung vor dem Stream fehlschlägt, werden folgende Fehlercodes als JSON-Envelope zurückgegeben:

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Beschreibung
   * - 200
     - SSE-Stream gestartet (Erfolg).
   * - 400
     - Ungültige Anfrage (z. B. fehlendes ``message``-Feld, ``rag.chat.enabled=false``).
   * - 403
     - Fehlender oder abgelaufener CSRF-Token.
   * - 405
     - HTTP-Methode nicht erlaubt.
   * - 413
     - Request-Body überschreitet die Größenbegrenzung.
   * - 415
     - Nicht unterstützter ``Content-Type``.
   * - 429
     - Rate-Limit überschritten.
   * - 500
     - Interner Serverfehler.

cURL-Beispiel
-------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

DELETE /chat/sessions/{session_id}
===================================

Löscht den Gesprächsverlauf der angegebenen Chat-Sitzung.
Die Sitzung wird durch den Pfadparameter ``session_id`` identifiziert.

Bei Erfolg wird ``cleared: true`` zurückgegeben. Wenn keine übereinstimmende aktive Sitzung gefunden wird, wird ein ``not_found``-Fehler (HTTP 404) zurückgegeben.

Endpunkt
--------

::

    DELETE /api/v2/chat/sessions/{session_id}

Pfadparameter
-------------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - Parameter
     - Typ
     - Beschreibung
   * - ``session_id``
     - string
     - Sitzungs-ID, deren Verlauf gelöscht werden soll. minLength 1, maxLength 128, Muster ``^[A-Za-z0-9._-]+$``.

Antwort
-------

**Bei Erfolg (HTTP 200, ChatClearResponse)**

Die Antwort ist im gemeinsamen Envelope ``response`` enthalten. ``session_id`` und ``cleared`` sind stets vorhanden.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elemente von response
   :header-rows: 1

   * - Feld
     - Typ
     - Beschreibung
   * - ``session_id``
     - string
     - Sitzungs-ID.
   * - ``cleared``
     - boolean
     - Stets ``true`` (wenn die Sitzung gefunden und gelöscht wurde).

Antwort-Beispiel:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

HTTP-Statuscodes
----------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Beschreibung
   * - 200
     - Sitzung wurde gelöscht.
   * - 400
     - Ungültige Anfrage.
   * - 401
     - Authentifizierung erforderlich.
   * - 403
     - Fehlender oder abgelaufener CSRF-Token.
   * - 404
     - Keine übereinstimmende aktive Sitzung gefunden.
   * - 405
     - HTTP-Methode nicht erlaubt.
   * - 429
     - Rate-Limit überschritten.
   * - 500
     - Interner Serverfehler.

cURL-Beispiel
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

Sicherheit
==========

Sicherheitshinweise bei der Verwendung der Chat-API:

1. **Authentifizierung**: Die v2-API verwendet sitzungsbasierte Authentifizierung. Details siehe :doc:`api-overview`.
2. **CSRF**: Für zustandsändernde Anfragen ist der ``X-Fess-CSRF-Token``-Header erforderlich.
3. **Rate-Limiting**: Zum Schutz vor DoS-Angriffen gilt ein benutzerspezifisches Rate-Limit (Standard: 30/Minute). Der Konfigurationsschlüssel ist ``api.v2.chat.rate.limit.per.user.per.minute``.

Referenzinformationen
=====================

- :doc:`../config/rag-chat` - Konfiguration des KI-Suchmodus
- :doc:`../config/llm-overview` - Übersicht zur LLM-Integration
- :doc:`../user/chat-search` - Chat-Suchanleitung für Endbenutzer
- :doc:`api-overview` - API-Übersicht
