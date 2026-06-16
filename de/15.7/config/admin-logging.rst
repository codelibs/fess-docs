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
   * - ``fess-crawler.log``
     - Protokolle bei Crawler-Ausführung, Ziel-URLs, abgerufene Dokumentinformationen, Fehler
   * - ``fess-suggest.log``
     - Protokolle bei Vorschlags-Generierung, Index-Aktualisierungsinformationen
   * - ``fess-thumbnail.log``
     - Protokolle des Thumbnail-Generierungsprozesses
   * - ``fess-llm.log``
     - LLM/RAG-Chat-bezogene Protokolle
   * - ``searchlog.log``
     - Suchprotokolle
   * - ``fess-urls.log``
     - Crawler-URL-Statistikprotokoll (wird vom Crawl-Prozess ausgegeben)
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
   - Crawler-Fehler → ``fess-crawler.log``
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

Änderung über Konfigurationsdatei
----------------------------------

Für eine detailliertere Protokollkonfiguration bearbeiten Sie die Log4j2-Konfigurationsdatei.

Speicherort der Konfigurationsdatei
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **ZIP-Installation**: ``app/WEB-INF/classes/log4j2.xml``
- **RPM/DEB-Pakete**: ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``

Grundlegende Konfigurationsbeispiele
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Standard-Protokollebene:**

In der Standard-Datei ``log4j2.xml`` wird die Protokollebene über die Variable ``${log.level}`` angegeben.
Diese Variable wird beim Start mit dem Wert von ``-Dfess.log.level`` (``FESS_LOG_LEVEL``, Standard: ``warn``) aufgelöst.

::

    <Logger name="org.codelibs" level="${log.level}"/>

Sie können anstelle der Variable auch direkt eine Ebene angeben.

**Beispiel: Auf DEBUG-Ebene ändern**

::

    <Logger name="org.codelibs" level="debug"/>

**Beispiel: Protokollebene für bestimmtes Paket ändern**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   Die Ebenen ``DEBUG`` und ``TRACE`` geben große Mengen an Protokollen aus.
   Verwenden Sie diese nicht in Produktionsumgebungen, da sie Festplattenspeicher und Leistung beeinträchtigen.

Konfiguration über Umgebungsvariablen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Protokollebene kann auch beim Systemstart festgelegt werden.
Setzen Sie ``FESS_LOG_LEVEL`` in ``fess.in.sh`` (Linux).

::

    FESS_LOG_LEVEL=debug

Der Standardwert ist ``warn``.

.. note::
   Die Windows-Datei ``fess.in.bat`` liest die Umgebungsvariable ``FESS_LOG_LEVEL`` nicht aus.
   Da der Wert dort direkt als ``-Dfess.log.level=warn`` eingetragen ist, muss diese Zeile in
   ``fess.in.bat`` direkt bearbeitet werden, um die Protokollebene unter Windows zu ändern.

   ::

       set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.log.level=debug

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

- **Dateigröße**: Rotation bei über 100 MB
- **Aufbewahrungsgenerationen**: Maximal 10 Dateien

Beispiel für Konfigurationsdatei (``log4j2.xml``):

::

    <RollingFile name="AppFile"
                 fileName="${log.file.basedir}/${domain.name}.log"
                 filePattern="${log.file.basedir}/${domain.name}${backup.date.suffix}-%i.log.gz">
        <PatternLayout><Pattern>${log.pattern}</Pattern></PatternLayout>
        <Policies>
            <TimeBasedTriggeringPolicy />
            <SizeBasedTriggeringPolicy size="100 MB"/>
        </Policies>
        <DefaultRolloverStrategy fileIndex="max" min="1"
            max="${backup.max.history}" compressionLevel="9">
            <Delete basePath="${log.file.basedir}">
                <IfFileName glob="${domain.name}*.log.gz" />
                <IfLastModified age="P${backup.max.age}D" />
            </Delete>
        </DefaultRolloverStrategy>
    </RollingFile>

Referenzinformationen
========

- :doc:`admin-log-notification` - Log-Benachrichtigungskonfiguration
- :doc:`setup-memory` - Speicherkonfiguration
- :doc:`crawler-advanced` - Erweiterte Crawler-Konfiguration
- :doc:`admin-index-backup` - Index-Backup
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
