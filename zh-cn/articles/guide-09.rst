==============================
搜索日语、英语、中文混合的文档
==============================

前言
====

当日语会议纪要、英语技术规格书和中文市场报告并存于同一台文件服务器或同一个内部网站上时，就会出现这样的声音：“英语文档能搜到，日语的活用形却匹配不上”“只想搜索中文文档”“想用日语词语找到用英语写的资料”。

Fess 无需特别配置即可搜索任何语言的文档。
但是，如果不清楚哪种语言的分析在何处生效就往词典里添加条目，搜索结果并不会改变。
本文以配置文件中的实际值为依据，说明 Fess 15.9 如何为多语言文档建立索引以及如何进行搜索。
在此基础上，让您能够完成以下操作：

- 确认每个文档被判定的语言，并用 ``lang:`` 按语言筛选搜索
- 通过 ``query.default.languages`` 等设置，决定搜索时使用哪种语言的分析
- 根据词典（同义词、Kuromoji、停用词等）生效的字段来编辑词典，并使更改生效
- 通过搜索结果和 ``_analyze`` API 确认更改已经生效

利用搜索日志推进改进的方法本身，请参见 :doc:`guide-08`。

索引的机制：通用字段与语言专用字段
==================================

在 Fess 的索引中，正文和标题以两种形式存储。
其定义位于 Fess 自带的 ``fess_indices/fess.json`` （分析器）和 ``fess_indices/fess/doc.json`` （映射）中。

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - 字段
     - 分析器
     - 分析内容
   * - ``content``、``title``、``important_content``
     - ``standard_analyzer`` （搜索时为 ``standard_search_analyzer``）
     - 所有文档通用。汉字、平假名、片假名和韩文按每 2 个字符切分（bi-gram），并进行英语停用词去除和词干提取（stemming）。同义词仅在搜索时展开
   * - ``content_ja``、``title_ja`` 等
     - ``japanese_analyzer``
     - 基于 Kuromoji 的形态素分析。将动词等还原为基本形，并去除助词、助动词和符号
   * - ``content_en``、``title_en`` 等
     - ``english_analyzer``
     - 英语停用词去除和词干提取
   * - ``content_zh-cn``、``title_zh-cn`` 等
     - ``simplified_chinese_analyzer``
     - 使用中文分词器切分为词语
   * - ``content_zh-tw``、``title_zh-tw`` 等
     - ``traditional_chinese_analyzer``
     - 先将繁体字转换为简体字，再用与简体字相同的分词器切分

所有文档都有通用字段。
语言专用字段只有在文档的语言确定时才会创建。
在索引处理中，会把语言代码写入 ``lang`` 字段，并把 ``content``、``important_content``、``title`` （``indexer.language.fields``）的值复制到 ``content_ja`` 这样的 ``<字段>_<语言>`` 字段中。
一个文档只会被赋予一种语言。

文档语言的确定方式
------------------

``lang`` 按以下顺序确定。

1. 对于 Web 爬取的 HTML，使用 ``<html lang="...">`` 的值（``crawler.document.html.lang.xpath=//HTML/@lang``）。在爬取配置的「配置参数」中写入 ``field.xpath.default.lang=<XPath>``，即可仅针对该配置更改读取值的位置
2. 未能通过第 1 步确定语言的文档，会根据正文自动判定。按 ``content``、``important_content``、``title`` 的顺序，查看开头 1000 个字符（``indexer.language.detect.length``）。文件爬取时，仅根据提取出的正文进行判定
3. 如果判定结果是 ``supported.languages`` 中没有的语言，或者无法判定，则不会设置 ``lang``，也不会创建语言专用字段

``ja-JP`` 或 ``zh_CN`` 这样的值，会统一为小写加连字符的形式（``ja``、``zh-cn``）后保存。

数据存储的文档在建立索引时也会经过相同的自动判定。
如果在脚本中为 ``lang`` 设置 ``supported.languages`` 中已有的语言（如 ``ja``），该值会优先于自动判定。

搜索的机制：搜索哪种语言的字段
==============================

