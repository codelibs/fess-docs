================
Protokollbenachrichtigung
================

Übersicht
====

|Fess| verfügt über eine Funktion, die Protokollereignisse der Ebenen ERROR und WARN automatisch erfasst und Administratoren benachrichtigt.
Diese Funktion ermöglicht eine schnelle Erkennung von Systemanomalien und einen frühzeitigen Beginn der Störungsbehandlung.

Hauptmerkmale:

- **Unterstützte Benachrichtigungskanäle**: E-Mail, Slack, Google Chat
- **Betroffene Prozesse**: Hauptanwendung, Crawler, Vorschlags-Generierung, Thumbnail-Generierung
- **Standardmäßig deaktiviert**: Da es sich um ein Opt-in-Verfahren handelt, muss die Funktion explizit aktiviert werden

Funktionsweise
======

Die Protokollbenachrichtigung arbeitet nach folgendem Ablauf.

1. Der ``LogNotificationAppender`` von Log4j2 erfasst Protokollereignisse ab der konfigurierten Ebene.
2. Die erfassten Ereignisse werden in einem Puffer im Arbeitsspeicher (maximal 1.000 Einträge) gesammelt.
3. Ein Timer schreibt die Ereignisse im Puffer alle 30 Sekunden in einen OpenSearch-Index (``fess_log.notification_queue``).
4. Ein geplanter Job liest alle 5 Minuten Ereignisse aus OpenSearch, gruppiert sie nach Protokollebene und sendet Benachrichtigungen.
5. Nach dem Versand der Benachrichtigungen werden die verarbeiteten Ereignisse aus dem Index gelöscht.

.. note::
   Protokolle der Benachrichtigungsfunktion selbst (``LogNotificationHelper``, ``LogNotificationJob`` usw.)
   werden von der Benachrichtigung ausgeschlossen, um Endlosschleifen zu vermeiden.

Einrichtung
============

Aktivierung
------

Aktivierung über die Verwaltungsoberfläche
~~~~~~~~~~~~~~~~~~~~

