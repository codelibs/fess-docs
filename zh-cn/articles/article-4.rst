============================================================
使用 Fess 构建基于 Elasticsearch 的搜索服务器 ~ FSS 篇
============================================================

前言
========

本文介绍如何利用已构建的 Fess 服务器，将搜索服务嵌入到网站中。
通过使用 Fess Site Search(FSS) 提供的标签和 JavaScript 文件，可以在现有网站中显示搜索框和搜索结果。


目标读者
========

- 希望在现有网站中添加搜索功能的用户

- 希望从 Google Site Search 或 Google 自定义搜索等服务迁移的用户。


什么是 Fess Site Search(FSS)
================================

FSS 是将搜索服务器 Fess 引入现有网站的功能。该功能由 CodeLibs 项目在 FSS 站点 上提供。与 Google Site Search(GSS) 等站内搜索类似，只需在希望使用搜索服务的页面中嵌入 JavaScript 标签即可使用，因此从 GSS 迁移也非常简单。

FSS JS 是什么
=============

FSS JS 是用于显示 Fess 搜索结果的 JavaScript 文件。通过将此 JavaScript 文件部署到网站上，即可显示搜索结果。
FSS JS 可以通过"https://fss-generator.codelibs.org/"上的 FSS JS Generator 生成并获取。
FSS JS 支持 Fess 11.3 及以上版本，因此在构建 Fess 时请安装 Fess 11.3 及以上版本。关于 Fess 的构建方法，请参阅\ `入门篇 <https://fess.codelibs.org/ja/articles/article-1.html>`__\ 。


FSS JS Generator 可以指定搜索表单的配色和字体。
点击"Generate"按钮，即可生成指定配置的 JavaScript 文件。

|image0|

如果预览显示没有问题，请点击"Download JS"按钮下载 JavaScript 文件。

|image1|

导入到网站
================

本次以在静态 HTML 构建的"`www.n2sm.net`"中引入站内搜索为例进行说明。

搜索结果设定为在该站点内的 search.html 中显示，Fess 服务器则另外构建在"nss833024.n2search.net"上。

下载的 FSS JS 的 JavaScript 文件以 /js/fess-ss.min.js 的路径部署在站点上。

将上述信息汇总如下。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - 名称
     - URL
   * - 搜索目标站点
     - https://www.n2sm.net/
   * - 搜索结果页面
     - https://www.n2sm.net/search.html
   * - FSS JS
     - https://www.n2sm.net/js/fess-ss.min.js
   * - Fess 服务器
     - https://nss833024.n2search.net/

JavaScript 标签的嵌入方法为：在 search.html 中希望显示搜索结果的位置放置以下标签。

..
  <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      // 将FSS JS的URL设置到src中
      fess.src = 'https://www.n2sm.net/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      // 将Fess的搜索API的URL设置到fess-url中
      fess.setAttribute('fess-url', 'https://nss833024.n2search.net/json');
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(fess, s);
    })();
  </script>
  <fess:search></fess:search>

访问 search.html 后将显示搜索表单。

输入搜索词后，即可如下所示显示搜索结果。

|image2|

要在其他页面放置搜索表单并显示搜索结果，请在各页面中放置如下搜索表单，并设置跳转到"`https://www.n2sm.net/search.html?q=搜索词`"。

..
  <form action="https://www.n2sm.net/search.html" method="get">
    <input type="text" name="q">
    <input type="submit" value="搜索">
  </form>


总结
======

本文介绍了仅通过放置 JavaScript 标签，即可将 Fess 的搜索结果嵌入网站的方法。
通过 FSS，从 GSS 的迁移也只需替换现有的 JavaScript 标签即可实现。
FSS JS 还提供了其他显示方式以及将搜索日志与 Google Analytics 联动的方法等。关于其他设置方法，请参阅 `FSS的[手册] <https://fss-generator.codelibs.org/ja/docs/manual>`__ 。

参考资料
========
- `Fess Site Search <https://fss-generator.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/5/FSS-JS-Generator1.png
.. |image1| image:: ../../resources/images/ja/article/5/FSS-JS-Generator2.png
.. |image2| image:: ../../resources/images/ja/article/5/N2Search-review.png
