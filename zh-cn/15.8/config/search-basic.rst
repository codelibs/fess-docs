========
搜索功能
========

概述
====

|Fess| 提供强大的全文搜索功能。
本章节介绍搜索功能的详细配置和使用方法。

搜索结果数量显示
================

默认行为
--------

``query.track.total.hits`` 的默认值为 ``10000``\ 。
因此，当搜索结果超过 10,000 条时，搜索结果页面会显示"约 10,000 条以上"。
这是 OpenSearch 将统计精确总命中数的上限限制为 ``query.track.total.hits`` 的值，以降低大规模搜索对性能影响的默认配置。

搜索示例

|image0|

.. |image0| image:: ../../../resources/images/zh-cn/15.8/config/search-result.png

显示准确命中数量
----------------

如需显示更大数量范围内的准确命中数量，请在 ``fess_config.properties`` 中修改 ``query.track.total.hits`` 的值。

::

    query.track.total.hits=100000

上述示例可获取最多 100,000 条的准确命中数量。
显示"约 N 条以上"的阈值也会随此配置值联动变化。
但设置较大的值可能会影响性能。

.. warning::
   值过大可能会降低搜索性能。
   请根据实际使用情况设置适当的值。

搜索选项
========

基本搜索
--------

在 |Fess| 中，只需在搜索框中输入关键词即可执行全文搜索。
输入多个关键词时，将执行 AND 搜索。

::

    搜索 引擎

上述示例将搜索同时包含"搜索"和"引擎"的文档。

OR 搜索
-------

要执行 OR 搜索，请在关键词之间插入 ``OR``\ 。

::

    搜索 OR 引擎

NOT 搜索
--------

要排除特定关键词，请在关键词前添加 ``-`` (减号)。

::

    搜索 -引擎

短语搜索
--------

要搜索完全匹配的短语，请用双引号括起来。

::

    "搜索引擎"

字段指定搜索
------------

可以指定特定字段进行搜索。

::

    title:搜索引擎
    url:https://fess.codelibs.org/

主要字段：

- ``title``: 文档标题
- ``content``: 文档正文
- ``url``: 文档 URL
- ``filetype``: 文件类型（例：pdf, html, doc）
- ``label``: 标签（分类）
- ``mimetype``: MIME 类型（例：text/html, application/pdf）
- ``filename``: 文件名
- ``host``: 主机名
- ``site``: 站点（主机名与路径的组合）
- ``lang``: 语言

可搜索的字段可在 ``fess_config.properties`` 的 ``query.additional.search.fields`` 中追加。

通配符搜索
----------

可以使用通配符进行搜索。

- ``*``: 0个或多个任意字符
- ``?``: 任意单个字符

::

    搜索*
    搜索?擎

模糊搜索
--------

可以使用模糊搜索处理拼写错误或表记差异。
默认情况下，对4个字符以上的关键词，在正常搜索的基础上会额外执行模糊搜索查询。

::

    搜索引擎~

可在 ``~`` 后指定数值来指定编辑距离。

搜索结果排序
============

搜索结果默认按相关度排序。
可在管理页面配置或 API 参数中指定以下排序方式。

- 相关度排序（``score``，默认）
- 更新时间排序（``last_modified``）
- 创建时间排序（``created``）
- 文件大小排序（``content_length``）
- 文件名排序（``filename``）
- 点击数排序（``click_count``）
- 收藏数排序（``favorite_count``）

可排序的字段可在 ``fess_config.properties`` 的 ``query.additional.sort.fields`` 中追加。

分面搜索
========

使用分面搜索可以按类别筛选搜索结果。
默认情况下，标签（label）字段被设置为分面。

点击搜索页面左侧显示的分面可以筛选搜索结果。

搜索结果高亮显示
================

搜索关键词会在搜索结果的标题和摘要部分高亮显示。
可在 ``fess_config.properties`` 中自定义高亮配置。

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

- ``query.highlight.tag.pre`` / ``query.highlight.tag.post``: 包裹高亮部分的标签（默认：``<strong>`` / ``</strong>``）
- ``query.highlight.fragment.size``: 高亮片段（Fragment）的字符数（默认：``60``）
- ``query.highlight.number.of.fragments``: 显示的最大片段数（默认：``2``）

作为摘要（Snippet）高亮的目标字段，可通过 ``query.highlight.content.description.fields``\ （默认：``hl_content,digest``）指定。

建议功能
========

在搜索框中输入字符时会显示建议（输入补全）。
建议基于过去的搜索关键词和热门搜索关键词生成。

可在管理页面的"常规"设置中启用/禁用建议功能。

搜索日志
========

|Fess| 记录所有搜索查询和点击日志。
这些日志可用于以下目的。

- 搜索质量分析与改进
- 用户行为分析
- 了解热门搜索关键词
- 识别搜索结果为0的关键词

搜索日志和点击日志分别保存在 OpenSearch 中以 ``fess_log`` 为前缀的索引中
（搜索查询保存在 ``fess_log.search_log`` 索引，点击日志保存在 ``fess_log.click_log`` 索引）。
这些日志可使用 OpenSearch Dashboards 进行可视化和分析。
|Fess| 内置了可视化用的仪表板定义文件，详情请参阅 :doc:`admin-opensearch-dashboards`。

性能调优
========

搜索超时配置
------------

可以配置搜索超时时间。默认为10秒。

::

    query.timeout=10000

搜索查询最大字符数
------------------

为了安全和性能，可以限制搜索查询的最大字符数。

::

    query.max.length=1000

缓存的使用
----------

|Fess| 本身不具备缓存搜索结果（搜索响应）的功能。
但是，后端的 OpenSearch 在引擎层面提供了分片请求缓存和查询缓存，有助于缩短相同条件搜索的响应时间。
由于这些是 OpenSearch 侧的功能，如有需要请在 OpenSearch 的配置中进行调整。

故障排除
========

搜索结果未显示
--------------

1. 请确认索引是否正确创建。
2. 请确认爬取是否正常完成。
3. 请确认目标文档是否因基于角色/权限的搜索过滤而对当前用户（包括访客）不可见。
4. 请确认 OpenSearch 是否正常运行。

搜索速度慢
----------

1. 请确认 OpenSearch 的堆内存大小。
2. 请优化索引的分片数和副本数。
3. 请确认搜索查询的复杂度。
4. 请确认硬件资源（CPU、内存、磁盘I/O）。

显示不相关结果
--------------

1. 请调整提升设置（``query.boost.title``, ``query.boost.content``\ 等）。
2. 请重新评估模糊搜索配置。
3. 请确认 Analyzer 配置。
4. 如有需要，请咨询商业支持。
5. 您还可以通过使用 Rank Fusion 来提高搜索精度。详情请参阅 :doc:`rank-fusion`。
