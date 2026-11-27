====================================
SSO-Konfiguration mit OpenID Connect
====================================

Überblick
=========

|Fess| unterstützt Single Sign-On (SSO) Authentifizierung mit OpenID Connect (OIDC).
OpenID Connect ist ein Authentifizierungsprotokoll, das auf OAuth 2.0 aufbaut und ID-Token (JWT) für die Benutzerauthentifizierung verwendet.
Durch die Verwendung von OpenID Connect können Benutzerinformationen, die von einem OpenID Provider (OP) authentifiziert wurden, mit |Fess| integriert werden.

.. note::
   Die Unterstützung für die OpenID Connect Authentifizierung kommt aus dem Plugin
   ``fess-sso-oidc``, das nicht Teil der Distribution ist. Installieren Sie es über die Seite
   **System > Plugin** in der Administrationsoberfläche oder mit
   ``bin/fess-setup install plugin fess-sso-oidc``. Das Plugin heißt ``fess-sso-oidc``, während
   der Wert von ``sso.type`` weiterhin ``oic`` lautet.
   Bis dahin wird eine Anfrage an ``/sso/`` mit ``sso.type=oic`` nur zur Anmeldeseite
   zurückgeleitet.

Funktionsweise der OpenID Connect Authentifizierung
----------------------------------------------------

Bei der OpenID Connect Authentifizierung fungiert |Fess| als Relying Party (RP) und arbeitet mit einem externen OpenID Provider (OP) für die Authentifizierung zusammen.

1. Benutzer greift auf den |Fess| SSO-Endpunkt (``/sso/``) zu
2. |Fess| leitet zum Autorisierungsendpunkt des OP weiter
3. Benutzer authentifiziert sich beim OP
4. OP leitet den Autorisierungscode an |Fess| weiter
5. |Fess| verwendet den Autorisierungscode, um ein ID-Token vom Token-Endpunkt zu erhalten
6. |Fess| prüft die Claims des ID-Tokens (JWT), ruft daraus Benutzerinformationen ab und meldet den Benutzer an

.. note::
   |Fess| verwendet den Authorization Code Flow. Das ID-Token wird nicht über den Browser, sondern direkt vom Token-Endpunkt über einen Backkanal (Server-zu-Server-Kommunikation) zwischen |Fess| und dem OP abgerufen.
   |Fess| dekodiert das ID-Token und entnimmt daraus Claims (z. B. ``email`` und ``groups``), um die Benutzerinformationen zusammenzustellen, führt jedoch keine kryptografische Überprüfung der JWT-Signatur durch. OpenID Connect Core erlaubt dies, weil das Token direkt vom Token-Endpunkt über TLS empfangen wird; daher muss die Token-Endpunkt-URL (``oic.token.server.url``) HTTPS verwenden. ``http`` wird nur für ``localhost``, ``127.x.x.x`` und ``::1`` akzeptiert.
   |Fess| prüft aber die Claims: ``aud`` muss ``oic.client.id`` enthalten (und ``azp`` muss, sofern vorhanden, ihm entsprechen), ``exp`` muss vorhanden und darf nicht abgelaufen sein (eine Zeitabweichung von bis zu 300 Sekunden wird toleriert), und ``iss`` muss ``oic.issuer`` entsprechen, sofern dieser Schlüssel gesetzt ist. Ohne ``oic.issuer`` wird ``iss`` nicht geprüft, und bei der ersten Anmeldung nach jedem Start wird eine Warnung protokolliert. Mit jeder Autorisierungsanfrage wird ein ``nonce`` gesendet, und der ``nonce``-Claim des ID Tokens muss ihm entsprechen; ein Token ohne diesen Claim oder mit einem anderen Wert wird abgelehnt. Ein OP, der den ``nonce`` nicht zurückgibt, kann nicht verwendet werden, und es gibt keine Einstellung, die diese Prüfung abschaltet. PKCE (S256) wird standardmäßig verwendet: Jede Autorisierungsanfrage enthält einen ``code_challenge``, und die Token-Anfrage sendet den ``code_verifier``. Setzen Sie ``oic.pkce=false`` in ``system.properties`` nur für einen OP, der PKCE ablehnt (die Administrationsseite hat dafür kein Feld; der Schlüssel wird bei jeder Anmeldung gelesen, ein Neustart ist daher nicht nötig). ``iat`` und ``nbf`` werden nicht geprüft.

