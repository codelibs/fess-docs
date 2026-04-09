============================================
实践指南
============================================

用 Fess 实现知识活用战略
=========================

以目标为导向的企业搜索实践指南。
以用例为起点，全23回从 Fess 的导入到 AI 活用进行全面解说。

**基础篇（面向初学者）**

- :doc:`articles/guide-01` - 解析企业信息检索的必要性与分散信息的活用课题
- :doc:`articles/guide-02` - 用 Docker Compose 几分钟内启动 Fess 并体验搜索的快速入门
- :doc:`articles/guide-03` - 向现有网站嵌入搜索小部件的3种模式介绍
- :doc:`articles/guide-04` - 构建跨文件服务器和云存储等多数据源的统一检索
- :doc:`articles/guide-05` - 使用角色和标签实现按部门·权限的搜索结果过滤

**实践解决方案篇（面向中级用户）**

- :doc:`articles/guide-06` - 构建统一检索 Git·Wiki·工单等开发知识的环境
- :doc:`articles/guide-07` - 配置和运维 Google Drive·SharePoint·Box 的统一搜索
- :doc:`articles/guide-08` - 基于搜索日志分析的调优改进循环实践
- :doc:`articles/guide-09` - 正确搜索日语·英语·中文文档的分析器配置
- :doc:`articles/guide-10` - 生产环境的监控·备份·故障对策最佳实践
- :doc:`articles/guide-11` - 使用 REST API 与 CRM·内部系统的集成模式集
- :doc:`articles/guide-12` - Salesforce·数据库等 SaaS 数据的索引化步骤

**架构与扩展篇（面向高级用户）**

- :doc:`articles/guide-13` - 用一个 Fess 实例为多个组织提供服务的租户设计
- :doc:`articles/guide-14` - 从单服务器到集群架构的分阶段扩展策略
- :doc:`articles/guide-15` - SSO（OIDC/SAML）集成与零信任环境下的访问控制设计
- :doc:`articles/guide-16` - Fess 配置的代码管理与 CI/CD 流水线自动化部署
- :doc:`articles/guide-17` - 自定义数据源插件和 Ingest 流水线的实现方法

**AI·下一代搜索篇（面向高级用户）**

- :doc:`articles/guide-18` - 概述从关键词搜索到向量搜索·语义搜索的进化
- :doc:`articles/guide-19` - 利用 RAG 构建基于企业文档的问答系统的步骤
- :doc:`articles/guide-20` - 将 Fess 作为 MCP 服务器与 Claude 等外部 AI 工具集成
- :doc:`articles/guide-21` - 通过向量嵌入实现文本·图像的跨模态搜索
- :doc:`articles/guide-22` - 用 OpenSearch Dashboards 可视化搜索日志并分析信息活用

**总结**

- :doc:`articles/guide-23` - 整合全23回要素的全公司知识基础设施参考架构

用例与示例
==========

- :doc:`articles/use-cases` - 按行业和企业规模分类的用例
- :doc:`articles/comparison` - Fess与其他搜索解决方案的比较（Elasticsearch、Solr等）

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-03
   articles/guide-04
   articles/guide-05
   articles/guide-06
   articles/guide-07
   articles/guide-08
   articles/guide-09
   articles/guide-10
   articles/guide-11
   articles/guide-12
   articles/guide-13
   articles/guide-14
   articles/guide-15
   articles/guide-16
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-22
   articles/guide-23
   articles/use-cases
   articles/comparison
