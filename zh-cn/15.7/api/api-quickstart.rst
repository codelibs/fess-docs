===================
API 快速入门
===================

本页提供快速开始使用 |Fess| API 的实用指南。

5 分钟快速上手
========================

前提条件
-------------

- |Fess| 正在运行（可通过 http://localhost:8080/ 访问）
- 在管理面板 > 系统 > 常规设置中已启用 JSON 响应

尝试搜索 API
------------------

**curl 命令示例：**

.. code-block:: bash

    # 基本搜索
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # 获取 20 条搜索结果
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # 获取第 2 页（从第 21 条结果开始）
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # 使用标签过滤搜索
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # 使用分面（聚合）搜索
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # 搜索含特殊字符的关键词（URL 编码）
    curl "http://localhost:8080/api/v1/documents?q=search%20engine"

**响应示例（格式化后）：**

.. code-block:: json

    {
      "q": "fess",
      "exec_time": 0.15,
      "record_count": 125,
      "page_size": 20,
      "page_number": 1,
      "data": [
        {
          "title": "Fess - Open Source Enterprise Search Server",
          "url": "https://fess.codelibs.org/",
          "content_description": "<strong>Fess</strong> is an easy to deploy...",
          "host": "fess.codelibs.org",
          "mimetype": "text/html"
        }
      ]
    }

尝试建议 API
-------------------

.. code-block:: bash

    # 获取建议
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # 响应示例
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

尝试标签 API
-----------------

.. code-block:: bash

    # 获取可用标签
    curl "http://localhost:8080/api/v1/labels"

尝试健康检查 API
------------------------

.. code-block:: bash

    # 检查服务器状态
    curl "http://localhost:8080/api/v1/health"

    # 响应示例
    # {"data":{"status":"green","cluster_name":"fess"}}

使用 Postman
=============

|Fess| API 可以方便地通过 Postman 使用。

集合设置
----------------

1. 打开 Postman 并创建一个新集合
2. 添加以下请求：

**搜索 API：**

- 方法: ``GET``
- URL: ``http://localhost:8080/api/v1/documents``
- 查询参数:
  - ``q``: 搜索关键词
  - ``num``: 结果数量（可选）
  - ``start``: 起始位置（可选）

**建议 API：**

- 方法: ``GET``
- URL: ``http://localhost:8080/api/v1/suggest``
- 查询参数:
  - ``q``: 输入字符串

**标签 API：**

- 方法: ``GET``
- URL: ``http://localhost:8080/api/v1/labels``

环境变量
---------------------

建议使用 Postman 环境变量来管理服务器 URL。

1. 在"Environments"中创建新环境
2. 添加变量: ``fess_url`` = ``http://localhost:8080``
3. 将请求 URL 改为 ``{{fess_url}}/api/v1/documents``

各编程语言的代码示例
====================================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # Fess 服务器 URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """调用 Fess 搜索 API"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # 使用示例
    results = search("enterprise search")
    print(f"Total hits: {results['record_count']}")
    for doc in results['data']:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v1/documents?${params}`);
      return response.json();
    }

    // 使用示例
    search('enterprise search').then(results => {
      console.log(`Total hits: ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

JavaScript (浏览器)
--------------------

.. code-block:: javascript

    // 使用 JSONP
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // 回调函数
    function handleResults(results) {
      console.log(`Total hits: ${results.record_count}`);
    }

    // 使用示例
    search('Fess', 'handleResults');

Java
----

.. code-block:: java

    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.net.URLEncoder;
    import java.nio.charset.StandardCharsets;

    public class FessApiClient {
        private static final String FESS_URL = "http://localhost:8080";
        private final HttpClient client = HttpClient.newHttpClient();

        public String search(String query) throws Exception {
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(FESS_URL + "/api/v1/documents?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("enterprise search");
            System.out.println(result);
        }
    }

API 版本兼容性
=========================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess 版本
     - API 版本
     - 备注
   * - 15.x
     - v1
     - 最新版本。完全支持所有功能
   * - 14.x
     - v1
     - API 相似。部分参数可能存在差异
   * - 13.x
     - v1
     - 基本 API 支持

.. note::

   API 兼容性保持一致，但新功能仅在最新版本中可用。
   关于各版本的详细差异，请参阅 `发布说明 <https://github.com/codelibs/fess/releases>`__。

故障排除
===============

API 无法正常工作
---------------

1. **确认 JSON 响应是否已启用**

   在管理面板 > 系统 > 常规设置中，确认"JSON 响应"已启用。

2. **浏览器中出现 CORS 错误**

   如果从浏览器访问时出现 CORS 错误，请使用 JSONP 或
   在服务器上配置 CORS 设置。

   JSONP 示例：

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **需要认证**

   如果配置了访问令牌，请在请求头中包含令牌：

   .. code-block:: bash

       curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
            "http://localhost:8080/api/v1/documents?q=fess"

下一步
==========

- :doc:`api-search` - 搜索 API 详细说明
- :doc:`api-suggest` - 建议 API 详细说明
- :doc:`admin/index` - 管理 API 的使用方法
