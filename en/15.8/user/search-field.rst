========================
Field-Specified Search
========================

Field-Specified Search
======================

By searching within a specific field (field-specified search), you can narrow your search to just the title, just the URL, and so on. Content crawled by |Fess| is stored in separate fields such as title and body. You can search by specifying these fields. By specifying fields, you can define detailed search conditions such as by document type or size.

Available Fields
----------------

By default, you can search using the following fields:

.. list-table::
   :header-rows: 1

   * - Field Name
     - Description
     - Data Type
   * - url
     - Crawled URL
     - Keyword
   * - host
     - Host name contained in the crawled URL
     - Keyword
   * - site
     - The URL with the scheme and query string removed (host name and path). Matched using prefix search
     - Keyword
   * - title
     - Title
     - Text
   * - content
     - Body text
     - Text
   * - content_length
     - Document size (in bytes)
     - Numeric
   * - last_modified
     - Last modified date and time of the document
     - Date
   * - timestamp
     - Registration date and time of the document (the crawl execution time, if the last modified date and time cannot be obtained)
     - Date
   * - mimetype
     - MIME type of the document (e.g., ``text/html``)
     - Keyword
   * - filetype
     - File type determined from the MIME type (e.g., ``html``, ``word``, ``pdf``; ``others`` if none apply)
     - Keyword
   * - filename
     - File name at the end of the URL path
     - Keyword
   * - label
     - Value of the label assigned to the document
     - Keyword
   * - lang
     - Language code of the document (e.g., ``ja``, ``en``)
     - Keyword
   * - anchor
     - Link destination URLs extracted from within the HTML page (web crawl only)
     - Keyword
   * - click_count
     - Number of times the document has been clicked
     - Numeric
   * - favorite_count
     - Number of times the document has been added as a favorite
     - Numeric

Table: Available Field List

"Data Type" indicates the difference in search method for each field.

* Keyword: Searches for an exact match against the entire value. It can also be combined with wildcard search or prefix search.
* Text: Performs full-text search against tokens split by morphological analysis, etc. This applies to fields such as title and content.
* Numeric/Date: You can use :doc:`Range-Specified Search <search-range>`.

If no field is specified, the search targets the title and content fields. Depending on the configuration, you can also add fields to be searched.

.. note::
    Depending on the crawl target, some fields may not have values registered. For example, anchor is registered only during web crawling, and lang is registered only when the HTML has a language attribute. Fields such as segment (a session ID representing the crawl execution unit) and doc_id (an internal ID assigned by the system) can also be specified, but they are not used in normal searches.

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

   url:https\:\/\/fess.codelibs.org\/ja\/15.8\/*
   url:"https://fess.codelibs.org/ja/15.8/*"

The first format supports wildcard search, so you can also write it as ``url:*\/\/fess.codelibs.org\/*``. The ":" and "/" characters contained in the URL are special characters in the search query, so escape them with ``\`` (see :doc:`special-char`). The second format does not support wildcard search, but a term ending in ``*`` is treated as a prefix (leading) match search.

.. tip::
    If you want to search using part of the URL, you can use ``inurl:`` to perform a partial match search against the URL. For example, ``inurl:15.8`` searches for documents whose URL contains ``15.8``.

When specifying a field whose value contains "/", such as mimetype, filetype, or site, enclose it in quotes as in ``mimetype:"text/html"``, or escape it as in ``mimetype:text\/html``.

For related search syntax, see also :doc:`Wildcard Search <search-wildcard>`, :doc:`Range-Specified Search <search-range>`, :doc:`Sort Search <search-sort>`, and :doc:`Special Characters <special-char>`.

Related Topics
--------------

- :doc:`search-range` - Range-specified search
- :doc:`search-wildcard` - Wildcard search
- :doc:`special-char` - Special characters and escaping
