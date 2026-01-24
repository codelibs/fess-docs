====================================
SAML-Authentifizierung SSO-Einrichtung
====================================

Übersicht
=========

|Fess| unterstützt Single Sign-On (SSO) Authentifizierung mit SAML (Security Assertion Markup Language) 2.0.
Durch die Verwendung von SAML-Authentifizierung können Benutzerinformationen, die von einem IdP (Identity Provider) authentifiziert wurden, mit |Fess| integriert werden. In Kombination mit rollenbasierter Suche ermöglicht dies die Anzeige von Suchergebnissen basierend auf Benutzerberechtigungen.

Funktionsweise der SAML-Authentifizierung
-----------------------------------------

Bei der SAML-Authentifizierung fungiert |Fess| als SP (Service Provider) und arbeitet mit einem externen IdP zur Authentifizierung zusammen.

1. Benutzer greift auf den |Fess| SSO-Endpunkt (``/sso/``) zu
2. |Fess| leitet die Authentifizierungsanfrage an den IdP weiter
3. Benutzer authentifiziert sich beim IdP
4. IdP sendet SAML-Assertion an |Fess|
5. |Fess| validiert die Assertion und meldet den Benutzer an

Für die Integration mit rollenbasierter Suche siehe :doc:`security-role`.

Voraussetzungen
===============

Überprüfen Sie vor der Konfiguration der SAML-Authentifizierung die folgenden Voraussetzungen:

- |Fess| 15.5 oder höher ist installiert
- Ein SAML 2.0-kompatibler IdP (Identity Provider) ist verfügbar
- |Fess| ist über HTTPS erreichbar (erforderlich für Produktionsumgebungen)
- Sie haben die Berechtigung, |Fess| als SP beim IdP zu registrieren

Unterstützte IdP-Beispiele:

- Microsoft Entra ID (Azure AD)
- Okta
- Google Workspace
- Keycloak
- OneLogin
- Andere SAML 2.0-kompatible IdPs

Grundkonfiguration
==================

SSO aktivieren
--------------

Um die SAML-Authentifizierung zu aktivieren, fügen Sie die folgende Einstellung in ``app/WEB-INF/conf/system.properties`` hinzu:

::

    sso.type=saml

SP (Service Provider) Konfiguration
-----------------------------------

Um |Fess| als SP zu konfigurieren, geben Sie die SP Base URL an.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.sp.base.url``
     - SP Basis-URL
     - (Erforderlich)

Diese Einstellung konfiguriert automatisch die folgenden Endpunkte:

- **Entity ID**: ``{base_url}/sso/metadata``
- **ACS URL**: ``{base_url}/sso/``
- **SLO URL**: ``{base_url}/sso/logout``

Beispiel::

    saml.sp.base.url=https://fess.example.com

Individuelle URL-Konfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sie können URLs auch einzeln angeben, anstatt die Base URL zu verwenden.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.sp.entityid``
     - SP Entity ID
     - (Erforderlich bei individueller Konfiguration)
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - (Erforderlich bei individueller Konfiguration)
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - (Optional)

IdP (Identity Provider) Konfiguration
-------------------------------------

Konfigurieren Sie die von Ihrem IdP erhaltenen Informationen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.idp.entityid``
     - IdP Entity ID
     - (Erforderlich)
   * - ``saml.idp.single_sign_on_service.url``
     - IdP SSO-Service-URL
     - (Erforderlich)
   * - ``saml.idp.x509cert``
     - IdP-Signatur X.509-Zertifikat (Base64-codiert, ohne Zeilenumbrüche)
     - (Erforderlich)
   * - ``saml.idp.single_logout_service.url``
     - IdP SLO-Service-URL
     - (Optional)

.. note::
   Geben Sie für ``saml.idp.x509cert`` nur den Base64-codierten Inhalt des Zertifikats in einer einzigen Zeile ohne Zeilenumbrüche an.
   Die Zeilen ``-----BEGIN CERTIFICATE-----`` und ``-----END CERTIFICATE-----`` dürfen nicht enthalten sein.

SP-Metadaten abrufen
--------------------

Nach dem Start von |Fess| können Sie die SP-Metadaten im XML-Format vom Endpunkt ``/sso/metadata`` abrufen.

::

    https://fess.example.com/sso/metadata

Importieren Sie diese Metadaten in Ihren IdP oder registrieren Sie den SP manuell auf der IdP-Seite unter Verwendung der Metadateninhalte.

.. note::
   Um die Metadaten abzurufen, müssen Sie zuerst die grundlegende SAML-Konfiguration (``sso.type=saml`` und ``saml.sp.base.url``) abschließen und |Fess| starten.

IdP-seitige Konfiguration
=========================

Bei der Registrierung von |Fess| als SP auf der IdP-Seite konfigurieren Sie die folgenden Informationen:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Einstellung
     - Wert
   * - ACS URL / Reply URL
     - ``https://<Fess-Host>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Fess-Host>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` (Empfohlen)

Informationen vom IdP abrufen
-----------------------------

