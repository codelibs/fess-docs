==================
Systemanforderungen
==================

Auf dieser Seite werden die Hardware- und Softwareanforderungen beschrieben, die für den Betrieb von |Fess| erforderlich sind.

Hardwareanforderungen
=====================

Mindestanforderungen
--------------------

Die folgenden Mindestanforderungen gelten für Evaluierungs- und Entwicklungsumgebungen:

- CPU: 2 Kerne oder mehr
- Arbeitsspeicher: 4 GB oder mehr
- Festplattenkapazität: 10 GB oder mehr freier Speicherplatz

Empfohlene Anforderungen
------------------------

Für Produktionsumgebungen werden folgende Spezifikationen empfohlen:

- CPU: 4 Kerne oder mehr
- Arbeitsspeicher: 8 GB oder mehr (abhängig von der Indexgröße)
- Festplattenkapazität:

  - Systembereich: 20 GB oder mehr
  - Datenbereich: Mindestens das Dreifache der Indexgröße (einschließlich Replikate)

- Netzwerk: 1 Gbps oder mehr

.. note::

   Wenn die Indexgröße zunimmt oder häufige Crawls durchgeführt werden,
   sollten Arbeitsspeicher und Festplattenkapazität entsprechend erhöht werden.

Softwareanforderungen
=====================

Betriebssystem
--------------

|Fess| läuft auf folgenden Betriebssystemen:

**Linux**

- Red Hat Enterprise Linux 8 oder höher
- CentOS 8 oder höher
- Ubuntu 20.04 LTS oder höher
- Debian 11 oder höher
- Andere Linux-Distributionen (Umgebungen, in denen Java 21 ausgeführt werden kann)

**Windows**

- Windows Server 2019 oder höher
- Windows 10 oder höher

**Sonstiges**

- macOS 11 (Big Sur) oder höher (nur für Entwicklungsumgebungen empfohlen)
- Umgebungen, in denen Docker ausgeführt werden kann

Erforderliche Software
----------------------

Je nach Installationsmethode wird folgende Software benötigt:

TAR.GZ/ZIP/RPM/DEB Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Java 21**: `Eclipse Temurin <https://adoptium.net/temurin>`__ wird empfohlen

  - OpenJDK 21 oder höher
  - Eclipse Temurin 21 oder höher

- **OpenSearch 3.3.0**: Erforderlich für Produktionsumgebungen (eingebettete Version nicht empfohlen)

  - Unterstützte Version: OpenSearch 3.3.0
  - Bei anderen Versionen ist auf Plugin-Kompatibilität zu achten

Docker Version
~~~~~~~~~~~~~~

- **Docker**: 20.10 oder höher
- **Docker Compose**: 2.0 oder höher

Netzwerkanforderungen
=====================

Erforderliche Ports
-------------------

Die Hauptports, die von |Fess| verwendet werden, sind wie folgt:

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - Port
     - Protokoll
     - Verwendungszweck
   * - 8080
     - HTTP
     - |Fess| Weboberfläche (Such- und Verwaltungsseite)
   * - 9200
     - HTTP
     - OpenSearch HTTP API (Kommunikation von |Fess| zu OpenSearch)
   * - 9300
     - TCP
     - OpenSearch Transport-Kommunikation (bei Cluster-Konfiguration)

.. warning::

   In Produktionsumgebungen wird dringend empfohlen, den direkten Zugriff auf die Ports 9200 und 9300 von außen zu beschränken.
   Diese Ports sollten nur für die interne Kommunikation zwischen |Fess| und OpenSearch verwendet werden.

Firewall-Konfiguration
----------------------

Wenn |Fess| von außen zugänglich sein soll, muss Port 8080 geöffnet werden.

**Linux (mit firewalld)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (mit iptables)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

Browseranforderungen
====================

Für die Verwaltungs- und Suchoberfläche von |Fess| werden folgende Browser empfohlen:

- Google Chrome (neueste Version)
- Mozilla Firefox (neueste Version)
- Microsoft Edge (neueste Version)
- Safari (neueste Version)

.. note::

   Internet Explorer wird nicht unterstützt.

Checkliste für Voraussetzungen
===============================

Überprüfen Sie vor der Installation folgende Punkte:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Prüfpunkt
     - Status
   * - Werden die Hardwareanforderungen erfüllt?
     - □
   * - Ist Java 21 installiert? (außer Docker-Version)
     - □
   * - Ist Docker installiert? (Docker-Version)
     - □
   * - Sind die erforderlichen Ports verfügbar?
     - □
   * - Ist die Firewall-Konfiguration korrekt?
     - □
   * - Ist ausreichend Festplattenkapazität vorhanden?
     - □
   * - Funktioniert die Netzwerkverbindung? (beim Crawlen externer Sites)
     - □

Nächste Schritte
================

Nachdem Sie die Systemanforderungen überprüft haben, fahren Sie mit den Installationsanweisungen für Ihre Umgebung fort:

- :doc:`install-linux` - Installation für Linux (TAR.GZ/RPM/DEB)
- :doc:`install-windows` - Installation für Windows (ZIP)
- :doc:`install-docker` - Installation für Docker
- :doc:`install` - Übersicht über Installationsmethoden
