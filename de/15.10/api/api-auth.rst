====================================
Authentifizierungs- und Sitzungs-API
====================================

Übersicht
=========

Die v2-API verwendet sitzungsbasierte Authentifizierung.
Die Anmeldung erfolgt über ``POST /auth/login``. Bei Erfolg wird eine Sitzung aufgebaut und ein CSRF-Token ausgestellt.

Für zustandsändernde Anfragen (``POST``) ist der ``X-Fess-CSRF-Token``-Header erforderlich.
Informationen zum Abrufen und Rotieren des CSRF-Tokens sowie zum gemeinsamen Antwort-Envelope und Fehlermodell finden Sie unter :doc:`api-overview`.

Diese Seite beschreibt die folgenden vier Endpunkte:

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Endpunktübersicht
   :header-rows: 1
   :widths: 25 15 60

   * - Endpunkt
     - Methode
     - Beschreibung
   * - ``/auth/me``
     - GET
     - Ruft den aktuell authentifizierten Benutzer ab.
   * - ``/auth/login``
     - POST
     - Meldet den Benutzer mit Benutzername und Passwort an.
   * - ``/auth/logout``
     - POST
     - Meldet den Benutzer ab (idempotent).
   * - ``/auth/password``
     - POST
     - Ändert das Passwort des aktuellen Benutzers.

.. _api-auth-userpayload:

Gemeinsame Benutzerinformationen (UserPayload)
==============================================

Die in den Antworten von ``GET /auth/me`` und ``POST /auth/login`` enthaltenen Benutzerinformationen werden in einer gemeinsamen ``UserPayload``-Struktur zurückgegeben.
Alle Array-Felder sind nicht-null; bei fehlenden Werten wird ein leeres Array zurückgegeben.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Beschreibung
   * - ``user_id``
     - string
     - Benutzer-ID. (Pflichtfeld)
   * - ``username``
     - string
     - Angezeigter Benutzername für das Kontomenü der SPA. Derzeit identisch mit ``user_id``, kann aber künftig vom Backend unabhängig bereitgestellt werden. (Pflichtfeld)
   * - ``name``
     - string
     - Angezeigter Name für das Kontomenü der SPA. Derzeit identisch mit ``user_id``. (Pflichtfeld)
   * - ``roles``
     - string[]
     - Array der Benutzerrollen. (Pflichtfeld)
   * - ``groups``
     - string[]
     - Array der Benutzergruppen. (Pflichtfeld)
   * - ``permissions``
     - string[]
     - Array der Benutzerberechtigungen. (Pflichtfeld)
   * - ``editable``
     - boolean
     - Gibt an, ob die Benutzerinformationen bearbeitbar sind. (Pflichtfeld)
   * - ``admin``
     - boolean
     - Wird ``true``, wenn der Benutzer eine der konfigurierten ``authentication.admin.roles`` besitzt. Steuert die Anzeige des Menüpunkts „Verwaltung" in der SPA. (Pflichtfeld)
   * - ``permission_state``
     - string
     - Ob die Gruppen- und Rollenberechtigungen des Benutzers aufgelöst sind (``RESOLVED``, ``PENDING`` oder ``FAILED``). ``PENDING`` (wird noch aufgelöst) und ``FAILED`` (fehlgeschlagen oder nur teilweise aufgelöst) bedeuten, dass der Benutzer weniger Berechtigungen hat, als er haben sollte, sodass bei einer Suche Dokumente fehlen können, die er sehen dürfte. (Pflichtfeld)

Authentifizierungsstatus abrufen
================================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/auth/me``
==================  ====================================================

Ruft den aktuell authentifizierten Benutzer ab.
Bei anonymen Aufrufen wird kein Fehler zurückgegeben, sondern ``authenticated: false``.
Bei authentifizierten Aufrufen enthält ``user`` eine :ref:`UserPayload <api-auth-userpayload>`.

Antwort
-------

