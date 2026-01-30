==================================
Salesforce连接器
==================================

概述
====

Salesforce连接器提供从Salesforce对象（标准对象、自定义对象）获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-salesforce`` 插件。

支持的对象
================

- **标准对象**: Account、Contact、Lead、Opportunity、Case、Solution等
- **自定义对象**: 自己创建的对象
- **Knowledge文章**: Salesforce Knowledge

前提条件
========

1. 需要安装插件
2. 需要创建Salesforce Connected App（连接应用程序）
3. 需要设置OAuth认证
4. 需要对象的读取访问权限

插件安装
------------------------

从管理界面的「系统」→「插件」进行安装。

或者，详情请参阅 :doc:`../../admin/plugin-guide`。

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
     - Salesforce CRM
   * - 处理器名称
     - SalesforceDataStore
   * - 启用
     - 开

参数设置
----------------

OAuth Token认证（推荐）:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

OAuth Password认证:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``base_url``
     - 是
     - Salesforce的URL（生产: ``https://login.salesforce.com``，沙盒: ``https://test.salesforce.com``）
   * - ``auth_type``
     - 是
     - 认证类型（``oauth_token`` 或 ``oauth_password``）
   * - ``username``
     - 是
     - Salesforce用户名
   * - ``client_id``
     - 是
     - Connected App的Consumer Key
   * - ``private_key``
     - oauth_token时
     - 私钥（PEM格式，换行使用 ``\n``）
   * - ``client_secret``
     - oauth_password时
     - Connected App的Consumer Secret
   * - ``security_token``
     - oauth_password时
     - 用户的安全令牌
   * - ``number_of_threads``
     - 否
     - 并行处理线程数（默认: 1）
   * - ``ignoreError``
     - 否
     - 出错时继续处理（默认: true）
   * - ``custom``
     - 否
     - 自定义对象名（逗号分隔）
   * - ``<对象>.title``
     - 否
     - 用于标题的字段名
   * - ``<对象>.contents``
     - 否
     - 用于内容的字段名（逗号分隔）

脚本设置
--------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

可用字段
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``object.type``
     - 对象类型（例: Case、User、Solution）
   * - ``object.title``
     - 对象名称
   * - ``object.description``
     - 对象描述
   * - ``object.content``
     - 对象的文本内容
   * - ``object.id``
     - 对象ID
   * - ``object.content_length``
     - 内容长度
   * - ``object.created``
     - 创建时间
   * - ``object.last_modified``
     - 最后更新时间
   * - ``object.url``
     - 对象的URL
   * - ``object.thumbnail``
     - 缩略图URL

Salesforce Connected App设置
====================================

1. 创建Connected App
-----------------------------

在Salesforce Setup中:

1. 打开「应用程序管理器」
2. 点击「新建Connected App」
3. 输入基本信息:

   - Connected App名称: Fess Crawler
   - API名称: Fess_Crawler
   - 联系邮箱: your-email@example.com

4. 勾选「启用API（启用OAuth设置）」

2. OAuth Token认证设置（推荐）
--------------------------------

在OAuth设置中:

1. 勾选「使用数字签名」
2. 上传证书（按照下面的步骤创建）
3. 选择的OAuth范围:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. 点击「保存」
5. 复制Consumer Key

创建证书:

::

    # 生成私钥
    openssl genrsa -out private_key.pem 2048

    # 生成证书
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # 确认私钥
    cat private_key.pem

将证书（certificate.crt）上传到Salesforce，
将私钥（private_key.pem）的内容设置到参数。

3. OAuth Password认证设置
---------------------------

在OAuth设置中:

1. 回调URL: ``https://localhost`` （不会使用但必需）
2. 选择的OAuth范围:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. 点击「保存」
4. 复制Consumer Key和Consumer Secret

获取安全令牌:

1. 在Salesforce中打开个人设置
2. 点击「重置我的安全令牌」
3. 复制通过邮件发送的令牌

4. 授权Connected App
-----------------------------

在「管理」→「管理Connected App」中:

1. 选择创建的Connected App
2. 点击「编辑」
3. 将「允许的用户」更改为「管理员批准的用户已预先授权」
4. 分配配置文件或权限集

自定义对象设置
==========================

爬取自定义对象
------------------------------

在参数中使用 ``custom`` 指定自定义对象名:

::

    custom=FessObj,CustomProduct,ProjectTask

各对象的字段映射:

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

字段映射规则
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``<对象名>.title`` - 用于标题的字段（单个字段）
- ``<对象名>.contents`` - 用于内容的字段（可用逗号分隔指定多个）

使用示例
======

爬取标准对象
--------------------------

参数:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

脚本:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

爬取自定义对象
------------------------------

参数:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

脚本:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

爬取沙盒环境
---------------------

参数:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

脚本:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

故障排除
======================

认证错误
----------

**症状**: ``Authentication failed`` 或 ``invalid_grant``

**确认事项**:

1. OAuth Token认证时:

   - 确认Consumer Key是否正确
   - 确认私钥是否正确复制（换行是否为 ``\n``）
   - 确认证书是否已上传到Salesforce
   - 确认用户名是否正确

2. OAuth Password认证时:

   - 确认Consumer Key和Consumer Secret是否正确
   - 确认安全令牌是否正确
   - 确认是否没有将密码和安全令牌连接（需分别设置）

3. 通用:

   - 确认base_url是否正确（生产环境还是沙盒环境）
   - 确认Connected App是否已授权

无法获取对象
--------------------------

**症状**: 爬取成功但对象数为0

**确认事项**:

1. 确认用户是否有对象的读取权限
2. 自定义对象时，确认对象名是否正确（API名称）
3. 确认字段映射是否正确
4. 在日志中确认错误信息

自定义对象名称
--------------------------

确认自定义对象的API名称:

1. 在Salesforce Setup中打开「对象管理器」
2. 选择自定义对象
3. 复制「API名称」（通常以 ``__c`` 结尾）

示例:

- 显示标签: Product
- API名称: Product__c （使用这个）

确认字段名
------------------

确认自定义字段的API名称:

1. 打开对象的「字段和关系」
2. 选择自定义字段
3. 复制「字段名称」（通常以 ``__c`` 结尾）

示例:

- 字段显示标签: Product Description
- 字段名称: Product_Description__c （使用这个）

API速率限制
-------------

**症状**: ``REQUEST_LIMIT_EXCEEDED``

**解决方法**:

1. 减少 ``number_of_threads``（设置为1）
2. 增加爬取间隔
3. 确认Salesforce API使用情况
4. 如需要，购买额外的API限制

有大量数据的情况
----------------------

**症状**: 爬取耗时长或超时

**解决方法**:

1. 将对象分割到多个数据存储
2. 调整 ``number_of_threads``（2~4左右）
3. 分散爬取计划
4. 只映射必要的字段

私钥格式错误
--------------------------

**症状**: ``Invalid private key format``

**解决方法**:

确认私钥的换行是否正确为 ``\n``:

::

    # 正确格式
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 错误格式（包含实际换行）
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
