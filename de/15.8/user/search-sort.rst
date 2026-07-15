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


Sie können auch eigene Felder als Sortierziel hinzufügen. Geben Sie dazu in ``query.additional.sort.fields`` in ``fess_config.properties`` die gewünschten Feldnamen durch Kommas getrennt an (der Standardwert ist leer). Die hier angegebenen Felder werden zu den oben genannten Standardfeldern hinzugefügt und stehen dann zur Sortierung zur Verfügung. Zu beachten ist, dass die als Sortierziel vorgesehenen Felder zuvor im Index registriert sein müssen.

Verwendung
-----------

Bei der Suche können Sortierkriterien ausgewählt werden. Sortierkriterien können im Suchoptionen-Dialog ausgewählt werden, der durch Klicken auf die Optionsschaltfläche angezeigt wird.

|image0|

Um im Suchfeld zu sortieren, geben Sie "sort:Feldname" in das Suchformular ein, wobei sort und Feldname durch einen Doppelpunkt (:) getrennt sind.

Das Folgende sucht nach fess und sortiert nach Dokumentgröße in aufsteigender Reihenfolge.

::

    fess sort:content_length

Um in absteigender Reihenfolge zu sortieren, fügen Sie ``.desc`` hinter dem Feldnamen an.

::

    fess sort:content_length.desc

Als Suffix nach dem Feldnamen kann ``.asc`` (aufsteigend) oder ``.desc`` (absteigend) angegeben werden; wird es weggelassen, wird aufsteigend sortiert.

Um nach mehreren Feldern zu sortieren, geben Sie diese wie folgt durch Kommas (,) getrennt an. Das zuerst angegebene Feld hat Vorrang, und Dokumente mit demselben Wert für dieses Feld werden anhand des nächsten Feldes sortiert.

::

    fess sort:content_length.desc,last_modified

.. note::
   Wenn Sie einen Feldnamen angeben, der nicht in der Liste der sortierbaren Felder enthalten ist, oder eine andere Sortierreihenfolge als ``asc`` oder ``desc``, führt die Suche zu einem Fehler.

.. |image0| image:: ../../../resources/images/en/15.8/user/search-sort-1.png
.. pdf            :width: 300 px
