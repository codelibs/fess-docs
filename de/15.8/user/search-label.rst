====================
Label-basierte Suche
====================

Label-basierte Suche (Kategoriesuche)
=====================================

Durch Hinzufügen von Label-Informationen zur Kategorisierung der zu durchsuchenden Dokumente ist es möglich, bei der Suche eine nach Labeln gefilterte Suche durchzuführen. Mithilfe von Labeln können Sie den Suchbereich beispielsweise auf Abteilungen, Websites oder Dokumenttypen eingrenzen.

Wenn Labels vorab in der Verwaltungsoberfläche registriert werden, kann die Filterung nach Labeln im Suchbildschirm verwendet werden. Die verfügbaren Labels können bei der Suche über ein Dropdown-Menü in Mehrfachauswahl ausgewählt werden. Werden mehrere Labels ausgewählt, umfasst die Suche Dokumente, denen mindestens eines der ausgewählten Labels zugewiesen ist. Wenn keine Labels registriert sind, wird das Label-Dropdown-Feld nicht angezeigt.

.. note::
    Da für Labels Berechtigungen festgelegt werden können, werden im Dropdown-Menü nur die Labels angezeigt, auf die der suchende Benutzer Zugriff hat. Außerdem können die angezeigten Labels je nach virtuellem Host oder Locale (Sprache) unterschiedlich sein. Daher werden registrierte Labels je nach Benutzer unter Umständen nicht im Dropdown-Menü angezeigt.

Labels werden definiert, indem die Ziele, denen ein Label zugewiesen werden soll, über einen regulären Ausdruck für den URL-Pfad angegeben werden. Informationen zur Registrierung von Labels und zu den Konfigurationselementen finden Sie in der :doc:`Label-Verwaltungsanleitung <../admin/labeltype-guide>`.

Verwendung
----------

Bei der Suche können Sie Label-Informationen auswählen. Die Label-Informationen können in den Suchoptionen ausgewählt werden, die durch Klicken auf die Schaltfläche „Optionen" angezeigt werden.

|image0|

Indem Sie Labels festlegen und einen Index erstellen, können Sie nach Dokumenten suchen, denen jeweils ein Label zugewiesen wurde. Eine Suche ohne Angabe eines Labels entspricht wie gewohnt einer Suche über alle Dokumente.

Die Zuweisung von Labels zu Dokumenten erfolgt beim Crawlen und Erstellen des Index, indem die URL des Dokuments mit den für das Label konfigurierten Pfaden abgeglichen wird. Wenn Sie daher die Label-Definition (Zielpfade oder ausgeschlossene Pfade) hinzufügen oder ändern, wirkt sich dies nicht automatisch auf bereits indexierte Dokumente aus. Um die Änderungen zu übernehmen, crawlen Sie die betreffenden Dokumente erneut, oder aktualisieren Sie den Index, indem Sie den im Scheduler registrierten Job „Label Updater" ausführen.

.. |image0| image:: ../../../resources/images/en/15.8/user/search-label-1.png
.. pdf   :width: 300 px
