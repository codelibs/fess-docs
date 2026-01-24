=============
Analyzer-Konfiguration
=============

Über Analyzer
==============

Bei Erstellung eines Index für die Suche müssen Dokumente für Registrierung als Index aufgeteilt werden.
In |Fess| ist die Funktion zum Zerlegen von Dokumenten in Wörter als Analyzer registriert.
Analyzer besteht aus CharFilter, Tokenizer und TokenFilter.

Grundsätzlich können Einheiten kleiner als die vom Analyzer aufgeteilten Einheiten bei Suche nicht gefunden werden.
Betrachten Sie zum Beispiel den Satz "Wohnen in Tokyo".
Angenommen, dieser Satz wurde vom Analyzer in "Tokyo", "in", "wohnen" aufgeteilt.
In diesem Fall wird eine Suche nach "Tokyo" einen Treffer ergeben.
Eine Suche nach "Kyoto" ergibt jedoch keinen Treffer.

Analyzer-Konfiguration wird beim Start von |Fess| registriert, indem fess-Index mit app/WEB-INF/classes/fess_indices/fess.json erstellt wird, wenn fess-Index nicht existiert.
Für Zusammensetzungsmethode des Analyzers siehe OpenSearch-Analyzer-Dokumentation.

Analyzer-Konfiguration hat großen Einfluss auf Suche.
Bei Änderung des Analyzers führen Sie dies nach Verständnis der Funktionsweise des Lucene-Analyzers durch oder konsultieren Sie kommerziellen Support.
