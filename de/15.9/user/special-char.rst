================
Sonderzeichen
================

Die folgenden Zeichen haben in der Syntax der Suchanfrage eine besondere Bedeutung und werden daher in Suchbegriffen als Sonderzeichen behandelt. Um diese Zeichen als literale Suchzeichen zu verwenden, müssen Sie sie maskieren.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

Diese Zeichen werden verwendet, um Suchfunktionen wie erforderliche/ausgeschlossene Begriffe (``+`` ``-``), boolesche Operatoren (``&&`` ``||`` ``!``), Gruppierung (``( )``), Bereichssuche (``[ ]`` ``{ }``), Boost-Suche (``^``), Phrasensuche (``"``), unscharfe Suche (``~``), Platzhaltersuche (``*`` ``?``) und Feldsuche (``:``) aufzurufen.

Wird beispielsweise ein in einer URL oder einem Dateipfad enthaltenes „/" oder „:" oder ein in Programmcode enthaltenes „+" oder „-" unmaskiert als Suchbegriff verwendet, kann dies zu einem unerwarteten Suchergebnis führen.

Liste der Sonderzeichen und ihre Bedeutung
--------------------------------------------

.. list-table::
   :header-rows: 1

   * - Sonderzeichen
     - Bedeutung
     - Verwandte Seite
   * - ``+`` ``-``
     - Kennzeichnung von Pflicht- bzw. ausgeschlossenen Begriffen (AND-Suche / NOT-Suche)
     - :doc:`search-and` / :doc:`search-not`
   * - ``&&`` ``||``
     - AND-Suche / OR-Suche
     - :doc:`search-and` / :doc:`search-or`
   * - ``!``
     - NOT-Suche (Ausschlusssuche)
     - :doc:`search-not`
   * - ``( )``
     - Gruppierung von Suchbedingungen
     - :doc:`advanced-search`
   * - ``[ ]`` ``{ }``
     - Bereichssuche (``[ ]`` schließt die Grenzwerte ein, ``{ }`` schließt sie aus)
     - :doc:`search-range`
   * - ``^``
     - Boost-Suche (Gewichtung)
     - :doc:`search-boost`
   * - ``"``
     - Phrasensuche (behandelt den eingeschlossenen Text als zusammenhängendes Wort; kann auch anstelle einer Maskierung verwendet werden)
     - :doc:`advanced-search`
   * - ``~``
     - Unscharfe Suche (Fuzzy-Suche)
     - :doc:`search-fuzzy`
   * - ``*`` ``?``
     - Wildcard-Suche
     - :doc:`search-wildcard`
   * - ``:``
     - Angabe des Suchfelds
     - :doc:`search-field`
   * - ``\``
     - Escape-Zeichen (Maskierungszeichen)
     - (diese Seite)
   * - ``/``
     - Schrägstrich (muss maskiert werden, wenn er z. B. in einer URL enthalten ist)
     - :doc:`search-field`

Verwendung
-----------

Um ein Sonderzeichen als literales Suchzeichen zu behandeln, verwenden Sie eine der folgenden Methoden.

* Setzen Sie ``\`` unmittelbar vor das zu maskierende Zeichen. Das darauffolgende einzelne Zeichen wird als normales Zeichen behandelt und nicht als Syntax der Suchanfrage interpretiert.
* Schließen Sie den Suchbegriff in ``"`` ein. Die eingeschlossene Zeichenfolge wird als Phrasensuche behandelt, und die darin enthaltenen Sonderzeichen werden nicht als Syntax der Suchanfrage interpretiert. Beachten Sie jedoch, dass dadurch Funktionen wie die Platzhaltersuche (``*`` ``?``) nicht verfügbar sind, da es sich um eine Phrasensuche handelt.

::

    aaa\/bbb
    "aaa/bbb"

Möchten Sie beispielsweise „C++" als Suchbegriff verwenden, maskieren Sie es wie folgt:

::

    C\+\+
    "C++"

Siehe auch
-----------

- :doc:`search-field`
- :doc:`search-wildcard`
- :doc:`search-fuzzy`
- :doc:`advanced-search`