Bei Erfolg (HTTP 200) wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben (Beispiel für authentifizierten Benutzer):

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
          "admin": true,
          "permission_state": "RESOLVED"
        }
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Antwortinformationen
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Beschreibung
   * - ``authenticated``
     - boolean
     - Gibt an, ob der Benutzer authentifiziert ist. (Pflichtfeld)
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`. Ist nur vorhanden, wenn ``authenticated`` ``true`` ist.

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort
   :header-rows: 1
   :widths: 25 75

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn ein Anfrageparameter angegeben wurde, der sich nicht dekodieren lässt (zum Beispiel ``?q=%ff``). ``error.code`` ist ``invalid_request``.
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Anmelden
========

Anfrage
-------

==================  ====================================================
HTTP-Methode         POST
Endpunkt             ``/api/v2/auth/login``
==================  ====================================================

Meldet den Benutzer mit Benutzername und Passwort an.
Bei erfolgreicher Anmeldung wird die Servlet-Sitzungs-ID rotiert, ein neues CSRF-Token ausgestellt. Außerdem wird die Aufzeichnung früherer fehlgeschlagener Versuche für dieselbe Kombination aus aufrufender IP und Benutzername (der Bucket pro Benutzer) geleert. Der Bucket pro IP wird nicht geleert, da er auch Versuche gegen andere Benutzer von derselben IP zählt; zurückgegeben wird nur der eine Platz, den dieser Versuch belegt hat.

Das Rate-Limiting erfolgt nach zwei Dimensionen: pro aufrufender IP und pro Benutzer. Bei Überschreitung des IP-seitigen Limits wird ``429 Too Many Requests`` zusammen mit einem ``Retry-After``-Header (in Sekunden) zurückgegeben. Bei Überschreitung des benutzerseitigen Limits wird – um den Zählerzustand von außen nicht erkennbar zu machen – dieselbe ``401 Unauthorized``-Antwort wie bei ungültigen Anmeldedaten zurückgegeben (ohne ``Retry-After``-Header).

Auch bei bereits authentifizierten Sitzungen wird kein Kurzschluss durchgeführt; die übermittelten Anmeldedaten werden stets überprüft.

``return_to`` muss ein relativer Pfad sein, der dem Muster ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$`` entspricht.
Außerdem werden protokollrelative Pfade (führendes ``//``) und Pfade mit ASCII-Steuerzeichen abgelehnt und stillschweigend aus der Echo-Antwort entfernt.

.. note::

   Dieser Endpunkt ist **von der CSRF-Überprüfung ausgenommen** (da vor der Anmeldung kein Token vorhanden ist).

.. note::

   Anders als bei anderen zustandsändernden Endpunkten fasst dieser Endpunkt übermäßig große Request-Bodys und nicht unterstützte ``Content-Type``-Werte zu ``400 invalid_request`` zusammen (andere Endpunkte geben ``413`` bzw. ``415`` zurück).

.. note::

   Die Rate-Limits für Anmeldung und Passwortänderung können mit folgenden Eigenschaften konfiguriert werden (Standardwerte in Klammern):

   - ``theme.api.login.rate.limit.per.ip.per.minute`` (``10``): Maximale Anzahl von Versuchen pro Minute und IP-Adresse. Gilt sowohl für ``/auth/login`` als auch für das Anmeldeformular ``POST /login/login``; beide teilen sich denselben Bucket.
   - ``theme.api.login.rate.limit.per.user.per.minute`` (``5``): Maximale Anzahl von Versuchen pro Minute und Benutzer. Gilt für ``/auth/login`` und ``POST /login/login`` (diese teilen sich je Kombination aus aufrufender IP und Benutzername einen Bucket) sowie für ``/auth/password``.
   - ``theme.api.login.lockout.seconds`` (``900``): Sperrungsdauer (in Sekunden) nach Überschreitung des Limits. Wird als Wert des ``Retry-After``-Headers zurückgegeben.

   Das Anmeldeformular (``POST /login/login``) teilt sich die Buckets und die Sperrung mit ``/auth/login``; Fehlversuche am Formular zählen daher zum Limit von ``/auth/login`` und umgekehrt. Wird das Limit am Formular überschritten, wird dies als gewöhnlicher Anmeldefehler behandelt und nicht mit ``429`` beantwortet.

   Hinter einem Reverse-Proxy, der nicht in ``rate.limit.trusted.proxies`` (Standard ``127.0.0.1,::1``) aufgeführt ist, werden alle Clients als eine einzige IP-Adresse (die des Proxys) behandelt. Wiederholte fehlgeschlagene Anmeldungen können dann für die Dauer der Sperrung alle Benutzer aussperren. Tragen Sie die Adresse des Proxys in ``rate.limit.trusted.proxies`` ein, damit die tatsächliche Client-IP aus ``X-Forwarded-For`` übernommen wird.

Anfrage-Body (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type ist ``application/json`` (Zeichensatz UTF-8). Die maximale Größe des Anfrage-Bodys beträgt 4 KiB.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - Feld
     - Typ
     - Pflicht
     - Beschreibung
   * - ``username``
     - string
     - Ja
     - Benutzername. ``minLength`` ist 1.
   * - ``password``
     - string
     - Ja
     - Passwort. ``minLength`` ist 1.
   * - ``return_to``
     - string
     - Nein
     - Weiterleitungsziel nach der Anmeldung. Muss ein relativer Pfad sein, der dem oben genannten Muster entspricht.

Anfrage-Beispiel:

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

Antwort
-------

Bei Erfolg (HTTP 200, LoginResponse) wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

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
          "admin": true,
          "permission_state": "RESOLVED"
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Antwortinformationen
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Beschreibung
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`.
   * - ``csrf_token``
     - string
     - Neues CSRF-Token, das mit der neuen Sitzung verknüpft ist. (Pflichtfeld)
   * - ``return_to``
     - string
     - Wird nur zurückgegeben, wenn der Anfragewert die Zulässigkeitsprüfung bestanden hat.

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort
   :header-rows: 1
   :widths: 25 75

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist (einschließlich übermäßig großer Request-Bodys und nicht unterstützter ``Content-Type``-Werte).
   * - 401 Unauthorized
     - Wenn die Anmeldedaten ungültig sind.
   * - 403 Forbidden
     - Wenn die Anfrage als Cross-Site-Anfrage blockiert wurde: Der Header ``Origin`` (oder ``Referer``) nennt einen nicht zulässigen Origin. Dies ist die grundlegende Prüfung, die jede zustandsändernde Anfrage durchläuft, und ist vom CSRF-Token getrennt, das die Anmeldung nicht benötigt.
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 429 Too Many Requests
     - Wenn das Rate-Limit überschritten wurde. Der ``Retry-After``-Header gibt die Wartezeit in Sekunden an.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
   * - 503 Service Unavailable
     - Wenn die Suchmaschine die Anfrage nicht entgegennehmen konnte: Sie ist nicht erreichbar oder hat die Anfrage wegen fehlender Kapazität abgelehnt. ``error.code`` ist ``service_unavailable``, und ein ``Retry-After``-Header nennt die Wartezeit in Sekunden (``5``). Die Anfrage selbst ist in Ordnung; versuchen Sie es nach kurzer Wartezeit erneut.

