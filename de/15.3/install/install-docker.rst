==============================
Installation mit Docker (Detailliert)
==============================

Diese Seite beschreibt die Installationsschritte von |Fess| mit Docker und Docker Compose.
Mit Docker können Sie schnell und einfach eine |Fess|-Umgebung einrichten.

Voraussetzungen
===============

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

Das Docker-Image von |Fess| besteht aus folgenden Komponenten:

- **Fess**: Volltext-Suchsystem
- **OpenSearch**: Suchmaschine

Das offizielle Docker-Image wird auf `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__ veröffentlicht.

Schritt 1: Herunterladen der Docker Compose-Dateien
====================================================

Für den Start mit Docker Compose werden folgende Dateien benötigt.

Methode 1: Einzeln Dateien herunterladen
-----------------------------------------

Laden Sie folgende Dateien herunter:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.0/compose/compose-opensearch3.yaml

Methode 2: Repository mit Git klonen
-------------------------------------

Wenn Git installiert ist, können Sie auch das gesamte Repository klonen:

::

    $ git clone --depth 1 --branch v15.3.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Schritt 2: Überprüfung der Docker Compose-Dateien
==================================================

Inhalt von ``compose.yaml``
----------------------------

``compose.yaml`` enthält die grundlegende Konfiguration von Fess.

Hauptkonfigurationspunkte:

- **Portnummer**: Port der Fess-Weboberfläche (Standard: 8080)
- **Umgebungsvariablen**: Einstellungen wie Java-Heap-Größe
- **Volumes**: Einstellungen für Datenpersistenz

Inhalt von ``compose-opensearch3.yaml``
----------------------------------------

``compose-opensearch3.yaml`` enthält die OpenSearch-Konfiguration.

Hauptkonfigurationspunkte:

- **OpenSearch-Version**: Verwendete OpenSearch-Version
- **Speichereinstellungen**: JVM-Heap-Größe
- **Volumes**: Einstellungen für Indexdaten-Persistenz

Anpassung der Konfiguration (Optional)
---------------------------------------

Wenn Sie die Standardkonfiguration ändern möchten, bearbeiten Sie ``compose.yaml``.

Beispiel: Änderung der Portnummer::

    services:
      fess:
        ports:
          - "9080:8080"  # Zuordnung zu Port 9080 des Hosts

Beispiel: Änderung der Speichereinstellungen::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Fess-Heap-Größe auf 2 GB setzen

Schritt 3: Starten der Docker-Container
========================================

Grundlegender Start
-------------------

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
----------------------

Überprüfen Sie den Status der Container::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Vergewissern Sie sich, dass folgende Container laufen:

- ``fess``
- ``opensearch``

.. tip::

   Der Start kann einige Minuten dauern.
   Warten Sie, bis im Protokoll „Fess is ready" oder eine ähnliche Meldung erscheint.

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

Datenpersistenz
===============

Volumes werden automatisch erstellt, um Daten auch nach dem Löschen der Docker-Container zu erhalten.

Überprüfung der Volumes::

    $ docker volume ls

|Fess|-bezogene Volumes:

- ``fess-es-data``: OpenSearch-Indexdaten
- ``fess-data``: Fess-Konfigurationsdaten

.. important::

   Volumes werden beim Löschen der Container nicht gelöscht.
   Um Volumes zu löschen, muss explizit der Befehl ``docker volume rm`` ausgeführt werden.

Stoppen der Docker-Container
=============================

Container stoppen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Container stoppen und löschen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Der Befehl ``down`` löscht Container, aber keine Volumes.
   Um auch Volumes zu löschen, fügen Sie die Option ``-v`` hinzu::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Achtung**: Dieser Befehl löscht alle Daten.

Erweiterte Konfiguration
========================

Anpassung der Umgebungsvariablen
---------------------------------

Durch Hinzufügen oder Ändern von Umgebungsvariablen in ``compose.yaml`` sind detaillierte Konfigurationen möglich.

Hauptumgebungsvariablen:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Umgebungsvariable
     - Beschreibung
   * - ``FESS_HEAP_SIZE``
     - Fess JVM-Heap-Größe (Standard: 1g)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch HTTP-Endpunkt
   * - ``TZ``
     - Zeitzone (z.B.: Asia/Tokyo)

Beispiel::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Europe/Berlin"

Verbindung zu externem OpenSearch
----------------------------------

Bei Verwendung eines bestehenden OpenSearch-Clusters bearbeiten Sie ``compose.yaml`` und ändern Sie das Verbindungsziel.

1. Verwenden Sie ``compose-opensearch3.yaml`` nicht::

       $ docker compose -f compose.yaml up -d

2. Setzen Sie ``SEARCH_ENGINE_HTTP_URL``::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Konfiguration des Docker-Netzwerks
-----------------------------------

Bei Integration mit mehreren Diensten können Sie ein benutzerdefiniertes Netzwerk verwenden.

Beispiel::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
        networks:
          - fess-network

Produktionsbetrieb mit Docker Compose
======================================

Empfohlene Einstellungen bei Verwendung von Docker Compose in Produktionsumgebungen:

1. **Ressourcenbeschränkungen**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **Neustartrichtlinie**::

       restart: unless-stopped

3. **Protokollkonfiguration**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **Aktivierung der Sicherheitseinstellungen**

   Aktivieren Sie das Sicherheits-Plugin von OpenSearch und konfigurieren Sie entsprechende Authentifizierung.
   Weitere Informationen finden Sie unter :doc:`security`.

Fehlerbehebung
==============

Container startet nicht
-----------------------

1. Überprüfen Sie die Protokolle::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. Überprüfen Sie Portnummer-Konflikte::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. Überprüfen Sie die Festplattenkapazität::

       $ df -h

Speicher-Fehler
---------------

Wenn OpenSearch aufgrund von Speichermangel nicht startet, muss ``vm.max_map_count`` erhöht werden.

Unter Linux::

    $ sudo sysctl -w vm.max_map_count=262144

Für dauerhafte Einstellung::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Dateninitialisierung
--------------------

Alle Daten löschen und in den Ausgangszustand zurücksetzen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   Dieser Befehl löscht alle Daten vollständig.

Nächste Schritte
================

Nach Abschluss der Installation lesen Sie bitte folgende Dokumentation:

- :doc:`run` - Start und Ersteinrichtung von |Fess|
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Fehlerbehebung

Häufig gestellte Fragen
=======================

F: Wie groß sind die Docker-Images?
------------------------------------

A: Das Fess-Image ist ca. 1 GB, das OpenSearch-Image ca. 800 MB.
Beim ersten Start kann der Download einige Zeit dauern.

F: Ist Betrieb auf Kubernetes möglich?
---------------------------------------

A: Ja, möglich. Durch Konvertierung der Docker Compose-Dateien in Kubernetes-Manifeste
oder durch Verwendung von Helm Charts ist Betrieb auf Kubernetes möglich.
Weitere Informationen finden Sie in der offiziellen Fess-Dokumentation.

F: Wie aktualisiert man Container?
-----------------------------------

A: Aktualisieren Sie mit folgenden Schritten:

1. Besorgen Sie die neuesten Compose-Dateien
2. Stoppen Sie die Container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Holen Sie neue Images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Starten Sie die Container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

F: Ist Multi-Node-Konfiguration möglich?
-----------------------------------------

A: Ja, möglich. Durch Bearbeiten von ``compose-opensearch3.yaml`` und Definition mehrerer OpenSearch-Knoten
kann eine Cluster-Konfiguration erstellt werden. Für Produktionsumgebungen wird jedoch die Verwendung von Orchestrierungs-Tools wie Kubernetes empfohlen.
