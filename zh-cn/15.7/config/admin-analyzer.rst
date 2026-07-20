==================
Analyzer 的设置
==================

关于 Analyzer
==============

在创建用于搜索的索引时,需要对文档进行分词以作为索引注册。
|Fess| 将文档分解为单词的功能注册为 Analyzer。
Analyzer 由 CharFilter、Tokenizer 和 TokenFilter 组成。

基本上,小于 Analyzer 分词单位的内容,即使进行搜索也不会命中。
例如,考虑"住在东京都"这句话。
假设这句话被 Analyzer 分割为"住"、"在"、"东京都"。
这种情况下,用"东京都"进行搜索会命中。
但是,用"京都"进行搜索不会命中。

|Fess| 为每种语言准备了专用的 Analyzer。
索引中字段名的后缀(例如: ``content_ja`` 、 ``content_en`` )决定了自动切换应用哪种语言的 Analyzer。

Analyzer 的定义文件
====================

Analyzer 没有专用的管理界面,需要直接编辑配置文件进行修改。
相关文件存放在 ``app/WEB-INF/classes/fess_indices/`` 目录下。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 文件
     - 内容
   * - ``fess_indices/fess.json``
     - 文档索引的设置。包含 CharFilter、Tokenizer、TokenFilter 和 Analyzer 的定义。
   * - ``fess_indices/fess/doc.json``
     - 文档索引的映射。按 ``*_ja`` 和 ``*_en`` 等字段名模式分别指定应用的 Analyzer。
   * - ``fess_indices/fess/<语言>/``
     - 各语言的词典文件(例如: ``ja/kuromoji.txt`` 、 ``ko/nori.txt`` 、 ``en/protwords.txt`` 、 ``en/stemmer_override.txt`` 、各语言的 ``stopwords.txt`` )。
   * - ``fess_indices/fess/mapping.txt`` 、 ``fess_indices/fess/synonym.txt``
     - 所有语言共享的字符映射词典和同义词词典。

Analyzer 本身的定义(Tokenizer 和 TokenFilter 的组合)在 ``fess.json`` 中进行,而哪个字段使用哪个 Analyzer 则在 ``fess/doc.json`` 中指定。

.. note::
   使用 Amazon OpenSearch Service 等托管服务时,会优先使用与搜索引擎类型对应的配置文件,例如 ``fess_indices/_aws/fess.json`` 或 ``fess_indices/_cloud/fess.json`` 。

Analyzer 的注册
================

Analyzer 的设置在 |Fess| 启动时,如果搜索用索引不存在,则会基于上述配置文件创建索引并进行注册。
索引以带时间戳的名称(例如: ``fess.20240101120000000`` )创建,并分配 ``fess.search`` 和 ``fess.update`` 别名。

配置文件中的 ``${fess.dictionary.path}`` 等占位符在索引创建时会被替换为实际值。
词典文件的存放路径可通过系统属性 ``fess.dictionary.path`` 进行更改。

如果已存在索引,则会复用已定义的设置。
因此,修改 Analyzer 的定义后,需要重新创建索引才能使更改生效。

通过词典进行调整
================

Analyzer 所引用的词典可以通过管理界面进行编辑。

* :doc:`../admin/kuromoji-guide` - 日语形态素分析的用户词典
* :doc:`../admin/synonym-guide` - 同义词词典
* :doc:`../admin/mapping-guide` - 字符映射
* :doc:`../admin/stopwords-guide` - 停用词
* :doc:`../admin/protwords-guide` - 保护词
* :doc:`../admin/stemmeroverride-guide` - 词干提取覆盖

Analyzer 的构成方法请参考 OpenSearch 的 Analyzer 文档。

注意事项
========

Analyzer 的设置对搜索有很大影响。
如需变更 Analyzer,请在理解 Lucene 的 Analyzer 工作原理后进行,或咨询商业支持。
