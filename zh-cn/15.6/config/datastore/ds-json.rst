==================================
JSON连接器
==================================

概述
====

JSON连接器提供从本地JSON文件或JSONL文件获取数据并注册到
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
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``files``
     - 否
     - JSON文件路径（可指定多个：逗号分隔）
   * - ``directories``
     - 否
     - 包含JSON文件的目录路径
   * - ``fileEncoding``
     - 否
     - 字符编码（默认: UTF-8）

.. warning::
   必须指定 ``files`` 或 ``directories`` 其中之一。
   如果两者都未指定，将会发生 ``DataStoreException`` 。
   如果两者都指定了， ``files`` 优先， ``directories`` 将被忽略。

.. note::
   此连接器仅支持本地文件系统上的JSON文件，不支持HTTP访问或API认证功能。

脚本设置
--------------

简单JSON对象:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

嵌套JSON对象:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

数组元素处理:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

可用字段
~~~~~~~~~~~~~~~~~~~~

- ``data.<字段名>`` - JSON对象的字段
- ``data.<父>.<子>`` - 嵌套对象
- ``data.<数组>[<索引>]`` - 数组元素
- ``data.<数组>.<方法>`` - 数组的方法（join、length等）

JSON格式详情
==============

JSON文件格式
----------------

JSON连接器读取JSONL（JSON Lines）格式的文件。
这是一种每行记录一个JSON对象的格式。

.. note::
   数组格式的JSON文件（ ``[{...}, {...}]`` ）无法直接读取。
   请转换为JSONL格式。

JSONL格式的文件:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

使用示例
======

产品目录
--------------

参数:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

脚本:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 价格: " + data.price + "元"
    digest=data.category
    price=data.price

多JSON文件整合
---------------------

参数:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

脚本:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

故障排除
======================

找不到文件
----------------------

**症状**: ``FileNotFoundException``

**确认事项**:

1. 确认文件路径是否正确
2. 确认文件是否存在
3. 确认是否有文件读取权限

JSON解析错误
--------------

**症状**: ``JsonParseException`` 或 ``Unexpected character``

**确认事项**:

1. 确认JSON文件格式是否正确:

   ::

       # 验证JSON
       cat data.json | jq .

2. 确认字符编码是否正确
3. 确认是否有非法字符或换行
4. 确认是否包含注释（JSON标准不允许注释）

无法获取数据
--------------------

**症状**: 爬取成功但数量为0

**确认事项**:

1. 确认JSON结构
2. 确认脚本设置是否正确
3. 确认字段名是否正确（包括大小写）
4. 在日志中确认错误信息

大型JSON文件
------------------

**症状**: 内存不足或超时

**解决方法**:

1. 将JSON文件分割成多个
2. 增加 |Fess| 的堆大小

脚本的高级使用示例
========================

条件处理
------------

每个字段作为独立的表达式进行求值。条件值使用三元运算符:

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

数组合并
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

设置默认值
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "无标题"
    content=data.description ?: (data.summary ?: "无描述")
    price=data.price ?: 0

日期格式化
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

数值处理
----------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price as Float
    stock=data.stock_quantity as Integer

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-csv` - CSV连接器
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