搜索词始终会针对通用字段进行搜索。
此外，对于每次搜索时确定的每种“搜索语言”，相应的语言专用字段都会加入搜索条件。
各字段的条件以 OR（``bool`` 查询的 ``should``）连接，因此只要匹配其中任意一个字段，文档就会出现在搜索结果中。

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - 字段
     - 配置键
     - 默认值
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<搜索语言>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<搜索语言>``
     - ``query.boost.content.lang``
     - ``0.1``

搜索语言取自以下各项中第一个有值的项。

1. ``fess_config.properties`` 中的 ``query.default.languages`` （默认为空）。有值时，其他所有指定都会被忽略
2. 请求的 ``lang`` 参数。即在搜索页面的 [选项] >「首选语言」或高级搜索的「首选语言」中选择的语言，或者 ``/api/v2/search`` 的 ``lang``
3. 浏览器发送的 ``Accept-Language`` 请求头中的语言

例如，在日语浏览器中搜索“会議”（会议）时，搜索语言为 ``ja``，除 ``content`` 之外还会搜索 ``content_ja``。
英语文档没有 ``content_ja``，因此英语文档只会通过通用字段的 bi-gram 匹配。
反过来，日语文档如果在 ``title_ja``、``content_ja`` 中也匹配，得分就会相应提高，更容易排在前面。
由于 Kuromoji 会把活用形还原为基本形，用“走った”（跑了）搜索时，写有“走る”（跑）的日语文档也会在 ``content_ja`` 中匹配。

因此，「首选语言」是把该语言的文档排到前面的指定，而不是排除其他语言文档的筛选。

按语言筛选：``lang:`` 搜索
==========================

要按语言筛选，请在搜索时指定 ``lang`` 字段。
``lang`` 是可搜索的关键词（keyword）类型字段，无需为每种语言创建标签。

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

最后一个示例在排除被判定为日语的文档后搜索“会議”。
通过 API 时，可以在 ``q`` 中写入相同的表达式，或者加上 ``fields.lang=en`` （会添加 ``lang:"en"`` 条件）。

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

没有 ``lang`` 的文档（无法判定语言的文档）不会匹配任何 ``lang:`` 条件。

确认语言判定结果
----------------

在更改词典或设置之前，先确认文档被赋予了哪种语言。

1. 在搜索页面分别搜索 ``lang:ja``、``lang:en``、``lang:zh-cn``、``lang:zh-tw``，比较结果数量。使用 API 时，可以通过 ``response.record_count`` 查看数量

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. 对于单个文档，在管理页面的 [系统信息] > [搜索] 中通过 URL 等找到并打开它，即可在 ``lang`` 栏中确认其值

判定结果与预期不符时，请确认以下几点。

- HTML 的 ``<html lang>`` 优先于自动判定。如果网站模板在日语页面上也输出 ``lang="en"``，这些页面就会被当作英语处理
- 像 ``<html lang="zh">`` 这样不带地区的中文会成为 ``zh``。``zh`` 没有使用中文分析器的语言专用字段，因此中文分析只有通用字段的 bi-gram
- 汉字多、假名少的日语短文档，有时会被判定为 ``zh-cn`` 等

还有将所有 HTML 或所有文件视为同一种语言的设置。
如果为 ``crawler.document.html.default.lang`` 和 ``crawler.document.file.default.lang`` 设置了值，就不会使用 ``<html lang>`` 和自动判定，Fess 的全部爬取都会固定为该语言。
在文档语言混杂的环境中，请保持为空。

确定搜索语言：``query.default.languages``
=========================================

默认情况下，搜索语言会随每个用户的浏览器语言而变化。
例如使用英语浏览器的员工搜索日语文档时不会使用 ``content_ja``，结果的排序因用户而异。
如果想避免这种情况，可以用 ``query.default.languages`` 固定搜索语言。

::

    query.default.languages=ja,en,zh-cn,zh-tw

在此示例中，无论谁用哪种语言搜索，4 个语言专用字段都会全部加入搜索条件。
每个文档只有一个属于自身语言的字段，因此任何语言的文档都能在相同条件下受益于语言专用分析。
相应地，通过「首选语言」把特定语言排到前面的操作将不再生效。
如果以日语文档为主，也可以像 ``query.default.languages=ja`` 这样只指定一种语言。

