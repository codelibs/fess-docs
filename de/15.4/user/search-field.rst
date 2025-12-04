=======================
Feldspezifische Suche
=======================

Feldspezifische Suche
=======================

Die von |Fess| gecrawlten Ergebnisse werden in einzelnen Feldern wie Titel oder Haupttext gespeichert. Sie können nach diesen Feldern suchen. Durch die Angabe von Feldern können Sie detaillierte Suchkriterien wie Dokumenttyp oder Größe festlegen.

Verfügbare Felder
-------------------

Standardmäßig können die folgenden Felder für die Suche angegeben werden.

.. list-table::
   :header-rows: 1

   * - Feldname
     - Beschreibung
   * - url
     - Gecrawlte URL
   * - host
     - In der gecrawlten URL enthaltener Hostname
   * - title
     - Titel
   * - content
     - Haupttext
   * - content_length
     - Größe des gecrawlten Dokuments
   * - last_modified
     - Letztes Änderungsdatum und Uhrzeit des gecrawlten Dokuments
   * - mimetype
     - MIME-Typ des Dokuments

Tabelle: Liste der verfügbaren Felder


Wenn kein Feld angegeben ist, werden title und content als Suchziel verwendet.
Es ist auch möglich, Felder hinzuzufügen und als Suchziel festzulegen.

Wenn HTML-Dateien als Suchziel verwendet werden, wird das title-Tag im title-Feld und die Zeichenkette unter dem body-Tag im content-Feld registriert.

Verwendung
-----------

Um eine feldspezifische Suche durchzuführen, geben Sie "Feldname:Suchbegriff" in das Suchformular ein, wobei Feldname und Suchbegriff durch einen Doppelpunkt (:) getrennt sind.

Um nach fess im title-Feld zu suchen, geben Sie Folgendes ein:

::

    title:fess

Mit dieser Suche werden Dokumente angezeigt, die fess im title-Feld enthalten.

Um nach dem url-Feld zu suchen, geben Sie Folgendes ein:

::

   url:https\:\/\/fess.codelibs.org\/ja\/15.4\/*
   url:"https://fess.codelibs.org/ja/15.4/*"

Ersteres ermöglicht Wildcard-Abfragen, sodass Schreibweisen wie ``url:*\/\/fess.codelibs.org\/*`` möglich sind. ":" und "/" in der URL sind reservierte Zeichen und müssen maskiert werden. Letzteres erlaubt keine Wildcard-Abfragen, aber Präfix-Abfragen sind möglich.
