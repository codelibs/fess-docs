==================
Protwords-Wörterbuch
==================

Übersicht
=========

Sie können Wörter verwalten, die von der Stemming-Verarbeitung ausgeschlossen werden sollen.
Da die Stemming-Verarbeitung grundsätzlich regelbasiert ist, kann eine unbeabsichtigte Normalisierung auftreten.
Beispielsweise wird das Wort Maine (Name eines US-Bundesstaates) zu main normalisiert.

Damit dieses Wort unverändert durchsuchbar bleibt, registrieren Sie ``maine`` (Wörter werden in Kleinbuchstaben geschrieben; Einzelheiten siehe „Konfigurationsparameter").

Die Liste zeigt je Sprache ein Wörterbuch (``en/protwords.txt``, ``de/protwords.txt`` usw.). Wählen Sie das Wörterbuch aus, das zur Sprache des Wortes passt, und bearbeiten Sie es. Welches Wörterbuch auf welche Felder wirkt, steht unter :doc:`dict-guide`.
Das Speichern allein wirkt sich noch nicht auf die Suche aus. Wie Sie eine Änderung übernehmen, steht unter :ref:`dict-apply-changes`.

Verwaltung
==========

Anzeige
-------

Um die Protwords-Konfigurationsübersichtsseite zu öffnen, wählen Sie im linken Menü [System > Wörterbuch] aus und klicken Sie dann auf protwords.

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfigurationsmethode
---------------------

Um die Protwords-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Wortinformation
:::::::::::::::

Geben Sie Wörter ein, die von der Stemming-Verarbeitung ausgeschlossen werden sollen.

Geben Sie die Wörter in Kleinbuchstaben ein. Die Analyse wandelt ein Wort in Kleinbuchstaben um, bevor sie es mit diesem Wörterbuch abgleicht; die Eingabe von ``Maine`` schützt das Wort daher nicht. Im Beispiel der Übersicht geben Sie ``maine`` ein.


Download
========

Sie können im Protwords-Wörterbuchformat herunterladen.

Upload
======

Sie können im Protwords-Wörterbuchformat hochladen.

.. warning::

   Beim Hochladen wird der Inhalt des Wörterbuchs durch den Inhalt der hochgeladenen Datei ersetzt. Wörter, die nicht in der Datei stehen, werden entfernt, auch solche, die über die Oberfläche registriert wurden. Laden Sie das Wörterbuch bei Bedarf zuerst herunter und nehmen Sie dessen Inhalt in die hochzuladende Datei auf.


.. |image0| image:: ../../../resources/images/en/15.9/admin/protwords-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/protwords-2.png
