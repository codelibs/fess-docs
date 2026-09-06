============================================================
SSO-Konfiguration mit Windows-integrierter Authentifizierung
============================================================

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

- |Fess| 15.8 oder höher ist installiert
- Ein Active Directory (AD)-Server ist verfügbar
- |Fess|-Server ist von der AD-Domäne aus erreichbar
- Sie haben die Berechtigung, Dienstprinzipalnamen (SPN) in AD zu konfigurieren
- Ein Konto zum Abrufen von Benutzerinformationen über LDAP ist verfügbar

Active Directory-seitige Konfiguration
=======================================

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
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

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

.. warning::
   Ein Service-Ticket mit einem Verschlüsselungstyp, der nicht in ``permitted_enctypes`` aufgeführt ist,
   wird von der Kerberos-Gegenstelle mit ``encryption type not in permitted_enctypes list`` abgelehnt.
   Active Directory stellt in der Regel AES256-Service-Tickets aus, daher muss AES256 enthalten sein.

.. note::
   RC4 (``rc4-hmac``), 3DES und DES sind ab Java 17 standardmäßig deaktiviert; sie aufzuführen hat
   keine Wirkung. Das obige Beispiel gibt daher nur AES an.
   ``aes256-cts-hmac-sha384-192`` und ``aes128-cts-hmac-sha256-128`` sind die von Windows Server 2025
   unterstützten AES-SHA2-Typen (RFC 8009).
   Ein Dienstkonto, das nur einen RC4-Schlüssel besitzt, kann nicht für die Kerberos-Authentifizierung
   verwendet werden. Setzen Sie sein Kennwort zurück, damit AES-Schlüssel erzeugt werden.

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

.. note::
   Die Standarddateinamen für ``krb5.conf`` und ``auth_login.conf`` werden über ``spnego.krb5.conf`` bzw. ``spnego.login.conf`` festgelegt, die Dateien selbst müssen jedoch zwingend erstellt werden.
   SPNEGO wird bei der ersten Anmeldung initialisiert. Fehlen diese Dateien, startet |Fess| zwar, die SSO-Anmeldung schlägt jedoch fehl.

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
     - (Erforderlich, sofern kein Keytab verwendet wird)
   * - ``spnego.preauth.password``
     - AD-Verbindungspasswort
     - (Erforderlich, sofern kein Keytab verwendet wird)
   * - ``spnego.krb5.conf``
     - Pfad zur Kerberos-Konfigurationsdatei
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Pfad zur Login-Konfigurationsdatei
     - ``auth_login.conf``

.. note::
   Bleiben ``spnego.preauth.username`` und ``spnego.preauth.password`` beide leer, verwendet das
   Server-Login-Modul eine Keytab-Datei.
   Wenn Sie das Kennwort des AD-Dienstkontos nicht in einer |Fess|-Konfigurationsdatei speichern
   möchten, erstellen Sie eine Keytab-Datei und konfigurieren Sie ``spnego-server`` in
   ``auth_login.conf`` wie folgt.

   ::

       spnego-server {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/var/lib/fess/fess.keytab"
           principal="HTTP/fess-server.example.local@EXAMPLE.LOCAL"
           storeKey=true
           isInitiator=false;
       };

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
     - ``false``
   * - ``spnego.prompt.ntlm``
     - Bei Empfang eines NTLM-Tokens auf Basic-Authentifizierung zurückfallen
     - ``true``
   * - ``spnego.allow.localhost``
     - Localhost-Zugriff erlauben
     - ``false``
   * - ``spnego.allow.delegation``
     - Delegierung erlauben
     - ``false``
   * - ``spnego.allowed.realms``
     - Zusätzlich zur Server-Realm akzeptierte Kerberos-Realms (kommagetrennt)
     - (Keine)
   * - ``spnego.logger.level``
     - Interner Protokollierungsgrad der SPNEGO-Bibliothek (``1`` =FINEST, ``2`` =FINER, ``3`` =FINE, ``4`` =CONFIG, ``6`` =WARNING, ``7`` =SEVERE; alle anderen Werte einschließlich ``0`` und ``5`` werden als INFO behandelt)
     - (Automatisch)

.. warning::
   ``spnego.allow.unsecure.basic=true`` kann Base64-kodierte Anmeldeinformationen über unverschlüsselte Verbindungen senden.
   Für Produktionsumgebungen wird dringend empfohlen, dies auf ``false`` zu setzen und HTTPS zu verwenden.

