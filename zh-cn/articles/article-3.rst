========================================================
使用Fess创建基于Elasticsearch的搜索服务器 ～ API 篇
========================================================

前言
========

本次将介绍如何利用 Fess 提供的 API,在客户端(浏览器端)进行搜索并显示搜索结果。
通过使用 API,即使是现有的 Web 系统也可以将 Fess 作为搜索服务器使用,仅通过修改 HTML 就可以集成。

本文使用 Fess 15.3.0 进行说明。
关于 Fess 的构建方法,请参考\ `导入篇 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ 。

目标读者
========

-  希望在现有 Web 系统中添加搜索功能的人员

必要环境
==========

本文内容已在以下环境中进行了验证。

-  Google Chrome 120 及以上版本

JSON API
========

Fess 除了通常的 HTML 搜索表现形式外,还可以通过 API 以 JSON 形式响应搜索结果。
通过使用 API,可以轻松实现构建 Fess 服务器,然后从现有系统仅查询搜索结果。
由于搜索结果以不依赖于开发语言的格式处理,因此也易于将 Fess 集成到 Java 以外的系统中。

关于 Fess 提供的 API 返回何种响应,请参考 `JSON 响应 <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__。

Fess 使用 OpenSearch 作为内部搜索引擎。
OpenSearch 也提供 JSON API,但与 Fess 的 API 不同。
使用 Fess 的 API 而不是 OpenSearch 的 API 的优势在于,通过使用 Fess 的 API 可以利用搜索日志管理和浏览权限控制等各种 Fess 特有的功能。
如果想从零开始独立开发文档爬取机制,使用 OpenSearch 会比较好,但如果只是想简单地添加搜索功能,使用 Fess 可以大幅削减开发成本。

使用 JSON API 构建搜索网站
==================================

本次将说明如何构建使用 Fess API 的网站。
与 Fess 服务器的交互使用 JSON 响应。
本次使用的 Fess 服务器是 Fess 项目公开的演示用 Fess 服务器。
如果想使用自己的 Fess 服务器,请安装 Fess 15.3.0 或更高版本。

JSON 和 CORS
-----------

使用 JSON 访问时需要注意同源策略。
因此,如果输出显示在浏览器中的 HTML 的服务器与 Fess 服务器在同一域中,就可以使用 JSON,但如果不同则需要使用 CORS(跨域资源共享)。
本次将在 HTML 所在服务器与 Fess 服务器位于不同域的情况下进行说明。
Fess 支持 CORS,设置值可以在 app/WEB-INF/classes/fess_config.properties 中设置。默认设置如下。

::

    api.cors.allow.origin=*
    api.cors.allow.methods=GET, POST, OPTIONS, DELETE, PUT
    api.cors.max.age=3600
    api.cors.allow.headers=Origin, Content-Type, Accept, Authorization, X-Requested-With
    api.cors.allow.credentials=true

本次使用默认设置,但如果更改了设置,请重启 Fess。


创建的文件
----------------

本次将在 HTML 上使用 JavaScript 实现搜索处理。
JavaScript 库使用 jQuery。
要创建的文件如下。

-  显示搜索表单和搜索结果的 HTML 文件「index.html」

- 与 Fess 服务器通信的 JS 文件「fess.js」

本次构建示例实现了以下功能。

-  通过搜索按钮发送搜索请求

-  搜索结果列表

-  搜索结果的分页处理

创建 HTML 文件
------------------

首先,创建显示搜索表单和搜索结果的 HTML。
本次为了便于理解,未使用 CSS 调整设计,采用了简单的标签结构。
使用的 HTML 文件如下。

index.html 的内容
::

    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>搜索网站</title>
    </head>
    <body>
    <div id="header">
      <form id="searchForm">
        <input id="searchQuery" type="text" name="query" size="30"/>
        <input id="searchButton" type="submit" value="搜索"/>
        <input id="searchStart" type="hidden" name="start" value="0"/>
        <input id="searchNum" type="hidden" name="num" value="20"/>
      </form>
    </div>
    <div id="subheader"></div>
    <div id="result"></div>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="fess.js"></script>
    </body>
    </html>

查看 body 标签以下,首先在 id 属性为 header 的 div 标签处,放置了搜索输入栏和搜索按钮。
此外,hidden 表单保存了显示开始位置(start)和显示件数(num)。
发送搜索请求后,JavaScript 会更新 start 和 num 的值。
但是,显示件数是每页的显示件数,在本次示例代码中没有更改显示件数的功能,因此 num 的值不会改变。

接下来的 subheader 的 div 标签处会显示搜索命中件数等信息。
result 的 div 标签会显示搜索结果和分页链接。

