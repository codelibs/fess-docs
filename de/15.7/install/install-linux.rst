======================================================
Installation unter Linux (Detaillierte Anleitung)
======================================================

Diese Seite beschreibt die Installationsschritte von |Fess| in Linux-Umgebungen.
Sie behandelt die Paketformate TAR.GZ, RPM und DEB.

.. warning::

   In Produktionsumgebungen wird der Betrieb mit eingebettetem OpenSearch nicht empfohlen.
   Bitte richten Sie unbedingt einen externen OpenSearch-Server ein.

Voraussetzungen
====================

- Die in :doc:`prerequisites` beschriebenen Systemanforderungen sind erfüllt
- Java 21 ist installiert
- OpenSearch 3.7.0 ist verfügbar (oder wird neu installiert)

Auswahl der Installationsmethode
=====================================

In Linux-Umgebungen können Sie aus folgenden Installationsmethoden wählen:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Methode
     - Empfohlene Umgebung
     - Merkmale
   * - TAR.GZ
     - Entwicklungsumgebung, Umgebungen mit Anpassungsbedarf
     - Kann in beliebiges Verzeichnis entpackt werden
   * - RPM
     - RHEL, CentOS, Fedora-Systeme
     - Dienstverwaltung mit systemd möglich
   * - DEB
     - Debian, Ubuntu-Systeme
     - Dienstverwaltung mit systemd möglich

Systemkonfiguration für den Betrieb von OpenSearch
=======================================================

Um OpenSearch unter Linux stabil zu betreiben, müssen die folgenden Kernel-Parameter und Ressourcenbegrenzungen konfiguriert werden.
Diese sind hauptsächlich für die TAR.GZ-Version erforderlich (wenn OpenSearch manuell installiert wird).
Bei den RPM-/DEB-Versionen legen die Pakete von OpenSearch und |Fess| die Anzahl der Dateideskriptoren usw. über systemd fest, aber da ``vm.max_map_count`` eine Kernel-Einstellung auf Host-Ebene ist, sollten Sie diese unabhängig von der gewählten Methode überprüfen.

Maximale Anzahl virtueller Speicher-Mappings
-------------------------------------------------

Da OpenSearch eine große Anzahl an Speicher-Mappings verwendet, setzen Sie ``vm.max_map_count`` auf mindestens ``262144``.

Für eine temporäre Einstellung::

    $ sudo sysctl -w vm.max_map_count=262144

Für eine dauerhafte Einstellung::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Anzahl der Dateideskriptoren
---------------------------------

Wenn Sie OpenSearch manuell ausführen (TAR.GZ-Version), setzen Sie das Limit für die Anzahl der Dateideskriptoren des Benutzers, der OpenSearch ausführt, auf mindestens ``65535``.

Fügen Sie Folgendes zu ``/etc/security/limits.conf`` hinzu (ersetzen Sie ``opensearch`` durch den Benutzernamen, unter dem OpenSearch ausgeführt wird)::

    opensearch  -  nofile  65535

.. note::

   Bei den RPM-/DEB-Versionen wird das Limit für die Anzahl der Dateideskriptoren bereits in der systemd-Dienstdefinition festgelegt, sodass diese Einstellung nicht erforderlich ist.

Installation mit TAR.GZ-Version
====================================

Schritt 1: Installation von OpenSearch
-------------------------------------------

1. Download von OpenSearch

   Laden Sie die TAR.GZ-Version von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.tar.gz
       $ tar -xzf opensearch-3.7.0-linux-x64.tar.gz
       $ cd opensearch-3.7.0

   .. note::

      In diesem Beispiel wird OpenSearch 3.7.0 verwendet.
      |Fess| 15.7 unterstützt OpenSearch 3.7.0.

