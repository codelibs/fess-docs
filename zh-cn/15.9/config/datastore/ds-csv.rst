==================================
CSV连接器
==================================

概述
====

CSV连接器提供从CSV文件获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-csv`` 插件。

前提条件
========

1. 需要安装插件
2. 需要具有CSV文件的访问权限
3. 需要了解CSV文件的字符编码

插件安装
------------------------

方法1: 直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # 放置
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或者
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products CSV
   * - 处理器名称
     - CsvDataStore
   * - 启用
     - 开

参数设置
----------------

本地文件:

::

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

多个文件:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

.. note::

   在 |Fess| 15.9 中，引号处理和转义处理默认为 **启用** 状态。
   字段内包含分隔符或换行符的CSV（符合RFC 4180规范）无需指定任何参数即可正确解析。
   如需了解如何恢复为以前版本的行为（禁用引号处理）及相关注意事项，
   请参阅后文的「禁用引号与转义处理」。

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``files``
     - 否
     - CSV文件路径（本地路径，可指定多个：逗号分隔）。 ``files`` 和 ``directories`` 至少需要指定其中一个。两者均指定时 ``files`` 优先。指定的文件扩展名必须为 ``.csv`` 或 ``.tsv``，其他扩展名的文件将被跳过。
   * - ``directories``
     - 否
     - 包含CSV文件的目录路径（可指定多个：逗号分隔）。目录内仅处理 ``.csv`` 和 ``.tsv`` 文件。未指定 ``files`` 时使用。
   * - ``file_encoding``
     - 否
     - 字符编码（默认: UTF-8）
   * - ``has_header_line``
     - 否
     - 是否有标题行（默认: false）
   * - ``separator_character``
     - 否
     - 分隔符（默认: 逗号 ``,``）。可指定 ``\t`` 等转义序列（制表符分隔）。
   * - ``quote_character``
     - 否
     - 引号字符（默认: 双引号 ``"``）。引号处理默认为启用状态（参见 ``quote_disabled``）。
   * - ``escape_character``
     - 否
     - 转义字符（默认: 与 ``quote_character`` 相同的字符；按照RFC 4180规范，通过将引号重复两次进行转义）。转义处理是否启用取决于 ``quote_disabled`` 的解析结果（参见 ``escape_disabled``）。

.. note::

   ``files`` 和 ``directories`` 均未指定时将报错（ ``DataStoreException`` ）。
   请至少指定其中一个。

高级参数
~~~~~~~~~~~~~~~~

以下参数用于精细控制CSV的解析行为及索引注册行为：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数
     - 说明
   * - ``quote_disabled``
     - 是否禁用引号处理（默认: false）。默认情况下，符合RFC 4180规范的带引号字段可被正确解析。若要恢复为以前的行为（将引号视为普通字符），请指定 ``true``\ 。
   * - ``escape_disabled``
     - 是否禁用转义处理（默认: 与 ``quote_disabled`` 的解析结果相同）。若明确指定该值，则以指定值为准。
   * - ``delete_old_docs``
     - 爬取完成后，是否删除属于该数据存储配置、且在本次爬取会话中未被重新注册的文档（默认: true）。若在不同时间将多个CSV文件投入同一数据存储配置，请指定 ``false``\ ，否则先前投入的文档将被删除（详情参见后文的故障排除部分）。
   * - ``keep_expires_docs``
     - 通过 ``delete_old_docs`` 进行删除时，是否将有效期（通过 ``time_to_live`` 等设置的expires）尚未到期的文档排除在删除对象之外（默认: true）。设为 ``false``\ 时，即使在有效期内，未被重新注册的文档也会被删除。
   * - ``time_to_live``
     - 文档的有效期设置为注册时刻起的多少分钟后（以分钟为单位。默认: 未设置=无限期）。
   * - ``skip_lines``
     - 跳过的开头行数（默认: 0）
   * - ``ignore_line_patterns``
     - 忽略行的正则表达式模式（例: ``^#.*`` 忽略注释行）
   * - ``ignore_empty_lines``
     - 是否忽略空行（默认: false）
   * - ``ignore_trailing_whitespaces``
     - 是否忽略行尾空白（默认: false）
   * - ``ignore_leading_whitespaces``
     - 是否忽略行首空白（默认: false）
   * - ``null_string``
     - 视为null值的字符串
   * - ``break_string``
     - 替换字段值中换行符的字符串
   * - ``readInterval``
     - 每处理一条记录的等待时间（毫秒）（默认: 0）

