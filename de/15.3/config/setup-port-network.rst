======================
Port- und Netzwerkkonfiguration
======================

Übersicht
====

Dieser Abschnitt beschreibt die netzwerkbezogenen Konfigurationen von |Fess|.
Er behandelt Einstellungen für Netzwerkverbindungen wie Änderungen der Portnummer, Proxy-Konfiguration und HTTP-Kommunikationseinstellungen.

Konfiguration der verwendeten Ports
================

Standard-Ports
----------------

|Fess| verwendet standardmäßig die folgenden Ports.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Dienst
     - Portnummer
   * - Fess-Webanwendung
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Ändern des Ports der Fess-Webanwendung
--------------------------------------

Konfiguration in Linux-Umgebungen
~~~~~~~~~~~~~~~~~

Um die Portnummer in Linux-Umgebungen zu ändern, bearbeiten Sie ``bin/fess.in.sh``.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

Beispiel für die Verwendung von Port 80:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   Für die Verwendung von Portnummern unter 1024 sind Root-Rechte oder entsprechende Berechtigungen (CAP_NET_BIND_SERVICE) erforderlich.

Konfiguration über Umgebungsvariablen
~~~~~~~~~~~~~~~~~~

Sie können die Portnummer auch über eine Umgebungsvariable angeben.

::

    export FESS_PORT=8080

Bei RPM/DEB-Paketen
~~~~~~~~~~~~~~~~~~~~~~~~

Bei RPM-Paketen bearbeiten Sie ``/etc/sysconfig/fess``, bei DEB-Paketen ``/etc/default/fess``.

::

    FESS_PORT=8080

Konfiguration in Windows-Umgebungen
~~~~~~~~~~~~~~~~~~~

In Windows-Umgebungen bearbeiten Sie ``bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

Bei Registrierung als Windows-Dienst
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wenn Sie |Fess| in einer Windows-Umgebung als Dienst registrieren und verwenden möchten, ändern Sie bitte auch die Portkonfiguration in ``bin\service.bat``.
Weitere Informationen finden Sie unter :doc:`setup-windows-service`.

Konfiguration des Kontextpfads
----------------------

Wenn Sie |Fess| in einem Unterverzeichnis veröffentlichen möchten, können Sie einen Kontextpfad konfigurieren.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

Mit dieser Einstellung wird der Zugriff unter ``http://localhost:8080/search/`` möglich.

.. warning::
   Wenn Sie den Kontextpfad ändern, müssen Sie auch die Pfade für statische Dateien entsprechend konfigurieren.

Proxy-Konfiguration
============

Übersicht
----

Beim Crawlen externer Websites aus einem Intranet oder beim Zugriff auf externe APIs kann die Kommunikation durch eine Firewall blockiert werden.
In solchen Umgebungen ist eine Konfiguration für die Kommunikation über einen Proxy-Server erforderlich.

Proxy-Konfiguration für den Crawler
--------------------------

Grundkonfiguration
~~~~~~~~

Geben Sie in den Crawl-Einstellungen in der Verwaltungsoberfläche die folgenden Konfigurationsparameter an.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

Konfiguration eines Proxys mit Authentifizierung
~~~~~~~~~~~~~~~~~~~~~~~~~~

Wenn der Proxy-Server eine Authentifizierung erfordert, fügen Sie Folgendes hinzu.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

Ausschluss bestimmter Hosts vom Proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um bestimmte Hosts (z. B. Server im Intranet) ohne Proxy zu verbinden:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.nonProxyHosts=localhost|*.local|192.168.*

Systemweite HTTP-Proxy-Konfiguration
------------------------------

Um einen HTTP-Proxy für die gesamte |Fess|-Anwendung zu verwenden, konfigurieren Sie dies in ``fess_config.properties``.

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   Passwörter werden unverschlüsselt gespeichert. Setzen Sie entsprechende Dateiberechtigungen.

HTTP-Kommunikationseinstellungen
============

Beschränkung von Datei-Uploads
--------------------------

Sie können die Größe von Datei-Uploads über die Verwaltungsoberfläche beschränken.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Konfigurationselement
     - Beschreibung
   * - ``http.fileupload.max.size``
     - Maximale Datei-Upload-Größe (Standard: 262144000 Bytes = 250 MB)
   * - ``http.fileupload.threshold.size``
     - Schwellenwertgröße für die Speicherung im Arbeitsspeicher (Standard: 262144 Bytes = 256 KB)
   * - ``http.fileupload.max.file.count``
     - Anzahl der Dateien, die gleichzeitig hochgeladen werden können (Standard: 10)

Konfigurationsbeispiel in ``fess_config.properties``:

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

Einstellungen für Verbindungs-Timeouts
--------------------