1. Melden Sie sich an der Verwaltungsoberfläche an.
2. Wählen Sie im Menü "System" den Punkt "Allgemein".
3. Aktivieren Sie das Kontrollkästchen "Protokollbenachrichtigung".
4. Wählen Sie unter "Protokollbenachrichtigungsebene" die gewünschte Ebene aus (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Klicken Sie auf die Schaltfläche "Aktualisieren".

.. note::
   Standardmäßig wird nur die Ebene ``ERROR`` benachrichtigt.
   Bei Auswahl von ``WARN`` werden sowohl ``WARN`` als auch ``ERROR`` benachrichtigt.

Aktivierung über Systemeigenschaften
~~~~~~~~~~~~~~~~~~~~~~~~

Die Aktivierung kann auch durch direkte Bearbeitung der Systemeigenschaften erfolgen, die in den "Allgemein"-Einstellungen der Verwaltungsoberfläche gespeichert werden.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Konfiguration der Benachrichtigungsziele
------------

E-Mail-Benachrichtigung
~~~~~~~~~~

Für die E-Mail-Benachrichtigung sind folgende Einstellungen erforderlich.

1. Konfiguration des Mailservers (``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Geben Sie in den "Allgemein"-Einstellungen der Verwaltungsoberfläche unter "Benachrichtigungsziel" die E-Mail-Adresse ein. Mehrere Adressen können durch Komma getrennt angegeben werden.

Slack-Benachrichtigung
~~~~~~~~~~

Durch Konfiguration einer Slack Incoming Webhook URL können Benachrichtigungen an einen Slack-Kanal gesendet werden.

Google Chat-Benachrichtigung
~~~~~~~~~~~~~~~~

Durch Konfiguration einer Google Chat Webhook URL können Benachrichtigungen an einen Google Chat-Bereich gesendet werden.

Konfigurationseigenschaften
==============

In der Datei ``fess_config.properties`` können folgende Eigenschaften konfiguriert werden.

.. list-table:: Eigenschaften der Protokollbenachrichtigung
   :header-rows: 1
   :widths: 40 15 45

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``log.notification.flush.interval``
     - ``30``
     - Intervall für das Schreiben vom Puffer nach OpenSearch (Sekunden)
   * - ``log.notification.buffer.size``
     - ``1000``
     - Maximale Anzahl der im Arbeitsspeicher-Puffer gehaltenen Ereignisse
   * - ``log.notification.interval``
     - ``300``
     - Ausführungsintervall des Benachrichtigungsjobs (Sekunden)
   * - ``log.notification.search.size``
     - ``1000``
     - Maximale Anzahl der pro Jobausführung aus OpenSearch abgerufenen Ereignisse
   * - ``log.notification.max.display.events``
     - ``50``
     - Maximale Anzahl der Ereignisse pro Benachrichtigungsnachricht
   * - ``log.notification.max.message.length``
     - ``200``
     - Maximale Zeichenanzahl pro Protokollnachricht (Überschuss wird abgeschnitten)
   * - ``log.notification.max.details.length``
     - ``3000``
     - Maximale Zeichenanzahl des Detailbereichs der Benachrichtigungsnachricht

.. note::
   Änderungen an diesen Eigenschaften werden erst nach einem Neustart von |Fess| wirksam.

Format der Benachrichtigungsnachrichten
====================

E-Mail-Benachrichtigung
----------

E-Mail-Benachrichtigungen werden im folgenden Format gesendet.

**Betreff:**

::

    [FESS] ERROR Log Alert: hostname

**Nachrichtentext:**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR- und WARN-Ereignisse werden als separate Benachrichtigungen pro Ebene gesendet.

Slack- / Google Chat-Benachrichtigung
------------------------

Benachrichtigungen für Slack und Google Chat werden mit demselben Inhalt als Nachricht gesendet.

Betriebshandbuch
==========

Empfohlene Einstellungen
--------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Umgebung
     - Empfohlene Ebene
     - Begründung
   * - Produktionsumgebung
     - ``ERROR``
     - Nur kritische Fehler benachrichtigen, um Störgeräusche zu reduzieren
   * - Staging-Umgebung
     - ``WARN``
     - Auch potenzielle Probleme einbeziehen
   * - Entwicklungsumgebung
     - Deaktiviert
     - Protokolldateien direkt überprüfen

OpenSearch-Index
----------------------

Die Protokollbenachrichtigungsfunktion verwendet den Index ``fess_log.notification_queue`` zur temporären Speicherung von Ereignissen.
Dieser Index wird bei der erstmaligen Nutzung der Funktion automatisch erstellt.
Da Ereignisse nach dem Versand der Benachrichtigungen gelöscht werden, wächst der Index normalerweise nicht übermäßig an.

Fehlerbehebung
======================

Benachrichtigungen werden nicht gesendet
------------------

1. **Aktivierung überprüfen**

   Überprüfen Sie in den "Allgemein"-Einstellungen der Verwaltungsoberfläche, ob "Protokollbenachrichtigung" aktiviert ist.

2. **Benachrichtigungsziel überprüfen**

   Überprüfen Sie bei E-Mail-Benachrichtigung, ob unter "Benachrichtigungsziel" eine E-Mail-Adresse konfiguriert ist.

3. **Mailserver-Einstellungen überprüfen**

   Überprüfen Sie in ``fess_env.properties``, ob der Mailserver korrekt konfiguriert ist.

4. **Protokolle überprüfen**

   Überprüfen Sie in ``fess.log`` die Fehlermeldungen zur Benachrichtigung.

   ::

       grep -i "notification" /var/log/fess/fess.log

Zu viele Benachrichtigungen
--------------

1. **Protokollebene erhöhen**

   Ändern Sie die Benachrichtigungsebene von ``WARN`` auf ``ERROR``.

2. **Ursache beheben**

   Falls häufig Fehler auftreten, untersuchen Sie die eigentliche Ursache der Fehler.

Benachrichtigungsinhalt wird abgeschnitten
------------------------

Passen Sie folgende Eigenschaften an.

- ``log.notification.max.details.length``: Maximale Zeichenanzahl des Detailbereichs
- ``log.notification.max.display.events``: Maximale Anzahl der anzuzeigenden Ereignisse
- ``log.notification.max.message.length``: Maximale Zeichenanzahl pro Nachricht

Referenzinformationen
========

- :doc:`admin-logging` - Protokollkonfiguration
- :doc:`setup-memory` - Speicherkonfiguration