.. note::
   Mit ``spnego.allow.unsecure.basic=false`` (Standard) wird die Basic-Authentifizierung nur für
   Anfragen angeboten, bei denen ``HttpServletRequest#isSecure()`` ``true`` zurückgibt.
   Wird TLS an einem Reverse-Proxy terminiert und die Anfrage per HTTP an |Fess| weitergeleitet,
   ist dieser Wert ``false``. Ein Client, der kein Kerberos-Ticket erhalten kann und auf NTLM
   zurückfällt, kann sich dann nicht anmelden. Setzen Sie ``tomcat.secure=true`` in
   ``tomcat_config.properties``, damit |Fess| die Anfrage als über HTTPS eingegangen behandelt.
   Diese Datei liegt in der ZIP-Distribution unter ``lib/classes/`` und in den DEB/RPM-Paketen
   unter ``/etc/fess/``; nach einer Änderung muss |Fess| neu gestartet werden.

.. note::
   Mit ``spnego.allow.delegation=true`` nimmt die SPNEGO-Bibliothek die vom Client delegierten
   Kerberos-Anmeldeinformationen entgegen und verknüpft sie mit dem authentifizierten Principal.
   |Fess| verwendet diese Anmeldeinformationen derzeit jedoch an keiner Stelle: Crawling, Suche und
   LDAP-Abfragen greifen ausschließlich auf den Benutzernamen zurück. Auf den SPNEGO-Handshake
   selbst wirkt sich die Einstellung ebenfalls nicht aus — die Acceptor-Anmeldeinformationen und
   die Flags des GSS-Kontexts bleiben unverändert, und ob überhaupt delegiert wird, entscheidet
   allein der Client (die Browser-Konfiguration und ob dem Konto in Active Directory für
   Delegierungszwecke vertraut wird). Belassen Sie die Einstellung beim Standardwert ``false``;
   ist sie aktiviert, versucht das JDK bei jeder authentifizierten Anfrage eine eingeschränkte
   Delegierung — ohne jeden Nutzen.

.. warning::
   In |Fess| 15.8 wird eine Anmeldung standardmäßig abgelehnt, wenn sich die Realm des
   Client-Principals von der Realm des Servers unterscheidet. Melden sich Benutzer aus einer
   untergeordneten Domäne einer AD-Domänenstruktur oder aus einer vertrauten Gesamtstruktur an,
   tragen Sie diese Realms kommagetrennt in ``spnego.allowed.realms`` ein. Andernfalls werden
   Benutzer, die sich bis 15.7 anmelden konnten, mit ``Kerberos realm is not allowed``
   abgewiesen.

.. warning::
   |Fess| identifiziert einen Benutzer über den Teil des Principals vor ``@``; die Realm ist damit
   nicht Teil des Benutzernamens. Wenn Sie in ``spnego.allowed.realms`` weitere Realms eintragen,
   werden Benutzer, die denselben Kontonamen in mehreren Realms besitzen — zum Beispiel
   ``alice@CORP.EXAMPLE.COM`` und ``alice@PARTNER.EXAMPLE.COM`` — zu demselben |Fess|-Benutzer
   und teilen sich dessen Gruppen, Rollen und Dokumentberechtigungen. Tragen Sie eine Realm nur
   dann ein, wenn der Kontoname über alle aufgeführten Realms hinweg genau eine Person
   identifiziert.

.. note::
   Die Zulassungsliste gilt auch für den Rückfall auf die Basic-Authentifizierung. Gibt ein
   Benutzer einen Namen der Form ``user@REALM`` ein, wird diese Realm gegen
   ``spnego.allowed.realms`` geprüft und die Anmeldung abgelehnt, wenn sie nicht zulässig ist. Ein
   einfacher Kontoname oder die Form ``DOMAIN\user`` benennt keine Realm und wird in der
   Standard-Realm aus ``krb5.conf`` authentifiziert. Da eine Basic-Anmeldung direkt gegen die vom
   Benutzer eingegebene Realm authentifiziert wird, halten Sie die Zulassungsliste möglichst klein
   und setzen Sie ``spnego.allow.basic`` auf ``false``, wenn Sie sich auf sie als Sicherheitsgrenze
   verlassen.

.. note::
   Wenn ``spnego.prompt.ntlm=true`` (Standard), muss auch ``spnego.allow.basic`` auf ``true`` gesetzt sein.
   Wenn Sie ``spnego.allow.basic=false`` setzen, müssen Sie gleichzeitig ``spnego.prompt.ntlm=false`` setzen.
   Wird diese Bedingung nicht erfüllt, tritt bei der SPNEGO-Initialisierung ein Fehler auf.

.. note::
   ``spnego.logger.level`` steuert den Protokollierungsgrad des internen Loggers der SPNEGO-Bibliothek (``java.util.logging``-Logger mit dem Namen ``Spnego``).
   Wenn nicht gesetzt, wird er automatisch entsprechend dem Protokollierungsgrad von |Fess| bestimmt.

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

