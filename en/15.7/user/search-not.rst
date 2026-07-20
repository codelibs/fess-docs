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

Instead of NOT, you can also place a ``-`` (hyphen) directly in front of the word you want to exclude. The following has the same meaning as the example above.

::

    term1 -term2

Related Topics
--------------

- :doc:`search-and` - AND search syntax
- :doc:`search-or` - OR search syntax
- :doc:`special-char` - Special characters and escaping
