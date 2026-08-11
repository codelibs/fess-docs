==========================================
SAML-Authentifizierung SSO-Einrichtung
==========================================

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

- |Fess| 15.8 oder höher ist installiert
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
   Insbesondere ``saml.security.*``, ``saml.strict`` und ``saml.debug`` haben auch kein Feld auf der Administrationsseite;
   der einzige Weg, sie zu setzen, ist der direkte Eintrag in ``system.properties``.

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

.. warning::
   Wenn ``saml.attribute.role.name`` gesetzt ist, werden die vom IdP gesendeten Attributwerte
   unverändert zu |Fess|-Rollen. Da ``authentication.admin.roles`` in ``fess_config.properties``
   standardmäßig ``admin`` lautet, erhält jeder Benutzer, dessen Rollenattribut ``admin`` enthält,
   Administratorrechte in |Fess|. Prüfen Sie, wer das Rollenattribut auf der IdP-Seite steuern kann,
   und ändern Sie ``authentication.admin.roles`` bei Bedarf in einen anderen Namen.

Sicherheitskonfiguration
========================

Für Produktionsumgebungen wird empfohlen, die folgenden Sicherheitseinstellungen zu aktivieren.

.. note::
   Wenn nicht empfohlene Einstellungen bestehen bleiben, wird beim Laden der SAML-Einstellungen eine
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
   * - ``saml.security.reject_deprecated_alg``
     - Veraltete Signaturalgorithmen wie SHA-1 ablehnen
     - ``false``

.. warning::
   Sicherheitsfunktionen sind standardmäßig deaktiviert.
   Für Produktionsumgebungen wird dringend empfohlen, mindestens ``saml.security.want_assertions_signed=true`` zu setzen.

.. note::
   Solange ``saml.security.reject_deprecated_alg`` auf ``false`` steht, werden auch Assertions und
   Nachrichten akzeptiert, die mit SHA-1 (``rsa-sha1`` und ``dsa-sha1``) signiert wurden.
   Die Option ist nicht standardmäßig aktiviert, weil sie IdPs ablehnt, die weiterhin mit SHA-1 signieren.
   Stellen Sie sicher, dass Ihr IdP mit SHA-256 oder stärker signiert, und setzen Sie anschließend
   ``saml.security.reject_deprecated_alg=true``.

.. warning::
   Wenn Single Logout konfiguriert ist (``saml.idp.single_logout_service.url``), setzen Sie unbedingt
   auch ``saml.security.want_messages_signed=true``.
   Solange die Option ``false`` ist, wird für eine an ``/sso/logout`` eingehende LogoutRequest keine
   Signatur verlangt. Geprüft werden lediglich das XML-Schema, ``NotOnOrAfter`` (falls vorhanden),
   ``Destination`` (falls vorhanden) und die Übereinstimmung des Issuers mit ``saml.idp.entityid``;
   die NameID in der LogoutRequest wird nie mit dem angemeldeten Benutzer verglichen.
   Ein Angreifer, der die Entity-ID des IdP kennt (eine öffentliche Information), kann daher eine
   unsignierte LogoutRequest erzeugen und die Sitzung eines authentifizierten Benutzers beenden,
   indem er diesen auf die entsprechende URL lockt.
   Die Auswirkung ist eine erzwungene Abmeldung (Denial of Service), keine Kontoübernahme.

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

Konfiguration von SP-Zertifikat und privatem Schlüssel
------------------------------------------------------

