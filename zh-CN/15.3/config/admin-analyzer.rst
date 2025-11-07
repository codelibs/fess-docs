=============
Analyzer 配置
=============

关于 Analyzer
==============

在创建用于搜索的索引时,需要对文档进行分词以作为索引注册。
|Fess| 将文档分解为单词的功能注册为 Analyzer。
Analyzer 由 CharFilter、Tokenizer 和 TokenFilter 组成。

基本上,小于 Analyzer 分词单位的内容,即使进行搜索也不会命中。
例如,考虑"东京都に住む"这句话。
假设这句话被 Analyzer 分割为"东京都"、"に"、"住む"。
这种情况下,用"东京都"进行搜索会命中。
但是,用"京都"进行搜索不会命中。

Analyzer 的配置在 |Fess| 启动时,如果 fess 索引不存在,则会使用 app/WEB-INF/classes/fess_indices/fess.json 创建 fess 索引并注册。
Analyzer 的构成方法请参考 OpenSearch 的 Analyzer 文档。

Analyzer 的配置对搜索有很大影响。
如需变更 Analyzer,请在理解 Lucene 的 Analyzer 工作原理后进行,或咨询商业支持。
