====================
启动、停止、初始设置
====================

本页面说明 |Fess| 服务器的启动、停止和初始设置步骤。

.. important::

   启动 |Fess| 前，必须先启动 OpenSearch。
   如果 OpenSearch 未启动，|Fess| 将无法正常工作。

启动方法
========

根据安装方法的不同，启动步骤也不同。

TAR.GZ 版的情况
-------------

启动 OpenSearch
~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.7.0
    $ ./bin/opensearch

在后台启动::

    $ ./bin/opensearch -d

启动 Fess
~~~~~~~~~~

::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess

在后台启动::

    $ ./bin/fess -d

.. note::

   启动可能需要几分钟。
   可以在日志文件（``logs/fess.log``）中确认启动状态。

ZIP 版的情况（Windows）
---------------------

启动 OpenSearch
~~~~~~~~~~~~~~~~

1. 打开 OpenSearch 的安装目录
2. 双击 ``bin`` 文件夹中的 ``opensearch.bat``

或者，从命令提示符::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch.bat

启动 Fess
~~~~~~~~~~

1. 打开 Fess 的安装目录
2. 双击 ``bin`` 文件夹中的 ``fess.bat``

或者，从命令提示符::

    C:\> cd C:\fess-15.8.0
    C:\fess-15.8.0> bin\fess.bat

RPM/DEB 版的情况 (chkconfig)
--------------------------

启动 OpenSearch::

    $ sudo service opensearch start

启动 Fess::

    $ sudo service fess start

确认启动状态::

    $ sudo service fess status

RPM/DEB 版的情况 (systemd)
------------------------

启动 OpenSearch::

    $ sudo systemctl start opensearch.service

启动 Fess::

    $ sudo systemctl start fess.service

确认启动状态::

    $ sudo systemctl status fess.service

启用服务自动启动::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

Docker 版的情况
-------------

.. note::

   ``compose.yaml`` 和 ``compose-opensearch3.yaml`` 并不包含在 |Fess| 本体中。
   这些文件由 docker-fess 项目（https://github.com/codelibs/docker-fess）提供；
   请获取该仓库，并在 ``compose`` 目录中执行以下命令。

使用 Docker Compose 启动::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

确认启动状态::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

确认日志::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

确认启动
==========

确认 |Fess| 是否正常启动。

健康检查
------------

在浏览器或使用 curl 命令访问以下 URL::

    http://localhost:8080/

如果正常启动，会显示 Fess 的搜索页面。

在命令行确认::

    $ curl -I http://localhost:8080/

如果返回 ``HTTP/1.1 200 OK``，则正常启动。

确认日志
--------

确认启动日志，检查是否有错误。

TAR.GZ/ZIP 版::

    $ tail -f /path/to/fess-15.8.0/logs/fess.log

RPM/DEB 版::

    $ sudo tail -f /var/log/fess/fess.log

或使用 journalctl::

    $ sudo journalctl -u fess.service -f

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

.. tip::

   启动成功完成后，控制台及日志中会显示如下启动完成消息::

       ...Booting the Tomcat: port=8080 contextPath=/
       ...
       Boot successful: url -> http://localhost:8080

在浏览器中访问
====================

访问以下 URL 确认 Web 界面。

搜索页面
--------

**URL**: http://localhost:8080/

显示 Fess 的搜索页面。初始状态下，由于未进行爬取配置，不会显示搜索结果。

管理页面
--------

**URL**: http://localhost:8080/admin

默认管理员账号：

- **用户名**: ``admin``
- **密码**: ``admin``

.. warning::

   **关于安全的重要注意事项**

   必须更改默认密码。
   特别是在生产环境中，强烈建议在首次登录后立即更改密码。

初始设置
==============

登录管理页面后，进行以下初始配置。

步骤 1: 更改管理员密码
-------------------------------

