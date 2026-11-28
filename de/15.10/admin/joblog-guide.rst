=========
Jobprotokoll
=========

Übersicht
=========

Zeigt die Ergebnisse ausgeführter Jobs als Liste an.

Verwaltung
==========

Anzeige
-------

Um die Jobprotokoll-Überprüfungsseite zu öffnen, klicken Sie im linken Menü auf [Systeminformationen > Jobprotokoll].

|image0|

Die Übersicht zeigt Jobname, Ausführungsstatus sowie Start- und Endzeit.
Klicken Sie unter der Liste auf die Schaltfläche „Alle löschen", um alle Jobprotokolle zu löschen. Es wird ein Bestätigungsdialog angezeigt.

Jobprotokoll-Details
--------------------

Sie können den Protokollinhalt des Jobs überprüfen. Es werden Jobname, Status, Start-/Abschlusszeit, Ergebnis usw. angezeigt.

|image1|

Name
::::

Der Name des ausgeführten Jobs.

Status
::::::

Das Ausführungsergebnis des Jobs.

.. note::
   Ein Crawl-Job mit dem Status OK (``ok``) hat nicht unbedingt jedes Dokument in den Index aufgenommen. Der Status gibt an, ob der Crawler-Prozess normal beendet wurde. Ein Dokument, dessen Schreiben die Suchmaschine ablehnt, wird nicht indexiert, und der Job kann trotzdem mit OK enden. Ein abgelehntes Dokument wird in ``fess-crawler.log`` mit einer Warnung wie ``Failed to index a document`` protokolliert. Bei Web- und Datei-Crawls wird es nicht als Fehler-URL erfasst. Prüfen Sie zusätzlich die Anzahl der Dokumente im Index (siehe "Dokumentanzahl im Index und Aktualität des Crawls" in :doc:`../config/admin-logging`).

Ziel
::::

Das Ziel, für das der Job ausgeführt wird.

Startzeit
:::::::::

Datum und Uhrzeit, zu der der Job gestartet wurde.

Endzeit
:::::::

Datum und Uhrzeit, zu der der Job beendet wurde.

Ausführungsmethode
::::::::::::::::::

Die Ausführungsumgebung, in der der Job ausgeführt wurde.

Skript
::::::

Der Ausführungsinhalt des Jobs.

Ergebnis
::::::::

Das Ausführungsergebnis des Jobs.

Klicken Sie auf der Detailseite auf die Schaltfläche „Löschen", um das Jobprotokoll zu löschen. Es wird ein Bestätigungsdialog angezeigt.

.. |image0| image:: ../../../resources/images/de/15.10/admin/joblog-1.png
.. |image1| image:: ../../../resources/images/de/15.10/admin/joblog-2.png
