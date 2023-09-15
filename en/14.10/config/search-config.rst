=======================
Search-Related Settings
=======================

The settings described below are specified in the `fess_config.properties` file. A restart of |Fess| is required after making changes.

Fuzzy Search
============

Fuzzy search is applied to words with 4 or more characters, allowing for 1-character differences to still result in matches. To disable this setting, specify `-1`.
::

    query.boost.fuzzy.min.length=-1

Search Timeout Value
====================

You can specify the search timeout value. The default value is 10 seconds.
::

    query.timeout=10000

Maximum Character Count for Searches
====================================

You can specify the maximum character count for searches. The default value is 1000 characters.
::

    query.max.length=1000

Search Timeout Logging
======================

This setting controls log output when a timeout occurs during a search. The default value is `true (enabled)`.
::

    query.timeout.logging=true

Display Total Hits
==================

Specify this when you need to display more than 10,000 hits. By default, it will be displayed as follows when there are more than 10 million hits:

`xxxxx Search Results Approximately 10,000 or more items 1 - 10 items (4.94 seconds)`
::

    query.track.total.hits=10000

Index Name for Geospatial Searches
==================================

Specify the index name for geospatial searches. The default value is `location`.
::

    query.geo.fields=location

Language Specification in Request Parameters
============================================

Specify the parameter name for language selection in request parameters. For example, if you pass `browser_lang=en` as a request parameter in the URL, the display language will switch to English.
::

    query.browser.lang.parameter.name=browser_lang

Prefix Query for Prefix Search
==============================

When specified with `〜*` during an exact match search, it performs a prefix search. The default value is `true (enabled)`.
::

    query.replace.term.with.prefix.query=true

Highlight Characters
====================

Use the specified characters here to separate sentences and achieve natural highlighting. The specified characters should be Unicode characters starting with "u" as the delimiter.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

The default value is set as follows (decoded conversion):

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Highlight Fragments
===================

Specify the number of characters and the number of fragments for highlights obtained from OpenSearch.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Highlight Generation Method
===========================

Specify the highlight generation method for OpenSearch.
::

    query.highlight.type=fvh

Tags for Highlighting
=====================

Specify the starting and ending tags for highlighting.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

Values to Pass to OpenSearch Highlighter
========================================

Specify the values to pass to the OpenSearch highlighter.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

..
    TODO
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
        query.max.search.result.offset=100000
        query.additional.default.fields=


Field Names to Add
==================

Specify field names to add when adding search field names or facet field names.
::

    query.additional.search.fields=
    query.additional.facet.fields=

..
    TODO
        query.additional.sort.fields=
        query.additional.analyzed.fields=
        query.additional.not.analyzed.fields=


Settings for Obtaining Search Results in GSA-Compatible XML Format
==================================================================

Used when obtaining search results in GSA-compatible XML format.

Specify field names to add to the response when using GSA-compatible XML format.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

Specify the language when using GSA-compatible XML format.
    ::

        query.gsa.default.lang=en

Specify the default sort when using GSA-compatible XML format.
    ::

        query.gsa.default.sort=

