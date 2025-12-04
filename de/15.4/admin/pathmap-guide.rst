============
Pfad-Mapping
============

Übersicht
=========

Hier wird die Konfiguration des Pfad-Mappings erläutert.
Pfad-Mapping ist eine Funktion, die reguläre Ausdrücke verwendet, um URLs von Dokumenten zu transformieren, die von |Fess| gecrawlt wurden.
Zum Beispiel kann es verwendet werden, wenn Sie Dokumente von einem Dateiserver (Pfade, die mit ``file://`` beginnen) crawlen und diese über einen Webserver (``http://``) aus den Suchergebnissen zugänglich machen möchten.

Verwaltung
==========

Anzeige
-------

Um die Pfad-Mapping-Konfigurationsübersichtsseite zu öffnen, klicken Sie im linken Menü auf [Crawler > Pfad-Mapping].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Pfad-Mapping-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Regulärer Ausdruck
::::::::::::::::::

Geben Sie die zu ersetzende Zeichenkette an.
Die Beschreibungsmethode folgt regulären Java-Ausdrücken.

Ersetzung
:::::::::

Geben Sie die Zeichenkette an, durch die der übereinstimmende reguläre Ausdruck ersetzt werden soll.

Verarbeitungstyp
::::::::::::::::

Geben Sie den Zeitpunkt der Ersetzung an. Wählen Sie den geeigneten Typ entsprechend Ihrem Zweck.

Crawl
  Ersetzt die URL nach dem Abrufen des Dokuments beim Crawlen und vor der Indizierung.
  Die konvertierte URL wird im Index gespeichert.
  Verwenden Sie dies, wenn Sie Dateipfade in Web-Server-URLs konvertieren und im Index speichern möchten.

Anzeige
  Ersetzt die URL vor der Anzeige der Suchergebnisse und beim Klicken auf Suchergebnis-Links.
  Im Index gespeicherte URLs werden nicht geändert.
  Verwenden Sie dies, wenn Sie die Original-URL im Index behalten, aber beim Anzeigen der Suchergebnisse in eine andere URL konvertieren möchten.

Crawl/Anzeige
  Ersetzt die URL sowohl beim Crawlen als auch bei der Anzeige.
  Verwenden Sie dies, wenn Sie die gleiche Konvertierung zu beiden Zeitpunkten anwenden möchten.

Extrahierte URL-Konvertierung
  Ersetzt Link-URLs beim Extrahieren von Links aus HTML-Dokumenten.
  Nur mit dem Web-Crawler wirksam (nicht wirksam mit dem Datei-Crawler).
  Im Index gespeicherte URLs werden nicht geändert.
  Verwenden Sie dies, wenn Sie aus HTML extrahierte Link-URLs konvertieren und zur Crawl-Warteschlange hinzufügen möchten.

Anzeigereihenfolge
::::::::::::::::::

Sie können die Verarbeitungsreihenfolge des Pfad-Mappings angeben.
Wird in aufsteigender Reihenfolge verarbeitet.

Benutzer-Agent
::::::::::::::

Geben Sie dies an, wenn Sie Pfad-Mapping nur auf bestimmte Benutzer-Agenten anwenden möchten.
Das Matching erfolgt mittels regulärer Ausdrücke.
Wenn nicht gesetzt, gilt es für alle Anfragen.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Beispiele
=========

Dateiserver über Webserver zugreifen
------------------------------------

Dies ist eine Beispielkonfiguration zum Crawlen von Dokumenten von einem Dateiserver und zum Zugriff über einen Webserver aus den Suchergebnissen.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Wert
   * - Regulärer Ausdruck
     - ``file:/srv/documents/``
   * - Ersetzung
     - ``http://fileserver.example.com/documents/``
   * - Verarbeitungstyp
     - Crawl

Mit dieser Konfiguration werden URLs als ``http://fileserver.example.com/documents/...`` im Index gespeichert.

URL nur bei der Anzeige konvertieren
------------------------------------

Dies ist eine Beispielkonfiguration zum Beibehalten des ursprünglichen Dateipfads im Index und zum Konvertieren in eine Webserver-URL nur bei der Anzeige der Suchergebnisse.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Wert
   * - Regulärer Ausdruck
     - ``file:/srv/documents/``
   * - Ersetzung
     - ``http://fileserver.example.com/documents/``
   * - Verarbeitungstyp
     - Anzeige

Mit dieser Konfiguration werden URLs als ``file:/srv/documents/...`` im Index gespeichert und beim Klicken auf Suchergebnisse in ``http://...`` konvertiert.

Link-Konvertierung bei Server-Migration
---------------------------------------

Dies ist eine Beispielkonfiguration zum Konvertieren von Links in HTML von einem alten Server zu einem neuen Server beim Crawlen einer Website.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Wert
   * - Regulärer Ausdruck
     - ``http://old-server\\.example\\.com/``
   * - Ersetzung
     - ``http://new-server.example.com/``
   * - Verarbeitungstyp
     - Extrahierte URL-Konvertierung

Mit dieser Konfiguration werden aus HTML extrahierte Links konvertiert und zur Crawl-Warteschlange hinzugefügt.

Hinweise
========

Über extrahierte URL-Konvertierung
----------------------------------

Die extrahierte URL-Konvertierung ist nur mit dem Web-Crawler wirksam.
Sie wird beim Crawlen von Dateisystemen nicht angewendet.
Außerdem werden im Index gespeicherte URLs nicht geändert; es werden nur URLs konvertiert, die zur Crawl-Warteschlange hinzugefügt werden.

Über reguläre Ausdrücke
-----------------------

Reguläre Ausdrücke werden im Java-Format für reguläre Ausdrücke geschrieben.

* Rückverweise (``$1``, ``$2`` usw.) können verwendet werden
* Sonderzeichen müssen maskiert werden (z.B. ``.`` → ``\\.``)

Über die Sortierreihenfolge
---------------------------

Pfad-Mappings werden sequentiell in der konfigurierten Sortierreihenfolge (aufsteigend) angewendet.
Wenn mehrere Pfad-Mappings übereinstimmen, werden sie beginnend mit der ersten Übereinstimmung angewendet.

.. |image0| image:: ../../../resources/images/en/15.4/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/pathmap-2.png