1. 登录管理页面（http://localhost:8080/admin）
2. 点击左侧菜单的「系统」→「用户」
3. 点击 ``admin`` 用户
4. 在 [密码] 字段输入新密码
5. 在 [密码 (确认)] 字段再次输入相同密码
6. 点击 [更新] 按钮

.. important::

   推荐密码满足以下条件：

   - 8个字符或以上（``password.min.length`` 所设置的最低长度要求）
   - 组合使用大写字母、小写字母、数字、符号
   - 不易被猜测

   默认情况下，仅要求满足最低长度（8个字符），不强制要求字符类型组合。
   可通过 ``password.require.uppercase`` 等设置启用字符类型要求。

步骤 2: 创建爬取配置
---------------------------

创建要爬取的网站或文件系统的配置。

1. 点击左侧菜单的「爬虫」→「网页」
2. 点击「新建」按钮
3. 输入必要信息：

   - **名称**: 爬取配置的名称（例：公司网站）
   - **URL**: 要爬取的目标 URL（例：https://www.example.com/）。如需指定多个 URL，请每行输入一个 URL
   - **最大访问数**: 爬取文档数的上限（可选）
   - **间隔**: 各次访问之间的等待时间（毫秒；默认值：``10000``）

   .. note::

      其他项目（如用户代理、线程数、深度等）留空时将使用默认值。

4. 点击「创建」按钮

步骤 3: 执行爬取
-----------------------

1. 点击左侧菜单的 [系统] → [调度器]
2. 打开 [Default Crawler] 作业，点击「立即开始」按钮
3. 等待爬取完成（可在仪表板查看进度）

步骤 4: 确认搜索
-------------------

1. 访问搜索页面（http://localhost:8080/）
2. 输入搜索关键词
3. 确认显示搜索结果

.. note::

   爬取可能需要较长时间。
   对于大规模网站，可能需要数小时到数天。

其他推荐设置
==============

在生产环境运行时，还需要考虑以下设置。

通过环境变量进行主要设置
--------------------------

端口号、JVM 堆大小、OpenSearch 连接 URL 等设置可通过环境变量更改。
TAR.GZ 版请编辑 ``bin/fess.in.sh``，RPM 版请编辑 ``/etc/sysconfig/fess``，DEB 版请编辑 ``/etc/default/fess``。
更改后需要重启 |Fess|。

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 环境变量
     - 默认值
     - 说明
   * - ``FESS_PORT``
     - ``8080``
     - |Fess| 监听的 HTTP 端口。
   * - ``FESS_HEAP_SIZE``
     - （未设置）
     - JVM 堆大小。最小值和最大值设置为相同的值。未设置时，最小值为 ``256m``，最大值为 ``2g``（ZIP 版（Windows）最大值为 ``1g``）；RPM/DEB 版使用 ``512m``。
   * - ``SEARCH_ENGINE_HTTP_URL``
     - （未设置）
     - 连接的 OpenSearch 的 URL。未设置时，使用内部默认值 ``http://localhost:9201``。当 OpenSearch 在不同端口或主机上运行时请更改此项（:doc:`install-linux` 的安装步骤会将其设置为 ``http://localhost:9200`` 以匹配 OpenSearch 的监听端口）。RPM/DEB 版通过软件包环境配置文件默认设置为 ``http://localhost:9200``。
   * - ``FESS_LOG_LEVEL``
     - ``warn``
     - |Fess| 的日志级别。

.. note::

   Windows ZIP 版的 ``bin\fess.in.bat`` 不读取这些环境变量（与代理相关的变量除外）。
   各项值直接写在文件中，如需更改请直接编辑 ``bin\fess.in.bat``。

邮件服务器设置
------------------

为了通过邮件接收故障通知等消息，请配置 SMTP 服务器和通知收件人地址。

1. 在配置文件 ``app/WEB-INF/classes/fess_env.properties`` 中，通过 ``mail.smtp.server.main.host.and.port``（默认值：``localhost:25``）指定 SMTP 服务器的主机名和端口。更改后需要重启 |Fess|。
2. 在管理界面中，点击左侧菜单的 [系统] → [通用]。
3. 在 [通知邮件] 字段输入收件人邮件地址。
4. 点击 [更新] 按钮。
5. 可使用 [发送测试邮件] 按钮验证邮件是否正常发送。

