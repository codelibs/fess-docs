============
Protokollkonfiguration
============

Übersicht
====

|Fess| gibt mehrere Protokolldateien aus, um Systembetriebsstatus und Fehlerinformationen aufzuzeichnen.
Durch angemessene Protokollkonfiguration werden Fehlersuche und Systemüberwachung erleichtert.

Arten von Protokolldateien
==================

Hauptprotokoll

dateien
------------------

Hauptprotokolldateien, die |Fess| ausgibt:

.. list-table:: Liste der Protokolldateien
   :header-rows: 1
   :widths: 25 75

   * - Dateiname
     - Inhalt
   * - ``fess.log``
     - Betriebsprotokolle in Verwaltungs- und Suchoberfläche, Anwendungsfehler, Systemereignisse
   * - ``fess_crawler.log``
     - Protokolle bei Crawler-Ausführung, Ziel-URLs, abgerufene Dokumentinformationen, Fehler
   * - ``fess_suggest.log``
     - Protokolle bei Vorschlags-Generierung, Index-Aktualisierungsinformationen
   * - ``server_?.log``
     - Systemprotokolle des Anwendungsservers wie Tomcat
   * - ``audit.log``
     - Audit-Protokolle für Benutzerauthentifizierung, An-/Abmeldung, wichtige Operationen

Speicherort der Protokolldateien
------------------

**Bei Zip-Installation:**

::

    {FESS_HOME}/logs/

**Bei RPM/DEB-Paketen:**

::

    /var/log/fess/

Protokollüberprüfung bei Fehlersuche
----------------------------------

Bei Problemen überprüfen Sie Protokolle wie folgt:

1. **Fehlertyp identifizieren**

   - Anwendungsfehler → ``fess.log``
   - Crawler-Fehler → ``fess_crawler.log``
   - Authentifizierungsfehler → ``audit.log``
   - Serverfehler → ``server_?.log``

2. **Neueste Fehler überprüfen**

   ::

       tail -f /var/log/fess/fess.log

3. **Nach bestimmten Fehlern suchen**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

Konfiguration der Protokollebenen
================

Was sind Protokollebenen?
--------------

Protokollebenen steuern Detailgrad der auszugebenden Protokolle.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Ebene
     - Beschreibung
   * - ``FATAL``
     - Kritische Fehler (Anwendung kann nicht fortgesetzt werden)
   * - ``ERROR``
     - Fehler (Teil der Funktionalität funktioniert nicht)
   * - ``WARN``
     - Warnung (potenzielle Probleme)
   * - ``INFO``
     - Information (wichtige Ereignisse)
   * - ``DEBUG``
     - Debug-Informationen (detaillierte Betriebsprotokolle)
   * - ``TRACE``
     - Trace-Informationen (am detailliertesten)

Empfohlene Protokollebenen
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Umgebung
     - Empfohlene Ebene
     - Begründung
   * - Produktionsumgebung
     - ``WARN``
     - Fokus auf Leistung und Speicherplatz
   * - Staging-Umgebung
     - ``INFO``
     - Aufzeichnung wichtiger Ereignisse
   * - Entwicklungsumgebung
     - ``DEBUG``
     - Detaillierte Debug-Informationen erforderlich
   * - Bei Problemuntersuchung
     - ``DEBUG`` oder ``TRACE``
     - Temporär detaillierte Protokolle aktivieren

Protokollrotation
==================

Übersicht
----

Protokolldateien wachsen mit der Zeit, daher ist regelmäßige Rotation (Generationsverwaltung) erforderlich.

Automatische Rotation durch Log4j2
-------------------------------

|Fess| verwendet RollingFileAppender von Log4j2 für automatische Protokollrotation.

Standardkonfiguration
~~~~~~~~~~~~~~~~

- **Dateigröße**: Rotation bei über 10 MB
- **Aufbewahrungsgenerationen**: Maximal 10 Dateien

Beispiel für Konfigurationsdatei (``log4j2.xml``):

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

Referenzinformationen
========

- :doc:`setup-memory` - Speicherkonfiguration
- :doc:`crawler-advanced` - Erweiterte Crawler-Konfiguration
- :doc:`admin-index-backup` - Index-Backup
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