Abmelden
========

Anfrage
-------

==================  ====================================================
HTTP-Methode         POST
Endpunkt             ``/api/v2/auth/logout``
==================  ====================================================

Meldet den Benutzer ab. Diese Operation ist idempotent; auch wenn keine aktive Sitzung vorhanden ist, wird sie als No-op behandelt und kein Fehler zurückgegeben. Es wird stets ``ok: true`` zurückgegeben.

Der ``X-Fess-CSRF-Token``-Header ist erforderlich.

Antwort
-------

Bei Erfolg (HTTP 200, OkResponse) wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Antwortinformationen
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Beschreibung
   * - ``ok``
     - boolean
     - Stets ``true``. (Pflichtfeld)

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort
   :header-rows: 1
   :widths: 25 75

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn ein Anfrageparameter angegeben wurde, der sich nicht dekodieren lässt (zum Beispiel ``?q=%ff``). ``error.code`` ist ``invalid_request``.
   * - 403 Forbidden
     - Wenn der CSRF-Token fehlt oder abgelaufen ist.
   * - 405 Method Not Allowed
     - Wenn eine andere Methode als POST angegeben wurde. Es wird ein ``Allow: POST``-Header beigefügt.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Passwort ändern
===============

Anfrage
-------

==================  ====================================================
HTTP-Methode         POST
Endpunkt             ``/api/v2/auth/password``
==================  ====================================================

