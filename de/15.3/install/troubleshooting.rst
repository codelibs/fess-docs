==================
Fehlerbehebung
==================

Diese Seite beschreibt häufige Probleme und deren Lösungen bei Installation, Start und Betrieb von |Fess|.

Probleme bei der Installation
==============================

Java wird nicht erkannt
-----------------------

**Symptom:**

::

    -bash: java: command not found

Oder::

    'java' is not recognized as an internal or external command

**Ursache:**

Java ist nicht installiert oder die PATH-Umgebungsvariable ist nicht korrekt gesetzt.

**Lösung:**

1. Überprüfen Sie, ob Java installiert ist::

       $ which java
       $ java -version

2. Falls nicht installiert, installieren Sie Java 21::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. Setzen Sie die JAVA_HOME-Umgebungsvariable::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   Fügen Sie für permanente Einstellung zu ``~/.bashrc`` oder ``/etc/profile`` hinzu.

Plugin-Installation schlägt fehl
---------------------------------

**Symptom:**

::

    ERROR: Plugin installation failed

**Ursache:**

- Netzwerkverbindungsprobleme
- Plugin-Version stimmt nicht mit OpenSearch-Version überein
- Berechtigungsprobleme

**Lösung:**

1. Überprüfen Sie die OpenSearch-Version::

       $ /path/to/opensearch/bin/opensearch --version

2. Passen Sie die Plugin-Version an die OpenSearch-Version an::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0

3. Überprüfen Sie Berechtigungen::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. Bei Installation über Proxy::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

Probleme beim Start
===================

Fess startet nicht
------------------

**Symptom:**

Beim Ausführen des Fess-Startbefehls tritt ein Fehler auf oder es endet sofort.

**Prüfpunkte:**

1. **Überprüfen Sie, ob OpenSearch läuft**::

       $ curl http://localhost:9200/

   Bei normalem Betrieb wird eine JSON-Antwort zurückgegeben.

2. **Überprüfen Sie Portnummer-Konflikte**::

       $ sudo netstat -tuln | grep 8080

   Falls Port 8080 bereits verwendet wird, ändern Sie die Portnummer in der Konfigurationsdatei.

3. **Überprüfen Sie Protokolldateien**::

       $ tail -f /path/to/fess/logs/fess.log

   Identifizieren Sie die Ursache anhand der Fehlermeldungen.

4. **Überprüfen Sie die Java-Version**::

       $ java -version

   Vergewissern Sie sich, dass Java 21 oder höher installiert ist.

5. **Überprüfen Sie Speichermangel**::

       $ free -h

   Bei Speichermangel passen Sie die Heap-Größe an oder erhöhen Sie den Systemspeicher.

OpenSearch startet nicht
-------------------------

**Symptom:**

::

    ERROR: bootstrap checks failed

**Ursache:**

Die Systemkonfiguration erfüllt nicht die Anforderungen von OpenSearch.

**Lösung:**

1. **Einstellung von vm.max_map_count**::

       $ sudo sysctl -w vm.max_map_count=262144

   Permanente Einstellung::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **Erhöhung der Dateideskriptor-Grenze**::

       $ sudo vi /etc/security/limits.conf

   Fügen Sie Folgendes hinzu::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **Einstellung für Memory-Lock**::

       $ sudo vi /etc/security/limits.conf

   Fügen Sie Folgendes hinzu::

       opensearch  -  memlock  unlimited

4. OpenSearch neu starten::

       $ sudo systemctl restart opensearch

Portnummer-Konflikt
-------------------

**Symptom:**

::

    Address already in use

**Lösung:**

1. Überprüfen Sie verwendete Ports::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. Stoppen Sie den verwendenden Prozess oder ändern Sie die Fess-Portnummer

   Ändern Sie die Portnummer in der Konfigurationsdatei (``system.properties``)::

       server.port=9080

Verbindungsprobleme
===================

Fess kann nicht mit OpenSearch verbinden
-----------------------------------------