脚本设置
--------------

各字段的值通过引用CSV各列的值来构建。CSV的列在脚本中可作为
**无前缀的变量** 直接引用（不加 ``data.`` 等前缀）。

有标题行时（按列名引用）:

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

无标题行时（按列索引引用）:

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

可用字段
~~~~~~~~~~~~~~~~

- ``<列名>`` - 直接使用标题行的列名引用（仅在 ``has_header_line=true`` 且列名非空时有效）
- ``cell<N>`` - 按列索引引用（ ``cell1``、``cell2``\ ……从1开始，无论是否有标题行均可使用）
- ``csvfile`` - 当前处理的CSV文件的完整路径
- ``csvfilename`` - 当前处理的CSV文件名

.. note::

   列名中包含空格、连字符等Groovy标识符非法字符时，无法通过列名引用。
   此时请使用 ``cell<N>`` 方式引用。

CSV格式详情
=============

标准CSV（RFC 4180兼容）
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

.. note::

   如上述 ``"Book, Programming"`` 所示，即使在字段内包含分隔符并使用引号包裹，
   在默认设置（引号处理已启用）下也会被正确解析为单个字段。
   如需恢复为以前的行为（将引号视为普通字符，字段按分隔符分割），
   请参阅后文的「禁用引号与转义处理」。

禁用引号与转义处理
------------------

在 |Fess| 15.9 中，引号处理和转义处理默认为启用状态。默认引号字符为双引号 ``"``，
默认转义字符与引号字符相同（按照RFC 4180规范，通过将引号重复两次进行转义）；
符合RFC 4180规范的标准CSV无需任何参数即可直接解析。

.. warning::

   在引号处理启用的状态下，若CSV文件中存在哪怕一个没有对应闭合引号的 ``"``\ ，
   则从该引号开始之后的整个文件内容（包括后续行）都会被读取为单个字段值，
   此后的行将不再生成文档。由于以前的版本中每行都是独立解析的，
   这种行为可能在升级后才首次显现出来。
   由于 ``delete_old_docs``\ （前文所述）默认为启用状态，这不仅会导致未生成的文档丢失，
   还可能删除之前爬取时已注册的文档。
   升级前请检查CSV文件中是否包含未闭合的引号，或考虑指定 ``quote_disabled=true``
   以恢复为以前的解析方式。

禁用引号处理（恢复为以前的行为）:

::

    # 参数
    quote_disabled=true

指定 ``quote_disabled=true`` 后，转义处理也会同时被禁用
（明确指定 ``escape_disabled=false`` 的情况除外）。

仅禁用转义处理:

::

    # 参数
    escape_disabled=true

更改分隔符
------------------

制表符分隔（TSV）:

::

    # 参数
    separator_character=\t

分号分隔:

::

    # 参数
    separator_character=;

自定义引号
--------------

单引号:

::

    # 参数
    quote_character='

编码
----------------

中文文件（Shift_JIS）:

::

    file_encoding=Shift_JIS

中文文件（EUC-JP）:

::

    file_encoding=EUC-JP

使用示例
========

产品目录CSV
-----------

CSV文件（products.csv）:

::

    product_id,name,description,price,category,in_stock
    1001,笔记本电脑,高性能笔记本电脑,120000,电脑,true
    1002,鼠标,无线鼠标,2500,外设,true
    1003,键盘,机械键盘,8500,外设,false

参数:

::

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

脚本:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " 类别: " + category + " 价格: " + price + "元"
    digest=category
    price=price

库存信息过滤:

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

员工名册CSV
-----------

CSV文件（employees.csv）:

::

    emp_id,name,department,email,phone,position
    E001,张三,销售部,zhang@example.com,010-1234-5678,部长
    E002,李四,开发部,li@example.com,010-2345-6789,经理
    E003,王五,总务部,wang@example.com,010-3456-7890,专员

参数:

::

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

脚本:

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="部门: " + department + "\n职位: " + position + "\n邮箱: " + email + "\n电话: " + phone
    digest=department

