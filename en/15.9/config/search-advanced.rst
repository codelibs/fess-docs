=======================
Search-Related Settings
=======================

The settings described below are specified in fess_config.properties.
|Fess| must be restarted after changes.

Fuzzy Search
============

Fuzzy search is applied to keywords of 4 or more characters, matching results that differ by one character.
To disable this setting, specify ``-1``.
::

    query.boost.fuzzy.min.length=-1

The default value is ``4``. For detailed fuzzy search settings, see "Relevance (Boost) Settings" below.

Search Timeout Value
====================

You can specify the timeout value for searches in milliseconds.
The default is 10 seconds (10000 milliseconds).
::

    query.timeout=10000

Maximum Query Length
====================

You can specify the maximum number of characters in a search query.
Search queries exceeding this length are not accepted.
The default is 1000 characters.
::

    query.max.length=1000

Search Timeout Logging
======================

Whether to log searches whose results are incomplete because the query timed out or a shard failed.
When enabled, a WARN log line is written in the following cases:

- ``[SEARCH TIMEOUT]``: the query timeout (``query.timeout``) elapsed and the search engine stopped collecting results.
- ``[SEARCH SHARD FAILURE]``: one or more shards failed.

When both happen, both lines are written.
Each line contains ``exec_time`` (milliseconds), the request and the full response.
For a shard failure, the reason is in ``_shards.failures`` of that response; the search engine itself logs it only at DEBUG level.
The default is ``true`` (enabled).
::

    query.timeout.logging=true

Hit Count Display
=================

Specifies the upper limit for the exact hit count to be counted.
By default, when there are more than 10,000 hits, the result is displayed as follows:

``Search results for xxxxx: approximately 10,000 or more, 1 - 10 of (4.94 seconds)``

Specify a larger value when you need to display exact hit counts exceeding 10,000.
::

    query.track.total.hits=10000

.. note::
   Setting a large value may affect search performance. Set an appropriate value according to your usage.

Maximum Search Result Offset
=============================

Specifies the upper limit for the offset (search start position) that can be retrieved in search results.
If an offset exceeding this value is specified, the search will return an error.
This functions as the upper limit for deep page navigation via paging.
The default is 100000.
::

    query.max.search.result.offset=100000

OR Search Re-Search Threshold
==============================

When the number of hits from a normal search is less than or equal to the value specified here,
the search is re-executed with the search operator switched to OR.
This allows results to be supplemented even when an AND search yields few hits.
The default is ``-1``, which disables this feature.
::

    query.orsearch.min.hit.count=-1

Field Name for Geolocation Search
==================================

Specifies the field name to use for geolocation searches.
To specify multiple fields, separate them with commas.
The default is ``location``.
::

    query.geo.fields=location

For details on how to use geolocation search, refer to :doc:`search-geosearch`.

Request Parameter Language Specification
=========================================

Specifies the parameter name used for language specification via request parameters.
For example, passing ``browser_lang=en`` as a request parameter in the URL switches the display language to English.
::

    query.browser.lang.parameter.name=browser_lang

Default Search Language
========================

Specifies the default language(s) to use at search time, separated by commas.
When a value is set, it takes precedence over the language specified by request parameters or the browser.
The default is empty (unspecified), which means the request parameter or browser language is used.
::

    query.default.languages=

Language Code Mapping
=====================

Specifies normalization mappings for language codes used during search.
Language codes passed from the browser or request are converted to the language codes used internally by |Fess|.
These normally do not need to be changed. The default value defines mappings for major languages.
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

Prefix Query Specification
===========================

When a search term ends with ``*`` (e.g., ``search*``), that term is searched as a prefix query.
The default is ``true`` (enabled). Specifying ``false`` causes terms ending with ``*`` to be searched as-is.
::

    query.replace.term.with.prefix.query=true

Highlight String
================

The string specified here is used to split sentences to achieve natural highlight display.
The specified string uses u as the start delimiter, followed by Unicode character codes.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

The default setting is as follows (decoded):

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Highlight Fragment
==================

Specifies the number of characters in highlight fragments and the number of fragments retrieved from OpenSearch.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Highlight Generation Method
============================

Specifies the OpenSearch highlight generation method.
::

    query.highlight.type=fvh

Highlight Tags
==============

Specifies the opening and closing tags for highlights.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

Values Passed to OpenSearch Highlighter
========================================

Specifies values passed to the OpenSearch highlighter.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

Advanced Highlight Settings
============================

Settings to control the detailed behavior of highlighting.
::

    query.highlight.force.source=false
    query.highlight.fragmenter=span
    query.highlight.fragment.offset=-1
    query.highlight.no.match.size=0
    query.highlight.order=score
    query.highlight.phrase.limit=256
    query.highlight.content.description.fields=hl_content,digest
    query.highlight.boundary.position.detect=true
    query.highlight.text.fragment.type=query
    query.highlight.text.fragment.size=3
    query.highlight.text.fragment.prefix.length=5
    query.highlight.text.fragment.suffix.length=5

