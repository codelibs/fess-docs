==================================
Installation unter Linux (Detaillierte Anleitung)
==================================

Diese Seite beschreibt die Installationsschritte von |Fess| in Linux-Umgebungen.
Sie behandelt die Paketformate TAR.GZ, RPM und DEB.

.. warning::

   In Produktionsumgebungen wird der Betrieb mit eingebettetem OpenSearch nicht empfohlen.
   Bitte richten Sie unbedingt einen externen OpenSearch-Server ein.

Voraussetzungen
===============

- Die in :doc:`prerequisites` beschriebenen Systemanforderungen sind erfüllt
- Java 21 ist installiert
- OpenSearch 3.3.2 ist verfügbar (oder wird neu installiert)

Auswahl der Installationsmethode
=================================

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

Installation mit TAR.GZ-Version
================================

Schritt 1: Installation von OpenSearch
---------------------------------------

1. Download von OpenSearch

   Laden Sie die TAR.GZ-Version von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.tar.gz
       $ tar -xzf opensearch-3.3.2-linux-x64.tar.gz
       $ cd opensearch-3.3.2

   .. note::

      In diesem Beispiel wird OpenSearch 3.3.2 verwendet.
      Überprüfen Sie die unterstützte Version für |Fess|.

2. Installation der OpenSearch-Plugins

   Installieren Sie die von |Fess| benötigten Plugins.

   ::

       $ cd /path/to/opensearch-3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

   .. important::

      Die Plugin-Version muss mit der OpenSearch-Version übereinstimmen.
      Im obigen Beispiel sind alle auf 3.3.2 gesetzt.

3. Konfiguration von OpenSearch

   Fügen Sie in ``config/opensearch.yml`` folgende Einstellungen hinzu.

   ::

       # Pfad für Konfigurationssynchronisation (als absoluter Pfad angeben)
       configsync.config_path: /path/to/opensearch-3.3.2/data/config/

       # Deaktivierung des Sicherheits-Plugins (nur Entwicklungsumgebung)
       plugins.security.disabled: true

   .. warning::

      **Wichtiger Sicherheitshinweis**

      ``plugins.security.disabled: true`` sollte nur in Entwicklungs- oder Testumgebungen verwendet werden.
      In Produktionsumgebungen aktivieren Sie bitte das Sicherheits-Plugin von OpenSearch und konfigurieren Sie entsprechende Authentifizierungs- und Autorisierungseinstellungen.
      Weitere Informationen finden Sie unter :doc:`security`.

   .. tip::

      Passen Sie andere Einstellungen wie Clustername und Netzwerkeinstellungen entsprechend Ihrer Umgebung an.
      Konfigurationsbeispiel::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

Schritt 2: Installation von Fess
---------------------------------

1. Download und Entpacken von Fess

   Laden Sie die TAR.GZ-Version von der `Download-Site <https://fess.codelibs.org/ja/downloads.html>`__ herunter.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz
       $ cd fess-15.3.2

2. Konfiguration von Fess

   Bearbeiten Sie ``bin/fess.in.sh`` und konfigurieren Sie die Verbindungsinformationen zu OpenSearch.

   ::

       $ vi bin/fess.in.sh

   Fügen Sie folgende Einstellungen hinzu oder ändern Sie sie::

       # OpenSearch HTTP-Endpunkt
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

       # Pfad für Wörterbuchdateien (identisch mit configsync.config_path von OpenSearch)
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.3.2/data/config/

   .. note::

      Wenn OpenSearch auf einem anderen Host ausgeführt wird,
      ändern Sie ``SEARCH_ENGINE_HTTP_URL`` auf den entsprechenden Hostnamen oder die IP-Adresse.
      Beispiel: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``

3. Überprüfung der Installation

   Überprüfen Sie, ob die Konfigurationsdateien korrekt bearbeitet wurden::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Schritt 3: Start
----------------

Die Startanleitung finden Sie unter :doc:`run`.

Installation mit RPM-Version
=============================

Die RPM-Version wird für RPM-basierte Linux-Distributionen wie Red Hat Enterprise Linux, CentOS und Fedora verwendet.

Schritt 1: Installation von OpenSearch
---------------------------------------

