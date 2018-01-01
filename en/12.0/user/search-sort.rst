====
Sort
====

Sort
====

To select sort field in Search Options dialog, the search results are sorted by the field.

Sort field
----------

The following sort fields are available.

+-----------------+------------------------------------------------+
| Field name      | Description                                    |
+-----------------+------------------------------------------------+
| created         | Time to crawl document                         |
+-----------------+------------------------------------------------+
| content_length  | Size of document                               |
+-----------------+------------------------------------------------+
| last_modified   | Last modified time of document                 |
+-----------------+------------------------------------------------+
| filename        | File name                                      |
+-----------------+------------------------------------------------+
| score           | Score value                                    |
+-----------------+------------------------------------------------+
| timestamp       | Indexed time                                   |
+-----------------+------------------------------------------------+
| click_count     | The number of clicked documents                |
+-----------------+------------------------------------------------+
| favorite_count  | The number of liked documents                  |
+-----------------+------------------------------------------------+

Table: Sort fields

Usage
-----

To click Options button, Sort fields are selectable on Search Options dialog.

|image0|

In addition to selecting sort field on the dialog, sort prefix operator is available in query syntax. 
The format is colon-separated query, such as sort:fieldname.

To sort search results which contains fess by content size, the query is below.

::

    fess sort:content_length

To sort in descending order as below.

::

    fess sort:content_length.desc

If you want to sort by multiple sort fields, it's below.

::

    fess sort:content_length.desc,last_modified

.. |image0| image:: ../../../resources/images/en/12.0/user/search-sort-1.png
