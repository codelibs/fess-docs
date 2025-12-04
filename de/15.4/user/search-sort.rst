==================
Sortierte Suche
==================

Sie können Suchergebnisse nach Feldern wie dem Suchdatum sortieren.

Sortierbare Felder
--------------------

Standardmäßig können die folgenden Felder zum Sortieren angegeben werden.

.. list-table::
   :header-rows: 1

   * - Feldname
     - Beschreibung
   * - created
     - Crawl-Datum und Uhrzeit
   * - content_length
     - Größe des gecrawlten Dokuments
   * - last_modified
     - Letztes Änderungsdatum und Uhrzeit des gecrawlten Dokuments
   * - filename
     - Dateiname
   * - score
     - Bewertung
   * - timestamp
     - Datum und Uhrzeit der Dokumentindizierung
   * - click_count
     - Anzahl der Klicks auf das Dokument
   * - favorite_count
     - Anzahl der Favorisierungen des Dokuments

Tabelle: Liste der sortierbaren Felder


Durch Anpassung können Sie auch eigene Felder als Sortierziel hinzufügen.

Verwendung
-----------

Bei der Suche können Sortierkriterien ausgewählt werden. Sortierkriterien können im Suchoptionen-Dialog ausgewählt werden, der durch Klicken auf die Optionsschaltfläche angezeigt wird.

|image0|

Um im Suchfeld zu sortieren, geben Sie "sort:Feldname" in das Suchformular ein, wobei sort und Feldname durch einen Doppelpunkt (:) getrennt sind.

Das Folgende sucht nach fess und sortiert nach Dokumentgröße in aufsteigender Reihenfolge.

::

    fess sort:content_length

Um in absteigender Reihenfolge zu sortieren, geben Sie Folgendes ein:

::

    fess sort:content_length.desc

Um nach mehreren Feldern zu sortieren, geben Sie diese durch Kommas getrennt an:

::

    fess sort:content_length.desc,last_modified

.. |image0| image:: ../../../resources/images/en/15.4/user/search-sort-1.png
.. pdf            :width: 300 px
