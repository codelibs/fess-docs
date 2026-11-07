==================
Crawl-Informationen
==================

Übersicht
=========

Die Crawl-Ausführungsergebnisse werden aufgezeichnet, und Crawl-Informationen können auf diesem Verwaltungsbildschirm überprüft werden.

Verwaltung
==========

Übersicht
=========

Jedes Mal, wenn ein Crawl ausgeführt wird, wird er als Crawl-Information aufgezeichnet.
In der Übersicht können Sie den Sitzungsnamen und die Ausführungszeit des durchgeführten Crawls überprüfen.
Um Details der Crawl-Informationen anzuzeigen, klicken Sie auf die entsprechende Crawl-Information.

|image0|

Laufende Crawls
===============

Solange Crawls laufen, wird oberhalb der Liste „Laufende Crawls" angezeigt. Für jede Crawl-Konfiguration (Web, Dateisystem oder Datenspeicher) gibt es eine Zeile mit den folgenden Angaben.

- Crawl-Konfiguration: Der Name der Crawl-Konfiguration.
- Verarbeitete Dokumente: Die Anzahl der Dokumente, die der laufende Crawl bisher verarbeitet hat. Bei Web- und Dateisystem-Crawls ist das die Anzahl der Zugriffsergebnisse, bei Datenspeicher-Crawls die Anzahl der für die Crawl-Konfiguration indexierten Dokumente.
- Fortschritt: Die verarbeiteten Dokumente in Prozent der Dokumentanzahl des vorherigen abgeschlossenen Crawls. Bis zum Abschluss des Crawls beträgt der Wert höchstens 99 %. Gibt es keinen vorherigen abgeschlossenen Crawl (z. B. beim ersten Crawl), lässt sich kein Prozentwert berechnen; dann wird ``-`` angezeigt und nur die Anzahl genannt.

Hinweise:

- Der Block zeigt den Stand beim Öffnen der Seite. Laden Sie die Seite neu, um die aktuellen Werte zu sehen.
- Ein abgeschlossener Crawl ist beim nächsten Öffnen der Seite nicht mehr im Block. Ein gestoppter Crawl (oder einer, bei dem der Crawler aufhört, ohne das zu vermerken, etwa weil der Prozess beendet wird) verschwindet innerhalb von etwa 30 Sekunden (Standard) nach der letzten Aktualisierung; nach dem Stoppen kann er also noch kurz angezeigt werden. Ein gestoppter oder fehlgeschlagener Crawl lässt die Dokumentanzahl des vorherigen abgeschlossenen Crawls unverändert, ebenso ein Crawl, der ohne ein verarbeitetes Dokument abgeschlossen wird.
- Der Fortschrittsstatus wird vom System im Feld ``metadata`` der Crawl-Konfiguration gespeichert. Er kann in der Verwaltungsoberfläche und über die Admin-API nicht bearbeitet werden.
- Dieselben Informationen sind über die Admin-API abrufbar (siehe :doc:`../api/admin/api-admin-crawlinginfo`).

Details
=======

Durch Klicken auf die Sitzungs-ID der Crawl-Informationen in der Übersicht werden die Details der entsprechenden Crawl-Informationen angezeigt.

|image1|

Parameterliste
--------------

Sitzungs-ID
:::::::::::

Die Sitzungs-ID bei der Crawl-Ausführung.

Crawler-Startzeit
:::::::::::::::::

Die Uhrzeit, zu der der gesamte Crawl gestartet wurde.

Crawl-Startzeit (Web/Datei)
:::::::::::::::::::::::::::

Die Uhrzeit, zu der das Web- und Dateisystem-Crawling gestartet wurde.

Crawl-Startzeit (Datenspeicher)
::::::::::::::::::::::::::::::::

Die Uhrzeit, zu der das Datenspeicher-Crawling gestartet wurde.

Crawl-Endzeit (Web/Datei)
:::::::::::::::::::::::::

Die Uhrzeit, zu der das Web- und Dateisystem-Crawling beendet wurde.

Crawl-Ausführungszeit (Datenspeicher)
::::::::::::::::::::::::::::::::::::::

Die Ausführungszeit des Datenspeicher-Crawlings (in Millisekunden).

Indizierungs-Ausführungszeit (Datenspeicher)
:::::::::::::::::::::::::::::::::::::::::::::

Die Zeit, die für die Indizierung der Web- und Dateisystem-Crawl-Ergebnisse benötigt wurde (in Millisekunden).

Indexgröße (Datenspeicher)
::::::::::::::::::::::::::

Die Anzahl der indizierten Dokumente.

Crawl-Endzeit (Datenspeicher)
::::::::::::::::::::::::::::::

Die Uhrzeit, zu der das Datenspeicher-Crawling beendet wurde.

Crawler-Status
::::::::::::::

Ob der Crawl erfolgreich war oder nicht.

Crawler-Endzeit
:::::::::::::::

Die Uhrzeit, zu der der gesamte Crawl beendet wurde.

Crawler-Ausführungszeit
:::::::::::::::::::::::

Die Ausführungszeit des gesamten Crawls (in Millisekunden).

.. |image0| image:: ../../../resources/images/en/15.10/admin/crawlinginfo-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/crawlinginfo-2.png
