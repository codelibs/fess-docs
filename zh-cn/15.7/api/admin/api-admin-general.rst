==========================
General API
==========================

概述
====

General API是用于管理 |Fess| 常规设置（系统整体配置）的API。
可以获取和更新与爬取、日志、搜索结果显示、建议、日志保留期限、通知、
认证（LDAP / SSO）以及云存储集成相关的设置。这些设置对应管理界面中的
"常规"设置（:doc:`../../admin/general-guide`）。

基础URL
=======

::

    /api/admin/general

访问此API需要具有 ``Radmin-api`` 权限的访问令牌。
有关认证方式的详细信息，请参阅 :doc:`api-admin-overview`。

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

此端点不接受查询参数。

响应
----

``response.setting`` 中包含当前的常规设置。响应中包含所有可更新的设置字段；
以下示例仅展示具有代表性的字段。
开/关设置以 ``"true"`` / ``"false"`` 字符串表示，
而保留天数和线程数等值则以数字表示。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "storageAccessKey": "**********",
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   出于安全原因，密码和密钥类值不会原样返回。LDAP管理员密码
   ``ldapAdminSecurityCredentials`` 始终以 ``null`` 返回。
   其他密钥类字段（``storageAccessKey``、``storageSecretKey``、
   ``oicClientId``、``oicClientSecret``、``spnegoPreauthPassword``、
   ``entraidClientId``、``entraidClientSecret``）在已设置时以掩码值
   ``"**********"`` 返回，未设置时以空字符串返回。

更新常规设置
============

请求
----

::

    PUT /api/admin/general
    Content-Type: application/json

请求体
~~~~~~

更新作为部分更新（merge）处理。服务器读取当前设置值后，仅覆盖请求中包含的
非 ``null`` 字段。请求中未包含的字段以及设置为 ``null`` 的字段将保留其现有值。

.. important::

   请求体在执行覆盖处理之前会进行验证。因此，必需字段
   （``dayForCleanup``、``crawlingThreadCount``、
   ``failureCountThreshold``、``csvFileEncoding``）**无论修改内容如何，
   都必须始终包含在请求中**。如果缺少其中任何一个，请求将验证失败并返回
   ``status: 1``。若只想修改部分字段，请先通过 ``GET`` 获取当前设置，
   然后在 ``PUT`` 请求中包含必需字段的当前值。

.. note::

   密码和密钥类字段（``ldapAdminSecurityCredentials``、
   ``storageAccessKey``、``storageSecretKey``、``oicClientId``、``oicClientSecret``、
   ``spnegoPreauthPassword``、``entraidClientId``、``entraidClientSecret``）
   在发送空字符串或掩码值（``**********``）时会被忽略，现有值将被保留。
   这些字段仅在发送实际值时才会被更新。

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

主要字段
~~~~~~~~