将设置写入 ``fess_config.properties``，然后重启 Fess。
文件位置在 ZIP 版中为 ``app/WEB-INF/classes/fess_config.properties``，在 RPM/DEB 版中为 ``/etc/fess/fess_config.properties``。
使用 Docker 时，将其作为 JVM 选项添加到 ``compose.yaml`` 中 ``fess01`` 的 ``environment``，然后重新创建容器。

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS`` 以空格分隔，因此值中不要包含空格。
重新创建容器后，在 [系统] > [通用] 中修改的设置会随容器内的 ``system.properties`` 一起丢失（:doc:`guide-02`）。

语言专用字段的匹配占多大权重，可以通过 ``query.boost.title.lang`` 和 ``query.boost.content.lang`` 调整。
更改后，请按照下文“确认”中的步骤比较搜索结果的排序。

按语言分别使用词典
==================

词典在 [系统] > [字典] 中编辑。
每个词典生效的字段是固定的，如果没有选择对目标字段生效的词典，搜索结果就不会改变。

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - 词典（文件）
     - 生效的字段
     - 在多语言环境中的用途
   * - 同义词（``synonym.txt``）
     - ``content``、``title`` （仅搜索时）
     - 跨语言的同义替换（“会議”与“meeting”）、写法差异。对语言专用字段无效
   * - Kuromoji（``ja/kuromoji.txt``）
     - 仅 ``_ja`` 字段
     - 让内部用语或产品名称被视为一个日语词
   * - 停用词（``ja/stopwords.txt``）
     - 仅 ``_ja`` 字段
     - 在日语文档中不用于搜索的词
   * - 停用词（``en/stopwords.txt``）
     - ``content``、``title`` 和 ``_en`` 字段
     - 不需要的英语词。由于对通用字段生效，会影响所有语言的文档
   * - Protwords（``en/protwords.txt``）
     - ``content``、``title`` 和 ``_en`` 字段
     - 不希望进行词干提取的英语单词（产品名称等）
   * - 词干覆盖（``en/stemmer_override.txt``）
     - ``content``、``title`` 和 ``_en`` 字段
     - 指定英语词干提取的结果
   * - 映射（``mapping.txt``）
     - ``content``、``title``
     - 字符替换。``ja/mapping.txt`` 是用于 ``_ja`` 字段的另一个文件

没有日语用的保护词（Protwords）词典。
这是因为 ``japanese_analyzer`` 中没有读取保护词的过滤器。
简体中文和繁体中文的字段没有可在管理页面中编辑的用户词典（停用词为 ``zh-cn/stopwords.txt``、``zh-tw/stopwords.txt``）。

跨语言的同义词
--------------

如果想用日语词语找到英语文档，可以把对译词登记为同义词。
在上传文件的格式中，每行列出含义相同的词，用逗号分隔。

::

    会議,ミーティング,meeting
    見積,quotation

同义词在搜索时于通用字段中展开，因此无需重新爬取。
平假名以片假名登记、全角英文数字以半角登记等登记规则，请参见 `同义词词典 <https://fess.codelibs.org/zh-cn/stable/admin/synonym-guide.html>`__。

Kuromoji 用户词典
-----------------

Kuromoji 词典中登记的是词元（token）、切分后的词元、读音（片假名）和词性。
如果想让被 Kuromoji 切得过细的内部用语或产品名称作为一个词处理，就在词元和切分后的词元中写入相同的词。

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

该词典只对 ``_ja`` 字段生效。
通用字段 ``content`` 按 bi-gram 切分，因此即使更改 Kuromoji 词典，``content`` 中的匹配也不会改变。
只有在搜索语言包含 ``ja`` 的搜索中，并且针对被判定为日语的文档，才会体现出效果。

使词典更改生效
--------------

仅保存词典，搜索结果并不会改变。

1. 打开 [系统信息] > [维护]，在「重新加载文档索引」中点击 [重新加载]。由于会关闭并重新打开索引，在此期间搜索会出错或返回 0 条结果。请在使用较少的时段执行
2. 同义词只在搜索时使用，因此重新加载后即已生效
3. 同义词以外的词典（Kuromoji、映射、停用词、Protwords、词干覆盖）也会改变建立索引时的分析。已在索引中的文档仍保持用旧词典分析的状态，因此需要重新爬取相关内容

