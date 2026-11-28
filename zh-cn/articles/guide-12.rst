======================================
搜索数据库、CSV 和 Salesforce 中的数据
======================================

前言
====

产品主数据存放在公司内部的数据库中，客户列表存放在核心业务系统每晚导出的 CSV 中，商机和咨询记录则存放在 Salesforce 中。
这类业务数据往往只能在各自系统的界面中查找。
使用 Fess 的数据存储插件，可以按记录导入这些数据，并在与文件服务器、内部网站文档相同的搜索页面中查找。

本文说明如何分别配置这 3 个信息源的导入，以及如何按信息源筛选、安排执行计划和确认结果。
插件的安装、处理程序名称·参数·脚本的写法、作业的创建等数据存储的通用步骤，已汇总在 :doc:`datastore-basics` 中。
请先阅读该文章再继续。
文中的设置值基于 Fess 15.9 和各插件的 15.9.0 版本。

本文要搭建的结构
================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - 信息源
     - 插件
     - 处理程序名称
     - 需要事先准备的内容
   * - 数据库（产品主数据）
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - JDBC 驱动程序的 jar 文件，以及只能执行 SELECT 的数据库用户
   * - CSV（客户列表）
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - 导出 CSV 的目录（爬虫可以读取的位置）
   * - Salesforce（客户、商机、个案）
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - Connected App，以及用于 JWT 签名的密钥对

如果使用 Docker 运行，请在 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 里，以空格分隔指定这 3 个插件。

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

如果通过管理界面或 ``fess-setup`` 安装，则需要重启 Fess。

首先要决定：搜索结果给谁看
==========================

这 3 个插件都不会把源系统的访问权限（ACL）带入 Fess。
导入文档的角色仅由数据存储配置中「权限」栏的值决定。
该栏一开始就填有 ``{role}guest``，保持原样的话，未登录的用户也能搜索到。

对于包含价格或客户信息的数据，请将该栏改为允许查看的组（例如 ``{group}sales``）。
从同一个配置注册的文档全部带有相同的权限。
面向不同对象的数据，请拆分到不同的数据存储配置中。
组的设计请参阅 :doc:`guide-05`。

数据库：导入产品主数据
======================

放置 JDBC 驱动程序
------------------

``fess-ds-db`` 不包含 JDBC 驱动程序。
请获取与所连接数据库相匹配的驱动程序 jar 文件（PostgreSQL 为 ``postgresql-<版本>.jar``，MySQL 为 ``mysql-connector-j-<版本>.jar``），并放到爬虫的类路径上。
数据存储的爬取在独立于 Fess 主体的爬虫进程中运行，其类路径包含以下 2 个目录中的 jar。

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

ZIP 包位于 Fess 解压目录下，RPM / DEB 则位于 ``/usr/share/fess/`` 下。
放置后重启 Fess。

在 Docker 镜像中，Fess 同样位于 ``/usr/share/fess/``。
复制到容器内的 jar 会在重新创建容器时消失，因此请只将这一个 jar 文件挂载到 ``compose.yaml`` 的 ``fess01`` 中。

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

如果挂载整个目录，镜像放在该目录中的 jar 将不可见，爬虫也就无法启动。
请务必按文件挂载。
修改后，使用 ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d`` 重新创建容器。

参数与 SQL
----------

这里以 PostgreSQL 的 ``products`` 表为例。
搜索结果的链接目标使用产品主数据的查询界面（例如 ``https://erp.example.com/products/<产品ID>``）。
在 [爬虫] > [数据存储] > [新建] 中，处理程序名称选择 ``DatabaseDataStore``，并按如下方式填写参数。

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

脚本如下。

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

``sql`` 要写在一行中。
SQL 会原样发送给数据库，结果中的 1 行就是 1 个文档。
如果在 SQL 中拼好链接目标 URL 和正文，脚本中只需写列名即可。
``concat_ws`` 在拼接时会跳过 NULL 列，因此即使是说明为空的产品，正文也不会变成 NULL。
在 MySQL 中 ``CONCAT_WS`` 的行为相同，但 ``CONCAT`` 只要参数中有 NULL，整个结果就会变成 NULL。