设置项种类繁多。以下列出代表性字段
（所有字段均对应管理界面的"常规"设置）。开/关设置以
``"true"`` / ``"false"`` 字符串指定。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 字段
     - 必需
     - 说明
   * - ``incrementalCrawling``
     - 否
     - 增量爬取的启用/禁用
   * - ``dayForCleanup``
     - 是
     - 保留已爬取文档的天数（-1=禁用清理；取值范围：-1 至 1000）
   * - ``crawlingThreadCount``
     - 是
     - 爬取使用的线程数（取值范围：0 至 100）
   * - ``failureCountThreshold``
     - 是
     - 停止URL爬取的失败次数阈值（-1=禁用；取值范围：-1 至 10000）
   * - ``csvFileEncoding``
     - 是
     - CSV导出的编码
   * - ``searchLog``
     - 否
     - 搜索查询日志的启用/禁用
   * - ``userInfo``
     - 否
     - 用户信息记录的启用/禁用
   * - ``userFavorite``
     - 否
     - 收藏功能的启用/禁用
   * - ``webApiJson``
     - 否
     - JSON Web API的启用/禁用
   * - ``popularWord``
     - 否
     - 热门词汇的统计与显示的启用/禁用
   * - ``defaultLabelValue``
     - 否
     - 默认标签值
   * - ``defaultSortValue``
     - 否
     - 默认排序顺序
   * - ``appendQueryParameter``
     - 否
     - 向搜索结果URL附加查询参数
   * - ``loginRequired``
     - 否
     - 搜索是否需要登录
   * - ``thumbnail``
     - 否
     - 缩略图生成的启用/禁用
   * - ``ignoreFailureType``
     - 否
     - 要忽略的爬取失败类型
   * - ``purgeSearchLogDay``
     - 否
     - 保留搜索日志的天数（-1=禁用；取值范围：-1 至 100000）
   * - ``purgeJobLogDay``
     - 否
     - 保留作业日志的天数（-1=禁用；取值范围：-1 至 100000）
   * - ``purgeUserInfoDay``
     - 否
     - 保留用户信息的天数（-1=禁用；取值范围：-1 至 100000）
   * - ``purgeSuggestSearchLogDay``
     - 否
     - 保留建议搜索日志的天数（0=禁用；取值范围：0 至 100000）
   * - ``purgeByBots``
     - 否
     - 要丢弃搜索日志的机器人User-Agent
   * - ``notificationTo``
     - 否
     - 系统通知的接收邮箱地址
   * - ``notificationLogin``
     - 否
     - 在登录页面显示的通知消息
   * - ``notificationSearchTop``
     - 否
     - 在搜索首页显示的通知消息
   * - ``notificationAdvanceSearch``
     - 否
     - 在高级搜索页面显示的通知消息
   * - ``suggestSearchLog``
     - 否
     - 来自搜索日志的建议的启用/禁用
   * - ``suggestDocuments``
     - 否
     - 来自文档的建议的启用/禁用
   * - ``logLevel``
     - 否
     - 系统日志的日志级别
   * - ``logNotificationEnabled``
     - 否
     - ERROR/WARN日志通知的启用/禁用
   * - ``logNotificationLevel``
     - 否
     - 日志通知级别
   * - ``slackWebhookUrls``
     - 否
     - 用于通知的Slack Webhook URL
   * - ``googleChatWebhookUrls``
     - 否
     - 用于通知的Google Chat Webhook URL

认证相关字段
~~~~~~~~~~~~

LDAP以及SSO（OpenID Connect、SAML、SPNEGO、Entra ID）相关的设置也通过此API管理。
以下列出代表性字段（所有字段均对应管理界面的"常规"设置）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 字段
     - 说明
   * - ``ldapProviderUrl``
     - LDAP连接URL
   * - ``ldapBaseDn``
     - LDAP基础DN
   * - ``ldapSecurityPrincipal``
     - 用于LDAP绑定的安全主体
   * - ``ldapAdminSecurityPrincipal``
     - 用于LDAP管理操作的安全主体
   * - ``ldapAdminSecurityCredentials``
     - LDAP管理员密码（在响应中替换为 ``null``）
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - 用户/组搜索过滤器
   * - ``ssoType``
     - SSO类型（``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``）
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` 等
     - OpenID Connect的设置
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` 等
     - SAML的设置
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` 等
     - SPNEGO的设置
   * - ``entraidClientId`` / ``entraidTenant`` 等
     - Microsoft Entra ID的设置

存储相关字段
~~~~~~~~~~~~

也可以管理云存储（S3 / GCS）集成的设置。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 字段
     - 说明
   * - ``storageType``
     - 存储类型（``auto`` / ``s3`` / ``gcs``）
   * - ``storageEndpoint``
     - 存储的端点URL
   * - ``storageAccessKey`` / ``storageSecretKey``
     - 用于认证的访问密钥/私密密钥
   * - ``storageBucket``
     - 存储桶名称
   * - ``storageRegion``
     - S3的区域
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - GCS的项目ID / 凭据文件路径

响应
----

更新成功时，仅返回 ``version`` 和 ``status``（不包含 ``id`` 或 ``created``）。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

如果更新失败（例如由于验证错误），``status`` 将设置为非零值（验证错误为 ``1``），
``message`` 中包含错误详情。有关 ``status`` 值的列表，请参阅 :doc:`api-admin-overview`。

使用示例
========

.. note::

   以下示例包含必需字段（``dayForCleanup``、``crawlingThreadCount``、
   ``failureCountThreshold``、``csvFileEncoding``）。由于这些字段无论修改内容如何
   都必须始终指定，实际操作中请使用通过 ``GET`` 获取的当前值。

更新爬取设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

更新日志保留期限
----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

更新建议设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`../../admin/general-guide` - 常规设置指南
