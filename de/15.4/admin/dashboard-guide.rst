===========
Dashboard
===========

Übersicht
=========

Das Dashboard bietet ein Web-Verwaltungstool zur Verwaltung der OpenSearch-Cluster und -Indizes, auf die |Fess| zugreift.

|image0|

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table:: Von |Fess| verwaltete Indizes
   :header-rows: 1

   * - Indexname
     - Beschreibung
   * - fess.YYYYMMDD
     - Indizierte Dokumente
   * - fess_log
     - Zugriffsprotokolle
   * - fess.suggest.YYYYMMDD
     - Vorschlagswörter
   * - fess_config
     - |Fess| Konfiguration
   * - fess_user
     - Benutzer-/Rollen-/Gruppendaten
   * - configsync
     - Wörterbuchkonfiguration
   * - fess_suggest
     - Vorschlags-Metadaten
   * - fess_suggest_array
     - Vorschlags-Metadaten
   * - fess_suggest_badword
     - Liste unerwünschter Vorschlagswörter
   * - fess_suggest_analyzer
     - Vorschlags-Metadaten
   * - fess_crawler
     - Crawl-Informationen


Indexnamen, die mit einem Punkt (.) beginnen, sind Systemindizes und werden daher nicht angezeigt.
Um Systemindizes anzuzeigen, aktivieren Sie das Kontrollkästchen „special".

Anzahl indizierter Dokumente überprüfen
========================================

Die Anzahl der indizierten Dokumente wird wie in der Abbildung unten im Fess-Index angezeigt.

|image1|

Wenn Sie auf das Symbol oben rechts in jedem Index klicken, wird ein Operationsmenü für den Index angezeigt.
Um indizierte Dokumente zu löschen, löschen Sie sie über den Verwaltungssuchbildschirm. Achten Sie darauf, NICHT „delete index" zu verwenden.

.. |image0| image:: ../../../resources/images/en/15.4/admin/dashboard-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/dashboard-2.png
.. pdf            :width: 400 px
