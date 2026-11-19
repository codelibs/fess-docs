==========================================
SAML-Authentifizierung SSO-Einrichtung
==========================================

Übersicht
=========

|Fess| unterstützt Single Sign-On (SSO) Authentifizierung mit SAML (Security Assertion Markup Language) 2.0.
Durch die Verwendung von SAML-Authentifizierung können Benutzerinformationen, die von einem IdP (Identity Provider) authentifiziert wurden, mit |Fess| integriert werden. In Kombination mit rollenbasierter Suche ermöglicht dies die Anzeige von Suchergebnissen basierend auf Benutzerberechtigungen.

.. note::
   Die Unterstützung für die SAML-Authentifizierung kommt aus dem Plugin ``fess-sso-saml``,
   das nicht Teil der Distribution ist. Installieren Sie es über die Seite **System > Plugin**
   in der Administrationsoberfläche oder mit ``bin/fess-setup install plugin fess-sso-saml``.
   Das Plugin verarbeitet SAML-Nachrichten mit der SAML-Bibliothek `saml4j <https://github.com/codelibs/saml4j>`__.
   Bis dahin wird eine Anfrage an ``/sso/`` mit ``sso.type=saml`` nur zur Anmeldeseite
   zurückgeleitet.

Funktionsweise der SAML-Authentifizierung
-----------------------------------------

Bei der SAML-Authentifizierung fungiert |Fess| als SP (Service Provider) und arbeitet mit einem externen IdP zur Authentifizierung zusammen.

1. Benutzer greift auf den |Fess| SSO-Endpunkt (``/sso/``) zu
2. |Fess| leitet die Authentifizierungsanfrage an den IdP weiter
3. Benutzer authentifiziert sich beim IdP
4. IdP sendet SAML-Assertion an |Fess|
5. |Fess| validiert die Assertion und meldet den Benutzer an

.. note::
   Unterstützt wird ausschließlich die SP-initiierte Anmeldung, die wie oben beschrieben am
   |Fess| SSO-Endpunkt (``/sso/``) beginnt. |Fess| bindet jede SAML-Antwort an die ID der von ihm
   gesendeten AuthnRequest. Eine IdP-initiierte (unaufgeforderte) Antwort, etwa von einer
   |Fess| -Kachel im Okta-Dashboard oder im Portal „Meine Apps" von Microsoft Entra ID, hat daher
   keine zugehörige AuthnRequest und wird abgelehnt. Wenn Sie auf der IdP-Seite eine Kachel
   anlegen, lassen Sie diese auf den |Fess| -Endpunkt ``/sso/`` verweisen.

   Beachten Sie: In 15.7 funktionierte eine IdP-initiierte Anmeldung zufällig, wenn
   ``tomcat.sameSiteCookies=none`` gesetzt war. |Fess| schickte die nicht zuordenbare Antwort an den
   IdP zurück, und der IdP lieferte sofort eine angeforderte Assertion. In 15.8 erfolgt dieses
   Zurückschicken nicht mehr, sodass die IdP-initiierte Anmeldung nicht funktioniert.

Für die Integration mit rollenbasierter Suche siehe :doc:`security-role`.

Voraussetzungen
===============

Überprüfen Sie vor der Konfiguration der SAML-Authentifizierung die folgenden Voraussetzungen:

- |Fess| 15.10 oder höher ist installiert
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

.. note::
   ``sso.type`` und die grundlegenden SAML-Einstellungen (IdP-Informationen, SP-Informationen, Benutzerattribut-Zuordnung) können auch über die Administrationsseite „System > Allgemein" konfiguriert werden.
   Im Admin-Bereich vorgenommene Änderungen werden in ``system.properties`` gespeichert und bleiben nach einem Neustart erhalten.
   Sicherheitseinstellungen wie Signierung/Verschlüsselung sowie das SP-Zertifikat und der private Schlüssel können jedoch nicht über die Administrationsseite konfiguriert werden und müssen direkt in ``system.properties`` eingetragen werden.

.. note::
   Einstellungen, die mit ``saml.`` beginnen, werden ausschließlich aus ``system.properties`` gelesen.
   JVM-Systemeigenschaften wie ``-Dsaml.security....`` oder ``-Dfess.saml.security....`` werden nicht ausgewertet.
   Insbesondere ``saml.security.*`` hat auch kein Feld auf der Administrationsseite;
   der einzige Weg, es zu setzen, ist der direkte Eintrag in ``system.properties``.

Konfiguration des Sitzungs-Cookies
----------------------------------

