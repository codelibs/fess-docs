==================================
数据库连接器
==================================

概述
====

数据库连接器提供从JDBC兼容的关系数据库获取数据并
注册到 |Fess| 索引的功能。

此功能内置于 |Fess| 中，无需额外插件。

支持的数据库
================

支持所有JDBC兼容的数据库。主要包括：

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

前提条件
========

1. 需要JDBC驱动程序
2. 需要对数据库的读取访问权限
3. 获取大量数据时，适当的查询设计很重要

JDBC驱动程序安装
----------------------------

将JDBC驱动程序放置在 ``lib/`` 目录中：

::

    # 例如：MySQL驱动程序
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

重启 |Fess| 以加载驱动程序。

设置方法
========

从管理界面的"爬虫"→"数据存储"→"新建"进行设置。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 名称
     - Products Database
   * - 处理器名
     - DatabaseDataStore
   * - 启用
     - 开

参数设置
----------------

MySQL/MariaDB示例：

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

PostgreSQL示例：

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必须
     - 说明
   * - ``driver``
     - 是
     - JDBC驱动程序类名
   * - ``url``
     - 是
     - JDBC连接URL
   * - ``username``
     - 是
     - 数据库用户名
   * - ``password``
     - 是
     - 数据库密码
   * - ``sql``
     - 是
     - 数据获取用SQL查询
   * - ``fetch.size``
     - 否
     - 获取大小（默认：100）

脚本设置
--------------

将SQL列名映射到索引字段：

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

可用字段：

- ``data.<column_name>`` - SQL查询的结果列

SQL查询设计
===============

高效查询
--------------

处理大量数据时，查询性能很重要：

::

    # 使用索引的高效查询
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
    ORDER BY id

增量抓取
------------

只获取更新记录的方法：

::

    # 按更新时间过滤
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # 按ID范围指定
    sql=SELECT * FROM articles WHERE id > 10000

URL生成
---------

文档的URL在脚本中生成：

::

    # 固定模式
    url="https://example.com/article/" + data.id

    # 组合多个字段
    url="https://example.com/" + data.category + "/" + data.slug

    # 使用存储在数据库中的URL
    url=data.url

多字节字符支持
====================

处理包含中文等多字节字符的数据时：

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL通常默认使用UTF-8。如有需要：

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

连接池
==============

处理大量数据时，请考虑连接池：

::

    # 使用HikariCP时的设置
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

安全性
============

数据库认证信息保护
--------------------------

.. warning::
   在配置文件中直接写入密码存在安全风险。

推荐方法：

1. 使用环境变量
2. 使用 |Fess| 的加密功能
3. 使用只读用户

最小权限原则
--------------

只为数据库用户授予必要的最小权限：

::

    -- MySQL示例
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

使用示例
======

产品目录搜索
------------------

参数：

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

脚本：

::

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " 类别：" + data.category + " 价格：" + data.price + "元"
    lastModified=data.updated_at

知识库文章
------------------

参数：

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

脚本：

::

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

故障排除
======================

找不到JDBC驱动程序
----------------------------

**症状**：``ClassNotFoundException`` 或 ``No suitable driver``

**解决方法**：

1. 确认JDBC驱动程序是否放置在 ``lib/`` 中
2. 确认驱动程序类名是否正确
3. 重启 |Fess|

连接错误
----------

**症状**：``Connection refused`` 或认证错误

**检查项**：

1. 数据库是否已启动
2. 主机名、端口号是否正确
3. 用户名、密码是否正确
4. 防火墙设置

查询错误
------------

**症状**：``SQLException`` 或SQL语法错误

**检查项**：

1. 直接在数据库中执行SQL查询进行测试
2. 确认列名是否正确
3. 确认表名是否正确

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-csv` - CSV连接器
- :doc:`ds-json` - JSON连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