Ändert das Passwort des aktuellen Benutzers.
Überprüft ``current_password``, wendet die konfigurierte Passwortrichtlinie auf ``new_password`` an, invalidiert die aktuelle Sitzung und fordert die SPA durch ``re_login_required: true`` zur Weiterleitung zur Anmeldeseite auf.

Da die Sitzung serverseitig zerstört wird, wird kein ``csrf_token`` zurückgegeben. Die SPA muss nach erneuter Authentifizierung ein neues Token abrufen.

Der ``X-Fess-CSRF-Token``-Header ist erforderlich.

Für diesen Endpunkt gilt ein benutzerseitiges Rate-Limit; bei Überschreitung wird ``429 Too Many Requests`` zusammen mit einem ``Retry-After``-Header zurückgegeben (die Einstellungen sind gemeinsam mit der Anmeldung).

Anfrage-Body (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type ist ``application/json`` (Zeichensatz UTF-8). Die maximale Größe des Anfrage-Bodys beträgt 4 KiB.

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - Feld
     - Typ
     - Pflicht
     - Beschreibung
   * - ``current_password``
     - string
     - Ja
     - Aktuelles Passwort. ``minLength`` ist 1.
   * - ``new_password``
     - string
     - Ja
     - Neues Passwort. Muss die konfigurierte Passwortrichtlinie erfüllen (standardmäßig mindestens 8 Zeichen). ``minLength`` ist 1.
   * - ``confirm_password``
     - string
     - Ja
     - Bestätigungspasswort. Muss mit ``new_password`` übereinstimmen. ``minLength`` ist 1.

Antwort
-------

Bei Erfolg (HTTP 200) wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Antwortinformationen
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Beschreibung
   * - ``ok``
     - boolean
     - Stets ``true``. (Pflichtfeld)
   * - ``re_login_required``
     - boolean
     - Stets ``true``. Die aktuelle Sitzung wurde serverseitig invalidiert. Die SPA muss zur Anmeldeseite weiterleiten, um eine neue Sitzung und ein neues CSRF-Token zu erhalten. (Pflichtfeld)

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort
   :header-rows: 1
   :widths: 25 75

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist.
   * - 401 Unauthorized
     - Wenn Authentifizierung erforderlich ist oder ``current_password`` ungültig ist.
   * - 403 Forbidden
     - Wenn der CSRF-Token fehlt oder abgelaufen ist.
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 413 Payload Too Large
     - Wenn der Request-Body die Größenbegrenzung überschreitet.
   * - 415 Unsupported Media Type
     - Wenn ein nicht unterstützter ``Content-Type`` angegeben wurde.
   * - 429 Too Many Requests
     - Wenn das Rate-Limit überschritten wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
   * - 503 Service Unavailable
     - Wenn die Suchmaschine die Anfrage nicht entgegennehmen konnte: Sie ist nicht erreichbar oder hat die Anfrage wegen fehlender Kapazität abgelehnt. ``error.code`` ist ``service_unavailable``, und ein ``Retry-After``-Header nennt die Wartezeit in Sekunden (``5``). Die Anfrage selbst ist in Ordnung; versuchen Sie es nach kurzer Wartezeit erneut.
