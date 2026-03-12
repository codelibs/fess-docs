==========================
General API
==========================

概述
====

General API是用于管理 |Fess| 常规设置的API。
您可以获取和更新系统整体相关的设置。

基础URL
=======

::

    /api/admin/general

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /
     - 获取常规设置
   * - PUT
     - /
     - 更新常规设置

获取常规设置
============

请求
----

::

    GET /api/admin/general

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "crawlerDocumentMaxSize": "10485760",
          "crawlerDocumentMaxSiteLength": "50",
          "crawlerDocumentMaxFetcherSize": "3",
          "crawlerDocumentCrawlerThreadCount": "10",
          "crawlerDocumentMaxDepth": "-1",
          "crawlerDocumentMaxAccessCount": "100",
          "indexerThreadDumpEnabled": "true",
          "indexerUnprocessedDocumentSize": "1000",
          "indexerClickCountEnabled": "true",
          "indexerFavoriteCountEnabled": "true",
          "indexerWebfsMaxContentLength": "10485760",
          "indexerWebfsContentEncoding": "UTF-8",
          "queryReplaceTermWithPrefixQuery": "false",
          "queryMaxSearchResultOffset": "100000",
          "queryMaxPageSize": "1000",
          "queryDefaultPageSize": "20",
          "queryAdditionalDefaultQuery": "",
          "queryGeoEnabled": "false",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "suggestBadWord": "true",
          "suggestPopularWordSeedLength": "1",
          "suggestPopularWordTags": "user",
          "suggestPopularWordFields": "tags",
          "suggestPopularWordExcludeWordFields": "",
          "ldapInitialContextFactory": "com.sun.jndi.ldap.LdapCtxFactory",
          "ldapSecurityAuthentication": "simple",
          "ldapProviderUrl": "ldap://localhost:389",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapBindDn": "",
          "ldapBindPassword": "",
          "notificationLogin": "true",
          "notificationSearchTop": "true"
        }
      }
    }

更新常规设置
============

请求
----

::

    PUT /api/admin/general
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "crawlerDocumentMaxSize": "20971520",
      "crawlerDocumentMaxSiteLength": "100",
      "crawlerDocumentCrawlerThreadCount": "20",
      "queryMaxPageSize": "500",
      "queryDefaultPageSize": "50",
      "suggestSearchLog": "true",
      "suggestDocuments": "true",
      "suggestBadWord": "true",
      "notificationLogin": "false",
      "notificationSearchTop": "false"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 字段
     - 说明
   * - ``crawlerDocumentMaxSize``
     - 爬虫目标文档的最大大小（字节）
   * - ``crawlerDocumentMaxSiteLength``
     - 爬虫目标站点的最大长度
   * - ``crawlerDocumentMaxFetcherSize``
     - 最大抓取器大小
   * - ``crawlerDocumentCrawlerThreadCount``
     - 爬虫线程数
   * - ``crawlerDocumentMaxDepth``
     - 爬虫最大深度（-1=无限制）
   * - ``crawlerDocumentMaxAccessCount``
     - 最大访问数
   * - ``indexerThreadDumpEnabled``
     - 启用线程转储
   * - ``indexerUnprocessedDocumentSize``
     - 未处理文档数
   * - ``indexerClickCountEnabled``
     - 启用点击计数
   * - ``indexerFavoriteCountEnabled``
     - 启用收藏计数
   * - ``queryReplaceTermWithPrefixQuery``
     - 转换为前缀查询
   * - ``queryMaxSearchResultOffset``
     - 搜索结果最大偏移量
   * - ``queryMaxPageSize``
     - 每页最大记录数
   * - ``queryDefaultPageSize``
     - 每页默认记录数
   * - ``queryAdditionalDefaultQuery``
     - 附加默认查询
   * - ``suggestSearchLog``
     - 启用搜索日志建议
   * - ``suggestDocuments``
     - 启用文档建议
   * - ``suggestBadWord``
     - 启用屏蔽词过滤
   * - ``ldapProviderUrl``
     - LDAP连接URL
   * - ``ldapBaseDn``
     - LDAP基础DN
   * - ``notificationLogin``
     - 登录通知
   * - ``notificationSearchTop``
     - 搜索顶部通知

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用示例
========

更新爬虫设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "crawlerDocumentMaxSize": "52428800",
           "crawlerDocumentCrawlerThreadCount": "15",
           "crawlerDocumentMaxAccessCount": "1000"
         }'

更新搜索设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "queryMaxPageSize": "1000",
           "queryDefaultPageSize": "50",
           "queryMaxSearchResultOffset": "50000"
         }'

更新建议设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true",
           "suggestBadWord": "true"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`../../admin/general-guide` - 常规设置指南

