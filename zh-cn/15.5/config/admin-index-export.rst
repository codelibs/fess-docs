==============
索引导出功能
==============

概述
====

索引导出功能允许您将 OpenSearch 中索引的搜索文档导出为本地文件系统上的 HTML 文件。此功能适用于以下场景：

- 创建索引内容的静态备份
- 生成文档的离线副本用于存档
- 构建静态搜索结果页面
- 将内容迁移到其他系统

导出的文件保持源文档的原始 URL 路径结构，便于浏览和管理导出的内容。

工作原理
========

索引导出作业运行时，执行以下流程：

1. **查询文档**：使用滚动 API 从 OpenSearch 检索文档，实现高效批处理
2. **处理内容**：提取文档字段（标题、内容、URL 等）
3. **创建目录结构**：在导出目录中复制 URL 路径结构
4. **生成 HTML 文件**：创建包含文档内容的 HTML 文件
5. **持续直到完成**：批量处理所有文档直到索引完全导出

滚动 API 确保高效处理大型文档集而不会出现内存问题。

配置属性
========

在 ``fess_config.properties`` 中配置索引导出功能：

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 属性
     - 默认值
     - 说明
   * - ``index.export.path``
     - ``/var/fess/export``
     - 导出文件存储目录
   * - ``index.export.exclude.fields``
     - ``cache``
     - 要排除的字段列表（逗号分隔）
   * - ``index.export.scroll.size``
     - ``100``
     - 每批处理的文档数

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
3. 在作业列表中找到 **Index Export Job**
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

添加自定义查询过滤器：

1. 导航至 **系统** > **调度器**
2. 编辑 **Index Export Job**
3. 修改作业脚本以包含查询过滤器

带日期过滤器的脚本示例：

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "created:>=now-7d"
    job.execute()

带站点过滤器的脚本示例：

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "url:*example.com*"
    job.execute()

导出文件结构
============

导出的文件按原始 URL 结构组织。

例如，URL 为 ``https://example.com/docs/guide/intro.html`` 的文档将导出到：

::

    /var/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

每个导出的 HTML 文件包含：

- 文档标题
- 主要内容正文
- 元数据（最后修改日期、内容类型等）
- 原始 URL 引用

最佳实践
========

存储注意事项
------------

- 确保导出目录有足够的磁盘空间
- 对于大型文档集，考虑使用专用存储
- 如果运行定期导出，实施旧导出的定期清理

性能提示
--------

- 根据文档大小调整 ``index.export.scroll.size``：
  - 较小文档：较大的批处理大小（200-500）
  - 较大文档：较小的批处理大小（50-100）
- 在低使用率时段安排导出
- 监控导出操作期间的磁盘 I/O

安全建议
--------

- 为导出目录设置适当的文件权限
- 不要将导出目录直接暴露给 Web
- 如果包含敏感信息，考虑加密导出内容
- 定期审计对导出文件的访问

故障排除
========

导出作业未运行
--------------

1. 验证作业在调度器中已启用
2. 检查 cron 表达式语法
3. 查看 |Fess| 日志中的错误消息：

::

    tail -f /var/log/fess/fess.log | grep IndexExport

导出目录为空
------------

1. 确认索引中存在文档
2. 检查导出路径权限
3. 验证查询过滤器（如果自定义）是否匹配文档

::

    # 检查索引文档数
    curl -X GET "localhost:9201/fess.YYYYMMDD/_count?pretty"

导出中途失败
------------

1. 检查可用磁盘空间
2. 查看日志中的内存或超时错误
3. 对于大型文档，考虑减小 ``scroll.size``
4. 检查 OpenSearch 滚动上下文超时设置

文件无法访问
------------

1. 验证文件权限：``ls -la /var/fess/export``
2. 检查目录所有者是否与 |Fess| 进程用户匹配
3. 确认 SELinux 或 AppArmor 策略允许访问

相关主题
========

- :doc:`admin-index-backup` - 索引备份和恢复程序
- :doc:`admin-logging` - 配置日志设置以进行故障排除
