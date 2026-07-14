==================
Special Characters
==================

The following characters have a special meaning in the search query syntax, so they are treated as special characters in search terms. To use these characters as literal search characters, you need to escape them.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

These characters are used to invoke search features such as required/prohibited terms (``+`` ``-``), boolean operators (``&&`` ``||`` ``!``), grouping (``( )``), range search (``[ ]`` ``{ }``), boost search (``^``), phrase search (``"``), fuzzy search (``~``), wildcard search (``*`` ``?``), and field search (``:``).


Usage
-----

To treat a special character as a literal search character, use one of the following methods.

* Put ``\`` immediately before the character to escape it. The single character that follows is treated as a normal character instead of query syntax.
* Enclose the search term in ``"``. The enclosed string is treated as a phrase search, and the special characters inside it are not interpreted as query syntax. Note, however, that because it becomes a phrase search, features such as wildcard search (``*`` ``?``) are not available.

::

    aaa\/bbb
    "aaa/bbb"
