====================================
SSO-Konfiguration mit OpenID Connect
====================================

Überblick
=========

|Fess| unterstützt Single Sign-On (SSO) Authentifizierung mit OpenID Connect (OIDC).
OpenID Connect ist ein Authentifizierungsprotokoll, das auf OAuth 2.0 aufbaut und ID-Token (JWT) für die Benutzerauthentifizierung verwendet.
Durch die Verwendung von OpenID Connect können Benutzerinformationen, die von einem OpenID Provider (OP) authentifiziert wurden, mit |Fess| integriert werden.

Funktionsweise der OpenID Connect Authentifizierung
----------------------------------------------------

Bei der OpenID Connect Authentifizierung fungiert |Fess| als Relying Party (RP) und arbeitet mit einem externen OpenID Provider (OP) für die Authentifizierung zusammen.

1. Benutzer greift auf den |Fess| SSO-Endpunkt (``/sso/``) zu
2. |Fess| leitet zum Autorisierungsendpunkt des OP weiter
3. Benutzer authentifiziert sich beim OP
4. OP leitet den Autorisierungscode an |Fess| weiter
5. |Fess| verwendet den Autorisierungscode, um ein ID-Token vom Token-Endpunkt zu erhalten
6. |Fess| ruft Benutzerinformationen aus dem ID-Token (JWT) ab und meldet den Benutzer an

.. note::
   |Fess| verwendet den Authorization Code Flow. Das ID-Token wird nicht über den Browser, sondern direkt vom Token-Endpunkt über einen Backkanal (Server-zu-Server-Kommunikation) zwischen |Fess| und dem OP abgerufen.
   |Fess| dekodiert das ID-Token und entnimmt daraus Claims (z. B. ``email`` und ``groups``), um die Benutzerinformationen zusammenzustellen, führt jedoch keine kryptografische Überprüfung der JWT-Signatur durch.
   Daher muss die Kommunikation mit dem Token-Endpunkt zwingend über HTTPS erfolgen; stellen Sie sicher, dass der Kommunikationsweg zwischen |Fess| und dem OP vertrauenswürdig ist.

Für die Integration mit rollenbasierter Suche siehe :doc:`security-role`.

Voraussetzungen
===============

Bevor Sie die OpenID Connect Authentifizierung konfigurieren, überprüfen Sie die folgenden Voraussetzungen:

- |Fess| 15.8 oder höher ist installiert
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
   ``sso.type`` sowie die im Folgenden beschriebenen ``oic.*``-Einstellungen können auch über die Administrationsseite „System > Allgemein" konfiguriert und geändert werden.
   Über die Administrationsseite vorgenommene Änderungen werden in ``system.properties`` gespeichert und bleiben auch nach einem Neustart erhalten.

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

.. note::
   Diese URLs können vom Discovery-Endpunkt des OP (``/.well-known/openid-configuration``) abgerufen werden.

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

Benutzerattribut-Konfiguration
-------------------------------

Konfigurieren Sie die Standardgruppen und -rollen, die OIDC-authentifizierten Benutzern zugewiesen werden.
Benutzer-ID, Gruppen und Rollen werden jeweils wie folgt ermittelt:

- **Benutzer-ID**: Wird aus dem ``email``-Claim des ID-Tokens (JWT) bezogen. Daher muss der Scope in der Praxis ``email`` enthalten (kann der ``email``-Claim nicht abgerufen werden, ist kein ordnungsgemäßer Login möglich).
- **Gruppen**: Werden aus dem ``groups``-Claim des ID-Tokens bezogen. Ist kein ``groups``-Claim vorhanden, wird der Wert von ``oic.default.groups`` verwendet.
- **Rollen**: Es wird stets der Wert von ``oic.default.roles`` verwendet (ein Mechanismus zur Übernahme von Rollen aus ID-Token-Claims ist nicht vorhanden).

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
- **Client-ID**: Vom OP ausgestellte Client-Kennung
- **Client-Secret**: Geheimer Schlüssel für die Client-Authentifizierung

.. note::
   Die meisten OPs ermöglichen es Ihnen, die Autorisierungs- und Token-Endpunkt-URLs vom
   Discovery-Endpunkt (``https://<OP>/.well-known/openid-configuration``) zu überprüfen.

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

Benutzerinformationen können nicht abgerufen werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Stellen Sie sicher, dass der Scope die erforderlichen Berechtigungen (``email``, ``profile`` usw.) enthält
- Überprüfen Sie, ob die erforderlichen Scopes für den Client auf der OP-Seite erlaubt sind

Debug-Einstellungen
--------------------

Um Probleme zu untersuchen, können Sie detaillierte OpenID Connect-bezogene Protokolle ausgeben, indem Sie die |Fess| Protokollebene anpassen.

In ``app/WEB-INF/classes/log4j2.xml`` können Sie den folgenden Logger hinzufügen, um die Protokollebene zu ändern:

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-saml` - SSO-Konfiguration mit SAML-Authentifizierung
- :doc:`sso-entraid` - SSO-Konfiguration speziell für Microsoft Entra ID (bei Verwendung von Entra ID kann statt der allgemeinen OpenID Connect-Konfiguration auch die dedizierte Einstellung verwendet werden)
