================
Sonderzeichen
================

Bei der Suche mit |Fess| werden die folgenden Zeichen als Sonderzeichen (reservierte Zeichen) der Suchsyntax behandelt.
Wenn Sie eines dieser Zeichen als gewöhnliches Suchzeichen verwenden möchten, müssen Sie es maskieren.
Wird beispielsweise ein in einer URL oder einem Dateipfad enthaltenes „/" oder „:" oder ein in Programmcode enthaltenes „+" oder „-" unmaskiert gesucht, kann dies zu einem unerwarteten Suchergebnis führen.
Wie Sie diese Zeichen maskieren, erfahren Sie im folgenden Abschnitt.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

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

Maskieren Sie mit \ oder umschließen Sie den Suchbegriff mit ".

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