最后加载 jQuery 的 JS 文件和本次创建的「fess.js」JavaScript。
jQuery 的 JS 文件也可以保存在与「index.html」相同的目录中,但本次设置为通过 Google 的 CDN 获取。

创建 JS 文件
----------------

接下来创建与 Fess 服务器通信并显示搜索结果的 JS 文件「fess.js」。
以下内容创建「fess.js」,并放置在与「index.html」相同的目录中。

fess.js 的内容
::

    $(function(){
        // (1) Fess 的 URL
        var baseUrl = "http://SERVERNAME:8080/api/v1/documents?q=";
        // (2) 搜索按钮的 jQuery 对象
        var $searchButton = $('#searchButton');

        // (3) 搜索处理函数
        var doSearch = function(event){
          // (4) 获取显示开始位置、显示件数
          var start = parseInt($('#searchStart').val()),
              num = parseInt($('#searchNum').val());
          // 检查显示开始位置
          if(start < 0) {
            start = 0;
          }
          // 检查显示件数
          if(num < 1 || num > 100) {
            num = 20;
          }
          // (5) 获取显示页面信息
          switch(event.data.navi) {
            case -1:
              // 前一页的情况
              start -= num;
              break;
            case 1:
              // 下一页的情况
              start += num;
              break;
            default:
            case 0:
              start = 0;
              break;
          }
          // 修剪搜索字段的值并存储
          var searchQuery = $.trim($('#searchQuery').val());
          // (6) 检查搜索表单是否为空字符
          if(searchQuery.length != 0) {
            var urlBuf = [];
            // (7) 禁用搜索按钮
            $searchButton.attr('disabled', true);
            // (8) 构建 URL
            urlBuf.push(baseUrl, encodeURIComponent(searchQuery),
              '&start=', start, '&num=', num);
            // (9) 发送搜索请求
            $.ajax({
              url: urlBuf.join(""),
              dataType: 'json',
            }).done(function(data) {
              // 搜索结果处理
              var dataResponse = data.response;
              // (10) 状态检查
              if(dataResponse.status != 0) {
                alert("搜索过程中发生问题。请咨询管理员。");
                return;
              }

              var $subheader = $('#subheader'),
                  $result = $('#result'),
                  record_count = dataResponse.record_count,
                  offset = 0,
                  buf = [];
              if(record_count == 0) { // (11) 没有搜索结果的情况
                // 输出到子标题区域
                $subheader[0].innerHTML = "";
                // 输出到结果区域
                buf.push("<b>", dataResponse.q, "</b>未找到匹配的信息。");
                $result[0].innerHTML = buf.join("");
              } else { // (12) 搜索命中的情况
                var page_number = dataResponse.page_number,
                    startRange = dataResponse.start_record_number,
                    endRange = dataResponse.end_record_number,
                    i = 0,
                    max;
                offset = startRange - 1;
                // (13) 输出到子标题
                buf.push("<b>", dataResponse.q, "</b> 的搜索结果 ",
                  record_count, " 件中 ", startRange, " - ",
                  endRange, " 件 (", dataResponse.exec_time,
                    " 秒)");
                $subheader[0].innerHTML = buf.join("");

                // 清除搜索结果区域
                $result.empty();

                // (14) 输出搜索结果
                var $resultBody = $("<ol/>");
                var results = dataResponse.result;
                for(i = 0, max = results.length; i < max; i++) {
                  buf = [];
                  buf.push('<li><h3 class="title">', '<a href="',
                    results[i].url_link, '">', results[i].title,
                    '</a></h3><div class="body">', results[i].content_description,
                    '<br/><cite>', results[i].site, '</cite></div></li>');
                  $(buf.join("")).appendTo($resultBody);
                }
                $resultBody.appendTo($result);

                // (15) 输出页码信息
                buf = [];
                buf.push('<div id="pageInfo">', page_number, '页<br/>');
                if(dataResponse.prev_page) {
                  // 前一页的链接
                  buf.push('<a id="prevPageLink" href="#">&lt;&lt;前一页</a> ');
                }
                if(dataResponse.next_page) {
                  // 下一页的链接
                  buf.push('<a id="nextPageLink" href="#">下一页&gt;&gt;</a>');
                }
                buf.push('</div>');
                $(buf.join("")).appendTo($result);
              }
              // (16) 更新页面信息
              $('#searchStart').val(offset);
              $('#searchNum').val(num);
              // (17) 将页面显示移到顶部
              $(document).scrollTop(0);
            }).always(function() {
              // (18) 启用搜索按钮
              $searchButton.attr('disabled', false);
            });
          }
          // (19) 不提交,返回 false
          return false;
        };

        // (20) 在搜索输入栏按 Enter 键时的处理
        $('#searchForm').submit({navi:0}, doSearch);
        // (21) 点击前一页链接时的处理
        $('#result').on("click", "#prevPageLink", {navi:-1}, doSearch)
        // (22) 点击下一页链接时的处理
          .on("click", "#nextPageLink", {navi:1}, doSearch);
      });

