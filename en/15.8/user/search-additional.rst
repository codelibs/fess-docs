========================
Hidden Search Conditions
========================

You can use the ``ex_q`` parameter when you want to carry a specific search condition without displaying its text on the screen. Conditions specified in ``ex_q`` are not shown in the search keyword input field, and they are retained even when the screen is refreshed through pagination or facet filtering.

In ``ex_q``, you can use the same query syntax as the regular search keyword (``q``) — the ``field:value`` format, phrases, range specifications, operators such as ``OR``, and so on. The specified condition is combined with the ``q`` condition using AND by default when the search is executed. In other words, documents that do not match the ``ex_q`` condition are excluded from the search results.

Usage
-----

When executing a search (for example, from a search form), append the value of ``ex_q`` as a hidden form field or as a URL query parameter, then execute the search. This lets you search without displaying the condition on the screen.

You can specify ``ex_q`` more than once. As shown in the example below, passing multiple ``ex_q`` values adds each one as a search condition (empty or duplicate values are ignored).

.. code-block:: none

    /search?q=keyword&ex_q=label:manual&ex_q=filetype:pdf

Retention During Pagination
---------------------------

Fess automatically appends the value of ``ex_q`` to pagination links (such as next page and previous page) and facet filtering links. As a result, the ``ex_q`` condition is retained even when the screen is refreshed through these operations.

On the other hand, if you enter a keyword in the standard search keyword input field (the search box) and search again, ``ex_q`` is not carried over. If you want the condition to be retained through the search box as well, add a hidden ``ex_q`` field to your own search form and submit ``ex_q`` with every search.

.. note::

    * If the length of an individual ``ex_q`` value exceeds ``query.max.length`` (default: 1000 characters), that value is ignored without causing an error.
    * ``ex_q`` can be used not only for searches on the web screen but also with the search API (``/api/v2``). In the API, the maximum number of ``ex_q`` elements per request (``api.v2.param.max.array.size``, default: 100) and the maximum length of each element (``api.v2.param.max.length``, default: 1000 characters) apply.
