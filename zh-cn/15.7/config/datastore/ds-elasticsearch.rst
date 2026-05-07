==================================
Elasticsearch/OpenSearch连接器
==================================

概述
====

Elasticsearch/OpenSearch连接器提供从Elasticsearch或OpenSearch集群获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-elasticsearch`` 插件。

支持版本
==============

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

前提条件
========

1. 需要安装插件
2. 需要对Elasticsearch/OpenSearch集群的读取访问权限
3. 需要执行查询的权限

插件安装
------------------------

方法1: 直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # 放置
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或者
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 从管理界面安装

1. 打开「系统」→「插件」
2. 上传JAR文件
3. 重启 |Fess|

配置方法
========

从管理界面的「爬虫」→「数据存储」→「新建」进行配置。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 名称
     - External Elasticsearch
   * - 处理器名称
     - ElasticsearchDataStore
   * - 启用
     - 开

参数设置
----------------

基本连接:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    size=100
    scroll=5m

带认证的连接:

::

    settings.fesen.http.url=https://elasticsearch.example.com:9200
    index=myindex
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=100
    scroll=5m

多主机设置:

::

    settings.fesen.http.url=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    size=100
    scroll=5m

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - 参数
     - 必需
     - 说明
   * - ``settings.fesen.http.url``
     - 否
     - Elasticsearch/OpenSearch主机（可用逗号分隔指定多个）。未指定时会发生连接错误
   * - ``index``
     - 否
     - 目标索引名（默认: ``_all``）。可用逗号分隔指定多个
   * - ``settings.fesen.username``
     - 否
     - 认证用户名
   * - ``settings.fesen.password``
     - 否
     - 认证密码
   * - ``size``
     - 否
     - 滚动时的获取数量（默认: 100）
   * - ``scroll``
     - 否
     - 滚动超时时间（默认: 1m）
   * - ``query``
     - 否
     - 查询JSON（默认: match_all）。仅指定查询主体（外部 ``{"query":...}`` 包装不需要）
   * - ``fields``
     - 否
     - 要获取的字段（逗号分隔）
   * - ``timeout``
     - 否
     - 请求超时时间（默认: 1m）
   * - ``preference``
     - 否
     - 搜索执行时的分片副本优先设置（默认: ``_local``）
   * - ``delete.processed.doc``
     - 否
     - 是否从源索引中删除已处理的文档（默认: false）
   * - ``readInterval``
     - 否
     - 每个文档处理之间的等待时间（毫秒，默认: 0）

脚本设置
--------------

基本映射:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

访问嵌套字段:

::

    url=source.metadata.url
    title=source.title
    content=source.body.content
    author=source.author.name
    created=source.created_at
    last_modified=source.updated_at

可用字段
~~~~~~~~~~~~~~~~~~~~

- ``source.<field_name>`` - Elasticsearch文档的 ``_source`` 字段
- ``id`` - 文档ID
- ``index`` - 索引名
- ``score`` - 搜索得分
- ``version`` - 文档版本
- ``seqNo`` - 序列号
- ``primaryTerm`` - 主要期限
- ``clusterAlias`` - 集群别名（用于跨集群搜索）
- ``hit`` - SearchHit对象（高级用法）

查询设置
============

获取所有文档
--------------------

默认获取所有文档。
如果不指定 ``query`` 参数，将使用 ``match_all``。

特定条件过滤
--------------------------

::

    query={"term":{"status":"published"}}

范围指定:

