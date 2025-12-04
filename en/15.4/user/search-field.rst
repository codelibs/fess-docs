========================
Field-Specified Search
========================

Field-Specified Search
======================

Content crawled by |Fess| is stored in separate fields such as title and body. You can search by specifying these fields. By specifying fields, you can define detailed search conditions such as by document type or size.

Available Fields
----------------

By default, you can search using the following fields:

.. list-table::
   :header-rows: 1

   * - Field Name
     - Description
   * - url
     - Crawled URL
   * - host
     - Host name contained in the crawled URL
   * - title
     - Title
   * - content
     - Body text
   * - content_length
     - Crawled document size
   * - last_modified
     - Last modified date and time of the crawled document
   * - mimetype
     - Document MIME type

Table: Available Field List


If no field is specified, the search targets the title and content fields.
You can also add custom fields to make them searchable.

For HTML files, the title tag is stored in the title field, and the text under the body tag is stored in the content field.

Usage
-----

To perform a field-specified search, enter "field_name:search_term" in the search form, separating the field name and search term with a colon (:).

To search for fess in the title field, enter:

::

    title:fess

The above search displays documents containing fess in the title field.

To search the url field, enter:

::

   url:https\:\/\/fess.codelibs.org\/ja\/15.4\/*
   url:"https://fess.codelibs.org/ja/15.4/*"

The first format allows wildcard queries, so you can also write it as ``url:*\/\/fess.codelibs.org\/*``. The ":" and "/" characters in URLs are reserved words and must be escaped. The second format does not support wildcard queries but supports prefix queries.