Wenn der SP Authentifizierungsanfragen oder Logout-Nachrichten signiert (z. B. ``saml.security.authnrequest_signed``) oder die Verschlüsselung von Assertions oder der NameID anfordert (z. B. ``saml.security.want_assertions_encrypted``), müssen der private Schlüssel und das X.509-Zertifikat des SP konfiguriert werden.

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
   * - ``saml.strict``
     - Strikter Modus (strenge Validierung durchführen)
     - ``true``
   * - ``saml.security.want_xml_validation``
     - XML-Schema-Validierung von Nachrichten durchführen
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Signaturalgorithmus
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - Angeforderter Authentifizierungskontext
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - NameID-Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| verwendet intern eine SAML-Bibliothek (java-saml), und Eigenschaften mit dem Präfix ``saml.`` werden auf die entsprechenden Einstellungen der Bibliothek (Präfix ``onelogin.saml2.``) abgebildet.
   Daher können in ``system.properties`` neben den hier aufgeführten Einstellungen auch detailliertere Einstellungen vorgenommen werden, wie z. B. Bindings (z. B. ``saml.sp.assertion_consumer_service.binding``), Organisationsinformationen (``saml.organization.*``) und Kontaktinformationen (``saml.contacts.*``).

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

    # Aktivieren, nachdem bestätigt wurde, dass der IdP mit SHA-256 oder stärker signiert
    saml.security.reject_deprecated_alg=true

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
  Browser das Sitzungs-Cookie nicht mit. |Fess| findet dann keine passende AuthnRequest-ID und lässt
  die Anmeldung an dieser Stelle einmalig fehlschlagen. Der Browser kehrt zur Anmeldeseite mit der
  Meldung „SSO-Anmeldevorgang fehlgeschlagen." zurück, und im Protokoll erscheint eine Warnung, die
  mit ``Received a SAML response with no matching AuthnRequest ID in the session.`` beginnt.
  Setzen Sie in diesem Fall ``tomcat.sameSiteCookies = none`` (``SameSite=None`` erfordert HTTPS)

.. note::
   In 15.7 leitete |Fess| in derselben Situation immer wieder zum IdP weiter, sodass die Anmeldung in
   einer Schleife lief. In 15.8 schlägt sie stattdessen einmalig fehl. An der Konfigurationslösung
   ändert sich nichts.

Destination-Validierung schlägt hinter einem Reverse Proxy fehl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wenn |Fess| hinter einem TLS-terminierenden Reverse Proxy oder Load Balancer betrieben wird, kann die
Assertion-Validierung fehlschlagen, obwohl ``saml.sp.base.url`` korrekt gesetzt ist.

Die Ursache: Die SAML-Bibliothek vergleicht das Attribut ``Destination`` der Assertion mit der vom
Servlet-Container rekonstruierten Anfrage-URL und nicht mit der konfigurierten ACS-URL. Wenn der Proxy
HTTPS terminiert, sieht |Fess| eine interne Anfrage-URL wie
``http://<interner-host>:<interner-port>/sso/``, die nicht mit der vom IdP gesendeten URL
``https://fess.example.com/sso/`` übereinstimmt. ``saml.sp.base.url`` wird für diesen Vergleich nicht
herangezogen; die Einstellung allein behebt das Problem daher nicht.

Setzen Sie ``saml.debug=true``, damit der Grund ins Protokoll geschrieben wird:

::

    The response was received at http://... instead of https://fess.example.com/sso/

Passen Sie die Connector-Einstellungen in ``tomcat_config.properties`` an das von außen sichtbare
Schema und den Port an. Diese Einstellungen werden auskommentiert ausgeliefert:

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

Konfigurieren Sie außerdem den Reverse Proxy so, dass er den ursprünglichen ``Host``-Header an |Fess|
durchreicht, denn der Hostname-Teil der Anfrage-URL wird aus diesem Header gebildet. Nach Änderungen
an ``tomcat_config.properties`` muss |Fess| neu gestartet werden.

Dieselbe Prüfung gilt für Single-Logout-Nachrichten; konfigurieren Sie dies bei Verwendung von SLO
entsprechend.

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

    saml.debug=true

Durch das Setzen von ``saml.debug=true`` wird bei einem fehlgeschlagenen SAML-Authentifizierungsversuch die detaillierte Fehlerursache in das Protokoll ausgegeben.

Außerdem können detaillierte SAML-bezogene Protokolle ausgegeben werden, indem der folgende Logger in ``app/WEB-INF/classes/log4j2.xml`` hinzugefügt wird:

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-oidc` - SSO-Konfiguration mit OpenID Connect
- :doc:`sso-entraid` - SSO-Konfiguration speziell für Microsoft Entra ID
