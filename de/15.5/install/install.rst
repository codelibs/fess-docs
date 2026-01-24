==============================
Auswahl der Installationsmethode
==============================

Diese Seite beschreibt eine Übersicht über die Installationsmethoden von |Fess|.
Bitte wählen Sie die für Ihre Umgebung geeignete Installationsmethode.

.. warning::

   **Wichtiger Hinweis für Produktionsumgebungen**

   In Produktionsumgebungen oder bei Lasttests wird der Betrieb mit eingebettetem OpenSearch nicht empfohlen.
   Bitte richten Sie unbedingt einen externen OpenSearch-Server ein.

Überprüfung der Voraussetzungen
================================

Überprüfen Sie vor Beginn der Installation die Systemanforderungen.

Weitere Informationen finden Sie unter :doc:`prerequisites`.

Vergleich der Installationsmethoden
====================================

|Fess| kann mit folgenden Methoden installiert werden. Wählen Sie je nach Umgebung und Verwendungszweck die passende Methode.

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - Methode
     - Ziel-OS
     - Empfohlene Verwendung
     - Detaillierte Dokumentation
   * - Docker
     - Linux, Windows, macOS
     - Entwicklungs-/Evaluierungsumgebung, schnelle Einrichtung
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - Umgebungen, die Anpassungen erfordern
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - Produktionsumgebung (RPM-basiert)
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - Produktionsumgebung (DEB-basiert)
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Entwicklung/Produktion in Windows-Umgebung
     - :doc:`install-windows`

Merkmale der einzelnen Installationsmethoden
=============================================

Docker-Version
--------------

**Vorteile:**

- Schnellste Einrichtung möglich
- Keine Verwaltung von Abhängigkeiten erforderlich
- Ideal für Entwicklungsumgebungen
- Einfaches Starten und Stoppen von Containern

**Nachteile:**

- Docker-Kenntnisse erforderlich

**Empfohlene Umgebung:** Entwicklungsumgebung, Evaluierungsumgebung, POC, Produktionsumgebung

Details: :doc:`install-docker`

Linux-Paketversion (TAR.GZ/RPM/DEB)
-----------------------------------

**Vorteile:**

- Hohe Leistung in nativer Umgebung
- Als Systemdienst verwaltbar (RPM/DEB)
- Detaillierte Anpassungen möglich

**Nachteile:**

- Manuelle Installation von Java und OpenSearch erforderlich
- Konfigurationsaufwand

**Empfohlene Umgebung:** Produktionsumgebung, Umgebungen mit Anpassungsbedarf

Details: :doc:`install-linux`

Windows-Version (ZIP)
---------------------

**Vorteile:**

- Läuft in nativer Windows-Umgebung
- Kein Installer erforderlich

**Nachteile:**

- Manuelle Installation von Java und OpenSearch erforderlich
- Konfigurationsaufwand

**Empfohlene Umgebung:** Entwicklung/Evaluierung in Windows-Umgebung, Produktionsbetrieb auf Windows Server

Details: :doc:`install-windows`

Grundlegender Installationsablauf
==================================

Der grundlegende Ablauf ist bei allen Installationsmethoden gleich.

1. **Überprüfung der Systemanforderungen**

   Siehe :doc:`prerequisites` und überprüfen Sie, ob die Systemanforderungen erfüllt sind.

2. **Software-Download**

   Laden Sie |Fess| von der `Download-Site <https://fess.codelibs.org/de/downloads.html>`__ herunter.

   Bei der Docker-Version laden Sie die Docker Compose-Dateien herunter.

3. **Einrichtung von OpenSearch**

   Bei anderen Versionen als der Docker-Version muss OpenSearch separat eingerichtet werden.

   - Installation von OpenSearch 3.3.2
   - Installation der erforderlichen Plugins
   - Bearbeitung der Konfigurationsdateien

4. **Einrichtung von Fess**

   - Installation von Fess
   - Bearbeitung der Konfigurationsdateien (Verbindungsinformationen zu OpenSearch usw.)

5. **Start und Überprüfung**

   - Start des Dienstes
   - Zugriff über den Browser und Funktionsprüfung

   Details finden Sie unter :doc:`run`.

Erforderliche Komponenten
=========================

Für den Betrieb von |Fess| sind folgende Komponenten erforderlich.

Fess-Hauptsystem
----------------

Das Volltext-Suchsystem selbst. Es bietet Funktionen wie Weboberfläche, Crawler und Indexer.

OpenSearch
----------

Verwendet OpenSearch als Suchmaschine.

- **Unterstützte Version**: OpenSearch 3.3.2
- **Erforderliche Plugins**:

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   Die Version von OpenSearch und die Version der Plugins müssen übereinstimmen.
   Versionsunterschiede können zu Startfehlern oder unerwartetem Verhalten führen.

Java (außer Docker-Version)
----------------------------

Für die TAR.GZ/ZIP/RPM/DEB-Version ist Java 21 oder höher erforderlich.

- Empfohlen: `Eclipse Temurin <https://adoptium.net/temurin>`__
- OpenJDK 21 oder höher kann ebenfalls verwendet werden

.. note::

   Bei der Docker-Version ist Java im Docker-Image enthalten und muss nicht separat installiert werden.

Nächste Schritte
================

Überprüfen Sie die Systemanforderungen und wählen Sie die geeignete Installationsmethode.

1. :doc:`prerequisites` - Überprüfung der Systemanforderungen
2. Auswahl der Installationsmethode:

   - :doc:`install-docker` - Installation mit Docker
   - :doc:`install-linux` - Installation unter Linux
   - :doc:`install-windows` - Installation unter Windows

3. :doc:`run` - Start und Ersteinrichtung von |Fess|
4. :doc:`security` - Sicherheitseinstellungen (für Produktionsumgebungen)

Häufig gestellte Fragen
=======================

F: Ist OpenSearch erforderlich?
--------------------------------

A: Ja, es ist erforderlich. |Fess| verwendet OpenSearch als Suchmaschine.
Bei der Docker-Version wird es automatisch eingerichtet, bei anderen Methoden muss es manuell installiert werden.

F: Ist ein Upgrade von früheren Versionen möglich?
---------------------------------------------------

A: Ja, das ist möglich. Weitere Informationen finden Sie unter :doc:`upgrade`.

F: Kann das System auf mehreren Servern konfiguriert werden?
-------------------------------------------------------------

A: Ja, das ist möglich. Fess und OpenSearch können auf separaten Servern ausgeführt werden.
Durch Konfiguration von OpenSearch als Cluster sind hohe Verfügbarkeit und Leistungsverbesserungen möglich.

Downloads
=========

|Fess| und zugehörige Komponenten können von folgenden Quellen heruntergeladen werden:

- **Fess**: `Download-Site <https://fess.codelibs.org/de/downloads.html>`__
- **OpenSearch**: `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)**: `Adoptium <https://adoptium.net/>`__
- **Docker**: `Get Docker <https://docs.docker.com/get-docker/>`__

Versionsinformationen
=====================

Diese Dokumentation bezieht sich auf folgende Versionen:

- **Fess**: 15.5.0
- **OpenSearch**: 3.3.2
- **Java**: 21 oder höher
- **Docker**: 20.10 oder höher
- **Docker Compose**: 2.0 oder höher

Dokumentation für frühere Versionen finden Sie in der jeweiligen Versionsdokumentation.
