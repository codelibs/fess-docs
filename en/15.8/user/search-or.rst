=========
OR Search
=========

Use OR search to find documents that contain any of the specified search terms. When multiple words are entered in the search input field, the default is AND search.

Usage
-----

To use OR search, specify OR between search terms. OR must be written in uppercase letters with spaces before and after it.

For example, to search for documents containing either "term1" or "term2", enter the following in the search form:

::

    term1 OR term2

You can also connect three or more search terms with OR.

::

    term1 OR term2 OR term3

.. note::

    OR must be written in uppercase letters. If written in lowercase as ``or``, it is not treated as an operator but is searched as an ordinary search term "or". ``||`` can also be used with the same meaning as OR.

Using parentheses ``( )``, you can combine OR search with other search conditions. For example, to search for documents that contain either "term1" or "term2", and also contain "term3", enter the following:

::

    (term1 OR term2) term3

You can also perform an OR search by specifying a field. In the following example, it searches for documents that contain "term1" in the title field, or "term2" in the content field.

::

    title:term1 OR content:term2
