===========
Sort Search
===========

You can sort search results by specifying fields such as search date and time.

Sort Target Fields
------------------

By default, you can specify the following fields for sorting:

.. list-table::
   :header-rows: 1

   * - Field Name
     - Description
   * - created
     - Crawled date and time
   * - content_length
     - Crawled document size
   * - last_modified
     - Last modified date and time of the crawled document
   * - filename
     - File name
   * - score
     - Score value
   * - timestamp
     - Date and time when the document was indexed
   * - click_count
     - Number of times the document was clicked
   * - favorite_count
     - Number of times the document was favorited

Table: Sort Target Field List


You can also customize to add your own fields as sort targets.

Usage
-----

You can select sort conditions when searching. Sort conditions can be selected in the search options dialog displayed by clicking the Options button.

|image0|

To sort using the search field, enter "sort:field_name" in the search form, separating sort and the field name with a colon (:).

The following sorts documents containing fess by document size in ascending order:

::

    fess sort:content_length

To sort in descending order:

::

    fess sort:content_length.desc

To sort by multiple fields, specify them separated by commas:

::

    fess sort:content_length.desc,last_modified

.. |image0| image:: ../../../resources/images/ja/15.3/user/search-sort-1.png
.. pdf            :width: 300 px
