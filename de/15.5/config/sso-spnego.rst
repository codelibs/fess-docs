====================================================
SSO-Konfiguration mit Windows-Integrierte Auth
====================================================

Übersicht
=========

|Fess| unterstützt Single Sign-On (SSO)-Authentifizierung mit Windows-integrierter Authentifizierung (SPNEGO/Kerberos).
Durch die Verwendung der Windows-integrierten Authentifizierung können Benutzer, die an einem Windows-Domänencomputer angemeldet sind, ohne zusätzliche Anmeldevorgänge auf |Fess| zugreifen.

Wie die Windows-integrierte Authentifizierung funktioniert
----------------------------------------------------------

Bei der Windows-integrierten Authentifizierung verwendet |Fess| das SPNEGO-Protokoll (Simple and Protected GSSAPI Negotiation Mechanism) für die Kerberos-Authentifizierung.

1. Benutzer meldet sich an der Windows-Domäne an
2. Benutzer greift auf |Fess| zu
3. |Fess| sendet eine SPNEGO-Herausforderung
4. Browser erhält ein Kerberos-Ticket und sendet es an den Server
5. |Fess| validiert das Ticket und ruft den Benutzernamen ab
6. Gruppeninformationen des Benutzers werden über LDAP abgerufen
7. Benutzer ist angemeldet und Gruppeninformationen werden auf die rollenbasierte Suche angewendet

Informationen zur Integration mit der rollenbasierten Suche finden Sie unter :doc:`security-role`.

Voraussetzungen
===============

Bevor Sie die Windows-integrierte Authentifizierung konfigurieren, überprüfen Sie die folgenden Voraussetzungen:

- |Fess| 15.5 oder höher ist installiert
- Ein Active Directory (AD)-Server ist verfügbar
- |Fess|-Server ist von der AD-Domäne aus erreichbar
- Sie haben die Berechtigung, Dienstprinzipalnamen (SPN) in AD zu konfigurieren
- Ein Konto zum Abrufen von Benutzerinformationen über LDAP ist verfügbar

Active Directory-Seitige Konfiguration
======================================

Registrieren des Dienstprinzipalnamens (SPN)
--------------------------------------------

Sie müssen einen SPN für |Fess| in Active Directory registrieren.
Öffnen Sie eine Eingabeaufforderung auf einem Windows-Computer, der der AD-Domäne beigetreten ist, und führen Sie den Befehl ``setspn`` aus.

::

    setspn -S HTTP/<Fess-Server-Hostname> <AD-Zugriffsbenutzer>

Beispiel:

::

    setspn -S HTTP/fess-server.example.local svc_fess

So überprüfen Sie die Registrierung:

::

    setspn -L <AD-Zugriffsbenutzer>

.. note::
   Wenn Sie den Befehl auf dem Fess-Server ausgeführt haben, melden Sie sich nach der SPN-Registrierung von Windows ab und wieder an.

Grundkonfiguration
==================

SSO aktivieren
--------------

Um die Windows-integrierte Authentifizierung zu aktivieren, fügen Sie die folgende Einstellung in ``app/WEB-INF/conf/system.properties`` hinzu:

::

    sso.type=spnego

Kerberos-Konfigurationsdatei
----------------------------

Erstellen Sie ``app/WEB-INF/classes/krb5.conf`` mit der Kerberos-Konfiguration.

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   Ersetzen Sie ``EXAMPLE.LOCAL`` durch Ihren AD-Domänennamen (Großbuchstaben) und ``AD-SERVER.EXAMPLE.LOCAL`` durch Ihren AD-Server-Hostnamen.

Login-Konfigurationsdatei
-------------------------

Erstellen Sie ``app/WEB-INF/classes/auth_login.conf`` mit der JAAS-Login-Konfiguration.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Erforderliche Einstellungen
---------------------------

Fügen Sie die folgenden Einstellungen zu ``app/WEB-INF/conf/system.properties`` hinzu.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``spnego.preauth.username``
     - AD-Verbindungsbenutzername
     - (Erforderlich)
   * - ``spnego.preauth.password``
     - AD-Verbindungspasswort
     - (Erforderlich)
   * - ``spnego.krb5.conf``
     - Pfad zur Kerberos-Konfigurationsdatei
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Pfad zur Login-Konfigurationsdatei
     - ``auth_login.conf``

Optionale Einstellungen
-----------------------

Die folgenden Einstellungen können bei Bedarf hinzugefügt werden.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``spnego.login.client.module``
     - Name des Client-Moduls
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - Name des Server-Moduls
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Basic-Authentifizierung erlauben
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - Unsichere Basic-Authentifizierung erlauben
     - ``true``
   * - ``spnego.prompt.ntlm``
     - NTLM-Aufforderung anzeigen
     - ``true``
   * - ``spnego.allow.localhost``
     - Localhost-Zugriff erlauben
     - ``true``
   * - ``spnego.allow.delegation``
     - Delegierung erlauben
     - ``false``
   * - ``spnego.exclude.dirs``
     - Von der Authentifizierung ausgeschlossene Verzeichnisse (kommagetrennt)
     - (Keine)
   * - ``spnego.logger.level``
     - Protokollebene (0-7)
     - (Auto)

