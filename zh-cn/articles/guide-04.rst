========================
统一搜索网站和文件服务器
========================

前言
====

企业内部的资料往往分散在门户网站、各部门的共享文件夹、存放旧资料的归档目录等多个地方。
查找资料的人需要先想起资料在哪里，再到各个地方分别查找。

本文使用 Fess 15.9 爬取以下 3 个位置，让用户可以通过一个搜索框进行查找。
在搜索页面上，还可以使用标签将结果筛选为“仅门户”“仅共享文件夹”等。

- 内部门户（网站）
- Windows 文件服务器上的共享文件夹（SMB）
- 服务器上的归档目录（本地文件）

操作步骤以 :doc:`guide-02` 中启动的 Docker 环境（``fess01`` 和 ``search01``）为前提。
Google Drive、SharePoint、Box 等云存储将在 :doc:`guide-07` 中介绍。
引入文件服务器搜索之前需要确认的事项汇总在 :doc:`file-server-search` 中。

本文搭建的配置
==============

.. list-table::
   :header-rows: 1
   :widths: 18 40 14 28

   * - 对象
     - 爬取的路径
     - 标签的值
     - 爬取的执行时间
   * - 内部门户
     - ``https://portal.example.com/``
     - ``portal``
     - 每天 2:00
   * - 共享文件夹
     - ``smb://fileserver.example.com/shared/``
     - ``shared``
     - 每天 3:00
   * - 归档
     - ``file:/data/archive/``\ （主机上的 ``/srv/archive``）
     - ``archive``
     - 每周日 4:00

主机名和目录均为示例。
请根据自己的环境替换。
前提是有一个可以读取共享文件夹的服务账号（只读权限即可），并且 ``fess01`` 容器能够连接到文件服务器的 SMB 端口（445）。

标签是在爬取时添加的，因此要先于爬网配置创建。
请按照本文各节标题的顺序进行操作。

让容器能读取归档目录
====================

在 docker-fess v15.9.0 的 ``compose.yaml`` 中，``fess01`` 没有定义卷。
因此，主机上的 ``/srv/archive`` 默认无法在容器内看到。
在 ``compose.yaml`` 的 ``fess01`` 中添加 ``volumes``，同时在 ``environment`` 中加入 ``FESS_JAVA_OPTS`` 这一行。

.. code-block:: yaml

    services:
      fess01:
        image: ghcr.io/codelibs/fess:15.9.0
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_JAVA_OPTS=-Duser.timezone=Asia/Tokyo -Dfess.system.day.for.cleanup=10"
        volumes:
          - /srv/archive:/data/archive:ro
        # ports 及之后的内容保持不变

- ``/srv/archive:/data/archive:ro`` 将主机上的 ``/srv/archive`` 以只读方式挂载到容器的 ``/data/archive``
- ``-Duser.timezone=Asia/Tokyo`` 用于让后面设置的作业执行时间按日本时间处理。compose.yaml 和镜像中都没有指定时区，如果不指定，作业会在与日本时间错开的时刻运行
- ``-Dfess.system.day.for.cleanup=10`` 将文档有效期（天数）的默认值设为 10 天。原因将在后面的“每周一次的作业与文档有效期”中说明

修改后，重新创建容器。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

由于 ``fess01`` 会被重新创建，此前在 [系统] > [通用] 中修改的设置会丢失（参见 :doc:`guide-02` 的“停止与重启”）。
需要修改 [通用] 的操作，请在此步骤之后进行。

容器内的 Fess 以用户 ``fess``\ （UID 1001）运行。
确认该用户能够看到文件列表。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -u fess fess01 ls /data/archive

如果出现 ``Permission denied``，请让 UID 1001 能够读取主机上 ``/srv/archive`` 下的内容（例如，为其他用户授予读取权限，并为目录授予执行权限）。

创建标签
========

当文档的 URL 与正则表达式匹配时，就会添加标签。
爬网配置页面中没有选择标签的项目（默认不显示），因此需要在标签一侧的「包含的路径」中指定添加标签的范围。