「fess.js」的处理在 HTML 文件的 DOM 构建完成后执行。
首先,在 1 处指定构建的 Fess 服务器的 URL。

2 保存搜索按钮的 jQuery 对象。
由于会多次使用搜索按钮的 jQuery 对象,因此保存在变量中以便重复使用。

3 定义搜索处理函数。此函数的内容将在下一节说明。

20 注册搜索表单提交时的事件。
当按下搜索按钮或在搜索输入栏按下 Enter 键时,会执行在 20 处注册的处理。
事件发生时调用搜索处理函数 doSearch。
navi 的值在调用搜索处理函数时传递,该值用于分页处理。

21 和 22 注册点击分页处理中添加的链接时的事件。
由于这些链接是动态添加的,因此需要通过 delegate 注册事件。
这些事件也与 20 相同,调用搜索处理函数。

搜索处理函数 doSearch
--------------------

说明 3 的搜索处理函数 doSearch。

4 获取显示开始位置和显示件数。
这些值作为 hidden 值保存在 header 区域的搜索表单中。
假设显示开始位置为 0 以上,显示件数为 1 到 100 之间的值,如果获取到其他值则设置默认值。

5 判断在 doSearch 注册事件时传递的参数 navi 的值,修正显示开始位置。
这里,-1 表示移动到前一页,1 表示移动到下一页,其他情况改为移动到首页。

6 判断如果搜索输入栏的值已输入则执行搜索,如果为空则不执行任何操作直接结束处理。

7 为了防止双重提交,在向 Fess 服务器查询期间禁用搜索按钮。

8 组装用于发送 Ajax 请求的 URL。
将 1 的 URL 与搜索词、显示开始位置、显示件数结合。

9 发送 Ajax 请求。
如果请求正常返回,会执行 success 函数。
success 的参数会传递从 Fess 服务器返回的搜索结果对象。

首先,在 10 处确认响应状态的内容。
如果搜索请求正常处理,会设置为 0。
Fess 的 JSON 响应详细信息请参考\ `Fess 网站 <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__\ 。

如果搜索请求正常处理但搜索结果未命中,在 11 的条件语句内清空 subheader 区域的内容,在 result 区域显示未命中搜索结果的消息。

如果搜索结果命中,在 12 的条件语句内处理搜索结果。
13 在 subheader 区域设置显示件数和执行时间等消息。
14 将搜索结果添加到 result 区域。
搜索结果以数组形式存储在 data.response.result 中。
通过 results[i].〜访问可以获取搜索结果文档的字段值。

15 将当前显示的页码以及前一页和下一页的链接添加到 result 区域。
16 将当前的显示开始位置和显示件数保存在搜索表单的 hidden 中。
显示开始位置和显示件数将在下次搜索请求时再次使用。

接下来,17 更改页面的显示位置。
当点击下一页的链接时,由于页面本身不会更新,因此通过 scrollTop 移动到页面顶部。

18 在搜索处理完成后启用搜索按钮。
无论请求成功还是失败都会执行,因此设置为由 complete 调用。

19 在调用搜索处理函数后,为了防止表单或链接被发送,返回 false。
这样可以防止发生页面跳转。

执行
----

在浏览器中访问「index.html」。
会显示如下搜索表单。

搜索表单
|image1|

输入适当的搜索词,按下搜索按钮后会显示搜索结果。
默认显示件数为 20 件,但如果命中的搜索件数很多,搜索结果列表下方会显示下一页的链接。

搜索结果
|image2|

总结
======

使用 Fess 的 JSON API 构建了基于 jQuery 的客户端搜索网站。
通过使用 JSON API,不仅限于基于浏览器的应用程序,还可以构建从其他应用程序调用并使用 Fess 的系统。

此外,本文的示例代码展示了传统的 API 端点格式,但在 Fess 15.3 中推荐使用 ``/api/v1/documents`` 端点。
详情请参考 `API 规格 <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__。

参考资料
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `jQuery <http://jquery.com/>`__

.. |image0| image:: ../../resources/images/en/article/4/sameorigin.png
.. |image1| image:: ../../resources/images/en/article/4/searchform.png
.. |image2| image:: ../../resources/images/en/article/4/searchresult.png
