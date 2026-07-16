==========================
SystemInfo API
==========================

概述
====

SystemInfo API是用于获取 |Fess| 系统信息的API。
您可以查看环境变量、Java系统属性、|Fess| 的配置属性以及用于错误报告的信息。

基础URL
=======

::

    /api/admin/systeminfo

访问此API需要持有具备 ``Radmin-api`` 权限的访问令牌。
认证方式的详细信息请参阅 :doc:`api-admin-overview`。

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
     - 获取系统信息

获取系统信息
============

请求
----

::

    GET /api/admin/systeminfo

此端点不接受任何查询参数。

响应
----

响应包含表示产品版本的 ``version``、表示处理结果的 ``status``，以及
以下4组属性。每组属性是包含 ``label`` 和 ``value`` 的
对象数组。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``version``
     - |Fess| 的产品版本（例如：``15.7.0``）。
   * - ``status``
     - 表示处理结果的状态码。\ ``0`` 表示正常结束。
   * - ``envProps``
     - 环境变量列表（``label`` / ``value`` 的对象数组）。返回通过 ``System.getenv()`` 获取的值，不做任何修改。
   * - ``systemProps``
     - Java系统属性列表（``label`` / ``value`` 的对象数组）。返回通过 ``System.getProperties()`` 获取的值，不做任何修改。
   * - ``fessProps``
     - |Fess| 配置属性列表（``label`` / ``value`` 的对象数组）。包含 ``fess_config.properties`` 中的配置值以及通过管理界面设置的系统属性。敏感项目将被屏蔽（参见下方注意事项）。
   * - ``bugReportProps``
     - 为错误报告收集的信息列表（``label`` / ``value`` 的对象数组）。包含与OS及Java运行环境相关的主要系统属性（``os.name``、``os.version``、``java.vm.version`` 等）以及 |Fess| 的系统属性设置值。

.. note::

   ``fessProps`` 中，以下敏感配置值将被屏蔽，以 ``XXXXXXXX`` 返回：
   ``http.proxy.password``、``ldap.admin.security.credentials``、``spnego.preauth.password``、
   ``app.cipher.key``、``oic.client.id``、``oic.client.secret``\ 。

.. warning::

   ``envProps``\ （环境变量）和 ``systemProps``\ （Java系统属性）不会被屏蔽，
   其值将原样返回。如果环境变量或系统属性中包含认证信息等敏感数据，
   这些信息将出现在响应中，请注意。

使用示例
========

获取系统信息
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

提取特定的系统属性
------------------

.. code-block:: bash

    # 仅提取 java.version 的值
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

列出环境变量
------------

.. code-block:: bash

    # 以 label=value 格式显示环境变量
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-stats` - 统计API
- :doc:`api-admin-general` - 一般设置API
- :doc:`../../admin/systeminfo-guide` - 系统信息指南