在 [爬虫] > [标签] > [新建] 中创建以下 3 个标签。

.. list-table::
   :header-rows: 1
   :widths: 18 14 68

   * - 名称
     - 值
     - 包含的路径
   * - 门户
     - ``portal``
     - ``https://portal.example.com/.*``
   * - 共享文件夹
     - ``shared``
     - ``smb://fileserver.example.com/shared/.*``
   * - 归档
     - ``archive``
     - ``file:/data/archive/.*``

- 「名称」是显示在搜索页面上的字符串，可以使用中文等非 ASCII 字符
- 「值」只能使用字母、数字和下划线（使用连字符或中文等非 ASCII 字符会导致输入错误）
- 「包含的路径」需要与整个 URL 匹配，因此不要省略末尾的 ``.*``。如果留空，该标签不会添加到任何文档上
- 「权限」中已填入 ``{role}guest``。这样未登录的用户也能看到该标签，保持原样即可

在创建标签之前爬取的文档没有标签。
如果之后添加或修改了标签，可以重新爬取，或者在 [系统] > [调度器] 中用 [立即开始] 运行「Label Updater」，将标签应用到现有文档。

创建爬网配置
============

内部门户（Web 爬网）
--------------------

在 [爬虫] > [Web] > [新建] 中输入以下项目，然后点击 [创建]。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 项目
     - 值
   * - 名称
     - ``内部门户``
   * - URL
     - ``https://portal.example.com/``
   * - 要包含在爬网中的URL
     - ``https://portal.example.com/.*``
   * - 要从爬网中排除的URL
     - 在已有的行下方添加 ``https://portal.example.com/admin/.*``

「要从爬网中排除的URL」中预先填入了排除图片、CSS 等的正则表达式。
请不要删除，而是添加新行。
「线程数」的初始值为 ``1``，「间隔」为 ``10000`` 毫秒，这是控制门户负载的设置。

共享文件夹（SMB）与文件认证
---------------------------

首先，在 [爬虫] > [文件系统] > [新建] 中创建以下配置。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 项目
     - 值
   * - 名称
     - ``共享文件夹``
   * - 路径
     - ``smb://fileserver.example.com/shared/``
   * - 要包含在爬网中的路径
     - ``smb://fileserver.example.com/shared/.*``
   * - 要从爬网中排除的路径
     - ``.*\.tmp$``

文件爬网的初始值：「线程数」为 ``5``，「间隔」为 ``1000`` 毫秒。

接着，将服务账号关联到该配置。
文件认证是通过选择文件爬网配置来创建的。
在还没有任何文件爬网配置时，[文件认证] 页面上不会显示 [新建]。

在 [爬虫] > [文件认证] > [新建] 中输入以下项目，然后点击 [创建]。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 项目
     - 值
   * - 主机名
     - ``fileserver.example.com``\ （与路径中主机名的写法相同）
   * - 端口
     - 留空
   * - 方案
     - ``Samba``
   * - 用户名 / 密码
     - 服务账号的用户名和密码
   * - 参数
     - 如果是域账号，按 ``domain=EXAMPLE`` 的形式指定域名
   * - 文件爬网配置
     - ``共享文件夹``

「主机名」必须与路径中的主机名逐字一致。
如果路径中使用的是 IP 地址，这里也要填写 IP 地址。
「端口」留空的认证，会用于 ``smb://主机名/共享名/`` 这样未写端口的路径。

.. note::

   通过 SMB 爬取的文件，默认会带有根据文件访问权限（ACL）生成的角色，并添加到爬网配置的「权限」中。
   只要「权限」中还保留初始值 ``{role}guest``，包括未登录用户在内的所有人都可以搜索到这些文件。
   如果要根据访问权限区分显示搜索结果，请参阅 :doc:`file-server-search` 和 :doc:`guide-05`。

归档（本地文件）
----------------

在 [爬虫] > [文件系统] > [新建] 中创建以下配置。
路径使用容器内的路径来指定。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 项目
     - 值
   * - 名称
     - ``归档``
   * - 路径
     - ``file:/data/archive/``
   * - 要包含在爬网中的路径
     - ``file:/data/archive/.*``
   * - 要从爬网中排除的路径
     - ``.*\.(log|bak)$``

