===========================================================================
第11回 通过搜索API扩展现有系统 -- CRM与内部系统的集成模式集
===========================================================================

前言
====

Fess 不仅可以作为独立的搜索系统使用，还可以作为"搜索微服务"为现有业务系统提供搜索功能。

本文介绍使用 Fess 的 API 与现有系统集成的具体模式。
涵盖将客户信息搜索嵌入 CRM、构建 FAQ 搜索小部件、搭建文档门户等实际集成场景。

目标读者
========

- 希望为现有业务系统添加搜索功能的人员
- 对使用 Fess API 进行系统集成感兴趣的人员
- 具备 Web 应用程序开发基础知识的人员

Fess API 概览
==============

下面整理 Fess 提供的主要 API。

.. list-table:: Fess API 一览
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - 用途
     - 端点
   * - 搜索 API
     - 文档的全文搜索
     - ``/api/v1/documents``
   * - 标签 API
     - 获取可用的标签
     - ``/api/v1/labels``
   * - 建议 API
     - 获取自动补全候选项
     - ``/api/v1/suggest-words``
   * - 热门词汇 API
     - 获取热门搜索关键词
     - ``/api/v1/popular-words``
   * - 健康检查 API
     - 确认系统运行状态
     - ``/api/v1/health``
   * - 管理 API
     - 配置操作（CRUD）
     - ``/api/admin/*``

访问令牌
--------

使用 API 时，建议通过访问令牌进行认证。

1. 在管理界面的 [系统] > [访问令牌] 中创建访问令牌
2. 在 API 请求的头部中包含令牌

::

    Authorization: Bearer {访问令牌}

可以为令牌分配角色，通过 API 进行的搜索也会应用基于角色的搜索结果控制。

模式1：在 CRM 中嵌入搜索功能
==============================

场景
----

为销售团队使用的 CRM 系统添加客户相关文档的搜索功能。
使用户能够从 CRM 的客户界面跨文档搜索提案书、会议记录、合同等。

实现方式
--------

在 CRM 的客户界面中嵌入搜索小部件。
将客户名称作为搜索查询发送到 Fess API，并在 CRM 界面中显示结果。

.. code-block:: javascript

    // CRM 界面中的搜索小部件
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

要点
----

- 使用 ``fields.label`` 将结果限定为销售相关文档
- 使用 ``num`` 限制显示条数（根据 CRM 界面中的可用空间调整）
- 不仅可以按客户名称搜索，还能按项目名称或项目编号搜索会更加方便

模式2：FAQ 搜索小部件
======================

场景
----

在公司内部的咨询处理系统中添加 FAQ 搜索小部件。
在员工提交咨询之前，通过搜索相关 FAQ 促进自行解决。

实现方式
--------

组合使用建议 API 和搜索 API，在输入过程中实时显示候选项。

.. code-block:: javascript

    // 输入中的建议
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

建议 API 用于在用户输入关键词时显示候选项。
当用户确定关键词并执行搜索时，通过搜索 API 获取详细的搜索结果。

要点
----

- 建议 API 的实时性非常重要，请确认响应速度
- 使用标签管理 FAQ 类别，并提供按类别筛选的功能
- 通过热门词汇 API 显示"常被搜索的关键词"，辅助用户进行搜索

模式3：文档门户
================

场景
----

构建公司内部的文档管理门户。
提供将分类浏览与全文搜索相结合的界面。

实现方式
--------

使用标签 API 获取类别列表，使用搜索 API 获取各类别内的文档。

.. code-block:: javascript

    // 获取标签列表
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // 按标签筛选的搜索
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

要点
----

- 标签 API 动态获取类别列表（标签的添加和删除会立即反映在 API 端）
- 使用 ``sort=last_modified.desc`` 将最新文档显示在前面
- 使用 ``q=*`` 可以实现无关键词的浏览（获取全部记录）

模式4：内容索引 API
=====================

场景
----

将外部系统生成的数据（日志、报告、聊天机器人的应答记录等）注册到 Fess 的索引中，使其成为可搜索的对象。

实现方式
--------

使用 Fess 的管理 API，可以从外部将文档注册到索引中。

使用管理 API 的文档端点，通过 POST 请求发送标题、URL、正文等信息。

要点
----

- 对于无法通过爬虫获取的数据源的集成非常有效
- 也可以通过批量处理一次性注册多个文档
- 适当设置访问令牌的权限，限制写入权限

API 集成最佳实践
==================

错误处理
--------

在 API 集成中，针对网络故障和 Fess 服务器维护的错误处理非常重要。

- 超时设置：为搜索 API 调用设置适当的超时
- 重试逻辑：针对临时性错误进行重试（最多约3次）
- 降级方案：Fess 无响应时提供替代显示（如"搜索服务当前不可用"）

性能考量
--------

- 响应缓存：将相同查询的结果短时间缓存
- 限制搜索结果数量：仅获取所需数量的结果（``num`` 参数）
- 字段指定：仅获取所需字段以减小响应大小

安全性
------

- 使用 HTTPS 通信
- 定期轮换访问令牌
- 将令牌权限设置为最低限度（如只读）
- 适当配置 CORS

总结
====

本文介绍了使用 Fess API 与现有系统集成的模式。

- **CRM 集成**：从客户界面搜索相关文档
- **FAQ 小部件**：通过建议 + 搜索实现实时候选项显示
- **文档门户**：通过标签 API 实现分类浏览
- **内容索引**：通过 API 注册外部数据

Fess 的 API 基于 REST，简洁易用，因此能够轻松地与各种系统集成。
能够为现有系统"事后"添加搜索功能，是 Fess 的一大优势。

下一回将介绍使 SaaS 和数据库数据变为可搜索的场景。

参考资料
========

- `Fess 搜索 API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `Fess 管理 API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