::

    query={"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}

多条件:

::

    query={"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}

.. note::
   ``query`` 参数仅接受查询主体。不需要外部 ``{"query":...}`` 包装。
   排序等搜索级别的选项不能在此参数中指定。

只获取特定字段
========================

使用fields参数限制获取字段
----------------------------------------

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

要获取所有字段，请不指定 ``fields`` 或留空。

使用示例
======

基本索引爬取
------------------------------

参数:

::

    settings.fesen.http.url=http://localhost:9200
    index=articles
    size=100
    scroll=5m

脚本:

::

    url=source.url
    title=source.title
    content=source.content
    created=source.created_at
    last_modified=source.updated_at

从带认证的集群爬取
------------------------------

参数:

::

    settings.fesen.http.url=https://es.example.com:9200
    index=products
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=200
    scroll=10m

脚本:

::

    url="https://shop.example.com/product/" + source.product_id
    title=source.name
    content=source.description + " " + source.specifications
    digest=source.category
    last_modified=source.updated_at

从多个索引爬取
------------------------------

参数:

::

    settings.fesen.http.url=http://localhost:9200
    index=logs-2024-*
    query={"term":{"level":"error"}}
    size=100

脚本:

::

    url="https://logs.example.com/view/" + id
    title=source.message
    content=source.stack_trace
    digest=source.service + " - " + source.level
    last_modified=source.timestamp

OpenSearch集群爬取
----------------------------

参数:

::

    settings.fesen.http.url=https://opensearch.example.com:9200
    index=documents
    settings.fesen.username=admin
    settings.fesen.password=admin
    size=100
    scroll=5m

脚本:

::

    url=source.url
    title=source.title
    content=source.body
    last_modified=source.modified_date

限制字段爬取
----------------------------

参数:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    size=100

脚本:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

多主机负载均衡
----------------------

参数:

::

    settings.fesen.http.url=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=5m

脚本:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

故障排除
======================

连接错误
----------

**症状**: ``Connection refused`` 或 ``No route to host``

**确认事项**:

1. 确认主机URL是否正确（协议、主机名、端口）
2. 确认Elasticsearch/OpenSearch是否已启动
3. 确认防火墙设置
4. 如果是HTTPS，确认证书是否有效

认证错误
----------

**症状**: ``401 Unauthorized`` 或 ``403 Forbidden``

**确认事项**:

1. 确认用户名和密码是否正确
2. 确认用户是否有适当的权限:

   - 索引的读取权限
   - Scroll API的使用权限

3. 如果启用了Elasticsearch Security（X-Pack），确认是否正确配置

找不到索引
--------------------------

**症状**: ``index_not_found_exception``

**确认事项**:

1. 确认索引名是否正确（包括大小写）
2. 确认索引是否存在:

   ::

       GET /_cat/indices

3. 确认通配符模式是否正确（例: ``logs-*``）

查询错误
------------

**症状**: ``parsing_exception`` 或 ``search_phase_execution_exception``

**确认事项**:

1. 确认查询JSON是否正确
2. 确认查询是否与Elasticsearch/OpenSearch版本兼容
3. 确认字段名是否正确
4. 直接在Elasticsearch/OpenSearch上测试查询:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

滚动超时
----------------------

**症状**: ``No search context found`` 或 ``Scroll timeout``

**解决方法**:

1. 增加 ``scroll``:

   ::

       scroll=10m

2. 减小 ``size``:

   ::

       size=50

3. 确认集群资源

大量数据爬取
--------------------

**症状**: 爬取速度慢或超时

**解决方法**:

1. 调整 ``size``（太大会变慢）:

   ::

       size=100  # 默认
       size=500  # 较大

2. 使用 ``fields`` 限制获取字段
3. 使用 ``query`` 只过滤必要的文档
4. 分割成多个数据存储（按索引、时间范围等）

内存不足
----------

**症状**: OutOfMemoryError

**解决方法**:

1. 减小 ``size``
2. 使用 ``fields`` 限制获取字段
3. 增加 |Fess| 的堆大小
4. 排除大字段（二进制数据等）

SSL/TLS连接
===========

自签名证书的情况
--------------------

.. warning::
   在生产环境中请使用正确签名的证书。

使用自签名证书时，将证书添加到Java keystore:

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

客户端证书认证
----------------------

如果需要客户端证书，需要额外的参数设置。
详情请参考Elasticsearch客户端文档。

高级查询示例
==============

包含聚合的查询
----------------

.. note::
   ``query`` 参数仅接受查询主体。聚合（aggs）、排序等搜索级别的
   选项不能指定。只获取文档。

脚本字段
--------------------

.. note::
   Elasticsearch/OpenSearch的脚本字段不包含在 ``_source`` 中，因此无法
   通过 ``source.*`` 前缀访问。要使用脚本字段，请通过 ``hit`` 对象的
   ``hit.getFields()`` 方法访问。

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