Field Names to Add to Response
===============================

Specifies field names to add to responses for normal searches or API searches.
Each setting corresponds to the response for normal search, API (JSON/GSA) search, scroll search, and cache display respectively.
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

.. note::

   ``query.additional.api.response.fields`` only adds fields to the list of fields that may be
   written to the search API (``/api/v2/search``) response. On its own, it does not make a field
   appear in the response. The search API fetches the same fields from the search engine as a normal
   search, including those in ``query.additional.response.fields``, and returns only the fetched fields
   that are on that list. To include a custom field in the search API response, specify the same field
   name in both settings.

   ::

       query.additional.response.fields=category
       query.additional.api.response.fields=category

For details on scroll search response fields, refer to :doc:`search-scroll`.

Adding Field Names
==================

Specify when adding search field names, facet field names, sort target field names, and so on.
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

The meaning of each setting is as follows:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Setting
     - Description
   * - ``query.additional.default.fields``
     - Adds fields to the default fields searched by queries without a field specification.
   * - ``query.additional.search.fields``
     - Adds fields that can be searched by specifying a field name.
   * - ``query.additional.facet.fields``
     - Adds fields that can be used as facets.
   * - ``query.additional.sort.fields``
     - Adds fields that can be used as sort targets.
   * - ``query.additional.highlighted.fields``
     - Adds fields to be included in highlighting.
   * - ``query.additional.analyzed.fields``
     - Adds fields to be treated as analyzer-analyzed fields.
   * - ``query.additional.not.analyzed.fields``
     - Adds fields that are not analyzed by the analyzer.

.. _search-custom-field-facet-sort-range:

Using a Custom Field for Facets, Sorting and Range Search
---------------------------------------------------------

A field that a data store script or a crawl configuration adds, such as ``category`` or ``price``,
has no definition in the index mapping. OpenSearch creates one from the first value it indexes for
that field:

- A string becomes a ``text`` field, with a ``keyword`` sub-field named ``<field>.keyword``
  (strings longer than 256 characters are not stored in the sub-field).
- A number becomes a numeric field: ``long`` for a whole number, ``float`` for a number with a
  fraction. The JavaScript engine hands every number over as a floating-point value, so a value
  converted with ``parseInt`` becomes ``float`` as well.

Each use needs the right one:

.. list-table::
   :header-rows: 1
   :widths: 15 45 40

   * - Use
     - Field to use
     - Setting
   * - Facet
     - ``<field>.keyword``. A facet on the ``text`` field itself fails with ``400``.
     - ``query.additional.facet.fields``
   * - Sort
     - A numeric (or date) field. The sort value is ``<field>.asc`` or ``<field>.desc``, so a field
       name containing a dot, such as ``<field>.keyword``, cannot be sorted on, and a sort on a
       ``text`` field fails with ``400``.
     - ``query.additional.sort.fields``
   * - Range search
     - A numeric (or date) field. On a string field the bounds are compared as text:
       ``price:[1000 TO 5000]`` also matches ``120000``, without an error.
     - ``query.additional.search.fields``. A field that is not listed is not searched as a
       range at all.

A value read from CSV, JSON or a database is a string unless the script converts it, so convert the
values you want to sort or search by range. With the JavaScript engine, the default for data store
configurations created in 15.9 (``script_type=javascript``)::

    url="https://example.com/product/" + id
    title=name
    content=description
    category=category
    price=parseInt(price, 10)

Define a numeric field in the index mapping before the first document that has it is indexed. The
``float`` type that is created otherwise keeps only about seven significant digits, and a whole
number above 16,777,216 may be rounded to a nearby value: a document whose ``price`` is ``20000001``
matches ``price:[20000000 TO 20000000]``, and sorting cannot tell the two apart. Use ``long`` for
whole numbers and ``double`` for decimals.

1. Add the field to the current document index through the ``fess.update`` alias.

   ::

       $ curl -X PUT http://localhost:9200/fess.update/_mapping -H 'Content-Type: application/json' \
           -d '{"properties":{"price":{"type":"long"}}}'