Der IdP sendet die Assertion als **seitenübergreifenden POST** an |Fess| zurück. Ein ``SameSite=Lax``-Cookie wird bei einer solchen Anfrage nicht mitgesendet, sodass die SAML-Anmeldung mit dem von |Fess| ausgelieferten Standardwert nicht abgeschlossen wird.

Ändern Sie ``tomcat.sameSiteCookies`` in ``tomcat_config.properties`` auf ``none``. Diese Datei liegt beim ZIP-Paket unter ``lib/classes/`` und bei den DEB-/RPM-Paketen unter ``/etc/fess/``.

::

    tomcat.sameSiteCookies = none

.. warning::
   Browser akzeptieren ``none`` nur bei einem Cookie, das auch das Attribut ``Secure`` trägt. |Fess| muss daher über HTTPS bereitgestellt werden. Über einfaches HTTP macht diese Einstellung eine Anmeldung bei |Fess| unmöglich.

.. note::
   Der Standardwert ``lax`` ist für SSO-Verfahren gedacht, deren Callback als Weiterleitung (GET) zurückkommt. Die HTTP-POST-Bindung von SAML gehört nicht dazu, daher ist diese Änderung nur bei Verwendung von SAML erforderlich. Nach der Änderung muss |Fess| neu gestartet werden.

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
     - ``http://localhost:8080``

.. note::
   Der Standardwert von ``saml.sp.base.url`` ist ``http://localhost:8080``.
   Außerhalb von Testumgebungen muss immer die URL gesetzt werden, über die |Fess| von außen erreichbar ist (in Produktionsumgebungen HTTPS).

Diese Einstellung konfiguriert automatisch die folgenden Endpunkte:

- **Entity ID**: ``{saml.sp.base.url}/sso/metadata``
- **ACS URL**: ``{saml.sp.base.url}/sso/``
- **SLO URL**: ``{saml.sp.base.url}/sso/logout``

Beispiel::

    saml.sp.base.url=https://fess.example.com

Individuelle URL-Konfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normalerweise werden durch das Setzen von ``saml.sp.base.url`` alle Endpunkt-URLs automatisch konfiguriert. Bei Bedarf können einzelne URLs jedoch auch explizit mit den folgenden Eigenschaften überschrieben werden.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.sp.entityid``
     - SP Entity ID
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - ``{saml.sp.base.url}/sso/logout``

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
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - Zusätzliche IdP-Signaturzertifikate (zum Beispiel bei einem Schlüsselwechsel)
     - (Optional)

.. note::
   Das IdP-Zertifikat ist der einzige Vertrauensanker für Signaturen; ein in einer Nachricht mitgesendetes Zertifikat wird nie als vertrauenswürdig behandelt.
   IdP- und SP-Zertifikate müssen RSA-Schlüssel mit mindestens 2048 Bit sein.
   ``saml.idp.x509cert`` kann entfallen, wenn ``saml.idp.x509certMulti.N`` gesetzt ist.

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

.. note::
   |Fess| prüft bei jeder Assertion Folgendes. Die URLs werden aus ``saml.sp.base.url`` (oder den einzelnen URL-Eigenschaften) abgeleitet, nicht aus der eingehenden Anfrage.

   - Die Assertion enthält eine ``AudienceRestriction``, die die SP-Entity-ID nennt
   - Die ``Destination`` einer signierten Response und der ``Recipient`` der SubjectConfirmation entsprechen der Assertion-Consumer-Service-URL

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

.. note::
   |Fess| übernimmt die Gruppenwerte aus der Assertion unverändert: Es findet keine
   Verzeichnisabfrage statt, und verschachtelte (transitive) Gruppen werden nicht aufgelöst.
   Ob übergeordnete Gruppen enthalten sind, hängt daher allein von der Claim-Konfiguration des IdP
   ab -- anders als bei :doc:`sso-entraid`, wo |Fess| übergeordnete Gruppen über die
   Microsoft Graph API auflöst.

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

.. warning::
   Wenn ``saml.attribute.role.name`` gesetzt ist, werden die vom IdP gesendeten Attributwerte
   unverändert zu |Fess|-Rollen. Da ``authentication.admin.roles`` in ``fess_config.properties``
   standardmäßig ``admin`` lautet, erhält jeder Benutzer, dessen Rollenattribut ``admin`` enthält,
   Administratorrechte in |Fess|. Prüfen Sie, wer das Rollenattribut auf der IdP-Seite steuern kann,
   und ändern Sie ``authentication.admin.roles`` bei Bedarf in einen anderen Namen.

