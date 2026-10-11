==================================
Wikipedia Connector
==================================

Overview
========

The Wikipedia Connector provides functionality to read a Wikipedia dump file
and register its pages in the |Fess| index.
It works with the dumps of Wikipedia, other Wikimedia projects and any MediaWiki site.

This feature requires the ``fess-ds-wikipedia`` plugin.

Supported Dumps
===============

The ``source`` parameter selects the dump format.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - Description
   * - ``cirrus``
     - A CirrusSearch index dump, which Wikimedia publishes for its wikis under
       ``https://dumps.wikimedia.org/other/cirrus_search_index/``. It carries the text that MediaWiki itself rendered, with templates expanded,
       so no wikitext markup reaches the index. This is the recommended format for Wikipedia and other Wikimedia wikis
   * - ``xml``
     - A MediaWiki XML export (``*-pages-articles.xml.bz2``, or the output of ``Special:Export`` or ``dumpBackup.php`` of any MediaWiki).
       It carries wikitext, which the connector converts to plain text (see "Plain Text of XML Dumps")
   * - ``auto``
     - The default. A location that contains ``cirrus_search_index`` or ends with ``.json.bz2`` or ``.json`` is read as ``cirrus``; any other location is read as ``xml``

The compression of a dump (such as bzip2 or gzip) is detected from its content, and an uncompressed file can be read as well.

Prerequisites
=============

1. Plugin installation is required
2. A dump file must be reachable, either as an HTTP(S) URL or as a path on the |Fess| server
3. Time for the crawl: the dump of a large Wikipedia is several gigabytes. Use ``limit`` to try a configuration first

Plugin Installation
-------------------

Install from "System" -> "Plugins" in the admin console, or run ``bin/fess-setup install plugin fess-ds-wikipedia``
and restart |Fess|.
See :doc:`../../admin/plugin-guide` for details.

Configuration
=============

Configure in the admin console under "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - Japanese Wikipedia
   * - Handler Name
     - WikipediaDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``url``
     - No
     - Location of the dump: an HTTP(S) URL, a ``file:`` URL or a local path. The default is the English Wikipedia dump
       (``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``), so specify this parameter explicitly.
       For ``source=cirrus``, see "CirrusSearch Dumps" for the forms that can be specified
   * - ``source``
     - No
     - ``auto``, ``cirrus`` or ``xml`` (default: ``auto``)
   * - ``limit``
     - No
     - Stop after this many pages. ``0`` means no limit (default: ``0``). Use it to try a configuration on a small number of pages
   * - ``user_agent``
     - No
     - User-Agent header sent when downloading the dump. If not specified, the User-Agent name of the |Fess| crawler is used
   * - ``max_digest_length``
     - No
     - Maximum length of ``digest``, in characters (default: ``100``)
   * - ``total_entity_size_limit``
     - No
     - Upper limit, in bytes, on the total size of the entities that the XML parser processes (default: ``100000000``). Applied to ``source=xml`` only
   * - ``text_extractor``
     - No
     - How the wikitext of an XML dump is converted to plain text: ``sweble`` (default) or ``regex``. See "Plain Text of XML Dumps"
   * - ``drop_templates``
     - No
     - Comma-separated template names whose text is dropped from the content of an XML dump, or ``*`` for all templates
   * - ``keep_templates``
     - No
     - Comma-separated template names whose text is kept although ``drop_templates`` matches them
   * - ``drop_captions``
     - No
     - Drop the captions of images and galleries from the content of an XML dump (default: ``false``)

CirrusSearch Dumps
~~~~~~~~~~~~~~~~~~

A CirrusSearch dump is published as numbered chunks, such as ``jawiki_content-20261004-00000.json.bz2``.
For ``source=cirrus``, ``url`` accepts a comma-separated list whose entries can each be:

- a single file (an HTTP(S) URL or a local path)
- a local directory: every file in it whose name ends with ``.json.bz2`` or ``.json`` is read, in name order
- an HTTP(S) URL that ends with ``/``: the directory listing is fetched and every file whose name ends with ``.json.bz2`` or ``.json`` is read, in name order

For example, to read all chunks of the content index of the Japanese Wikipedia:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimedia removes old dates from the server. Look up an existing date in the listing at
   ``https://dumps.wikimedia.org/other/cirrus_search_index/`` before you configure the crawl.

Script Configuration
--------------------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Available Fields
~~~~~~~~~~~~~~~~

The following values can be referenced from the script.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Page ID
   * - ``title``
     - Page title
   * - ``encodedTitle``
     - The title in the form used in a MediaWiki page URL (spaces become ``_`` and other characters are percent-encoded)
   * - ``content``
     - Plain text of the page
   * - ``digest``
     - ``content`` abbreviated to ``max_digest_length`` characters
   * - ``contentLength``
     - Length of ``content``
   * - ``wikitext``
     - Wikitext of the page, if the dump carries it
   * - ``format``, ``model``
     - Format and content model of the page
   * - ``timestamp``
     - Timestamp of the page
   * - ``ns``
     - Namespace number
   * - ``categories``, ``links``
     - Categories of the page and the pages it links to
   * - ``redirect``, ``redirectTitle``
     - Whether the page is a redirect, and its target
   * - ``stub``, ``disambiguation``
     - Whether the page is a stub, and whether it is a disambiguation page
   * - ``lang``, ``host``, ``site``, ``url``
     - Derived from the dump location. See "Values Derived From the Dump Location"

