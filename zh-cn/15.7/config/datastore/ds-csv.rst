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
    quote_disabled=false

多个文件:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   引号处理和转义处理默认为 **禁用** 状态。
   如需处理字段内包含分隔符或换行符的CSV（符合RFC 4180规范），
   请明确指定 ``quote_disabled=false`` 以启用引号处理。
   详情请参阅后文的「启用引号与转义处理」。

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
     - 引号字符（默认: 双引号 ``"``）。但引号处理默认为禁用状态（参见 ``quote_disabled``）。
   * - ``escape_character``
     - 否
     - 转义字符（默认: 反斜杠 ``\``）。但转义处理默认为禁用状态（参见 ``escape_disabled``）。

.. note::

   ``files`` 和 ``directories`` 均未指定时将报错（ ``DataStoreException`` ）。
   请至少指定其中一个。

高级参数
~~~~~~~~~~~~~~~~

以下参数用于精细控制CSV的解析行为：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数
     - 说明
   * - ``quote_disabled``
     - 是否禁用引号处理（默认: true）。处理符合RFC 4180规范的带引号字段时，请指定 ``false``。
   * - ``escape_disabled``
     - 是否禁用转义处理（默认: true）。启用 ``escape_character`` 转义时，请指定 ``false``。
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
- ``cell<N>`` - 按列索引引用（ ``cell1``、``cell2``……从1开始，无论是否有标题行均可使用）
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

   如上述 ``"Book, Programming"`` 所示，若要在字段内包含分隔符并使用引号包裹，
   需指定 ``quote_disabled=false`` 以启用引号处理。
   引号处理禁用时（默认），引号被视为普通字符，字段按分隔符分割。

启用引号与转义处理
------------------

引号处理和转义处理默认为禁用状态。请按以下方式明确启用。

启用引号处理:

::

    # 参数
    quote_disabled=false
    quote_character="

启用转义处理:

::

    # 参数
    escape_disabled=false
    escape_character=\

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

单引号（需启用引号处理）:

::

    # 参数
    quote_disabled=false
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
3. 确认文件扩展名是否为 ``.csv`` 或 ``.tsv``（其他扩展名将被跳过）
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

2. 处理带引号字段（字段内含分隔符）时，请启用引号处理:

   ::

       quote_disabled=false

3. 确认CSV文件格式（是否符合RFC 4180）

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
由于引号处理默认为禁用状态，需指定 ``quote_disabled=false``：

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
    quote_disabled=false
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

.. note::

   ``CsvListDataStore`` 在处理完成后会自动删除CSV文件。处理过程中发生错误时，文件将被重命名为 ``.txt``（重命名失败时则直接删除）。

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
