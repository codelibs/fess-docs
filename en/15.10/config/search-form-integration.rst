=======================
Search Form Integration
=======================

Search Form Integration Method
===============================

By placing a search form on existing sites, you can direct users to |Fess| search results.
This example explains placing |Fess| at https://search.n2sm.co.jp/ and adding a search form to each page of an existing site.

Search Form
-----------

Place the following code where you want the search form on your page:

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="Search">
    </form>

To match your site design, add class names with the class attribute and adjust with CSS as needed.
Change the https://search.n2sm.co.jp/ URL to the URL of your |Fess| server.

The search keyword is sent as the ``q`` parameter to the |Fess| search page (``/search/``).
Set ``maxlength`` to a value that matches ``query.max.length`` (default ``1000``), which is the maximum keyword length on the |Fess| side.


Suggest Feature
---------------

You can also configure the suggest feature for the search form.
To configure, add the following code before </body>:

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.7.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v2/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "background-color": "#fff",
          "z-index": "10000"
        },
        minterm: 2,
        adjustWidthVal : 11,
        searchForm : $('#searchForm')
      });
    });
    </script>

If your site already uses jQuery, you do not need to add the jQuery script element.

The suggest feature uses the |Fess| suggest API (``/api/v2/suggest-words``).
Change ``url`` to match the URL of your |Fess| server.

The main options that can be specified for ``suggestor`` are as follows.

.. list-table:: Main suggestor options
   :header-rows: 1
   :widths: 25 75

   * - Option
     - Description
   * - ``ajaxinfo.url``
     - The suggest API URL. Specify ``/api/v2/suggest-words`` of your |Fess| server.
   * - ``ajaxinfo.fn``
     - An array of field names to get suggestions from. You can use the default ``["_default", "content", "title"]`` as is.
   * - ``ajaxinfo.num``
     - The maximum number of suggestion candidates to display.
   * - ``ajaxinfo.lang``
     - The language used to narrow down suggestion candidates (optional).
   * - ``minterm``
     - The minimum number of input characters before suggestions are requested.
   * - ``adjustWidthVal``
     - The value (in pixels) added to the input field width to adjust the width of the suggestion box.
   * - ``searchForm``
     - The search form element that is submitted when a candidate is selected.
   * - ``boxCssInfo``
     - The CSS applied to the suggestion box.
   * - ``listSelectedCssInfo``
     - The CSS applied to the selected candidate (optional).
   * - ``listDeselectedCssInfo``
     - The CSS applied to non-selected candidates (optional).

Specify a value for "z-index" that does not overlap with other elements.

.. note::
    When the search form is placed on a page whose domain differs from the |Fess| server, the request to the suggest API becomes a cross-origin request.
    |Fess| allows all origins by default (``api.cors.allow.origin=*``), so it works as is.
    To restrict access, change ``api.cors.allow.origin`` in ``fess_config.properties``.

.. note::
    ``/api/v2/suggest-words`` is the API provided by |Fess| itself.
    The ``/api/v1/suggest-words`` endpoint used in earlier versions is no longer provided by |Fess| core, and the ``fess-webapp-v1-api`` plugin must be installed to use it.
    For new setups, use ``/api/v2/suggest-words``.
