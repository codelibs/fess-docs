========================
Sicherheitseinstellungen
========================

Diese Seite beschreibt die empfohlenen Sicherheitseinstellungen für den sicheren Betrieb von |Fess| in Produktionsumgebungen.

.. danger::

   **Sicherheit ist äußerst wichtig**

   In Produktionsumgebungen wird dringend empfohlen, alle auf dieser Seite beschriebenen Sicherheitseinstellungen zu implementieren.
   Vernachlässigung der Sicherheitseinstellungen erhöht das Risiko von unbefugtem Zugriff, Datenlecks und Systemkompromittierung.

Erforderliche Sicherheitseinstellungen
=======================================

Änderung des Administratorpassworts
------------------------------------

Das Standard-Administratorpasswort (``admin`` / ``admin``) muss unbedingt geändert werden.

**Vorgehensweise:**

1. Anmeldung in der Verwaltungsseite: http://localhost:8080/admin
2. Klicken Sie auf „Benutzer" → „Benutzer"
3. Wählen Sie den Benutzer ``admin``
4. Setzen Sie ein starkes Passwort
5. Klicken Sie auf die Schaltfläche „Aktualisieren"

.. note::

   Sobald Sie das Passwort von ``admin`` geändert haben, können Sie es nicht mehr auf einen einfachen Wert wie ``admin`` zurücksetzen (eine Sperrliste für Administratorpasswörter wird über ``password.invalid.admin.passwords`` konfiguriert). Außerdem können Sie das Initialpasswort des Benutzers ``admin`` bereits vor dem ersten Start ändern, indem Sie ``index.user.initial_password`` in ``fess_config.properties`` setzen. ``bin/fess-setup init`` setzt es für Sie; siehe :doc:`fess-setup`.

**Empfohlene Passwort-Richtlinie:**

|Fess| bietet eine integrierte Funktion, die die Mindest- und Höchstlänge des Passworts sowie Anforderungen an die Zeichenarten erzwingt. Konfigurieren Sie die folgenden Eigenschaften in ``fess_config.properties`` (Standardwerte in Klammern):

- ``password.min.length`` (Standard: ``8``): Mindestlänge. 12 oder mehr wird empfohlen.
- ``password.max.length`` (Standard: ``100``): Höchstlänge.
- ``password.require.uppercase`` (Standard: ``false``): Großbuchstaben erforderlich.
- ``password.require.lowercase`` (Standard: ``false``): Kleinbuchstaben erforderlich.
- ``password.require.digit`` (Standard: ``false``): Ziffern erforderlich.
- ``password.require.special.char`` (Standard: ``false``): Sonderzeichen erforderlich.

.. note::

   Standardmäßig beträgt die Mindestlänge ``8`` und alle Anforderungen an Zeichenarten sind deaktiviert. Um Passwörter zu stärken, setzen Sie die oben genannten Eigenschaften explizit. Beachten Sie, dass |Fess| keine Funktion zum Ablaufen von Passwörtern (erzwungene regelmäßige Änderung) besitzt. Wenn Sie regelmäßige Passwortänderungen als Betriebsregel durchsetzen möchten, führen Sie diese manuell durch.

**Sitzungen nach einer Passwortänderung:**

Wird das Passwort eines lokalen Benutzers geändert, sei es durch den Benutzer selbst oder durch einen Administrator auf der Benutzerverwaltungsseite oder über die Admin-REST-API, enden die übrigen Anmeldesitzungen dieses Benutzers bei ihrer nächsten Prüfung (siehe unten). Jede Anmeldesitzung liest den Zeitpunkt der letzten Passwortänderung höchstens einmal je ``password.changed.check.interval`` aus ``fess_config.properties`` aus dem Benutzerindex (Standard: ``60`` Sekunden; bei ``0`` oder weniger wird bei jeder Anfrage geprüft), sodass die übrigen Sitzungen auf jedem Knoten innerhalb dieser Anzahl von Sekunden enden. Über LDAP oder SSO authentifizierte Benutzer sind nicht betroffen, da ihre Passwörter außerhalb von |Fess| verwaltet werden.

Chiffrierschlüssel ändern
-------------------------

``app.cipher.key`` in ``fess_config.properties`` ist der Schlüssel, der die in Crawl-Konfigurationen und Datenspeicher-Konfigurationen gespeicherten Passwörter verschlüsselt. Der mitgelieferte Wert (``___change__me___``) ist öffentlich bekannt. Ist der Schlüssel leer oder noch der mitgelieferte Wert, schreibt |Fess| beim Start eine Warnung in ``fess.log`` (siehe :ref:`upgrade-1510-cipher-key`). |Fess| ändert den Schlüssel nicht selbstständig.