2. Add the same definition under ``properties`` in ``app/WEB-INF/classes/fess_indices/fess/doc.json``
   of the installation, so that a document index |Fess| creates later (on the first start against an
   empty cluster, or by a reindex on the :doc:`../admin/maintenance-guide` page) has it too. An
   upgrade replaces ``doc.json`` with the file of the new version, so add the definition again
   after upgrading.

   ::

       "properties": {
         "price": {
           "type": "long"
         },
         "anchor": {
           "type": "keyword"
         },
         ...

Then list the fields in ``fess_config.properties`` and restart |Fess|::

    query.additional.search.fields=price
    query.additional.facet.fields=category.keyword
    query.additional.sort.fields=price

The fields can then be used through the search API::

    $ curl -G http://localhost:8080/api/v2/search --data-urlencode 'q=price:[1000 TO 5000]' \
        --data-urlencode 'facet.field=category.keyword' --data-urlencode 'sort=price.desc'

.. note::

   The type of a field is fixed when the first document that has it is indexed, and the mapping
   API cannot change it afterwards. To change the type of a field that is already indexed, as a
   string or as ``float``, add the definition to ``doc.json`` as in step 2 above, then run Reindex
   on the :doc:`../admin/maintenance-guide` page with Update Aliases enabled. The documents are
   copied into a new index created from ``doc.json``.

.. note::

   The search screen bundled with |Fess| (the static theme ``bootstrap``) draws only the ``label``
   facet (and the facet queries of ``query.facet.queries``), and its sort menu offers only the
   standard fields. Facets on other fields are available through the API or in a theme of your
   own. A range search, and a sort written in the search box as ``sort:price.desc``, work on the
   search screen as well.

Similar Document Collapsing (collapse)
=======================================

Settings for the collapse feature that folds similar (near-duplicate) documents using the ``content_minhash_bits`` field.
``query.collapse.inner.hits.name`` is the field name that stores similar documents within search results,
``query.collapse.inner.hits.size`` is the number of similar documents to retrieve per group (``0`` means none are retrieved),
``query.collapse.inner.hits.sorts`` is the sort condition for retrieving similar documents, and
``query.collapse.max.concurrent.group.results`` is the maximum number of concurrent requests when retrieving groups.
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

Search Preference
=================

Specifies the preference (value that determines which shard to search) passed to OpenSearch during JSON API searches.
Specifying ``_query`` causes the hash value of the search query to be used as the preference, routing identical queries to the same shard.
The default is ``_query``.
::

    query.json.default.preference=_query

Relevance (Boost) Settings
============================

Specifies the boost values used for relevance (score) calculation during searches.
Settings with ``.lang`` are boost values for language-specific fields (e.g., ``content_ja``).
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

The boost values and behavior for fuzzy search are specified as follows.
``query.boost.fuzzy.min.length`` is the minimum number of characters required to apply fuzzy search (``-1`` to disable).
::

    query.boost.fuzzy.min.length=4
    query.boost.fuzzy.title=0.01
    query.boost.fuzzy.title.fuzziness=AUTO
    query.boost.fuzzy.title.expansions=10
    query.boost.fuzzy.title.prefix_length=0
    query.boost.fuzzy.title.transpositions=true
    query.boost.fuzzy.content=0.005
    query.boost.fuzzy.content.fuzziness=AUTO
    query.boost.fuzzy.content.expansions=10
    query.boost.fuzzy.content.prefix_length=0
    query.boost.fuzzy.content.transpositions=true

Query Type Settings
===================

Specifies the type of query to use during searches and the detailed behavior of each.
``query.default.query_type`` is the default query type to use,
``query.dismax.tie_breaker`` is the tie breaker value for dismax queries, and
``query.bool.minimum_should_match`` is the minimum_should_match value for bool queries (left empty means unspecified).
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

Prefix and Fuzzy Query Detailed Settings
=========================================

Specifies the detailed behavior of prefix queries and fuzzy queries.
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

Facet Settings
==============

Specifies the default behavior of faceted search.
``query.facet.fields`` is the field to use for faceting,
``query.facet.fields.size`` is the upper limit of facets to retrieve,
``query.facet.fields.min_doc_count`` is the minimum document count to display in a facet,
``query.facet.fields.sort`` is the sort order for facets, and
``query.facet.fields.missing`` is the value assigned to documents without a value.
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

The search screen bundled with |Fess| requests only the ``label`` facet, whatever
``query.facet.fields`` says; see :ref:`search-custom-field-facet-sort-range`.

Settings for Retrieving Search Results in GSA-Compatible XML Format
====================================================================

Used when retrieving search results in GSA-compatible XML format.

Specify field names to add to responses when using GSA-compatible XML format.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

Specify language when using GSA-compatible XML format.
    ::

        query.gsa.default.lang=en

Specify default sort when using GSA-compatible XML format.
    ::

        query.gsa.default.sort=

Specify metadata prefix when using GSA-compatible XML format.
    ::

        query.gsa.meta.prefix=MT_

Specify charset field when using GSA-compatible XML format.
    ::

        query.gsa.index.field.charset=charset

Specify content_type field when using GSA-compatible XML format.
    ::

        query.gsa.index.field.content_type.=content_type

Specify default preference when using GSA-compatible XML format.
    ::

        query.gsa.default.preference=_query
