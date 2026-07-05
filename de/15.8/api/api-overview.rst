=============
API-Übersicht
=============


Von |Fess| bereitgestellte APIs
================================

Dieses Dokument beschreibt die Web-API (v2), die von |Fess| bereitgestellt wird.
Durch die Verwendung der API kann |Fess| auch in bestehenden Websystemen und Single-Page-Anwendungen (SPA) als Suchserver genutzt werden.

.. note::

   In |Fess| 15.8 wurde die API auf **v2** erneuert. Die bisherige JSON-Such-API
   und die Chat-API unter ``/api/v1`` wurden abgekündigt und in ``/api/v2``
   zusammengeführt. Clients, die ``/api/v1`` verwenden, sollten auf ``/api/v2``
   migrieren.

Basis-URL
=========

Die v2-API-Endpunkte von |Fess| sind unter folgender Basis-URL erreichbar:

::

    http://<Server Name>/api/v2/

Beispielsweise sieht die URL in einer lokalen Umgebung wie folgt aus:

::

    http://localhost:8080/api/v2/

Antwort-Envelope
================

Alle JSON-Antworten von v2 werden in einer gemeinsamen Envelope-Struktur zurückgegeben.

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` gibt das Verarbeitungsergebnis an und folgt der Konvention von v1.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Werte von status

   * - 0
     - Erfolg
   * - 1
     - Client-Fehler
   * - 9
     - Systemfehler

Tabelle: Werte von status

Es gilt stets: ``response.status >= 1`` entspricht einem HTTP-Statuscode von ``400`` oder höher.

Feldnamen
---------

Alle JSON-Schlüssel – einschließlich Request-Body, Response-Body und SSE-Ereignisdaten – werden einheitlich in ``snake_case`` geschrieben.

Fehlerantwort
=============

Im Fehlerfall wird dem Envelope ein ``error``-Objekt hinzugefügt.

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
.. list-table:: Elemente von error

   * - code
     - Stabiler Fehlercode (``snake_case``). Clients sollten diesen Wert als Basis für die Lokalisierung verwenden.
   * - message
     - Für Menschen lesbarer Fehlermeldungstext (englisch). Bei der Anzeige sollte der Client den ``code`` zur Lokalisierung nutzen.
   * - details
     - Optionales Objekt mit zusätzlichen strukturierten Informationen (kann fehlen). Nur einige Endpunkte liefern dieses Feld. Beispielsweise bettet :doc:`api-health` einen Snapshot des Suchmaschinenclusters unter ``error.details.engine`` ein.

Tabelle: Elemente von error

Fehlercodes und HTTP-Statuscodes
---------------------------------

Abhängig von ``error.code`` wird ein standardmäßiger HTTP-Statuscode zurückgegeben.

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: Liste der Fehlercodes

   * - error.code
     - HTTP-Status
     - Beschreibung
   * - ``invalid_request``
     - 400
     - Die Anfrage ist ungültig.
   * - ``auth_required``
     - 401
     - Authentifizierung erforderlich oder Anmeldedaten ungültig.
   * - ``forbidden``
     - 403
     - Nicht erlaubt (z. B. fehlender oder abgelaufener CSRF-Token).
   * - ``not_found``
     - 404
     - Ressource nicht gefunden.
   * - ``method_not_allowed``
     - 405
     - HTTP-Methode nicht erlaubt. Der ``Allow``-Header listet die unterstützten Methoden auf.
   * - ``not_acceptable``
     - 406
     - Anfrage nicht akzeptierbar.
   * - ``conflict``
     - 409
     - Ressourcenkonflikt aufgetreten.
   * - ``payload_too_large``
     - 413
     - Request-Body überschreitet die Größenbegrenzung.
   * - ``unsupported_media_type``
     - 415
     - Nicht unterstützter ``Content-Type`` (die meisten Endpunkte erfordern ``application/json``).
   * - ``rate_limited``
     - 429
     - Rate-Limit überschritten. Der ``Retry-After``-Header gibt die Wartezeit in Sekunden an.
   * - ``internal_error``
     - 500
     - Interner Serverfehler aufgetreten.
   * - ``service_unavailable``
     - 503
     - Dienst vorübergehend nicht verfügbar.

Tabelle: Liste der Fehlercodes

.. note::

   Bei einer ``method_not_allowed``-Antwort wird ein ``Allow``-Header
   beigefügt, der die unterstützten HTTP-Methoden auflistet.

Authentifizierung und Sitzung
==============================

Die v2-API verwendet sitzungsbasierte Authentifizierung.
Die Anmeldung erfolgt über ``POST /auth/login``. Bei Erfolg wird eine Sitzung aufgebaut und ein CSRF-Token ausgestellt.
Den aktuellen Authentifizierungsstatus kann man mit ``GET /auth/me`` abfragen. Details siehe :doc:`api-auth`.

Endpunkte wie die Suche, für die keine Anmeldung erforderlich ist, können anonym genutzt werden (abhängig von der Option „Anmeldung erforderlich" in den Systemeinstellungen).

CSRF-Token
----------

Für zustandsändernde Anfragen (``POST`` / ``PUT`` / ``DELETE``) ist der ``X-Fess-CSRF-Token``-Header erforderlich.
Der CSRF-Token kann auf folgende Weise abgerufen werden:

- Feld ``csrf_token`` in der Antwort von ``POST /auth/login``
- Antwort von ``GET /ui/config`` (Feld ``csrf_token``, wenn ``csrf_required=true``)

Der Token wird bei jedem Anmelde-, Abmelde- oder Passwortänderungsvorgang rotiert.

.. note::

   Die CSRF-Überprüfung erfolgt **vor** der Authentifizierung. Daher erhalten
   zustandsändernde Anfragen ohne gültige Sitzung und ohne gültigen CSRF-Token
   den Fehler ``403 forbidden`` statt ``401 auth_required``. ``/auth/login``
   ist von der CSRF-Überprüfung ausgenommen, da vor dem Anmelden noch kein
   Token vorhanden ist.

Streaming-Format
================

Einige Endpunkte geben Antworten im Streaming-Format statt als gewöhnliches JSON zurück.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Streaming-Formate

   * - Endpunkt
     - Content-Type
     - Beschreibung
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events (SSE). Details siehe :doc:`api-chat`.
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON (jede Zeile ist ein Dokument im Format ``{"data":{...}}``. Nur bei einem Fehler mitten im Stream ist die letzte Zeile ``{"error":{...}}``). Details siehe :doc:`api-search`.

Tabelle: Streaming-Formate

API-Typen
=========

|Fess| stellt folgende v2-APIs bereit:

.. tabularcolumns:: |p{3cm}|p{4cm}|p{8cm}|
.. list-table::

   * - Typ
     - Hauptendpunkte
     - Beschreibung
   * - :doc:`search <api-search>`
     - ``/search`` , ``/documents/all``
     - API zum Suchen von Dokumenten und zum vollständigen Abruf aller Dokumente (Scroll).
   * - :doc:`label <api-label>`
     - ``/labels``
     - API zum Abrufen der Liste der konfigurierten Labels.
   * - :doc:`suggest <api-suggest>`
     - ``/suggest-words``
     - API zum Abrufen von Vorschlagswörtern.
   * - :doc:`popularword <api-popularword>`
     - ``/popular-words``
     - API zum Abrufen beliebter Suchbegriffe.
   * - :doc:`related <api-related>`
     - ``/related-queries`` , ``/related-content``
     - API zum Abrufen verwandter Abfragen und verwandter Inhalte.
   * - :doc:`health <api-health>`
     - ``/health``
     - API zum Abrufen des Zustands des Suchmaschinenclusters.
   * - :doc:`auth <api-auth>`
     - ``/auth/login`` , ``/auth/logout`` , ``/auth/me`` , ``/auth/password``
     - API für Authentifizierungs- und Sitzungsoperationen (Anmelden, Abmelden, Authentifizierungsstatus abrufen, Passwort ändern).
   * - :doc:`ui <api-uiconfig>`
     - ``/ui/config``
     - API zum Abrufen der Anfangskonfiguration (UI-Einstellungen) für SPAs.
   * - :doc:`favorite <api-favorite>`
     - ``/favorites`` , ``/documents/{docId}/favorite``
     - API zum Verwalten von favorisierten Dokumenten.
   * - :doc:`click <api-click>`
     - ``/click``
     - API zum Protokollieren von Klicks auf Suchergebnisse.
   * - :doc:`cache <api-cache>`
     - ``/cache/{docId}``
     - API zum Abrufen des gecachten Dokumentinhalts.
   * - :doc:`chat <api-chat>`
     - ``/chat`` , ``/chat/stream``
     - API zur Nutzung des KI-Suchmodus (RAG-Chat).

Tabelle: API-Typen
