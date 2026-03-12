==================
批量获取搜索结果
==================

概述
====

|Fess| 的常规搜索通过分页功能仅显示一定数量的搜索结果。
如需批量获取所有搜索结果,请使用滚动搜索(Scroll Search)功能。

此功能适用于数据批量导出、备份、大量数据分析等
需要处理所有搜索结果的情况。

用例
============

滚动搜索适用于以下用途。

- 搜索结果全量导出
- 数据分析用大量数据获取
- 批处理中的数据获取
- 与外部系统的数据同步
- 报告生成用数据收集

.. warning::
   滚动搜索会返回大量数据,与常规搜索相比
   会消耗更多服务器资源。请仅在必要时启用。

配置方法
========

启用滚动搜索
----------------------

默认情况下,出于安全和性能考虑,滚动搜索被禁用。
要启用,请在 ``app/WEB-INF/classes/fess_config.properties`` 或 ``/etc/fess/fess_config.properties`` 中
修改以下配置。

::

    api.search.scroll=true

.. note::
   配置变更后,需要重启 |Fess|。

响应字段配置
--------------------------

可以自定义搜索结果响应中包含的字段。
默认仅返回基本字段,但可以指定其他字段。

::

    query.additional.scroll.response.fields=content,mimetype,filename,created,last_modified

指定多个字段时,请用逗号分隔。

滚动超时配置
----------------------------

可以配置滚动上下文的有效期。
默认为1分钟。

::

    api.search.scroll.timeout=1m

单位:
- ``s``: 秒
- ``m``: 分钟
- ``h``: 小时

使用方法
========

基本使用方法
----------------

滚动搜索通过以下 URL 访问。

::

    http://localhost:8080/json/scroll?q=搜索关键词

搜索结果以 NDJSON(Newline Delimited JSON)格式返回。
每行以 JSON 格式输出一个文档。

**示例:**

::

    curl "http://localhost:8080/json/scroll?q=Fess"

请求参数
--------------------

滚动搜索可使用以下参数。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 参数名
     - 说明
   * - ``q``
     - 搜索查询(必需)
   * - ``size``
     - 一次滚动获取的条数(默认: 100)
   * - ``scroll``
     - 滚动上下文有效时间(默认: 1m)
   * - ``fields.label``
     - 按标签过滤

指定搜索查询
----------------

可以像常规搜索一样指定搜索查询。

**示例: 关键词搜索**

::

    curl "http://localhost:8080/json/scroll?q=搜索引擎"

**示例: 字段指定搜索**

::

    curl "http://localhost:8080/json/scroll?q=title:Fess"

**示例: 全量获取(无搜索条件)**

::

    curl "http://localhost:8080/json/scroll?q=*:*"

指定获取条数
--------------

可以更改一次滚动获取的条数。

::

    curl "http://localhost:8080/json/scroll?q=Fess&size=500"

.. note::
   ``size`` 参数过大会增加内存使用量。
   通常建议设置在100〜1000范围内。

按标签过滤
--------------------------

可以仅获取属于特定标签的文档。

::

    curl "http://localhost:8080/json/scroll?q=*:*&fields.label=public"

需要认证时
----------------

使用基于角色的搜索时,需要包含认证信息。

::

    curl -u username:password "http://localhost:8080/json/scroll?q=Fess"

或使用 API 令牌:

::

    curl -H "Authorization: Bearer YOUR_API_TOKEN" \
         "http://localhost:8080/json/scroll?q=Fess"

响应格式
==============

NDJSON 格式
----------

滚动搜索的响应以 NDJSON(Newline Delimited JSON)格式返回。
每行表示一个文档。

**示例:**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

响应字段
--------------------

默认包含的主要字段:

- ``url``: 文档 URL
- ``title``: 标题
- ``content``: 正文(摘录)
- ``score``: 搜索评分
- ``boost``: 提升值
- ``created``: 创建时间
- ``last_modified``: 最后更新时间

数据处理示例
============

Python 处理示例
----------------

.. code-block:: python

    import requests
    import json

    # 执行滚动搜索
    url = "http://localhost:8080/json/scroll"
    params = {
        "q": "Fess",
        "size": 100
    }

    response = requests.get(url, params=params, stream=True)

    # 逐行处理 NDJSON 格式的响应
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

保存到文件
----------------

将搜索结果保存到文件的示例:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=*:*" > all_documents.ndjson

转换为 CSV
-----------

使用 jq 命令转换为 CSV 的示例:

.. code-block:: bash

    curl "http://localhost:8080/json/scroll?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

数据分析
----------

分析获取数据的示例:

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # 读取 NDJSON 文件
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # 转换为 DataFrame
    df = pd.DataFrame(documents)

    # 基本统计
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL 域名分析
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

性能和最佳实践
==================================

高效使用方法
----------------

1. **设置适当的 size 参数**

   - 太小会增加通信开销
   - 太大会增加内存使用量
   - 推荐: 100〜1000

2. **优化搜索条件**

   - 指定搜索条件以仅获取所需文档
   - 仅在确实需要时执行全量获取

3. **使用非高峰时间**

   - 大量数据获取请在系统负载较低的时段执行

4. **批处理使用**

   - 定期数据同步等作为批处理任务执行

内存使用量优化
--------------------

处理大量数据时,使用流处理来抑制内存使用量。

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/json/scroll"
    params = {"q": "*:*", "size": 100}

    # 流式处理
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # 处理文档
                process_document(doc)

安全注意事项
====================

访问限制
------------

滚动搜索会返回大量数据,请设置适当的访问限制。

1. **IP 地址限制**

   仅允许特定 IP 地址访问

2. **API 认证**

   使用 API 令牌或 Basic 认证

3. **基于角色的限制**

   仅允许具有特定角色的用户访问

速率限制
----------

为防止过度访问,建议在反向代理上设置速率限制。

故障排除
======================

无法使用滚动搜索
----------------------------

1. 请确认 ``api.search.scroll`` 是否设置为 ``true``。
2. 请确认是否已重启 |Fess|。
3. 请确认错误日志。

发生超时错误
----------------------------

1. 请增加 ``api.search.scroll.timeout`` 的值。
2. 请减小 ``size`` 参数以分散处理。
3. 请缩小搜索条件以减少获取数据量。

内存不足错误
----------------

1. 请减小 ``size`` 参数。
2. 请增加 |Fess| 的堆内存大小。
3. 请确认 OpenSearch 的堆内存大小。

响应为空
--------------------

1. 请确认搜索查询是否正确。
2. 请确认指定的标签和过滤条件是否正确。
3. 请确认基于角色的搜索权限设置。

参考信息
========

- :doc:`search-basic` - 搜索功能详情
- :doc:`search-scroll` - 搜索相关配置
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
