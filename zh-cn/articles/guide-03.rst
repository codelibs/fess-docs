============================================================
第3回 在企业内部门户中嵌入搜索功能 -- 为现有网站添加搜索功能的场景
============================================================

前言
========

上一篇文章中，我们使用 Docker Compose 启动了 Fess 并体验了搜索功能。
然而在实际业务中，除了"直接使用 Fess 的搜索页面"之外，还有很多"想在现有的企业内部网站或门户中添加搜索功能"的需求。

本文将介绍三种将 Fess 搜索功能集成到现有网站中的方法，并解说各自的特点和选择标准。

目标读者
========

- 希望在企业内部门户或网站中添加搜索功能的人
- 具备前端开发基础知识的人
- 已按照第2回的步骤启动了 Fess

所需环境
==========

- 第2回中搭建的 Fess 环境（Docker Compose）
- 用于测试的网页（本地 HTML 文件也可以）

三种集成方法
====================

将 Fess 的搜索功能集成到现有网站中，主要有以下三种方法。

.. list-table:: 集成方法对比
   :header-rows: 1
   :widths: 15 30 25 30

   * - 方法
     - 概要
     - 开发工作量
     - 适用场景
   * - FSS（Fess Site Search）
     - 只需嵌入 JavaScript 标签
     - 最小（几行代码）
     - 希望便捷地添加搜索功能
   * - 搜索表单联动
     - 通过 HTML 表单跳转到 Fess
     - 小（仅修改 HTML）
     - 希望直接使用 Fess 的搜索页面
   * - 搜索 API 联动
     - 使用 JSON API 构建自定义 UI
     - 中到大（前端开发）
     - 希望完全自定义设计和行为

下面将结合具体场景逐一解说各种方法。

方法1: 使用 FSS（Fess Site Search）便捷添加
==================================================

场景
--------

企业内部有一个门户网站，拥有 HTML 的编辑权限，但希望避免大规模改动。
希望通过最小限度的修改，使用户能够在门户上搜索企业内部文档。

什么是 FSS
--------

Fess Site Search（FSS）是一种只需在网页中嵌入 JavaScript 标签即可添加搜索功能的机制。
搜索框和搜索结果的显示全部由 JavaScript 处理，因此几乎不需要修改现有页面的结构。

实现步骤
--------

1. 在 Fess 管理页面中允许 API 访问。
   在［系统］ > ［常规设置］ 页面中，启用 JSON 响应。

2. 在需要添加搜索功能的页面中嵌入以下代码。

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

在放置 ``<fess:search>`` 标签的位置，将显示搜索框和搜索结果。

自定义
------------

FSS 的外观可以通过 CSS 进行自定义。
通过覆盖 Fess 提供的默认样式，可以使其匹配现有网站的设计。

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

方法2: 通过搜索表单联动简单实现
================================================

场景
--------

企业内部门户的头部已经有导航栏。
希望在导航栏中添加搜索框，搜索执行时跳转到 Fess 的搜索结果页面。
不使用 JavaScript，仅用 HTML 实现。

实现步骤
--------

在现有的导航栏中添加如下 HTML 表单。

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="企业内部搜索..." />
      <button type="submit">搜索</button>
    </form>

仅此即可实现搜索执行时跳转到 Fess 的搜索结果页面。
通过自定义 Fess 端搜索页面的设计，可以提供统一的用户体验。

自定义 Fess 搜索页面
----------------------------

Fess 的搜索页面由 JSP 文件构成，也可以从管理页面进行编辑。

1. 在管理页面中选择 ［系统］ > ［页面设计］
2. 自定义页眉、页脚、CSS 等

例如，通过将 Logo 与企业内部门户统一，或统一配色方案，可以为用户提供无违和感的搜索体验。

利用路径映射
--------------------

可以将搜索结果中显示的 URL 转换为用户更容易访问的 URL。
例如，即使爬取时的 URL 为 ``http://internal-server:8888/docs/``，也可以在搜索结果中显示为 ``https://portal.example.com/docs/``。

可以在管理页面的 ［爬虫］ > ［路径映射］ 中进行设置。

方法3: 使用搜索 API 完全自定义
======================================

场景
--------

希望在企业内部业务应用中集成搜索功能。
希望完全控制设计和搜索结果的显示方式。
拥有前端开发资源。

搜索 API 基础
----------------

Fess 提供基于 JSON 的搜索 API。

::

    GET http://localhost:8080/api/v1/documents?q=检索关键词

响应为以下 JSON 格式。

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "ドキュメントタイトル",
          "url": "https://example.com/doc.html",
          "content_description": "...検索キーワードを含む本文の抜粋..."
        }
      ]
    }

JavaScript 实现示例
----------------------

以下是使用搜索 API 的基本实现示例。

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

API 附加参数
---------------------

搜索 API 可以通过各种参数来自定义搜索行为。

.. list-table:: 主要 API 参数
   :header-rows: 1
   :widths: 20 50 30

   * - 参数
     - 说明
     - 示例
   * - ``q``
     - 搜索关键词
     - ``q=Fess``
   * - ``num``
     - 每页显示条数
     - ``num=20``
   * - ``start``
     - 搜索结果的起始位置
     - ``start=20``
   * - ``fields.label``
     - 按标签筛选
     - ``fields.label=intranet``
   * - ``sort``
     - 排序方式
     - ``sort=last_modified.desc``

通过活用 API，可以实现搜索结果的过滤、排序、分页等精细控制。

如何选择合适的方法
========================

根据实际情况选择三种方法。

**选择 FSS 的场景**

- 开发资源有限
- 希望以最小改动在现有页面中添加搜索功能
- 搜索功能的外观使用标准样式即可

**选择搜索表单联动的场景**

- Fess 搜索页面的设计已经足够
- 不想使用 JavaScript
- 只需在页眉或侧边栏中添加搜索框

**选择搜索 API 的场景**

- 希望完全自定义搜索结果的显示
- 希望集成到 SPA（Single Page Application）中
- 希望对搜索结果应用自定义逻辑（过滤、高亮等）
- 拥有前端开发资源

也可以组合使用
----------------

这些方法并不是互斥的。
例如，在首页通过 FSS 便捷地添加搜索功能，而在专用搜索页面提供基于 API 的自定义 UI，这样的组合方式也是有效的。

总结
======

本文介绍了将 Fess 搜索功能集成到现有网站中的三种方法。

- **FSS**: 仅通过嵌入 JavaScript 标签即可添加搜索功能
- **搜索表单联动**: 通过 HTML 表单跳转到 Fess 的搜索页面
- **搜索 API**: 使用 JSON API 构建完全自定义的搜索体验

无论选择哪种方法，都可以直接利用 Fess 后端提供的搜索质量。
请根据需求和开发资源选择最合适的方法。

下一篇文章将介绍统一搜索文件服务器和云存储等多个数据源的场景。

参考资料
========

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `Fess 搜索 API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
