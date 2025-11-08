============
Pfad-Mapping
============

Übersicht
=========

Hier wird die Konfiguration des Pfad-Mappings erläutert.
Pfad-Mapping kann verwendet werden, wenn Sie Links ersetzen möchten, die in Suchergebnissen angezeigt werden.

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

Geben Sie den Zeitpunkt der Ersetzung an.

* Crawl: Ersetzt die URL nach dem Abrufen des Dokuments beim Crawlen und vor der Indizierung.
* Anzeige: Ersetzt die URL bei der Suche vor der Anzeige.
* Crawl/Anzeige: Ersetzt die URL sowohl beim Crawlen als auch bei der Anzeige.
* Gespeicherte URL: Ersetzt die URL beim Crawlen vor dem Abrufen des Dokuments.

Anzeigereihenfolge
::::::::::::::::::

Sie können die Verarbeitungsreihenfolge des Pfad-Mappings angeben.
Wird in aufsteigender Reihenfolge verarbeitet.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

.. |image0| image:: ../../../resources/images/en/15.3/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/15.3/admin/pathmap-2.png