.. warning::
   ``spnego.allow.unsecure.basic=true`` kann Base64-kodierte Anmeldeinformationen über unverschlüsselte Verbindungen senden.
   Für Produktionsumgebungen wird dringend empfohlen, dies auf ``false`` zu setzen und HTTPS zu verwenden.

LDAP-Konfiguration
==================

Die LDAP-Konfiguration ist erforderlich, um Gruppeninformationen für Benutzer abzurufen, die über Windows-integrierte Authentifizierung authentifiziert werden.
Konfigurieren Sie LDAP-Einstellungen im |Fess|-Administrationsbereich unter "System" -> "Allgemein".

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Element
     - Beispiel
   * - LDAP-URL
     - ``ldap://AD-SERVER.example.local:389``
   * - Basis-DN
     - ``dc=example,dc=local``
   * - Bind-DN
     - ``svc_fess@example.local``
   * - Passwort
     - Passwort für AD-Zugriffsbenutzer
   * - Benutzer-DN
     - ``%s@example.local``
   * - Kontofilter
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - memberOf-Attribut
     - ``memberOf``

Browser-Einstellungen
=====================

Client-Browser-Einstellungen sind erforderlich, um die Windows-integrierte Authentifizierung zu verwenden.

Internet Explorer / Microsoft Edge
----------------------------------

1. Internetoptionen öffnen
2. Registerkarte "Sicherheit" auswählen
3. Auf "Sites" für die Zone "Lokales Intranet" klicken
4. Auf "Erweitert" klicken und die Fess-URL hinzufügen
5. Auf "Stufe anpassen" für die Zone "Lokales Intranet" klicken
6. Unter "Benutzerauthentifizierung" -> "Anmeldung" die Option "Automatische Anmeldung nur in der Intranetzone" auswählen
7. Auf der Registerkarte "Erweitert" die Option "Integrierte Windows-Authentifizierung aktivieren" aktivieren

Google Chrome
-------------

Chrome verwendet normalerweise die Windows-Internetoptionseinstellungen.
Falls zusätzliche Konfiguration erforderlich ist, setzen Sie ``AuthServerAllowlist`` über Gruppenrichtlinie oder Registrierung.

Mozilla Firefox
---------------

1. ``about:config`` in die Adressleiste eingeben
2. Nach ``network.negotiate-auth.trusted-uris`` suchen
3. Die Fess-Server-URL oder Domäne setzen (z.B. ``https://fess-server.example.local``)

Konfigurationsbeispiele
=======================

Minimale Konfiguration (zum Testen)
-----------------------------------

Das Folgende ist ein minimales Konfigurationsbeispiel für eine Testumgebung.

``app/WEB-INF/conf/system.properties``:

::

    # SSO aktivieren
    sso.type=spnego

    # SPNEGO-Einstellungen
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf``:

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf``:

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Empfohlene Konfiguration (für Produktion)
-----------------------------------------

Das Folgende ist ein empfohlenes Konfigurationsbeispiel für Produktionsumgebungen.

``app/WEB-INF/conf/system.properties``:

::

    # SSO aktivieren
    sso.type=spnego

    # SPNEGO-Einstellungen
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # Sicherheitseinstellungen (Produktion)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.allow.localhost=false

Fehlerbehebung
==============

Häufige Probleme und Lösungen
-----------------------------

Authentifizierungsdialog erscheint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob der Fess-Server in den Browser-Einstellungen zur Zone "Lokales Intranet" hinzugefügt wurde
- Überprüfen Sie, ob "Integrierte Windows-Authentifizierung aktivieren" aktiviert ist
- Überprüfen Sie, ob der SPN korrekt registriert ist (``setspn -L <Benutzername>``)

Authentifizierungsfehler treten auf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob der Domänenname (Großbuchstaben) und der AD-Servername in ``krb5.conf`` korrekt sind
- Überprüfen Sie, ob ``spnego.preauth.username`` und ``spnego.preauth.password`` korrekt sind
- Überprüfen Sie die Netzwerkverbindung zum AD-Server

Gruppeninformationen können nicht abgerufen werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die LDAP-Einstellungen korrekt sind
- Überprüfen Sie, ob Bind-DN und Passwort korrekt sind
- Überprüfen Sie, ob der Benutzer in AD zu Gruppen gehört

Debug-Einstellungen
-------------------

Um Probleme zu untersuchen, können Sie detaillierte SPNEGO-bezogene Protokolle ausgeben, indem Sie die |Fess|-Protokollebene anpassen.

Fügen Sie Folgendes zu ``app/WEB-INF/conf/system.properties`` hinzu:

::

    spnego.logger.level=1

Oder fügen Sie die folgenden Logger zu ``app/WEB-INF/classes/log4j2.xml`` hinzu:

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>
    <Logger name="org.codelibs.spnego" level="DEBUG"/>

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-saml` - SSO-Konfiguration mit SAML-Authentifizierung
- :doc:`sso-oidc` - SSO-Konfiguration mit OpenID Connect-Authentifizierung
- :doc:`sso-entraid` - SSO-Konfiguration mit Microsoft Entra ID

