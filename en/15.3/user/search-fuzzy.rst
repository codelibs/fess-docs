============
Fuzzy Search
============

Fuzzy Search (Approximate Search)
==================================

Fuzzy search is available when you want to search for words that do not exactly match the search term. |Fess| supports fuzzy search based on Levenshtein distance.

Usage
-----

Add "~" after the search term to which you want to apply fuzzy search.

For example, to perform a fuzzy search for the word "Fess", enter the following in the search form to search for documents containing words similar to "Fess" (such as "Fes"):

::

    Fess~
