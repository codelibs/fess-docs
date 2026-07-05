==========================
Analyzer-Konfiguration
==========================

Über Analyzer
=============

Bei der Erstellung eines Index für die Suche müssen Dokumente für die Registrierung als Index aufgeteilt werden.
In |Fess| ist die Funktion zum Zerlegen von Dokumenten in Wörter als Analyzer registriert.
Ein Analyzer besteht aus CharFilter, Tokenizer und TokenFilter.

Grundsätzlich können Einheiten, die kleiner sind als die vom Analyzer aufgeteilten Einheiten, bei einer Suche nicht gefunden werden.
Betrachten Sie zum Beispiel den Satz "Wohnen in Tokyo".
Angenommen, dieser Satz wurde vom Analyzer in "Tokyo", "in" und "wohnen" aufgeteilt.
In diesem Fall wird eine Suche nach "Tokyo" einen Treffer ergeben.
Eine Suche nach "Kyoto" ergibt jedoch keinen Treffer.

|Fess| stellt für jede Sprache einen eigenen Analyzer bereit.
Anhand des Suffixes des Feldnamens im Index (z. B. ``content_ja``, ``content_en``) wird der anzuwendende sprachspezifische Analyzer automatisch ausgewählt.

Definitionsdateien für Analyzer
================================

Analyzer verfügen über keine eigene Administrationsoberfläche; Änderungen erfolgen durch direkte Bearbeitung der Konfigurationsdateien.
Die zugehörigen Dateien befinden sich unter ``app/WEB-INF/classes/fess_indices/``.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Datei
     - Inhalt
   * - ``fess_indices/fess.json``
     - Konfiguration des Dokumentenindex. Enthält die Definitionen von CharFilter, Tokenizer, TokenFilter und Analyzer.
   * - ``fess_indices/fess/doc.json``
     - Mapping des Dokumentenindex. Weist jedem Feldnamensmuster (z. B. ``*_ja`` oder ``*_en``) den anzuwendenden Analyzer zu.
   * - ``fess_indices/fess/<Sprache>/``
     - Wörterbuchdateien pro Sprache (z. B. ``ja/kuromoji.txt``, ``ko/nori.txt``, ``en/protwords.txt``, ``en/stemmer_override.txt``, ``stopwords.txt`` je Sprache).
   * - ``fess_indices/fess/mapping.txt``, ``fess_indices/fess/synonym.txt``
     - Zeichenmapping-Wörterbuch und Synonymwörterbuch, die sprachübergreifend verwendet werden.

Die Definition des Analyzers selbst (Kombination aus Tokenizer und TokenFilter) erfolgt in ``fess.json``; welcher Analyzer auf welches Feld angewendet wird, wird in ``fess/doc.json`` festgelegt.

.. note::
   Bei Verwendung eines verwalteten Dienstes wie Amazon OpenSearch Service wird vorrangig die zur Suchmaschinenvariante passende Konfigurationsdatei verwendet, z. B. ``fess_indices/_aws/fess.json`` oder ``fess_indices/_cloud/fess.json``.

Registrierung von Analyzern
============================

Die Analyzer-Konfiguration wird beim Start von |Fess| registriert: Falls kein Suchindex vorhanden ist, wird der Index anhand der oben genannten Konfigurationsdateien erstellt.
Der Index wird mit einem zeitstempelbasierten Namen erstellt (z. B. ``fess.20240101120000000``), dem die Aliase ``fess.search`` und ``fess.update`` zugewiesen werden.

Platzhalter in den Konfigurationsdateien wie ``${fess.dictionary.path}`` werden bei der Indexerstellung durch die tatsächlichen Werte ersetzt.
Das Verzeichnis für Wörterbuchdateien kann über die Systemeigenschaft ``fess.dictionary.path`` geändert werden.

Ist ein bestehender Index vorhanden, werden die bereits definierten Einstellungen wiederverwendet.
Wenn die Analyzer-Definition geändert wird, muss der Index daher neu erstellt werden, damit die Änderungen wirksam werden.

Anpassung über Wörterbücher
=============================

Die vom Analyzer verwendeten Wörterbücher können über die Administrationsoberfläche bearbeitet werden.

* :doc:`../admin/kuromoji-guide` - Benutzerwörterbuch für die japanische morphologische Analyse
* :doc:`../admin/synonym-guide` - Synonymwörterbuch
* :doc:`../admin/mapping-guide` - Zeichenmapping
* :doc:`../admin/stopwords-guide` - Stoppwörter
* :doc:`../admin/protwords-guide` - Geschützte Wörter
* :doc:`../admin/stemmeroverride-guide` - Überschreibung des Stemmings

Zur Zusammensetzungsmethode des Analyzers siehe die OpenSearch-Analyzer-Dokumentation.

Hinweise
========

Die Analyzer-Konfiguration hat großen Einfluss auf die Suche.
Nehmen Sie Änderungen am Analyzer erst vor, nachdem Sie die Funktionsweise des Lucene-Analyzers verstanden haben, oder wenden Sie sich an den kommerziellen Support.
