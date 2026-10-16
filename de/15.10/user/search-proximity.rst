================
Näherungssuche
================
Näherungssuche (Proximity-Suche)
==================================

Mit der Näherungssuche finden Sie Dokumente, in denen die Wörter einer Phrase nahe beieinander stehen, auch wenn sie nicht direkt aufeinander folgen. Sie ist nützlich, wenn zwischen den gesuchten Wörtern weitere Wörter stehen können.

Verwendung
------------

Schließen Sie die Wörter in doppelte Anführungszeichen ein und fügen Sie hinter dem schließenden Anführungszeichen "~" und eine Zahl an.

Die folgende Suche findet beispielsweise Dokumente, in denen "Fess" und "Suche" innerhalb eines Abstands von 3 vorkommen:

::

    "Fess Suche"~3

Die Zahl gibt die maximale Anzahl an Positionsverschiebungen an, die zwischen den Wörtern zulässig sind (siehe "Wie der Abstand gezählt wird" weiter unten). Je größer die Zahl, desto weiter dürfen die Wörter auseinander liegen.

Sie können die Näherungssuche auch auf ein bestimmtes Feld anwenden. Im folgenden Beispiel wird das Feld title durchsucht.

::

    title:"Fess Suche"~3

Wenn Sie die Zahl weglassen und nur "~" angeben (zum Beispiel ``"Fess Suche"~``), wird die Phrase als normale Phrasensuche behandelt, bei der die Wörter direkt aufeinander folgen müssen. Eine Dezimalzahl wird auf eine ganze Zahl gekürzt (``~2.5`` wird als ``~2`` behandelt).

Die Näherungssuche kann mit einem Boost kombiniert werden. Im folgenden Beispiel wird die Näherungssuche mit dem Faktor 2 gewichtet (siehe :doc:`search-boost`).

::

    "Fess Suche"~5^2

Wie der Abstand gezählt wird
------------------------------

* Die Zahl ist die maximale Anzahl an Positionsverschiebungen zwischen den Wörtern. Sie wird in Token gezählt, die der Analyzer des Zielfelds erzeugt, nicht in Zeichen oder durch Leerzeichen getrennten Wörtern. Bei englischem Text entspricht sie ungefähr der Anzahl der Wörter zwischen den Begriffen. Wörter, die bei der Analyse als Stoppwörter entfernt werden, werden dennoch mitgezählt.
* Die Wörter dürfen in anderer Reihenfolge vorkommen, für die umgekehrte Reihenfolge ist jedoch eine größere Zahl erforderlich. Ein Dokument mit "quick brown fox" trifft beispielsweise auf ``"quick fox"~1`` zu, auf ``"fox quick"`` aber erst ab ``~3``.

::

    "quick fox"~1
    "fox quick"~3

Japanische, chinesische und koreanische Texte (CJK)
-----------------------------------------------------

Bei japanischen und anderen CJK-Texten hängt die Einheit, in der der Abstand gezählt wird, vom Feld ab.

* In den allgemeinen Feldern title und content entspricht der Abstand in etwa der Anzahl der Zeichen zwischen den Wörtern.
* In den sprachspezifischen Feldern wird in morphologischen Token gezählt; entfernte Partikel werden ebenfalls mitgezählt.

Trennen Sie die Wörter daher durch Leerzeichen und geben Sie eine großzügige Zahl an.

::

    "全文 検索"~5
    "大阪 おいしい"~10

Eine Zeichenfolge ohne Leerzeichen (zum Beispiel ``"大阪おいしい"~10``) funktioniert als Näherungssuche zwischen den Wörtern möglicherweise nicht wie erwartet, da sie in den allgemeinen Feldern als eine zusammenhängende Zeichenfolge abgeglichen wird. Trennen Sie die Wörter daher durch Leerzeichen. Der Abstand lässt sich nicht exakt in eine Zeichenanzahl umrechnen. Beginnen Sie daher mit einer großzügigen Zahl und grenzen Sie sie anhand der Ergebnisse ein.

Siehe auch
============

- :doc:`search-fuzzy`
- :doc:`search-boost`
- :doc:`search-field`
- :doc:`special-char`