IdPs mit wiederholten Attributnamen
-----------------------------------

Wenn der IdP denselben Attributnamen auf mehrere ``<Attribute>``-Elemente verteilt, führt |Fess|
deren Werte zusammen.

Keycloak sendet standardmäßig Assertions dieser Form: Seine Rollen- und Gruppen-Mapper geben pro
Wert ein eigenes ``<Attribute>``-Element aus, solange deren Option ``single`` nicht aktiviert ist,
und jedes Keycloak-Konto besitzt mehrere Standard-Realm-Rollen. In |Fess| ist dafür keine Einstellung nötig.

Sicherheitskonfiguration
========================

Die folgenden Sicherheitseinstellungen werden aus ``system.properties`` gelesen.

.. note::
   Wenn Einstellungen bestehen bleiben, die die Standardwerte abschwächen (``saml.security.want_logout_signed=false``
   bei konfiguriertem Single Logout, ``saml.security.allow_deprecated_alg=true`` oder
   ``saml.security.allow_rsa_1_5=true``), wird beim Laden der SAML-Einstellungen eine
   Warnung ``Insecure SAML settings: ...`` in das Protokoll geschrieben.

Signatureinstellungen
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.security.authnrequest_signed``
     - Authentifizierungsanfragen signieren (erfordert ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Signatur der Response erfordern
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Signatur der Assertion erfordern
     - ``false``
   * - ``saml.security.want_logout_signed``
     - Signatur der Logout-Nachrichten vom IdP erfordern
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - SHA-1-Signaturen akzeptieren
     - ``false``
   * - ``saml.security.signature_algorithm``
     - Algorithmus ausgehender Signaturen: die URI von ``rsa-sha256``, ``rsa-sha384`` oder ``rsa-sha512``
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   Unabhängig von diesen Einstellungen muss entweder die Response oder die Assertion signiert sein.
   Verwenden Sie ``saml.security.want_messages_signed`` oder ``saml.security.want_assertions_signed``, um die Signatur für das Element zu erzwingen, das Ihr IdP signiert.
   Die Signatur muss das signierte Element über dessen eigene ID referenzieren und ``rsa-sha256``, ``rsa-sha384`` oder ``rsa-sha512`` (oder die ECDSA-Varianten) verwenden.
   SHA-1-Signaturen werden abgelehnt, solange nicht ``saml.security.allow_deprecated_alg=true`` gesetzt ist; stellen Sie daher sicher, dass Ihr IdP mit SHA-256 oder stärker signiert.

.. note::
   Wenn Single Logout konfiguriert ist (``saml.idp.single_logout_service.url``), müssen die vom IdP
   gesendeten LogoutRequest und LogoutResponse mit dem Schlüssel von ``saml.idp.x509cert`` signiert sein
   (``saml.security.want_logout_signed=true`` ist der Standardwert).
   Setzen Sie ``saml.security.want_logout_signed=false`` nur für einen IdP, der sie nicht signieren kann.
   Der Single-Logout-Dienst (``/sso/logout``) akzeptiert die Redirect-Bindung (GET) und die POST-Bindung.
   Registrieren Sie die URL ``/sso/logout`` auch für die POST-Bindung auf der IdP-Seite; eine LogoutResponse,
   die der IdP an den Assertion Consumer Service postet, wird nicht erkannt.

Verschlüsselungseinstellungen
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.security.want_assertions_encrypted``
     - Assertion-Verschlüsselung erfordern (erfordert ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - RSA-1.5-Key-Transport akzeptieren (erfordert ``saml.sp.privatekey``). Andernfalls wird nur OAEP akzeptiert
     - ``false``

.. note::
   Lassen Sie ``saml.security.allow_rsa_1_5`` auf ``false``, es sei denn, Ihr IdP kann nur mit RSA 1.5 verschlüsseln.

Konfiguration von SP-Zertifikat und privatem Schlüssel
------------------------------------------------------

Wenn der SP Authentifizierungsanfragen oder Logout-Nachrichten signiert (z. B. ``saml.security.authnrequest_signed``) oder die Verschlüsselung von Assertions oder der NameID anfordert (z. B. ``saml.security.want_assertions_encrypted``), müssen der private Schlüssel (PKCS#8) und das X.509-Zertifikat des SP konfiguriert werden.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.sp.x509cert``
     - SP X.509-Zertifikat (Base64-codiert, ohne Zeilenumbrüche)
     -
   * - ``saml.sp.privatekey``
     - Privater Schlüssel des SP (Base64-codiert, ohne Zeilenumbrüche)
     -

.. note::
   Für ``saml.sp.x509cert`` und ``saml.sp.privatekey`` gilt, wie bei ``saml.idp.x509cert``, dass der Base64-codierte Inhalt als einzelne Zeile ohne Zeilenumbrüche angegeben werden muss (die Zeilen ``-----BEGIN ...-----`` und ``-----END ...-----`` dürfen nicht enthalten sein).
   Wenn Signierung oder Verschlüsselung aktiviert wird, muss das SP-Zertifikat auch auf der IdP-Seite registriert werden. Das SP-Zertifikat wird im SP-Metadaten-Endpunkt unter ``/sso/metadata`` veröffentlicht.

Weitere Sicherheitseinstellungen
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.security.requested_authncontext``
     - Angeforderter Authentifizierungskontext (ein leerer Wert fordert keinen an)
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - Vergleich für den angeforderten Authentifizierungskontext (``exact``, ``minimum``, ``maximum`` oder ``better``)
     - ``exact``
   * - ``saml.security.clock_drift``
     - Bei der Prüfung von Gültigkeitszeiträumen tolerierte Zeitabweichung (Sekunden, 0 bis 600)
     - ``120``
   * - ``saml.security.max_message_size``
     - Größte akzeptierte decodierte Nachricht (Bytes, 1024 bis 16777216)
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - NameID-Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   Audience, Recipient, Destination, Issuer und Gültigkeitszeitraum einer Assertion werden immer geprüft,
   und eine Response muss auf eine Anmeldung antworten, die |Fess| gestartet hat.
   Eine Assertion ohne Audience oder mit einer Audience, die die SP-Entity-ID nicht nennt, wird abgelehnt.
   Die Validierung ist immer strikt: ``saml.strict=false`` wird abgelehnt.

Nicht mehr verwendete Eigenschaften
-----------------------------------

Die folgenden Eigenschaften werden ignoriert. Eine einzelne Warnung, die sie nennt, wird in das Protokoll geschrieben.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Eigenschaft
     - Jetzt
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1-Signaturen werden standardmäßig abgelehnt; ``saml.security.allow_deprecated_alg=true`` akzeptiert sie
   * - ``saml.security.allowed_key_transport_algorithms``
     - Standardmäßig wird nur OAEP akzeptiert; ``saml.security.allow_rsa_1_5=true`` akzeptiert zusätzlich RSA 1.5
   * - ``saml.security.allow_duplicated_attribute_name``
     - Wiederholte Attribute werden immer zusammengeführt
   * - ``saml.security.reject_missing_audience``
     - Eine Assertion ohne Audience wird immer abgelehnt
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - Setzen Sie ``saml.idp.x509cert``; ein Fingerabdruck ist kein Vertrauensanker
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``, die Eigenschaften ``*.binding`` und ``*.response.url``
     - Werden nicht mehr verwendet

Jede andere ``saml.``-Eigenschaft, die die Bibliothek nicht kennt, beendet SAML-Anmeldungen mit einer Meldung, die sie nennt,
damit eine falsch geschriebene Sicherheitseinstellung nicht unbemerkt bleibt. ``saml.debug`` wird akzeptiert und hat keine Wirkung.

AuthnRequest-Gültigkeitsdauer
=============================

|Fess| sendet bei jedem Zugriff auf ``/sso/`` eine AuthnRequest an den IdP und speichert deren ID in der Sitzung.
Die vom IdP zurückgegebene SAML-Antwort wird anhand der gespeicherten ID validiert.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``saml.request.id.ttl``
     - Wie lange die ID einer unbeantworteten AuthnRequest aufbewahrt wird (Sekunden)
     - ``3600``

Eine gespeicherte ID wird verworfen, sobald dieser Zeitraum verstrichen ist.
Ist die Gültigkeit abgelaufen (zum Beispiel weil die Anmeldeseite des IdP offen gelassen wurde), kann die zurückgegebene Assertion nicht zugeordnet werden, und die Anmeldung schlägt einmalig fehl.

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
    # Die Signatur für das Element erzwingen, das Ihr IdP signiert
    # (saml.security.want_messages_signed=true für die Response)
    saml.security.want_assertions_signed=true

Fehlerbehebung
==============

Häufige Probleme und Lösungen
-----------------------------

Kann nach der Authentifizierung nicht zu Fess zurückkehren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die ACS URL auf der IdP-Seite korrekt konfiguriert ist
- Stellen Sie sicher, dass der Wert von ``saml.sp.base.url`` mit der IdP-Konfiguration übereinstimmt
- Die SAML-Assertion trifft als seitenübergreifender POST vom IdP ein. Wenn
  ``tomcat.sameSiteCookies`` in ``tomcat_config.properties`` auf ``lax`` (Standard) steht, sendet der
  Browser das Sitzungs-Cookie nicht mit, und die Anmeldung schlägt einmalig fehl.
  Setzen Sie in diesem Fall ``tomcat.sameSiteCookies = none`` (``SameSite=None`` erfordert HTTPS)
- Wenn die Anmeldung am IdP zu lange gedauert hat, ist die AuthnRequest-ID nicht mehr vorhanden,
  sobald die Assertion zurückkommt; die Anmeldung schlägt einmalig fehl und muss neu gestartet werden
- |Fess| setzt in ``app/WEB-INF/web.xml`` kein ``session-timeout``, sodass der Standardwert des
  Servlet-Containers von 30 Minuten gilt; er ist kürzer als die 3600 Sekunden von
  ``saml.request.id.ttl``, sodass die Sitzung zuerst verworfen wird. Ein höherer Wert für
  ``saml.request.id.ttl`` allein verlängert daher nicht die Zeit, die Benutzer für die Anmeldung am
  IdP haben. Erhöhen Sie dafür auch den Sitzungs-Timeout

Destination- oder Recipient-Validierung schlägt fehl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die ``Destination`` einer signierten Response und der ``Recipient`` der SubjectConfirmation müssen der
Assertion-Consumer-Service-URL von |Fess| entsprechen. Diese URL stammt aus ``saml.sp.base.url`` (oder
``saml.sp.assertion_consumer_service.url``), nicht aus der Anfrage, die bei |Fess| ankommt; ein
TLS-terminierender Reverse Proxy hat daher keinen Einfluss auf den Vergleich.

- Setzen Sie ``saml.sp.base.url`` auf die von außen sichtbare URL, einschließlich Schema und Port
- Registrieren Sie auf der IdP-Seite dieselbe ACS URL (``{saml.sp.base.url}/sso/``)
- Wenn ``saml.sp.entityid`` überschrieben wird, muss der IdP diesen Wert als Audience verwenden

Signaturüberprüfungsfehler
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob das IdP-Zertifikat korrekt konfiguriert ist
- Stellen Sie sicher, dass das Zertifikat nicht abgelaufen ist
- Das Zertifikat sollte nur als Base64-codierter Inhalt ohne Zeilenumbrüche angegeben werden
- Das IdP-Zertifikat muss ein RSA-Schlüssel mit mindestens 2048 Bit sein
- Entweder die Response oder die Assertion muss signiert sein, und die Signatur muss SHA-256 oder stärker verwenden
  (SHA-1 wird nur mit ``saml.security.allow_deprecated_alg=true`` akzeptiert)
- Der Grund, warum eine Response abgelehnt wurde, wird als ``Authentication failed: <reason> - <detail>`` in das Protokoll geschrieben

Benutzergruppen/-rollen werden nicht reflektiert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Attribute auf der IdP-Seite korrekt konfiguriert sind
- Stellen Sie sicher, dass der Wert von ``saml.attribute.group.name`` mit dem vom IdP gesendeten Attributnamen übereinstimmt
- Bei Microsoft Entra ID enthält der Gruppen-Claim die ``ObjectId``-GUIDs der Gruppen, sofern kein
  anderes Quellattribut ausgewählt ist; die Werte stimmen daher nicht mit den Gruppennamen überein
- Microsoft Entra ID lässt den Gruppen-Claim vollständig weg, wenn ein Benutzer mehr als 150
  Gruppen angehört (verschachtelte Gruppen zählen mit); |Fess| greift dann auf
  ``saml.default.groups`` zurück
- Vergleichen Sie die Attributnamen mit denen in der Assertion, die der IdP tatsächlich sendet

Protokolleinstellungen
----------------------

Wenn die SAML-Authentifizierung fehlschlägt, wird der Grund immer als Warnung in das Protokoll geschrieben.
Die Eigenschaft ``saml.debug`` hat keine Wirkung.

Um detaillierte SAML-bezogene Protokolle auszugeben, fügen Sie den folgenden Logger in ``app/WEB-INF/classes/log4j2.xml`` hinzu:

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-oidc` - SSO-Konfiguration mit OpenID Connect
- :doc:`sso-entraid` - SSO-Konfiguration speziell für Microsoft Entra ID