无标题行的CSV
-------------

CSV文件（data.csv）:

::

    1,商品A,这是商品A,1000
    2,商品B,这是商品B,2000
    3,商品C,这是商品C,3000

参数:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,

脚本:

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

多CSV文件整合
-------------

参数:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

脚本:

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

制表符分隔（TSV）文件
---------------------

TSV文件（data.tsv）:

::

    id	title	content	category
    1	文章1	这是文章1的内容	新闻
    2	文章2	这是文章2的内容	博客

参数:

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t

脚本:

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

故障排除
========

找不到文件
----------

**症状**: 爬取执行但文件未被处理，日志中出现 ``is not found``

**确认事项**:

1. 确认文件路径是否正确（推荐使用绝对路径）
2. 确认文件是否存在
3. 确认文件扩展名是否为 ``.csv`` 或 ``.tsv``\ （其他扩展名将被跳过）
4. 确认是否有文件读取权限
5. 确认 |Fess| 运行用户是否可以访问

出现乱码
--------

**症状**: 中文无法正确显示

**解决方法**:

指定正确的字符编码:

::

    # UTF-8
    file_encoding=UTF-8

    # Shift_JIS
    file_encoding=Shift_JIS

    # EUC-JP
    file_encoding=EUC-JP

    # Windows标准（CP932）
    file_encoding=Windows-31J

确认文件编码:

::

    file -i data.csv
    # 或者
    nkf -g data.csv

列无法正确识别
--------------

**症状**: 列分隔符无法正确识别，或带引号的字段被拆分

**确认事项**:

1. 确认分隔符是否正确:

   ::

       # 逗号
       separator_character=,

       # 制表符
       separator_character=\t

       # 分号
       separator_character=;

2. 带引号字段（字段内含分隔符）默认即可被正确解析。
   请确认是否无意中指定了 ``quote_disabled=true``\ 。
3. 确认CSV文件格式（是否符合RFC 4180）。若文件中包含没有对应闭合引号的 ``"``\ ，
   则从该处开始之后的整个文件内容都会被读取为单个字段值。

标题行处理
----------

**症状**: 第一行被识别为数据

**解决方法**:

有标题行时:

::

    has_header_line=true

无标题行时:

::

    has_header_line=false

无法获取数据
------------

**症状**: 爬取成功但数量为0

**确认事项**:

1. 确认CSV文件是否为空
2. 确认脚本设置是否正确（列名和 ``cell<N>`` 的引用是否不含 ``data.`` 前缀）
3. 确认列名是否正确（has_header_line=true 时）
4. 在日志中确认错误信息
5. 确认日志中是否出现 ``Unknown parameter(s)``\ 警告（参数名的拼写错误仅在爬取
   开始时警告一次，除此之外将被静默忽略）

第二次导入CSV会导致之前的索引消失
---------------------------------

**症状**: 爬取第一个CSV文件后，改天再爬取同一数据存储配置下的第二个CSV文件时，
从第一个CSV文件注册的文档从搜索结果中消失了。

**原因**:

爬取完成后，|Fess| 会从索引中删除属于该数据存储配置、且在本次会话中未被重新注册的文档
（ ``delete_old_docs``\ ，默认: true）。若在不同时间将多个CSV文件投入同一数据存储配置，
则在爬取后投入的文件时，先前投入文件的内容会被视为「本次会话中未被重新注册」的文档而被删除。

**解决方法**:

如果要在不同时间将多个CSV文件投入同一数据存储配置，并希望各自的内容不断累积，
请指定以下内容。

::

    delete_old_docs=false

大型CSV文件
-----------

**症状**: 内存不足或超时

**解决方法**:

1. 将CSV文件分割成多个
2. 在脚本中只使用必要的列
3. 增加 |Fess| 的堆大小
4. 过滤不必要的行

包含换行符的字段
----------------

RFC 4180格式中，可通过引号包裹来处理包含换行符的字段。
由于引号处理默认为启用状态，无需指定任何参数即可正确解析：

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

参数:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

CsvListDataStore
================

``fess-ds-csv`` 插件除 ``CsvDataStore`` 外，还包含 ``CsvListDataStore`` 处理器。

``CsvListDataStore`` 是 ``CsvDataStore`` 的扩展，提供以下附加功能：

