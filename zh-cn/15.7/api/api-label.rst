========
标签 API
========

本文档介绍 |Fess| v2 标签 API。
公共响应信封及错误模型，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

获取标签
========

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/labels``
==================  ====================================================

以公共信封格式获取 |Fess| 中已注册的标签列表。

返回的标签列表会根据请求用户及请求内容进行如下筛选：

- **按权限筛选**：根据标签上配置的访问权限与用户角色进行筛选。由于 v2 采用基于会话的认证方式，已登录用户只能获取其角色有权访问的标签。访问权限不匹配的标签不会包含在列表中。
- **按语言区域筛选**：标签可按语言区域注册。与 ``Accept-Language`` 请求头匹配的语言区域所注册的标签，以及未指定语言区域的标签，均会被返回。
- **按虚拟主机筛选**：启用虚拟主机时，仅返回分配给相应虚拟主机的标签。

请求参数
--------

无查询参数。返回标签的筛选如上所述，基于已认证用户的权限及 ``Accept-Language`` 请求头进行。

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
          {
            "label": "AWS",
            "value": "aws"
          },
          {
            "label": "Azure",
            "value": "azure"
          }
        ]
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 响应字段

   * - ``record_count``
     - 返回的标签数量（integer）。
   * - ``labels``
     - 标签的数组。
   * - ``label``
     - 标签的显示名称（标签名）。
   * - ``value``
     - 标签的值。将此值指定为 :doc:`api-search` 的 ``fields.label`` 参数，可按该标签筛选搜索结果。

表: 响应字段

使用示例
========

使用 curl 命令的请求示例：

::

    curl "http://localhost:8080/api/v2/labels"

错误响应
========

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 指定了 GET 以外的 HTTP 方法时。\ ``error.code`` 为 ``method_not_allowed``\ ，响应中会附带 ``Allow: GET`` 头。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。\ ``error.code`` 为 ``internal_error``\ 。

表: 错误响应
