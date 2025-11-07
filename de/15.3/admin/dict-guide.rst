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


.. |image0| image:: ../../../resources/images/ja/15.3/admin/dict-1.png
            :height: 940px