2. Installation der OpenSearch-Plugins

   Installieren Sie die von |Fess| benötigten Plugins.

   ::

       $ cd /path/to/opensearch-3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. important::

      Die Plugin-Version muss mit der OpenSearch-Version übereinstimmen.
      Im obigen Beispiel sind alle auf 3.7.0 gesetzt.

3. Konfiguration von OpenSearch

   Fügen Sie in ``config/opensearch.yml`` folgende Einstellungen hinzu.

   ::

       # Pfad für Konfigurationssynchronisation (als absoluter Pfad angeben)
       configsync.config_path: /path/to/opensearch-3.7.0/data/config/

       # Deaktivierung des Sicherheits-Plugins (nur Entwicklungsumgebung)
       plugins.security.disabled: true

   .. warning::

      **Wichtiger Sicherheitshinweis**

      ``plugins.security.disabled: true`` sollte nur in Entwicklungs- oder Testumgebungen verwendet werden.
      In Produktionsumgebungen aktivieren Sie bitte das Sicherheits-Plugin von OpenSearch und konfigurieren Sie entsprechende Authentifizierungs- und Autorisierungseinstellungen.
      Wenn Sie das Sicherheits-Plugin unter OpenSearch 2.12 oder höher aktivieren, muss beim ersten Start ein Administratorkennwort (Umgebungsvariable ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``) festgelegt werden.
      Weitere Informationen finden Sie unter :doc:`security`.

   .. tip::

      Passen Sie andere Einstellungen wie Clustername und Netzwerkeinstellungen entsprechend Ihrer Umgebung an.
      Konfigurationsbeispiel::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

   .. tip::

      Die Heap-Größe von OpenSearch wird über ``-Xms`` / ``-Xmx`` in ``config/jvm.options`` konfiguriert.
      Es wird empfohlen, für ``-Xms`` und ``-Xmx`` denselben Wert anzugeben, der höchstens die Hälfte des verfügbaren physischen Arbeitsspeichers beträgt und unter 32 GB liegt.

Schritt 2: Installation von Fess
-------------------------------------

1. Download und Entpacken von Fess

   Laden Sie die TAR.GZ-Version von der `Download-Site <https://fess.codelibs.org/de/downloads.html>`__ herunter.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.tar.gz
       $ tar -xzf fess-15.7.0.tar.gz
       $ cd fess-15.7.0

