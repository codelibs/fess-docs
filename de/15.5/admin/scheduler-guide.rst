=========
Scheduler
=========

Übersicht
=========

Hier wird die Konfiguration des Job-Schedulers erläutert.

Verwaltung
==========

Anzeige
-------

Um die Job-Scheduler-Konfigurationsübersichtsseite zu öffnen, klicken Sie im linken Menü auf [System > Scheduler].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Scheduler-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Der in der Übersicht angezeigte Name.

Ziel
::::

Das Ziel kann als Kennung verwendet werden, um zu bestimmen, ob ein Job ausgeführt werden soll, wenn er direkt über einen Batch-Befehl ausgeführt wird.
Wenn Sie das Crawling nicht per Befehl ausführen, geben Sie „all" an.

Zeitplan
::::::::

Konfigurieren Sie den Zeitplan.
Der hier konfigurierte Zeitplan führt den im Skript beschriebenen Job aus.

Das Beschreibungsformat ist das CRON-Format in der Form „Minute Stunde Tag Monat Wochentag".
Zum Beispiel führt „0 12 \* \* 3" den Job jeden Mittwoch um 12:00 Uhr aus.

Ausführungsmethode
::::::::::::::::::

Geben Sie die Skriptausführungsumgebung an.
Derzeit wird nur „groovy" unterstützt.

Skript
::::::

Beschreiben Sie den Ausführungsinhalt des Jobs in der unter „Ausführungsmethode" angegebenen Sprache.

Um beispielsweise nur drei Crawl-Konfigurationen als Crawl-Job auszuführen, schreiben Sie Folgendes (vorausgesetzt, die Web-Crawl-Konfigurations-IDs sind 1 und 2 und die Dateisystem-Crawl-Konfigurations-ID ist 1):

::

    return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"] as String[]).fileConfigIds(["1"] as String[]).dataConfigIds([] as String[]).execute(executor);

Protokollierung
:::::::::::::::

Durch Aktivierung wird der Vorgang im Jobprotokoll aufgezeichnet.

Crawler-Job
:::::::::::

Durch Aktivierung wird er als Crawler-Job behandelt.
Durch Konfiguration von job.max.crawler.processes in fess_config.properties können Sie verhindern, dass mehr Crawler als erforderlich gestartet werden.
Standardmäßig gibt es keine Begrenzung für die Anzahl der Crawler-Starts.

Status
::::::

Geben Sie den aktiven/inaktiven Status des Jobs an.
Wenn deaktiviert, wird der Job nicht ausgeführt.

Anzeigereihenfolge
::::::::::::::::::

Geben Sie die Anzeigereihenfolge in der Job-Übersicht an.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Manuelles Crawlen
=================

Klicken Sie unter „Scheduler" auf „Default Crawler" und dann auf die Schaltfläche „Jetzt starten".
Um den Crawler zu stoppen, klicken Sie auf „Default Crawler" und dann auf die Schaltfläche „Stoppen".

.. |image0| image:: ../../../resources/images/en/15.5/admin/scheduler-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/scheduler-2.png
