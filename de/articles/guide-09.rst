===================================================
Dokumente in Japanisch, Englisch, Chinesisch suchen
===================================================

Einleitung
==========

Wenn japanische Besprechungsprotokolle, englische technische Spezifikationen und chinesische Marktberichte nebeneinander auf demselben Dateiserver oder derselben Intranet-Site liegen, hört man bald Aussagen wie „Englische Dokumente werden gefunden, aber japanische Beugungsformen treffen nicht“, „Ich möchte nur die chinesischen Dokumente durchsuchen“ oder „Ich möchte englischsprachige Unterlagen mit japanischen Begriffen finden“.

Fess kann Dokumente in jeder Sprache ohne besondere Konfiguration durchsuchen.
Wenn Sie jedoch Wörterbucheinträge hinzufügen, ohne zu wissen, wo welche Sprachanalyse greift, ändern sich die Ergebnisse nicht.
Dieser Artikel erklärt anhand der tatsächlichen Werte in den Konfigurationsdateien, wie Fess 15.9 mehrsprachige Dokumente indexiert und durchsucht.
Darauf aufbauend können Sie anschließend Folgendes tun:

- Die für jedes Dokument erkannte Sprache prüfen und die Suche mit ``lang:`` auf eine Sprache eingrenzen
- Mit ``query.default.languages`` und verwandten Einstellungen festlegen, welche Sprachanalyse bei der Suche verwendet wird
- Wörterbücher (Synonyme, Kuromoji, Stoppwörter usw.) passend zu den Feldern bearbeiten, auf die sie wirken, und die Änderungen übernehmen
- Anhand der Suchergebnisse und der ``_analyze``-API bestätigen, dass eine Änderung wirkt

Wie Sie Verbesserungen anhand von Suchprotokollen vorantreiben, behandelt :doc:`guide-08`.

So funktioniert die Indexierung: gemeinsame und sprachspezifische Felder
========================================================================

Im Fess-Index werden Fließtext und Titel in zwei Formen gespeichert.
Definiert ist dies in den mit Fess ausgelieferten Dateien ``fess_indices/fess.json`` (Analyzer) und ``fess_indices/fess/doc.json`` (Mapping).

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - Feld
     - Analyzer
     - Art der Analyse
   * - ``content``, ``title``, ``important_content``
     - ``standard_analyzer`` (bei der Suche ``standard_search_analyzer``)
     - Gemeinsam für alle Dokumente. Kanji, Hiragana, Katakana und Hangul werden in Einheiten von je zwei Zeichen (Bi-Gramme) zerlegt; außerdem werden englische Stoppwörter entfernt und Stemming angewendet. Synonyme werden nur bei der Suche expandiert
   * - ``content_ja``, ``title_ja`` usw.
     - ``japanese_analyzer``
     - Morphologische Analyse mit Kuromoji. Verben und andere Wörter werden auf ihre Grundform zurückgeführt; Partikeln, Hilfsverben und Symbole werden entfernt
   * - ``content_en``, ``title_en`` usw.
     - ``english_analyzer``
     - Entfernung englischer Stoppwörter und Stemming
   * - ``content_zh-cn``, ``title_zh-cn`` usw.
     - ``simplified_chinese_analyzer``
     - Zerlegt den Text mit einem Tokenizer für Chinesisch in Wörter
   * - ``content_zh-tw``, ``title_zh-tw`` usw.
     - ``traditional_chinese_analyzer``
     - Wandelt traditionelle in vereinfachte Schriftzeichen um und zerlegt den Text dann mit demselben Tokenizer wie bei vereinfachtem Chinesisch

Die gemeinsamen Felder hat jedes Dokument.
Sprachspezifische Felder werden nur angelegt, wenn die Sprache des Dokuments bestimmt wurde.
Bei der Indexierung wird der Sprachcode in das Feld ``lang`` geschrieben, und die Werte von ``content``, ``important_content`` und ``title`` (``indexer.language.fields``) werden in Felder der Form ``<Feld>_<Sprache>`` wie ``content_ja`` kopiert.
Einem Dokument wird genau eine Sprache zugeordnet.

