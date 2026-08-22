==============================
索引导出功能
==============================

概述
====

索引导出功能将 OpenSearch 中已索引的搜索文档导出为本地文件系统上的 HTML 或 JSON 文件。此功能适用于以下场景：

- 创建索引内容的静态备份
- 生成文档的离线副本用于存档
- 构建静态搜索结果页面
- 将内容迁移到其他系统

导出的文件保持源文档的原始 URL 路径结构，便于管理导出的内容。

工作原理
========

索引导出作业运行时，执行以下流程：

1. **获取文档**：使用滚动 API 从 OpenSearch 高效地批量获取文档
2. **处理内容**：提取文档字段（标题、内容、URL 等），并移除需要排除的字段
3. **创建目录结构**：根据文档的 ``url`` 字段，在导出目录中重建 URL 路径结构
4. **生成文件**：创建包含文档内容的文件（HTML 或 JSON）
5. **持续直到完成**：批量处理所有文档，直到索引完全导出

滚动 API 确保能够高效处理大型文档集而不会出现内存问题。

.. note::

   导出的目标是搜索索引（``fess.search``）中的文档。不含 ``url`` 字段的文档将被跳过。

配置属性
========

在 ``fess_config.properties`` 中配置索引导出功能。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 属性
     - 默认值
     - 说明
   * - ``index.export.path``
     - ``/var/lib/fess/export``
     - 导出文件的保存目录
   * - ``index.export.exclude.fields``
     - ``cache``
     - 要从导出中排除的字段（逗号分隔）
   * - ``index.export.scroll.size``
     - ``100``
     - 每批处理的文档数
   * - ``index.export.format``
     - ``html``
     - 导出文件格式（``html`` 或 ``json``）

配置示例：

::

    index.export.path=/data/fess/export
    index.export.exclude.fields=cache,boost,role
    index.export.scroll.size=200

启用作业
========

索引导出作业已注册为计划作业，但默认处于禁用状态。

启用作业的步骤：

1. 登录 |Fess| 管理控制台
2. 导航至 **系统** > **调度器**
3. 在作业列表中找到 **Index Exporter**
4. 点击编辑作业设置
5. 使用 cron 表达式设置计划
6. 保存设置

cron 表达式示例：

- ``0 0 2 * * ?`` - 每天凌晨2点运行
- ``0 0 3 ? * SUN`` - 每周日凌晨3点运行
- ``0 0 0 1 * ?`` - 每月1日午夜运行

自定义查询过滤
==============

您可以通过修改作业脚本来自定义导出作业，仅导出特定文档。

**Index Exporter** 作业的默认脚本会导出所有文档：

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.matchAllQuery())
        .execute()

添加自定义查询过滤器的步骤：

1. 导航至 **系统** > **调度器**
2. 编辑 **Index Exporter**
3. 修改作业脚本以添加查询过滤器

日期过滤器示例（仅导出最近7天的文档）：

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.rangeQuery("created").gte("now-7d"))
        .execute()

站点过滤器示例（仅导出特定站点的文档）：

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.wildcardQuery("url", "*example.com*"))
        .execute()

以 JSON 格式导出的示例：

::

    return new org.codelibs.fess.job.IndexExportJob()
        .format("json")
        .execute()

导出文件结构
============

导出的文件按原始 URL 结构组织。

例如，URL 为 ``https://example.com/docs/guide/intro.html`` 的文档将导出到以下位置：

::

    /var/lib/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

文件路径根据文档的 ``url`` 字段按以下规则确定：

- 主机名成为顶层目录。若 URL 中不含主机名，则使用 ``_local``\ 。
- 若路径以斜杠结尾或不含路径，则创建索引文件（``index.html`` 或 ``index.json``）。
- 若路径不含文件扩展名，则根据格式附加相应扩展名（``.html`` 或 ``.json``）。
- 文件名中不允许使用的字符（``< > : " | ? * \``）将替换为 ``_``，各路径组成部分最多截断为200个字符。
- 若 URL 无法解析或检测到路径遍历，则以 URL 的哈希值为文件名保存至 ``_invalid`` 目录。

对于 HTML 格式，每个文件按以下结构生成：

- ``title`` 字段 → ``<title>`` 元素
- ``lang`` 字段 → ``<html>`` 元素的 ``lang`` 属性
- ``content`` 字段 → ``<body>`` 元素的正文内容
- 其他未排除的字段 → ``<head>`` 中的 ``<meta name="fess:字段名" content="值">`` 标签

::

    <!DOCTYPE html>
    <html lang="zh-cn">
    <head>
    <meta charset="UTF-8">
    <title>示例文档</title>
    <meta name="fess:url" content="https://example.com/docs/guide/intro.html">
    <meta name="fess:last_modified" content="2024-01-01T00:00:00.000Z">
    <meta name="fess:content_type" content="text/html">
    </head>
    <body>
    文档的正文内容
    </body>
    </html>

对于 JSON 格式，每个文件是包含所有未排除字段的 JSON 对象：

::

    {
      "url": "https://example.com/docs/guide/intro.html",
      "title": "示例文档",
      "content": "文档的正文内容",
      "last_modified": "2024-01-01T00:00:00.000Z",
      "content_type": "text/html"
    }

最佳实践
========

存储注意事项
------------

- 确保导出目录有足够的磁盘空间
- 对于大型文档集，考虑使用专用存储
- 如果运行定期导出，需定期清理旧的导出文件

性能提示
--------

- 根据文档大小调整 ``index.export.scroll.size``：
  - 较小文档：较大的批处理大小（200-500）
  - 较大文档：较小的批处理大小（50-100）
- 在低使用率时段安排导出
- 导出操作期间监控磁盘 I/O

安全建议
--------

- 为导出目录设置适当的文件权限
- 不要将导出目录直接暴露到 Web
- 若内容包含敏感信息，考虑对导出文件进行加密
- 定期审计对导出文件的访问情况

故障排除
========

导出作业未运行
--------------

1. 确认作业在调度器中已启用
2. 检查 cron 表达式语法
3. 查看 |Fess| 日志中的错误消息：

::

    tail -f /var/log/fess/fess.log | grep IndexExport

导出目录为空
------------

1. 确认索引中存在文档
2. 检查导出路径的权限
3. 验证查询过滤器（如有自定义设置）是否与文档匹配

::

    # 检查索引文档数
    curl -X GET "localhost:9201/fess.search/_count?pretty"

导出中途失败
------------

1. 检查可用磁盘空间
2. 查看日志中的内存或超时错误
3. 对于大型文档，考虑减小 ``scroll.size``
4. 检查 OpenSearch 滚动上下文的超时设置

文件无法访问
------------

1. 验证文件权限：``ls -la /var/lib/fess/export``
2. 检查目录所有者是否与 |Fess| 进程用户一致
3. 确认 SELinux 或 AppArmor 策略允许访问

相关主题
========

- :doc:`admin-index-backup` - 索引备份与恢复步骤
- :doc:`admin-logging` - 配置日志以进行故障排除