.. note::
   |Fess| liest das Attribut ``memberOf`` des Benutzers nur eine Ebene tief, sodass verschachtelte
   Gruppen (eine Gruppe als Mitglied einer anderen Gruppe) standardmäßig nicht aufgelöst werden.
   Um verschachtelte AD-Gruppen abzubilden, setzen Sie unter „System“ → „Allgemein“ in der
   Administrationsoberfläche den Gruppenfilter (``ldap.group.filter``) auf
   ``(member:1.2.840.113556.1.4.1941:=%s)``. Die Auflösung läuft nach der Anmeldung asynchron,
   daher enthält der Anmeldeeintrag im Audit-Log nur die zuvor aufgelösten Gruppen.

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
------------------------------------

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
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

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
------------------------------------------

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
    spnego.prompt.ntlm=false
    spnego.allow.localhost=false

.. note::
   Wenn Sie ``spnego.allow.basic=false`` setzen, müssen Sie auch ``spnego.prompt.ntlm=false`` zwingend setzen.
   Da ``spnego.prompt.ntlm`` standardmäßig ``true`` ist, tritt bei der Initialisierung ein Fehler auf, wenn diese Einstellung weggelassen wird.

Fehlerbehebung
==============

Häufige Probleme und Lösungen
------------------------------

Authentifizierungsdialog erscheint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob der Fess-Server in den Browser-Einstellungen zur Zone "Lokales Intranet" hinzugefügt wurde
- Überprüfen Sie, ob "Integrierte Windows-Authentifizierung aktivieren" aktiviert ist
- Überprüfen Sie, ob der SPN korrekt registriert ist (``setspn -L <Benutzername>``)

Authentifizierungsfehler treten auf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob der Domänenname (Großbuchstaben) und der AD-Servername in ``krb5.conf`` korrekt sind
- Überprüfen Sie, ob ``spnego.preauth.username`` und ``spnego.preauth.password`` korrekt sind
- Überprüfen Sie die Netzwerkverbindung zum AD-Server

Gruppeninformationen können nicht abgerufen werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die LDAP-Einstellungen korrekt sind
- Überprüfen Sie, ob Bind-DN und Passwort korrekt sind
- Überprüfen Sie, ob der Benutzer in AD zu Gruppen gehört

Die Anmeldung liefert HTTP 400
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bei Benutzern mit vielen Gruppenmitgliedschaften wird das Kerberos-Ticket (PAC) groß, und der
``Authorization``-Header kann Tomcats Standardgrenze von 8 KB überschreiten, was mit 400 beantwortet wird.
Die Anfrage erreicht |Fess| nie, daher wird nichts protokolliert.
Erhöhen Sie das Limit in ``tomcat_config.properties``.

::

    tomcat.maxHttpHeaderSize=65536

Nach Änderung des Dienstkonto-Kennworts schlägt die Authentifizierung fehl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Server-Anmeldeinformationen werden einmalig bei der ersten Anmeldung ermittelt und für die
Laufzeit des Prozesses zwischengespeichert.
Starten Sie |Fess| neu, nachdem Sie das Kennwort des Dienstkontos in AD geändert oder die
Keytab-Datei ersetzt haben. Ebenso ist nach einer Änderung von ``spnego.*``-Einstellungen ein
Neustart erforderlich.

Debug-Einstellungen
--------------------

Um Probleme zu untersuchen, können Sie detaillierte SPNEGO-bezogene Protokolle ausgeben.

Um detaillierte interne Protokolle der SPNEGO-Bibliothek auszugeben, fügen Sie Folgendes zu ``app/WEB-INF/conf/system.properties`` hinzu.
``spnego.logger.level=1`` gibt die ausführlichsten Protokolle (FINEST) aus.

::

    spnego.logger.level=1

Um detaillierte Protokolle der SPNEGO-Integrations-Verarbeitung auf der |Fess|-Seite (Paket ``org.codelibs.fess.sso.spnego``) auszugeben, fügen Sie den folgenden Logger zu ``app/WEB-INF/classes/log4j2.xml`` hinzu.

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>

.. note::
   Die Protokolle der SPNEGO-Bibliothek selbst werden über ``java.util.logging`` ausgegeben und daher über ``spnego.logger.level`` und nicht über ``log4j2.xml`` gesteuert.
   Die Protokolle der Integrations-Verarbeitung auf der |Fess|-Seite werden über den Logger in ``log4j2.xml`` gesteuert.

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-saml` - SSO-Konfiguration mit SAML-Authentifizierung
- :doc:`sso-oidc` - SSO-Konfiguration mit OpenID Connect-Authentifizierung
- :doc:`sso-entraid` - SSO-Konfiguration mit Microsoft Entra ID
