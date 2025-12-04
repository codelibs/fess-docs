============
页面设计
============

概述
====

本节介绍搜索界面设计的相关配置。

配置方法
======

显示方法
------

要打开下图所示的页面设计配置列表页面,请单击左侧菜单中的[系统 > 页面设计]。

|image0|


文件管理器
---------------

可以下载或删除搜索界面中可用的文件。

页面文件显示
---------------

可以编辑搜索界面的 JSP 文件。
单击目标 JSP 文件的"编辑"按钮,即可编辑该 JSP 文件。
此外,单击"使用默认值"按钮,可以编辑为安装时的 JSP 文件。
在编辑界面单击"更新"按钮保存后,更改将生效。

以下总结了可编辑页面的说明。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - /index.jsp
     - 搜索首页的 JSP 文件。该 JSP 文件会 include 各部分的 JSP 文件。
   * - /header.jsp
     - 页眉的 JSP 文件。
   * - /footer.jsp
     - 页脚的 JSP 文件。
   * - /search.jsp
     - 搜索结果列表页面的 JSP 文件。该 JSP 文件会 include 各部分的 JSP 文件。
   * - /searchResults.jsp
     - 表示搜索结果列表页面的搜索结果部分的 JSP 文件。有搜索结果时使用的 JSP 文件。要自定义搜索结果的呈现时进行更改。
   * - /searchNoResult.jsp
     - 表示搜索结果列表页面的搜索结果部分的 JSP 文件。没有搜索结果时使用的 JSP 文件。
   * - /searchOptions.jsp
     - 搜索选项界面的 JSP 文件。
   * - /advance.jsp
     - 高级搜索界面的 JSP 文件。
   * - /help.jsp
     - 帮助页面的 JSP 文件。
   * - /error/error.jsp
     - 搜索错误页面的 JSP 文件。要自定义搜索错误的呈现时进行更改。
   * - /error/notFound.jsp
     - 找不到页面时显示的错误页面 JSP 文件。
   * - /error/system.jsp
     - 系统错误时显示的错误页面 JSP 文件。
   * - /error/redirect.jsp
     - 发生 HTTP 重定向时显示的错误页面 JSP 文件。
   * - /error/badRequest.jsp
     - 发生非法请求时显示的错误页面 JSP 文件。
   * - /cache.hbs
     - 显示搜索结果缓存的文件。
   * - /login/index.jsp
     - 登录界面的 JSP 文件。
   * - /profile/index.jsp
     - 用户密码更改界面的 JSP 文件。
   * - /profile/newpassword.jsp
     - 管理员密码更新界面的 JSP 文件。登录时如果用户名和密码是相同的字符串,将要求更改密码。


表: 可编辑的 JSP 文件

|image1|

上传文件
------------------

可以上传搜索界面中使用的文件。
支持的图像文件名为 jpg、gif、png、css、js。

文件上传
:::::::::::::::::

指定要上传的文件。

文件名(可选)
:::::::::::::::::

要为上传的文件指定文件名时使用。
省略时将使用上传文件的文件名。
例如,指定 logo.png 后,搜索首页的图像将更改。


.. |image0| image:: ../../../resources/images/en/15.4/admin/design-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/design-2.png
