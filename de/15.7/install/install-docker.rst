=====================================
Installation mit Docker (Detailliert)
=====================================

Diese Seite beschreibt die Installationsschritte von |Fess| mit Docker und Docker Compose.
Mit Docker können Sie schnell und einfach eine |Fess|-Umgebung einrichten.

Voraussetzungen
================

- Die in :doc:`prerequisites` beschriebenen Systemanforderungen sind erfüllt
- Docker 20.10 oder höher ist installiert
- Docker Compose 2.0 oder höher ist installiert

Überprüfung der Docker-Installation
====================================

Überprüfen Sie die Version von Docker und Docker Compose mit folgenden Befehlen.

::

    $ docker --version
    $ docker compose version

.. note::

   Bei Verwendung einer älteren Version von Docker Compose verwenden Sie den Befehl ``docker-compose``.
   Diese Dokumentation verwendet das neue ``docker compose``-Befehlsformat.

Über Docker-Images
===================

Wenn Sie |Fess| mit Docker Compose starten, laufen die folgenden zwei Container:

- **Fess** (``fess01``): das Volltext-Suchsystem selbst
- **OpenSearch** (``search01``): die Suchmaschine

Das offizielle Docker-Image wird auf der `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__ veröffentlicht.
Die Compose-Dateien und die Startanleitung werden im Repository `docker-fess <https://github.com/codelibs/docker-fess>`__ verwaltet.

Schritt 1: Abrufen der Docker Compose-Dateien
==============================================

Für den Start mit Docker Compose werden folgende Dateien benötigt.

Methode 1: Dateien einzeln herunterladen
-----------------------------------------

Laden Sie folgende Dateien herunter:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose-opensearch3.yaml

Methode 2: Repository mit Git klonen
-------------------------------------

Wenn Git installiert ist, können Sie auch das gesamte Repository klonen:

::

    $ git clone --depth 1 --branch v15.7.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Schritt 2: Überprüfung der Docker Compose-Dateien
==================================================

Inhalt von ``compose.yaml``
----------------------------

``compose.yaml`` enthält die Konfiguration von Fess selbst (dem ``fess01``-Dienst).

Hauptkonfigurationspunkte:

- **Portnummer**: Port der Fess-Weboberfläche (Standard: 8080)
- **Umgebungsvariablen**: z. B. das OpenSearch-Verbindungsziel (``SEARCH_ENGINE_HTTP_URL``) oder der Pfad der Wörterbuchdateien (``FESS_DICTIONARY_PATH``)
- **Startreihenfolge**: Über ``depends_on`` ist konfiguriert, dass der Start erst erfolgt, nachdem OpenSearch (``search01``) einen normalen Zustand erreicht hat

Inhalt von ``compose-opensearch3.yaml``
----------------------------------------

``compose-opensearch3.yaml`` enthält die Konfiguration der Suchmaschine (dem ``search01``-Dienst, OpenSearch).

Hauptkonfigurationspunkte:

- **OpenSearch-Image**: das verwendete OpenSearch-Image (``ghcr.io/codelibs/fess-opensearch``)
- **Speichereinstellungen**: JVM-Heap-Größe
- **Volumes**: Volumes zur Datenpersistenz (``search01_data``: Indexdaten, ``search01_dictionary``: Wörterbuchdateien)

Anpassung der Konfiguration (Optional)
-----------------------------------------

Wenn Sie die Standardkonfiguration ändern möchten, bearbeiten Sie ``compose.yaml``.

Beispiel: Änderung der Portnummer::

    services:
      fess01:
        ports:
          - "9080:8080"  # Zuordnung zu Port 9080 auf dem Host

Beispiel: Änderung der Speichereinstellungen::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Fess-Heap-Größe auf 2 GB setzen

Schritt 3: Starten der Docker-Container
========================================

Grundlegender Start
--------------------

Starten Sie Fess und OpenSearch mit folgendem Befehl:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - Mit der Option ``-f`` werden mehrere Compose-Dateien angegeben
   - Mit der Option ``-d`` wird im Hintergrund ausgeführt

