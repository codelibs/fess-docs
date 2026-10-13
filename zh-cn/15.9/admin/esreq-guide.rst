====================
对OpenSearch的请求
====================

概述
====

本页面将 JSON 文件中描述的请求发送到 OpenSearch。

|image0|

此页面不在左侧菜单中。要显示此页面，请以管理员身份登录后，在 URL 路径中输入 ``/admin/sereq/`` 。
发送请求需要 ``admin`` 角色（管理员）或 ``admin-sereq`` 角色。

操作方法
========

发送请求
--------

将要发送给 OpenSearch 的请求创建为 JSON 文件，在“请求文件”中选择该文件，然后点击“发送”按钮，即可向 OpenSearch 发送请求。
响应将作为文件下载。

配置项
------

请求文件
::::::::

指定描述了请求的文件。

在第一行用一个半角空格分隔写入 ``<方法> <路径>`` ，从第二行起写入请求正文（如查询 DSL）。
方法可以使用 GET、POST、PUT、DELETE。路径是 OpenSearch 上的路径，开头的 ``/`` 可以省略。
例如，文件的内容如下所示。

::

    POST /_search
    {
      "query": {
        "match_all": {}
      }
    }

正文中的换行会被去掉，各行连接后发送。因此，无法发送每行一个 JSON 的格式（如 ``_bulk`` ）的请求。

.. warning::

   方法为 PUT 或 DELETE 的请求同样会原样发送到 OpenSearch。
   根据文件内容，可能会修改或删除 |Fess| 使用的索引，导致数据丢失。发送前请仔细确认内容。

.. |image0| image:: ../../../resources/images/en/15.9/admin/esreq-1.png
