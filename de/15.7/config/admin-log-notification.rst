=========================
Protokollbenachrichtigung
=========================

Übersicht
=========

|Fess| verfügt über eine Funktion, die Protokollereignisse der Ebenen ERROR und WARN automatisch erfasst und Administratoren benachrichtigt.
Diese Funktion ermöglicht eine schnelle Erkennung von Systemanomalien und einen frühzeitigen Beginn der Störungsbehandlung.

Hauptmerkmale:

- **Unterstützte Benachrichtigungskanäle**: E-Mail, Slack, Google Chat
- **Betroffene Prozesse**: Hauptanwendung, Crawler, Vorschlags-Generierung, Thumbnail-Generierung
- **Standardmäßig deaktiviert**: Da es sich um ein Opt-in-Verfahren handelt, muss die Funktion explizit aktiviert werden

Funktionsweise
==============

Die Protokollbenachrichtigung arbeitet nach folgendem Ablauf.

1. Der ``LogNotificationAppender`` von Log4j2 erfasst Protokollereignisse ab der konfigurierten Ebene.
2. Die erfassten Ereignisse werden in einem Puffer im Arbeitsspeicher (standardmäßig maximal 1.000 Einträge) gesammelt. Übersteigt der Puffer das Maximum, werden die ältesten Ereignisse zuerst verworfen.
3. Ein Timer schreibt die Ereignisse im Puffer alle 30 Sekunden in einen OpenSearch-Index (``fess_log.notification_queue``).
4. Der geplante Job „Log Notification“ liest alle 5 Minuten Ereignisse aus OpenSearch, gruppiert sie nach Protokollebene und sendet pro Ebene eine Benachrichtigung.
5. Nach dem Versand der Benachrichtigungen werden die verarbeiteten Ereignisse aus dem Index gelöscht.

.. note::
   Jeder Knoten benachrichtigt nur über die von ihm selbst aufgezeichneten Protokolle (die Ereignisse werden nach ``hostname`` gefiltert).
   In einer Cluster-Konfiguration wird pro Knoten eine eigene Benachrichtigung gesendet.

.. note::
   Um Endlosschleifen zu vermeiden, werden Protokolle der Logger, die zur Benachrichtigungsfunktion selbst gehören
   (``LogNotificationAppender``, ``LogNotificationHelper``, ``LogNotificationTarget``,
   ``LogNotificationJob``, ``NotificationHelper`` sowie das für die HTTP-Kommunikation verwendete
   ``org.codelibs.curl``), von der Benachrichtigung ausgeschlossen.

Einrichtung
===========

Aktivierung
-----------

