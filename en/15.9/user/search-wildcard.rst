================
Wildcard Search
================

You can use single-character or multiple-character wildcards within search terms. ? can be specified as a single-character wildcard, and \* can be specified as a multiple-character wildcard. Wildcards apply to words. Wildcard searches on phrases are not supported.

Usage
-----

To use a single-character wildcard, use ? as follows:

::

    te?t

In the above case, this matches any single character at the position of ?, as in text or test.

To use a multiple-character wildcard, use \* as follows:

::

    test*

In the above case, this matches zero or more arbitrary characters at the position of \*, as in test, tests, or tester. You can also use it in the middle of a search term, as shown below:

::

    te*t

Furthermore, you can use a wildcard at the beginning of a search term, as shown below:

::

    *test

You can also perform a wildcard search on a specific field. In the following example, documents containing a word in the title field that starts with te and ends with t are searched for.

::

    title:te*t

If you do not specify a field, wildcard search is performed on the title and content fields.

Usage Conditions
----------------

Please note the following points when using wildcard search.

* Wildcards match strings (tokens) registered in the index. Since the search term is not re-analyzed, if the index was created using bi-gram or similar methods, Japanese text is treated as fixed-length strings without meaning, and wildcards in Japanese will not work as expected. When using wildcards in Japanese, use them on fields that utilize morphological analysis.
* Wildcard patterns are case-sensitive. Since words registered in the index are usually converted to lowercase, use lowercase letters in your patterns. For example, ``Test*`` does not match ``test``, which is registered in lowercase.
* A search with a wildcard at the beginning (for example, ``*test``) scans all words in the index, so it may take longer to process.
