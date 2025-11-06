================
Wildcard Search
================

You can use single-character or multiple-character wildcards within search terms. ? can be specified as a single-character wildcard, and \* can be specified as a multiple-character wildcard. Wildcards apply to words. Wildcard searches on phrases are not supported.

Usage
-----

To use a single-character wildcard, use ? as follows:

::

    te?t

In the above case, it is treated as a single-character wildcard, such as text or test.

To use a multiple-character wildcard, use \* as follows:

::

    test*

In the above case, it is treated as a multiple-character wildcard, such as test, tests, or tester. You can also use it within a search term:

::

    te*t

Usage Conditions
----------------

Wildcards are used on strings registered in the index.
Therefore, if an index is created with bi-gram or similar methods, Japanese text is treated as fixed-length strings without meaning, so wildcards do not work as expected in Japanese.
When using wildcards in Japanese, use them in fields that utilize morphological analysis.
