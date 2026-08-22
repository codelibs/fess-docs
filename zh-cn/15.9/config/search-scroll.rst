========================
批量获取搜索结果
========================

概述
====

|Fess| 的常规搜索通过分页功能仅显示一定数量的搜索结果。
如需批量获取所有搜索结果，请使用滚动搜索（Scroll Search）功能。

此功能适用于数据批量导出、备份、大量数据分析等
需要处理所有搜索结果的情况。

用例
====

滚动搜索适用于以下用途。

- 搜索结果全量导出
- 数据分析用大量数据获取
- 批处理中的数据获取
- 与外部系统的数据同步
- 报告生成用数据收集

.. warning::
   滚动搜索会返回大量数据，与常规搜索相比
   会消耗更多服务器资源。请仅在必要时启用。

配置方法
========

启用滚动搜索
------------

默认情况下，出于安全和性能考虑，滚动搜索被禁用。
要启用，请在 ``app/WEB-INF/classes/fess_config.properties`` （RPM/DEB 包的情况下为
``/etc/fess/fess_config.properties`` ）中修改以下配置。

::

    api.search.scroll=true

.. note::
   配置变更后，需要重启 |Fess|\ 。

滚动上下文有效期
----------------

滚动搜索的滚动上下文有效期在 |Fess| 内部固定为 ``1m`` （1分钟）。
该值无法通过 ``fess_config.properties`` 修改。

.. note::
   ``index.scroll.search.timeout`` 配置项存在，但该项用于涉及索引更新、删除的
   内部处理（update by query / delete by query），不会影响本功能（搜索
   滚动）的超时时间。

响应字段配置
------------

可以自定义搜索结果响应中包含的字段。
默认返回多个字段，但可以通过以下配置追加字段。

::

    query.additional.scroll.response.fields=content

指定多个字段时，请用逗号分隔。

.. note::
   ``content`` 字段默认不包含在响应中。如需获取正文全文，请通过上述配置追加。

使用方法
========

基本使用方法
------------

滚动搜索通过以下 URL 访问。

::

    http://localhost:8080/api/v2/documents/all?q=搜索关键词

搜索结果以 NDJSON（Newline Delimited JSON）格式返回。
每行以 JSON 格式输出一个文档。

**示例:**

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess"

请求参数
--------

滚动搜索可使用以下参数。

.. note::
   滚动搜索仅支持 GET 方法。使用 GET 以外的方法访问时，将返回
   ``405 Method Not Allowed``\ 。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 参数名
     - 说明
   * - ``q``
     - 搜索查询（必需）
   * - ``num``
     - 一次滚动获取的条数（默认值：10，最大值：100）
   * - ``fields.label``
     - 按标签过滤

.. note::
   ``num`` 的最大值由 ``paging.search.page.max.size`` （默认值：100）控制。
   指定超过最大值的数值时，将自动截断为最大值。
   默认值使用 ``paging.search.page.size`` （默认值：10）。
   ``num`` 指定 0 以下的值时，将返回错误（``INVALID_REQUEST``）。

指定搜索查询
------------

可以像常规搜索一样指定搜索查询。

**示例：关键词搜索**

::

    curl "http://localhost:8080/api/v2/documents/all?q=搜索引擎"

**示例：字段指定搜索**

::

    curl "http://localhost:8080/api/v2/documents/all?q=title:Fess"

**示例：全量获取（无搜索条件）**

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*"

指定获取条数
------------

可以更改一次滚动获取的条数。

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess&num=100"

.. note::
   ``num`` 参数设置过大会导致内存使用量增加。
   默认最大值为 100。如需更大的值，请修改
   ``paging.search.page.max.size`` 配置。

按标签过滤
----------

可以仅获取属于特定标签的文档。

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*&fields.label=public"

关于访问控制
------------

.. note::
   滚动搜索与常规搜索相同，同样会应用基于角色的访问控制（RBAC）。
   仅返回基于请求角色信息可访问的文档，
   无查看权限的文档不会包含在结果中。

.. warning::
   滚动搜索端点默认不要求认证（任何人均可访问）。
   但返回的文档会经过上述基于角色的访问控制进行过滤。
   如需限制端点本身的访问，请通过反向代理等设置 IP 地址限制或
   认证。

响应格式
========

NDJSON 格式
-----------

滚动搜索的响应以 NDJSON（Newline Delimited JSON）格式返回。
Content-Type 为 ``application/x-ndjson; charset=UTF-8``\ 。
每行表示以 ``{"data": {...}}`` 形式包装的一个文档。

**示例:**

::

    {"data":{"url":"http://example.com/page1","title":"Page 1","digest":"..."}}
    {"data":{"url":"http://example.com/page2","title":"Page 2","digest":"..."}}
    {"data":{"url":"http://example.com/page3","title":"Page 3","digest":"..."}}

.. note::
   每个文档存储在 ``data`` 键下。客户端在解析每行后，
   请引用 ``data`` 键的值。

