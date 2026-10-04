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
        "version": "15.9.0",
        "status": 0,
        "setting": {
          "incremental_crawling": "true",
          "day_for_cleanup": -1,
          "crawling_thread_count": 5,
          "search_log": "true",
          "user_info": "true",
          "user_favorite": "false",
          "web_api_json": "true",
          "default_label_value": "",
          "default_sort_value": "",
          "append_query_parameter": "false",
          "login_required": "false",
          "thumbnail": "true",
          "failure_count_threshold": -1,
          "popular_word": "true",
          "csv_file_encoding": "UTF-8",
          "purge_search_log_day": 30,
          "purge_job_log_day": 30,
          "purge_user_info_day": 30,
          "purge_suggest_search_log_day": 30,
          "notification_to": "",
          "suggest_search_log": "true",
          "suggest_documents": "true",
          "ldap_provider_url": "ldap://localhost:389/",
          "ldap_base_dn": "dc=example,dc=com",
          "ldap_admin_security_principal": "cn=admin,dc=example,dc=com",
          "log_level": "",
          "sso_type": "none",
          "storage_type": "",
          "notification_login": "",
          "notification_search_top": ""
        }
      }
    }

.. note::

   上述仅为代表性字段示例。实际响应的 ``setting`` 对象中包含所有常规设置字段
   （爬取、搜索、通知、LDAP、SSO、存储等）。全部字段请参阅管理界面的"常规"设置页面。

.. note::

   出于安全原因，包含凭据的字段不会以实际值返回。

   - LDAP管理员密码 ``ldap_admin_security_credentials`` 始终不包含在响应中。
   - 其他机密字段（``storage_access_key`` / ``storage_secret_key`` /
     ``oic_client_id`` / ``oic_client_secret`` / ``spnego_preauth_password`` /
     ``entraid_client_id`` / ``entraid_client_secret``）在已设置的情况下
     以掩码值 ``"**********"`` 返回，未设置时以空字符串（``""``）返回。

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

.. warning::

   以下四个字段为必需字段，**每次** PUT请求中都必须包含这些字段，
   即使是部分更新也是如此。

   - ``day_for_cleanup``
   - ``crawling_thread_count``
   - ``failure_count_threshold``
   - ``csv_file_encoding``

   如果缺少其中任何一个，请求将验证失败，API将返回 HTTP 400，
   并附带 ``status: 1`` 和错误 ``message``\ 。由于发送的值会覆盖现有设置，
   如果不想更改某个值，请先通过 ``GET`` 获取当前值并原样发送。
   上述字段以外的字段均为可选项，省略时将保留现有值。

.. note::

   数值字段具有类型和范围验证。发送无法解析为整数的值或超出允许范围的值
   将导致验证错误（HTTP 400，并附带 ``status: 1``）。
   各数值字段的有效取值范围请参阅下方的字段表。

.. note::

   对于开/关（``available`` 类）字段，只有 ``"true"`` 或 ``"on"``
   （均不区分大小写）表示启用。发送其他任何值（如 ``"false"`` 或空字符串）
   均视为禁用（``false``）。只有省略该字段（不发送）时，才会保留现有值。
   另外，在 GET 响应中，这些字段以 ``"true"`` / ``"false"`` 字符串形式返回。

