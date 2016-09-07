============
Field Search
============

Search with field
=================

|Fess| stores crawling data to each field, such as title and content, in the indexed document.
Since some of fields are searchable, you can search documents by the field.

Available fields
----------------

The default searchable fields are below.

+-----------------+------------------------------------------------+
| Field name      | Description                                    |
+-----------------+------------------------------------------------+
| url             | Crawled URL                                    |
+-----------------+------------------------------------------------+
| host            | Crawled host name                              |
+-----------------+------------------------------------------------+
| title           | Title of document                              |
+-----------------+------------------------------------------------+
| content         | Content of document                            |
+-----------------+------------------------------------------------+
| content_length  | Document size                                  |
+-----------------+------------------------------------------------+
| last_modified   | Last modified time of document                 |
+-----------------+------------------------------------------------+
| mimetype        | The MIME type of document                      |
+-----------------+------------------------------------------------+

Table: Searchable fields

For HTML document, title field is a value of title tag and content field is a value under body tag without tags.

Usage
-----

The format of Field search is colon-separated word, such as fieldname:searchword.
If field name is not specified, |Fess| searchs documents in values of title and content field.

To search documents that contains "fess" in title field:

::

    title:fess

To search documents that contains "fess" in url field:

::

    url:"*fess*"