Wie die Sprache eines Dokuments bestimmt wird
---------------------------------------------

``lang`` wird in der folgenden Reihenfolge bestimmt.

1. Bei HTML aus einem Web-Crawl wird der Wert von ``<html lang="...">`` verwendet (``crawler.document.html.lang.xpath=//HTML/@lang``). Wenn Sie in den „Konfigurationsparameter“ einer Crawl-Konfiguration ``field.xpath.default.lang=<XPath>`` eintragen, ändern Sie nur für diese Konfiguration, woher der Wert gelesen wird
2. Bei Dokumenten, deren Sprache durch Schritt 1 nicht feststeht, wird sie automatisch aus dem Text erkannt. Dabei werden die ersten 1000 Zeichen (``indexer.language.detect.length``) von ``content``, ``important_content`` und ``title`` in dieser Reihenfolge ausgewertet. Bei Datei-Crawls wird nur der extrahierte Fließtext herangezogen
3. Wenn die erkannte Sprache nicht in ``supported.languages`` enthalten ist oder sich keine Sprache erkennen lässt, wird kein ``lang`` gesetzt und es werden keine sprachspezifischen Felder angelegt

Werte wie ``ja-JP`` oder ``zh_CN`` werden einheitlich in Kleinbuchstaben mit Bindestrich (``ja``, ``zh-cn``) gespeichert.

Auch Dokumente aus Datenspeichern durchlaufen bei der Indexierung dieselbe automatische Erkennung.
Setzt ein Skript ``lang`` auf eine in ``supported.languages`` enthaltene Sprache (etwa ``ja``), hat dieser Wert Vorrang vor der automatischen Erkennung.

So funktioniert die Suche: welche Sprachfelder durchsucht werden
================================================================

Suchbegriffe werden immer in den gemeinsamen Feldern gesucht.
Zusätzlich werden für jede „Suchsprache“, die bei jeder Suche ermittelt wird, die entsprechenden sprachspezifischen Felder in die Suchbedingung aufgenommen.
Die Bedingungen der einzelnen Felder sind mit OR verknüpft (``should`` einer ``bool``-Abfrage); ein Dokument erscheint also im Ergebnis, sobald es in einem beliebigen Feld übereinstimmt.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Feld
     - Konfigurationsschlüssel
     - Standardwert
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<Suchsprache>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<Suchsprache>``
     - ``query.boost.content.lang``
     - ``0.1``

Die Suchsprachen werden aus der ersten der folgenden Quellen übernommen, die einen Wert hat.

1. ``query.default.languages`` in ``fess_config.properties`` (standardmäßig leer). Ist ein Wert gesetzt, werden alle anderen Angaben ignoriert
2. Der Parameter ``lang`` der Anfrage: die Sprache, die auf der Suchseite unter [Optionen] > „Bevorzugte Sprache“ oder in der erweiterten Suche unter „Bevorzugte Sprache“ gewählt wurde, oder ``lang`` von ``/api/v2/search``
3. Die Sprache aus dem vom Browser gesendeten Header ``Accept-Language``

Suchen Sie beispielsweise in einem auf Japanisch eingestellten Browser nach „会議“ („Besprechung“), ist die Suchsprache ``ja``, und neben ``content`` wird auch ``content_ja`` durchsucht.
Englische Dokumente haben kein ``content_ja`` und treffen daher nur über die Bi-Gramme der gemeinsamen Felder.
Umgekehrt steigt die Bewertung eines japanischen Dokuments, wenn es zusätzlich in ``title_ja`` oder ``content_ja`` übereinstimmt, sodass es eher weiter oben erscheint.
Da Kuromoji Beugungsformen auf die Grundform zurückführt, findet eine Suche nach „走った“ („lief“) über ``content_ja`` auch japanische Dokumente, in denen „走る“ („laufen“) steht.

„Bevorzugte Sprache“ schiebt also Dokumente in dieser Sprache nach oben; es ist kein Filter, der Dokumente in anderen Sprachen ausschließt.

Nach Sprache eingrenzen: die ``lang:``-Suche
============================================

Um nach Sprache einzugrenzen, geben Sie bei der Suche das Feld ``lang`` an.
``lang`` ist ein durchsuchbares Keyword-Feld; Sie müssen also nicht für jede Sprache ein Label anlegen.

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

Das letzte Beispiel sucht nach „会議“ und schließt dabei als Japanisch erkannte Dokumente aus.
Über die API schreiben Sie denselben Ausdruck in ``q`` oder hängen ``fields.lang=en`` an (dadurch wird die Bedingung ``lang:"en"`` hinzugefügt).

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

Dokumente ohne ``lang`` (Dokumente, deren Sprache nicht erkannt werden konnte) treffen auf keine ``lang:``-Bedingung zu.

Die erkannte Sprache prüfen
---------------------------

Prüfen Sie, bevor Sie Wörterbücher oder Einstellungen ändern, welche Sprache Ihren Dokumenten zugeordnet ist.

1. Suchen Sie auf der Suchseite nacheinander nach ``lang:ja``, ``lang:en``, ``lang:zh-cn`` und ``lang:zh-tw`` und vergleichen Sie die Trefferzahlen. Über die API finden Sie die Anzahl in ``response.record_count``

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. Einzelne Dokumente suchen Sie in der Verwaltungsoberfläche unter [Systeminformationen] > [Suche] etwa anhand der URL und öffnen sie; den Wert sehen Sie im Feld ``lang``

Weicht die Erkennung von Ihren Erwartungen ab, prüfen Sie die folgenden Punkte.

- ``<html lang>`` im HTML hat Vorrang vor der automatischen Erkennung. Gibt die Vorlage der Site auch auf japanischen Seiten ``lang="en"`` aus, werden diese Seiten als Englisch behandelt
- Chinesisch ohne Region, etwa ``<html lang="zh">``, wird zu ``zh``. Für ``zh`` gibt es kein sprachspezifisches Feld mit einem Analyzer für Chinesisch, daher beschränkt sich die chinesische Analyse auf die Bi-Gramme der gemeinsamen Felder
- Kurze japanische Dokumente mit vielen Kanji und wenig Kana werden mitunter als ``zh-cn`` o. Ä. erkannt

Es gibt auch Einstellungen, die alle HTML-Dokumente bzw. alle Dateien als eine einzige Sprache behandeln.
Wenn Sie ``crawler.document.html.default.lang`` und ``crawler.document.file.default.lang`` einen Wert geben, werden weder ``<html lang>`` noch die automatische Erkennung verwendet, und die Sprache ist für alle Crawls in Fess auf diesen Wert festgelegt.
In einer Umgebung mit Dokumenten in gemischten Sprachen lassen Sie diese Einstellungen leer.

Die Suchsprachen festlegen: ``query.default.languages``
=======================================================

Standardmäßig richtet sich die Suchsprache nach der Browsersprache des jeweiligen Benutzers.
Sucht etwa ein Mitarbeiter mit englischem Browser nach japanischen Dokumenten, wird ``content_ja`` nicht verwendet, und die Reihenfolge der Ergebnisse unterscheidet sich von Benutzer zu Benutzer.
Wenn Sie das vermeiden möchten, legen Sie die Suchsprachen mit ``query.default.languages`` fest.

::

    query.default.languages=ja,en,zh-cn,zh-tw

In diesem Beispiel werden alle vier sprachspezifischen Felder in die Suchbedingung aufgenommen, unabhängig davon, wer in welcher Sprache sucht.
Jedes Dokument hat nur ein Feld für seine eigene Sprache, daher profitieren Dokumente aller Sprachen unter denselben Bedingungen von der sprachspezifischen Analyse.
Im Gegenzug hat das Hochstufen einer bestimmten Sprache über „Bevorzugte Sprache“ keine Wirkung mehr.
Bestehen Ihre Dokumente überwiegend aus Japanisch, können Sie auch nur eine Sprache angeben, etwa ``query.default.languages=ja``.

Tragen Sie die Einstellung in ``fess_config.properties`` ein und starten Sie Fess neu.
Die Datei liegt bei der ZIP-Version unter ``app/WEB-INF/classes/fess_config.properties``, bei den RPM/DEB-Versionen unter ``/etc/fess/fess_config.properties``.
Bei Docker fügen Sie sie als JVM-Option unter ``environment`` von ``fess01`` in ``compose.yaml`` hinzu und erstellen den Container neu.

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS`` wird an Leerzeichen aufgetrennt, verwenden Sie im Wert daher keine Leerzeichen.
Beim Neuerstellen des Containers gehen Einstellungen, die unter [System] > [Allgemein] geändert wurden, zusammen mit ``system.properties`` im Container verloren (:doc:`guide-02`).

Wie stark Treffer in sprachspezifischen Feldern gewichtet werden, stellen Sie mit ``query.boost.title.lang`` und ``query.boost.content.lang`` ein.
Vergleichen Sie nach einer Änderung die Reihenfolge der Suchergebnisse anhand der Schritte unter „Überprüfen“ weiter unten.

Wörterbücher je nach Sprache einsetzen
======================================

Wörterbücher bearbeiten Sie unter [System] > [Wörterbuch].
Jedes Wörterbuch wirkt auf bestimmte Felder; wählen Sie nicht das Wörterbuch, das auf das gewünschte Feld wirkt, ändern sich die Suchergebnisse nicht.

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - Wörterbuch (Datei)
     - Wirkt auf
     - Einsatz in einer mehrsprachigen Umgebung
   * - Synonyme (``synonym.txt``)
     - ``content``, ``title`` (nur bei der Suche)
     - Sprachübergreifende Umschreibungen („会議“ und „meeting“) und Schreibvarianten. Wirkt nicht auf sprachspezifische Felder
   * - Kuromoji (``ja/kuromoji.txt``)
     - Nur ``_ja``-Felder
     - Interne Begriffe und Produktnamen als ein japanisches Wort behandeln lassen
   * - Stoppwörter (``ja/stopwords.txt``)
     - Nur ``_ja``-Felder
     - Wörter, die bei japanischen Dokumenten nicht für die Suche verwendet werden sollen
   * - Stoppwörter (``en/stopwords.txt``)
     - ``content``, ``title`` und ``_en``-Felder
     - Überflüssige englische Wörter. Da sie auf die gemeinsamen Felder wirken, betreffen sie Dokumente aller Sprachen
   * - Protwords (``en/protwords.txt``)
     - ``content``, ``title`` und ``_en``-Felder
     - Englische Wörter, die nicht gestemmt werden sollen (etwa Produktnamen)
   * - Stemmer-Überschreibung (``en/stemmer_override.txt``)
     - ``content``, ``title`` und ``_en``-Felder
     - Das Ergebnis des englischen Stemmings vorgeben
   * - Zuordnung (``mapping.txt``)
     - ``content``, ``title``
     - Zeichenersetzung. ``ja/mapping.txt`` ist eine separate Datei für die ``_ja``-Felder

Ein Wörterbuch geschützter Wörter (Protwords) für Japanisch gibt es nicht.
Der Grund ist, dass ``japanese_analyzer`` keinen Filter hat, der geschützte Wörter liest.
Für die Felder für vereinfachtes und traditionelles Chinesisch gibt es kein Benutzerwörterbuch, das sich in der Verwaltungsoberfläche bearbeiten lässt (die Stoppwörter liegen in ``zh-cn/stopwords.txt`` bzw. ``zh-tw/stopwords.txt``).

Sprachübergreifende Synonyme
----------------------------

Um englische Dokumente mit japanischen Begriffen zu finden, registrieren Sie die Übersetzungen als Synonyme.
Im Format der hochzuladenden Datei stehen bedeutungsgleiche Wörter kommagetrennt in einer Zeile.

::

    会議,ミーティング,meeting
    見積,quotation

Synonyme werden bei der Suche in den gemeinsamen Feldern expandiert, daher ist kein erneutes Crawlen nötig.
Regeln für die Registrierung, etwa Hiragana als Katakana und Vollbreiten-Alphanumerik als Halbbreite zu erfassen, finden Sie unter `Synonym-Wörterbuch <https://fess.codelibs.org/de/stable/admin/synonym-guide.html>`__.

Kuromoji-Benutzerwörterbuch
---------------------------

Im Kuromoji-Wörterbuch registrieren Sie ein Token, seine zerlegten Tokens, seine Lesung (in Katakana) und seine Wortart.
Damit ein interner Begriff oder Produktname, den Kuromoji zu fein zerlegt, als ein Wort behandelt wird, tragen Sie dasselbe Wort als Token und als zerlegte Tokens ein.

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

Dieses Wörterbuch wirkt nur auf die ``_ja``-Felder.
Das gemeinsame Feld ``content`` wird in Bi-Gramme zerlegt, daher ändern sich Treffer in ``content`` nicht, wenn Sie das Kuromoji-Wörterbuch ändern.
Eine Wirkung zeigt sich nur bei Suchen, deren Suchsprachen ``ja`` enthalten, und nur bei Dokumenten, die als Japanisch erkannt wurden.

Wörterbuchänderungen übernehmen
-------------------------------

Allein durch das Speichern eines Wörterbuchs ändern sich die Suchergebnisse nicht.

1. Öffnen Sie [Systeminformationen] > [Wartung] und klicken Sie unter „Dokumentenindex neu laden“ auf [Neu laden]. Der Index wird geschlossen und wieder geöffnet; währenddessen liefern Suchen Fehler oder 0 Treffer. Führen Sie dies zu einer Zeit mit geringer Nutzung aus
2. Synonyme werden nur bei der Suche verwendet, daher sind sie nach dem Neuladen bereits übernommen
3. Die übrigen Wörterbücher (Kuromoji, Zuordnung, Stoppwörter, Protwords, Stemmer-Überschreibung) ändern auch die Analyse beim Aufbau des Index. Bereits indexierte Dokumente bleiben mit dem alten Wörterbuch analysiert; crawlen Sie die betroffenen Inhalte daher erneut

Ist beim erneuten Crawlen „Letzte Änderung prüfen“ unter [System] > [Allgemein] aktiviert (Standard), werden nicht aktualisierte Dateien und Seiten nicht erneut abgerufen.
Deaktivieren Sie die Option vorübergehend, führen Sie den Crawl aus und aktivieren Sie sie danach wieder.

Überprüfen
==========

Token-Grenzen mit der ``_analyze``-API ansehen
----------------------------------------------

Am zuverlässigsten prüfen Sie, ob eine Wörterbuchänderung übernommen wurde, indem Sie mit der ``_analyze``-API von OpenSearch dieselbe Zeichenfolge durch die Analyzer des gemeinsamen Felds und des japanischen Felds schicken und die Ergebnisse vergleichen.
In der Docker-Umgebung aus :doc:`guide-02` ist OpenSearch über Port 9200 des Hosts erreichbar.

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

Mit ``japanese_analyzer`` wird der Text in Wörter zerlegt, und „を“ und „た“ werden entfernt.
Mit ``standard_analyzer`` wird er in Einheiten von je zwei Zeichen wie „全文“, „文検“ und „検索“ zerlegt.
Nachdem Sie „東京スカイツリー“ im Kuromoji-Wörterbuch registriert und neu geladen haben, liefert ``japanese_analyzer`` für dieses Wort ein einziges Token.
Ein registriertes Synonym prüfen Sie, indem Sie „会議“ mit ``"analyzer":"standard_search_analyzer"`` analysieren und bestätigen, dass ein aus „meeting“ erzeugtes Token (gestemmt zu ``meet``) erscheint.

In den Suchergebnissen prüfen
-----------------------------

1. Suchen Sie auf der Suchseite nach einem Wort, das sowohl in japanischen als auch in englischen Dokumenten vorkommt
2. Wechseln Sie unter [Optionen] die „Bevorzugte Sprache“ zwischen „Japanisch“ und „Englisch“ und prüfen Sie, dass sich die Sprache der obersten Dokumente ändert. Wenn Sie ``query.default.languages`` gesetzt haben, prüfen Sie, dass sich die Reihenfolge beim Wechseln nicht ändert
3. Prüfen Sie nach dem Registrieren von Übersetzungssynonymen und dem Neuladen, dass ``lang:en 会議`` englische Dokumente findet
4. Suchen Sie nach dem Ändern des Kuromoji-Wörterbuchs und erneutem Crawlen nach dem registrierten Wort und prüfen Sie, dass japanische Dokumente gefunden werden, die es enthalten. Dass sich die Zerlegung selbst geändert hat, prüfen Sie mit ``_analyze`` wie oben beschrieben

Ändern sich die Ergebnisse nicht, gleichen Sie die Spalte „Wirkt auf“ der Wörterbuchtabelle mit dem ``lang`` des Dokuments ab.
Fügen Sie beispielsweise ``en/stopwords.txt`` ein japanisches Wort mit drei oder mehr Zeichen hinzu, hat das keine Wirkung, weil der Text in den gemeinsamen Feldern zu Tokens aus je zwei Zeichen wird und das Wort nie übereinstimmt.

Zusammenfassung
===============

- Jedes Dokument ist über die gemeinsamen Felder (``content``, ``title``) durchsuchbar, die Bi-Gramme und englisches Stemming anwenden
- Die erkannte Sprache in ``lang`` und die sprachspezifischen Felder (etwa ``content_ja``) ergänzen eine zur Sprache passende Analyse
- Die Suchsprachen werden in der Reihenfolge ``query.default.languages``, ``lang`` der Anfrage und Browsersprache bestimmt; sie schieben Dokumente nach oben, statt sie zu filtern
- Um nach Sprache einzugrenzen, geben Sie das Feld ``lang`` an, etwa ``lang:en``
- Bearbeiten Sie das Wörterbuch, das auf das gewünschte Feld wirkt, und übernehmen Sie die Änderung durch Neuladen des Dokumentenindex und bei Bedarf durch erneutes Crawlen

Weiterführende Artikel
======================

- Verbesserungspunkte in Suchprotokollen finden und mit Synonymen und Schlüsselübereinstimmungen beheben: :doc:`guide-08`
- Interne Websites und Dateiserver gemeinsam crawlen: :doc:`guide-04`
- Dokumente mit ähnlicher Bedeutung finden, auch wenn die Stichwörter nicht übereinstimmen: :doc:`guide-18`
- Die Such-API aus Geschäftsanwendungen aufrufen: :doc:`guide-11`

Referenzen
==========

- `Wörterbuch <https://fess.codelibs.org/de/stable/admin/dict-guide.html>`__
- `Kuromoji-Wörterbuch <https://fess.codelibs.org/de/stable/admin/kuromoji-guide.html>`__
- `Synonym-Wörterbuch <https://fess.codelibs.org/de/stable/admin/synonym-guide.html>`__
- `Stoppwort-Wörterbuch <https://fess.codelibs.org/de/stable/admin/stopwords-guide.html>`__
- `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__
- `Suchbezogene Konfigurationen (Standardsprache für die Suche) <https://fess.codelibs.org/de/stable/config/search-advanced.html>`__
- `Erweiterte Crawler-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-advanced.html>`__
- `Feldsuche <https://fess.codelibs.org/de/stable/user/search-field.html>`__
- `Such-API <https://fess.codelibs.org/de/stable/api/api-search.html>`__