本地文件按 ``file:/data/archive/`` 的形式书写，即 ``file:`` 后面只跟一个斜杠。
爬虫找到的文件 URL 形如 ``file:/data/archive/2020/report.pdf``，「要包含在爬网中的路径」会与这个 URL 进行匹配。
如果写成 ``file:///data/archive/.*``，将不会匹配任何文件，一个文档也不会被注册。

为每个配置创建作业
==================

调度器中的「Default Crawler」会在每天 0:00 一并执行所有已启用的爬网配置。
如果要为每个对象设置不同的执行时间，就需要为每个爬网配置分别创建作业。

1. 在 [爬虫] > [Web] 中点击「内部门户」，然后在详情页面点击 [创建新作业]
2. 作业创建页面打开后，「名称」中已填入 ``Web Crawler - 内部门户``，「脚本」中已填入只爬取该配置的内容
3. 「计划」为空，输入 cron 表达式后点击 [创建]
4. 对 [爬虫] > [文件系统] 中的「共享文件夹」和「归档」执行同样的操作（名称类似 ``File Crawler - 共享文件夹``）

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - 作业
     - 计划
     - 含义
   * - ``Web Crawler - 内部门户``
     - ``0 2 * * *``
     - 每天 2:00
   * - ``File Crawler - 共享文件夹``
     - ``0 3 * * *``
     - 每天 3:00
   * - ``File Crawler - 归档``
     - ``0 4 * * 0``
     - 每周日 4:00

cron 表达式的顺序是“分 时 日 月 星期”，星期中的 ``0`` 表示星期日。

最后，避免「Default Crawler」在 0:00 再次爬取相同的配置。
在 [系统] > [调度器] 中点击「Default Crawler」，通过 [编辑] 清空「计划」，然后点击 [更新]。
只要不取消「状态」中的「启用」，在需要一并爬取所有配置时，仍然可以用 [立即开始] 运行（如果禁用，[立即开始] 将不再显示）。

每周一次的作业与文档有效期
--------------------------

通过爬取注册的文档会带有有效期，超过有效期后，「Doc Purger」作业（每分钟执行）会将其从索引中删除。
有效期为从开始爬取的时间起，经过 [系统] > [通用] 中「删除以前的文档」所设天数后的时间，初始值为 ``3`` 天。
如果下一次爬取时找到了相同的文件，有效期就会延长。

如果保持初始值，只在星期日爬取的归档文档到星期三就无法再被搜索到。
因此，需要让这个天数大于最长的爬取间隔（7 天）。
本文留出余量，设为 ``10`` 天，即使作业失败一次文档也不会消失。

- 在 Docker 环境中，前面提到的 ``-Dfess.system.day.for.cleanup=10`` 就是这个初始值。[通用] 中的值在重新创建 ``fess01`` 时会丢失，因此写在 compose.yaml 中更可靠
- 在 Docker 以外的环境中，将 [通用] 中的「删除以前的文档」设为 ``10``，然后点击 [更新]

延长这个天数后，已从文件服务器删除的文件，在最后一次被找到的爬取之后，最多也会在搜索结果中保留这么多天。

执行并确认结果
==============

执行作业
--------

不必等到第二天，在 [系统] > [调度器] 中依次点击 3 个作业，并分别点击 [立即开始]。

确认完成
--------

1. 在 [系统信息] > [作业日志] 中，等待 3 个作业的「状态」从「运行中」变为「OK」。如果显示「失败」，点击该行并查看「结果」
2. 在 [系统信息] > [爬网信息] 中，查看各会话的「索引大小 (Web/文件)」，确认注册的文档数是否接近预期
3. 如果文档数偏少，打开 [系统信息] > [失败URL]。其中记录了未能获取的 URL，以及错误类型和日志

常见原因如下。