如果使用 Docker 运行，``url`` 中的 ``localhost`` 指的不是数据库服务器，而是 Fess 容器本身。
请填写数据库的主机名或 IP 地址。

列名与脚本的对应关系
--------------------

脚本的右侧直接写 SELECT 结果的列标签（用 ``AS`` 起的别名）。
请注意以下 3 点。

- 列标签的大小写因数据库而异。对于未加引号的别名，PostgreSQL 会转为小写，Oracle 和 H2 会转为大写，MySQL 则按原样返回。脚本中要按数据库返回的大小写书写。不一致时，该字段不会被赋值
- 在脚本中，参数栏的值也会作为同名变量可见。如果结果中没有 ``url`` 列却写了 ``url=url``，JDBC 的连接 URL 就会成为文档的 URL。请为链接目标列起一个不与参数重名的名称，例如 ``page_url``
- 卡住的查询即使停止作业也不会停止。请务必设置 ``query_timeout``\ （秒）

``fess-ds-db`` 没有增量爬取的选项。
每次运行都会执行整个 ``sql``，并重新注册所有行。
对于行数较多的表，请在数据库负载较低的时间段运行作业（参见后面的“按信息源创建作业”）。

CSV：导入核心业务系统导出的客户列表
===================================

CSV 连接器的基本用法，在 :doc:`datastore-basics` 中 CSV 文件示例的一节里有说明。
这里只补充导入核心业务系统定期导出的 CSV 时需要注意的地方。

举例来说，假设一个日本的核心业务系统每晚 2:00 导出如下的 ``customers_20261128.csv``。
字符编码为 MS932（Windows 版的 Shift_JIS），第 1 行是日文标题（客户代码、客户名称、所在地、负责部门、交易状态）。

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

文件的存放位置
--------------

请将 CSV 导出到 Fess 爬虫所在服务器可以读取的路径。
在 Docker 中，将导出目录以只读方式挂载到 ``fess01``。

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

参数与脚本
----------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- 指定 ``directories`` 后，会按修改时间从旧到新的顺序读取该目录中所有扩展名为 ``.csv`` / ``.tsv`` 的文件。即使每天以带日期的文件名导出，也无需修改参数。如果保留旧文件，这些文件中的行也会每次都被读取
- 日文版 Excel 或面向日文 Windows 的系统导出的 CSV 大多是 MS932。如果指定 ``Shift_JIS``，``①`` 和 ``㈱`` 之类的字符会变成替换字符，因此请指定 ``MS932``
- 即使像本例这样标题是日文等非 ASCII 字符，也可以用 ``has_header_line=true`` 跳过第 1 行。在脚本中按列号（``cell1``、``cell2`` …）引用最为可靠。标题中含有空格或符号的列无法通过标题名引用
- 制表符分隔的文件需要添加 ``separator_character=\t``
- ``url`` 为 ``null`` 的行不会被注册。本例中排除了状态为“取引終了”（交易结束）的客户，只注册状态为“取引中”（交易中）的客户。排除的行数会以 WARN 的形式输出到 ``fess-crawler.log``：``Skipped 1 row(s) in ... because the script did not set the url field.``

如果读取了正在导出中的文件，则只会注册到当时为止已写入的行。
请在 CSV 导出完成的时刻之后运行作业。

Salesforce：导入客户、商机和个案
================================

Salesforce 端的准备
-------------------

``fess-ds-salesforce`` 支持 ``auth_type=oauth_token``\ （JWT 持有者流程）和 ``auth_type=oauth_password``\ （用户名和密码）2 种认证方式。
这里使用无需保存密码的 ``oauth_token``。
``oauth_password`` 所用的用户名密码 OAuth 流程，可能会因 Salesforce 组织的设置而被禁用。

1. 创建密钥对和证书

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. 在 Salesforce Setup 中创建 Connected App，启用 OAuth 设置，并在「使用数字签名」中上传 ``certificate.crt``。OAuth 范围按参考文档的说明选择
3. 在 Connected App 的策略中，将「允许的用户」设为「管理员批准的用户已预先授权」，并分配用于爬取的用户的配置文件或权限集
4. 记下 Connected App 的 Consumer Key

