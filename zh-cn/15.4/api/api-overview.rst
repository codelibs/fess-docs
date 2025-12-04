========
API概述
========


|Fess| 提供的API
==================

本文档介绍 |Fess| 提供的API。
通过使用API，您可以将 |Fess| 作为搜索服务器集成到现有的Web系统中。

基础URL
========

|Fess| API端点的基础URL如下：

::

    http://<Server Name>/api/v1/

例如，在本地环境中运行时，URL如下：

::

    http://localhost:8080/api/v1/

身份验证
====

当前版本的API无需身份验证。
但是，需要在管理界面的各项设置中启用API功能。

HTTP方法
==========

所有API端点均使用 **GET** 方法访问。

响应格式
==================

所有API响应均以 **JSON格式** 返回（Google Search Appliance兼容API除外）。
响应的 ``Content-Type`` 为 ``application/json``。

错误处理
===============

当API请求失败时，将返回相应的HTTP状态码和错误信息。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: HTTP状态码

   * - 200
     - 请求已成功处理。
   * - 400
     - 请求参数无效。
   * - 404
     - 未找到请求的资源。
   * - 500
     - 服务器内部错误。

表: HTTP状态码

API类型
========

|Fess| 提供以下API：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - 获取搜索结果的API。
   * - popularword
     - 获取热门词的API。
   * - label
     - 获取已创建标签列表的API。
   * - health
     - 获取服务器状态的API。
   * - suggest
     - 获取建议词的API。

表: API类型
