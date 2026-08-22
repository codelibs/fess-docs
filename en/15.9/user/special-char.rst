==================
Special Characters
==================

The following characters have a special meaning in the search query syntax, so they are treated as special characters in search terms. To use these characters as literal search characters, you need to escape them.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

These characters are used to invoke search features such as required/prohibited terms (``+`` ``-``), boolean operators (``&&`` ``||`` ``!``), grouping (``( )``), range search (``[ ]`` ``{ }``), boost search (``^``), phrase search (``"``), fuzzy search (``~``), wildcard search (``*`` ``?``), and field search (``:``).

For example, searching directly for a "/" or ":" in a URL or file path, or a "+" or "-" in program code, can produce unexpected search results. See below for how to escape these characters.

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

To treat a special character as a literal search character, use one of the following methods.

* Put ``\`` immediately before the character to escape it. The single character that follows is treated as a normal character instead of query syntax.
* Enclose the search term in ``"``. The enclosed string is treated as a phrase search, and the special characters inside it are not interpreted as query syntax. Note, however, that because it becomes a phrase search, features such as wildcard search (``*`` ``?``) are not available.

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