Überprüfung der Startprotokolle::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

Drücken Sie ``Ctrl+C``, um die Protokollanzeige zu beenden.

Überprüfung des Starts
------------------------

Überprüfen Sie den Status der Container::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Vergewissern Sie sich, dass folgende Container gestartet sind:

- ``fess01``
- ``search01``

.. tip::

   Der Start kann einige Minuten dauern. Zuerst erreicht OpenSearch (``search01``) einen normalen Zustand, danach startet Fess (``fess01``).
   Überprüfen Sie mit ``docker compose ... ps`` den Status der einzelnen Container; sobald ``fess01`` gestartet ist, können Sie im Browser auf http://localhost:8080/ zugreifen.

Schritt 4: Zugriff über den Browser
====================================

Nach Abschluss des Starts greifen Sie auf folgende URL zu:

- **Suchseite**: http://localhost:8080/
- **Verwaltungsseite**: http://localhost:8080/admin

Standard-Administratorkonto:

- Benutzername: ``admin``
- Passwort: ``admin``

.. warning::

   **Wichtiger Sicherheitshinweis**

   In Produktionsumgebungen ändern Sie bitte unbedingt das Administratorpasswort.
   Weitere Informationen finden Sie unter :doc:`security`.

Aktivierung des AI-Suchmodus (LLM-Plugins)
============================================

Seit |Fess| 15.7 wurde die Funktion des AI-Suchmodus (RAG Chat) als ``fess-llm-*``-Plugins ausgelagert.
Das offizielle Repository `docker-fess <https://github.com/codelibs/docker-fess>`__ enthält Overlay-Dateien für die wichtigsten LLM-Anbieter.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Overlay
     - Verwendung
   * - ``compose-ollama.yaml``
     - Ollama (lokales LLM, startet zusätzlichen ``ollama01``-Dienst)
   * - ``compose-gemini.yaml``
     - Google Gemini (Cloud-API)
   * - ``compose-openai.yaml``
     - OpenAI (Cloud-API)

Jedes Overlay lädt automatisch das entsprechende Plugin über ``FESS_PLUGINS`` und aktiviert RAG Chat, indem es
``-Dfess.config.rag.chat.enabled=true`` in ``FESS_JAVA_OPTS`` setzt.
Bei Gemini und OpenAI, die Cloud-APIs verwenden, wird zusätzlich über ``-Dfess.system.rag.llm.name`` der verwendete Anbieter angegeben,
und es werden der API-Schlüssel (``rag.llm.<provider>.api.key``) sowie das Modell (``rag.llm.<provider>.model``) konfiguriert.
Bei Ollama wird der Standardwert von ``rag.llm.name`` (``ollama``) unverändert verwendet, sodass keine explizite Angabe erforderlich ist,
und es wird lediglich das Verbindungsziel (``rag.llm.ollama.api.url``) konfiguriert.

Beispiel für die Verwendung von Gemini::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Beispiel für die Verwendung von OpenAI::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   Das verwendete Modell kann über die Umgebungsvariablen ``GEMINI_MODEL`` und ``OPENAI_MODEL`` geändert werden
   (die Standardwerte sind ``gemini-2.5-flash`` bzw. ``gpt-5-mini``).