Legen Sie ihn vor dem ersten Start fest, zusammen mit dem Initialpasswort des Benutzers ``admin``::

    $ bin/fess-setup init

Bei den RPM- und DEB-Paketen führen Sie ``/usr/share/fess/bin/fess-setup init`` aus. Der Befehl erzeugt einen zufälligen Schlüssel oder übernimmt einen mit ``--cipher-key`` angegebenen; siehe :doc:`fess-setup`. Um ihn stattdessen von Hand zu setzen, bearbeiten Sie ``app.cipher.key`` in ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` beim ZIP-Paket, ``/etc/fess/fess_config.properties`` bei den RPM- und DEB-Paketen). Mit dem Standardwert ``aes`` für ``app.cipher.algorithm`` muss der Schlüssel 16, 24 oder 32 Zeichen lang sein.

.. warning::

   Wird der Schlüssel geändert, nachdem Passwörter in Crawl- oder Datenspeicher-Konfigurationen gespeichert wurden, lassen sich diese Werte nicht mehr entschlüsseln. Bewahren Sie den Schlüssel zusammen mit Ihren Sicherungen von ``fess_config.properties`` auf und verwenden Sie bei einem Umzug auf eine andere Installation denselben Schlüssel.

Aktivierung des OpenSearch-Sicherheits-Plugins
-----------------------------------------------

**Vorgehensweise:**

1. Entfernen oder kommentieren Sie folgende Zeile in ``opensearch.yml``::

       # plugins.security.disabled: true

2. Konfiguration des Sicherheits-Plugins::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. Konfiguration von TLS/SSL-Zertifikaten

4. Neustart von OpenSearch

5. Konfigurieren Sie auf Seiten von |Fess| die Verbindung zu OpenSearch.

   Geben Sie die Verbindungs-URL über die Umgebungsvariable ``SEARCH_ENGINE_HTTP_URL`` an (bearbeiten Sie ``bin/fess.in.sh`` oder die Umgebungsdatei des Dienstes; der Standardwert stammt aus ``search_engine.http.url`` in ``fess_config.properties``)::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   Geben Sie die Zugangsdaten über die folgenden Eigenschaften in ``fess_config.properties`` an (die ZIP-, RPM- und DEB-Pakete kennen die Umgebungsvariablen ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD`` nicht; die docker-fess-Images unterstützen sie)::

       search_engine.username=admin
       search_engine.password=<strong_password>

Details finden Sie unter `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__.

Aktivierung von HTTPS
----------------------

HTTP-Kommunikation ist nicht verschlüsselt und birgt Risiken von Abhören und Manipulation. In Produktionsumgebungen muss unbedingt HTTPS verwendet werden.

**Methode 1: Verwendung eines Reverse-Proxys (empfohlen)**

Platzieren Sie Nginx oder Apache vor |Fess| für HTTPS-Terminierung.

