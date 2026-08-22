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

方法1：从管理界面安装

1. 打开"系统"→"插件"
2. 上传JAR文件
3. 重启 |Fess|

方法2：直接放置JAR文件

::

    # 从CodeLibs仓库下载
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # 放置（与从管理界面安装时的目录相同）
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # 或
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

JDBC驱动程序安装
----------------

JDBC驱动程序未包含在插件中。请另行获取对应连接数据库的驱动程序并自行放置。

数据存储爬取在爬虫进程中执行，因此驱动程序必须位于 **爬虫进程的类路径** 中。以下任一目录均可：

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # 示例：MySQL驱动程序
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # 或
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

放置JDBC驱动程序后，重启 |Fess| 以加载驱动程序。

.. note::
   找不到驱动程序时，爬取将以
   ``The JDBC driver ... is not on the crawler classpath.`` 消息失败。

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
     - JDBC获取大小。``MIN_VALUE`` 用于让MySQL逐行读取结果集，其他驱动程序不接受负值（将输出警告并以驱动程序默认值继续）。负值或非数值将输出警告并被忽略
   * - ``query_timeout``
     - 否
     - 查询超时时间（秒）。``0`` 表示无限制（JDBC默认值）。未指定该参数时不设置超时
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
   * - ``last_crawl_time``
     - 否
     - 增量抓取的基准时间。爬取完成时会自动回写（参见"增量抓取"）
   * - ``last_crawl_time_format``
     - 否
     - ``last_crawl_time`` 的格式。默认值：``yyyy-MM-dd HH:mm:ss``

.. note::
   查询挂起时，即使停止作业也不会释放爬虫线程。
   停止请求只在行与行之间进行判断，因此对在驱动程序内部阻塞的调用无效。
   对于可能长时间执行的查询，请设置 ``query_timeout``。

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
- ``crawlingConfig`` - 数据存储配置
- ``crawlingContext`` - 爬取过程中的上下文。可通过 ``crawlingContext.doc`` 引用正在构建的文档

.. note::
   列名需与 ``SELECT`` 子句中的列标签（别名）一致。
   使用聚合函数或表达式时，请用 ``AS`` 明确指定别名
   （例：``COUNT(*) AS total``）。

.. note::
   列标签的大小写因数据库而异。PostgreSQL会将未加引号的标识符转换为小写，
   H2会转换为大写，而MySQL则按声明原样返回。若脚本中引用的名称无法解析，
   该字段将保持未设置状态（不会报错）。若重视可移植性，请用 ``AS`` 明确指定别名。

.. warning::
   脚本不仅可以引用SQL的结果列，还可以将 **整个数据存储参数** 作为同名变量引用。
   ``driver`` 、 ``url`` 、 ``username`` 、 ``password`` 、 ``sql`` 等也会作为变量可见，
   因此可能会意外遮蔽同名的列，或者在列不存在时混入参数的值。
   当存在同名的列时，以列的值优先。

BLOB/二进制数据的导入
=====================

二进制列（BLOB、 ``BYTEA`` 、字节数组、二进制流）会经过内容提取处理
（与文件爬取使用相同的提取器），以文本形式导入。

另一方面，CLOB、NCLOB和字符流 **不会经过提取器** ，而是直接按字符串读取。
下述MIME类型的指定对它们不适用。

数组类型的列将变为以空格连接各元素的字符串。NULL值将变为空字符串。

.. note::
   即使是同样的BLOB列，不同的JDBC驱动程序有的返回 ``java.sql.Blob`` ，有的返回字节数组
   （MySQL和PostgreSQL返回字节数组）。两者的提取方式相同。

.. note::
   CLOB、NCLOB会不受大小限制地全部读入内存。处理非常大的文本列时，
   请考虑在SQL端使用 ``SUBSTRING`` 等进行截断。经过提取器的路径则会应用
   爬虫的最大内容长度设置。

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

在 ``sql`` 中写入 ``${last_crawl_time}`` ，它会被替换为上次爬取开始的时间：

::

    sql=SELECT id, title, content, url, updated_at FROM articles WHERE updated_at > '${last_crawl_time}'

首次运行时会被替换为 ``1970-01-01 00:00:00`` ，因此会获取全部记录。
读完整个结果集后，本次爬取的开始时间会作为 ``last_crawl_time`` 回写到数据存储配置中，
并在下次爬取时使用。

