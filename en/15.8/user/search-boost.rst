============
Boost Search
============

Boost Search (Weighted Search)
===============================

Use boost search when you want to prioritize specific search terms among your search keywords. Boost search allows you to search according to the importance of each search term.

Usage
-----

To use boost search, specify a boost value (weighting value) in the format "^boost_value" immediately after the search term. Do not include a space between the search term and the boost value.

For example, if you want to prioritize "apple" when searching for "apple orange", enter the following in the search form:

::

    apple^100 orange

In this example, the boost value is applied only to "apple", not to "orange".

Boost Value
-----------

Specify a number for the boost value. You can specify not only integers but also decimals such as ``2.5``.

- Specifying a value greater than 1 increases the weight of that search term.
- Specifying a value greater than 0 and less than 1 (e.g., ``0.5``) decreases the weight of that search term.

The boost value does not determine the search result score in absolute terms; rather, it adjusts the relative weighting among search terms.

Combining with Other Search Syntax
-----------------------------------

Boost search can be combined with other search syntax. For example, you can also add a boost value to a search term that specifies a field.

::

    title:apple^100 orange

In this example, documents whose title field contains "apple" are prioritized.
