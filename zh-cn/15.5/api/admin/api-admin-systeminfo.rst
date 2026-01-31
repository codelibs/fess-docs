==========================
SystemInfo API
==========================

概述
====

SystemInfo API是用于获取 |Fess| 系统信息的API。
您可以查看版本信息、环境变量、JVM信息等。

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

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "fessVersion": "15.5.0",
          "opensearchVersion": "2.11.0",
          "javaVersion": "21.0.1",
          "serverName": "Apache Tomcat/10.1.15",
          "osName": "Linux",
          "osVersion": "5.15.0-89-generic",
          "osArchitecture": "amd64",
          "jvmTotalMemory": "2147483648",
          "jvmFreeMemory": "1073741824",
          "jvmMaxMemory": "4294967296",
          "processorCount": "8",
          "fileEncoding": "UTF-8",
          "userLanguage": "ja",
          "userTimezone": "Asia/Tokyo"
        },
        "environmentInfo": {
          "JAVA_HOME": "/usr/lib/jvm/java-21",
          "FESS_DICTIONARY_PATH": "/var/lib/fess/dict",
          "FESS_LOG_PATH": "/var/log/fess"
        },
        "systemProperties": {
          "java.version": "21.0.1",
          "java.vendor": "Oracle Corporation",
          "os.name": "Linux",
          "os.version": "5.15.0-89-generic",
          "user.dir": "/opt/fess",
          "user.home": "/home/fess",
          "user.name": "fess"
        }
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``fessVersion``
     - Fess版本
   * - ``opensearchVersion``
     - OpenSearch版本
   * - ``javaVersion``
     - Java版本
   * - ``serverName``
     - 应用服务器名称
   * - ``osName``
     - 操作系统名称
   * - ``osVersion``
     - 操作系统版本
   * - ``osArchitecture``
     - 操作系统架构
   * - ``jvmTotalMemory``
     - JVM总内存（字节）
   * - ``jvmFreeMemory``
     - JVM空闲内存（字节）
   * - ``jvmMaxMemory``
     - JVM最大内存（字节）
   * - ``processorCount``
     - 处理器数量
   * - ``fileEncoding``
     - 文件编码
   * - ``userLanguage``
     - 用户语言
   * - ``userTimezone``
     - 用户时区

使用示例
========

获取系统信息
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

检查版本
--------

.. code-block:: bash

    # 仅提取Fess版本
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo.fessVersion'

检查内存使用情况
----------------

.. code-block:: bash

    # 提取JVM内存信息
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo | {total: .jvmTotalMemory, free: .jvmFreeMemory, max: .jvmMaxMemory}'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-stats` - 统计API
- :doc:`api-admin-general` - 常规设置API
- :doc:`../../admin/systeminfo-guide` - 系统信息指南

