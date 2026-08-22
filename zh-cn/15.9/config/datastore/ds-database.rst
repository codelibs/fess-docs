==============================
数据库连接器（数据库搜索）
==============================

概述
====

数据库连接器可将JDBC兼容的关系型数据库(MySQL、PostgreSQL、Oracle、SQL Server等)中的记录注册到 |Fess| 索引,实现数据库搜索(对数据库内容进行全文搜索)。它会将SELECT语句获取到的各列映射到搜索字段后进行注册。

数据库连接器提供从JDBC兼容的关系数据库获取数据并
注册到 |Fess| 索引的功能。

此功能需要安装 ``fess-ds-db`` 插件。

支持的数据库
============

支持所有JDBC兼容的数据库。主要包括：

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

前提条件
========

1. 需要安装 ``fess-ds-db`` 插件
2. 需要对应连接数据库的JDBC驱动程序
3. 需要对数据库的读取访问权限
4. 获取大量数据时，适当的查询设计很重要

插件安装
--------

方法1：直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # 放置
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2：从管理界面安装

1. 打开"系统"→"插件"
2. 上传JAR文件
3. 重启 |Fess|

JDBC驱动程序安装
----------------

将对应连接数据库的JDBC驱动程序放置在 |Fess| 的类路径（ ``app/WEB-INF/lib/`` 目录）中：

::

    # 示例：MySQL驱动程序
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # 或
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

放置JDBC驱动程序后，重启 |Fess| 以加载驱动程序。

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
--------

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
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 参数
     - 必须
     - 说明
   * - ``driver``
     - 是
     - JDBC驱动程序类名（未指定时将抛出 ``DataStoreException``）
   * - ``url``
     - 是
     - JDBC连接URL（连接必须项）
   * - ``sql``
     - 是
     - 数据获取用SQL查询（未指定时将抛出 ``DataStoreException``）
   * - ``username``
     - 否
     - 数据库用户名
   * - ``password``
     - 否
     - 数据库密码
   * - ``fetch_size``
     - 否
     - JDBC获取大小。MySQL流式结果集请指定 ``MIN_VALUE``
   * - ``default_mimetype``
     - 否
     - 提取BLOB/二进制列内容时使用的默认MIME类型
   * - ``column_label.mimetype``
     - 否
     - 指定存储BLOB/二进制列提取所用MIME类型的列名（例：``column_label.mimetype=content_type``）
   * - ``column_label.filename``
     - 否
     - 指定存储BLOB/二进制列提取所用文件名的列名（从扩展名推断MIME类型）
   * - ``info.*``
     - 否
     - 附加JDBC连接属性（例：``info.ssl=true``）。去掉 ``info.`` 前缀后的键将传递给JDBC驱动程序
   * - ``readInterval``
     - 否
     - 每行处理之间的延迟（毫秒）。默认值：0
   * - ``script_type``
     - 否
     - 脚本引擎类型。默认值：groovy

脚本设置
--------

将SQL列名映射到索引字段：

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

可用字段：

- ``<column_name>`` - SQL查询的结果列（直接使用列标签名称访问，不带 ``data.`` 等前缀）

.. note::
   列名需与 ``SELECT`` 子句中的列标签（别名）一致。
   使用聚合函数或表达式时，请用 ``AS`` 明确指定别名
   （例：``COUNT(*) AS total``）。

BLOB/二进制数据的导入
=====================

BLOB、CLOB、NCLOB、字节数组、二进制流等列将自动经过
内容提取处理（与文件爬取使用相同的提取器），以文本形式
导入。数组类型的列将转换为空格分隔的字符串。NULL值将
变为空字符串。

要从BLOB或二进制流中正确提取文本，需要判断数据类型（MIME类型）。
判断时使用以下优先顺序：

1. ``column_label.mimetype=<列名>`` - 将指定列的值作为MIME类型使用
2. ``column_label.filename=<列名>`` - 将指定列的值作为文件名处理，从扩展名推断MIME类型
3. ``default_mimetype`` - 上述方式无法判断时使用的默认MIME类型

示例（使用 ``content_type`` 列的MIME类型提取 ``file_data`` 列的BLOB）：

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

SQL查询设计
===========

高效查询
--------

处理大量数据时，查询性能很重要。
SQL将原样发送到数据库（不进行参数绑定）：

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

增量抓取
--------

只获取更新记录的方法：

::

    # 按更新时间过滤
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # 按ID范围指定
    sql=SELECT * FROM articles WHERE id > 10000

URL生成
-------

文档的URL在脚本中生成：

::

    # 固定模式
    url="https://example.com/article/" + id

    # 组合多个字段
    url="https://example.com/" + category + "/" + slug

    # 使用存储在数据库中的URL
    url=url

多字节字符支持
==============

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

安全性
======

数据库认证信息保护
------------------

.. warning::
   在配置文件中直接写入密码存在安全风险。

推荐方法：

1. 使用环境变量
2. 使用 |Fess| 的加密功能
3. 使用只读用户

最小权限原则
------------

只为数据库用户授予必要的最小权限：

::

    -- MySQL示例
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

使用示例
========

产品目录搜索
------------

参数：

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

脚本：

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " 类别：" + category + " 价格：" + price + "元"
    lastModified=updated_at

知识库文章
----------

参数：

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

脚本：

::

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

故障排除
========

找不到JDBC驱动程序
------------------

**症状**：``ClassNotFoundException`` 或 ``No suitable driver``

**解决方法**：

1. 确认JDBC驱动程序是否放置在 ``lib/`` 中
2. 确认驱动程序类名是否正确
3. 重启 |Fess|

连接错误
--------

**症状**：``Connection refused`` 或认证错误

**检查项**：

1. 数据库是否已启动
2. 主机名、端口号是否正确
3. 用户名、密码是否正确
4. 防火墙设置

查询错误
--------

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
- :doc:`../crawler-basic` - 爬虫基本配置
- :doc:`../search-basic` - 搜索功能
