===========
仪表板
===========

概述
====

仪表板提供了一个 Web 管理工具,用于管理 |Fess| 访问的 OpenSearch 集群和索引。

|image0|

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table:: |Fess| 管理的索引
   :header-rows: 1

   * - 索引名称
     - 说明
   * - fess.YYYYMMDD
     - 已索引的文档
   * - fess_log
     - 访问日志
   * - fess.suggest.YYYYMMDD
     - 建议词
   * - fess_config
     - |Fess| 的配置
   * - fess_user
     - 用户/角色/组数据
   * - configsync
     - 词典配置
   * - fess_suggest
     - 建议元数据
   * - fess_suggest_array
     - 建议元数据
   * - fess_suggest_badword
     - 建议的禁用词列表
   * - fess_suggest_analyzer
     - 建议元数据
   * - fess_crawler
     - 爬取信息


以点(.)开头的索引名称是系统索引,因此不会显示。
要显示系统索引,请启用 special 复选框。

确认已索引的文档数
================================

已索引的文档数显示在 fess 索引中,如下图所示。

|image1|

单击每个索引右上角的图标,将显示索引操作菜单。
要删除已索引的文档,请在管理搜索界面中删除。请注意不要使用"delete index"删除。

.. |image0| image:: ../../../resources/images/en/15.4/admin/dashboard-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/dashboard-2.png
.. pdf            :width: 400 px