Für die Integration mit rollenbasierter Suche siehe :doc:`security-role`.

.. note::
   Die |Fess|-Anmeldesitzung endet nicht, wenn die vom OP ausgestellten Token ablaufen. |Fess| prüft ``exp`` des ID-Tokens nur, wenn sich der Benutzer anmeldet, und die Lebensdauer des Tokens wird für die Sitzung nicht verwendet. Ohne ``oic.jwks.uri`` besteht die Anmeldung, bis sich der Benutzer abmeldet oder das Sitzungs-Timeout erreicht ist. Damit die |Fess|-Sitzung endet, wenn sich der Benutzer beim OP abmeldet, richten Sie das `Back-Channel-Logout`_ ein. Bei SAML ist das anders: Die Sitzung endet mit der Sitzung des IdP (siehe :doc:`sso-saml`).

.. note::
   Wenn Sie mehrere Knoten betreiben, setzen Sie die Umgebungsvariable ``FESS_SESSION_STORE=opensearch``, um die HTTP-Sitzung zwischen ihnen zu teilen; eine auf einem Knoten begonnene Anmeldung kann dann auf einem anderen abgeschlossen werden. Aktualisieren Sie das Plugin auf jedem Knoten auf 15.10, bevor Sie dies aktivieren: Ein Plugin 15.9.0 teilt den Anmeldestatus nicht, und ein Benutzer, der zu einem anderen Knoten zurückkehrt, bleibt anonym. Ohne gemeinsame Sitzung binden Sie jede Sitzung am Load Balancer an einen Knoten.

   Mit ``FESS_SESSION_STORE=opensearch`` ändert das Hinzufügen oder Entfernen eines SSO-Plugins (``fess-sso-saml``, ``fess-sso-oidc`` oder ``fess-sso-entraid``) die Formatversion der gespeicherten Sitzungen. Alle gespeicherten Sitzungen werden dadurch ungültig, und alle Benutzer müssen sich erneut anmelden. Installieren oder entfernen Sie diese Plugins auf allen Knoten: Ein Knoten, dessen Plugin-Satz sich von dem der anderen Knoten unterscheidet, kann die von diesen gespeicherten Sitzungen nicht lesen, und diese können seine Sitzungen nicht lesen. Andere Plugins, etwa die Storage-, Skript- und SPNEGO-Plugins, ändern das Format nicht.

Voraussetzungen
===============

Bevor Sie die OpenID Connect Authentifizierung konfigurieren, überprüfen Sie die folgenden Voraussetzungen:

- |Fess| 15.10 oder höher ist installiert
- Ein OpenID Connect-kompatibler Provider (OP) ist verfügbar
- |Fess| ist über HTTPS erreichbar (erforderlich für Produktionsumgebungen)
- Sie haben die Berechtigung, |Fess| als Client (RP) auf der OP-Seite zu registrieren

Beispiele für unterstützte Provider:

- Microsoft Entra ID (Azure AD)
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- Andere OpenID Connect-kompatible Provider

Grundkonfiguration
==================

SSO aktivieren
--------------

Um die OpenID Connect Authentifizierung zu aktivieren, fügen Sie die folgende Einstellung in ``app/WEB-INF/conf/system.properties`` hinzu:

::

    sso.type=oic

.. note::
   ``sso.type`` sowie die im Folgenden beschriebenen ``oic.*``-Einstellungen mit Ausnahme von ``oic.issuer`` und ``oic.jwks.uri`` können auch über die Administrationsseite „System > Allgemein" konfiguriert und geändert werden.
   Über die Administrationsseite vorgenommene Änderungen werden in ``system.properties`` gespeichert und bleiben auch nach einem Neustart erhalten.
   ``oic.issuer`` und ``oic.jwks.uri`` lassen sich nur in ``system.properties`` festlegen.

Provider-Konfiguration
----------------------

Konfigurieren Sie die vom OP erhaltenen Informationen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``oic.auth.server.url``
     - Autorisierungsendpunkt-URL
     - ``https://accounts.google.com/o/oauth2/auth``
   * - ``oic.token.server.url``
     - Token-Endpunkt-URL
     - ``https://accounts.google.com/o/oauth2/token``
   * - ``oic.issuer``
     - Aussteller-Kennung (Issuer, optional). Wenn gesetzt, muss der ``iss``-Claim des ID-Tokens exakt damit übereinstimmen (ein abschließender Schrägstrich zählt mit)
     - (leer: ``iss`` wird nicht geprüft)
   * - ``oic.jwks.uri``
     - Die ``jwks_uri`` des OP (optional). Wenn gesetzt, ist das Back-Channel-Logout aktiviert (siehe `Back-Channel-Logout`_)
     - (leer: kein Back-Channel-Logout)

