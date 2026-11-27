=============
API-Übersicht
=============


Von |Fess| bereitgestellte APIs
================================

Dieses Dokument beschreibt die Web-API (v2), die von |Fess| bereitgestellt wird.
Durch die Verwendung der API kann |Fess| auch in bestehenden Websystemen und Single-Page-Anwendungen (SPA) als Suchserver genutzt werden.

.. note::

   In |Fess| 15.7 wurde die API auf **v2** erneuert. Die bisherige JSON-Such-API
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
     - Für Menschen lesbarer Fehlermeldungstext. Meldungen, für die es eine Übersetzung gibt, etwa die Ablehnung von Suchparametern oder von Eingaben an die Tag-API, werden in der Sprache des Request-Headers ``Accept-Language`` zurückgegeben (fehlt der Header ``Accept-Language``, in der Sprache des Standard-Locales des Servers, also des JVM-Standards, nicht unbedingt auf Englisch); die übrigen (zum Beispiel ``internal error`` oder ``invalid access token``) sind in jeder Sprache derselbe englische Text. ``code`` und der HTTP-Statuscode ändern sich nicht mit der Sprache, daher sollte der Client anhand von ``code`` entscheiden, nicht anhand des Textes von ``message``. Wenn alle Meldungen in der Sprache des Benutzers angezeigt werden müssen, sollte der Client den ``code`` zur Lokalisierung nutzen.
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
     - Anfrage nicht akzeptierbar. Reservierter Code, der derzeit von keinem Endpunkt zurückgegeben wird (eine Anfrage wird nicht wegen des Werts des ``Accept``-Headers abgelehnt).
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
     - Das Versuchslimit eines Endpunkts, etwa für Anmeldung, Passwortänderung oder Chat, wurde überschritten. Der ``Retry-After``-Header gibt die Wartezeit in Sekunden an.
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

.. note::

   Das serverweite Rate-Limit für HTTP-Anfragen (``rate.limit.enabled=true``, siehe :doc:`../config/rate-limiting`)
   greift vor der v2-API; seine Antworten verwenden daher nicht das obige Envelope-Format.
   Eine Anfrage über dem Limit erhält HTTP 429 mit einem ``Retry-After``-Header (``rate.limit.retry.after.seconds``,
   Standard ``60``) und diesem Body:

   ::

       {"error":"rate_limit_exceeded","message":"Too many requests. Please retry after 60 seconds.","retry_after":60}

   Eine IP-Adresse über dem Limit wird für ``rate.limit.block.duration.ms`` blockiert. Anfragen in dieser Zeit
   (ebenso Anfragen von IP-Adressen in ``rate.limit.blocked.ips``) erhalten HTTP 403 mit diesem Body.
   Diese Antwort hat keinen ``Retry-After``-Header.

   ::

       {"error":"ip_blocked","message":"Access denied."}

Authentifizierung und Sitzung
==============================

Die v2-API verwendet sitzungsbasierte Authentifizierung.
Die Anmeldung erfolgt über ``POST /auth/login``. Bei Erfolg wird eine Sitzung aufgebaut und ein CSRF-Token ausgestellt.
Den aktuellen Authentifizierungsstatus kann man mit ``GET /auth/me`` abfragen. Details siehe :doc:`api-auth`.

Endpunkte wie die Suche, für die keine Anmeldung erforderlich ist, können anonym genutzt werden (abhängig von der Option „Anmeldung erforderlich" in den Systemeinstellungen).

Anmeldedaten
------------

Die OpenAPI-Definition der v2-API (``openapi-user.yaml``) listet im Eintrag ``security`` jeder Operation die Anmeldedaten auf, die sie akzeptiert. Es gibt zwei Arten:

- ``sessionCookie``: das Sitzungs-Cookie ``JSESSIONID``, das die Antwort von ``POST /auth/login`` (oder der Passkey-Anmeldung) setzt. Senden Sie es nach der Anmeldung mit jeder Anfrage. Die Anmeldung erneuert die Sitzungs-ID; behalten Sie daher das Cookie der Anmeldeantwort. Das Cookie ist ``HttpOnly``; das Attribut ``Secure`` wird ergänzt, wenn ``session.cookie.secure`` aktiviert ist, und ``SameSite`` ist standardmäßig ``Lax`` (``tomcat.sameSiteCookies``). Sein Name ändert sich nicht, wenn Sitzungen in der Suchmaschine gespeichert werden (``FESS_SESSION_STORE``).
- ``accessToken``: ein von einem Administrator erstelltes Zugriffstoken, gesendet als ``Authorization: Bearer <Token>`` (ein bloßes ``Authorization: <Token>`` wird ebenfalls akzeptiert). Nur die Suchoperationen führen es auf: ``/search``, ``/documents/all``, ``/documents/export``, ``/documents/{docId}/similar``, ``/suggest-words``, ``/labels`` und ``/popular-words``. Das Token bestimmt, welche Dokumente sie zurückgeben, und ersetzt, solange „Anmeldung erforderlich" aktiviert ist, die Anmeldung. Bei den übrigen Endpunkten (Favoriten, Tags, Suchverlauf, Passwortänderung, Passkeys, Chat, Klick, Cache) ersetzt es die Anmeldung nicht. Ein Token, das fehlerhaft, nicht registriert oder abgelaufen ist, wird mit ``401 auth_required`` beantwortet.

Ein leerer Eintrag in ``security`` bedeutet, dass die Operation auch ohne Anmeldedaten funktioniert; das gilt nur, solange „Anmeldung erforderlich" deaktiviert ist. Der Header ``X-Fess-CSRF-Token`` gehört nicht zu den Anmeldedaten, sondern ist eine eigene Anforderung (siehe unten).

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
   * - :doc:`similar <api-similar>`
     - ``/documents/{docId}/similar``
     - API zum Abrufen der Dokumente, die denselben Inhalt wie ein Dokument haben.
   * - :doc:`chat <api-chat>`
     - ``/chat`` , ``/chat/stream``
     - API zur Nutzung des KI-Suchmodus (RAG-Chat).

Tabelle: API-Typen
