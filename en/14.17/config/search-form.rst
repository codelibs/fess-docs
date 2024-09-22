========================
Placement of Search Form
========================

How to Place the Search Form
============================

You can guide users to Fess search results by adding a search form to an existing website.
Here, we will explain with an example of setting up Fess on https://search.n2sm.co.jp/ and placing a search form on various pages of an existing site.

Search Form
-----------

Place the following code in the location where you want to have a search form within the page:

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="検索">
    </form>

Please adjust it as needed using CSS to match the design of your site by adding class names through the class attribute.
Make sure to replace the URL of https://search.n2sm.co.jp/ with the URL of the Fess server you have set up for your use.

Suggestion
----------

You can also set up a suggestion feature for the placed search form. If you wish to set it up, add the following code before </body>:

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.4.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/suggest',
          fn : '_default,content,title',
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

If you are already using jQuery on your site, there is no need to add the jQuery script element.

Specify a value for "z-index" that does not overlap with other elements.

