====
字典
====

概述
====

本节介绍字典的相关配置。

请在理解各字典相关规范后再进行字典更改。
如果字典更改失败,可能无法访问索引。

列表
====

要打开下图所示的可管理字典列表页面,请单击左侧菜单中的[系统 > 字典]。


|image0|


各词典的作用范围与生效时机
==========================

每个词典作用的字段和生效的时机都不同。
如果编辑了词典但搜索结果没有变化，请先查看下表。

.. list-table::
   :header-rows: 1
   :widths: 22 26 28 24

   * - 词典
     - 文件
     - 作用的字段
     - 生效时机
   * - Kuromoji
     - ``ja/kuromoji.txt``
     - 仅 ``content_ja`` 等 ``_ja`` 字段
     - 索引时（需要重新爬取）
   * - 同义词
     - ``synonym.txt``
     - ``content`` 和 ``title``
     - 搜索时（无需重新爬取）
   * - 映射（各语言通用）
     - ``mapping.txt``
     - ``content`` 和 ``title``
     - 索引时（需要重新爬取）
   * - 映射（按语言）
     - ``ja/mapping.txt``
     - 仅 ``content_ja`` 等 ``_ja`` 字段
     - 索引时（需要重新爬取）
   * - Protwords
     - ``en/protwords.txt``
     - ``content`` 和 ``title``
     - 索引时与搜索时
   * - 停用词
     - ``en/stopwords.txt``
     - ``content`` 和 ``title``
     - 索引时与搜索时
   * - Stemmer 覆盖
     - ``en/stemmer_override.txt``
     - ``content`` 和 ``title``
     - 索引时与搜索时

.. note::

   分析器是在打开索引时构建的，因此更新词典文件后
   **在索引 close / open 之前不会生效**\ 。
   而且在索引时生效的词典不会追溯应用到已经索引的文档，这些文档需要重新爬取。
   使更改生效的步骤请参见 :ref:`dict-apply-changes`\ 。

.. warning::

   对 ``content`` 字段（大多数搜索由该字段作答）生效的字符替换词典是\ **根目录的**
   ``mapping.txt`` ，而不是 ``ja/mapping.txt`` 。二者同名为映射，但是不同的文件。

.. _dict-apply-changes:

使词典的更改生效
----------------

仅保存词典，无论等待多久，搜索结果都不会改变。OpenSearch 的 configsync 插件大约每分钟将已保存的
词典写入词典文件，但分析器只在打开索引时读取词典，因此已经打开的索引会继续使用旧的词典。
编辑词典后，请重新加载文档索引：

1. 打开左侧菜单中的 [系统信息 > 维护]。
2. 在“重新加载文档索引”中单击 [重新加载] 按钮。

该按钮会先将已保存的词典写入文件，然后关闭（close）并重新打开（open） ``fess.update`` 别名所指向的
索引，因此无需等待定期写入。同义词这类在搜索时生效的词典，会在索引重新打开时生效。对于在索引时
生效的词典，还需要重新爬取相关文档。

.. warning::

   在索引关闭期间，以及打开后分片重新分配完成之前，无法搜索该索引：搜索会出错或返回 0 条结果。
   索引越大，所需时间越长，请在访问较少的时段执行。

如果不使用管理界面、而要从脚本等执行，请向 OpenSearch 发送相同的操作::

    curl -X POST "localhost:9200/_configsync/flush"
    curl -X POST "localhost:9200/fess.update/_close"
    curl -X POST "localhost:9200/fess.update/_open"

``_configsync/flush`` 会立即将已保存的词典写入文件。如果省略此步骤，请在保存词典后至少等待 1 分钟，
再关闭索引。

Kuromoji 用户词典与搜索结果
----------------------------

``content`` 字段使用 standard 分词器和 ``cjk_bigram`` 进行分析，因此不受 Kuromoji
形态素切分结果的影响。将日语复合词注册到 Kuromoji 用户词典后重新爬取，对 ``content``
的搜索结果仍然不会改变。注册的效果体现在 ``content_ja`` 上，该字段会根据请求的语言
加入到查询条件中。

Kuromoji
========

管理日语形态素分析用的词典。
ja/kuromoji.txt 是日语形态素分析用词典。

同义词
=====

管理同义词词典。
synonym.txt 是通用于所有语言的同义词词典文件。

映射
========

管理字符替换词典。
mapping.txt 是通用于所有语言或各语言的单词替换词典文件。

Protwords
=========

管理保护单词词典。
protwords.txt 按各语言配置,是用于排除词干提取等的单词列表文件。

停用词
===========

管理停用词词典。
stopwords.txt 按各语言配置,是在创建索引时排除的单词列表文件。

Stemmer覆盖
============

管理 Stemmer 覆盖词典。
stemmer_override.txt 按各语言配置,是用于覆盖词干提取处理的单词替换词典文件。


.. |image0| image:: ../../../resources/images/en/15.9/admin/dict-1.png
            :height: 940px