错误时的行为
------------

流式传输开始后若服务器端发生错误，响应的最后一行将
输出如下错误终止行。

::

    {"error":{"code":"internal_error","message":"stream error"}}

.. note::
   客户端可通过检查最后一行是否包含 ``error`` 键，来判断
   "流是否正常完成"还是"服务器端中途发生了错误"。
   需要注意的是，若错误终止行本身的写入失败，则终止行不会输出，
   流将中途结束，因此请将意外断开也视为错误处理。

响应字段
--------

默认包含的字段：

- ``score``: 搜索评分
- ``_id``: 文档 ID（OpenSearch 的文档 ID）
- ``doc_id``: 文档 ID（|Fess| 内部）
- ``boost``: 提升值
- ``content_length``: 内容长度
- ``host``: 主机名
- ``site``: 站点
- ``last_modified``: 最后更新时间
- ``timestamp``: 时间戳
- ``mimetype``: MIME 类型
- ``filetype``: 文件类型
- ``filename``: 文件名
- ``created``: 创建时间
- ``title``: 标题
- ``digest``: 正文摘要
- ``url``: 文档 URL
- ``thumbnail``: 缩略图
- ``click_count``: 点击次数
- ``favorite_count``: 收藏次数
- ``has_cache``: 是否有缓存
- ``content_title``: 显示用标题
- ``content_description``: 显示用正文摘要
- ``url_link``: 显示用链接 URL
- ``site_path``: 站点路径

.. note::
   实际输出的字段仅限于 API 响应中允许的字段。
   不存在值的字段不会输出。

.. note::
   ``content`` （正文全文）默认不包含在响应中。
   可通过 ``query.additional.scroll.response.fields`` 追加。

数据处理示例
============

Python 处理示例
---------------

.. code-block:: python

    import requests
    import json

    # 执行滚动搜索
    url = "http://localhost:8080/api/v2/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # 逐行处理 NDJSON 格式的响应
    for line in response.iter_lines():
        if line:
            record = json.loads(line)
            if "error" in record:
                # 流传输中途发生错误
                print("stream error:", record["error"])
                break
            doc = record["data"]
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

保存到文件
----------

将搜索结果保存到文件的示例：

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=*:*" > all_documents.ndjson

转换为 CSV
----------

使用 jq 命令转换为 CSV 的示例：

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=Fess" | \
        jq -r '.data | [.url, .title, .score] | @csv' > results.csv

数据分析
--------

分析获取数据的示例：

.. code-block:: python

    import json
    import pandas as pd

    # 读取 NDJSON 文件（提取每行的 data 键）
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            record = json.loads(line)
            if "data" in record:
                documents.append(record["data"])

    # 转换为 DataFrame
    df = pd.DataFrame(documents)

    # 基本统计
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL 域名分析
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

性能与最佳实践
==============

高效使用方法
------------

1. **设置适当的 num 参数**

   - 过小会增加通信开销
   - 过大会增加内存使用量
   - 默认最大值：100

2. **优化搜索条件**

   - 指定搜索条件以仅获取所需文档
   - 仅在确实需要时执行全量获取

3. **使用非高峰时段**

   - 大量数据获取请在系统负载较低的时段执行

4. **批处理使用**

   - 定期数据同步等作为批处理任务执行

内存使用量优化
--------------

处理大量数据时，请使用流式处理来抑制内存使用量。

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v2/documents/all"
    params = {"q": "*:*", "num": 100}

    # 流式处理
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                record = json.loads(line)
                if "error" in record:
                    break
                # 处理文档
                process_document(record["data"])

安全注意事项
============

访问限制
--------

滚动搜索会返回大量数据，请设置适当的访问限制。
端点本身默认不要求认证，请根据需要考虑以下对策。

1. **IP 地址限制**

   仅允许特定 IP 地址访问

2. **API 认证**

   通过反向代理等使用 API 令牌或 Basic 认证

3. **基于角色的访问控制**

   返回的文档经 |Fess| 的基于角色的访问控制过滤

速率限制
--------

为防止过度访问，建议在反向代理上设置速率限制。

故障排除
========

无法使用滚动搜索
----------------

1. 请确认 ``api.search.scroll`` 是否设置为 ``true``\ 。
2. 请确认是否已重启 |Fess|\ 。
3. 请确认错误日志。

发生超时错误
------------

1. 请减小 ``num`` 参数以分散处理。
2. 请缩小搜索条件以减少获取数据量。

内存不足错误
------------

1. 请减小 ``num`` 参数。
2. 请增加 |Fess| 的堆内存大小。
3. 请确认 OpenSearch 的堆内存大小。

响应为空
--------

1. 请确认搜索查询是否正确。
2. 请确认指定的标签和过滤条件是否正确。
3. 基于角色的访问控制会将无查看权限的文档排除在结果之外。请确认请求的角色配置。

参考信息
========

- :doc:`search-basic` - 搜索功能详情
- :doc:`search-advanced` - 搜索相关配置
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
