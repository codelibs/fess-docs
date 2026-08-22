==========
AND Search
==========

Use AND search to find documents that contain all of the specified search terms. When multiple words are separated by spaces in the search input field, the default is AND search, so you can omit AND and still get the same result.

Usage
-----

To use AND search, specify AND between search terms. AND must be written in uppercase letters with spaces before and after it. AND can also be omitted.

For example, to search for documents containing both "term1" and "term2", enter the following in the search form:

::

    term1 AND term2

You can also omit AND and write it as follows, which gives the same result:

::

    term1 term2

You can also connect three or more search terms with AND.

::

    term1 AND term2 AND term3

.. note::

    AND must be written in uppercase letters. If written in lowercase as ``and``, it is not treated as an operator but is searched as an ordinary search term "and". ``&&`` can also be used with the same meaning as AND.

Using parentheses ``( )``, you can combine AND search with other search conditions. For example, to search for documents that contain "term1", and also contain either "term2" or "term3", enter the following:

::

    term1 AND (term2 OR term3)

You can also perform an AND search by specifying a field. In the following example, it searches for documents that contain "term1" in the title field, and "term2" in the content field.

::

    title:term1 AND content:term2
