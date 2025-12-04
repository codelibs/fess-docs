==============
查询请求
==============

概述
====

本页面向 OpenSearch 发送 JSON 文件的查询请求。

|image0|

操作方法
======

发送请求
------------

以管理员身份登录后,在 URL 路径中输入 /admin/esreq/。
将要发送给 OpenSearch 的查询请求创建为 JSON 文件,在"请求文件"中选择该 JSON 文件,然后单击"发送"按钮,即可向 OpenSearch 发送请求。
响应将作为文件下载。

配置项
------

请求文件
::::::::::::::

指定描述了查询 DSL 的 JSON 文件。
例如,JSON 文件的内容如下所示。

::

    POST /_search
    {
      "query": {
        "match_all": {}
      }
    }

.. |image0| image:: ../../../resources/images/en/15.4/admin/esreq-1.png
