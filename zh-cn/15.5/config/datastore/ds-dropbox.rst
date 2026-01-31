==================================
Dropbox连接器
==================================

概述
====

Dropbox连接器提供从Dropbox云存储获取文件并
注册到 |Fess| 索引的功能。

此功能需要 ``fess-ds-dropbox`` 插件。

支持的服务
============

- Dropbox（文件存储）
- Dropbox Paper（文档）

前提条件
========

1. 需要安装插件
2. 需要Dropbox开发者账户和应用程序创建
3. 需要获取访问令牌

插件安装
------------------------

从管理界面的"系统"→"插件"安装：

1. 从Maven Central下载 ``fess-ds-dropbox-X.X.X.jar``
2. 从插件管理界面上传并安装
3. 重启 |Fess|

或者，详情请参阅 :doc:`../../admin/plugin-guide`。

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
     - Company Dropbox
   * - 处理器名
     - DropboxDataStore 或 DropboxPaperDataStore
   * - 启用
     - 开

参数设置
----------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必须
     - 说明
   * - ``access_token``
     - 是
     - Dropbox的访问令牌（在App Console中生成）
   * - ``basic_plan``
     - 否
     - Basic计划时为 ``true``（默认：``false``）

脚本设置
--------------

Dropbox文件的情况
~~~~~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

可用字段：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``file.url``
     - 文件预览链接
   * - ``file.contents``
     - 文件的文本内容
   * - ``file.mimetype``
     - 文件的MIME类型
   * - ``file.filetype``
     - 文件类型
   * - ``file.name``
     - 文件名
   * - ``file.path_display``
     - 文件路径
   * - ``file.size``
     - 文件大小（字节）
   * - ``file.client_modified``
     - 客户端最后更新日期
   * - ``file.server_modified``
     - 服务器端最后更新日期
   * - ``file.roles``
     - 文件访问权限

Dropbox Paper的情况
~~~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Dropbox认证设置
=================

访问令牌获取步骤
--------------------------

1. 在Dropbox App Console创建应用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

访问 https://www.dropbox.com/developers/apps：

1. 点击"Create app"
2. 在API类型中选择"Scoped access"
3. 在访问类型中选择"Full Dropbox"或"App folder"
4. 输入应用名称并创建

2. 权限设置
~~~~~~~~~~~~~

在"Permissions"标签页选择所需权限：

**抓取文件所需的权限**：

- ``files.metadata.read`` - 读取文件元数据
- ``files.content.read`` - 读取文件内容
- ``sharing.read`` - 读取共享信息

**抓取Paper额外所需的权限**：

- ``files.content.read`` - 读取Paper文档

3. 生成访问令牌
~~~~~~~~~~~~~~~~~~~~~~~~~

在"Settings"标签页：

1. 滚动到"Generated access token"部分
2. 点击"Generate"按钮
3. 复制生成的令牌（此令牌只显示一次）

.. warning::
   请安全保管访问令牌。有了此令牌就可以访问Dropbox账户。

4. 设置令牌
~~~~~~~~~~~~~~~~~

将获取的令牌设置到参数中：

::

    access_token=sl.your-dropbox-token-here

Basic计划设置
=================

Dropbox Basic计划的限制
-------------------------

Dropbox Basic计划的API限制不同。
请将 ``basic_plan`` 参数设置为 ``true``：

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

这将进行对应API速率限制的处理。

使用示例
======

抓取整个Dropbox文件
------------------------------

参数：

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

脚本：

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

抓取Dropbox Paper文档
-----------------------------------

参数：

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

脚本：

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

故障排除
======================

认证错误
----------

**症状**：``Invalid access token`` 或 ``401 Unauthorized``

**检查项**：

1. 确认访问令牌是否正确复制
2. 确认令牌的有效期是否已过（使用长期令牌）
3. 确认在Dropbox App Console中是否授予了所需权限
4. 确认应用是否被禁用

无法获取文件
----------------------

**症状**：抓取成功但文件数为0

**检查项**：

1. 确认应用的"Access type"是否适当：

   - "Full Dropbox"：可访问整个Dropbox
   - "App folder"：只能访问特定文件夹

2. 确认是否授予了所需权限：

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. 确认Dropbox账户中是否存在文件

API速率限制错误
-------------------

**症状**：``429 Too Many Requests`` 错误

**解决方法**：

1. Basic计划时，设置 ``basic_plan=true``
2. 增加抓取间隔
3. 使用多个访问令牌进行负载均衡

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-box` - Box连接器
- :doc:`ds-gsuite` - Google Workspace连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
