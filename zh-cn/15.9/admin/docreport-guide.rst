========
文档报告
========

概述
====

文档报告是有助于整理已爬取的文件服务器等的管理页面。它会列出内容相同的文档和长期未更新的文档，并且各列表都可以下载为 CSV。

要打开该页面，请点击左侧菜单中的 [系统信息 > 文档报告]。查看需要 ``admin-docreport`` 或 ``admin-docreport-view`` 角色。该页面只进行显示和下载，不会修改任何文档。

两个选项卡都可以通过“URL 前缀”（例如 ``smb://server/share/`` ）缩小范围。

重复文档
========

将内容相同或几乎相同的文档分组，按文档数量从多到少显示。分组使用在编入索引时计算的内容签名（ ``content_minhash_bits``\ ，与折叠重复搜索结果所用的相同），因此无需重新索引。内容中没有词语的文档（如空文件）不在对象范围内。

页面最多显示 ``docreport.duplicate.group.size`` （默认值：100）个组，每个组最多显示 ``docreport.duplicate.docs.size`` （默认值：10）个文档。可以通过 [下载 CSV] 获取所有组。即使索引很大，CSV 也会读取所有组，并输出 ``group, groupSize, url, title, filename, contentLength, lastModified, owner, lastModifier, clickCount, docId`` 列。

.. note::

   在不保存内容签名的索引（ ``cloud``\ 、\ ``aws`` 用的映射）中，无法使用重复文档报告。

休眠文档
========

按从旧到新的顺序显示最后修改时间早于指定天数（“未更新天数”，默认值为 ``docreport.dormant.days`` 的 365）的文档。没有最后修改时间的文档不会显示。启用“从未在搜索结果中被打开”后，会排除曾从搜索结果中被点击过的文档。

页面显示符合条件的文档数量、合计大小和文档列表。列表的翻页有上限（ ``indexer.max.result.window.size`` ），超出该上限的文档请通过 [下载 CSV] 获取。

设置
====

可以通过 ``fess_config.properties`` 中的以下设置调整其行为。

.. list-table::
   :header-rows: 1
   :widths: 40 45 15

   * - 属性
     - 说明
     - 默认值
   * - ``docreport.duplicate.group.size``
     - 页面显示的重复组最大数量
     - ``100``
   * - ``docreport.duplicate.docs.size``
     - 页面中每个组列出的文档最大数量
     - ``10``
   * - ``docreport.duplicate.export.page.size``
     - 下载 CSV 时每次请求读取的内容签名数量
     - ``10000``
   * - ``docreport.dormant.days``
     - 视为休眠文档的、距最后修改的默认天数
     - ``365``