- 共享文件夹为 0 件，并且失败URL 中记录了共享的路径：检查文件认证的「主机名」与路径的写法、「文件爬网配置」的选择以及密码。如果日志中出现连接错误，确认容器能否解析文件服务器的名称、能否访问 445 端口
- 归档为 0 件，并且失败URL 也为空：检查路径是否写成了 ``file:///``，以及「要包含在爬网中的路径」是否与路径形式相同
- 归档出现读取错误：用前面介绍的 ``exec -u fess`` 命令，确认容器能否读取文件

按标签筛选
----------

在 ``http://localhost:8080/`` 上搜索一个 3 个位置中都可能包含的词。
结果中会按相关度混合排列门户的页面、共享文件夹中的 Office 文档、归档中的 PDF 等。

在 15.9 的搜索页面（主题 ``bootstrap``）中，有两处可以按标签筛选。

- 搜索结果旁边显示的「标签」列表：结果中包含的标签会连同件数一起列出，点击即可筛选到该标签
- 搜索框右侧的齿轮按钮：打开「搜索选项」，从「标签」列表中选择一个或多个，然后点击 [搜索]。选择多个时，带有其中任一标签的文档都会成为对象；不选择任何标签时则以全部文档为对象

筛选后的 URL 中会带上 ``fields.label=shared`` 这样的参数。
如果搜索结果旁边没有显示「标签」，或者筛选后结果为 0 件，请确认是否在创建标签之前就进行了爬取（运行「Label Updater」即可修复）。
如果「搜索选项」中没有显示「标签」列表，请确认标签的「权限」中是否包含搜索者的角色。

搜索结果的链接与路径映射
========================

点击来自共享文件夹或归档的搜索结果时，Fess 会读取文件并返回给浏览器。
这是由 [通用] 中的「Search File Proxy」实现的，初始状态下已启用。
即使浏览器无法直接打开 ``smb://`` 或 ``file:`` 的 URL，也能打开文件。

如果与归档相同的文件也在内部 Web 服务器（这里是 ``https://archive.example.com/``）上公开，并且希望用户打开那边的文件，可以用路径映射转换 URL。

在 [爬虫] > [路径映射] > [新建] 中输入以下项目，然后点击 [创建]。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 值
   * - 正则表达式
     - ``^file:/data/archive/(.*)$``
   * - 替换
     - ``https://archive.example.com/$1``
   * - 处理类型
     - 显示

「处理类型」最初选中的是「爬网」，请务必改为「显示」。

- 显示：索引中的 URL 保持 ``file:/data/archive/...`` 不变，只改变点击搜索结果链接时的跳转目标。创建后立即生效，无需重新爬取
- 爬网：改写保存到索引中的 URL 本身。在重新爬取之前不会生效，而且标签的「包含的路径」也需要改为与改写后的 ``https://`` URL 相匹配

设置完成后进行搜索，点击归档的结果，确认打开的是 ``https://archive.example.com/`` 的 Web 服务器。

延伸阅读
========

- 希望根据部门或职位改变可见的搜索结果：:doc:`guide-05`
- 希望确认文件服务器搜索的前提（支持的格式、访问权限的继承）：:doc:`file-server-search`
- 希望也能搜索 Google Drive、SharePoint、Box 中的文件：:doc:`guide-07`
- 希望查看搜索日志、改善搜索质量：:doc:`guide-08`
- 希望完善监控和备份，投入生产运行：:doc:`guide-10`

参考资料
========

- `文件抓取（文件服务器搜索） <https://fess.codelibs.org/zh-cn/stable/admin/fileconfig-guide.html>`__
- `文件认证 <https://fess.codelibs.org/zh-cn/stable/admin/fileauth-guide.html>`__
- `标签 <https://fess.codelibs.org/zh-cn/stable/admin/labeltype-guide.html>`__
- `调度器 <https://fess.codelibs.org/zh-cn/stable/admin/scheduler-guide.html>`__
- `常规 <https://fess.codelibs.org/zh-cn/stable/admin/general-guide.html>`__
- `路径映射 <https://fess.codelibs.org/zh-cn/stable/admin/pathmap-guide.html>`__
- `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__
