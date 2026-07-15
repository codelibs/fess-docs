=======================
Feldspezifische Suche
=======================

Feldspezifische Suche
=======================

Die von |Fess| gecrawlten Ergebnisse werden in einzelnen Feldern wie Titel oder Haupttext gespeichert. Durch die Angabe dieser Felder bei der Suche können Sie detaillierte Suchkriterien wie Dokumenttyp oder Größe festlegen.

Verfügbare Felder
-------------------

Standardmäßig können die folgenden Felder für die Suche angegeben werden.

.. list-table::
   :header-rows: 1

   * - Feldname
     - Beschreibung
     - Datentyp
   * - url
     - Gecrawlte URL
     - Keyword
   * - host
     - In der gecrawlten URL enthaltener Hostname
     - Keyword
   * - site
     - Zeichenkette aus der URL ohne Schema und Query-String (Hostname und Pfad). Die Suche erfolgt als Präfix-Suche (Anfangsübereinstimmung)
     - Keyword
   * - title
     - Titel
     - Text
   * - content
     - Haupttext
     - Text
   * - content_length
     - Größe des Dokuments (in Byte)
     - Numerisch
   * - last_modified
     - Datum und Uhrzeit der letzten Änderung des Dokuments
     - Datum
   * - timestamp
     - Datum und Uhrzeit der Registrierung des Dokuments (bzw. der Zeitpunkt des Crawlings, falls das letzte Änderungsdatum nicht ermittelt werden kann)
     - Datum
   * - mimetype
     - MIME-Typ des Dokuments (z. B. ``text/html``)
     - Keyword
   * - filetype
     - Aus dem MIME-Typ abgeleiteter Dateityp (z. B. ``html``, ``word``, ``pdf``; falls nicht zutreffend ``others``)
     - Keyword
   * - filename
     - Dateiname am Ende des URL-Pfads
     - Keyword
   * - label
     - Dem Dokument zugewiesener Label-Wert
     - Keyword
   * - lang
     - Sprachcode des Dokuments (z. B. ``ja``, ``en``)
     - Keyword
   * - anchor
     - Aus einer HTML-Seite extrahierte Ziel-URL eines Links (nur beim Web-Crawling)
     - Keyword
   * - click_count
     - Anzahl der Klicks auf das Dokument
     - Numerisch
   * - favorite_count
     - Anzahl der Favorisierungen des Dokuments
     - Numerisch

Tabelle: Liste der verfügbaren Felder

Der „Datentyp" gibt an, wie sich die Suchmethode je nach Feld unterscheidet.

* Keyword: Es wird eine exakte Übereinstimmung über den gesamten Wert durchgeführt. Kann auch mit Wildcard-Suche oder Präfix-Suche kombiniert werden.
* Text: Es wird eine Volltextsuche über die durch morphologische Analyse usw. zerlegten Wörter durchgeführt. Dies betrifft z. B. title und content.
* Numerisch/Datum: Die :doc:`Bereichssuche <search-range>` kann verwendet werden.

Wenn kein Feld angegeben wird, erfolgt die Suche über title und content. Je nach Konfiguration können auch weitere Felder als Suchziel hinzugefügt werden.

.. note::
    Je nach Crawling-Ziel werden manche Felder nicht mit einem Wert belegt. So wird anchor beispielsweise nur beim Web-Crawling registriert, und lang nur, wenn das HTML ein Sprachattribut enthält. Außerdem lassen sich Felder wie segment (eine Sitzungs-ID, die den jeweiligen Crawling-Lauf kennzeichnet) oder doc_id (eine vom System vergebene interne ID) angeben, diese werden jedoch bei der normalen Suche in der Regel nicht verwendet.

Wenn HTML-Dateien als Suchziel verwendet werden, wird das title-Tag im title-Feld und die Zeichenkette unter dem body-Tag im content-Feld registriert.

Verwendung
-----------

Um eine feldspezifische Suche durchzuführen, geben Sie "Feldname:Suchbegriff" in das Suchformular ein, wobei Feldname und Suchbegriff durch einen Doppelpunkt (:) getrennt sind.

Um nach fess im title-Feld zu suchen, geben Sie Folgendes ein:

::

    title:fess

Mit dieser Suche werden Dokumente als Suchergebnis angezeigt, die fess im title-Feld enthalten.

Um im url-Feld zu suchen, geben Sie Folgendes ein:

::

   url:https\:\/\/fess.codelibs.org\/ja\/15.8\/*
   url:"https://fess.codelibs.org/ja/15.8/*"

Da bei der ersten Variante Wildcard-Suche verwendet werden kann, ist auch eine Schreibweise wie ``url:*\/\/fess.codelibs.org\/*`` möglich. Da „:" und „/" in der URL Sonderzeichen der Suchabfrage sind, müssen sie mit ``\`` maskiert werden (siehe :doc:`special-char`). Bei der zweiten Variante kann keine Wildcard-Suche verwendet werden, aber ein Wort, das mit ``*`` endet, wird als Präfix-Suche (Anfangsübereinstimmung) behandelt.

.. tip::
    Wenn Sie nach einem Teil der URL suchen möchten, können Sie mit ``inurl:`` eine Teilübereinstimmungssuche für die URL durchführen. Beispielsweise sucht ``inurl:15.8`` nach Dokumenten, deren URL ``15.8`` enthält.

Wenn Sie Felder wie mimetype, filetype oder site angeben, deren Werte ein „/" enthalten, schließen Sie den Wert in Anführungszeichen ein, wie in ``mimetype:"text/html"``, oder maskieren Sie ihn wie in ``mimetype:text\/html``.

Zu verwandten Suchsyntaxen siehe auch die :doc:`Wildcard-Suche <search-wildcard>`, die :doc:`Bereichssuche <search-range>`, die :doc:`Sortierte Suche <search-sort>` und :doc:`Sonderzeichen <special-char>`.
