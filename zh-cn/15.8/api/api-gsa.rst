================================
Google Search Appliance兼容API
================================

|Fess| 提供可返回Google Search Appliance (GSA)兼容XML格式搜索结果的API。
关于XML格式的详细信息，请参阅\ `GSA官方文档 <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__\ 。

配置
====

请在system.properties中添加 ``web.api.gsa=true`` 以启用Google Search Appliance兼容API。

请求
========

向 |Fess| 发送
``http://localhost:8080/gsa/?q=搜索词``
形式的请求，可以获取GSA兼容XML格式的搜索结果。
可以指定的请求参数与\ `JSON响应搜索API <api-search.html>`__\ 相同。