2. Konfiguration von Fess

   Bearbeiten Sie ``bin/fess.in.sh`` und konfigurieren Sie die Verbindungsinformationen zu OpenSearch.
   Diese Datei enthält bereits vorbereitete, aber auskommentierte Einstellungen für die Verbindung zu einem externen OpenSearch-Cluster.

   ::

       $ vi bin/fess.in.sh

   Entfernen Sie die Kommentierung (das führende ``#``) der folgenden zwei Zeilen in der Nähe des Dateianfangs.

   Vor der Änderung (Standardzustand)::

       # External opensearch cluster
       #SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       #FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   Nach der Änderung::

       # External opensearch cluster
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.7.0/data/config/

   .. note::

      - Setzen Sie für ``FESS_DICTIONARY_PATH`` denselben Pfad wie den in ``opensearch.yml`` von OpenSearch angegebenen ``configsync.config_path``.
      - Wenn OpenSearch auf einem anderen Host ausgeführt wird, ändern Sie ``SEARCH_ENGINE_HTTP_URL`` auf den entsprechenden Hostnamen oder die IP-Adresse. Beispiel: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``
      - Fügen Sie keine neue Zeile ``SEARCH_ENGINE_HTTP_URL=...`` hinzu, sondern entfernen Sie die Kommentierung der vorhandenen Zeile und bearbeiten Sie diese.

   .. tip::

      Um die Heap-Größe von |Fess| zu ändern, bearbeiten Sie ``FESS_MIN_MEM`` (Standard: ``256m``) und ``FESS_MAX_MEM`` (Standard: ``2g``) in ``bin/fess.in.sh``, oder setzen Sie die Umgebungsvariable ``FESS_HEAP_SIZE``.

3. Überprüfung der Installation

   Überprüfen Sie, ob die Konfigurationsdatei korrekt bearbeitet wurde::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Schritt 3: Start
---------------------

Die Startanleitung finden Sie unter :doc:`run`.

Installation mit RPM-Version
=================================

Die RPM-Version wird für RPM-basierte Linux-Distributionen wie Red Hat Enterprise Linux, CentOS und Fedora verwendet.

Schritt 1: Installation von OpenSearch
-------------------------------------------

1. Download und Installation des OpenSearch-RPM

   Laden Sie das RPM-Paket von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.7.0-linux-x64.rpm

   Alternativ können Sie auch ein Repository hinzufügen und die Installation durchführen.
   Details finden Sie unter `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Installation der OpenSearch-Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. Konfiguration von OpenSearch

   Fügen Sie in ``/etc/opensearch/opensearch.yml`` folgende Einstellungen hinzu.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Hinzuzufügende Einstellungen::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      Verwenden Sie ``plugins.security.disabled: true`` nicht in Produktionsumgebungen.
      Siehe :doc:`security` für entsprechende Sicherheitseinstellungen.

Schritt 2: Installation von Fess
-------------------------------------

1. Installation des Fess-RPM

   Laden Sie das RPM-Paket von der `Download-Site <https://fess.codelibs.org/de/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.rpm
       $ sudo rpm -ivh fess-15.7.0.rpm

2. Konfiguration von Fess

   Bei der RPM-Version bearbeiten Sie die Umgebungsvariablen-Konfigurationsdatei ``/etc/sysconfig/fess``.
   Diese Datei bleibt auch bei einem Paket-Upgrade erhalten (``/usr/share/fess/bin/fess.in.sh`` wird bei einem Upgrade überschrieben, bearbeiten Sie diese Datei daher nicht direkt).

   ::

       $ sudo vi /etc/sysconfig/fess

   Konfigurieren Sie die Verbindungsinformationen zu OpenSearch. Die Standardwerte sind wie folgt. Ändern Sie diese bei Bedarf::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Geben Sie für ``FESS_DICTIONARY_PATH`` denselben Pfad wie ``configsync.config_path`` in ``opensearch.yml`` an.

3. Dienstregistrierung und -aktivierung

   Aktivieren Sie den Dienst mit systemd (bei RHEL 8 oder höher und CentOS 8 oder höher ist systemd der Standard)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      Da der |Fess|-Dienst vom OpenSearch-Dienst abhängt, muss OpenSearch zuerst gestartet werden.

   .. note::

      In älteren Umgebungen ohne systemd können Sie |Fess| mit ``chkconfig`` registrieren::

          $ sudo /sbin/chkconfig --add fess

Schritt 3: Start
---------------------

Die Startanleitung finden Sie unter :doc:`run`.

Installation mit DEB-Version
=================================

Die DEB-Version wird für DEB-basierte Linux-Distributionen wie Debian und Ubuntu verwendet.

Schritt 1: Installation von OpenSearch
-------------------------------------------

1. Download und Installation des OpenSearch-DEB

   Laden Sie das DEB-Paket von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.deb
       $ sudo dpkg -i opensearch-3.7.0-linux-x64.deb

   Alternativ können Sie auch ein Repository hinzufügen und die Installation durchführen.
   Details finden Sie unter `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Installation der OpenSearch-Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. Konfiguration von OpenSearch

   Fügen Sie in ``/etc/opensearch/opensearch.yml`` folgende Einstellungen hinzu.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Hinzuzufügende Einstellungen::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      Verwenden Sie ``plugins.security.disabled: true`` nicht in Produktionsumgebungen.
      Siehe :doc:`security` für entsprechende Sicherheitseinstellungen.

Schritt 2: Installation von Fess
-------------------------------------

1. Installation des Fess-DEB

   Laden Sie das DEB-Paket von der `Download-Site <https://fess.codelibs.org/de/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.deb
       $ sudo dpkg -i fess-15.7.0.deb

2. Konfiguration von Fess

   Bei der DEB-Version bearbeiten Sie die Umgebungsvariablen-Konfigurationsdatei ``/etc/default/fess``.
   Diese Datei bleibt auch bei einem Paket-Upgrade erhalten (``/usr/share/fess/bin/fess.in.sh`` wird bei einem Upgrade überschrieben, bearbeiten Sie diese Datei daher nicht direkt).

   ::

       $ sudo vi /etc/default/fess

   Konfigurieren Sie die Verbindungsinformationen zu OpenSearch. Die Standardwerte sind wie folgt. Ändern Sie diese bei Bedarf::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Geben Sie für ``FESS_DICTIONARY_PATH`` denselben Pfad wie ``configsync.config_path`` in ``opensearch.yml`` an.

3. Dienstregistrierung und -aktivierung

   Aktivieren Sie den Dienst mit systemd::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      Da der |Fess|-Dienst vom OpenSearch-Dienst abhängt, muss OpenSearch zuerst gestartet werden.

Schritt 3: Start
---------------------

Die Startanleitung finden Sie unter :doc:`run`.

Überprüfung nach der Installation
======================================

Überprüfen Sie nach Abschluss der Installation Folgendes:

1. **Überprüfung der Konfigurationsdateien**

   - Konfigurationsdatei von OpenSearch (opensearch.yml)
   - Konfigurationsdatei von |Fess|

     - TAR.GZ-Version: ``bin/fess.in.sh``
     - RPM-Version: ``/etc/sysconfig/fess``
     - DEB-Version: ``/etc/default/fess``

2. **Verzeichnisberechtigungen**

   Überprüfen Sie, ob das in der Konfiguration angegebene Verzeichnis (``configsync.config_path`` / ``FESS_DICTIONARY_PATH``) existiert und die entsprechenden Berechtigungen gesetzt sind.

   Bei der TAR.GZ-Version::

       $ ls -ld /path/to/opensearch-3.7.0/data/config/

   Bei der RPM-/DEB-Version::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Überprüfung der Kernel-Parameter**

   ::

       $ sysctl vm.max_map_count

   Überprüfen Sie, dass der Wert mindestens ``262144`` beträgt.

4. **Überprüfung der Java-Version**

   ::

       $ java -version

   Überprüfen Sie, ob Java 21 oder höher installiert ist.

Nächste Schritte
=====================

Nach Abschluss der Installation lesen Sie bitte folgende Dokumentation:

- :doc:`run` - Start und Ersteinrichtung von |Fess|
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Fehlerbehebung

Häufig gestellte Fragen
============================

F: Funktioniert OpenSearch auch mit anderen Versionen?
-----------------------------------------------------------

A: |Fess| hängt von einer bestimmten Version von OpenSearch ab.
Um die Plugin-Kompatibilität zu gewährleisten, wird die Verwendung der empfohlenen Version (3.7.0) dringend empfohlen.
Bei Verwendung anderer Versionen muss auch die Plugin-Version entsprechend angepasst werden.

F: Können mehrere Fess-Instanzen denselben OpenSearch teilen?
------------------------------------------------------------------

A: Möglich, aber nicht empfohlen. Es wird empfohlen, für jede Fess-Instanz einen eigenen OpenSearch-Cluster bereitzustellen.
Bei gemeinsamer Nutzung von OpenSearch durch mehrere Fess-Instanzen ist auf Indexnamen-Konflikte zu achten.

F: Wie konfiguriert man OpenSearch als Cluster?
----------------------------------------------------

A: Siehe die offizielle OpenSearch-Dokumentation `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
Bei Cluster-Konfiguration muss die Einstellung ``discovery.type: single-node`` entfernt und entsprechende Cluster-Einstellungen hinzugefügt werden.