Holen Sie die folgenden Informationen aus der Konfigurationsoberfläche oder den Metadaten Ihres IdPs für die |Fess|-Konfiguration:

- **IdP Entity ID**: URI zur Identifizierung des IdP
- **SSO URL (HTTP-Redirect)**: Single Sign-On Endpunkt-URL
- **X.509-Zertifikat**: Öffentliches Schlüsselzertifikat zur Überprüfung der SAML-Assertion-Signatur

Benutzerattribut-Zuordnung
==========================

Sie können Benutzerattribute aus SAML-Assertionen |Fess|-Gruppen und -Rollen zuordnen.

Gruppenattribut-Konfiguration
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.attribute.group.name``
     - Attributname mit Gruppeninformationen
     - ``memberOf``
   * - ``saml.default.groups``
     - Standardgruppen (kommagetrennt)
     - (Keine)

Beispiel::

    saml.attribute.group.name=groups
    saml.default.groups=user

Rollenattribut-Konfiguration
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.attribute.role.name``
     - Attributname mit Rolleninformationen
     - (Keine)
   * - ``saml.default.roles``
     - Standardrollen (kommagetrennt)
     - (Keine)

Beispiel::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   Wenn Attribute nicht vom IdP abgerufen werden können, werden Standardwerte verwendet.
   Bei Verwendung der rollenbasierten Suche konfigurieren Sie entsprechende Gruppen oder Rollen.

Sicherheitskonfiguration
========================

Für Produktionsumgebungen wird empfohlen, die folgenden Sicherheitseinstellungen zu aktivieren.

Signatureinstellungen
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.security.authnrequest_signed``
     - Authentifizierungsanfragen signieren
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Nachrichtensignaturen erfordern
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Assertion-Signaturen erfordern
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - Logout-Anfragen signieren
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - Logout-Antworten signieren
     - ``false``

.. warning::
   Sicherheitsfunktionen sind standardmäßig deaktiviert.
   Für Produktionsumgebungen wird dringend empfohlen, mindestens ``saml.security.want_assertions_signed=true`` zu setzen.

Verschlüsselungseinstellungen
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.security.want_assertions_encrypted``
     - Assertion-Verschlüsselung erfordern
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - NameID-Verschlüsselung erfordern
     - ``false``

Weitere Sicherheitseinstellungen
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.security.strict``
     - Strikter Modus (strenge Validierung durchführen)
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Signaturalgorithmus
     - ``http://www.w3.org/2000/09/xmldsig#rsa-sha1``
   * - ``saml.sp.nameidformat``
     - NameID-Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

Konfigurationsbeispiele
=======================

Minimale Konfiguration (für Tests)
----------------------------------

Das Folgende ist ein minimales Konfigurationsbeispiel zur Überprüfung in einer Testumgebung.

::

    # SSO aktivieren
    sso.type=saml

    # SP-Konfiguration
    saml.sp.base.url=https://fess.example.com

    # IdP-Konfiguration (Werte aus der IdP-Administrationskonsole setzen)
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(Base64-codiertes Zertifikat)

    # Standardgruppen
    saml.default.groups=user

Empfohlene Konfiguration (für Produktion)
-----------------------------------------

Das Folgende ist ein empfohlenes Konfigurationsbeispiel für Produktionsumgebungen.

::

    # SSO aktivieren
    sso.type=saml

    # SP-Konfiguration
    saml.sp.base.url=https://fess.example.com

    # IdP-Konfiguration
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(Base64-codiertes Zertifikat)

    # Benutzerattribut-Zuordnung
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # Sicherheitseinstellungen (für Produktion empfohlen)
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

Fehlerbehebung
==============

Häufige Probleme und Lösungen
-----------------------------

Kann nach der Authentifizierung nicht zu Fess zurückkehren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die ACS URL auf der IdP-Seite korrekt konfiguriert ist
- Stellen Sie sicher, dass der Wert von ``saml.sp.base.url`` mit der IdP-Konfiguration übereinstimmt

Signaturüberprüfungsfehler
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob das IdP-Zertifikat korrekt konfiguriert ist
- Stellen Sie sicher, dass das Zertifikat nicht abgelaufen ist
- Das Zertifikat sollte nur als Base64-codierter Inhalt ohne Zeilenumbrüche angegeben werden

Benutzergruppen/-rollen werden nicht reflektiert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Attribute auf der IdP-Seite korrekt konfiguriert sind
- Stellen Sie sicher, dass der Wert von ``saml.attribute.group.name`` mit dem vom IdP gesendeten Attributnamen übereinstimmt
- Aktivieren Sie den Debug-Modus, um den Inhalt der SAML-Assertion zu überprüfen

Debug-Einstellungen
-------------------

Um Probleme zu untersuchen, können Sie den Debug-Modus mit der folgenden Einstellung aktivieren:

::

    saml.security.debug=true

Sie können auch die |Fess|-Protokollierungsebenen anpassen, um detaillierte SAML-bezogene Protokolle auszugeben.

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