Aktivierung über die Verwaltungsoberfläche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Melden Sie sich an der Verwaltungsoberfläche an.
2. Wählen Sie im Menü **System** den Punkt **Allgemein**.
3. Aktivieren Sie das Kontrollkästchen **Log Notification**.
4. Wählen Sie unter **Log Notification Level** die zu benachrichtigende Ebene aus (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Klicken Sie auf die Schaltfläche „Aktualisieren“.

.. note::
   Standardmäßig wird nur die Ebene ``ERROR`` benachrichtigt.
   Bei Auswahl von ``WARN`` werden sowohl ``WARN`` als auch ``ERROR`` benachrichtigt.

Aktivierung über Systemeigenschaften
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sie können auch die Systemeigenschaften (``system.properties``), die über die **Allgemein**-Einstellungen der Verwaltungsoberfläche gespeichert werden, direkt setzen.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Konfiguration der Benachrichtigungsziele
----------------------------------------

Die Benachrichtigungsziele (E-Mail-Empfänger, Slack-/Google-Chat-Webhook-URLs) werden alle über die
Einstellungen unter **System** → **Allgemein** in der Verwaltungsoberfläche konfiguriert. Konfigurieren Sie mindestens ein Benachrichtigungsziel.
Ist kein einziges Benachrichtigungsziel konfiguriert, beendet der Protokollbenachrichtigungsjob seine Ausführung, ohne etwas zu senden.

E-Mail-Benachrichtigung
~~~~~~~~~~~~~~~~~~~~~~~~

Für die E-Mail-Benachrichtigung sind folgende Einstellungen erforderlich.

1. Konfiguration des Mailservers (``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Geben Sie in den **Allgemein**-Einstellungen der Verwaltungsoberfläche unter **Benachrichtigungs-E-Mail** die E-Mail-Adresse ein.
   Mehrere Adressen können durch Komma getrennt angegeben werden.

Slack-Benachrichtigung
~~~~~~~~~~~~~~~~~~~~~~~

Geben Sie die Slack Incoming Webhook URL in den **Allgemein**-Einstellungen der Verwaltungsoberfläche unter **Slack Webhook URLs** ein.
Mehrere URLs können durch Komma oder Leerzeichen getrennt angegeben werden.
Dieser Wert wird als Systemeigenschaft ``slack.webhook.urls`` gespeichert.

Google Chat-Benachrichtigung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Geben Sie die Google Chat Webhook URL in den **Allgemein**-Einstellungen der Verwaltungsoberfläche unter **Google Chat Webhook URLs** ein.
Mehrere URLs können durch Komma oder Leerzeichen getrennt angegeben werden.
Dieser Wert wird als Systemeigenschaft ``google.chat.webhook.urls`` gespeichert.

.. note::
   Wenn Sie ohne Konfiguration einer **Benachrichtigungs-E-Mail** nur die Slack- oder Google-Chat-Webhook-URL konfigurieren,
   wird keine E-Mail gesendet, sondern nur die Benachrichtigung an Slack bzw. Google Chat.
   An Slack bzw. Google Chat werden derselbe Betreff und derselbe Nachrichtentext wie bei der E-Mail-Benachrichtigung als Nachricht gesendet.

Konfigurationseigenschaften
===========================

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
     - In der Benachrichtigungsnachricht angezeigter Erfassungszeitraum (Sekunden). Ein reiner Anzeigewert, nicht das tatsächliche Ausführungsintervall des Jobs (siehe nachfolgenden Hinweis).
   * - ``log.notification.search.size``
     - ``1000``
     - Maximale Anzahl der pro Jobausführung aus OpenSearch abgerufenen Ereignisse
   * - ``log.notification.max.display.events``
     - ``50``
     - Maximale Anzahl der pro Benachrichtigungsnachricht enthaltenen Ereignisse
   * - ``log.notification.max.message.length``
     - ``200``
     - Maximale Zeichenanzahl pro Protokollnachricht (Überschuss wird abgeschnitten)
   * - ``log.notification.max.details.length``
     - ``3000``
     - Maximale Zeichenanzahl des Detailbereichs der Benachrichtigungsnachricht

.. note::
   Änderungen an ``log.notification.flush.interval`` werden erst nach einem Neustart von |Fess| wirksam.
   Die übrigen Eigenschaften werden ab dem nächsten Benachrichtigungszyklus wirksam.

.. note::
   ``log.notification.interval`` ist der Wert, der für den Anzeigetext „in den letzten N Sekunden“
   in der Benachrichtigungsnachricht verwendet wird; die Ausführungshäufigkeit des Jobs ändert sich dadurch nicht. Das tatsächliche
   Ausführungsintervall wird durch die Cron-Einstellung des geplanten Jobs „Log Notification“
   bestimmt (standardmäßig alle 5 Minuten). Wenn Sie das Ausführungsintervall des Jobs
   ändern möchten, ändern Sie den Cron-Ausdruck dieses Jobs unter **System** → **Scheduler** und
   passen Sie ``log.notification.interval`` entsprechend an, damit die Anzeige mit der Realität übereinstimmt.

Format der Benachrichtigungsnachrichten
=======================================

E-Mail-Benachrichtigung
-----------------------

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
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR- und WARN-Ereignisse werden als separate Benachrichtigungen pro Ebene gesendet.

.. note::
   Übersteigt die Anzahl der anzuzeigenden Ereignisse den Wert von ``log.notification.max.display.events``, beginnt der Anfang
   des Detailbereichs mit ``Total: N event(s) (showing M)`` und am Ende wird ``... and X more`` angefügt.
   Übersteigt eine Protokollnachricht den Wert von ``log.notification.max.message.length``, wird sie am Ende mit ``...``
   abgeschnitten, und übersteigt der gesamte Detailbereich den Wert von ``log.notification.max.details.length``, wird der Rest
   abgeschnitten.

Slack- / Google Chat-Benachrichtigung
-------------------------------------

Benachrichtigungen für Slack und Google Chat werden mit demselben Inhalt als Nachricht gesendet.

Betriebshandbuch
================

Empfohlene Einstellungen
------------------------

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
----------------

Die Protokollbenachrichtigungsfunktion verwendet den Index ``fess_log.notification_queue`` zur temporären Speicherung von Ereignissen
(der Indexname setzt sich aus dem Wert von ``index.log`` (Standard ``fess_log``) und dem angehängten ``.notification_queue``
zusammen). Dieser Index wird bei der erstmaligen Nutzung der Funktion automatisch erstellt.
Da Ereignisse nach dem Versand der Benachrichtigungen gelöscht werden, wächst der Index normalerweise nicht übermäßig an.

.. note::
   Die Anzahl der pro Jobausführung verarbeiteten Ereignisse ist durch ``log.notification.search.size`` (Standard
   1.000 Einträge) begrenzt. Über diese Grenze hinaus angesammelte Ereignisse werden nach dem Versand der Benachrichtigungen gesammelt verworfen
   und nicht in nachfolgende Ausführungen übernommen. In Umgebungen, in denen in kurzer Zeit große Mengen an Protokollen anfallen, erhöhen Sie
   bei Bedarf ``log.notification.search.size``.

Fehlerbehebung
==============

Benachrichtigungen werden nicht gesendet
----------------------------------------

1. **Aktivierung überprüfen**

   Überprüfen Sie in den **Allgemein**-Einstellungen der Verwaltungsoberfläche, ob **Log Notification** aktiviert ist.

2. **Benachrichtigungsziel überprüfen**

   Überprüfen Sie, ob mindestens ein Benachrichtigungsziel (eines von **Benachrichtigungs-E-Mail**, **Slack Webhook URLs** oder **Google Chat Webhook URLs**)
   konfiguriert ist. Ist keines konfiguriert, gibt der Job
   ``No notification targets configured.`` aus und sendet nichts.

3. **Mailserver-Einstellungen überprüfen**

   Überprüfen Sie bei Verwendung der E-Mail-Benachrichtigung in ``fess_env.properties``, ob der Mailserver korrekt
   konfiguriert ist.

4. **Geplanten Job überprüfen**

   Überprüfen Sie unter **System** → **Scheduler**, ob der Job **Log Notification** aktiviert ist.
   Ist dieser Job deaktiviert, werden keine Benachrichtigungen gesendet.

5. **Protokolle überprüfen**

   Überprüfen Sie in ``fess.log`` die Fehlermeldungen zur Benachrichtigung.

   ::

       grep -i "notification" /var/log/fess/fess.log

Zu viele Benachrichtigungen
---------------------------

1. **Protokollebene erhöhen**

   Ändern Sie die Benachrichtigungsebene von ``WARN`` auf ``ERROR``.

2. **Ursache beheben**

   Falls häufig Fehler auftreten, untersuchen Sie die eigentliche Ursache der Fehler.

Benachrichtigungsinhalt wird abgeschnitten
------------------------------------------

Passen Sie folgende Eigenschaften an.

- ``log.notification.max.details.length``: Maximale Zeichenanzahl des Detailbereichs
- ``log.notification.max.display.events``: Maximale Anzahl der anzuzeigenden Ereignisse
- ``log.notification.max.message.length``: Maximale Zeichenanzahl pro Nachricht

Referenzinformationen
=====================

- :doc:`admin-logging` - Protokollkonfiguration
- :doc:`setup-memory` - Speicherkonfiguration