Salesforce 端的界面和名称可能会变化，详情也请参阅 Salesforce 帮助中关于 JWT 持有者流程的说明。

Fess 能导入的，只有用于爬取的用户能够读取的记录和字段。
如果在后述的 ``contents`` 中指定了无法读取的字段，该对象的获取就会失败。

参数与脚本
----------

``private_key`` 中填写 ``private_key.pem`` 的内容，将换行替换为 ``\n``，写成一行。
插件只能读取 PKCS#8 格式（以 ``-----BEGIN PRIVATE KEY-----`` 开头的格式）。
用旧版 OpenSSL 生成的、以 ``-----BEGIN RSA PRIVATE KEY-----`` 开头的密钥，请先用 ``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem`` 转换后再使用。

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

以 Sandbox 为对象时，设置 ``base_url=https://test.salesforce.com``。

右侧的项目全部以 ``object.`` 开头。
如果像 ``url=url`` 这样不加前缀，表达式的求值会失败，记录不会被注册，而是记录到失败URL 中。
``object.url`` 的格式为 ``<实例 URL>/<记录 ID>``，点击后会打开 Salesforce 的记录页面。

缩小导入范围
------------

``fess-ds-salesforce`` 总是读取全部 23 种标准对象，包括 Account、Contact、Lead、Opportunity、Case、Task、User 等。
没有选择性读取对象的设置。
要缩小范围，请组合使用以下 3 种方式。

- ``include_pattern`` / ``exclude_pattern``：与整个 ``object.url`` 匹配的正则表达式，用于选择要注册的记录。Salesforce 记录 ID 的前 3 个字符按对象固定（Account ``001``、Opportunity ``006``、Case ``500`` 等）。上面的示例只注册这 3 种。获取本身仍针对所有对象进行，只是在注册前被丢弃
- ``<对象名>.title`` / ``<对象名>.contents``：用字段的 API 名称指定用于标题和正文的字段。标准对象的名称是 ``ACCOUNT``、``OPPORTUNITY``、``CASE`` 这样的大写蛇形命名。未指定时使用插件的默认字段
- ``custom``：以逗号分隔指定自定义对象的 API 名称，即可在标准对象之外一并读取

自定义对象没有默认字段，因此请务必指定 ``.title`` 和 ``.contents``。
标题字段也请包含在正文字段中。
插件只获取写在 ``.contents`` 等中的字段，因此只写在 ``.title`` 中的字段不会被获取，标题会为空。

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

用标签按信息源筛选
==================

在前面的示例中，通过脚本的 ``label`` 分别加上了 ``products``、``customers``、``salesforce``。
要让它们显示在搜索页面的标签选项中，请在 [爬虫] > [标签] 中创建「值」相同的标签（「包含的路径」可以留空）。
标签的值只能使用字母、数字和 ``_``。

如果想按对象区分 Salesforce 的数据，请不使用脚本的 ``label``，而是创建通过「包含的路径」查看记录 ID 前 3 个字符的标签。
例如，值为 ``sf_case``、包含的路径为 ``https://example\.my\.salesforce\.com/500.*`` 的标签只会加到个案上。
如果有与 URL 匹配的标签，脚本加上的标签就会丢失。
在一个数据存储配置中，请只使用其中一种方法（详情参见 :doc:`datastore-basics` 中关于标签的一节）。

按信息源创建作业
================

初始状态下的「Default Crawler」每天 0:00 会一并爬取所有配置。
各信息源合适的时间各不相同，因此请为每个数据存储配置创建作业。
在各配置的详情页面中点击 [创建新作业]，在「计划」中以 cron 格式填写时间（步骤参见 :doc:`datastore-basics` 中关于计划的一节）。

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 信息源
     - 计划示例
     - 考虑事项
   * - 数据库
     - ``0 3 * * *``
     - 每次都读取全部行，因此安排在数据库负载较低的时间段
   * - CSV
     - ``30 2 * * *``
     - 安排在导出完成的时刻之后
   * - Salesforce
     - ``0 7,12,18 * * *``
     - 每运行 1 次，就会按标准对象和自定义对象的数量创建 Bulk API 作业。请根据组织 API 限制的剩余量决定次数

