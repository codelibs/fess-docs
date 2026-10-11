==================================
Wikipedia连接器
==================================

概述
====

Wikipedia连接器提供读取Wikipedia转储文件并将其页面注册到
|Fess| 索引的功能。
它适用于Wikipedia、其他Wikimedia项目以及任何MediaWiki站点的转储文件。

此功能需要 ``fess-ds-wikipedia`` 插件。

支持的转储
==========

转储格式通过 ``source`` 参数选择。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - 说明
   * - ``cirrus``
     - CirrusSearch索引转储。Wikimedia在
       ``https://dumps.wikimedia.org/other/cirrus_search_index/`` 为各个wiki发布。它包含MediaWiki自身展开模板后渲染的文本，
       因此wikitext标记不会混入索引。对于Wikipedia和其他Wikimedia的wiki，推荐使用此格式
   * - ``xml``
     - MediaWiki XML导出（``*-pages-articles.xml.bz2``，或任意MediaWiki的 ``Special:Export`` 或 ``dumpBackup.php`` 的输出）。
       包含wikitext，由连接器转换为纯文本（参见“XML转储的纯文本转换”）
   * - ``auto``
     - 默认值。包含 ``cirrus_search_index`` 或以 ``.json.bz2``、``.json`` 结尾的位置按 ``cirrus`` 读取，其他位置按 ``xml`` 读取

转储的压缩格式（bzip2、gzip等）会根据内容自动识别，也可以读取未压缩的文件。

前提条件
========

1. 需要安装插件
2. 必须能够通过HTTP(S)的URL或 |Fess| 服务器上的路径访问转储文件
3. 需要爬取的时间。大型Wikipedia的转储有数GB。请先指定 ``limit`` 来试用配置

插件安装
--------

从管理界面的「系统」→「插件」进行安装，或执行 ``bin/fess-setup install plugin fess-ds-wikipedia`` 后
重启 |Fess|。
详情请参阅 :doc:`../../admin/plugin-guide`。

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
     - Japanese Wikipedia
   * - 处理器名称
     - WikipediaDataStore
   * - 启用
     - 开

参数设置
--------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

参数列表
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``url``
     - 否
     - 转储的位置。HTTP(S)的URL、``file:`` 的URL或本地路径。默认值是英文版Wikipedia的转储
       （``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``），因此请务必显式指定。
       ``source=cirrus`` 时可以指定的形式，参见“CirrusSearch转储”
   * - ``source``
     - 否
     - ``auto``、``cirrus``、``xml`` 之一（默认: ``auto``）
   * - ``limit``
     - 否
     - 处理到该页数后结束。``0`` 表示不限制（默认: ``0``）。用于以少量页面试用配置
   * - ``user_agent``
     - 否
     - 下载转储时发送的User-Agent请求头。未指定时使用 |Fess| 爬虫的User-Agent名称
   * - ``max_digest_length``
     - 否
     - ``digest`` 的最大字符数（默认: ``100``）
   * - ``total_entity_size_limit``
     - 否
     - XML解析器处理的实体总大小的上限（字节，默认: ``100000000``）。仅适用于 ``source=xml``
   * - ``text_extractor``
     - 否
     - 将XML转储的wikitext转换为纯文本的方式。``sweble`` （默认）或 ``regex``。参见“XML转储的纯文本转换”
   * - ``drop_templates``
     - 否
     - 要从XML转储的 ``content`` 中去除文本的模板名称，以逗号分隔。``*`` 表示去除所有模板
   * - ``keep_templates``
     - 否
     - 即使匹配 ``drop_templates`` 也保留文本的模板名称，以逗号分隔
   * - ``drop_captions``
     - 否
     - 从XML转储的 ``content`` 中去除图片和图库的说明文字（默认: ``false``）

CirrusSearch转储
~~~~~~~~~~~~~~~~

CirrusSearch转储以带编号的分块形式发布，例如 ``jawiki_content-20261004-00000.json.bz2``。
当 ``source=cirrus`` 时，``url`` 可以指定以逗号分隔的列表，每个元素可以是:

- 单个文件（HTTP(S)的URL或本地路径）
- 本地目录: 按名称顺序读取目录中名称以 ``.json.bz2`` 或 ``.json`` 结尾的所有文件
- 以 ``/`` 结尾的HTTP(S)的URL: 获取目录列表，并按名称顺序读取名称以 ``.json.bz2`` 或 ``.json`` 结尾的所有文件

例如，要读取日文版Wikipedia内容索引的所有分块，可以这样指定:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimedia的服务器会删除旧日期的转储。配置爬取之前，
   请先在 ``https://dumps.wikimedia.org/other/cirrus_search_index/`` 的列表中确认存在的日期。

脚本设置
--------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

可用字段
~~~~~~~~

脚本中可以引用以下值。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``id``
     - 页面ID
   * - ``title``
     - 页面标题
   * - ``encodedTitle``
     - MediaWiki页面URL中使用的形式的标题（空格变为 ``_``，其他字符进行百分号编码）
   * - ``content``
     - 页面的纯文本
   * - ``digest``
     - 截取为 ``max_digest_length`` 个字符的 ``content``
   * - ``contentLength``
     - ``content`` 的长度
   * - ``wikitext``
     - 页面的wikitext（转储中包含时）
   * - ``format``、``model``
     - 页面的格式和内容模型
   * - ``timestamp``
     - 页面的时间戳
   * - ``ns``
     - 命名空间编号
   * - ``categories``、``links``
     - 页面的分类和链接到的页面
   * - ``redirect``、``redirectTitle``
     - 页面是否为重定向及其目标
   * - ``stub``、``disambiguation``
     - 页面是否为小作品，以及是否为消歧义页面
   * - ``lang``、``host``、``site``、``url``
     - 由转储的位置推导得出。参见“由转储位置推导的值”

