==================
Sicherheitseinstellungen
==================

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

   Sobald Sie das Passwort von ``admin`` geändert haben, können Sie es nicht mehr auf einen einfachen Wert wie ``admin`` zurücksetzen (eine Sperrliste für Administratorpasswörter wird über ``password.invalid.admin.passwords`` konfiguriert). Außerdem können Sie das Initialpasswort des Benutzers ``admin`` bereits vor dem ersten Start ändern, indem Sie ``index.user.initial_password`` in ``fess_config.properties`` setzen.

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

   Geben Sie die Zugangsdaten über die folgenden Eigenschaften in ``fess_config.properties`` an (es gibt keine Umgebungsvariablen ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``)::

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

**Methode 2: HTTPS-Konfiguration in Fess selbst**

Fügen Sie in ``tomcat_config.properties`` Folgendes hinzu::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[Pfad zur Keystore-Datei]
    tomcat.certificateKeystorePassword=[Passwort, das beim Erstellen der Keystore-Datei angegeben wurde]
    tomcat.certificateKeyAlias=[Zertifikat-Alias]
    tomcat.sslProtocol=[SSL-Protokoll (z.B. TLS)]
    tomcat.enabledProtocols=Liste der aktivierten Protokolle (kommagetrennt) (z.B. TLSv1.2,TLSv1.1,TLSv1)

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

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # Bei benutzerdefiniertem Dienst
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

Alle anderen Rollen können frei über die Verwaltungsseite erstellt werden. In |Fess| ist eine Rolle ein Tag, das nur einen Namen besitzt, und wird hauptsächlich zur Zugriffskontrolle von Suchergebnissen verwendet (welche Dokumente ein Benutzer einsehen darf). Eine Rolle selbst ist nicht an bestimmte administrative Berechtigungen wie ‚Verwaltung von Crawl-Konfigurationen' oder ‚Bearbeitung von Suchergebnissen' gebunden.

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

Regelmäßige Sicherheitsupdates
-------------------------------

Wenden Sie regelmäßig Sicherheitsupdates für |Fess| und OpenSearch an.

**Empfohlene Vorgehensweise:**

1. Regelmäßige Überprüfung von Sicherheitsinformationen

   - `Fess-Versionsinformationen <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch Security Advisories <https://opensearch.org/security.html>`__

2. Überprüfung von Updates in der Testumgebung
3. Anwendung von Updates in der Produktionsumgebung

Datenschutz
===========

Verschlüsselung von Backups
----------------------------

Backup-Daten können vertrauliche Informationen enthalten. Verschlüsseln und speichern Sie Backup-Dateien.

Beispiel für verschlüsselte Backups::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

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

Konfigurieren Sie bei Bedarf Sicherheits-Header in Nginx oder Apache::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

Sicherheits-Checkliste
=======================

Überprüfen Sie vor der Bereitstellung in der Produktionsumgebung folgende Checkliste:

Grundkonfiguration
------------------

- [ ] Administratorpasswort geändert
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
