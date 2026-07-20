============
Fuzzy Search
============

Fuzzy Search (Approximate Search)
==================================

When you want to search for words that don't exactly match your search term, you can use fuzzy search (approximate search). This is useful when you want to include documents that don't match exactly due to typos, spelling variations, or other minor differences. |Fess| supports fuzzy search based on edit distance (Levenshtein distance), a measure of how different two words are.

Usage
-----

Add "~" after the search term to which you want to apply fuzzy search.

For example, to perform a fuzzy search for the word "Fess", enter the following in the search form to search for documents containing words similar to "Fess" (such as "Fes"):

::

    Fess~

You can specify the degree of fuzziness by adding a number from 0 to 2 after ``~``. The number represents the maximum edit distance allowed (the number of character insertions, deletions, or substitutions), and if omitted, the default edit distance is applied.

::

    Fess~1
    Fess~2

Specifying ``~2`` allows a search to match "Fess" with up to two characters of difference.

Related Topics
--------------

- :doc:`search-wildcard` - Wildcard search
- :doc:`special-char` - Special characters and escaping
