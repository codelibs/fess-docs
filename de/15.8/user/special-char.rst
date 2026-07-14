================
Sonderzeichen
================

Die folgenden Zeichen haben in der Syntax der Suchanfrage eine besondere Bedeutung und werden daher in Suchbegriffen als Sonderzeichen behandelt. Um diese Zeichen als literale Suchzeichen zu verwenden, müssen Sie sie maskieren.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

Diese Zeichen werden verwendet, um Suchfunktionen wie erforderliche/ausgeschlossene Begriffe (``+`` ``-``), boolesche Operatoren (``&&`` ``||`` ``!``), Gruppierung (``( )``), Bereichssuche (``[ ]`` ``{ }``), Boost-Suche (``^``), Phrasensuche (``"``), unscharfe Suche (``~``), Platzhaltersuche (``*`` ``?``) und Feldsuche (``:``) aufzurufen.

Verwendung
-----------

Um ein Sonderzeichen als literales Suchzeichen zu behandeln, verwenden Sie eine der folgenden Methoden.

* Setzen Sie ``\`` unmittelbar vor das zu maskierende Zeichen. Das darauffolgende einzelne Zeichen wird als normales Zeichen behandelt und nicht als Syntax der Suchanfrage interpretiert.
* Schließen Sie den Suchbegriff in ``"`` ein. Die eingeschlossene Zeichenfolge wird als Phrasensuche behandelt, und die darin enthaltenen Sonderzeichen werden nicht als Syntax der Suchanfrage interpretiert. Beachten Sie jedoch, dass dadurch Funktionen wie die Platzhaltersuche (``*`` ``?``) nicht verfügbar sind, da es sich um eine Phrasensuche handelt.

::

    aaa\/bbb
    "aaa/bbb"
