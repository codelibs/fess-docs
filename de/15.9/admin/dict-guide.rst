===========
Wörterbuch
===========

Übersicht
=========

Hier wird die Konfiguration von Wörterbüchern erläutert.

Nehmen Sie Wörterbuchänderungen nur vor, wenn Sie die Spezifikationen der jeweiligen Wörterbücher verstehen.
Fehlerhafte Wörterbuchänderungen können dazu führen, dass auf den Index nicht mehr zugegriffen werden kann.

Übersicht
=========

Um die Übersichtsseite der verwaltbaren Wörterbücher zu öffnen, klicken Sie im linken Menü auf [System > Wörterbuch].


|image0|


Geltungsbereich der Wörterbücher und Zeitpunkt der Wirksamkeit
==============================================================

Jedes Wörterbuch wirkt auf andere Felder und wird zu einem anderen Zeitpunkt
wirksam. Wenn Sie ein Wörterbuch bearbeitet haben und sich die Suchergebnisse
nicht ändern, prüfen Sie zuerst diese Tabelle.

.. list-table::
   :header-rows: 1
   :widths: 22 26 28 24

   * - Wörterbuch
     - Datei
     - Betroffene Felder
     - Zeitpunkt der Wirksamkeit
   * - Kuromoji
     - ``ja/kuromoji.txt``
     - Nur ``_ja``-Felder wie ``content_ja``
     - Beim Indexieren (erneutes Crawlen erforderlich)
   * - Synonym
     - ``synonym.txt``
     - ``content`` und ``title``
     - Bei der Suche (kein erneutes Crawlen nötig)
   * - Mapping (alle Sprachen)
     - ``mapping.txt``
     - ``content`` und ``title``
     - Beim Indexieren (erneutes Crawlen erforderlich)
   * - Mapping (je Sprache)
     - ``ja/mapping.txt``
     - Nur ``_ja``-Felder wie ``content_ja``
     - Beim Indexieren (erneutes Crawlen erforderlich)
   * - Protwords
     - ``en/protwords.txt``
     - ``content`` und ``title``
     - Beim Indexieren und bei der Suche
   * - Stoppwörter
     - ``en/stopwords.txt``
     - ``content`` und ``title``
     - Beim Indexieren und bei der Suche
   * - Stemmer-Überschreibung
     - ``en/stemmer_override.txt``
     - ``content`` und ``title``
     - Beim Indexieren und bei der Suche

.. note::

   Ein Analyzer wird beim Öffnen des Index aufgebaut. Eine Änderung an einer
   Wörterbuchdatei wird daher erst wirksam, **wenn der Index geschlossen und
   wieder geöffnet wird**. Ein Wörterbuch, das beim Indexieren wirkt, wird
   zudem nicht rückwirkend auf bereits indexierte Dokumente angewendet; diese
   müssen erneut gecrawlt werden.
   Wie Sie eine Änderung übernehmen, steht unter :ref:`dict-apply-changes`.

.. warning::

   Das Zeichenersetzungs-Wörterbuch, das auf ``content`` wirkt -- das Feld, aus
   dem die meisten Suchen beantwortet werden -- ist die ``mapping.txt`` im
   **Wurzelverzeichnis**, nicht ``ja/mapping.txt``. Beide heißen Mapping, sind
   aber verschiedene Dateien.

.. _dict-apply-changes:

Wörterbuchänderungen übernehmen
-------------------------------

Das Speichern eines Wörterbuchs ändert die Suchergebnisse nicht, egal wie lange Sie warten. Das
configsync-Plugin von OpenSearch schreibt die gespeicherten Wörterbücher etwa einmal pro Minute in
ihre Dateien, ein Analyzer liest seine Wörterbücher aber nur beim Öffnen des Index, sodass ein
bereits geöffneter Index weiter die alten verwendet. Laden Sie den Dokumentindex nach dem
Bearbeiten von Wörterbüchern neu:

1. Öffnen Sie im linken Menü [Systeminformationen > Wartung].
2. Klicken Sie unter „Dokumentenindex neu laden“ auf [Neu laden].

Die Schaltfläche schreibt zuerst die gespeicherten Wörterbücher in ihre Dateien und schließt und
öffnet dann den Index, auf den der Alias ``fess.update`` zeigt; auf das regelmäßige Schreiben
müssen Sie nicht warten. Ein Wörterbuch, das bei der Suche wirkt, etwa ein Synonym, wird wirksam,
sobald der Index wieder geöffnet ist. Bei einem Wörterbuch, das beim Indexieren wirkt, crawlen Sie
die betroffenen Dokumente zusätzlich erneut.

.. warning::

   Solange der Index geschlossen ist und bis seine Shards nach dem Öffnen wieder zugewiesen sind,
   kann der Index nicht durchsucht werden: Suchen schlagen fehl oder liefern keine Ergebnisse. Je
   größer der Index, desto länger dauert das; laden Sie ihn daher zu einer ruhigen Zeit neu.

Um dasselbe ohne die Verwaltungsoberfläche aus einem Skript heraus zu tun, senden Sie dieselben
Operationen an OpenSearch::

    curl -X POST "localhost:9200/_configsync/flush"
    curl -X POST "localhost:9200/fess.update/_close"
    curl -X POST "localhost:9200/fess.update/_open"

``_configsync/flush`` schreibt die gespeicherten Wörterbücher sofort in ihre Dateien. Ohne diesen
Aufruf warten Sie nach dem Speichern mindestens eine Minute, bevor Sie den Index schließen.

Kuromoji-Benutzerwörterbuch und Suchergebnisse
----------------------------------------------

Das Feld ``content`` wird mit dem Standard-Tokenizer und ``cjk_bigram``
analysiert und ist deshalb davon unabhängig, wie Kuromoji ein Wort zerlegt.
Ein japanisches Kompositum im Kuromoji-Benutzerwörterbuch zu registrieren und
erneut zu crawlen ändert an einer Suche gegen ``content`` also nichts. Wirksam
wird der Eintrag in ``content_ja``, das je nach Sprache der Anfrage zur Abfrage
hinzugenommen wird.

Kuromoji
========

Verwaltet das Wörterbuch für die japanische morphologische Analyse.
ja/kuromoji.txt ist das Wörterbuch für die japanische morphologische Analyse.

Synonyme
========

Verwaltet das Synonym-Wörterbuch.
synonym.txt ist die sprachübergreifend verwendete Synonym-Wörterbuchdatei.

Mapping
=======

Verwaltet das Zeichenersetzungs-Wörterbuch.
mapping.txt ist die sprachübergreifende oder sprachspezifische Wortersetzungs-Wörterbuchdatei.

Protwords
=========

Verwaltet das Schutzwort-Wörterbuch.
protwords.txt wird für jede Sprache platziert und ist eine Wortliste für Wörter, die vom Stemming ausgeschlossen werden sollen.

Stoppwörter
===========

Verwaltet das Stoppwort-Wörterbuch.
stopwords.txt wird für jede Sprache platziert und ist eine Wortliste für Wörter, die bei der Indexerstellung ausgeschlossen werden sollen.

Stemmer-Überschreibung
======================

Verwaltet das Stemmer-Überschreibungs-Wörterbuch.
stemmer_override.txt wird für jede Sprache platziert und ist eine Wortersetzungs-Wörterbuchdatei zum Überschreiben der Stemming-Verarbeitung.


.. |image0| image:: ../../../resources/images/en/15.9/admin/dict-1.png
            :height: 940px