**Symptom:**

Im Protokoll werden folgende Fehler angezeigt::

    Connection refused
    oder
    No route to host

**Lösung:**

1. **Überprüfen Sie, ob OpenSearch läuft**::

       $ curl http://localhost:9200/

2. **Überprüfen Sie die Verbindungs-URL**

   Überprüfen Sie, ob die in ``fess.in.sh`` oder ``fess.in.bat`` gesetzte URL korrekt ist::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **Überprüfen Sie die Firewall**::

       $ sudo firewall-cmd --list-all

   Überprüfen Sie, ob Port 9200 geöffnet ist.

4. **Überprüfen Sie die Netzwerkverbindung**

   Bei Ausführung von OpenSearch auf einem anderen Host::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

Kein Zugriff auf Fess über den Browser
---------------------------------------

**Symptom:**

Kein Zugriff auf http://localhost:8080/ über den Browser möglich.

**Lösung:**

1. **Überprüfen Sie, ob Fess läuft**::

       $ ps aux | grep fess

2. **Versuchen Sie Zugriff über Localhost**::

       $ curl http://localhost:8080/

3. **Überprüfen Sie die Firewall**::

       $ sudo firewall-cmd --list-all

   Überprüfen Sie, ob Port 8080 geöffnet ist.

4. **Bei Zugriff von einem anderen Host**

   Überprüfen Sie, ob Fess auf mehr als nur Localhost lauscht::

       $ netstat -tuln | grep 8080

   Falls ``127.0.0.1:8080``, ändern Sie die Konfiguration, um auf ``0.0.0.0:8080`` oder einer bestimmten IP-Adresse zu lauschen.

Leistungsprobleme
=================

Suche ist langsam
-----------------

**Ursache:**

- Index ist groß
- Speichermangel
- Langsames Festplatten-I/O
- Komplexe Query

**Lösung:**

1. **Heap-Größe erhöhen**

   Bearbeiten Sie ``fess.in.sh``::

       FESS_HEAP_SIZE=4g

   Passen Sie auch die OpenSearch-Heap-Größe an::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **Index optimieren**

   Führen Sie regelmäßig Optimierung über die Verwaltungsseite unter „System" → „Scheduler" aus.

3. **SSD verwenden**

   Bei Festplatten-I/O als Engpass wechseln Sie zu SSD.

4. **Cache aktivieren**

   Aktivieren Sie Query-Cache in der Konfigurationsdatei.

Crawling ist langsam
--------------------

**Ursache:**

- Langes Crawl-Intervall
- Langsame Antwort der Ziel-Site
- Geringe Anzahl an Threads

**Lösung:**

1. **Crawl-Intervall anpassen**

   Verkürzen Sie das „Intervall" in der Crawl-Konfiguration der Verwaltungsseite (in Millisekunden).

   .. warning::

      Ein zu kurzes Intervall belastet die Ziel-Site. Setzen Sie einen angemessenen Wert.

2. **Thread-Anzahl erhöhen**

   Erhöhen Sie die Anzahl der Crawl-Threads in der Konfigurationsdatei::

       crawler.thread.count=10

3. **Timeout-Wert anpassen**

   Bei langsam antwortenden Sites erhöhen Sie den Timeout-Wert.

Datenprobleme
=============

Keine Suchergebnisse angezeigt
-------------------------------

**Ursache:**

- Index nicht erstellt
- Crawling fehlgeschlagen
- Falsche Such-Query

**Lösung:**

1. **Index überprüfen**::

       $ curl http://localhost:9200/_cat/indices?v

   Überprüfen Sie, ob |Fess|-Indizes vorhanden sind.

2. **Crawl-Protokoll überprüfen**

   Überprüfen Sie in der Verwaltungsseite unter „System" → „Protokoll" das Crawl-Protokoll auf Fehler.

3. **Crawl erneut ausführen**

   Führen Sie in der Verwaltungsseite unter „System" → „Scheduler" den „Default Crawler" aus.

