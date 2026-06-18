==================================
JSON连接器
==================================

概述
====

JSON连接器提供从本地JSONL文件（JSON Lines格式）获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-json`` 插件。

前提条件
========

1. 需要安装插件
2. 需要对JSON文件的访问权限
3. 需要理解JSON的结构

插件安装
------------------------

方法1: 直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 放置
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或者
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products JSON
   * - 处理器名称
     - JsonDataStore
   * - 启用
     - 开

参数设置
----------------

本地文件:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

多个文件:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

目录指定:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 参数
     - 必需
     - 说明
   * - ``files``
     - 否
     - 要处理的JSON文件路径（可指定多个：逗号分隔）。仅处理扩展名为 ``.json`` 或 ``.jsonl`` 的文件。
   * - ``directories``
     - 否
     - 包含JSON文件的目录路径（可指定多个：逗号分隔）
   * - ``fileEncoding``
     - 否
     - 字符编码（默认: UTF-8）

.. warning::
   必须指定 ``files`` 或 ``directories`` 其中之一。
   如果两者都未指定（为空），将会发生 ``DataStoreException``。
   如果两者都指定了，``files`` 优先，``directories`` 将被忽略。

.. note::
   参数名使用驼峰命名法 ``fileEncoding``（而非蛇形命名法 ``file_encoding``）。

目录指定时的行为
~~~~~~~~~~~~~~~~~~~~~~~~~~

指定 ``directories`` 时，各目录直接下的文件将按以下规则处理。

- **不会遍历子目录**（不进行递归搜索）。
- 仅处理扩展名为 ``.json`` 或 ``.jsonl`` 的文件（不区分大小写）。
- 文件按修改时间（最后修改时刻）升序处理。

.. note::
   此连接器仅支持本地文件系统上的JSON文件，不支持HTTP访问或API认证功能。

脚本设置
--------------

各字段的值通过引用JSON对象各字段的值来组装。
JSON对象顶层字段在脚本中可作为 **无前缀的变量** 直接引用
（不带 ``data.`` 之类的前缀）。

简单JSON对象:

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

嵌套JSON对象（嵌套对象以映射形式引用）:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

数组元素处理:

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

可用字段
~~~~~~~~~~~~~~~~~~~~

- ``<字段名>`` - 通过名称直接引用JSON对象的顶层字段
- ``<父>.<子>`` - 嵌套对象的字段
- ``<数组>[<索引>]`` - 数组元素
- ``<数组>.<方法>`` - 数组的方法（``join``、``collect``、``size`` 等）

.. note::

   如果字段名包含空格或连字符等Groovy标识符中无效的字符，
   则无法直接将该字段作为变量名引用。

JSON格式详情
==============

JSON文件格式
----------------

JSON连接器读取JSONL（JSON Lines）格式的文件。
这是一种每行记录一个JSON对象的格式。文件逐行读取，
每行作为独立的JSON对象进行解析。

.. note::
   扩展名为 ``.json`` 的文件也在处理范围内，但内容必须为JSONL格式
   （每行一个对象）。
   数组格式的JSON文件（``[{...}, {...}]``）或经过多行格式化
   （pretty-print）的JSON无法直接读取，请转换为JSONL格式。

JSONL格式的文件:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

使用示例
========

产品目录
--------------

参数:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

脚本:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " 价格: " + price + " 日元"
    digest=category
    price=price

多JSON文件整合
---------------------

参数:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

脚本:

::

    url="https://example.com/item/" + id
    title=title
    content=content

故障排除
======================

找不到文件
----------------------

**症状**: 日志中输出 ``... is not found.`` 或 ``Source file ... does not exist.``

**确认事项**:

1. 确认文件路径是否正确
2. 确认文件是否存在
3. 确认文件扩展名是否为 ``.json`` 或 ``.jsonl``
4. 确认是否有文件读取权限

JSON解析错误
--------------

**症状**: 日志中输出 ``Crawling Access Exception`` 和 ``JsonParseException`` 等信息

如果包含非法行，仅该行被跳过并记录为失败URL，
爬取本身从下一行继续进行。

**确认事项**:

1. 确认JSON文件格式是否正确（每行一个对象的JSONL格式）:

   ::

       # 验证各行是否为有效的JSON对象
       cat data.json | jq -c .

2. 确认字符编码是否正确
3. 确认是否有单个对象跨多行的情况
4. 确认是否包含注释（JSON标准不允许注释）

无法获取数据
--------------------

**症状**: 爬取成功但数量为0

**确认事项**:

1. 确认JSON结构
2. 确认脚本设置是否正确（字段引用是否不带 ``data.`` 前缀）
3. 确认字段名是否正确（包括大小写）
4. 在日志中确认错误信息

大型JSON文件
------------------

**症状**: 内存不足或超时

由于文件逐行读取，文件整体大小不会直接影响内存使用量。
但如果单行（单个对象）极大，或索引注册负载较高，
则可能出现问题。

**解决方法**:

1. 将JSON文件分割成多个
2. 增加 |Fess| 的堆大小

脚本的高级使用示例
========================

条件处理
------------

各字段作为独立的表达式进行求值。条件值使用三元运算符:

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

数组合并
----------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

设置默认值
------------------

::

    url="https://example.com/item/" + id
    title=title ?: "无标题"
    content=description ?: (summary ?: "无描述")
    price=price ?: 0

日期格式化
------------------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

数值处理
----------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-csv` - CSV连接器
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