.. note::
   Diese URLs und der Aussteller können vom Discovery-Endpunkt des OP (``/.well-known/openid-configuration``) abgerufen werden; der Aussteller ist dessen ``issuer``-Wert.

   Die Token-Endpunkt-URL (``oic.token.server.url``) muss HTTPS verwenden. ``http`` wird nur akzeptiert, wenn der Host ``localhost`` (Groß-/Kleinschreibung egal), eine IPv4-Adresse der Form ``127.x.x.x`` oder ``::1`` ist. Der Host wird so verglichen, wie er geschrieben ist, und nie aufgelöst. Deshalb wird ein Docker-Compose-Servicename (z. B. ``http://keycloak:8080/...``) oder ein interner Hostname über ``http`` abgelehnt, auch wenn er auf denselben Rechner zeigt.

   Geprüft wird nur der Token-Endpunkt, nicht der Autorisierungsendpunkt (``oic.auth.server.url``). Die Prüfung erfolgt bei der Anmeldung, nicht beim Start. Das Setzen von ``oic.issuer`` lockert diese Regel nicht; es aktiviert nur die Prüfung des ``iss``-Claims.

Client-Konfiguration
--------------------

Konfigurieren Sie die beim OP registrierten Client-Informationen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``oic.client.id``
     - Client-ID
     - (leer)
   * - ``oic.client.secret``
     - Client-Secret
     - (leer)
   * - ``oic.scope``
     - Angeforderte Scopes
     - (leer)

.. note::
   Der Scope muss mindestens ``openid`` enthalten.
   Um die E-Mail-Adresse des Benutzers abzurufen, geben Sie ``openid email`` an.

Redirect-URL-Konfiguration
--------------------------

Konfigurieren Sie die Callback-URL nach der Authentifizierung.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``oic.redirect.url``
     - Redirect-URL (Callback-URL)
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - |Fess| Basis-URL
     - ``http://localhost:8080``

.. note::
   Wenn ``oic.redirect.url`` weggelassen wird, wird sie automatisch aus ``oic.base.url`` erstellt.
   Für Produktionsumgebungen setzen Sie ``oic.base.url`` auf eine HTTPS-URL.

.. warning::
   „Weggelassen" bedeutet, dass der Schlüssel gar nicht existiert. Speichern Sie ``oic.redirect.url`` auf der Administrationsseite „System > Allgemein" leer, wird der Schlüssel entfernt, und ``{oic.base.url}/sso/`` wird verwendet.
   Eine von Hand in ``system.properties`` geschriebene Zeile ``oic.redirect.url=`` (nur der Wert ist leer) ist dagegen keine weggelassene Einstellung, sondern ein leerer Wert: Die Autorisierungsanfrage enthält dann einen Parameter ``redirect_uri`` ohne Wert.
   Er stimmt nicht mit dem beim OP registrierten Redirect-URI überein, sodass der OP ihn ablehnt und die Anmeldung fehlschlägt.
   Geben Sie entweder einen Wert an oder entfernen Sie die Zeile.

Benutzerattribut-Konfiguration
-------------------------------

Konfigurieren Sie die Standardgruppen und -rollen, die OIDC-authentifizierten Benutzern zugewiesen werden.
Benutzer-ID, Gruppen und Rollen werden jeweils wie folgt ermittelt:

- **Benutzer-ID**: Wird aus dem ``email``-Claim des ID-Tokens (JWT) bezogen. Daher muss der Scope in der Praxis ``email`` enthalten (kann der ``email``-Claim nicht abgerufen werden, ist kein ordnungsgemäßer Login möglich).
- **Gruppen**: Werden aus dem ``groups``-Claim des ID-Tokens bezogen. Ist kein ``groups``-Claim vorhanden, wird der Wert von ``oic.default.groups`` verwendet. Ein leeres ``groups``-Array gilt als vorhanden: ``oic.default.groups`` wird dann nicht verwendet, und der Benutzer wird als Benutzer ohne Gruppen behandelt.
- **Rollen**: Es wird stets der Wert von ``oic.default.roles`` verwendet (ein Mechanismus zur Übernahme von Rollen aus ID-Token-Claims ist nicht vorhanden).

.. note::
   |Fess| übernimmt die Werte des ``groups``-Claims unverändert: Es findet keine
   Verzeichnisabfrage statt, und verschachtelte (transitive) Gruppen werden nicht aufgelöst.
   Ob übergeordnete Gruppen enthalten sind, hängt daher allein von der Claim-Konfiguration des OP
   ab -- anders als bei :doc:`sso-entraid`, wo |Fess| übergeordnete Gruppen über die
   Microsoft Graph API auflöst.
   Der Claim-Wert wird unverändert zur Suchberechtigung. Ist der OP so konfiguriert, dass er
   vollständige Gruppenpfade ausgibt, lauten die Werte etwa ``/uebergeordnet/untergeordnet`` und
   passen damit nicht zu Dokumenten, die nur mit dem reinen Gruppennamen versehen sind.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``oic.default.groups``
     - Standardgruppen (kommagetrennt)
     - (leer)
   * - ``oic.default.roles``
     - Standardrollen (kommagetrennt)
     - (leer)

.. note::
   Bei Verwendung der rollenbasierten Suche müssen Benutzern geeignete Gruppen oder Rollen zugewiesen werden.
   Weitere Informationen finden Sie unter :doc:`security-role`.

OP-seitige Konfiguration
========================

Wenn Sie |Fess| als Client (RP) auf der OP-Seite registrieren, konfigurieren Sie die folgenden Informationen:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Einstellung
     - Wert
   * - Anwendungstyp
     - Webanwendung
   * - Redirect-URI / Callback-URL
     - ``https://<Fess-Host>/sso/``
   * - Erlaubte Scopes
     - ``openid`` und erforderliche Scopes (``email``, ``profile`` usw.)

Vom OP zu erhaltende Informationen
-----------------------------------

Rufen Sie die folgenden Informationen vom Konfigurationsbildschirm oder Discovery-Endpunkt des OP für die |Fess| Konfiguration ab:

- **Autorisierungsendpunkt (Authorization Endpoint)**: URL zum Starten der Benutzerauthentifizierung
- **Token-Endpunkt (Token Endpoint)**: URL zum Abrufen von Token
- **Issuer** (optional): ``issuer``-Wert des Discovery-Dokuments, der für ``oic.issuer`` verwendet wird
- **Client-ID**: Vom OP ausgestellte Client-Kennung
- **Client-Secret**: Geheimer Schlüssel für die Client-Authentifizierung

.. note::
   Die meisten OPs ermöglichen es Ihnen, die Autorisierungs- und Token-Endpunkt-URLs vom
   Discovery-Endpunkt (``https://<OP>/.well-known/openid-configuration``) zu überprüfen.

Back-Channel-Logout
===================

Mit `OpenID Connect Back-Channel Logout 1.0 <https://openid.net/specs/openid-connect-backchannel-1_0.html>`__ teilt der OP |Fess| von Server zu Server mit, dass eine Anmeldung beim OP beendet wurde, und |Fess| beendet die Sitzung dieser Anmeldung.
Ohne diese Funktion besteht eine |Fess|-Sitzung auch nach der Abmeldung beim OP weiter.

Aktivierung
-----------

Setzen Sie die ``jwks_uri`` des OP in ``app/WEB-INF/conf/system.properties``. Damit wird das Back-Channel-Logout aktiviert; weitere Einstellungen müssen nicht umgeschaltet werden.

::

    oic.jwks.uri=https://op.example.com/jwks

- ``oic.jwks.uri`` lässt sich nur in ``system.properties`` festlegen (die Administrationsseite hat dafür kein Feld).
- ``oic.issuer`` und ``oic.client.id`` müssen ebenfalls gesetzt sein, weil das Logout-Token gegen sie geprüft wird. Ist einer der beiden Werte leer, wird jede Logout-Anfrage abgelehnt.
- ``oic.jwks.uri`` muss HTTPS sein. Wie beim Token-Endpunkt ist ``http`` nur erlaubt, wenn der Host ``localhost``, ``127.x.x.x`` oder ``::1`` ist. Die Prüfung erfolgt, wenn die Schlüssel für eine Logout-Anfrage abgerufen werden; eine URL, die sie nicht besteht, führt zur Ablehnung der Anfrage.
- ``jwks_uri`` und ``issuer`` können vom Discovery-Endpunkt des OP (``/.well-known/openid-configuration``) abgerufen werden; dort gibt ``backchannel_logout_supported`` an, ob der OP diese Funktion unterstützt.

Registrierung beim OP
---------------------

- Registrieren Sie in den Client-Einstellungen des OP ``https://<Fess-Host>/sso/logout`` als Back-Channel-Logout-URL.
- Sofern der OP die Option anbietet (``backchannel_logout_session_required``), lassen Sie ihn die Sitzungs-ID (``sid``) in das Logout-Token aufnehmen. Mit ``sid`` endet nur die eine passende Sitzung, nicht jede Sitzung des Benutzers. Das bei der Anmeldung ausgestellte ID-Token muss dieselbe ``sid`` enthalten.

Verhalten
---------

- Der OP sendet einen ``logout_token``-Parameter per POST an ``/sso/logout``. |Fess| antwortet mit ``200``, wenn das Logout erfasst wurde, und sonst mit ``400``, in beiden Fällen mit ``Cache-Control: no-store``.
- Geprüft werden die Signatur des Logout-Tokens (RS256, RS384, RS512, ES256, ES384 oder ES512 mit einem Schlüssel des ``jwks_uri``-Dokuments), ``iss`` (``oic.issuer``), ``aud`` (``oic.client.id``), ``iat`` und ``exp`` (mit derselben Zeitabweichung von 300 Sekunden wie beim ID-Token; ein Token, das vor mehr als einer Stunde ausgestellt wurde, wird abgelehnt), ``jti``, ``events``, das Fehlen von ``nonce`` und das Vorhandensein von ``sid`` oder ``sub``. Ein Token, das eine Prüfung nicht besteht, und ein bereits angenommenes Token (dieselbe ``jti``) werden mit ``400`` abgelehnt, und keine Sitzung endet. Ist ``oic.jwks.uri`` nicht gesetzt, wird ebenfalls jede Logout-Anfrage mit ``400`` abgelehnt.
- Enthält das Token ``sid``, endet nur die Sitzung der Anmeldung mit dieser ``sid``. Enthält es nur ``sub``, endet jede Sitzung dieses Benutzers, die geöffnet wurde, bevor |Fess| die Anfrage erhielt. Eine Anmeldung, deren ID-Token keine ``sid`` enthielt, wird durch ein Token mit ``sid`` nicht beendet.
- Eine Sitzung endet, wenn sie das nächste Mal verwendet wird, und diese Anfrage wird als anonym behandelt. An den OP wird kein Logout zurückgesendet; nur die |Fess|-Sitzung endet. Das Audit-Log erfasst ``SESSION_END`` mit dem ``reason`` ``idp_session_ended`` (siehe :doc:`../install/security`).
- Das Logout wird im Koordinator-Index der Suchmaschine (``fess_config.coordinator``) erfasst, den jeder Knoten liest. Es funktioniert daher mit mehreren Knoten, unabhängig davon, ob die HTTP-Sitzungen mit ``FESS_SESSION_STORE=opensearch`` geteilt werden. Auf dem Knoten, der die Anfrage erhalten hat, endet die Sitzung ohne Verzögerung bei ihrer nächsten Anfrage. Ein anderer Knoten prüft den Eintrag höchstens alle 30 Sekunden, sodass eine Sitzung dort bis zu 30 Sekunden nach der Anfrage weiterbestehen kann.
- Kann der Koordinator-Index nicht gelesen werden, endet keine Sitzung (es wird eine Warnung protokolliert). Bei einem Token mit nur ``sub`` kann der Zeitpunkt einer Anmeldung mit dem Zeitpunkt verglichen werden, zu dem ein anderer Knoten die Anfrage erhielt; halten Sie daher die Uhren der Knoten synchron.
- Die erste abgelehnte Anfrage jeder Art wird als Warnung protokolliert, die späteren auf DEBUG-Ebene. Weder Token noch ``sid`` oder ``sub`` werden protokolliert.
- Verschlüsselte Logout-Tokens (JWE) und Front-Channel-Logout werden nicht unterstützt.

Konfigurationsbeispiele
=======================

Minimalkonfiguration (für Tests)
---------------------------------

Das folgende Beispiel zeigt eine minimale Konfiguration zur Überprüfung in einer Testumgebung.

::

    # SSO aktivieren
    sso.type=oic

    # Provider-Konfiguration (vom OP erhaltene Werte eintragen)
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Client-Konfiguration
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # Redirect-URL (Testumgebung)
    oic.redirect.url=http://localhost:8080/sso/

Empfohlene Konfiguration (für Produktion)
------------------------------------------

Das folgende Beispiel zeigt eine empfohlene Konfiguration für Produktionsumgebungen.

::

    # SSO aktivieren
    sso.type=oic

    # Provider-Konfiguration
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Issuer (issuer-Wert des Discovery-Dokuments)
    oic.issuer=https://op.example.com

    # Client-Konfiguration
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # Basis-URL (HTTPS für Produktion verwenden)
    oic.base.url=https://fess.example.com

Fehlerbehebung
==============

Häufige Probleme und Lösungen
------------------------------

Rückkehr zu |Fess| nach der Authentifizierung nicht möglich
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Redirect-URI auf der OP-Seite korrekt konfiguriert ist
- Stellen Sie sicher, dass der Wert von ``oic.redirect.url`` oder ``oic.base.url`` mit der OP-Konfiguration übereinstimmt
- Überprüfen Sie, ob das Protokoll (HTTP/HTTPS) übereinstimmt

Authentifizierungsfehler treten auf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob Client-ID und Client-Secret korrekt konfiguriert sind
- Stellen Sie sicher, dass der Scope ``openid`` enthält
- Überprüfen Sie, ob die Autorisierungsendpunkt-URL und Token-Endpunkt-URL korrekt sind
- Wenn die Anmeldung fehlschlägt, enthält ``fess.log`` eine Warnung ``Failed to process the OpenID Connect callback:`` gefolgt vom Grund
- ``The ID token was not issued for this client``: Der ``aud``-Claim des ID-Tokens entspricht nicht ``oic.client.id``; überprüfen Sie die Client-ID
- ``The ID token has expired``: Die Uhren des |Fess|-Hosts und des OP weichen um mehr als 300 Sekunden voneinander ab; synchronisieren Sie die Uhrzeit (NTP)
- ``The ID token was not issued by the configured issuer``: ``oic.issuer`` weicht vom ``iss`` ab, das in der Meldung angezeigt wird; kopieren Sie den ``issuer``-Wert des Discovery-Dokuments exakt
- ``oic.token.server.url must be https``: Verwenden Sie eine HTTPS-Token-Endpunkt-URL (``http`` funktioniert nur für ``localhost``, ``127.x.x.x`` und ``::1``; ``http`` zu einem Docker-Compose-Servicenamen oder einem internen Hostnamen wird ebenfalls abgelehnt)

Benutzerinformationen können nicht abgerufen werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Stellen Sie sicher, dass der Scope die erforderlichen Berechtigungen (``email``, ``profile`` usw.) enthält
- Überprüfen Sie, ob die erforderlichen Scopes für den Client auf der OP-Seite erlaubt sind
- Bei Microsoft Entra ID enthält der ``groups``-Claim die ``ObjectId``-GUIDs der Gruppen, sofern
  kein anderes Quellattribut ausgewählt ist; die Werte stimmen daher nicht mit den Gruppennamen
  überein
- Microsoft Entra ID lässt den ``groups``-Claim vollständig weg, wenn ein Benutzer mehr als 200
  Gruppen angehört (verschachtelte Gruppen zählen mit); |Fess| greift dann auf
  ``oic.default.groups`` zurück

Debug-Einstellungen
--------------------

Um Probleme zu untersuchen, können Sie detaillierte OpenID Connect-bezogene Protokolle ausgeben, indem Sie die |Fess| Protokollebene anpassen.

In ``app/WEB-INF/classes/log4j2.xml`` können Sie den folgenden Logger hinzufügen, um die Protokollebene zu ändern:

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

.. warning::
   Steht dieser Logger auf DEBUG, werden die Claims des ID-Tokens (z. B. ``email`` und ``groups``)
   in die Protokolldatei geschrieben. Setzen Sie die Protokollebene nach der Untersuchung zurück
   und behandeln Sie die erzeugten Protokolle entsprechend.

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-saml` - SSO-Konfiguration mit SAML-Authentifizierung
- :doc:`sso-entraid` - SSO-Konfiguration speziell für Microsoft Entra ID (bei Verwendung von Entra ID kann statt der allgemeinen OpenID Connect-Konfiguration auch die dedizierte Einstellung verwendet werden)
