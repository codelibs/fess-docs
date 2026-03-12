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
2. Klicken Sie auf „System" → „Benutzer"
3. Wählen Sie den Benutzer ``admin``
4. Setzen Sie ein starkes Passwort
5. Klicken Sie auf die Schaltfläche „Aktualisieren"

**Empfohlene Passwort-Richtlinie:**

- Mindestens 12 Zeichen
- Enthält Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen
- Vermeiden Sie Wörter aus dem Wörterbuch
- Regelmäßige Änderung (alle 90 Tage empfohlen)

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

5. Aktualisieren Sie die |Fess|-Konfiguration und fügen Sie OpenSearch-Authentifizierungsinformationen hinzu::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200
       SEARCH_ENGINE_USERNAME=admin
       SEARCH_ENGINE_PASSWORD=<strong_password>

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

Fügen Sie in ``system.properties`` Folgendes hinzu::

    server.ssl.enabled=true
    server.ssl.key-store=/path/to/keystore.p12
    server.ssl.key-store-password=<password>
    server.ssl.key-store-type=PKCS12

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

Rollenbasierte Zugriffskontrolle (RBAC)
----------------------------------------

|Fess| unterstützt mehrere Benutzerrollen. Gemäß dem Prinzip der geringsten Rechte sollten Benutzern nur die minimal erforderlichen Rechte gewährt werden.

**Rollentypen:**

- **Administrator**: Alle Rechte
- **Normaler Benutzer**: Nur Suche
- **Crawler-Administrator**: Verwaltung von Crawl-Konfigurationen
- **Suchergebnis-Editor**: Bearbeitung von Suchergebnissen

**Vorgehensweise:**

1. Klicken Sie in der Verwaltungsseite auf „System" → „Rolle"
2. Erstellen Sie erforderliche Rollen
3. Weisen Sie Benutzern unter „System" → „Benutzer" Rollen zu

Aktivierung von Audit-Protokollen
----------------------------------

Audit-Protokolle sind standardmäßig aktiviert, um Systemoperationsverläufe aufzuzeichnen.

Aktivieren Sie Audit-Protokolle in der Konfigurationsdatei (``log4j2.xml``)::

    <Logger name="org.codelibs.fess.audit" level="info" additivity="false">
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

- [ ] Rollenbasierte Zugriffskontrolle konfiguriert
- [ ] Unnötige Benutzerkonten gelöscht
- [ ] Passwort-Richtlinie konfiguriert

Überwachung und Protokollierung
--------------------------------

- [ ] Audit-Protokolle aktiviert
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