Sie können Verbindungs-Timeouts für OpenSearch konfigurieren.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Konfigurationselement
     - Beschreibung
   * - ``search_engine.http.url``
     - OpenSearch-URL (Standard: http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - Intervall für Gesundheitsprüfungen (Millisekunden, Standard: 10000)

Ändern der OpenSearch-Verbindung
----------------------

Für die Verbindung zu einem externen OpenSearch-Cluster:

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

Verbindung zu mehreren Knoten
~~~~~~~~~~~~~~~~~~

Um eine Verbindung zu mehreren OpenSearch-Knoten herzustellen, geben Sie diese durch Kommas getrennt an.

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

Konfiguration von SSL/TLS-Verbindungen
-----------------

Für HTTPS-Verbindungen zu OpenSearch:

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   Für die Zertifikatsvalidierung geben Sie den Pfad zum CA-Zertifikat unter ``certificate_authorities`` an.

Konfiguration virtueller Hosts
==============

Übersicht
----

|Fess| kann Suchergebnisse basierend auf dem Hostnamen, über den darauf zugegriffen wird, unterschiedlich darstellen.
Weitere Informationen finden Sie unter :doc:`security-virtual-host`.

Grundkonfiguration
--------

Konfigurieren Sie den Header für virtuelle Hosts in ``fess_config.properties``.

::

    virtual.host.headers=X-Forwarded-Host,Host

Integration mit Reverse-Proxys
========================

Konfigurationsbeispiel für Nginx
--------------

::

    server {
        listen 80;
        server_name search.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Konfigurationsbeispiel für Apache
---------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

SSL/TLS-Terminierung
-----------

Konfigurationsbeispiel für SSL/TLS-Terminierung am Reverse-Proxy (Nginx):

::

    server {
        listen 443 ssl http2;
        server_name search.example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Firewall-Konfiguration
====================

Öffnen erforderlicher Ports
------------------

Um |Fess| von extern zugänglich zu machen, öffnen Sie die folgenden Ports.

**Konfigurationsbeispiel für iptables:**

::

    # Fess-Webanwendung
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # Für HTTPS-Zugriff (über Reverse-Proxy)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**Konfigurationsbeispiel für firewalld:**

::

    # Fess-Webanwendung
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

Konfiguration von Sicherheitsgruppen (Cloud-Umgebungen)
------------------------------------------

In Cloud-Umgebungen wie AWS, GCP oder Azure öffnen Sie bitte die entsprechenden Ports über Sicherheitsgruppen oder Netzwerk-ACLs.

Empfohlene Konfiguration:
- Eingehend: Ports 80/443 (über HTTP-Reverse-Proxy)
- Port 8080 nur intern zugänglich beschränken
- OpenSearch-Ports 9201/9301 nur intern zugänglich beschränken

Fehlersuche
======================

Kein Zugriff nach Portänderung möglich
------------------------------

1. Überprüfen Sie, ob |Fess| neu gestartet wurde.
2. Überprüfen Sie, ob der entsprechende Port in der Firewall geöffnet ist.
3. Überprüfen Sie Fehler in der Protokolldatei (``fess.log``).

Crawlen über Proxy nicht möglich
------------------------------

1. Überprüfen Sie, ob Hostname und Port des Proxy-Servers korrekt sind.
2. Wenn der Proxy-Server eine Authentifizierung erfordert, konfigurieren Sie Benutzername und Passwort.
3. Überprüfen Sie, ob Verbindungsversuche im Protokoll des Proxy-Servers aufgezeichnet werden.
4. Überprüfen Sie, ob die Konfiguration von ``nonProxyHosts`` korrekt ist.

Keine Verbindung zu OpenSearch möglich
-------------------------

1. Überprüfen Sie, ob OpenSearch läuft.
2. Überprüfen Sie, ob die Einstellung ``search_engine.http.url`` korrekt ist.
3. Überprüfen Sie die Netzwerkverbindung: ``curl http://localhost:9201``
4. Überprüfen Sie Fehler im OpenSearch-Protokoll.

Fehlfunktion beim Zugriff über Reverse-Proxy
----------------------------------------------------

1. Überprüfen Sie, ob der Header ``X-Forwarded-Host`` korrekt konfiguriert ist.
2. Überprüfen Sie, ob der Header ``X-Forwarded-Proto`` korrekt konfiguriert ist.
3. Überprüfen Sie, ob der Kontextpfad korrekt konfiguriert ist.
4. Überprüfen Sie Fehler im Reverse-Proxy-Protokoll.

Referenzinformationen
========

- :doc:`setup-memory` - Speicherkonfiguration
- :doc:`setup-windows-service` - Windows-Dienst-Konfiguration
- :doc:`security-virtual-host` - Konfiguration virtueller Hosts
- :doc:`crawler-advanced` - Erweiterte Crawler-Konfiguration
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
