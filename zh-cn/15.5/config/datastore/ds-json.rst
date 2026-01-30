==================================
JSON连接器
==================================

概述
====

JSON连接器提供从JSON文件或JSON API获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-json`` 插件。

前提条件
========

1. 需要安装插件
2. 需要对JSON文件或API的访问权限
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

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

HTTP文件:

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

REST API（带认证）:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

多个文件:

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``file_path``
     - 是
     - JSON文件路径或API URL（可指定多个：逗号分隔）
   * - ``encoding``
     - 否
     - 字符编码（默认: UTF-8）
   * - ``json_path``
     - 否
     - JSONPath数据提取路径（默认: ``$``）
   * - ``http_method``
     - 否
     - HTTP方法（GET、POST等，默认: GET）
   * - ``auth_type``
     - 否
     - 认证类型（bearer、basic）
   * - ``auth_token``
     - 否
     - 认证令牌（bearer认证时）
   * - ``auth_username``
     - 否
     - 认证用户名（basic认证时）
   * - ``auth_password``
     - 否
     - 认证密码（basic认证时）
   * - ``http_headers``
     - 否
     - 自定义HTTP头（JSON格式）

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

简单数组
----------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

参数:

::

    json_path=$

嵌套结构
--------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

参数:

::

    json_path=$.data.products

脚本:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

复杂数组
----------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

参数:

::

    json_path=$.articles

脚本:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

JSONPath的使用
===============

什么是JSONPath
------------

JSONPath是用于指定JSON内元素的查询语言。
相当于XML中的XPath。

基本语法
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 语法
     - 说明
   * - ``$``
     - 根元素
   * - ``$.field``
     - 顶层字段
   * - ``$.parent.child``
     - 嵌套字段
   * - ``$.array[0]``
     - 数组的第一个元素
   * - ``$.array[*]``
     - 数组的所有元素
   * - ``$..field``
     - 递归搜索

JSONPath示例
-------------

所有元素（根）:

::

    json_path=$

特定数组:

::

    json_path=$.data.items

嵌套数组:

::

    json_path=$.response.results.products

递归搜索:

::

    json_path=$..products

使用示例
======

产品目录API
---------------

API响应:

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "笔记本电脑",
            "description": "高性能笔记本电脑",
            "price": 120000,
            "category": "电脑",
            "in_stock": true
          }
        ]
      }
    }

参数:

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

脚本:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " 价格: " + data.price + "元"
    digest=data.category
    price=data.price

博客文章API
-------------

API响应:

::

    {
      "posts": [
        {
          "id": 1,
          "title": "文章标题",
          "body": "文章正文...",
          "author": {
            "name": "张三",
            "email": "zhang@example.com"
          },
          "tags": ["技术", "编程"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

参数:

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

脚本:

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

Bearer认证API
---------------

参数:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

脚本:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

Basic认证API
--------------

参数:

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

脚本:

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

使用自定义头
----------------------

参数:

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

脚本:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

多JSON文件整合
---------------------

参数:

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

脚本:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

POST请求
--------------

参数:

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

脚本:

::

    url="https://example.com/result/" + data.id
    title=data.title
    content=data.content

故障排除
======================

找不到文件
----------------------

**症状**: ``FileNotFoundException`` 或 ``404 Not Found``

**确认事项**:

1. 确认文件路径或URL是否正确
2. 确认文件是否存在
3. 如果是URL，确认API是否正在运行
4. 确认网络连接

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

JSONPath错误
--------------

**症状**: 无法获取数据或结果为空

**确认事项**:

1. 确认JSONPath语法是否正确
2. 确认目标元素是否存在
3. 使用测试工具验证JSONPath:

   ::

       # 使用jq确认
       cat data.json | jq '$.data.products'

4. 确认路径是否指向正确的层级

认证错误
----------

**症状**: ``401 Unauthorized`` 或 ``403 Forbidden``

**确认事项**:

1. 确认认证类型是否正确（bearer、basic）
2. 确认认证令牌或用户名/密码是否正确
3. 确认令牌的有效期
4. 确认API的权限设置

无法获取数据
--------------------

**症状**: 爬取成功但数量为0

**确认事项**:

1. 确认JSONPath是否指向正确的元素
2. 确认JSON结构
3. 确认脚本设置是否正确
4. 确认字段名是否正确（包括大小写）
5. 在日志中确认错误信息

数组处理
----------

JSON为数组的情况:

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

参数:

::

    json_path=$

JSON为包含数组的对象的情况:

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

参数:

::

    json_path=$.items

大型JSON文件
------------------

**症状**: 内存不足或超时

**解决方法**:

1. 将JSON文件分割成多个
2. 使用JSONPath只提取必要的部分
3. 如果是API，使用分页
4. 增加 |Fess| 的堆大小

API速率限制
-------------

**症状**: ``429 Too Many Requests``

**解决方法**:

1. 增加爬取间隔
2. 确认API的速率限制
3. 使用多个API密钥进行负载均衡

脚本的高级使用示例
========================

条件处理
------------

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

数组合并
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

设置默认值
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "无标题"
    content=data.description || data.summary || "无描述"
    price=data.price || 0

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
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-csv` - CSV连接器
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
