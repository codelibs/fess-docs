============
Fuzzy Search
============

Fuzzy Search
============

|Fess| supports Fuzzy search based on the Levenshtein Distance or Edit Distance algorithm.

Usage
-----

Fuzzy search syntax is word~number, such as Apple~0.8.
The number is beween 0 and 1, with a value closer to 1 only terms with a higher similarity will be matched.



To search documents which contains words close to Solr, the query is as below.

::

    Solr~0.8

If no fuzzy value, the default is 0.5.
