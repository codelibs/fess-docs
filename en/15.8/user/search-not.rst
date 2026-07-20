==========
NOT Search
==========

NOT search can be used to search for documents that do not contain a specific word. This is also called exclusion search, and it's useful when you want to reduce noise by excluding specific keywords from your search results.

Usage
-----

For NOT search, place NOT before the word to exclude. NOT must be in uppercase letters with spaces before and after it.

For example, to search for documents that contain "term1" but do not contain "term2", enter the following:

::

    term1 NOT term2

.. note::

    NOT must be written in uppercase letters. If written in lowercase as ``not``, it is not treated as an operator but is searched as an ordinary search term "not". Also, placing ``-`` directly before the word to exclude, as in ``term1 -term2``, has the same meaning as NOT.

Using parentheses ``( )``, you can combine NOT search with other search conditions. For example, to search for documents that contain either "term1" or "term2", but do not contain "term3", enter the following:

::

    (term1 OR term2) NOT term3

You can also perform a NOT search by specifying a field. In the following example, it searches for documents that contain "term1" in the title field, but do not contain "term2" in the title field.

::

    title:term1 NOT title:term2

Related Topics
--------------

- :doc:`search-and` - AND search syntax
- :doc:`search-or` - OR search syntax
- :doc:`special-char` - Special characters and escaping