.. code-block:: json

    {
      "incremental_crawling": "true",
      "day_for_cleanup": -1,
      "crawling_thread_count": 10,
      "failure_count_threshold": 100,
      "csv_file_encoding": "UTF-8",
      "popular_word": "true"
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
   * - ``incremental_crawling``
     - 否
     - 增量爬取的启用/禁用
   * - ``day_for_cleanup``
     - 是
     - 保留已爬取文档的天数（-1=禁用清理；取值范围：-1 至 1000）
   * - ``crawling_thread_count``
     - 是
     - 爬取使用的线程数（取值范围：0 至 100）
   * - ``failure_count_threshold``
     - 是
     - 停止URL爬取的失败次数阈值（-1=禁用；取值范围：-1 至 10000）
   * - ``csv_file_encoding``
     - 是
     - CSV导出的编码
   * - ``search_log``
     - 否
     - 搜索查询日志的启用/禁用
   * - ``user_info``
     - 否
     - 用户信息记录的启用/禁用
   * - ``user_favorite``
     - 否
     - 收藏功能的启用/禁用
   * - ``web_api_json``
     - 否
     - JSON Web API的启用/禁用
   * - ``app_value``
     - 否
     - 应用程序专用的附加配置值
   * - ``virtual_host_value``
     - 否
     - 虚拟主机配置（用于多租户环境）
   * - ``popular_word``
     - 否
     - 热门词汇的统计与显示的启用/禁用
   * - ``default_label_value``
     - 否
     - 默认标签值
   * - ``default_sort_value``
     - 否
     - 默认排序顺序
   * - ``append_query_parameter``
     - 否
     - 向搜索结果URL附加查询参数
   * - ``login_required``
     - 否
     - 搜索是否需要登录
   * - ``login_link``
     - 否
     - 搜索页面上登录链接显示的启用/禁用
   * - ``thumbnail``
     - 否
     - 缩略图生成的启用/禁用
   * - ``result_collapsed``
     - 否
     - 搜索结果中折叠相似文档的启用/禁用
   * - ``ignore_failure_type``
     - 否
     - 要忽略的爬取失败类型
   * - ``crawling_user_agent``
     - 否
     - 爬取时发送的User-Agent字符串
   * - ``purge_search_log_day``
     - 否
     - 保留搜索日志的天数（-1=禁用；取值范围：-1 至 100000）
   * - ``purge_job_log_day``
     - 否
     - 保留作业日志的天数（-1=禁用；取值范围：-1 至 100000）
   * - ``purge_user_info_day``
     - 否
     - 保留用户信息的天数（-1=禁用；取值范围：-1 至 100000）
   * - ``purge_suggest_search_log_day``
     - 否
     - 保留建议搜索日志的天数（0=禁用；取值范围：0 至 100000）
   * - ``purge_by_bots``
     - 否
     - 要丢弃搜索日志的机器人User-Agent
   * - ``notification_to``
     - 否
     - 系统通知的接收邮箱地址
   * - ``notification_login``
     - 否
     - 在登录页面显示的通知消息
   * - ``notification_search_top``
     - 否
     - 在搜索首页显示的通知消息
   * - ``notification_advance_search``
     - 否
     - 在高级搜索页面显示的通知消息
   * - ``suggest_search_log``
     - 否
     - 来自搜索日志的建议的启用/禁用
   * - ``suggest_documents``
     - 否
     - 来自文档的建议的启用/禁用
   * - ``log_level``
     - 否
     - 系统日志的日志级别
   * - ``log_notification_enabled``
     - 否
     - ERROR/WARN日志通知的启用/禁用
   * - ``log_notification_level``
     - 否
     - 日志通知级别
   * - ``slack_webhook_urls``
     - 否
     - 用于通知的Slack Webhook URL
   * - ``google_chat_webhook_urls``
     - 否
     - 用于通知的Google Chat Webhook URL
   * - ``search_use_browser_locale``
     - 否
     - 搜索时是否使用浏览器语言区域设置
   * - ``rag_llm_name``
     - 否
     - RAG所使用的LLM提供商名称
   * - ``llm_log_level``
     - 否
     - LLM相关包的日志级别

认证相关字段
~~~~~~~~~~~~

LDAP以及SSO（OpenID Connect、SAML、SPNEGO、Entra ID）相关的设置也通过此API管理。
以下列出代表性字段（所有字段均对应管理界面的"常规"设置）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 字段
     - 说明
   * - ``ldap_provider_url``
     - LDAP连接URL
   * - ``ldap_base_dn``
     - LDAP基础DN
   * - ``ldap_security_principal``
     - 用于LDAP绑定的安全主体
   * - ``ldap_admin_security_principal``
     - 用于LDAP管理操作的安全主体
   * - ``ldap_admin_security_credentials``
     - LDAP管理员密码（不包含在响应中）
   * - ``ldap_account_filter`` / ``ldap_group_filter``
     - 用户/组搜索过滤器
   * - ``ldap_memberof_attribute``
     - 表示组成员关系的LDAP属性名
   * - ``sso_type``
     - SSO类型（``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``）
   * - ``oic_client_id`` / ``oic_client_secret`` / ``oic_auth_server_url`` 等
     - OpenID Connect的设置
   * - ``saml_idp_entityid`` / ``saml_sp_entityid`` 等
     - SAML的设置
   * - ``spnego_krb5_conf`` / ``spnego_login_conf`` 等
     - SPNEGO的设置
   * - ``entraid_client_id`` / ``entraid_tenant`` 等
     - Microsoft Entra ID的设置

存储相关字段
~~~~~~~~~~~~

也可以管理云存储（S3 / GCS）集成的设置。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 字段
     - 说明
   * - ``storage_type``
     - 存储类型（``auto`` / ``s3`` / ``gcs``）
   * - ``storage_endpoint``
     - 存储的端点URL
   * - ``storage_access_key`` / ``storage_secret_key``
     - 用于认证的访问密钥/私密密钥
   * - ``storage_bucket``
     - 存储桶名称
   * - ``storage_region``
     - S3的区域
   * - ``storage_project_id`` / ``storage_credentials_path``
     - GCS的项目ID / 凭据文件路径

.. note::

   ``ldap_admin_security_credentials``、``storage_access_key`` / ``storage_secret_key``、
   ``oic_client_id`` / ``oic_client_secret``、``entraid_client_id`` / ``entraid_client_secret``、
   ``spnego_preauth_password`` 等机密字段，如果将掩码值 ``"**********"`` 原样发送，
   该值不会被更新，已保存的值将继续保留。只有在需要更改时，才发送实际值。

   由于此判断基于去除星号后的字符串是否为空，发送空字符串（``""``）或仅由星号
   组成的值同样不会更新。因此，这些机密字段无法通过API清空为空值。

响应
----

更新成功时，仅返回 ``version`` 和 ``status``\ （不包含 ``id`` 或 ``created``）。

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0
      }
    }

如果更新失败（例如由于验证错误），API将返回 HTTP 400，响应的 ``status`` 将设置为
非零值（验证错误为 ``1``），``message`` 中包含错误详情。
有关 ``status`` 值的列表，请参阅 :doc:`api-admin-overview`。

使用示例
========

.. note::

   以下示例包含必需字段（``day_for_cleanup``、``crawling_thread_count``、
   ``failure_count_threshold``、``csv_file_encoding``）。由于这些字段无论修改内容如何
   都必须始终发送，实际操作中请通过 ``GET`` 获取当前值后再包含这些字段
   （以下示例使用默认值）。

更新爬取设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incremental_crawling": "true",
           "crawling_thread_count": 10,
           "failure_count_threshold": 100,
           "day_for_cleanup": -1,
           "csv_file_encoding": "UTF-8"
         }'

更新日志保留期限
----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "purge_search_log_day": 90,
           "purge_job_log_day": 90,
           "purge_user_info_day": 90
         }'

更新建议设置
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "suggest_search_log": "true",
           "suggest_documents": "true"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`../../admin/general-guide` - 常规设置指南