重新爬取时，如果 [系统] > [通用] 中的「检查上次修改时间」处于启用状态（默认），未更新的文件和页面不会被重新获取。
请暂时禁用后执行爬取，结束后再重新启用。

确认
====

用 ``_analyze`` API 查看词元切分
--------------------------------

要确认词典是否已生效，最可靠的方法是使用 OpenSearch 的 ``_analyze`` API，将同一字符串分别交给通用字段和日语字段的分析器进行比较。
在 :doc:`guide-02` 的 Docker 配置中，可以通过主机的 9200 端口连接 OpenSearch。

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

使用 ``japanese_analyzer`` 时，文本按词语切分，“を”和“た”被去除。
使用 ``standard_analyzer`` 时，则像“全文”“文検”“検索”这样每 2 个字符切分。
在 Kuromoji 词典中登记“東京スカイツリー”并重新加载后，用 ``japanese_analyzer`` 分析该词会返回一个词元。
登记的同义词可以这样确认：用 ``"analyzer":"standard_search_analyzer"`` 分析“会議”，看是否出现由“meeting”生成的词元（词干提取后为 ``meet``）。

通过搜索结果确认
----------------

1. 在搜索页面搜索一个同时出现在日语和英语文档中的词
2. 将 [选项] 中的「首选语言」在「日语」和「英语」之间切换，确认排在前面的文档的语言发生变化。如果设置了 ``query.default.languages``，则确认切换后排序不变
3. 登记对译同义词并重新加载后，确认用 ``lang:en 会議`` 能找到英语文档
4. 更改 Kuromoji 词典并重新爬取后，用登记的词搜索，确认能找到包含该词的日语文档。切分本身是否改变，请用前面的 ``_analyze`` 确认

如果结果没有变化，请将词典表中的“生效的字段”与文档的 ``lang`` 进行对照。
例如，即使向 ``en/stopwords.txt`` 添加 3 个字符以上的日语词，由于在通用字段中会变成每 2 个字符的词元，也不会匹配，因而无效。

总结
====

- 所有文档都可以通过应用 bi-gram 和英语词干提取的通用字段（``content``、``title``）进行搜索
- 判定出的语言 ``lang`` 和语言专用字段（``content_ja`` 等）会追加适合该语言的分析
- 搜索语言按 ``query.default.languages``、请求的 ``lang``、浏览器语言的顺序确定，其作用是把文档排到前面，而不是筛选
- 按语言筛选时，像 ``lang:en`` 这样指定 ``lang`` 字段
- 选择对目标字段生效的词典进行编辑，并通过重新加载文档索引以及必要时重新爬取使其生效

延伸阅读
========

- 想从搜索日志中找出改进点，并用同义词或关键词匹配进行修正：:doc:`guide-08`
- 想一并爬取内部网站和文件服务器：:doc:`guide-04`
- 即使关键词不匹配，也想找到含义相近的文档：:doc:`guide-18`
- 想从业务系统调用搜索 API：:doc:`guide-11`

参考资料
========

- `字典 <https://fess.codelibs.org/zh-cn/stable/admin/dict-guide.html>`__
- `Kuromoji词典 <https://fess.codelibs.org/zh-cn/stable/admin/kuromoji-guide.html>`__
- `同义词词典 <https://fess.codelibs.org/zh-cn/stable/admin/synonym-guide.html>`__
- `停用词词典 <https://fess.codelibs.org/zh-cn/stable/admin/stopwords-guide.html>`__
- `维护 <https://fess.codelibs.org/zh-cn/stable/admin/maintenance-guide.html>`__
- `搜索相关配置（搜索默认语言） <https://fess.codelibs.org/zh-cn/stable/config/search-advanced.html>`__
- `爬虫高级配置 <https://fess.codelibs.org/zh-cn/stable/config/crawler-advanced.html>`__
- `字段指定检索 <https://fess.codelibs.org/zh-cn/stable/user/search-field.html>`__
- `搜索 API <https://fess.codelibs.org/zh-cn/stable/api/api-search.html>`__
