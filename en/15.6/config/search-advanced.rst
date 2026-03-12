=======================
Search-Related Settings
=======================

The settings described below are specified in fess_config.properties.
|Fess| must be restarted after changes.

Fuzzy Search
============

Fuzzy search is applied to keywords of 4 or more characters, matching one character difference.
To disable this setting, specify ``-1``.
::

    query.boost.fuzzy.min.length=-1

Search Timeout Value
====================

You can specify the timeout value for searches.
The default is 10 seconds.
::

    query.timeout=10000

Maximum Query Length
====================

You can specify the maximum query length.
The default is 1000 characters.
::

    query.max.length=1000

Search Timeout Logging
======================

Log output setting when search timeouts occur.
The default is ``true (enabled)``.
::

    query.timeout.logging=true

Hit Count Display
=================

Specify this when you need to display hit counts of more than 10,000.
By default, when there are more than 10,000 hits, it displays as follows:

`xxxxx search results Approximately 10,000 or more 1 - 10 of (4.94 seconds)`

::

    query.track.total.hits=10000

Index Name for Geolocation Search
==================================

Specifies the index name for geolocation search.
The default is ``location``.
::

    query.geo.fields=location

Request Parameter Language Specification
=========================================

Specifies the parameter name for language specification via request parameters.
For example, passing ``browser_lang=en`` as a request parameter in the URL switches the display language to English.
::

    query.browser.lang.parameter.name=browser_lang

Prefix Query Specification
===========================

When searching with exact match using ``~\*``, search as a prefix query.
The default is ``true (enabled)``.
::

    query.replace.term.with.prefix.query=true

Highlight String
================

The string specified here divides sentences to achieve natural highlight display.
The specified string is a Unicode character starting with u as the delimiter.
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

Specifies OpenSearch highlight generation method.
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

Field Names to Add to Response
===============================

Specifies field names to add to responses for normal searches or API searches.
::

    query.additional.response.fields=
    query.additional.api.response.fields=

Adding Field Names
==================

Specify when adding search field names or facet field names.
::

    query.additional.search.fields=
    query.additional.facet.fields=

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
