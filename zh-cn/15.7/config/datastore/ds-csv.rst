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

HTTP文件:

::

    files=https://example.com/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

多个文件:

::

    files=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - 参数
     - 必需
     - 说明
   * - ``files``
     - 是
     - CSV文件路径（本地、HTTP，可指定多个：逗号分隔）
   * - ``file_encoding``
     - 否
     - 字符编码（默认: UTF-8）
   * - ``has_header_line``
     - 否
     - 是否有标题行（默认: false）
   * - ``separator_character``
     - 否
     - 分隔符（默认: 逗号 ``,``）
   * - ``quote_character``
     - 否
     - 引号（默认: 双引号 ``"``）

脚本设置
--------------

有标题行的情况:

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

无标题行的情况（列索引指定）:

::

    url="https://example.com/product/" + data.cell1
    title=data.cell2
    content=data.cell3
    price=data.cell4

可用字段
~~~~~~~~~~~~~~~~~~~~

- ``data.<列名>`` - 标题行的列名（has_header_line=true 时）
- ``data.cell<N>`` - 列索引（has_header_line=false 时，从1开始: ``cell1``, ``cell2``...）

CSV格式详情
=============

标准CSV（RFC 4180兼容）
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

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

日语文件（Shift_JIS）:

::

    file_encoding=Shift_JIS

日语文件（EUC-JP）:

::

    file_encoding=EUC-JP

使用示例
======

产品目录CSV
-----------------

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
    quote_character="

脚本:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 类别: " + data.category + " 价格: " + data.price + "元"
    digest=data.category
    price=data.price

库存信息过滤:

::

    url=data.in_stock == "true" ? "https://shop.example.com/product/" + data.product_id : null
    title=data.in_stock == "true" ? data.name : null
    content=data.in_stock == "true" ? data.description : null
    price=data.in_stock == "true" ? data.price : null

员工名册CSV
-------------

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
    quote_character="

脚本:

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="部门: " + data.department + "\n职位: " + data.position + "\n邮箱: " + data.email + "\n电话: " + data.phone
    digest=data.department

无标题行的CSV
-----------------

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
    quote_character="

脚本:

::

    url="https://example.com/item/" + data.cell1
    title=data.cell2
    content=data.cell3
    price=data.cell4

多CSV文件整合
---------------------

参数:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

脚本:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

制表符分隔（TSV）文件
-------------------------

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
    quote_character="

脚本:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

故障排除
======================

找不到文件
----------------------

**症状**: ``FileNotFoundException`` 或 ``No such file``

**确认事项**:

1. 确认文件路径是否正确（推荐使用绝对路径）
2. 确认文件是否存在
3. 确认是否有文件读取权限
4. 确认 |Fess| 运行用户是否可以访问

出现乱码
------------------

**症状**: 中文/日文无法正确显示

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
----------------------

**症状**: 列分隔符无法正确识别

**确认事项**:

1. 确认分隔符是否正确:

   ::

       # 逗号
       separator_character=,

       # 制表符
       separator_character=\t

       # 分号
       separator_character=;

2. 确认引号设置
3. 确认CSV文件格式（是否符合RFC 4180）

标题行处理
----------------

**症状**: 第一行被识别为数据

**解决方法**:

有标题行时:

::

    has_header_line=true

无标题行时:

::

    has_header_line=false

无法获取数据
--------------------

**症状**: 爬取成功但数量为0

**确认事项**:

1. 确认CSV文件是否为空
2. 确认脚本设置是否正确
3. 确认列名是否正确（has_header_line=true 时）
4. 在日志中确认错误信息

大型CSV文件
-----------------

**症状**: 内存不足或超时

**解决方法**:

1. 将CSV文件分割成多个
2. 在脚本中只使用必要的列
3. 增加 |Fess| 的堆大小
4. 过滤不必要的行

包含换行符的字段
--------------------

RFC 4180格式中，可以通过引号包裹来处理包含换行符的字段:

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

脚本的高级使用示例
========================

数据加工
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=Integer.parseInt(data.price)
    category=data.category.toLowerCase()

条件索引
--------------------

::

    # 仅价格10000以上的商品
    url=Integer.parseInt(data.price) >= 10000 ? "https://example.com/product/" + data.id : null
    title=Integer.parseInt(data.price) >= 10000 ? data.name : null
    content=Integer.parseInt(data.price) >= 10000 ? data.description : null
    price=Integer.parseInt(data.price) >= 10000 ? data.price : null

多列合并
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\n规格:\n" + data.specs + "\n\n注意事项:\n" + data.notes
    category=data.category

日期格式化
------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # 如需日期格式转换则添加额外处理

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-json` - JSON连接器
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `RFC 4180 - CSV格式 <https://datatracker.ietf.org/doc/html/rfc4180>`_
