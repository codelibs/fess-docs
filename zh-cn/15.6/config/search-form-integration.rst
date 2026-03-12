==============
搜索表单集成
==============

搜索表单配置方法
=================

通过在现有网站上配置搜索表单,可以引导用户访问 |Fess| 的搜索结果。
本文以在 https://search.n2sm.co.jp/ 上构建 |Fess| 并在现有网站的各个页面上放置搜索表单为例进行说明。

搜索表单
---------

请在页面中要放置搜索表单的位置添加以下代码。

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="搜索">
    </form>

请根据网站设计,通过添加 class 属性的类名等使用 CSS 进行必要的调整。
请将 https://search.n2sm.co.jp/ 的 URL 更改为构建的 |Fess| 服务器的 URL 后使用。


建议功能
--------

也可以为配置的搜索表单设置建议功能。
要设置,请在 </body> 前添加以下代码。

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

如果网站已使用 jQuery,则无需添加 jQuery 的 script 元素。

请为 "z-index" 指定不与其他元素重叠的值。
