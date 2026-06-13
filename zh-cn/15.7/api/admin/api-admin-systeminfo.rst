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

响应
----

响应包含表示产品版本的 ``version``、表示处理结果的 ``status``，以及
以下4组属性。每组属性是包含 ``key`` 和 ``value`` 的
对象数组。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
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
   * - ``envProps``
     - 环境变量列表（``key`` / ``value`` 数组）
   * - ``systemProps``
     - Java系统属性列表（``key`` / ``value`` 数组）
   * - ``fessProps``
     - |Fess| 的配置属性列表（``key`` / ``value`` 数组）
   * - ``bugReportProps``
     - 为错误报告收集的信息列表（``key`` / ``value`` 数组）

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
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

列出环境变量
------------

.. code-block:: bash

    # 以 key=value 格式显示环境变量
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-stats` - 统计API
- :doc:`api-admin-general` - 一般设置API
- :doc:`../../admin/systeminfo-guide` - 系统信息指南
