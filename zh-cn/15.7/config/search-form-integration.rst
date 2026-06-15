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

搜索关键词会作为 ``q`` 参数发送到 |Fess| 的搜索页面(``/search/``)。
请将 ``maxlength`` 设置为与 ``query.max.length`` (初始值为 ``1000``)一致的值,该参数是 |Fess| 端关键词长度的上限。


建议功能
--------

也可以为配置的搜索表单设置建议功能。
要设置,请在 </body> 前添加以下代码。

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

如果网站已使用 jQuery,则无需添加 jQuery 的 script 元素。

建议功能使用 |Fess| 的建议 API(``/api/v2/suggest-words``)。
请将 ``url`` 更改为与构建的 |Fess| 服务器的 URL 一致。

可为 ``suggestor`` 指定的主要选项如下。

.. list-table:: suggestor 的主要选项
   :header-rows: 1
   :widths: 25 75

   * - 选项
     - 说明
   * - ``ajaxinfo.url``
     - 建议 API 的 URL。指定 |Fess| 服务器的 ``/api/v2/suggest-words`` 。
   * - ``ajaxinfo.fn``
     - 作为建议对象的字段名数组。可直接使用初始值 ``["_default", "content", "title"]`` 。
   * - ``ajaxinfo.num``
     - 显示的候选项的最大数量。
   * - ``ajaxinfo.lang``
     - 用于缩小建议候选项范围的语言(可省略)。
   * - ``minterm``
     - 开始建议所需的最小输入字符数。
   * - ``adjustWidthVal``
     - 在输入框宽度上加算以调整建议显示区域宽度的值(像素)。
   * - ``searchForm``
     - 选择候选项时提交的搜索表单元素。
   * - ``boxCssInfo``
     - 应用于建议显示区域的 CSS。
   * - ``listSelectedCssInfo``
     - 应用于选中候选项的 CSS(可省略)。
   * - ``listDeselectedCssInfo``
     - 应用于未选中候选项的 CSS(可省略)。

请为 "z-index" 指定不与其他元素重叠的值。

.. note::
    当搜索表单放置在与 |Fess| 服务器不同域名的页面上时,对建议 API 的请求将成为跨源(cross-origin)通信。
    |Fess| 在初始设置中允许所有来源(``api.cors.allow.origin=*``),因此可直接使用。
    如需限制访问,请更改 ``fess_config.properties`` 中的 ``api.cors.allow.origin`` 。

.. note::
    ``/api/v2/suggest-words`` 是 |Fess| 本体提供的 API。
    早期版本中使用的 ``/api/v1/suggest-words`` 已不再由 |Fess| 本体提供,要使用它需要安装 ``fess-webapp-v1-api`` 插件。
    新构建时请使用 ``/api/v2/suggest-words`` 。
