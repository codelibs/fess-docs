=================
API 快速入门
=================

本页为 |Fess| API（v2）提供便于快速上手的实践指南。

5 分钟快速上手
==============

前提条件
--------

- |Fess| 正在运行（可通过 http://localhost:8080/ 访问）

尝试搜索 API
------------

v2 的搜索端点为 ``GET /api/v2/search``\ 。

**curl 命令示例：**

.. code-block:: bash

    # 基本搜索
    curl "http://localhost:8080/api/v2/search?q=fess"

    # 获取 20 条搜索结果（num 为每页条数，默认值为 10）
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # 跳过前 20 条结果（start 为从 0 开始的起始位置）
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # 使用标签过滤搜索
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # 使用分面（聚合）搜索
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # 日语搜索（URL 编码）
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**响应示例（格式化后）：**

v2 的响应以 ``response`` 信封返回。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fess",
        "record_count": 125,
        "page_size": 10,
        "page_number": 1,
        "data": [
          {
            "title": "Fess - オープンソース全文検索サーバー",
            "url": "https://fess.codelibs.org/ja/",
            "content_description": "<strong>Fess</strong>は簡単に構築できる...",
            "host": "fess.codelibs.org",
            "mimetype": "text/html"
          }
        ]
      }
    }

.. note::

   上述示例仅供参考。``data`` 中包含的文档字段取决于服务器配置（响应字段白名单）。
   完整的请求参数和响应字段列表，请参阅 :doc:`api-search`。
   公共响应信封、错误模型及 CSRF 的说明，请参阅 :doc:`api-overview`。

尝试建议词 API
--------------

建议词端点为 ``GET /api/v2/suggest-words``\ 。

.. code-block:: bash

    # 获取建议词
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**响应示例（格式化后）：**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fes",
        "suggest_words": [
          { "text": "fess", "types": ["document"] }
        ]
      }
    }

尝试标签 API
------------

.. code-block:: bash

    # 获取可用标签列表
    curl "http://localhost:8080/api/v2/labels"

尝试健康检查 API
----------------

健康检查端点为 ``GET /api/v2/health``\ 。

.. code-block:: bash

    # 检查服务器（搜索引擎集群）状态
    curl "http://localhost:8080/api/v2/health"

**响应示例（格式化后）：**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess",
          "status": "green",
          "ping_status": 200
        }
      }
    }

使用 Postman
============

|Fess| API 可以方便地通过 Postman 使用。

集合设置
--------

1. 启动 Postman，创建新集合
2. 添加以下请求：

**搜索 API：**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query Parameters:
  - ``q``: 搜索关键词
  - ``num``: 结果数量（可选）
  - ``start``: 起始位置（可选）

**建议词 API：**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query Parameters:
  - ``q``: 输入字符串

**标签 API：**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

环境变量设置
------------

建议使用 Postman 的环境变量来管理服务器 URL。

1. 在"Environments"中创建新环境
2. 添加变量：\ ``fess_url`` = ``http://localhost:8080``
3. 将请求 URL 改为 ``{{fess_url}}/api/v2/search``

各编程语言代码示例
==================

以下示例均调用 ``GET /api/v2/search`` 并引用 ``response`` 信封。

Python
------

.. code-block:: python

    import requests

    # Fess 服务器的URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess検索APIを呼び出す"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # 使用例
    results = search("Fess 検索")
    print(f"ヒット件数: {results['response']['record_count']}")
    for doc in results["response"]["data"]:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v2/search?${params}`);
      return response.json();
    }

    // 使用例
    search('Fess 検索').then(results => {
      console.log(`ヒット件数: ${results.response.record_count}`);
      results.response.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

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
                .uri(URI.create(FESS_URL + "/api/v2/search?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("Fess 検索");
            System.out.println(result);
        }
    }

API 版本对应表
==============

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess 版本
     - API 版本
     - 备注
   * - 15.x
     - v2
     - 最新版本。支持所有功能
   * - 14.x
     - v1
     - 仅支持旧 API
   * - 13.x
     - v1
     - 支持基本 API

.. note::

   |Fess| 15.7 中，原有的 ``/api/v1`` JSON 搜索 API 和聊天 API 已废弃。
   使用 ``/api/v1`` 的客户端请迁移至 ``/api/v2``\ 。
   各版本间的详细差异，请参阅 `发布说明 <https://github.com/codelibs/fess/releases>`__。

故障排除
========

API 无法正常工作
----------------

1. **确认 |Fess| 是否正在运行**

   请确认可以访问 http://localhost:8080/。

2. **确认端点是否为 v2**

   请确认请求目标路径为 ``/api/v2/...``\ 。
   原有的 ``/api/v1`` 端点已废弃。

3. **需要认证时**

   有关需要认证的端点，请参阅 :doc:`api-auth`。

下一步
======

- :doc:`api-overview` - 通用 API 规范（响应信封、错误模型、认证/CSRF）
- :doc:`api-search` - 搜索 API 详细说明
- :doc:`api-suggest` - 建议词 API 详细说明
- :doc:`api-label` - 标签 API 详细说明
- :doc:`api-health` - 健康检查 API 详细说明
- :doc:`admin/index` - 管理 API 的使用方法
