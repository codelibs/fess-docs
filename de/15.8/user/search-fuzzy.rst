================
Unscharfe Suche
================

Unscharfe Suche (Fuzzy-Suche)
===============================

Wenn Sie auch nach Wörtern suchen möchten, die nicht exakt mit dem Suchbegriff übereinstimmen, können Sie die unscharfe Suche (Fuzzy-Suche) verwenden. Die unscharfe Suche ist eine Suchmethode, bei der ein Wort als Treffer gilt, wenn der Unterschied (die Editierdistanz) zwischen dem Suchbegriff und einem im Index registrierten Wort innerhalb eines bestimmten Bereichs liegt. Die Editierdistanz ist die minimale Anzahl an Einfügungen, Löschungen und Ersetzungen von Zeichen, die notwendig sind, um ein Wort in ein anderes umzuwandeln. |Fess| verwendet standardmäßig zusätzlich zu diesen Operationen die Damerau-Levenshtein-Distanz (optimal string alignment), bei der auch das Vertauschen von 2 benachbarten Zeichen als eine einzelne Änderung gezählt wird.

Verwendung
-----------

Fügen Sie "~" nach dem Suchbegriff an, auf den Sie die unscharfe Suche anwenden möchten.

Wenn Sie beispielsweise das Wort "Fess" unscharf suchen möchten, können Sie durch Eingabe des Folgenden in das Suchformular Dokumente finden, die Wörter enthalten, die "Fess" ähnlich sind (z. B. "Fes").

::

    Fess~

Wenn Sie nach "~" eine Zahl anfügen, können Sie die zulässige Editierdistanz (bis zu wie vielen Zeichen Unterschied toleriert wird) angeben. Zulässige Werte sind die ganzen Zahlen 0, 1 oder 2.

::

    Fess~1

Im obigen Beispiel werden Wörter gesucht, deren Editierdistanz zu "Fess" höchstens 1 beträgt.

Wenn Sie die Zahl weglassen und nur "~" angeben, wird eine Editierdistanz von 2 verwendet. Der Höchstwert der Editierdistanz ist 2; auch wenn ein Wert von 3 oder mehr angegeben wird, wird er als 2 behandelt.

Sie können die unscharfe Suche auch auf ein bestimmtes Feld anwenden. Im folgenden Beispiel werden im Feld title Dokumente gesucht, die Wörter enthalten, die "Fess" ähnlich sind.

::

    title:Fess~

Wenn kein Feld angegeben wird, erfolgt die unscharfe Suche in den Feldern title und content.

Nutzungsbedingungen
--------------------

Beachten Sie bei der Verwendung der unscharfen Suche die folgenden Punkte:

* Die unscharfe Suche wird auf einzelne Wörter angewendet. Sie kann nicht auf Phrasen angewendet werden, die in Anführungszeichen eingeschlossen sind. Eine Zahl, die einer Phrase angehängt wird (zum Beispiel ``"Fess Search"~2``), stellt dabei keine unscharfe Suche dar, sondern eine Näherungssuche (proximity search), die den Abstand zwischen den Wörtern angibt.
* Die unscharfe Suche erfolgt auf Basis der im Index registrierten Wörter, wobei der Suchbegriff nicht erneut analysiert wird. Daher funktioniert sie möglicherweise nicht wie erwartet bei Texten wie Japanisch, die per Bi-Gramm oder morphologischer Analyse in Token zerlegt werden. Die unscharfe Suche ist vor allem bei alphanumerischen Wörtern wirksam.
* Bei sehr kurzen Wörtern mit 1 bis 2 Zeichen kann das Verhalten trotz angehängtem "~" einer exakten Übereinstimmung nahekommen, da ein Treffer nur zustande kommt, wenn die Editierdistanz kleiner als die Wortlänge ist.

.. note::

    Das Verhalten der unscharfen Suche kann in ``fess_config.properties`` angepasst werden.

    * ``query.fuzzy.prefix_length`` (Standardwert: ``0``): Die Anzahl der Zeichen vom Anfang des Wortes an, die exakt übereinstimmen müssen. Ein höherer Wert schränkt den Bereich ein, in dem Abweichungen toleriert werden.
    * ``query.fuzzy.expansions`` (Standardwert: ``50``): Die maximale Anzahl der Wörter, die als Treffer-Kandidaten expandiert werden.
    * ``query.fuzzy.transpositions`` (Standardwert: ``true``): Legt fest, ob das Vertauschen von 2 benachbarten Zeichen als eine einzelne Änderung gezählt wird. Bei ``true`` wird die Damerau-Levenshtein-Distanz verwendet, bei ``false`` die klassische Levenshtein-Distanz.

.. note::

    Auch bei einer normalen Suche ohne angehängtes "~" fügt |Fess| für Suchbegriffe ab einer bestimmten Länge (standardmäßig ab 4 Zeichen) automatisch eine leicht gewichtete unscharfe Übereinstimmung als unterstützende Funktion hinzu, um die Relevanz zu erhöhen (``query.boost.fuzzy.*``). Dies dient der Anpassung der Rangfolge der Suchergebnisse und ist ein von der unscharfen Suche mittels "~" unabhängiger Mechanismus.