时区设置
----------------

|Fess| 使用服务器（操作系统 / JVM）的时区。管理界面中没有更改时区的设置项。
如需更改时区，请修改操作系统的时区设置，或在 ``bin/fess.in.sh`` 的 ``FESS_JAVA_OPTS`` 中添加 JVM 选项 ``-Duser.timezone=Asia/Tokyo``（Windows 系统请编辑 ``bin\fess.in.bat``）。

调整日志级别
--------------

在生产环境中，可以调整日志级别以减少磁盘使用量。

|Fess| 的整体日志级别可通过 ``FESS_LOG_LEVEL`` 环境变量更改（默认值：``warn``）。
如需对各个日志记录器进行精细控制，请编辑配置文件 ``app/WEB-INF/classes/log4j2.xml``。
爬取、suggest 和缩略图生成作为独立进程运行，因此请分别在 ``app/WEB-INF/env/{crawler,suggest,thumbnail}/resources/log4j2.xml`` 中配置各自的日志级别。

详情请参阅 :doc:`../admin/index`。

停止方法
========

TAR.GZ/ZIP 版的情况
-----------------

停止 Fess
~~~~~~~~~~

终止进程::

    $ ps aux | grep fess
    $ kill <PID>

或者，在前台运行时可以使用 ``Ctrl+C`` 停止。

停止 OpenSearch::

    $ ps aux | grep opensearch
    $ kill <PID>

RPM/DEB 版的情况 (chkconfig)
--------------------------

停止 Fess::

    $ sudo service fess stop

停止 OpenSearch::

    $ sudo service opensearch stop

RPM/DEB 版的情况 (systemd)
------------------------

停止 Fess::

    $ sudo systemctl stop fess.service

停止 OpenSearch::

    $ sudo systemctl stop opensearch.service

Docker 版的情况
-------------

停止容器::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

停止并删除容器::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   如果使用 ``down`` 命令时同时删除卷，请添加 ``-v`` 选项。
   这种情况下会删除所有数据，请注意。

重启方法
==========

TAR.GZ/ZIP 版的情况
-----------------

先停止后启动。

RPM/DEB 版的情况
--------------

chkconfig::

    $ sudo service fess restart

systemd::

    $ sudo systemctl restart fess.service

Docker 版的情况
-------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

故障排除
====================

无法启动的情况
------------

1. **确认 OpenSearch 是否启动**

   ::

       $ curl http://localhost:9200/

   如果 OpenSearch 未启动，请先启动 OpenSearch。

2. **确认端口号冲突**

   ::

       $ sudo netstat -tuln | grep 8080

   如果端口 8080 已被使用，请更改端口号。

   - TAR.GZ 版：在 ``bin/fess.in.sh`` 中更改 ``FESS_PORT``
   - ZIP 版（Windows）：直接编辑 ``bin\fess.in.bat`` 中的 ``-Dfess.port=8080``
   - RPM 版：在 ``/etc/sysconfig/fess`` 中更改 ``FESS_PORT``
   - DEB 版：在 ``/etc/default/fess`` 中更改 ``FESS_PORT``

3. **确认日志**

   确认错误消息以找出问题。

4. **确认 Java 版本**

   ::

       $ java -version

   请确认已安装 Java 21 或更高版本。

详细的故障排除请参阅 :doc:`troubleshooting`。

下一步
==========

|Fess| 正常启动后，请参阅以下文档开始运维：

- :doc:`../admin/index` - 爬取配置、搜索配置、系统配置的详情
- :doc:`security` - 生产环境的安全配置
- :doc:`troubleshooting` - 常见问题和解决方法
- :doc:`upgrade` - 版本升级步骤
- :doc:`uninstall` - 卸载步骤
