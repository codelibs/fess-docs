==================
Dokument-Boosting
==================

Übersicht
=========

Hier wird die Konfiguration für Dokument-Boosting erläutert.
Durch die Konfiguration von Dokument-Boosting können Sie Dokumente unabhängig vom Suchbegriff in den Suchergebnissen höher positionieren.

Verwaltung
==========

Anzeige
-------

Um die Konfigurationsübersichtsseite für Dokument-Boosting zu öffnen, klicken Sie im linken Menü auf [Crawler > Dokument-Boost].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Konfigurationsseite für Dokument-Boosting zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Bedingung
:::::::::

Geben Sie die Bedingung für Dokumente an, die höher positioniert werden sollen.
Wenn Sie beispielsweise URLs mit https://www.n2sm.net/ höher anzeigen möchten, schreiben Sie url.matches("https://www.n2sm.net/.\*").
Bedingungen werden in der Syntax der unter „Skripttyp" angegebenen Skript-Engine geschrieben.

Boost-Ausdruck
::::::::::::::

Geben Sie den Gewichtungswert für das Dokument an.
Ausdrücke werden in der Syntax der unter „Skripttyp" angegebenen Skript-Engine geschrieben.

Skripttyp
:::::::::

Geben Sie die Skript-Engine an, mit der die Bedingung und der Boost-Ausdruck ausgewertet werden.
Neue Konfigurationen sind mit ``javascript`` vorausgefüllt. Für ``groovy`` ist das Plugin
``fess-script-groovy`` erforderlich. Bleibt das Feld leer, werden die Ausdrücke als Groovy ausgewertet.

Sortierreihenfolge
::::::::::::::::::

Legen Sie die Sortierreihenfolge für das Dokument-Boosting fest.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt. Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.


.. |image0| image:: ../../../resources/images/en/15.9/admin/boostdoc-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/boostdoc-2.png