4. **Such-Query vereinfachen**

   Suchen Sie zunächst mit einem einfachen Stichwort und überprüfen Sie, ob Ergebnisse zurückgegeben werden.

Index ist beschädigt
--------------------

**Symptom:**

Bei der Suche treten Fehler auf oder es werden unerwartete Ergebnisse zurückgegeben.

**Lösung:**

1. **Index löschen und neu erstellen**

   .. warning::

      Beim Löschen des Index gehen alle Suchdaten verloren. Erstellen Sie unbedingt ein Backup.

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **Crawl erneut ausführen**

   Führen Sie über die Verwaltungsseite „Default Crawler" aus, um den Index neu zu erstellen.

Docker-spezifische Probleme
===========================

Container startet nicht
-----------------------

**Symptom:**

Container startet nicht mit ``docker compose up``.

**Lösung:**

1. **Protokolle überprüfen**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **Speichermangel überprüfen**

   Erhöhen Sie den Docker zugewiesenen Speicher (über Docker Desktop-Einstellungen).

3. **Port-Konflikte überprüfen**::

       $ docker ps

   Überprüfen Sie, ob andere Container Port 8080 oder 9200 verwenden.

4. **Docker Compose-Datei überprüfen**

   Überprüfen Sie auf Syntaxfehler in der YAML-Datei::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

Container läuft, aber kein Zugriff auf Fess möglich
----------------------------------------------------

**Lösung:**

1. **Container-Status überprüfen**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **Protokolle überprüfen**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **Netzwerkkonfiguration überprüfen**::

       $ docker network ls
       $ docker network inspect <network_name>

Windows-spezifische Probleme
=============================

Pfadprobleme
------------

**Symptom:**

Bei Pfaden mit Leerzeichen oder japanischen Zeichen treten Fehler auf.

**Lösung:**

Installieren Sie in einem Verzeichnis ohne Leerzeichen oder japanische Zeichen im Pfad.

Beispiel::

    C:\opensearch  (empfohlen)
    C:\Program Files\opensearch  (nicht empfohlen)

Registrierung als Dienst nicht möglich
---------------------------------------

**Lösung:**

Verwenden Sie ein Drittanbieter-Tool wie NSSM zur Registrierung als Windows-Dienst.

Details finden Sie unter :doc:`install-windows`.

Sonstige Probleme
=================

Änderung des Protokollniveaus
------------------------------

Ändern Sie das Protokollniveau auf DEBUG, um detaillierte Protokolle zu überprüfen.

Bearbeiten Sie ``log4j2.xml``::

    <Logger name="org.codelibs.fess" level="debug"/>

Datenbank zurücksetzen
-----------------------

Löschen Sie OpenSearch-Indizes, um die Konfiguration zurückzusetzen::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   Dieser Befehl löscht alle Konfigurationsdaten.

Support-Informationen
=====================

Falls das Problem nicht gelöst werden kann, nutzen Sie folgende Support-Ressourcen:

Community-Support
-----------------

- **Issues**: https://github.com/codelibs/fess/issues

  Fügen Sie beim Melden von Problemen folgende Informationen hinzu:

  - Fess-Version
  - OpenSearch-Version
  - OS und Version
  - Fehlermeldungen (aus Protokollen)
  - Reproduktionsschritte

- **Forum**: https://discuss.codelibs.org/

Kommerzieller Support
---------------------

Bei Bedarf an kommerziellem Support wenden Sie sich bitte an N2SM, Inc.:

- **Website**: https://www.n2sm.net/

Sammlung von Debug-Informationen
=================================

Beim Melden von Problemen ist das Sammeln folgender Informationen hilfreich:

1. **Versionsinformationen**::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **Systeminformationen**::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **Protokolldateien**::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **Konfigurationsdateien** (nach Entfernung vertraulicher Informationen)::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **OpenSearch-Status**::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
