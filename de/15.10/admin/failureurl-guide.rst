=========
Fehler-URLs
=========

Übersicht
=========

Hier werden Fehler-URLs erläutert.
URLs, die beim Crawlen nicht abgerufen werden konnten, werden aufgezeichnet und können als Fehler-URLs überprüft werden.

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite zur Überprüfung von Fehler-URLs zu öffnen, klicken Sie im linken Menü auf [Systeminformationen > Fehler-URL].

|image0|

Klicken Sie auf den Bestätigungslink der Fehler-URL, um Details anzuzeigen.

Angezeigte Spalten
------------------

Die Liste zeigt URL, Typ, MIME-Typ, HTTP-Status, Größe (Bytes) und letzte Zugriffszeit.

MIME-Typ, HTTP-Status und Größe werden nur aufgezeichnet, wenn der Crawler sie kannte; andernfalls bleiben sie leer.

- Aufgezeichnet bei: Verarbeitung nach dem Abruf des Dokuments fehlgeschlagen (z. B. Textextraktion fehlgeschlagen oder Größenlimit überschritten) oder der Server hat einen HTTP-Status geliefert, der in ``crawler.failure.url.status.codes`` aufgeführt ist. Wird ein Dokument abgelehnt, weil es vor dem Abruf ein Größenlimit überschreitet, wird nur die Größe aufgezeichnet.
- Nicht aufgezeichnet bei: keine Antwort erhalten, etwa bei Zeitüberschreitung oder Verbindungsfehler, sowie bei Fehlern von Datenspeicher-Crawls.
- Der HTTP-Status wird nur für ``http``-/``https``-URLs aufgezeichnet. Für Dateien, SMB und andere Protokolle bleibt er leer.
- Bei einer Fehler-URL, die vor |Fess| 15.10 aufgezeichnet wurde, bleiben diese Angaben leer, bis die URL erneut fehlschlägt.

CSV-Download
------------

Mit der Schaltfläche [CSV herunterladen] in der Liste laden Sie die Fehler-URLs, die den im Suchformular eingegebenen Bedingungen (URL, Fehleranzahl und Typ) entsprechen, als CSV-Datei herunter. Der Dateiname lautet ``failureurl_yyyyMMddHHmmss.csv``.

- Die erste Zeile enthält die Spaltennamen in dieser Reihenfolge: ``url``, ``errorName``, ``errorCount``, ``lastAccessTime``, ``httpStatusCode``, ``mimeType`` und ``contentLength``. Das Protokoll (Stacktrace) ist nicht enthalten.
- Alle passenden Zeilen werden geschrieben, die mit der neuesten letzten Zugriffszeit zuerst. Die Seitenaufteilung gilt nicht, und die Zeilenzahl ist nicht begrenzt.
- ``lastAccessTime`` steht im ISO-8601-Format in UTC (z. B. ``2026-01-01T00:00:00.000Z``).
- Die Zeichenkodierung folgt „CSV-Dateikodierung" unter [System > Allgemein]; eine UTF-8-Datei beginnt mit einer Byte-Order-Mark.
- Damit eine Tabellenkalkulation einen Wert nicht als Formel ausführt, wird einem Wert, der mit ``=``, ``+``, ``-``, ``@``, einem Tabulator oder einem Wagenrücklauf beginnt, ein ``'`` vorangestellt.

Fehler-URL-Details
==================

In den Fehler-URL-Details werden beim Crawlen aufgetretene Ausnahmen aufgezeichnet.

|image1|

Detailinhalt
------------

URL
:::

Die URL, bei der die Ausnahme aufgetreten ist.

Thread-Name
:::::::::::

Der Name des Threads, der den Crawl ausgeführt hat.
Kann beim Überprüfen von Protokolldateien verwendet werden.

Typ
:::

Der Typ der Ausnahme.

HTTP-Status
:::::::::::

Der HTTP-Status der Antwort für das Dokument. Wird nur für ``http``-/``https``-URLs aufgezeichnet, und nur wenn der Crawler ihn kannte.

MIME-Typ
::::::::

Der MIME-Typ des Dokuments. Wird nur aufgezeichnet, wenn der Crawler ihn kannte.

Größe (Bytes)
:::::::::::::

Die Größe des Dokuments. Wird nur aufgezeichnet, wenn der Crawler sie kannte.

Protokoll
:::::::::

Der Inhalt der Ausnahme.

Fehleranzahl
::::::::::::

Die Anzahl, wie oft diese Ausnahme aufgetreten ist.

Letzte Zugriffszeit
:::::::::::::::::::

Die Uhrzeit, zu der diese Ausnahme aufgetreten ist.


.. |image0| image:: ../../../resources/images/en/15.10/admin/failureurl-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/failureurl-2.png