当 ``source=cirrus`` 时，还可以使用以下值:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``openingText``
     - 页面的开头文本
   * - ``headings``
     - 标题（小节标题）
   * - ``externalLinks``
     - 外部链接
   * - ``templates``
     - 页面使用的模板
   * - ``redirects``
     - 重定向到此页面的标题
   * - ``auxiliaryText``
     - 图片说明等辅助文本
   * - ``weightedTags``
     - 带权重的标签
   * - ``wikibaseItem``
     - Wikidata条目ID
   * - ``incomingLinks``
     - 入链数量
   * - ``popularityScore``
     - 热门度得分
   * - ``revisionId``
     - 修订版本ID

由转储位置推导的值
------------------

``lang``、``host``、``site`` 和 ``url`` 由转储的名称推导得出。``jawiki-latest-pages-articles.xml.bz2`` 或
``index_name=jawiki_content`` 之类的名称会得到 ``lang`` 为 ``ja``，``host`` 和 ``site`` 为 ``ja.wikipedia.org``，
``url`` 为 ``https://ja.wikipedia.org/wiki/<编码后的标题>``。
名称中必须包含语言代码，其后紧跟 ``wiki``，再其后是 ``-``、``_`` 或 ``.`` 之一。
Wikiquote（``jawikiquote-...``）等姐妹项目因为错误的主机会产生失效链接，所以有意不做推导。

.. warning::

   转储名称不匹配时，不会设置 ``host``、``site`` 和 ``url``，``url`` 会保留 ``url`` 参数的值，即转储的位置。
   如果脚本直接使用 ``url``，所有页面都会得到相同的URL，整个爬取在索引中只会变成一个文档，而且没有任何错误提示。
   对于改过名称的转储或其他Wikimedia项目，请像上面的示例那样在脚本中拼接URL。例如:
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``

XML转储的纯文本转换
-------------------

当 ``source=xml`` 时，会使用Sweble wikitext解析器将wikitext转换为纯文本。命名空间名称从导出的 ``<siteinfo>`` 中读取，
因此无论哪种语言（``[[ファイル:...]]``、``[[Kategorie:...]]``），以及具有自有命名空间名称的wiki，都能识别图片和分类的声明。
Sweble无法转换的页面会用正则表达式转换。

``text_extractor=regex`` 对所有页面都使用正则表达式转换。速度快数倍，但嵌套的模板、表格和跨多行的标记会残留在文本中。

默认情况下，所有模板参数的文本（不含参数名）以及所有图片和图库的说明文字都会保留在 ``content`` 中，因此这些文本也可以被搜索到。
可以通过 ``drop_templates``、``keep_templates`` 和 ``drop_captions`` 进行过滤:

::

    # 去除这些模板的文本（嵌套时也一样。"*" 表示去除所有模板）
    drop_templates=Cite web,Cite news,Use dmy dates
    # 即使匹配 drop_templates 也保留这些模板
    # （同时指定 drop_templates=* 和 keep_templates=Note,Warning 时，只保留这两个）
    keep_templates=
    # 去除图片和图库的说明文字
    drop_captions=false

模板名称按MediaWiki解析的方式进行匹配: 首字母不区分大小写，``_`` 等同于空格，``Template:`` 前缀可以省略。
模板不会被展开，因此保留的模板提供的是其参数的文本，而不是MediaWiki渲染的内容。
CirrusSearch转储已经包含MediaWiki渲染的文本，因此这些参数不适用于 ``source=cirrus``。

使用示例
========

从CirrusSearch转储爬取日文版Wikipedia
-------------------------------------

参数:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

脚本:

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

从XML转储爬取日文版Wikipedia（去除引用模板）
--------------------------------------------

参数:

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

脚本与“脚本设置”相同。

爬取其他Wikimedia项目（Wikiquote）
----------------------------------

转储名称 ``jawikiquote-...`` 无法推导出 ``host`` 和 ``url``，因此请在脚本中拼接。

脚本:

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

故障排除
========

只有一个文档被建立索引
----------------------

参见“由转储位置推导的值”。请确认脚本为每个页面都设置了 ``url``。

爬取耗时过长
------------

1. 先指定 ``limit`` 来确认配置
2. 使用 ``source=cirrus``。对于XML转储，使用 ``text_extractor=regex``
3. 将转储放置在 |Fess| 服务器上，并指定本地路径

内容中残留wikitext标记
----------------------

请使用CirrusSearch转储（``source=cirrus``）。对于 ``source=xml``，``text_extractor=regex`` 会让嵌套的模板、表格和多行标记残留在文本中，因此请使用 ``sweble`` （默认）。

无法读取转储
------------

1. 确认URL或路径正确（CirrusSearch转储的日期可能已从服务器上删除）
2. 对于目录的URL，确认以 ``/`` 结尾，且其中的文件以 ``.json.bz2`` 或 ``.json`` 结尾
3. 在日志中查看确切的错误

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../../admin/plugin-guide` - 插件管理指南
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
