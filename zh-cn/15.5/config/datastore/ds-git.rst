==================================
Git连接器
==================================

概述
====

Git连接器提供从Git仓库获取文件并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-git`` 插件。

支持的仓库
==============

- GitHub（公共/私有）
- GitLab（公共/私有）
- Bitbucket（公共/私有）
- 本地Git仓库
- 其他Git托管服务

前提条件
========

1. 需要安装插件
2. 私有仓库需要认证信息
3. 需要仓库的读取访问权限

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
     - Project Git Repository
   * - 处理器名称
     - GitDataStore
   * - 启用
     - 开

参数设置
----------------

公共仓库示例:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=
    delete_old_docs=false

私有仓库示例（带认证）:

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=
    delete_old_docs=false

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``uri``
     - 是
     - Git仓库URI（用于clone）
   * - ``base_url``
     - 是
     - 文件显示用的基础URL
   * - ``extractors``
     - 否
     - 按MIME类型的提取器设置
   * - ``prev_commit_id``
     - 否
     - 上次提交ID（用于增量爬取）
   * - ``delete_old_docs``
     - 否
     - 从索引中删除已删除的文件（默认: ``false``）

脚本设置
--------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

可用字段
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``url``
     - 文件的URL
   * - ``path``
     - 仓库内的文件路径
   * - ``name``
     - 文件名
   * - ``content``
     - 文件的文本内容
   * - ``contentLength``
     - 内容长度
   * - ``timestamp``
     - 最后更新时间
   * - ``mimetype``
     - 文件的MIME类型
   * - ``author``
     - 最后提交者信息

Git仓库认证
===================

GitHub Personal Access Token
-----------------------------

1. 在GitHub生成Personal Access Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

访问 https://github.com/settings/tokens:

1. 点击「Generate new token」→「Generate new token (classic)」
2. 输入令牌名称（例: Fess Crawler）
3. 在范围中勾选「repo」
4. 点击「Generate token」
5. 复制生成的令牌

2. 在URI中包含认证信息
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git

GitLab Private Token
--------------------

1. 在GitLab生成Access Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GitLab的User Settings → Access Tokens:

1. 输入令牌名称
2. 在范围中勾选「read_repository」
3. 点击「Create personal access token」
4. 复制生成的令牌

2. 在URI中包含认证信息
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:glpat-abc123def456@gitlab.com/company/repo.git

SSH认证
-------

使用SSH密钥的情况:

::

    uri=git@github.com:company/repo.git

.. note::
   使用SSH认证时，需要设置运行 |Fess| 的用户的SSH密钥。

提取器设置
============

按MIME类型的提取器
--------------------

使用 ``extractors`` 参数指定按文件类型的提取器:

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

格式: ``<MIME类型正则表达式>:<提取器名>,``

默认提取器
~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - 用于文本文件
- ``tikaExtractor`` - 用于二进制文件（PDF、Word等）

只爬取文本文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

爬取所有文件
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

只爬取特定文件类型
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # 只爬取Markdown、YAML、JSON
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

增量爬取
============

只爬取上次提交以来的变更
------------------------------------

初次爬取后，将上次的提交ID设置到 ``prev_commit_id``:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    delete_old_docs=true

.. note::
   提交ID设置为最后一次爬取时的提交ID。
   这样只会爬取该提交之后的变更。

已删除文件的处理
------------------------

设置 ``delete_old_docs=true`` 时，从Git仓库删除的文件
也会从索引中删除。

使用示例
======

GitHub公共仓库
--------------------------

参数:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    delete_old_docs=false

脚本:

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

GitHub私有仓库
----------------------------

参数:

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    delete_old_docs=false

脚本:

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab（自托管）
----------------------

参数:

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=
    delete_old_docs=false

脚本:

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

只爬取文档（Markdown文件）
--------------------------------------------

参数:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,
    delete_old_docs=false

脚本:

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

只爬取特定目录
------------------------------

使用脚本过滤:

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

故障排除
======================

认证错误
----------

**症状**: ``Authentication failed`` 或 ``Not authorized``

**确认事项**:

1. 确认Personal Access Token是否正确
2. 确认令牌是否有适当的权限（``repo`` 范围）
3. 确认URI格式是否正确:

   ::

       # 正确
       uri=https://username:token@github.com/company/repo.git

       # 错误
       uri=https://github.com/company/repo.git?token=...

4. 确认令牌的有效期

找不到仓库
------------------------

**症状**: ``Repository not found``

**确认事项**:

1. 确认仓库URL是否正确
2. 确认仓库是否存在且未被删除
3. 确认认证信息是否正确
4. 确认是否有仓库访问权限

无法获取文件
----------------------

**症状**: 爬取成功但文件数为0

**确认事项**:

1. 确认 ``extractors`` 设置是否适当
2. 确认仓库中是否存在文件
3. 确认脚本设置是否正确
4. 确认目标分支中是否存在文件

MIME类型错误
----------------

**症状**: 特定文件未被爬取

**解决方法**:

调整提取器设置:

::

    # 爬取所有文件
    extractors=.*:tikaExtractor,

    # 添加特定MIME类型
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

大型仓库
----------------

**症状**: 爬取耗时长或内存不足

**解决方法**:

1. 使用 ``extractors`` 限制目标文件
2. 使用脚本只过滤特定目录
3. 使用增量爬取（设置 ``prev_commit_id``）
4. 调整爬取间隔

分支指定
--------------

爬取非默认分支的情况:

::

    uri=https://github.com/company/repo.git#develop
    base_url=https://github.com/company/repo/blob/develop/

在 ``#`` 后指定分支名。

URL生成
=========

base_url设置模式
----------------------

**GitHub**:

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab**:

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket**:

::

    base_url=https://bitbucket.org/user/repo/src/master/

``base_url`` 和文件路径组合生成URL。

在脚本中生成URL
---------------------

::

    url=base_url + path
    title=name
    content=content

或者，自定义URL:

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
