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


Suggest Feature
---------------

You can also configure the suggest feature for the search form.
To configure, add the following code before </body>:

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.6.3.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v1/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "-webkit-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "-moz-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
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

Specify a value for "z-index" that does not overlap with other elements.