Default Crawler 也会继续爬取这些配置。
如果不想重复运行，请将数据存储配置的「状态」设为「禁用」（指定了配置 ID 的作业也会爬取已禁用的配置）。

从源数据中消失的行如何处理
==========================

即使删除了数据库中的行，或 CSV 中的行不见了，对应的文档也不会在下次爬取时被删除。
通过数据存储注册的文档带有有效期，每次注册时有效期都会延长。
不再被注册的文档，在最后一次注册后经过 [系统] > [通用] 中「删除以前的文档」的天数（默认 3 天）后，会被自动删除。

这一机制也有需要注意的一面。
如果数据库连续多天无法连接，超过了这一天数，该配置的文档会全部从搜索结果中消失。
请用下一节的方法尽早发现导入失败。

确认运行情况
============

作业日志、[系统信息] > [爬网信息]、失败URL 和 ``fess-crawler.log`` 的查看方法，在 :doc:`datastore-basics` 中关于确认结果的一节里有说明。
数据存储爬取即使导入失败，作业也可能显示为“OK”，因此请根据件数和日志来判断。

1. 在 [系统信息] > [搜索] 中搜索 ``label:products``、``label:customers``、``label:salesforce``，并将件数与源数据进行比较（数据库的话，使用与 ``sql`` 条件相同的 ``SELECT count(*)``）
2. 确认 ``fess-crawler.log`` 中的 WARN 和 ERROR。在本文的结构中，容易出现的是以下消息

   - ``The JDBC driver ... is not on the crawler classpath.``：驱动程序的位置或 ``driver`` 的类名有误
   - ``Failed to connect to ...``：请确认数据库的主机名、端口、用户名和密码
   - ``is not a directory.`` 或 ``No CSV file.``：``directories`` 路径中没有爬虫可读取的 CSV
   - ``Batch:... Failed caused by ...``：未能获取 Salesforce 的部分对象。请确认 ``.contents`` 中的字段名，以及用于爬取的用户对字段的权限
   - ``Failed to process a data crawling: <配置名>``：整个配置失败。在 Salesforce 中，认证失败属于这种情况。请通过随后的堆栈跟踪确认原因

3. 对于修改过「权限」栏的配置，请以目标组的用户登录，确认文档会出现在搜索结果中，并确认在注销状态下不会出现

总结
====

- 3 个插件都不会带入源系统的权限，因此请将「权限」栏中的 ``{role}guest`` 改为允许查看的组
- 数据库需要将 JDBC 驱动程序放到爬虫的类路径上，并在 SQL 中拼好链接目标 URL 和正文。每次都会读取全部行
- 核心业务系统的 CSV 用 ``directories`` 和 ``file_encoding=MS932`` 读取，用 ``cellN`` 引用。``url`` 设为 ``null`` 的行不会被注册
- Salesforce 的脚本用 ``object.*`` 编写。标准对象无法选择，因此用 ``include_pattern`` 和 ``<对象名>.contents`` 缩小范围
- 按信息源创建作业，并以“从源数据中消失的行会在「删除以前的文档」的天数后消失”为前提进行运维

接下来阅读
==========

- 数据存储的通用机制（脚本、权限、标签、确认结果的方法）：:doc:`datastore-basics`
- 想要导入 Git、Confluence、Jira、Slack：:doc:`guide-06`
- 想要导入 Google Drive、SharePoint、Box：:doc:`guide-07`
- 想要按部门显示不同的搜索结果：:doc:`guide-05`
- 想要监控导入失败：:doc:`guide-10`

参考资料
========

- `数据库连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-database.html>`__
- `CSV 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-csv.html>`__
- `Salesforce 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-salesforce.html>`__
- `数据存储配置 <https://fess.codelibs.org/zh-cn/stable/admin/dataconfig-guide.html>`__
- `调度器 <https://fess.codelibs.org/zh-cn/stable/admin/scheduler-guide.html>`__
- `标签 <https://fess.codelibs.org/zh-cn/stable/admin/labeltype-guide.html>`__
- `通用 <https://fess.codelibs.org/zh-cn/stable/admin/general-guide.html>`__
