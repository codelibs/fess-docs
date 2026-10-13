=========
维护
=========

概述
====

维护页面用于执行系统数据操作。

|image0|

操作方法
======

重新索引
------------

可以从现有的 fess 索引重新创建新索引。
在需要更改索引映射等情况下执行。


配置项
------

更新别名
::::::::::::

启用后,可以在重新索引完成后,将分配给现有索引的 fess.search 和 fess.update 别名重新指向新索引。


重置字典
:::::::::

启用后,可以重置字典配置。

当 ``search_engine.type`` 为 ``vanilla`` 或 ``aws`` 时，不显示此项。


分片数
::::::::

可以指定 OpenSearch 的分片数(index.number_of_shards)。


最大副本数
:::::::::::

可以指定 OpenSearch 的最大副本数(index.auto_expand_replicas)。


重建配置索引
--------------------------

可以使用最新的映射重建配置索引（fess_config、fess_user、fess_log）。
此操作在后台运行。请在执行前备份配置等数据。


目标索引
::::::::::::

选择要重建的索引。可以从 fess_config、fess_user、fess_log 中选择。


加载默认数据
::::::::::::::::

启用后，重建时将加载默认数据。现有文档不会被覆盖。


重新加载文档索引
--------------------------

为了反映索引配置,可以重新加载文档索引。
使词典的更改在搜索中生效时也使用此功能：先将已保存的词典写入 OpenSearch 中的文件，然后关闭并重新打开
``fess.update`` 别名所指向的索引。索引关闭期间无法搜索该索引。详情请参见
:ref:`dict-apply-changes`\ 。

当 ``search_engine.type`` 为 ``vanilla`` 或 ``aws`` 时，不显示此功能。


爬虫索引
----------------

可以删除 fess_crawler 索引(爬网信息)。
请勿在爬虫运行期间执行。


诊断
----

可以下载诊断用的 zip 文件。zip 的 ``log<yyyyMMddHHmm>/`` 目录下包含以下文件。

- 日志目录中的 ``*.log`` 和 ``*.log.gz`` （ ``fess.log`` 、 ``fess-crawler.log`` 、 ``audit.log`` 、 ``searchlog.log`` 等）
- ``system.properties`` （系统设置）和 ``fess_config.properties`` （应用程序设置）
- ``fess_basic_config.bulk`` （爬取设置、认证设置、标签等设置索引的内容。不包含管理 API 的访问令牌）
- ``es_cat_*.txt`` 和 ``es_*.json`` （OpenSearch ``_cat`` API 的输出，以及集群、节点、任务等的状态）

在 ``system.properties`` 和 ``fess_config.properties`` 中，会按照与系统信息页面相同的规则，将机密值替换为 ``XXXXXXXX`` 。例如存储的密钥、Webhook URL（Slack 和 Google Chat）、SSO 客户端密钥、LLM 和嵌入的 API 密钥、应用程序的加密密钥（ ``app.cipher.key`` ）等。键会保留，因此仍可看出存在哪些设置。

.. note::

   日志文件和 ``fess_basic_config.bulk`` 的内容不会被屏蔽。将 zip 发送到外部之前，请先确认其内容。

.. |image0| image:: ../../../resources/images/en/15.9/admin/maintenance-1.png
