==================
Special Characters
==================

In |Fess| search, the following symbols are treated as special characters (reserved words) in the search syntax. If you want to search for one of these symbols as an ordinary search character, you need to escape it. For example, searching directly for a "/" or ":" in a URL or file path, or a "+" or "-" in program code, can produce unexpected search results. See below for how to escape these characters.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

List of Special Characters
---------------------------

.. list-table::
   :header-rows: 1

   * - Special Character
     - Meaning
     - Related
   * - ``+`` ``-``
     - Specifies required or prohibited terms (AND search / NOT search)
     - :doc:`search-and` / :doc:`search-not`
   * - ``&&`` ``||``
     - AND search / OR search
     - :doc:`search-and` / :doc:`search-or`
   * - ``!``
     - NOT search (exclusion search)
     - :doc:`search-not`
   * - ``( )``
     - Groups search conditions
     - :doc:`advanced-search`
   * - ``[ ]`` ``{ }``
     - Range search (``[ ]`` includes the boundary values, ``{ }`` excludes them)
     - :doc:`search-range`
   * - ``^``
     - Boost search (weighting)
     - :doc:`search-boost`
   * - ``"``
     - Phrase search (treats the enclosed text as a single phrase; can also be used instead of escaping)
     - :doc:`advanced-search`
   * - ``~``
     - Fuzzy search
     - :doc:`search-fuzzy`
   * - ``*`` ``?``
     - Wildcard search
     - :doc:`search-wildcard`
   * - ``:``
     - Specifies the search field
     - :doc:`search-field`
   * - ``\``
     - Escape character
     - (this page)
   * - ``/``
     - Slash (must be escaped when it appears in a URL, etc.)
     - :doc:`search-field`

Usage
-----

Escape with \ or enclose the search term in ".

::

    aaa\/bbb
    "aaa/bbb"

For example, if you want to search for "C++" as a search term, escape it as follows.

::

    C\+\+
    "C++"

Related Topics
---------------

- :doc:`search-field` - Field-specified search
- :doc:`search-wildcard` - Wildcard search
- :doc:`search-fuzzy` - Fuzzy search
- :doc:`advanced-search` - Advanced search options