时间格式可通过 ``last_crawl_time_format`` 更改（默认值 ``yyyy-MM-dd HH:mm:ss``）。
请指定数据库能够作为时间戳字面量接受的格式。

基准时间是爬取的 **开始时间** 。爬取过程中被更新的行将在下次爬取时获取。
此外，如果爬取中途停止，则不会回写。

.. warning::
   增量抓取无法检测已删除的行。

   启用增量抓取后， |Fess| 从索引中删除"上次爬取未包含的文档"的处理
   （ ``delete_old_docs`` ）也会自动被禁用。如果不禁用，未发生变更的文档
   每次都会被全部删除。

   其结果是，数据库中已删除的行所对应的文档会一直保留在索引中，直到过期为止。
   请定期执行全量爬取（不包含 ``${last_crawl_time}`` 的配置）。

   若在数据存储配置中明确指定了 ``delete_old_docs`` ，则以其为准。

按ID指定范围等，像以往那样在 ``sql`` 中直接写入条件的方法也仍然可用：

::

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

.. warning::
   只有当 ``SELECT`` 的结果中存在标签为 ``url`` 的列时， ``url=url`` 才会按预期工作。
   若不存在对应的列，则同名的数据存储参数，即 **JDBC连接URL** 会被设置为文档的URL。
   若列名不同，请像 ``SELECT page_url AS url`` 那样指定别名，或像 ``url=page_url``
   那样在脚本中指定列名。

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

1. 利用自动加密

   与 ``app.encrypt.property.pattern`` （默认值 ``.*password|.*key|.*token|.*secret`` ）
   匹配的参数名，其值在从管理界面保存时会自动加密，并以 ``{cipher}`` 前缀保存。
   ``password`` 与该模式匹配，因此只要是从管理界面设置的，就不会以明文保存。

2. 使用环境变量

   以 ``FESS_ENV_`` 开头的环境变量，会在数据存储参数中以 ``${环境变量名}`` 的形式展开：

   ::

       password=${FESS_ENV_DB_PASSWORD}

   展开对象的环境变量名模式通过 ``crawler.data.env.param.key.pattern``
   （默认值 ``^FESS_ENV_.*`` ）设置。

3. 使用只读用户

.. note::
   即使将 ``org.codelibs.fess.ds`` 的日志级别设为DEBUG，密码等与
   ``app.encrypt.property.pattern`` 匹配的参数值，以及嵌入在JDBC连接URL中的认证信息，
   也会被掩码后输出。

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

爬取失败时，请先根据日志中的消息判断原因。

找不到JDBC驱动程序
------------------

**症状**：``The JDBC driver ... is not on the crawler classpath.``

**解决方法**：

1. 确认JDBC驱动程序是否放置在 ``app/WEB-INF/lib/`` 或 ``app/WEB-INF/env/crawler/lib/`` 中
2. 确认 ``driver`` 中指定的类名是否正确
3. 重启 |Fess|

连接错误
--------

**症状**：``Failed to connect to <URL>.``

**检查项**：

1. 数据库是否已启动
2. 主机名、端口号是否正确
3. 用户名、密码是否正确
4. 防火墙设置

查询错误
--------

**症状**：``Failed to execute the query.``

**检查项**：

1. 直接在数据库中执行SQL查询进行测试
2. 确认列名是否正确
3. 确认表名是否正确

参数缺失
--------

**症状**：``The driver parameter is required.`` 、 ``The url parameter is required.`` 、 ``The sql parameter is required.``

必填参数未设置。请确认参数栏。

仅部分行失败
------------

单行的失败不会中断爬取，而是记录到"系统"→"故障URL"中。
如果脚本已经生成了URL，则以该URL记录；如果在生成之前失败，则记录为
``datastore://<数据存储配置ID>/<行号>`` 。

文档未出现在搜索结果中
----------------------

1. 确认脚本中是否设置了 ``url`` 、 ``title`` 、 ``content``
2. 确认列标签的大小写是否与脚本一致（参见"脚本设置"）
3. 在爬取作业的日志中确认文档数

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-csv` - CSV连接器
- :doc:`ds-json` - JSON连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
- :doc:`../crawler-basic` - 爬虫基本配置
- :doc:`../search-basic` - 搜索功能