Beispiel für die Verwendung von Ollama::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   Der ``ollama01``-Dienst in ``compose-ollama.yaml`` ist standardmäßig so definiert, dass er eine NVIDIA-GPU verwendet
   (dafür ist das `NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__ erforderlich).
   Wenn Sie in einer Umgebung ohne GPU ausführen, entfernen oder kommentieren Sie den ``deploy:``-Block (die GPU-Angabe unter ``reservations``) in ``compose-ollama.yaml``.

.. tip::

   Nach dem Start können Sie im Verwaltungsbildschirm unter „System > Allgemein" den verwendeten LLM-Anbieter (``rag.llm.name``)
   und anbieterspezifische Einstellungen ändern. Diese Änderungen werden jedoch in einer Konfigurationsdatei innerhalb des Containers gespeichert
   und gehen daher verloren, wenn der Container neu erstellt wird (``docker compose down`` gefolgt von ``up``).
   Um die Einstellungen dauerhaft zu speichern, geben Sie sie wie in den obigen Beispielen über ``FESS_JAVA_OPTS`` in der Compose-Datei an.

Datenpersistenz
================

Alle Daten von |Fess| (Index, gecrawlte Dokumente, Benutzerinformationen, Einstellungen usw.) werden in OpenSearch gespeichert.
Da diese Daten in den Volumes von OpenSearch persistiert werden, bleiben sie auch nach dem Löschen der Container erhalten.
Der Container von Fess selbst (``fess01``) ist zustandslos und besitzt kein eigenes Volume.

Überprüfung der Volumes::

    $ docker volume ls

Die in ``compose-opensearch3.yaml`` definierten Hauptvolumes:

- ``search01_data``: Indexdaten von OpenSearch (enthält alle Daten von Fess)
- ``search01_dictionary``: Wörterbuchdateien

.. note::

   Dem Volume-Namen von Docker Compose wird der Projektname (standardmäßig der Name des Verzeichnisses, in dem sich die Compose-Datei befindet) als Präfix vorangestellt.
   Wenn Sie beispielsweise im Verzeichnis ``compose`` starten, lautet der tatsächliche Volume-Name z. B. ``compose_search01_data``.

.. important::

   Beim Löschen der Container werden die Volumes nicht gelöscht.
   Um Volumes zu löschen, muss explizit der Befehl ``docker volume rm`` ausgeführt werden.

Stoppen der Docker-Container
=============================

Container stoppen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Container stoppen und löschen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Der Befehl ``down`` löscht die Container, aber nicht die Volumes.
   Wenn Sie auch die Volumes (z. B. ``search01_data``) löschen möchten, fügen Sie die Option ``-v`` hinzu::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Achtung**: Wenn Sie diesen Befehl ausführen, werden alle in OpenSearch gespeicherten Daten gelöscht.

Erweiterte Konfiguration
==========================

Anpassung der Umgebungsvariablen
-----------------------------------

Durch Hinzufügen oder Ändern von Umgebungsvariablen in ``compose.yaml`` sind detaillierte Konfigurationen möglich.

Hauptumgebungsvariablen:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Umgebungsvariable
     - Beschreibung
   * - ``FESS_HEAP_SIZE``
     - Fess-JVM-Heap-Größe (Standardwert des Docker-Images: 512m)
   * - ``FESS_JAVA_OPTS``
     - Angabe zusätzlicher JVM-Optionen (z. B. Überschreiben von Einstellungen mittels ``-Dfess.config.*``)
   * - ``FESS_PLUGINS``
     - Beim Start automatisch zu installierende Plugins (durch Leerzeichen getrenntes Format ``name:version``. Beispiel: ``fess-ds-wikipedia:15.7.0``)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - HTTP-Endpunkt von OpenSearch (Standardwert in ``compose.yaml``: ``http://search01:9200``)
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - Anmeldedaten für die Verbindung zu einem OpenSearch mit aktivierter Authentifizierung
   * - ``FESS_DICTIONARY_PATH``
     - Pfad der Wörterbuchdateien (mit OpenSearch gemeinsam genutztes Verzeichnis)
   * - ``FESS_PORT``
     - Port, auf dem Fess innerhalb des Containers lauscht (Standardwert: 8080)

Beispiel::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   Wenn Sie die Zeitzone ändern möchten, geben Sie in ``FESS_JAVA_OPTS`` beispielsweise ``-Duser.timezone=Asia/Tokyo`` an.

Anwendung von Konfigurationsdateien
--------------------------------------

Detaillierte Einstellungen von |Fess| werden in der Datei ``fess_config.properties`` beschrieben.
Im Docker-Image befindet sich ``fess_config.properties`` unter ``/etc/fess`` im Container.
Um die Einstellungen in der Docker-Umgebung zu übernehmen, gibt es folgende Methoden.

Methode 1: Konfigurationsdatei mounten
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/etc/fess`` enthält auch andere Konfigurationsdateien, die für den Betrieb von Fess erforderlich sind. Wenn Sie dieses Verzeichnis direkt durch ein Mount ersetzen, schlägt der Start fehl.
Verwenden Sie stattdessen das Override-Verzeichnis ``/opt/fess``, das an den Anfang des Klassenpfads angehängt wird (im Ausgangszustand ist es leer).

1. Erstellen Sie auf der Host-Seite ein Verzeichnis zur Bereitstellung der Konfigurationsdatei::

       $ mkdir -p /path/to/fess-config

2. Holen Sie die Vorlage der Konfigurationsdatei (nur beim ersten Mal)::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.7.0/src/main/resources/fess_config.properties

3. Bearbeiten Sie ``/path/to/fess-config/fess_config.properties`` und tragen Sie die erforderlichen Einstellungen ein::

       # Beispiel
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. Fügen Sie im ``fess01``-Dienst von ``compose.yaml`` einen Volume-Mount hinzu::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. Starten Sie den Container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Da ``/opt/fess`` an den Anfang des Klassenpfads angehängt wird, hat die hier abgelegte ``fess_config.properties``
   Vorrang vor der im Image enthaltenen ``/etc/fess/fess_config.properties``.
   Property-Dateien werden dateiweise geladen und nicht Eintrag für Eintrag zusammengeführt.
   Daher müssen Sie nicht nur die zu überschreibenden Einträge, sondern eine **vollständige Datei mit allen Konfigurationseinträgen** bereitstellen.
   Wenn Sie nur einzelne Einträge ändern möchten, verwenden Sie die im Folgenden beschriebene „Methode 2".

Methode 2: Konfiguration über Systemeigenschaften
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sie können die Konfigurationseinträge von ``fess_config.properties`` über Umgebungsvariablen als Systemeigenschaften überschreiben.

Konfigurationseinträge, die in ``fess_config.properties`` stehen (z. B. ``crawler.document.cache.enabled=false``),
geben Sie im Format ``-Dfess.config.Einstellungsname=Wert`` an.

Fügen Sie den Umgebungsvariablen des ``fess01``-Dienstes in ``compose.yaml`` ``FESS_JAVA_OPTS`` hinzu::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   Der Teil nach ``-Dfess.config.`` entspricht dem Namen des Konfigurationseintrags in ``fess_config.properties``.
   Wenn Sie nur einzelne Einträge überschreiben möchten, ist diese Methode einfacher.

Verbindung zu externem OpenSearch
------------------------------------

Wenn Sie einen bestehenden OpenSearch-Cluster verwenden möchten, starten Sie nur mit ``compose.yaml`` ohne ``compose-opensearch3.yaml`` und ändern das Verbindungsziel.

1. Starten Sie, ohne ``compose-opensearch3.yaml`` anzugeben::

       $ docker compose -f compose.yaml up -d

2. Legen Sie im ``fess01``-Dienst von ``compose.yaml`` das Verbindungsziel fest::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   Wenn Sie sich mit einem OpenSearch mit aktivierter Authentifizierung verbinden, geben Sie zusätzlich ``SEARCH_ENGINE_USERNAME`` und ``SEARCH_ENGINE_PASSWORD`` an.

Weitere Overlays und Konfigurationen
----------------------------------------

Das ``docker-fess``-Repository enthält neben den oben genannten weitere Compose-Dateien und Verzeichnisse für unterschiedliche Einsatzzwecke.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Datei / Verzeichnis
     - Verwendung
   * - ``compose-dashboards3.yaml``
     - Fügt OpenSearch Dashboards hinzu (Port 5601, für die Datenvisualisierung)
   * - ``compose-minio.yaml``
     - Fügt MinIO (Objektspeicher) hinzu und verwendet es als Speicherziel für die Speicherfunktion von Fess
   * - ``vanilla/``
     - Konfiguration mit einem reinen OpenSearch ohne Fess-Plugins (einige Funktionen wie die Wörterbuchverwaltung stehen nicht zur Verfügung)
   * - ``snapshot/``
     - Konfiguration mit Entwicklungs-(Snapshot-)Images (einschließlich Cluster-Konfigurationen und der Kombination mit Elasticsearch 8)
   * - ``multi-instance/``
     - Konfiguration zum Starten mehrerer Fess-Instanzen, die sich ein einzelnes OpenSearch teilen

Konfiguration des Docker-Netzwerks
--------------------------------------

Bei der Integration mit mehreren Diensten können Sie ein benutzerdefiniertes Netzwerk verwenden.

Beispiel::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
        networks:
          - fess-network

Produktionsbetrieb mit Docker Compose
=======================================

Empfohlene Einstellungen bei Verwendung von Docker Compose in Produktionsumgebungen:

1. **Festlegen von Ressourcenbeschränkungen**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **Festlegen der Neustartrichtlinie**::

       restart: unless-stopped

3. **Protokollkonfiguration**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **Aktivierung der Sicherheitseinstellungen**

   Aktivieren Sie das Sicherheits-Plugin von OpenSearch und konfigurieren Sie eine geeignete Authentifizierung.
   Weitere Informationen finden Sie unter :doc:`security`.

Fehlerbehebung
================

Container startet nicht
--------------------------

1. Überprüfen Sie die Protokolle::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. Überprüfen Sie Portnummer-Konflikte::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. Überprüfen Sie den Festplattenspeicherplatz::

       $ df -h

Speicher-Fehler
------------------

Wenn OpenSearch aufgrund von Speichermangel nicht startet, muss ``vm.max_map_count`` erhöht werden.

Unter Linux::

    $ sudo sysctl -w vm.max_map_count=262144

Für eine dauerhafte Einstellung::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Dateninitialisierung
-----------------------

Alle Daten löschen und in den Ausgangszustand zurücksetzen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   Wenn Sie diesen Befehl ausführen, werden alle Daten vollständig gelöscht.

Nächste Schritte
==================

Nach Abschluss der Installation lesen Sie bitte die folgende Dokumentation:

- :doc:`run` - Start und Ersteinrichtung von |Fess|
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Fehlerbehebung

Häufig gestellte Fragen
==========================

F: Wie viel Speicherplatz wird für den Download der Images benötigt?
------------------------------------------------------------------------

A: Die Images von Fess und OpenSearch werden beim ersten Start heruntergeladen und benötigen zusammen einige GB an Speicherplatz.
Je nach Netzwerkumgebung kann der Download einige Zeit in Anspruch nehmen.

F: Ist ein Betrieb unter Kubernetes möglich?
-----------------------------------------------

A: Ja, das ist möglich. Sie können die Docker Compose-Dateien mit Tools wie ``kompose`` in Kubernetes-Manifeste konvertieren
oder eigene Manifeste erstellen und damit betreiben (ein offizielles Helm-Chart wird nicht bereitgestellt).

F: Wie aktualisiert man die Container?
------------------------------------------

A: Aktualisieren Sie mit folgenden Schritten:

1. Besorgen Sie die neuesten Compose-Dateien
2. Stoppen Sie die Container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Holen Sie neue Images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Starten Sie die Container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

F: Ist eine Multi-Node-Konfiguration möglich?
-------------------------------------------------

A: Ja, das ist möglich. Anhand von ``snapshot/compose-cluster.yaml`` im ``docker-fess``-Repository können Sie OpenSearch mit mehreren Knoten konfigurieren,
oder anhand von ``multi-instance/`` mehrere Fess-Instanzen konfigurieren, die sich ein einzelnes OpenSearch teilen.
Für Produktionsumgebungen wird jedoch die Verwendung von Orchestrierungs-Tools wie Kubernetes empfohlen.