- 多线程处理（通过 ``numOfThreads`` 参数控制）
- 自动删除已处理的CSV文件
- 基于时间戳的文件过滤（跳过正在写入的文件）

``CsvDataStore`` 的所有参数和脚本设置均可直接使用。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 处理器名称
     - CsvListDataStore

附加参数
--------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``timestamp_margin``
     - 否
     - 文件最后修改时间的经过时间（毫秒）。未达到此时间的文件将被视为正在写入而跳过（默认: 10000）
   * - ``numOfThreads``
     - 否
     - 处理线程数（默认: 1）
   * - ``delete_processed_file``
     - 否
     - 处理完成后是否删除该CSV文件（默认: true）
   * - ``ignore_data_store_exception``
     - 否
     - 处理某个CSV文件时若发生异常，是否继续整体爬取（默认: true）

.. warning::

   ``CsvListDataStore`` 在处理完成后会自动 **删除** CSV文件（ ``delete_processed_file`` 的默认值为 ``true``\ ）。处理过程中发生错误时，文件将被改为重命名为 ``.txt``\ （重命名失败时则直接删除）。若不希望删除文件，请指定 ``delete_processed_file=false``\ 。

CSV行格式（事件类型）
---------------------

传递给 ``CsvListDataStore`` 的CSV文件，每行至少需要「事件类型」和「URL」两列。
可以进一步添加列，并以 ``cell3``、``cell4``\ ……的形式引用
（例如用于向 ``timestamp.overwrite`` 传值）。

::

    <事件类型>,<URL>

事件类型可指定以下三种值。

- ``create`` - 文件已创建
- ``modify`` - 文件已更新
- ``delete`` - 文件已删除

``create`` 和 ``modify`` 被视为相同的处理（对目标URL的爬取与索引注册）。两者行为没有区别。

列名（有标题行时）及各事件类型的值，可通过以下参数进行更改。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数
     - 说明
   * - ``field.event_type``
     - 存储事件类型的列名（默认: ``event_type``）
   * - ``event.create``
     - 表示「创建」的值（默认: ``create``）
   * - ``event.modify``
     - 表示「更新」的值（默认: ``modify``）
   * - ``event.delete``
     - 表示「删除」的值（默认: ``delete``）

CSV文件示例:

::

    modify,smb://servername/data/testfile1.txt
    delete,smb://servername/data/testfile2.txt

脚本示例（无标题行时）:

::

    event_type=cell1
    url=cell2

覆盖字段值（.overwrite）
------------------------

在脚本中构建的索引字段名末尾加上 ``.overwrite``\ ，该字段的值将不再采用爬取结果
（实际文件爬取所获得的值），而是被CSV中设置的值覆盖。

::

    timestamp.overwrite=cell3

.. note::

   搜索界面的日期分面（facet）是通过 ``timestamp`` 字段而非 ``created`` 字段进行筛选的。
   如需用CSV中的值覆盖时间戳，请指定 ``timestamp.overwrite`` 而非 ``created.overwrite``\ 。

认证与代理设置的继承
--------------------

``CsvListDataStore`` 会实际爬取CSV中记载的URL，但文件爬取或网页爬取的数据存储配置中
注册的认证信息、代理设置不会被继承。请将所需设置单独指定为该数据存储配置的参数。

SMB认证示例:

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

代理设置示例:

::

    crawler.web.proxyHost=proxy.example.com
    crawler.web.proxyPort=8080

脚本高级使用示例
================

数据加工
--------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

条件索引
--------

::

    // 仅索引价格10000以上的商品
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

.. note::

   如上所示，``url`` 返回 ``null`` 的行不会被视为失败，而是被静默跳过。
   跳过的行数按CSV文件分别统计，并在该文件读取结束时，作为一条汇总WARN日志输出
   （并非每行失败的URL都会被单独记录。处理多个CSV文件时，会按文件数量输出对应的WARN日志）。

多列合并
--------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\n规格:\n" + specs + "\n\n注意事项:\n" + notes
    category=category

日期格式化
----------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // 如需日期格式转换则添加额外处理

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-json` - JSON连接器
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `RFC 4180 - CSV格式 <https://datatracker.ietf.org/doc/html/rfc4180>`_
