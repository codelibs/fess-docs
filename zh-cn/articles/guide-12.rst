============================================================
第12回：让 SaaS 数据可搜索 -- Salesforce 与数据库的集成场景
============================================================

前言
====

企业的重要数据不仅存储在文件服务器和云存储中，还存储在 SaaS 应用程序和数据库中。
Salesforce 中的客户信息、内部数据库中的产品主数据、以 CSV 管理的列表数据——这些数据通常只能在各自的系统内进行搜索。

本文介绍将 SaaS 和数据库的数据导入 Fess 索引，使其能够与其他文档一起进行跨源搜索的场景。

目标读者
========

- 希望将 SaaS 和数据库信息纳入搜索范围的人员
- 希望了解数据存储插件使用方法的人员
- 希望构建跨越多个数据源的搜索平台的人员

场景
====

某销售组织的数据分散在以下系统中。

.. list-table:: 数据源现状
   :header-rows: 1
   :widths: 20 35 45

   * - 系统
     - 存储数据
     - 当前问题
   * - Salesforce
     - 客户信息、商机记录、活动历史
     - 只能在 Salesforce 内搜索
   * - 内部数据库
     - 产品主数据、价格表、库存信息
     - 只能通过专用管理界面访问
   * - CSV 文件
     - 客户列表、活动参与者列表
     - 只能用 Excel 打开后目视查找
   * - 文件服务器
     - 提案书、报价单、合同
     - 已由 Fess 完成爬取

目标是通过 Fess 对所有这些数据进行跨源搜索，使销售活动所需的信息能够从一个搜索框中找到。

Salesforce 数据集成
=====================

要使 Salesforce 数据在 Fess 中可搜索，请使用 Salesforce 数据存储插件。

插件安装
--------

1. 在管理界面中选择 [系统] > [插件]
2. 安装 ``fess-ds-salesforce``

连接设置
--------

与 Salesforce 的集成需要配置 Connected App。

**Salesforce 端准备**

1. 在 Salesforce 设置界面中创建 Connected App
2. 启用 OAuth 设置
3. 获取消费者密钥和密钥

**Fess 端设置**

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称：选择 SalesforceDataStore
3. 配置参数和脚本
4. 标签：设置 ``salesforce``

**参数配置示例**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**脚本配置示例**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

``auth_type`` 指定 ``oauth_password``（用户名/密码认证）或 ``oauth_token``（JWT Bearer 令牌认证）。使用 JWT 认证时，在 ``private_key`` 中设置 RSA 私钥。

目标数据选定
------------

Salesforce 中包含许多对象，但并非所有对象都需要纳入搜索范围。
应集中在销售团队频繁搜索的对象上。

.. list-table:: 目标对象示例
   :header-rows: 1
   :widths: 25 35 40

   * - 对象
     - 搜索目标字段
     - 用途
   * - Account（客户）
     - 名称、行业、地址、描述
     - 搜索客户基本信息
   * - Opportunity（商机）
     - 名称、阶段、描述、金额
     - 搜索进行中的商机
   * - Case（案例）
     - 主题、描述、状态
     - 搜索咨询历史

数据库集成
==========

要使内部数据库的数据可搜索，请使用数据库数据存储插件。

插件安装
--------

安装 ``fess-ds-db`` 插件。
该插件可以通过 JDBC 连接到各种数据库（MySQL、PostgreSQL、Oracle、SQL Server 等）。

设置
----

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称：选择 DatabaseDataStore
3. 配置参数和脚本
4. 标签：设置 ``database``

**参数配置示例**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**脚本配置示例**

.. code-block:: properties

    url=url
    title=product_name
    content=description

``sql`` 中指定的 SQL 查询结果将被爬取。在脚本中使用 SQL 列名（或列标签）映射到 Fess 索引字段。

SQL 查询设计
------------

设计 ``sql`` 参数中的 SQL 查询时的要点如下。

- 包含作为搜索结果链接目标的 ``url`` 列（例如：``CONCAT('https://.../', id) AS url``）
- 包含作为搜索正文的列
- 使用 ``WHERE`` 子句排除不需要的数据（例如：``status = 'active'``）

在脚本中直接使用 SQL 列名映射到 Fess 索引字段。

CSV 文件集成
=============

CSV 文件的数据也可以纳入搜索范围。

设置
----

使用 ``fess-ds-csv`` 插件或 CSV 数据存储功能。

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称：选择 CsvDataStore
3. 配置参数和脚本
4. 标签：设置 ``csv-data``

**参数配置示例**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**脚本配置示例** （有标题行时使用列名）

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

当 ``has_header_line=true`` 时，可以在脚本中使用标题行的列名。没有标题行时，使用 ``cell1``、``cell2``、``cell3`` 等列编号进行引用。脚本可以编写 Groovy 表达式，支持字符串拼接等操作。

如果 CSV 文件定期更新，固定文件的存放位置并设置爬取计划，最新数据将自动反映到索引中。

数据源跨源搜索
================

所有数据源配置完成后，即可体验跨源搜索。

搜索示例
--------

搜索"ABC 股份有限公司"时，将返回以下结果：

1. Salesforce 客户信息（Account）
2. 文件服务器的提案书（PDF）
3. 数据库的产品购买记录
4. CSV 的展会参与者列表

用户无需关心信息的存储位置，即可找到所需信息。

按标签筛选
----------

当搜索结果较多时，可以通过标签进行筛选。

- ``salesforce``：仅 Salesforce 数据
- ``database``：仅数据库数据
- ``csv-data``：仅 CSV 数据
- ``共享文件``：仅文件服务器文档

运维注意事项
============

数据新鲜度
----------

SaaS 和数据库的数据可能会频繁更新。
请适当设置爬取频率，以保持搜索结果的新鲜度。

.. list-table:: 爬取频率参考
   :header-rows: 1
   :widths: 25 25 50

   * - 数据源
     - 推荐频率
     - 原因
   * - Salesforce
     - 每 4~6 小时
     - 商机和客户信息在工作时间内更新
   * - 数据库
     - 每 2~4 小时
     - 库存信息等变动较大的数据
   * - CSV
     - 每天一次
     - 通常通过批处理更新

数据库连接安全
--------------

直接连接数据库时，请充分注意安全性。

- 使用只读数据库用户
- 将连接来源限制为 Fess 服务器的 IP 地址
- 不授予对不必要表的访问权限
- 注意密码管理

总结
====

本文介绍了使 Salesforce、数据库和 CSV 文件的数据在 Fess 中可搜索的场景。

- 通过 Salesforce 数据存储插件实现 CRM 数据集成
- 通过数据库数据存储插件实现内部数据库集成
- 通过 CSV 数据存储实现列表数据集成
- 字段映射与 SQL 查询设计
- 跨源搜索中的标签活用

消除数据孤岛，实现所有信息源可从单一平台搜索的环境。
实践解决方案篇到此结束。从下一回开始，将进入架构与扩展篇，首先介绍多租户设计。

参考资料
========

- `Fess 数据存储设置 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess 插件管理 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
