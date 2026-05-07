============
Boost Search
============

Boost Search (Weighted Search)
===============================

Use boost search to prioritize specific search terms. Boost search enables searching based on the importance of search terms.

Usage
-----

To use boost search, specify a boost value (weighting value) in the format "^boost_value" after the search term.

For example, to search for "apple orange" with pages containing more instances of "apple" prioritized, enter the following in the search form:

::

    apple^100 orange

Specify an integer greater than or equal to 1 for the boost value.