For ``source=cirrus``, the following values are available in addition:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``openingText``
     - The opening text of the page
   * - ``headings``
     - Headings
   * - ``externalLinks``
     - External links
   * - ``templates``
     - Templates used by the page
   * - ``redirects``
     - Titles that redirect to the page
   * - ``auxiliaryText``
     - Auxiliary text, such as image captions
   * - ``weightedTags``
     - Weighted tags
   * - ``wikibaseItem``
     - Wikidata item ID
   * - ``incomingLinks``
     - Number of incoming links
   * - ``popularityScore``
     - Popularity score
   * - ``revisionId``
     - Revision ID

Values Derived From the Dump Location
-------------------------------------

``lang``, ``host``, ``site`` and ``url`` are derived from the name of the dump: a name such as ``jawiki-latest-pages-articles.xml.bz2``
or ``index_name=jawiki_content`` gives ``lang`` ``ja``, ``host`` and ``site`` ``ja.wikipedia.org`` and ``url`` ``https://ja.wikipedia.org/wiki/<encoded title>``.
The name must contain the language code immediately followed by ``wiki`` and then ``-``, ``_`` or ``.``.
Sister projects such as Wikiquote (``jawikiquote-...``) are not derived on purpose, because a wrong host would produce dead links.

.. warning::

   When the name of the dump does not match, ``host``, ``site`` and ``url`` are not set, and ``url`` keeps the value of the ``url`` parameter,
   which is the location of the dump. If the script uses ``url`` as it is, every page gets the same URL, and the whole crawl ends up as a single document in the index,
   with no error.
   For a renamed dump or another Wikimedia project, build the URL in the script, as the example above does, for example
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``.

Plain Text of XML Dumps
-----------------------

For ``source=xml``, the wikitext is converted to plain text with the Sweble wikitext parser. The namespace names are read from the ``<siteinfo>`` of the export,
so images and category statements are recognized in any language (``[[ファイル:...]]``, ``[[Kategorie:...]]``) and in wikis with their own namespace names.
A page that Sweble fails on is converted with regular expressions instead.

``text_extractor=regex`` uses regular expressions for every page. It is several times faster, but nested templates, tables and multi-line markup remain in the text.

By default, the text of every template argument (without the parameter names) and every image and gallery caption is kept in ``content``, so that this text can be found.
Use ``drop_templates``, ``keep_templates`` and ``drop_captions`` to filter it:

::

    # Drop the text of these templates, also when nested ("*" drops all templates)
    drop_templates=Cite web,Cite news,Use dmy dates
    # Keep these templates although drop_templates matches them
    # (drop_templates=* with keep_templates=Note,Warning keeps only those two)
    keep_templates=
    # Drop image and gallery captions
    drop_captions=false

Template names are matched the way MediaWiki resolves them: the first letter is case-insensitive, ``_`` equals a space, and the ``Template:`` prefix is optional.
Templates are not expanded, so a kept template contributes the text of its arguments, not what MediaWiki would render.
A CirrusSearch dump already contains the text rendered by MediaWiki, so these parameters do not apply to ``source=cirrus``.

Usage Examples
==============

Japanese Wikipedia From a CirrusSearch Dump
-------------------------------------------

Parameters:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

Script:

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Japanese Wikipedia From an XML Dump, Without Citation Templates
---------------------------------------------------------------

Parameters:

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

The script is the same as in "Script Configuration".

Another Wikimedia Project (Wikiquote)
-------------------------------------

The dump name ``jawikiquote-...`` does not give ``host`` and ``url``, so build them in the script.

Script:

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

Troubleshooting
===============

Only One Document Is Indexed
----------------------------

See "Values Derived From the Dump Location". Check that the script sets ``url`` for every page.

The Crawl Takes Too Long
------------------------

1. Start with ``limit`` to confirm the configuration
2. Use ``source=cirrus``, or ``text_extractor=regex`` for an XML dump
3. Place the dump on the |Fess| server and specify a local path

Wikitext Markup Remains in the Content
--------------------------------------

Use a CirrusSearch dump (``source=cirrus``). With ``source=xml``, ``text_extractor=regex`` leaves nested templates, tables and multi-line markup in the text, so use ``sweble`` (the default).

The Dump Cannot Be Read
-----------------------

1. Check that the URL or path is correct (the date of a CirrusSearch dump may have been removed from the server)
2. For a directory URL, check that it ends with ``/`` and that the files in it end with ``.json.bz2`` or ``.json``
3. Check the log for the exact error

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../../admin/plugin-guide` - Plugin Management Guide
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