Nginx-Konfigurationsbeispiel::

    server {
        listen 443 ssl http2;
        server_name ihre-fess-domain.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

Wenn TLS am Reverse-Proxy terminiert wird, setzen Sie zusätzlich Folgendes in ``fess_config.properties``, damit das Session-Cookie das Attribut ``Secure`` erhält. Starten Sie |Fess| nach der Änderung neu. Setzen Sie den Wert nicht, wenn Benutzer |Fess| auch über unverschlüsseltes HTTP aufrufen, da dann über HTTP keine Sitzung aufgebaut werden kann::

    session.cookie.secure=true

**Methode 2: HTTPS-Konfiguration in Fess selbst**

Fügen Sie in ``tomcat_config.properties`` Folgendes hinzu::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[Pfad zur Keystore-Datei]
    tomcat.certificateKeystorePassword=[Passwort, das beim Erstellen der Keystore-Datei angegeben wurde]
    tomcat.certificateKeyAlias=[Zertifikat-Alias]
    tomcat.sslProtocol=[SSL-Protokoll (z.B. TLS)]
    tomcat.enabledProtocols=Liste der aktivierten Protokolle (kommagetrennt) (z.B. TLSv1.2,TLSv1.3)

Empfohlene Sicherheitseinstellungen
====================================

Firewall-Konfiguration
-----------------------

Öffnen Sie nur erforderliche Ports und schließen Sie unnötige Ports.

**Zu öffnende Ports:**

- **8080** (oder HTTPS 443): |Fess| Weboberfläche (bei externem Zugriff erforderlich)
- **22**: SSH (nur für Verwaltung, nur von vertrauenswürdigen IP-Adressen)

**Zu schließende Ports:**

- **9200, 9300**: OpenSearch (nur interne Kommunikation, externer Zugriff blockieren)

Linux (firewalld) Konfigurationsbeispiel::

    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --add-port=8080/tcp  # nur bei direktem Zugriff auf Fess über Port 8080
    $ sudo firewall-cmd --reload

IP-Adressbeschränkung::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

Zugriffskontroll-Konfiguration
-------------------------------

Erwägen Sie, den Zugriff auf die Verwaltungsseite auf bestimmte IP-Adressen zu beschränken.

Nginx-Zugriffsbeschränkungsbeispiel::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

Rollen und Zugriffskontrolle
----------------------------

|Fess| stellt standardmäßig zwei Rollen bereit:

- ``admin``: Administratorrolle, die alle Operationen einschließlich der Verwaltungsseite ausführen kann.
- ``guest``: Rolle, die nicht angemeldeten (anonymen) Benutzern zugewiesen wird.

Alle anderen Rollen können frei über die Verwaltungsseite erstellt werden. In |Fess| ist eine Rolle ein Tag, das nur einen Namen besitzt, und wird hauptsächlich zur Zugriffskontrolle von Suchergebnissen verwendet (welche Dokumente ein Benutzer einsehen darf). Eine Ausnahme bildet eine Rolle mit dem Namen ``admin-``, gefolgt vom Namen einer Verwaltungsseite, etwa ``admin-user`` oder ``admin-scheduler``: Sie erlaubt es einem Benutzer, diese Seite zu öffnen, und die ``-view``-Form, etwa ``admin-user-view``, erlaubt reinen Lesezugriff.

.. warning::

   Die ``admin-*``-Rollen ermöglichen es, alltägliche Verwaltungsseiten auf mehrere Betreiber aufzuteilen, sie sind jedoch keine Berechtigungsgrenze. Ein Benutzer mit ``admin-user`` kann jedem Benutzer eine beliebige vorhandene Rolle zuweisen, einschließlich der Administratorrolle; ``admin-accesstoken`` kann ein Zugriffstoken mit der Berechtigung ``Radmin-api`` ausstellen, die die gesamte Admin API freigibt; ``admin-scheduler`` kann Skript-Jobs auf dem Server ausführen, und ``admin-plugin`` kann Plugins installieren. Behandeln Sie jede ``admin-*``-Rolle wie die Administratorrolle (``authentication.admin.roles``, Standardwert ``admin``) und gewähren Sie sie nur vertrauenswürdigen Betreibern.

Befolgen Sie das Prinzip der geringsten Rechte: Gewähren Sie die Administratorrolle (``admin``) nur Benutzern, die administrative Aufgaben durchführen, und nicht allgemeinen Suchbenutzern.

**Vorgehensweise:**

1. Klicken Sie in der Verwaltungsseite auf „Benutzer" → „Rolle"
2. Erstellen Sie die erforderlichen Rollen
3. Weisen Sie Benutzern unter „Benutzer" → „Benutzer" Rollen zu

Audit-Protokollierung
----------------------

Der Systembetriebsverlauf, wie Authentifizierung und administrative Operationen, wird standardmäßig als Audit-Protokoll aufgezeichnet. Das Audit-Protokoll wird vom Logger ``fess.log.audit`` ausgegeben, der in ``log4j2.xml`` definiert ist, und sein Standard-Ausgabeziel ist ``audit.log``.

Da dies standardmäßig aktiviert ist, ist keine zusätzliche Konfiguration erforderlich. Um das Ausgabeziel oder die Protokollstufe anzupassen, bearbeiten Sie die folgende Definition in ``log4j2.xml``::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

Jeder Audit-Eintrag ist eine Zeile aus tabulatorgetrennten ``key:value``-Feldern (LTSV). Ein Eintrag beginnt mit ``action`` und endet mit ``ip`` (der IP-Adresse des Clients) und ``time`` (UTC, ISO 8601). Ist ``app.audit.log.format`` auf ``ecs`` gesetzt, oder ist es leer und die Umgebungsvariable ``FESS_APP_TYPE`` hat den Wert ``docker``, werden die Einträge stattdessen als ECS-JSON geschrieben, mit den Feldern als ``labels.<key>``.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Aktion
     - Felder
     - Wird geschrieben, wenn
   * - ``LOGIN``
     - ``user``, ``permissions``
     - sich ein Benutzer anmeldet.
   * - ``LOGOUT``
     - ``user``, ``permissions``
     - sich ein Benutzer abmeldet.
   * - ``LOGIN_FAILURE``
     - ``class``, ``user``
     - eine Anmeldung abgelehnt wird, im Anmeldeformular, in der Anmelde-API oder per SSO. Auch eine Anmeldung, die ein SSO-Authentifikator mit einer Ausnahme ablehnt, wird erfasst.
   * - ``ACCESS``
     - ``user``, ``path``, ``execute``, ``method``, ``id``
     - eine Anfrage an eine Verwaltungsseite oder die Admin-REST-API eingeht, bevor die Aktion ausgeführt wird. Bei der Admin-REST-API geschieht das, nachdem das Zugriffstoken akzeptiert wurde.
   * - ``ACCESS_DENIED``
     - ``user``, ``path``
     - eine Anfrage an eine Verwaltungsseite wegen der Rollen des Benutzers abgelehnt wird oder eine Anfrage an die Admin-REST-API von der Prüfung des Zugriffstokens abgelehnt wird (die API antwortet mit HTTP 401).
   * - ``UPDATE_PASSWORD``
     - ``user``, ``target``
     - ein Passwort geändert wird: von einem Benutzer über die Anmeldeseite oder ``/api/v2/auth/password`` oder von einem Administrator, der auf der Benutzerverwaltungsseite oder über die Admin-REST-API ein neues Passwort für einen Benutzer setzt.
   * - ``UPDATE_PERMISSION``
     - ``user``, ``permissions``
     - die Berechtigungen eines LDAP-Benutzers aktualisiert werden.
   * - ``SCRIPT_EXECUTION``
     - ``scriptType``, ``source``, ``user``, ``result``, ``script``
     - ein Skript ausgeführt wird. Siehe :doc:`../config/scripting-overview`.

- ``LOGIN_FAILURE``: ``user`` ist der eingegebene Benutzername und ``class`` der Typ der Anmeldeinformationen. Lehnt ein SSO-Authentifikator eine Anmeldung mit einer Ausnahme ab, wurden keine Anmeldeinformationen ermittelt; der Eintrag enthält dann weder ``user`` noch ``class``, und nichts aus der Ausnahme wird geschrieben.
- ``ACCESS``: ``method`` ist die HTTP-Methode. ``id`` ist der Wert des Anfrageparameters ``id`` und wird nur geschrieben, wenn die Anfrage ihn enthält (bei einer Upload-Anfrage wird er nicht gelesen). Kein anderer Anfrageparameter wird geschrieben, weil die Verwaltungsformulare Passwörter und Schlüssel enthalten.
- ``ACCESS_DENIED``: Bei einer abgelehnten Anfrage an die Admin-REST-API wird nur der Pfad der Anfrage geschrieben. Weder das Zugriffstoken noch der Parameter, der es übermittelt hat, wird erfasst.
- ``UPDATE_PASSWORD``: ``user`` ist der Benutzer, der das Passwort geändert hat, und ``target`` der Name des Benutzers, dessen Passwort geändert wurde. Das Passwort und sein Hash werden nie geschrieben, und eine abgelehnte Änderung erzeugt keinen Eintrag.

Regelmäßige Sicherheitsupdates
-------------------------------

Wenden Sie regelmäßig Sicherheitsupdates für |Fess| und OpenSearch an.

**Empfohlene Vorgehensweise:**

1. Regelmäßige Überprüfung von Sicherheitsinformationen

   - `Fess-Versionsinformationen <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch Security Advisories <https://github.com/opensearch-project/OpenSearch/security/advisories>`__

2. Überprüfung von Updates in der Testumgebung
3. Anwendung von Updates in der Produktionsumgebung

Datenschutz
===========

Verschlüsselung von Backups
----------------------------

Backup-Daten können vertrauliche Informationen enthalten. Verschlüsseln und speichern Sie Backup-Dateien.

Beispiel für verschlüsselte Backups::

    $ tar czf fess-backup.tar.gz /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

Das Datenverzeichnis eines laufenden OpenSearch (``/var/lib/opensearch``) lässt sich durch Kopieren der Dateien nicht konsistent sichern. Verwenden Sie für die Indexdaten die `Snapshot-Funktion von OpenSearch <https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`__. Die Konfigurationsdaten von |Fess| können auf der Backup-Seite der Administrationsoberfläche heruntergeladen werden (siehe :doc:`../admin/backup-guide`).

Sicherheits-Best-Practices
===========================

Prinzip der geringsten Rechte
------------------------------

- Fess und OpenSearch nicht als Root-Benutzer ausführen
- Mit dediziertem Benutzerkonto ausführen
- Minimal erforderliche Dateisystemberechtigungen gewähren

Netzwerk-Isolation
------------------

- OpenSearch in privatem Netzwerk platzieren
- VPN oder privates Netzwerk für interne Kommunikation verwenden
- Nur |Fess| Weboberfläche in DMZ platzieren

Regelmäßige Sicherheitsaudits
------------------------------

- Regelmäßige Überprüfung von Zugriffslogs
- Erkennung abnormaler Zugriffsmuster
- Regelmäßige Durchführung von Schwachstellen-Scans

Konfiguration von Sicherheits-Headern
--------------------------------------

|Fess| setzt bei HTML-Antworten standardmäßig ``X-Frame-Options: SAMEORIGIN`` (``response.headers`` in ``fess_config.properties``); der Header muss daher nicht im Proxy ergänzt werden.

Konfigurieren Sie bei Bedarf Sicherheits-Header in Nginx oder Apache::

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

Sicherheits-Checkliste
=======================

Überprüfen Sie vor der Bereitstellung in der Produktionsumgebung folgende Checkliste:

Grundkonfiguration
------------------

- [ ] Administratorpasswort geändert
- [ ] Chiffrierschlüssel (``app.cipher.key``) vom mitgelieferten Wert geändert
- [ ] HTTPS aktiviert
- [ ] Standard-Portnummer geändert (optional)

Netzwerksicherheit
------------------

- [ ] Unnötige Ports mit Firewall geschlossen
- [ ] Zugriff auf Verwaltungsseite IP-beschränkt (falls möglich)
- [ ] Zugriff auf OpenSearch nur auf internes Netzwerk beschränkt

Zugriffskontrolle
-----------------

- [ ] Rollen und Zugriffsberechtigungen angemessen konfiguriert (Administratorrolle nur an notwendige Benutzer vergeben)
- [ ] Unnötige Benutzerkonten gelöscht
- [ ] Passwort-Richtlinie konfiguriert

Überwachung und Protokollierung
--------------------------------

- [ ] Bestätigt, dass die Audit-Protokollierung aktiviert ist
- [ ] Aufbewahrungsdauer für Protokolle konfiguriert
- [ ] Log-Überwachungsmechanismus eingerichtet (falls möglich)

Backup und Recovery
-------------------

- [ ] Regelmäßiger Backup-Zeitplan konfiguriert
- [ ] Backup-Daten verschlüsselt
- [ ] Wiederherstellungsverfahren getestet

Update- und Patch-Management
-----------------------------

- [ ] Mechanismus zum Empfangen von Sicherheitsupdate-Benachrichtigungen eingerichtet
- [ ] Update-Verfahren dokumentiert
- [ ] System zur Überprüfung von Updates in Testumgebung eingerichtet

Reaktion auf Sicherheitsvorfälle
=================================

Reaktionsverfahren bei Sicherheitsvorfällen:

1. **Erkennung von Vorfällen**

   - Überprüfung von Protokollen
   - Erkennung abnormaler Zugriffsmuster
   - Überprüfung von Systemanormalitäten

2. **Erstreaktion**

   - Identifizierung des Umfangs der Auswirkungen
   - Verhinderung der Schadensausweitung (Stoppen betroffener Dienste etc.)
   - Sicherung von Beweisen

3. **Untersuchung und Analyse**

   - Detaillierte Analyse von Protokollen
   - Identifizierung des Eindringwegs
   - Identifizierung möglicherweise durchgesickerter Daten

4. **Wiederherstellung**

   - Behebung von Schwachstellen
   - Systemwiederherstellung
   - Verstärkung der Überwachung

5. **Nachbereitung**

   - Erstellung eines Vorfallsberichts
   - Umsetzung von Präventivmaßnahmen
   - Berichterstattung an Stakeholder

Referenzinformationen
======================

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

Bei Fragen oder Problemen zur Sicherheit wenden Sie sich bitte an:

- Issues: https://github.com/codelibs/fess/issues
- Kommerzieller Support: https://www.n2sm.net/