1. Download und Installation des OpenSearch-RPM

   Laden Sie das RPM-Paket von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.3.2-linux-x64.rpm

   Alternativ können Sie auch ein Repository hinzufügen und die Installation durchführen.
   Details finden Sie unter `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Installation der OpenSearch-Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

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
---------------------------------

1. Installation des Fess-RPM

   Laden Sie das RPM-Paket von der `Download-Site <https://fess.codelibs.org/ja/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.rpm
       $ sudo rpm -ivh fess-15.3.2.rpm

2. Konfiguration von Fess

   Bearbeiten Sie ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Fügen Sie folgende Einstellungen hinzu oder ändern Sie sie::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Dienstregistrierung

   **Bei Verwendung von chkconfig**::

       $ sudo /sbin/chkconfig --add opensearch
       $ sudo /sbin/chkconfig --add fess

   **Bei Verwendung von systemd** (empfohlen)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Schritt 3: Start
----------------

Die Startanleitung finden Sie unter :doc:`run`.

Installation mit DEB-Version
=============================

Die DEB-Version wird für DEB-basierte Linux-Distributionen wie Debian und Ubuntu verwendet.

Schritt 1: Installation von OpenSearch
---------------------------------------

1. Download und Installation des OpenSearch-DEB

   Laden Sie das DEB-Paket von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.deb
       $ sudo dpkg -i opensearch-3.3.2-linux-x64.deb

   Alternativ können Sie auch ein Repository hinzufügen und die Installation durchführen.
   Details finden Sie unter `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Installation der OpenSearch-Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

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
---------------------------------

1. Installation des Fess-DEB

   Laden Sie das DEB-Paket von der `Download-Site <https://fess.codelibs.org/ja/downloads.html>`__ herunter und installieren Sie es.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.deb
       $ sudo dpkg -i fess-15.3.2.deb

2. Konfiguration von Fess

   Bearbeiten Sie ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Fügen Sie folgende Einstellungen hinzu oder ändern Sie sie::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Dienstregistrierung

   Aktivieren Sie den Dienst mit systemd::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Schritt 3: Start
----------------

Die Startanleitung finden Sie unter :doc:`run`.

Überprüfung nach der Installation
==================================

Überprüfen Sie nach Abschluss der Installation Folgendes:

1. **Überprüfung der Konfigurationsdateien**

   - OpenSearch-Konfigurationsdatei (opensearch.yml)
   - Fess-Konfigurationsdatei (fess.in.sh)

2. **Verzeichnisberechtigungen**

   Überprüfen Sie, ob die in der Konfiguration angegebenen Verzeichnisse existieren und die entsprechenden Berechtigungen gesetzt sind.

   TAR.GZ-Version::

       $ ls -ld /path/to/opensearch-3.3.2/data/config/

   RPM/DEB-Version::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Überprüfung der Java-Version**

   ::

       $ java -version

   Überprüfen Sie, ob Java 21 oder höher installiert ist.

Nächste Schritte
================

Nach Abschluss der Installation lesen Sie bitte folgende Dokumentation:

- :doc:`run` - Start und Ersteinrichtung von |Fess|
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Fehlerbehebung

Häufig gestellte Fragen
=======================

F: Funktioniert OpenSearch auch mit anderen Versionen?
-------------------------------------------------------

A: |Fess| hängt von einer bestimmten Version von OpenSearch ab.
Um die Plugin-Kompatibilität zu gewährleisten, wird die Verwendung der empfohlenen Version (3.3.2) dringend empfohlen.
Bei Verwendung anderer Versionen muss auch die Plugin-Version entsprechend angepasst werden.

F: Können mehrere Fess-Instanzen denselben OpenSearch teilen?
--------------------------------------------------------------

A: Möglich, aber nicht empfohlen. Es wird empfohlen, für jede Fess-Instanz einen eigenen OpenSearch-Cluster bereitzustellen.
Bei gemeinsamer Nutzung von OpenSearch durch mehrere Fess-Instanzen ist auf Indexnamen-Konflikte zu achten.

F: Wie konfiguriert man OpenSearch als Cluster?
------------------------------------------------

A: Siehe die offizielle OpenSearch-Dokumentation `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
Bei Cluster-Konfiguration muss die Einstellung ``discovery.type: single-node`` entfernt und entsprechende Cluster-Einstellungen hinzugefügt werden.
