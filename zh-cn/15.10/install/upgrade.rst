====================
升级步骤
====================

本页面说明将 |Fess| 从旧版本升级到最新版的步骤。

.. warning::

   **升级前的重要注意事项**

   - 升级前必须获取备份
   - 强烈建议在测试环境提前验证升级
   - 升级期间服务会停止，请设置适当的维护时间
   - 根据版本不同，配置文件的格式可能已更改

支持版本
============

本升级步骤支持以下版本之间的升级：

- Fess 14.x → Fess 15.10
- Fess 15.x → Fess 15.10

.. important::

   |Fess| 14.x 对应 OpenSearch 2.x 系列，\ |Fess| 15.10 对应 OpenSearch 3.9.0。
   由于 |Fess| 专用的 OpenSearch 插件必须与 OpenSearch 版本完全一致，
   因此从 14.x 升级时，也必须同时对 OpenSearch 进行主版本升级。
   请参阅 :ref:`upgrade-opensearch`。

.. note::

   如果从更旧的版本（13.x 及更早）升级，可能需要逐步升级。
   详情请确认发布说明。

升级前的准备
====================

确认版本兼容性
--------------------

请确认升级目标版本与当前版本的兼容性。

- `发布说明 <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - |Fess| 15.10 的系统要求（Java、OpenSearch 版本）

计划停机时间
----------------

升级工作需要停止系统。请考虑以下因素计划停机时间：

- 备份时间: 10分钟 ~ 数小时（取决于数据量）
- 升级时间: 10 ~ 30分钟
- 运行确认时间: 30分钟 ~ 1小时
- 预留时间: 30分钟

**推荐维护时间**: 总计 2 ~ 4小时

步骤 1: 数据备份
==============================

升级前，请备份所有数据。

备份配置数据
----------------------

1. **从管理页面备份**

   登录管理页面，点击「系统信息」→「备份」。

   备份页面按条目列出以下配置数据。
   点击各行下载（不是单个 ZIP 文件，而是按条目分别下载的独立文件。
   由于没有批量下载功能，需要将所需项目逐一下载）。

   - ``fess_basic_config.bulk`` - 配置索引（爬取设置、调度器、标签、
     关键词匹配、角色、Web/文件认证等 19 个索引）
   - ``fess_config.bulk`` - 除上述 19 个索引外，还包含爬取信息、失败 URL、作业日志、
     缩略图队列等运行时数据，共 25 个索引（15.8 及之前；15.10 增加了保存用户标签的
     ``tag_type`` 索引，共 26 个）
   - ``fess_user.bulk`` - 用户、角色、群组
   - ``system.properties`` - 包含常规设置的系统设置
   - ``fess.json`` - 索引设置（分片数、\ ``index.knn`` 等）
   - ``doc.json`` - 文档映射（字段定义）

   .. note::

      ``fess_config.bulk`` 包含 ``fess_basic_config.bulk``。作为升级前的
      配置备份，\ ``fess_basic_config.bulk``\ 、\ ``fess_user.bulk``\ 、
      ``system.properties`` 这 3 个文件就已足够。但是，如果备份来源为 15.10 或更高版本且使用了用户标签，由于保存用户标签的 ``tag_type`` 索引不包含在 ``fess_basic_config.bulk`` 中，请同时下载 ``fess_config.bulk``\ （参见 :doc:`../admin/tagtype-guide`\ ）。

   .. note::

      搜索日志、点击日志等日志数据（``search_log.ndjson``、``click_log.ndjson``、
      ``favorite_log.ndjson``、``user_info.ndjson``；15.10 中还会显示 ``chat_log.ndjson``）也可从
      同一页面下载。
      如果仅备份配置，则不需要下载这些文件。另外，这些 ``*.ndjson`` 文件无法
      通过备份页面的上传功能重新导入恢复
      （请参阅「回滚步骤」）。

2. **备份配置文件**

   ZIP 版::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   RPM 版::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   DEB 版::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess``\ （RPM 版）和 ``/etc/default/fess``\ （DEB 版）是
      用于指定 ``FESS_PORT``\ 、\ ``FESS_HEAP_SIZE``\ 、\ ``SEARCH_ENGINE_HTTP_URL``\ 、
      ``FESS_DICTIONARY_PATH`` 等内容的环境变量文件。
      ZIP 版中与之对应的设置位于 ``bin/fess.in.sh``。

3. **定制的配置文件**

   如有定制的配置文件，也请备份::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/
       $ cp /path/to/fess/lib/classes/tomcat_config.properties /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` 是 |Fess| 本体（Web）进程的日志配置。
      爬虫等子进程使用各自独立的文件
      （例如 ``app/WEB-INF/env/crawler/resources/log4j2.xml`` 等，\ ``crawler``\ 、\ ``suggest``\ 、
      ``thumbnail``\ 、\ ``chunk`` 共 4 个），如果修改过这些文件，
      请一并备份。

备份索引数据
------------------------------

备份 OpenSearch 的索引数据。

方法 1: 使用快照功能（推荐）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用 OpenSearch 的快照功能备份索引。

.. note::

   要注册文件系统仓库（``fs``），需要事先在 OpenSearch 的 ``opensearch.yml`` 的
   ``path.repo`` 中指定备份目标目录，并重启 OpenSearch。

1. 配置仓库::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. 创建快照::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. 确认快照::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

方法 2: 整体备份目录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

停止 OpenSearch 后，备份数据目录。

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Docker 版的备份
---------------------

OpenSearch 的数据保存在 Docker 卷中。\ ``compose-opensearch3.yaml`` 中定义了
用于索引数据的 ``search01_data`` 和用于词典文件的 ``search01_dictionary``
共 2 个卷。

.. note::

   实际的卷名会附加 Compose 项目名称（默认为放置 Compose 文件的目录名）作为前缀。
   请使用以下命令确认准确的卷名::

       $ docker volume ls

停止容器后，备份卷。\ ``docker run`` 的 ``-v`` 需要指定
包含前缀的实际卷名::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   如果在 ``-v`` 中指定不带前缀的 ``search01_data``，Docker 不会引用现有卷，
   而是会新建一个同名的空卷。命令不会报错，且会生成内容为空的归档文件，
   看起来就像是已经完成了备份。

.. note::

   |Fess| 本体（``fess01``）的容器没有专用卷，因此备份对象仅为
   上述 2 个卷。但是，从管理页面更改的常规设置以及从管理页面安装的
   插件仅保存在容器内部，重新创建容器后会丢失。
   请通过 Compose 文件的 ``FESS_JAVA_OPTS`` 或 ``FESS_PLUGINS`` 指定这些内容以实现持久化。

步骤 2: 停止当前版本
================================

停止 Fess 和 OpenSearch。

ZIP 版没有附带用于停止的脚本。\ ``bin/fess`` 如果是使用 ``-p`` 选项
启动的，可以使用 PID 文件停止::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

如果启动时未指定 ``-p``，请确认进程 ID 后使用 ``kill`` 停止
（仅使用 ``-d`` 不会创建 PID 文件）。

RPM/DEB 版 (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   开始步骤 3 之前，请确认 |Fess| 已经停止，不要替换仍在运行的 |Fess| 的软件包或文件。
   在运行中的 15.8 的 |Fess| 上将 DEB 软件包替换为 15.10 的软件包后，直到重启 |Fess|，
   搜索页面一直返回 ``404``\ 。软件包版可以通过 ``systemctl status fess.service`` 确认。

步骤 3: 安装新版本
======================================

根据安装方法，步骤有所不同。

ZIP 版
-------------

1. 下载并解压新版本::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.10.0/fess-15.10.0.zip
       $ unzip fess-15.10.0.zip

   .. note::

      |Fess| 的归档版仅以 ZIP 格式发布（不提供
      ``fess-15.10.0.tar.gz``）。

2. 复制旧版本的配置::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.10.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/

   .. warning::

      如果原样复制 ``fess_config.properties`` 与 ``fess.in.sh`` ，旧版本的值会被沿用，其中也包括
      15.10 中默认值已变更的项。例如，升级后新建的作业默认将使用 Groovy。执行最后两条命令之前，
      请将各文件与 ``fess-15.10.0`` 中的文件进行比较，只迁移自己修改过的值。需要确认的项目请参阅
      :ref:`upgrade-159-carried-over-config` 。

3. 如有定制内容，请同时复制以下文件::

       # Tomcat 设置（SAML 所需的 tomcat.sameSiteCookies=none 也在此文件中）
       $ cp /path/to/old-fess/lib/classes/tomcat_config.properties /path/to/fess-15.10.0/lib/classes/
       # 已安装的插件
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.10.0/app/WEB-INF/plugin/
       # 自己上传的静态主题（每个主题一个目录；不要复制 bootstrap）
       $ cp -r /path/to/old-fess/app/themes/<your-theme> /path/to/fess-15.10.0/app/themes/

   .. warning::

      如果不复制旧版本的 ``tomcat_config.properties`` ，``tomcat.sameSiteCookies`` 会在没有任何提示的
      情况下恢复为默认值 ``lax`` ，SAML 登录将无法使用（参阅 :ref:`upgrade-159-saml` ）。
      该文件的随附内容在 15.8.0 和 15.10 中相同，因此可以原样复制。

   .. warning::

      请不要将 ``log4j2.xml`` 复制并覆盖 15.10 的文件。15.10 的文件将 ``RequestLoggingFilter`` 的
      日志记录器固定为 ``warn`` ，而复制 15.8 的文件会丢失这一设置：将日志级别设为 DEBUG 时，
      请求头（包括 ``Authorization`` ）和请求参数（包括在登录表单中输入的密码）会被写入日志。
      请用 ``diff`` 比较这两个文件，只将自己修改过的内容重新应用到 15.10 的文件中。

   .. warning::

      请不要复制整个 ``app/themes/`` 目录。其中还包含 |Fess| 内置的主题 ``bootstrap`` ，
      将其覆盖到 15.10 的主题上，会使 15.10 的搜索界面被 15.8 版本的主题替换。
      只复制自己创建的主题目录。对于 |Fess| 项目发布的主题，请改为使用
      ``bin/fess-setup install theme <name>`` 安装面向 15.10 的构建（参阅 :doc:`fess-setup` ）。

   .. warning::

      请不要复制在管理页面「页面设计」中编辑过的 JSP（``app/WEB-INF/view/``）。15.10 的搜索
      界面是静态主题，不再使用这些 JSP；此类修改现在应放在何处，请参阅
      :ref:`upgrade-159-static-theme` 。

   .. note::

      从 ``app/WEB-INF/plugin/`` 复制的插件是为旧版本构建的。复制后，请在 ``fess-15.10.0`` 中执行
      ``bin/fess-setup upgrade plugins`` ，将各插件替换为针对 15.10 构建的版本（参阅
      :ref:`upgrade-plugin-versions` ）。

4. 确认配置差异，根据需要进行调整

RPM/DEB 版
----------

安装新版本的包::

    # RPM
    $ sudo rpm -Uvh fess-15.10.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.10.0.deb

.. note::

   RPM 版中，``/etc/fess/*`` 的配置文件被注册为 ``%config(noreplace)``，
   因此在升级时会被保留（新的默认文件会以 ``.rpmnew`` 的形式并存）。
   如果添加了新的配置选项，需要手动调整。修改过的 ``/etc/fess/fess_config.properties`` 与 ZIP 版
   步骤中复制的文件一样，在 15.10 中仍使用旧值。请参阅 :ref:`upgrade-159-carried-over-config` 。

.. warning::

   DEB 版中，``/etc/fess`` 下的文件（如 ``fess_config.properties`` 和
   ``tomcat_config.properties`` ）与 ``/etc/default/fess``\ 、\ ``/etc/init.d/fess``\ 、
   ``/usr/lib/systemd/system/fess.service`` 一样，被注册为 conffile。从 15.8 首次升级时，
   ``dpkg`` 的处理方式如下。

   - 从未编辑过的文件，会不经询问直接替换为 15.10 的文件。
   - 对于编辑过的文件，``dpkg`` 会询问。如果保留自己的文件（默认回答，或 ``--force-confold`` ），
     15.10 的文件会以 ``<文件名>.dpkg-dist`` 的形式并存。如果安装新文件（``Y`` 或
     ``--force-confnew`` ），自己的文件会保存为 ``<文件名>.dpkg-old`` 。
   - 无人可以回答时，``dpkg -i`` 和 ``apt-get install -y`` 会在第一个询问处停止。无人值守升级时，
     请指定 ``--force-confold`` （``--force-confdef`` 同样可以避免询问），例如
     ``sudo dpkg --force-confold -i fess-15.10.0.deb`` 或
     ``sudo apt-get install -y -o Dpkg::Options::=--force-confold ./fess-15.10.0.deb`` 。

   无论哪种情况，都请事先备份 ``/etc/fess`` （步骤 1）。保留下来的文件仍是 15.8 的值，
   因此不要原样使用，请与 ``.dpkg-dist`` 文件比较（参阅 :ref:`upgrade-159-carried-over-config` ）。
   另外，``/etc/fess/system.properties`` 是不包含在软件包中的运行时生成文件，
   因此不会被覆盖。

Docker 版
---------

1. 获取新版本的 Compose 文件::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose-opensearch3.yaml

2. 获取新镜像::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

步骤 4: 升级 OpenSearch
====================================

|Fess| 15.10 对应 OpenSearch 3.9.0。如果所连接的 OpenSearch 版本比这更旧，
请按照以下步骤升级。

.. note::

   本步骤适用于 ZIP 版及 RPM/DEB 版中手动运维 OpenSearch 的情况。
   对于 Docker 版，在步骤 3 中获取新镜像时，OpenSearch 和插件也会一并更新，
   因此无需执行本步骤。

.. important::

   无论是否使用分块向量搜索（语义搜索），\ |Fess| 15.10 都会在搜索索引的设置中始终
   包含 ``index.knn``，并在映射中始终包含 ``content_chunk_vector``\ （\ ``knn_vector``
   类型）。因此，所连接的 OpenSearch **必须安装 k-NN 插件**。

   - 标准发行版的 OpenSearch 以及 Docker 版镜像中已包含该插件。
   - **minimal 发行版不包含该插件，会导致索引新建失败，\ |Fess| 无法启动。**
   - 索引设置中还会始终发送 ``knn.derived_source.enabled``。无法识别该配置的
     旧版本 OpenSearch，无论是否安装 k-NN 插件，索引创建都会失败。

   详情请参阅 :doc:`../config/search-semantic` 中的「前提条件」。

.. warning::

   OpenSearch 的主版本升级需要谨慎进行。
   可能会出现索引兼容性问题。
   |Fess| 14.x 对应 OpenSearch 2.x 系列，因此从 14.x 升级时必然属于这种情况。

   在 OpenSearch 3.9.0 上创建的快照无法恢复到 OpenSearch 3.8.0 及更早版本。请保留升级前创建的快照，以备回滚。

1. 安装新版本的 OpenSearch

2. 重新安装插件::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-fess/3.9.0/opensearch-analysis-fess-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-extension/3.9.0/opensearch-analysis-extension-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-minhash/3.9.0/opensearch-minhash-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-configsync/3.9.0/opensearch-configsync-3.9.0.zip

   .. note::

      这些插件的版本必须与所使用的 OpenSearch 版本一致。
      |Fess| 15.10 对应 OpenSearch 3.9.0。如果版本不一致，
      插件安装将会失败。

      |Fess| 的 4 个插件发布在 maven.codelibs.org 上，因此通过 URL 指定。 ``opensearch-plugin install`` 的 ``groupId:artifactId:version`` 形式只查找 Maven Central。

3. 将词典目录移至 OpenSearch 配置目录下

   从 OpenSearch 3.8.0 开始，如果词典文件位于 OpenSearch 配置目录之外，OpenSearch 会拒绝创建索引。
   如果按照以前的步骤在 ``configsync.config_path`` 中指定了 ``/var/lib/opensearch/data/config/``\ （ZIP 版为 ``/path/to/opensearch/data/config/``\ ）等配置目录之外的位置，
   |Fess| 将无法创建索引，也无法启动。
   对于 RPM/DEB 版，请按如下方式将词典文件复制到 ``/etc/opensearch/dictionary/``::

       $ sudo install -d -o opensearch -g opensearch -m 0750 /etc/opensearch/dictionary
       $ sudo cp -a /var/lib/opensearch/data/config/. /etc/opensearch/dictionary/
       $ sudo chown -R opensearch:opensearch /etc/opensearch/dictionary

   然后，将 ``/etc/opensearch/opensearch.yml`` 中的 ``configsync.config_path`` 和 |Fess| 的 ``FESS_DICTIONARY_PATH``\ （RPM 版为 ``/etc/sysconfig/fess``\ ，DEB 版为 ``/etc/default/fess``\ ）都更改为 ``/etc/opensearch/dictionary/``\ 。
   对于 ZIP 版，请使用 OpenSearch 的 ``config/dictionary/``\ 。详情请参阅 :doc:`install-linux`。

4. 启动 OpenSearch::

       $ sudo systemctl start opensearch.service

步骤 5: 启动新版本
================================

ZIP 版::

    $ cd /path/to/fess-15.10.0
    $ ./bin/fess -d -p /path/to/fess-15.10.0/fess.pid

.. note::

   指定 ``-p`` 后会创建 PID 文件，下次停止时可以使用
   ``kill $(cat /path/to/fess-15.10.0/fess.pid)`` 来停止。

RPM/DEB 版::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

步骤 6: 运行确认
==================

1. **确认日志**

   确认没有错误。

   ZIP 版::

       $ tail -f /path/to/fess/logs/fess.log

   RPM/DEB 版::

       $ sudo tail -f /var/log/fess/fess.log

   Docker 版::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      同一日志目录下，还会输出爬取处理的 ``fess-crawler.log``\ 、认证与管理操作的
      ``audit.log``\ 、以及检索请求的 ``searchlog.log``。

2. **访问 Web 界面**

   在浏览器中访问 http://localhost:8080/。

3. **登录管理页面**

   访问 http://localhost:8080/admin 并使用管理员账号登录。

4. **确认版本**

   在管理页面点击「系统信息」→「配置信息」，确认「系统属性」中显示的
   ``fess.version`` 已更新为新版本。

5. **确认搜索运行**

   在搜索页面执行搜索，确认正常返回结果。

步骤 7: 重建索引（推荐）
====================================

对于主版本升级，建议重建索引。

.. note::

   以下步骤只是重新执行爬取，并不会更新索引映射（字段定义）。如果需要进行会更新映射的重新
   索引——例如要新启用分块向量搜索（语义搜索）时——请在管理界面的「系统信息」→「维护」中
   单独运行「重新索引」。详情请参阅 :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）。

   如果继续使用由 15.8 或更早版本创建的文档索引，另请参阅 :ref:`upgrade-reindex-new-fields`\ 。

.. warning::

   OpenSearch 3.9.0 会拒绝 15.8 曾接受的字典条目，例如重复保存的同一条 ``mapping`` 条目，或
   含有空格的 ``kuromoji`` 词元。存在此类条目时，「重新索引」不会创建新的文档索引：``fess.log``
   中只会输出 ``Failed to create index`` ，旧索引继续提供搜索。请在「系统」→「字典」下载字典，
   删除重复或无效的行后重新上传，然后再次运行「重新索引」。15.10 不再保存的条目请参阅
   :ref:`upgrade-159-api-requests` 。

1. 确认现有爬取计划
2. 从「系统」→「调度器」执行「Default Crawler」
3. 等待爬取完成
4. 确认搜索结果

.. warning::

   由于重新索引会以新的映射重建索引，在没有 k-NN 插件的 OpenSearch 中会失败。
   请确认步骤 4 中的注意事项。

从 15.9 升级到 15.10
====================

本节的变更适用于升级到 15.10 的所有情况。如果从 15.8 或更早版本升级，请在阅读本节之后，继续阅读下一节“从 15.8 升级到 15.10”。

.. _upgrade-1510-tika:

Apache Tika 4 和 ``tika.xml``
-----------------------------

15.9.0 使用 Apache Tika 3.3.2，15.10 使用 Apache Tika 4.1.0。
Tika 4 没有 XML 配置文件，因此 |Fess| 15.10 在代码中构建 Tika 解析器，不再读取 ``tika.xml``。
15.10 的 ZIP 版、RPM/DEB 版和 Docker 镜像中不包含该文件。

在 ``tika.xml`` 中编写的 ``parser-exclude`` 等设置将不再生效，被排除的解析器会重新运行。
如果配置目录中残留有以前版本的 ``tika.xml``，|Fess| 会忽略该文件，并在启动时向 ``fess.log`` 输出警告。请删除该文件。

- ZIP 版: 在 15.9 及更早的 ZIP 版中，该文件位于 ``app/WEB-INF/classes/tika.xml``。15.10 启动时的警告会同时检查 ``app/WEB-INF/classes`` 和 ``app/WEB-INF/conf``
- RPM/DEB 版: ``/etc/fess/tika.xml``

.. _upgrade-1510-tika-metadata:

元数据名称
----------

Tika 4 更改了许多元数据名称。例如，``pdf:charsPerPage`` 变为 ``pdf:chars-per-page``，``access_permission:*`` 变为 ``access-permission:*``，``Message:*`` 变为 ``message:*``。
对于 Tika 的 ``LegacyKeyMigrationFilter`` 能够识别的名称，|Fess| 会将其还原为 Tika 3 的名称，因此使用这些名称的 ``crawler.metadata.name.mapping`` 设置可以继续使用。
该过滤器不会转换的名称将以 Tika 4 的名称传递。例如，Excel 文件的 ``protected`` 现在是 ``msoffice:excel:protected-worksheet``。如果 ``crawler.metadata.name.mapping`` 中使用了这样的名称，请改为 Tika 4 的名称。

Tika 4 新增的元数据与其他元数据一样处理，只要名称不匹配 ``crawler.metadata.content.excludes``，就会添加到内容中。

例外是以 ``tk:``、``X-TIKA:`` 或 ``zip:`` 开头的名称，Tika 将它们用于内部管理（Tika 3 的 ``X-TIKA:Parsed-By`` 现在是 ``tk:parsed-by``）。|Fess| 会在这些名称到达文档之前将其删除。它们不会被还原为 Tika 3 的名称，无论是否列在 ``crawler.metadata.content.excludes`` 中，也都不会添加到内容中。如果在 ``crawler.metadata.name.mapping`` 中映射了 ``X-TIKA:*`` 或 ``tk:*`` 名称，或者在脚本中使用了它们，将无法再获得这些值。

内容中的图像元数据
------------------

15.9 及之前，图像文件（PNG、JPEG、TIFF、GIF、BMP 等）的所有元数据都会添加到内容中，因此图像的内容是一串关于像素、色彩配置文件和相机设置的数值。
15.10 中，对于 MIME 类型为 ``image/*`` 的文档，只有名称与 ``crawler.metadata.content.image.includes`` 匹配的元数据才会添加到内容中。默认情况下，包括 EXIF、XMP、IPTC 的标题、说明、作者、关键字、注释、版权和地名，以及 Windows 资源管理器的属性和 PNG 的文本块。
其他元数据仍会被提取，因此可以用于 ``crawler.metadata.name.mapping`` 和脚本。``crawler.metadata.content.excludes`` 同样适用于与该列表匹配的名称。

升级之前已建立索引的图像，其内容在重新爬取该图像之前不会改变。

爬取配置的 Tesseract 和 PDF 属性文件
------------------------------------

如果爬取配置中指定了 ``config.tika.tesseract.config`` 或 ``config.tika.pdf.config``，请检查对应的属性文件，因为 Tika 4 重命名或删除了部分属性。
对于无法应用的每个键，|Fess| 会在 ``fess-crawler.log`` 中输出警告并忽略该键。

- Tesseract 文件中的 ``timeoutSeconds`` 变为 ``timeoutMillis``。|Fess| 会将 ``timeoutSeconds`` 转换为 ``timeoutMillis``\ （数值乘以 1000），但今后请在 ``timeoutMillis`` 中以毫秒为单位编写。``crawler.document.ocr.timeout`` 仍以秒为单位。
- PDF 文件中的 ``ocrStrategy``、``ocrDPI``、``ocrImageType``、``ocrImageFormatName``、``ocrImageQuality``、``ocrRenderingStrategy``、``accessChecker`` 和 ``renderer`` 等属性已从 Tika 4 的 ``PDFParserConfig`` 中删除。|Fess| 会忽略这些属性，并在 ``fess-crawler.log`` 中输出警告。此时 PDF 的 OCR 遵循 Tika 4 的默认行为（自动）：在 ``tesseract`` 可用且 |Fess| 中启用了 OCR 时，对文字很少的页面执行 OCR。
- ``tesseract`` 的位置不能再在 ``tika.xml`` 中设置，Tesseract 文件中的 ``tesseractPath``、``tessdataPath`` 和 ``imageMagickPath`` 也不起作用。``tesseract``（以及使用时的 ImageMagick）必须能在爬虫进程的 ``PATH`` 中找到。

字符编码检测
------------

Tika 4 为文本文件报告的字符编码名称可能与 15.9 不同。例如，Shift_JIS 会被报告为 ``windows-31j``，ISO-8859-1 会被报告为 ``windows-1252``，EUC-JP 会被报告为 ``x-eucJP-Open``。

登录表单的次数限制
------------------

在 15.9 中，``theme.api.login.rate.limit.*`` 的次数限制只适用于 ``/api/v2/auth/login``，不适用于登录页面（``/login/``）的登录表单。
在 15.10 中，登录表单使用相同的限制和相同的计数器。当同一 IP 地址的登录失败达到每分钟 10 次，或同一用户名的密码从同一 IP 地址被拒绝 5 次时，来自该 IP 地址（或该 IP 地址与用户名的组合）的登录将在 ``theme.api.login.lockout.seconds``\ （默认 900 秒）内被拒绝。
被拒绝期间，即使密码正确也无法登录，页面显示的消息与密码错误时相同。登录成功后，该次尝试占用的名额会被退还。
对于可能发送错误密码的脚本，以及许多用户共用一个 IP 地址的环境，请考虑这一限制。

当反向代理将 ``X-Forwarded-For`` 作为单独的头部行添加时（例如 HAProxy 的 ``option forwardfor``），15.10 会读取所有行，并将从右数第一个不是信任代理的地址作为客户端 IP（参见 :doc:`../config/rate-limiting`）。15.9 及之前只读取第一行（客户端发送的那一行），因此客户端可以自行选择次数限制所用的地址。

爬取配置权限字段中的 (deny)
---------------------------

如果在爬取配置或类似设置的权限字段中，在 ``(deny)`` 后面加空格书写，例如 ``(deny) {user}name``，15.9 不会将其保存为拒绝，而是原样保存带空格的文本。随后在管理界面打开该配置并保存，它会变成允许（``{user}name``）。
15.10 会在保存前去掉 ``(deny)`` 和 ``(allow)`` 后面的空格，再次保存后拒绝仍然是拒绝。不含 ``{user}``、``{group}`` 或 ``{role}`` 的 ``(deny)`` 行不会被保存。

在 15.9 或更早版本中保存的设置不会自动修复。请检查每个使用 ``(deny)`` 的爬取配置的权限字段，按 ``(deny){user}name`` 的形式重新书写并保存，然后重新爬取。

audit.log 中的控制字符
----------------------

在 LTSV 格式中，字段值中的所有控制字符以及 Unicode 行分隔符（NEL、LS、PS）都会被替换为空格（制表符替换为下划线），因此输入的用户名无法开始第二条记录。15.9 只替换 CR 和 LF。

面向插件开发者的变更
--------------------

以下变更会影响使用 ``fess-crawler`` 类的插件。请针对 15.10 重新构建此类插件（参阅 :ref:`upgrade-plugin-versions`）。

- ``ExtractData`` 不再实现 Tika 的接口（``TikaCoreProperties``、``HttpHeaders`` 等）。字符串常量 ``CONTENT_TYPE`` 和 ``CONTENT_ENCODING`` 由 ``ExtractData`` 自身定义。``RESOURCE_NAME_KEY`` 仍为 ``"resourceName"``。
- 已删除 ``TikaExtractor.setTikaConfig`` 和 ``fess.xml`` 中的 ``tikaConfig`` 组件。
- 日志级别为 ``debug`` 时，``CrawlJob`` 不再向爬虫传递 ``-Dorg.apache.tika.service.error.warn=true``，因为 Tika 4 不再读取该属性。

从 15.8 升级到 15.10
===================

若从 15.8 升级，以下为不向后兼容的变更。若从 15.7 及更早版本升级，这些变更同样适用：请阅读从
「内嵌 OpenSearch 的移除」到「将新字段和假名规范化应用到现有文档索引」的所有小节（内嵌
OpenSearch、脚本引擎、S3 与 SSO 插件、Index Exporter 作业等），以及本页末尾的
「15.10 特有的迁移工作」。

内嵌 OpenSearch 的移除
----------------------

15.8 之前，未设置 ``SEARCH_ENGINE_HTTP_URL`` 而启动 ``bin/fess`` 时，|Fess| 会在自身的 JVM 内
启动 OpenSearch 节点。15.10 移除了该配置，搜索引擎始终是独立的服务器。

``bin/fess.in.sh`` 现在默认设置 ``SEARCH_ENGINE_HTTP_URL=http://localhost:9200``\ 。
如果没有可连接的 OpenSearch，|Fess| 将无法启动。可以使用 ``bin/fess-setup install opensearch``
进行安装（仅限 Linux 和 Windows。OpenSearch 没有官方的 macOS 发行版，请使用 Homebrew 或
Docker）。

|Fess| 还需要 ``FESS_DICTIONARY_PATH`` 与该 OpenSearch 的 ``opensearch.yml`` 中的 ``configsync.config_path`` 一致；否则 |Fess| 无法创建索引。当 |Fess| 目录下的 ``opensearch/`` 中恰好只有一个通过 ``bin/fess-setup install opensearch`` 安装的 OpenSearch 时，15.10 的 ``bin/fess.in.sh``\ （Windows 上为 ``bin\fess.in.bat``\ ）会自动设置该变量。使用其他 OpenSearch 时，请按照 :doc:`install-linux` 或 :doc:`install-windows` 的说明进行设置。

以下内容也一并移除：

- ``es/`` 目录（``es/modules``、``es/plugins``、``es/data``）
- ``-Dfess.es.dir`` 和 ``SEARCH_ENGINE_HOME``
- ``bin/module.xml`` 和 ``bin/plugin.xml``
- 对旧 ``elasticsearch.*`` 配置键的回退处理

此外，连接早于 OpenSearch 3 的版本时，15.8 只记录错误日志并继续运行，而 15.10 将启动失败。
这些版本未实现遍历全部文档的处理所依赖的 ``_shard_doc`` 排序，通过 HTTP 时此类请求不会失败，
而是不返回响应。

.. warning::

   使用内嵌 OpenSearch 运行时的索引数据无法继承。请新建外部 OpenSearch 服务器，通过管理界面的
   「备份」迁移配置后重新爬取。备份包含爬取配置、用户和日志，**不包含已爬取的文档**。

.. note::

   将 15.8 的备份恢复到新的 15.10 服务器时，请注意以下两点。

   - 作业仅在比服务器上的作业更新时才会恢复。因此，在 15.8 中从未编辑过的内置作业会保留 15.10 的 JavaScript 版本。
     在 15.8 中编辑或创建的作业会以保存时的脚本引擎恢复（内置作业为 ``groovy``），没有 ``fess-script-groovy``
     插件时会因 ``groovy is not found`` 而失败。请安装该插件，或将这些作业切换为 JavaScript；
     两种做法都在 :ref:`upgrade-159-script-engine` 中说明。
   - Web 认证、爬取配置和数据存储配置的参数中保存的密码和密钥，是用 ``app.cipher.key`` 加密的。
     请将旧环境的值设置到新服务器的 ``fess_config.properties`` 中（参阅
     :ref:`upgrade-159-carried-over-config` ）。否则无法解密。

Playwright 爬虫移至插件
-----------------------

Playwright 爬虫及其使用的 Node.js 可执行文件不再包含在发行包中。
在 ``fess-15.8.0.zip``\ （457.1 MiB）中，收纳 Node.js 可执行文件的 Playwright 驱动包占用了 204.3 MiB。

如果爬取配置的设置参数中指定了 Playwright 客户端（例如
``client.crawlerClients=playwright:http://.*``\ ），请同时安装插件与 Node.js。
插件也可以从管理界面的「系统 > 插件」页面安装。 ``bin/fess.in.sh`` 会检测 Node.js
的安装位置并设置 ``PLAYWRIGHT_NODEJS_PATH``\ 。

::

    $ bin/fess-setup install plugin fess-crawler-playwright
    $ bin/fess-setup install nodejs

没有插件时，此类配置仍会被爬取，但使用的是普通 HTTP 客户端，因此只有 JavaScript 才会生成的
文本不会被索引。爬取作业仍会正常结束，也不会记录失败 URL。每次爬取时， ``fess-crawler.log``
会按每个爬取配置记录一条警告，其中给出插件名称和上面的两条命令。

使用 Playwright 为 HTML 页面生成缩略图的 ``fess-thumbnail-playwright`` 插件同样依赖 Node.js 运行。
如果使用该插件，请同样通过 ``bin/fess-setup install nodejs`` 安装 Node.js，同一份安装由两个插件共用。

如果既不使用 Playwright 爬虫，也不使用 ``fess-thumbnail-playwright`` 插件，则无需处理。

Google Cloud Storage 移至插件
-----------------------------

Google Cloud Storage 的 SDK 不再包含在发行包中， ``gcs://`` 爬取与 ``gcs`` 存储类型改由
``fess-storage-gcs`` 插件提供。请从管理界面的「系统 > 插件」页面安装，或执行以下命令。

::

    $ bin/fess-setup install plugin fess-storage-gcs

``crawler.file.protocols`` 的随附取值中也去掉了 ``gcs``\ ，现为
``file,smb,smb1,ftp``\ 。安装插件后会重新加入。在此之前，路径以 ``gcs:`` 开头的文件
爬取配置只会记录一条警告，且什么都取不到。升级后的现有安装会保留自己的
``crawler.file.protocols``\ ，因此路径仍被接受，但没有可处理它的爬虫客户端；新安装中
``gcs:`` 不是已配置的协议，管理界面会拒绝保存该路径，而先前保存的路径会被当作本地文件
路径处理。存储页面同样会记录警告，并把失败作为错误显示出来，文字中包含需要安装的插件
名称；此前它只显示一个空的文件列表。

如果不使用 Google Cloud Storage，则无需处理。Amazon S3 以及 MinIO 等兼容 S3 的存储也以
同样的方式移至插件，请参阅下一节。

Amazon S3 移至插件
------------------

AWS SDK 不再包含在发行包中， ``s3://`` 爬取与 ``s3``\ 、 ``s3_compat`` 存储类型改由
``fess-storage-s3`` 插件提供。请从管理界面的「系统 > 插件」页面安装，或执行以下命令。

::

    $ bin/fess-setup install plugin fess-storage-s3

``crawler.file.protocols`` 的随附取值中也去掉了 ``s3``\ ，现为 ``file,smb,smb1,ftp``\ 。
安装插件后会重新加入。 ``storage.type`` 的默认值仍为 ``auto``\ ，未设置端点时会解析为
S3，因此即使从未显式指定 ``s3``\ ，在安装插件之前管理界面的存储功能也无法使用。
``storage.*`` 的取值位于 ``WEB-INF/conf/system.properties``\ ，因此会保留下来，现有的
``crawler.file.protocols`` 也不会被升级覆盖。

如果不使用 Amazon S3 或 MinIO 等兼容 S3 的存储，则无需处理。

SSO 认证移至插件
----------------

四种 SSO 认证均不再包含在发行包中，每个 ``sso.type`` 取值改由各自的插件提供，插件中同时
附带所需的认证库： ``saml`` 对应 ``fess-sso-saml``\ ， ``spnego`` 对应
``fess-sso-spnego``\ ， ``entraid``\ （旧名 ``aad`` 亦同）对应 ``fess-sso-entraid``\ ，
``oic`` 对应 ``fess-sso-oidc``\ 。请注意最后一组：插件名为 ``fess-sso-oidc``\ ，而
``sso.type`` 的取值仍为 ``oic``\ ，两者不一致的地方仅此一处。请从管理界面的
「系统 > 插件」页面安装所需的插件，或执行以下命令。

::

    $ bin/fess-setup install plugin fess-sso-saml

``sso.type`` 与 ``saml.*``\ 、 ``spnego.*``\ 、 ``entraid.*``\ 、 ``aad.*``\ 、 ``oic.*``
各项位于 ``WEB-INF/conf/system.properties``\ ，因此设置值会保留下来。管理页面
「系统」→「常规」也仍将四种类型全部列为选项，设置项也保留。这是因为插件无法提供 JSP，
因此该页面不会提示插件尚未安装。

安装插件之前，对 ``/sso/`` 的请求会被重定向回登录页面，页面上会提示 SSO 登录失败，无法
通过 SSO 登录。15.10 会将包含所查找的组件名与提供方插件名的警告记录到 ``fess.log``\ ；
15.8 之前在任何日志级别下都不会输出任何内容。

``oic`` 插件的校验比 15.8 的认证功能更严格。 ``oic.token.server.url`` 必须为 HTTPS（只有
``localhost``、``127.x.x.x`` 和 ``::1`` 可以使用 ``http``），并会校验 ID Token 的 ``aud`` 与
``exp`` 声明；设置了新增的 ``oic.issuer`` 键时，还会校验 ``iss``。详情请参阅
:doc:`../config/sso-oidc`。

在 15.8 中，``oic.token.server.url`` 可以指定任意主机的 ``http`` URL。在 15.10 中，指向Docker Compose服务名（如 ``http://keycloak:8080/...``）或内部主机名的 ``http`` 会被拒绝，即使它指向同一台机器。被拒绝时登录失败，``fess.log`` 中会输出以 ``Failed to process the OpenID Connect callback: oic.token.server.url must be https`` 开头的警告。请在更新前将令牌端点改为HTTPS的URL。

此外，建议将 ``oic.issuer`` 设置为OP的Discovery文档中 ``issuer`` 的值。未设置时不会校验 ``iss``，并在启动后的首次登录时输出警告。设置 ``oic.issuer`` 不会放宽HTTPS规则。

如果不使用 SSO，即 ``sso.type`` 为 ``none`` 或未设置，则无需处理。

.. _upgrade-159-script-engine:

内置脚本引擎由 Groovy 改为 JavaScript
-------------------------------------

15.8 之前内置的脚本引擎为 Groovy， ``job.default.script`` 的默认值也是 ``groovy`` 。15.10 中内置
引擎为 JavaScript，默认值为 ``javascript`` 。Groovy 已不再内置，改由 ``fess-script-groovy``
插件提供；要让 ``scriptType`` 的 ``groovy`` 生效，必须安装该插件。

升级不会更改各设置中保存的脚本引擎，而 15.10 之前保存且未记录引擎的设置会被视为 ``groovy`` 。
没有该插件时，以下内容将无法正常工作：

- 以 ``groovy`` 保存的计划任务。
  **15.8 自行注册的任务也属于这种情况。**\ Default Crawler、Suggest Indexer、Config Reloader、
  Log Aggregator、Doc Purger 等随附任务都以 ``groovy`` 保存，而 15.10 启动时只会添加尚不存在的
  随附任务，因此不会改动它们。这些任务每次按计划触发都会失败，Default Crawler 也不再进行爬取。
  大多数随附任务的「日志记录」处于关闭状态，因此失败不会出现在作业日志中，只会在 ``fess.log``
  中留下 ``Failed to execute job`` 警告。
- 在「配置参数」中编写了字段脚本（ ``field.script.<字段名>`` ）的 Web 爬取配置和文件爬取配置。
  该配置的所有文档都会因 ``ScriptEngineException`` 失败并记录为失败 URL，而爬取作业本身仍会
  正常结束。
- 设置了「脚本」的数据存储配置。除参数名本身以外的值无法求值。请参阅
  :doc:`../config/datastore/ds-overview` 。
- 文档提升规则。该规则不会提升任何文档。
- 「替换」以 ``groovy:`` 开头的路径映射。该映射不会被应用，URL 保持不变。

首次启动后，请在 ``fess.log`` 中查找以
``Settings use the script engine groovy, which is not registered`` 开头的警告。\ |Fess| 会在
启动时检查一次上述设置，并按类型输出使用了没有任何插件提供的引擎的设置数量。如果从 15.8 沿用的
``fess_config.properties`` 中仍为 ``job.default.script=groovy`` ，警告中也会列出该项，此时升级后
新建的任务同样会使用 Groovy（参阅 :ref:`upgrade-159-carried-over-config` ）。请采用以下任一方式
处理：

- 安装该插件并重启 |Fess| 。已保存的 Groovy 脚本可原样运行，警告也不再输出。也可以在管理页面
  「系统」→「插件」中安装该插件。

  ::

      $ bin/fess-setup install plugin fess-script-groovy

- 将各设置改用 JavaScript。先改写只有 Groovy 才接受的语法，再选择 JavaScript：

  - 计划任务：在管理页面「系统」→「调度器」中将「执行方法」改为 ``javascript`` 。随附任务的
    脚本除以下两项外，原样即是有效的 JavaScript：Thumbnail Purger 使用了 Groovy 的 ``long``
    字面量 ``1000L`` ，在 JavaScript 中会成为语法错误（请写成 ``1000`` ）；Index Exporter
    需要进行 :ref:`upgrade-159-index-exporter` 中所述的修改。JavaScript 的数组字面量会自动转换为
    Java 的 ``String[]`` ，因此不再需要 Groovy 写法中的 ``as String[]`` 。

    ::

        return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"]).fileConfigIds(["1"]).dataConfigIds([]).execute(executor);

  - Web 爬取配置和文件爬取配置：在「配置参数」中添加 ``config.script.type=javascript`` 。
  - 数据存储配置：在「参数」中添加 ``script_type=javascript`` 。
  - 文档提升规则：将「脚本类型」改为 ``javascript`` 。
  - 路径映射：将「替换」的开头由 ``groovy:`` 改为 ``javascript:`` 。
  - ``job.default.script`` ：在从 15.8 沿用的 ``fess_config.properties`` 中将其设置为
    ``javascript`` 。

``crawler.default.script`` 已删除
---------------------------------

``fess_config.properties`` 中已不存在 ``crawler.default.script`` 。请从配置中删除该项；
以该名称保留的值不会生效。

爬取协议 ``storage`` 已删除
---------------------------

``crawler.file.protocols`` 中不再接受 ``storage`` ，随附的值为 ``file,smb,smb1,ftp`` 。
请改用 ``s3`` ，并将路径以 ``storage:`` 开头的文件爬取配置改为 ``s3:`` 路径。 ``s3`` 需要
``fess-storage-s3`` 插件。

.. _upgrade-159-index-exporter:

Index Exporter 作业引用了已删除的包
-----------------------------------

15.10 不再包含 ``org.opensearch`` 的类，作业脚本使用的查询构建器已移至
``org.codelibs.fesen.opensearch`` 下。15.8 为 Index Exporter 作业保存的脚本引用了
``org.opensearch.index.query.QueryBuilders`` ，而升级不会替换该脚本，因此即使安装了
``fess-script-groovy`` ，该作业仍会失败。该作业随附时处于禁用状态且没有计划，因此只有在运行它时
才会受到影响。请在管理页面「系统」→「调度器」中打开该作业，将脚本中的包改为 15.10 所用的包：

::

    return new org.codelibs.fess.job.IndexExportJob().query(org.codelibs.fesen.opensearch.index.query.QueryBuilders.matchAllQuery()).execute()

如果自行编写的脚本中引用了 ``org.opensearch.index.query`` ，也请以同样方式修改。更多查询示例请
参阅 :doc:`../config/admin-index-export` 。

.. _upgrade-159-carried-over-config:

从 15.8 沿用的配置文件
----------------------

步骤 3 的 ZIP 版步骤会从旧安装中复制 ``fess_config.properties`` 与 ``bin/fess.in.sh`` ；RPM 版
升级则会保留修改过的 ``/etc/fess/fess_config.properties`` （15.10 的文件以
``fess_config.properties.rpmnew`` 的形式并存）。DEB 版升级在询问时保留自己的版本，也是同样的
结果（15.10 的文件以 ``fess_config.properties.dpkg-dist`` 的形式并存）。无论哪种情况，15.10 都会以
15.8 的值运行，15.10 中随附值已变更的键也不例外。请至少确认以下各键。

.. list-table::
   :header-rows: 1

   * - 键
     - 15.8.0
     - 15.10
     - 保留 15.8 的值时的影响
   * - ``job.default.script``
     - ``groovy``
     - ``javascript``
     - 在管理页面「系统」→「调度器」中新建的作业默认使用 ``groovy`` ，没有
       ``fess-script-groovy`` 插件时会失败。
   * - ``job.template.script``
     - 含 ``as String[]`` 的 Groovy 写法
     - JavaScript 写法
     - 从爬取配置创建的作业会得到 Groovy 脚本。
   * - ``crawler.file.protocols``
     - ``file,smb,smb1,ftp,storage,s3,gcs``
     - ``file,smb,smb1,ftp``
     - 以 ``s3:`` 或 ``gcs:`` 开头的路径即使没有对应插件也会被接受，爬取时记录警告并跳过。
       ``storage`` 已不再受支持。
   * - ``search_engine.http.url``
     - ``http://localhost:9201``
     - ``http://localhost:9200``
     - 在未设置 ``SEARCH_ENGINE_HTTP_URL`` 时使用。从 15.8 复制的 ``bin/fess.in.sh`` 中未设置
       该变量时即属于这种情况，此时 |Fess| 会在 9201 端口查找 OpenSearch，即 15.10 已移除的内嵌
       OpenSearch 所用的端口。
   * - ``jvm.crawler.options``\ 、\ ``jvm.thumbnail.options``
     - ``-Djcifs.smb.client.*``\ 、\ ``-Djcifs.smb1.smb.client.*``
     - ``-Djcifs.client.*``
     - SMB 超时保持为 jcifs 的默认值。请参阅 :ref:`upgrade-159-jcifs` 。
   * - ``response.headers``
     - 包含 ``text/html=Content-Security-Policy: reflected-xss block`` 这一行
     - 已删除该行
     - 登录页面、管理界面等由 |Fess| 自身渲染的页面，其响应会带有浏览器无法识别的
       ``Content-Security-Policy: reflected-xss block`` 头，浏览器控制台会输出
       ``Unrecognized Content-Security-Policy directive 'reflected-xss'`` 。该头不起任何限制作用。
       请按下文说明删除该行。
   * - ``app.encrypt.property.pattern``
     - ``.*password|.*key|.*token|.*secret``
     - ``.*password|.*passphrase|.*key|.*token|.*secret``
     - 名称以 ``passphrase`` 结尾的参数（例如数据存储配置的 ``ssh.passphrase`` ）会以明文保存。
       之前已保存的值会一直是明文，直到用 15.10 的模式重新保存该设置。
   * - ``index.backup.log.targets``
     - ``click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - 「系统信息」→「备份」页面不会显示 ``chat_log.ndjson`` 。
   * - ``index.export.exclude.fields``
     - ``cache``
     - ``cache,tag``
     - 保存用户标签的 ``tag`` 字段，不再从 Index Export 作业写出的文件中排除。
   * - ``crawler.default.script``\ 、\ ``theme.allowed.archive.extensions``\ 、
       ``theme.assets.cache.max.age``\ 、\ ``theme.assets.precompressed``\ 、
       ``rag.chat.message.max.length``\ 、\ ``supported.uploaded.js.extentions``\ 、
       ``supported.uploaded.css.extentions``\ 、\ ``supported.uploaded.media.extentions``\ 、
       ``supported.uploaded.files``\ 、\ ``online.help.name.design``
     - 存在
     - 已删除
     - 不起作用，请删除。

15.0 至 15.8 随附的 ``response.headers`` 中包含
``text/html=Content-Security-Policy: reflected-xss block`` 这一行。 ``reflected-xss`` 是
Content-Security-Policy 早期草案中的指令，现在的浏览器已不再识别，因此该头不起任何限制作用，只会在
控制台中产生错误。15.10 的随附值已删除这一行（ ``X-XSS-Protection`` 与 ``X-Frame-Options`` 两行保持不变），
但从 15.8 沿用的 ``response.headers`` 仍会保留它。请仅从 ``fess_config.properties`` 的
``response.headers`` 中删除下面这一行。每行末尾的 ``\n\`` 表示值在下一行继续，因此删除整行后，其余各行
可以原样使用::

    text/html=Content-Security-Policy: reflected-xss block\n\

如果是通过 ``-Dfess.config.response.headers`` 指定 ``response.headers`` ，请从该值中删除相同的项。

从 15.8 复制的 ``bin/fess.in.sh`` 还缺少 15.10 文件中的以下两点。15.10 会将
``SEARCH_ENGINE_HTTP_URL`` 设置为 ``http://localhost:9200`` ，而 15.8 的文件除非自行设置，否则
保持未设置状态。此外，它不会查找通过 ``bin/fess-setup install nodejs`` 安装的 Node.js，因此除非
自行设置 ``PLAYWRIGHT_NODEJS_PATH`` ，否则 Playwright 插件找不到 Node.js。

请不要整体复制这两个文件，而是以 15.10 随附的文件为基础，重新应用自己修改过的值。可以用
``diff`` 查看这些值::

    $ diff /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/fess_config.properties
    $ diff /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/fess.in.sh

RPM 版请以同样方式比较 ``/etc/fess/fess_config.properties`` 与
``/etc/fess/fess_config.properties.rpmnew`` ，DEB 版升级则比较 ``/etc/fess/fess_config.properties``
与 ``/etc/fess/fess_config.properties.dpkg-dist`` 。DEB 版升级时，从未编辑过的
``fess_config.properties`` 会被替换为 15.10 的文件（参阅步骤 3），因此从 15.10 的值开始。

``app.cipher.key`` 是即使 15.10 没有变更也必须沿用的值。它是对 Web 认证、爬取配置和数据存储配置
的参数中保存的密码和密钥进行加密的密钥。如果新环境使用的密钥与保存这些内容时的密钥不同
（因为使用了随附的 ``fess_config.properties`` ，或将备份恢复到了新服务器），就无法解密：
``fess-crawler.log`` 中会记录 ``CipherFailureException`` ，包含此类配置的爬取将无法索引任何内容。

.. note::

   |Fess| 15.10 同样使用 ``app.cipher.key`` 加密保存 Web 认证和文件认证的 ``password`` ，因此备份中的
   ``fess_basic_config.bulk`` 和 ``fess_config.bulk`` 包含加密后的值。恢复到其他安装环境时请沿用相同的 ``app.cipher.key`` ；
   密钥不同时，使用这些认证信息的爬取会因错误而失败。15.10 之前创建的备份以明文包含这些值，可以继续正常使用
   （详见 :doc:`../admin/backup-guide` ）。

.. _upgrade-159-jcifs:

SMB 超时改用 jcifs 3 的属性名
-----------------------------

|Fess| 爬取 SMB 文件服务器时使用的 jcifs 在版本 3 中更改了属性名： ``jcifs.smb.client.*`` 改为
``jcifs.client.*`` ，SMB1 专用的 ``jcifs.smb1.smb.client.*`` 也合并到了相同的属性中。15.8 之前，
``jvm.crawler.options`` 与 ``jvm.thumbnail.options`` 仍传递旧名称，而 jcifs 不读取这些名称，因此
SMB 爬取一直以 jcifs 的默认值运行。15.10 传递新名称：

::

    -Djcifs.client.responseTimeout=30000
    -Djcifs.client.soTimeout=35000
    -Djcifs.client.connTimeout=60000
    -Djcifs.client.sessionTimeout=60000

因此，连接超时与会话超时首次生效，从 jcifs 默认的 35 秒延长到 60 秒：对于没有响应的 SMB
服务器，爬取现在最多会等待 60 秒。响应超时与套接字超时与 jcifs 的默认值相同，因此不会变化。

如果修改过这些超时，请在两个选项中改用新名称。使用旧名称时，它们在 15.8 中同样不起作用。从 15.8
沿用的 ``fess_config.properties`` 会保留旧名称，也就仍使用 jcifs 的默认值。

删除了四个不起作用的属性
------------------------

以下键已从 ``fess_config.properties`` 中删除。\ |Fess| 从未从该文件读取它们，因此以这些名称保留的
值与以前一样不起作用。

- ``theme.allowed.archive.extensions``
- ``theme.assets.cache.max.age``
- ``theme.assets.precompressed``
- ``rag.chat.message.max.length``

``rag.chat.message.max.length`` 设定的上限仍然有效，但会作为系统属性读取：请按照
:doc:`../config/rag-chat` 中的说明，在 ``app/WEB-INF/conf/system.properties`` 中或通过
``-Dfess.system.rag.chat.message.max.length`` 进行设置。

.. _upgrade-159-static-theme:

搜索界面现已改为静态主题
------------------------

除非选择了其他主题，搜索界面由 |Fess| 内置的静态主题 ``bootstrap`` 提供。这适用于 ``/``、
``/search``、``/advance``、``/help``、``/profile``、``/cache``、``/chat`` 以及错误页面。在 15.8
及之前的版本中，除非设置了默认主题，这些页面都是 JSP。

升级时同样会进行切换。从未设置过默认主题的 15.8 环境， ``system.properties`` 中没有
``theme.default`` ，因此升级后会显示静态主题；不会向配置写入任何内容，也不会输出任何日志。
没有可以恢复 JSP 搜索界面的设置。如果在 15.8 中设置了默认主题，该设置会被保留；请安装该主题
面向 15.10 的构建（ ``bin/fess-setup install theme <name>`` ），因为若默认主题指定的是未安装的
主题，将回退到 ``bootstrap`` ，并在 ``fess.log`` 中输出警告。

如果通过管理界面的「页面设计」或 JAR 主题插件修改过搜索界面的 JSP、CSS 或图片，这些修改将
不再显示。请在静态主题中进行修改：按照 :ref:`theme-customize-bundled` 的说明复制内置主题并
修改副本，或者从管理界面的「系统」→「主题」或使用 ``bin/fess-setup install theme <name>``
安装已发布的主题。按虚拟主机区分的外观现在是以虚拟主机命名的静态主题；参阅
:doc:`../config/security-virtual-host` 。

以下两项也已不再提供。

- 按虚拟主机区分的登录界面。在 15.8 之前，保存「系统」→「常规」时，包括登录界面在内的 JSP
  会被复制到 ``WEB-INF/view/<虚拟主机名>/`` ，可以按虚拟主机分别编辑。15.10 不再创建这些副本。
  登录界面（ ``/login/`` ）仍然是 JSP，但所有虚拟主机都显示共用的 ``WEB-INF/view/admin/login/``
  中的界面。以前复制的 JSP 不会被使用。
- JAR 主题插件（ ``fess-theme-*`` ）。即使安装，它也只会作为种类为 ``jar`` 的通用 JAR 放置，
  界面不会改变。遗留的 JAR 可以在「系统」→「插件」页面或使用
  ``bin/fess-setup remove plugin <name>`` 删除（参见 :doc:`../dev/theme-development` ）。

如果在 15.8 中曾在 JSP 的搜索结果中显示自定义字段，除了 ``query.additional.response.fields``
之外，还请在 ``query.additional.api.response.fields`` 中添加相同的字段。静态主题从
``/api/v2/search`` 获取搜索结果。 ``query.additional.response.fields`` 只是增加从搜索引擎
获取的字段，而该 API 在响应中只包含 ``query.additional.api.response.fields`` 中列出的字段
（参见 :doc:`../config/search-advanced` ）。另外，请修改主题以显示该字段。

客户端看到的变化
~~~~~~~~~~~~~~~~

错误现在会在所请求的 URL 上直接渲染，并返回真实的 HTTP 状态码。浏览器（ ``Accept`` 头中包含
``text/html`` 的请求）会收到主题的错误页面；其他客户端会收到一行 ``text/plain`` 正文（例如
``404`` 时为 ``Not Found.`` ）。在 15.8 及之前的版本中，大多数错误会以 ``302`` 重定向到
``/error/...`` 页面，而该页面本身返回 ``200`` 。请检查监控、健康检查，以及跟随 ``Location``
头或期望 ``/error/`` URL 的客户端。

.. list-table::
   :header-rows: 1

   * - 请求
     - 15.8 及之前
     - 15.10
   * - 缺少参数，或针对不存在的文档的 ``/go/``
     - ``200`` ，或 ``302`` 到 ``/error/``
     - ``400`` 或 ``404``
   * - 缺少参数、针对未知文档或没有缩略图的 ``/thumbnail/``
     - ``200`` 或 ``302``
     - ``400`` 或 ``404``
   * - 所配置的 SSO 类型不处理时的 ``/sso/metadata`` 和 ``/sso/logout``
     - ``302`` 到 ``/error/badrequest/``
     - ``400``
   * - ``/api/v1/*``、``/json`` 以及任何未知 URL
     - ``302`` 到 ``/error/notfound/``
     - ``404``
   * - 未捕获的异常（包括管理 API 中的异常）
     - ``302`` 到 ``/error/systemerror/``
     - ``500`` ，正文为 ``System Error.`` （不是 JSON）
   * - ``/error/notfound/``、``/error/badrequest/``、``/error/systemerror/`` 本身
     - ``200``
     - ``404``、``400``、``500``

在 ``login.required=true`` 时，搜索页面不再重定向匿名用户。它们会返回 ``200`` 和主题，由主题提示
用户登录，而其背后的数据则会被拒绝：除 ``/health``、``/auth/*`` 和 ``/ui/config`` 以外的所有
``/api/v2/`` 端点（包括 ``/api/v2/search`` ）在用户登录之前都会返回 ``401`` 。 ``/go/``、
``/thumbnail/`` 和 ``/osdd`` 仍会重定向到登录页面。期望匿名请求 ``/`` 时发生重定向的检查，需要改为
检查 ``/api/v2/search`` 是否返回 ``401`` 。

搜索界面也通过 ``/api/v2/search`` 进行搜索，因此搜索日志是在调用该 API 时记录的，而不是在请求
``/search`` 时记录。不执行 JavaScript 的客户端会收到没有搜索结果的页面。

搜索界面的 HTML 带有 ``X-Frame-Options: DENY``，以及包含 ``frame-ancestors 'none'`` 的 ``Content-Security-Policy`` ，因此其他页面无法将它放入框架中显示。15.8 的 JSP 搜索界面按 ``response.headers`` 的默认值发送 ``X-Frame-Options: SAMEORIGIN`` ，可以显示在同源页面的 ``iframe`` 中。如果已将搜索界面嵌入同源的 ``iframe`` ，请在 ``fess_config.properties`` 中把 ``theme.index.frame.ancestors`` （默认值 ``'none'`` ）设置为 ``'self'`` 。如需从其他源嵌入，请指定该源（参见 :doc:`../dev/theme-development` ）。

删除了管理界面的「页面设计」
----------------------------

删除了管理界面中的 [系统 > 页面设计]。无法再从管理界面编辑搜索界面的 JSP、CSS 和图片。
如需更改搜索界面的外观，请使用静态主题（参见 :ref:`theme-customize-bundled`）。

以下键也已从 ``fess_config.properties`` 中删除。以这些名称保留的值不会被使用。

- ``supported.uploaded.js.extentions``
- ``supported.uploaded.css.extentions``
- ``supported.uploaded.media.extentions``
- ``supported.uploaded.files``
- ``online.help.name.design``

``admin-design`` 和 ``admin-design-view`` 角色不再授予任何权限。仅拥有这些角色的用户登录后会进入
搜索界面，而不是管理界面。

``api.access.token.required`` 已删除
------------------------------------

``fess_config.properties`` 中已不存在 ``api.access.token.required`` 。以该名称保留的值不会生效，
包括从 15.8 沿用的 ``fess_config.properties`` 中的值。设置为 ``true`` 时，它会拒绝所有来自未登录用户的
API 请求。由于搜索界面现在通过 ``/api/v2/search`` 进行搜索，该设置还会使匿名用户看到没有结果的搜索界面。

曾将其设置为 ``true`` 的环境，现在会像对待搜索界面一样，以访客角色响应匿名用户的 API 请求。
如需禁止匿名用户搜索，请设置 ``login.required=true`` 。访问令牌的行为不变：带有已注册访问令牌的请求
会获得该令牌的权限，带有未注册或已过期令牌的请求会被拒绝。

.. _upgrade-159-api-requests:

API 现在会拒绝的请求
--------------------

15.10 会拒绝以下 15.8 曾接受的请求。请检查为 15.8 编写的客户端和脚本是否发送了这些请求。管理 API 以 HTTP ``400`` 拒绝请求，响应正文中的 ``status`` 为 ``1`` 。

.. list-table::
   :header-rows: 1

   * - 请求
     - 15.8 及之前
     - 15.10
   * - 向 ``/api/v2/search`` 同时指定 ``facet.field`` 或 ``facet.query`` 与小于等于 ``0`` 的 ``facet.size`` ，或者不是整数的 ``facet.size`` 、 ``facet.minDocCount``
     - ``200`` 。但结果为空： ``record_count`` 为 ``0`` ， ``partial`` 为 ``true``
     - ``400`` （ ``invalid_request`` ）。 ``facet.size`` 必须大于等于 ``1``
   * - 指定 ``track_total_hits=false`` 。如果把 ``query.track.total.hits`` 设置为 ``false`` ，所有搜索都会受到影响
     - ``200`` 。但没有搜索结果
     - 搜索会被拒绝（ ``/api/v2/search`` 返回 ``400`` 和 ``invalid_request`` ）。 ``true`` 和正整数的行为不变
   * - 通过管理 API 向 ``mapping`` 或 ``kuromoji`` 字典添加或更新与已有条目重复的条目
     - 会被保存。之后加载字典时失败，可能导致无法搜索
     - ``400``
   * - 通过管理 API 向 ``kuromoji`` 字典添加或更新 ``token`` 含有空格的条目，或 ``segmentation`` 与 ``reading`` 按空格分隔的词数不同的条目
     - 会被保存。与上面相同，加载字典时失败
     - ``400``
   * - 没有删除任何内容的 ``DELETE /api/admin/searchlist/doc/{doc_id}`` （不存在的 ``doc_id`` ，或像文档列表所返回的 ``_id`` 那样不是 ``doc_id`` 的值）
     - ``200`` （ ``status`` 为 ``0`` ）。文档不会被删除
     - ``400``
   * - 在管理 API 的用户的 ``roles`` 、 ``groups`` 中指定角色名、组名
     - 会被保存，但所指定的名称不会作为角色起作用。对于某些名称，读取该用户会失败
     - ``400`` 。请指定角色、组的 ID（ ``GET /api/admin/role/settings`` 、 ``GET /api/admin/group/settings`` 所返回的 ``id`` ）
   * - 为管理 API 的用户设置违反密码策略（例如 ``password.min.length`` ，默认值 ``8`` ）的密码；创建时省略密码；发送与 ``password`` 不一致的 ``confirm_password``
     - 会被保存，该用户可以用该密码登录
     - ``400``
   * - ``GET /api/admin/log/file/{id}`` 指定了不允许作为日志文件的名称（例如不以 ``.log`` 或 ``.log.gz`` 结尾），或不在日志目录中的文件
     - 不允许的名称返回 ``200`` 和空响应
     - ``400``
   * - 通过管理 API 创建或更新省略了 ``output`` 的 ``mapping`` 字典条目
     - ``200`` （ ``id`` 为 ``0`` ）；不保存任何内容
     - ``400``
   * - 无法访问存储时的 ``GET /api/admin/storage/list`` （包括未安装存储客户端插件的情况）
     - ``200`` （ ``status`` 为 ``0`` ）和空列表
     - ``400`` 。 ``message`` 给出原因；缺少插件时会指出需要安装的插件
   * - 在登录表单（ ``POST /login/login`` ）上，短时间内从同一 IP 地址，或从同一 IP 地址针对同一用户重复登录失败
     - 无限制
     - 超过按 IP 或按 IP 与用户组合的上限（ ``theme.api.login.rate.limit.per.ip.per.minute`` 、 ``theme.api.login.rate.limit.per.user.per.minute`` ）后，来自该 IP 地址（按用户上限时为来自该 IP 地址的该用户）的登录，即使凭据正确，也会在 ``theme.api.login.lockout.seconds`` 秒内被拒绝。响应与凭据错误时相同，均为登录错误。上限和锁定与 ``/api/v2/auth/login`` 共用（参见 :doc:`../api/api-auth` ）在地址未列入 ``rate.limit.trusted.proxies`` 的反向代理之后，所有客户端会被算作同一个地址，因此连续失败可能使所有用户无法登录。请将代理的地址添加到 ``rate.limit.trusted.proxies`` （当 ``X-Forwarded-For`` 来自不受信任的对端时， ``fess.log`` 中会输出一次警告）。

``/api/v2/documents/all`` 的每一行不再带有 ``score`` 。15.8 及之前，每个文档都带有搜索得分；15.10 使用 point in time 和 ``search_after`` 获取全部结果，因此不会产生得分。旧 API 插件的 ``/json?type=scroll`` 和 ``/api/v1/documents/all`` 也是如此。读取 ``score`` 的脚本需要能够处理该值不存在的情况。

管理 API 的文件上传（6 种字典、 ``badword`` 、 ``elevateword`` 、 ``storage`` ）通过 ``POST`` 接收。15.8 的文档曾介绍使用 ``PUT`` ，但 ``multipart/form-data`` 的 ``PUT`` 不会传送文件，因此在 15.8 和 15.10 中都会因“需要文件”的验证错误而失败。 ``PUT`` 端点仍然保留，但上传请使用 ``POST`` 。

以下变更不属于请求被拒绝，但可能影响使用 API 或管理界面的脚本和客户端。

- 管理 API ``webauth`` 和 ``fileauth`` 的获取请求（ ``/api/admin/webauth/settings`` 、 ``/api/admin/webauth/setting/{id}`` 以及 ``fileauth`` 下相同的端点）不再返回已保存的密码。 ``PUT`` 时省略密码或发送空密码，将保留已保存的密码；发送非空密码则会替换。
- 已登录的用户由会话识别，而不是由请求携带的 ``userCode`` 参数或 Cookie 识别（例如收藏 API）。匿名用户仍使用参数和 Cookie。
- 管理界面中「搜索列表」和「爬取信息」的「全部删除」需要编辑角色（ ``admin-searchlist`` 、 ``admin-crawlinginfo`` ）。仅拥有查看角色（带有 ``-view`` 后缀的角色）的用户的请求会被拒绝。
- 如果在 ``fess.xml`` 的 ``roleQueryHelper`` 中启用了 ``parameterKey`` 、 ``headerKey`` 或 ``cookieKey`` ，却没有设置 ``cipher`` ，并且值加密标志（ ``encryptedParameterValue`` 、 ``encryptedHeaderValue`` 或 ``encryptedCookieValue`` ）仍为默认值 ``true`` ，则 15.8 会把该值当作未加密的角色信息读取。15.10 会忽略该值，并在日志中输出一次警告。如果值已加密，请设置 ``cipher`` ；如果本意是接收未加密的值，请将该标志设为 ``false`` 。
- ``Content-Type`` 中指定了 JVM 不认识的字符集（例如 ``charset=nope`` ）的请求，将按未指定字符集处理。此前 ``/api/v2/search`` 会返回 ``500`` （ ``internal_error`` ）。
- 通过管理 API 上传或下载 ``kuromoji`` 、 ``mapping`` 、 ``stemmeroverride`` 、 ``synonym`` 字典失败时，消息现在会指明该字典。在 15.8 中，所有这些字典都显示“protwords file”。

``search_engine.type`` 的 ``cloud`` 已弃用
------------------------------------------

15.10 为 ``search_engine.type`` 新增了 ``vanilla`` 值，用于不含 CodeLibs 插件的原生 OpenSearch（请参阅 :doc:`../config/search-engine-type` ）。 ``cloud`` 成为 ``vanilla`` 的已弃用别名，仍可继续使用，但启动时会在日志中输出警告。在 15.10 上运行后，请改为 ``vanilla`` 。 ``aws`` 的行为与之前相同。

* ``vanilla`` 需要 15.10 及更高版本。\ |Fess| 15.8 及更早版本无法识别该值，因此在仍有可能回退到 15.8 期间，请保持 ``cloud`` 不变。
* ``aws`` 和 ``cloud`` 的索引定义现在从 ``fess_indices/_vanilla/`` 读取。随附的 ``fess_indices/_aws/`` 和 ``fess_indices/_cloud/`` 已不存在，自行添加的 ``fess_indices/_aws/`` 或 ``fess_indices/_cloud/`` 也不再被读取，请将修改内容移到 ``fess_indices/_vanilla/`` 。已存在的索引不会改变。
* 15.8 保存在搜索引擎中的建议（suggest）设置会自动迁移，无需任何操作。

CSV 数据存储会解析带引号的字段
------------------------------

15.10 的 ``fess-ds-csv`` 插件默认会解释引号。 ``"山田, 太郎"`` 这样的字段会成为一列，而 15.8.0 的
插件会在逗号处将其拆分。执行 ``bin/fess-setup upgrade plugins`` 之后，请检查读取含有带引号字段的
CSV 文件的数据存储配置。要保持 15.8 的行为，请在「参数」中添加 ``quote_disabled=true`` ；
请参阅 :doc:`../config/datastore/ds-csv` ，其中也说明了引号不匹配时的行为。

.. _upgrade-reindex-new-fields:

将新字段和假名规范化应用到现有文档索引
--------------------------------------

15.10 在启动时会向配置、日志和用户索引添加新字段。对于文档索引，只会添加保存用户标签的 ``tag``
字段（``keyword``），映射的其余部分和分析设置不会更改。如果继续使用由 15.8 或更早版本创建的
文档索引，以下 15.10 的变更不会生效。

- **文件的所有者和最后修改者**\ （\ ``owner``\ 、\ ``last_modifier``\ ）: 文件系统、SMB 和 FTP 爬取时新索引的
  字段。现有文档索引中没有它们的定义，因此会根据首次爬取的值被自动映射为 ``text`` 类型，
  ``owner:alice`` 之类的搜索和 ``facet.field=owner`` 无法按预期工作。
- **ETag**\ （\ ``etag``\ ）: 爬虫保存所爬取页面 ETag 的字段，15.10 会将其作为 ``If-None-Match``
  回传，以避免重复获取未更改的页面。现有文档索引中同样没有它的定义，因此会被自动映射为 ``text``
  类型，而不是随附的不索引的 ``keyword`` 。使用该映射时条件请求仍可正常工作。
- **假名异体和代替长音符号书写的破折号的规范化**\ （例如将 ``サ―バ－`` 视为与 ``サーバー`` 相同的词）:
  规则位于文档索引的分析设置和词典 ``mapping.txt`` 中，因此不会应用到现有索引。

要同时应用两者，请在管理界面的「系统信息」→「维护」中启用「更新别名」和「重置字典」，然后运行
「重新索引」。重新索引会将现有文档复制到新索引，因此无需重新爬取。

.. warning::

   「重置字典」会用随附的词典文件覆盖 OpenSearch 端的词典。如果在管理界面的「字典」中编辑过同义词等，
   请事先下载，并在重新索引后重新应用：从下载的文件中删除重复或无效的条目（参阅步骤 7），
   上传后，在「系统信息」→「维护」的“重新加载文档索引”中单击 [重新加载]。在此之前，文档索引的
   分析器会继续使用随附的词典，恢复的同义词无论等待多久都不会匹配。在索引时生效的词典，还需要
   重新爬取文档；请参阅 :ref:`dict-apply-changes` 。

.. note::

   由 15.8 或更早版本索引的文件没有所有者和最后修改者的值。增量爬取不会重新获取未更改的文件，
   因此要添加这些值，请暂时禁用「系统」→「常规」中的「检查上次修改时间」后再进行爬取。


15.10 特有的迁移工作
===================

从 15.7 及更早版本升级到 15.10 时，需要根据所使用的功能执行以下工作。

若此前使用过语义搜索
----------------------------------

在 |Fess| 15.7 及更早版本中提供语义搜索功能的 ``fess-webapp-semantic-search`` 插件，
已在 15.10 中并入核心，现已不再需要（已弃用）。需要移除该插件、删除
``-Dfess.semantic_search.*`` 及 ``-Drank.fusion.searchers=default,semantic``\ ，
并解除旧的 ingest pipeline。详细步骤请参阅
:ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）。

若此前使用过 AI 搜索模式（RAG Chat）
---------------------------------------------

自 15.10 起，AI 搜索模式（RAG Chat）功能已拆分为 ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、
``fess-llm-gemini`` 等插件。请在管理页面「系统」→「插件」中安装与所使用的
提供商对应的插件。15.10 还新增了面向 Amazon Bedrock 的
``fess-llm-bedrock`` 。

若此前使用过 SPNEGO（Windows 集成认证）
---------------------------------------

自 15.10 起，如果客户端主体的 Kerberos 领域与服务器的领域不同，SPNEGO 登录将被拒绝。
如果用户来自 AD 域树的子域或建立了信任关系的林，请在管理页面「系统」→「通用」或
``app/WEB-INF/conf/system.properties`` 的 ``spnego.allowed.realms`` 中以逗号分隔列出
这些领域。否则，在 15.7 之前能够登录的用户将因 ``Kerberos realm is not allowed`` 而被拒绝。
详细内容请参阅 :doc:`../config/sso-spnego`\ 。

此外，15.10 中 ``spnego.allow.unsecure.basic`` 与 ``spnego.allow.localhost`` 的代码默认值也从
``true`` 改为了 ``false`` 。在 ``app/WEB-INF/conf/system.properties`` 中不存在这些键的环境中，
升级后会自动采用更严格的行为。特别是当 ``spnego.allow.unsecure.basic=false`` 时，SPNEGO 库仅对
``HttpServletRequest#isSecure()`` 返回 ``true`` 的请求提供 Basic 认证，
因此在反向代理上终止 TLS 并以 HTTP 转发的环境中，此前回退到 Basic 认证的客户端将无法登录。
此时请在 ``tomcat_config.properties`` 中设置 ``tomcat.secure=true`` 。
详细内容请参阅 :doc:`../config/sso-spnego`\ 。

.. warning::

   代码默认值仅在该键不存在时才生效，而管理页面「系统」→「通用」每次保存都会写入所有
   ``spnego.*`` 键。因此，在 15.7 中曾经在该页面上执行过更新的环境，仍然保存着
   ``spnego.allow.unsecure.basic=true`` 与 ``spnego.allow.localhost=true`` ，
   升级到 15.10 并不会使其变得更严格：宽松的行为会被静默沿用，15.10 只会在 SPNEGO 初始化时
   向 ``fess.log`` 输出一条警告。请在管理页面「系统」→「通用」或 ``system.properties`` 中
   有意识地关闭这两项。其中 ``spnego.allow.localhost=true`` 更为危险：SPNEGO 库会把来自同一
   主机的请求以服务器的 OS 用户身份进行认证，完全不做 Kerberos 验证，在同一主机上部署反向
   代理时并不安全。

.. _upgrade-159-saml:

若此前使用过 SAML 认证（SSO）
-----------------------------

自 15.10 起，|Fess| 会将每个 SAML 响应与自身发出的 AuthnRequest 的 ID 进行绑定校验，
因此 IdP 发起（未经请求的 unsolicited）的 SSO 无法再使用。从 IdP 门户（如 Okta 仪表板或
Microsoft Entra ID 的「我的应用」）中的 |Fess| 磁贴发起的登录没有可匹配的 AuthnRequest，
会被拒绝。在 15.7 之前它之所以可用，是因为 |Fess| 会将无法匹配的响应退回给 IdP，
而 IdP 会立即返回一个经过请求的断言。如果要在 IdP 侧放置磁贴，请将其链接指向 |Fess| 的
``/sso/`` 端点，使登录由 SP 发起。

此外，IdP 通过跨站 POST 返回断言，因此必须将 ``tomcat_config.properties`` 中的
``tomcat.sameSiteCookies`` 设置为 ``none``\ 。使用附带的默认值 ``lax`` 时，会话 Cookie
不会随该请求发送，SAML 登录无法完成。该文件在 ZIP 软件包中位于 ``lib/classes/``\ ，
在 DEB/RPM 软件包中位于 ``/etc/fess/``\ ，修改后需要重启 |Fess|\ 。浏览器仅对同时带有
``Secure`` 属性的 Cookie 接受 ``none``\ ，因此 |Fess| 必须通过 HTTPS 提供服务。
在 15.7 之前，同样的配置错误不会产生明确的错误，而是表现为不断重定向到 IdP 的死循环，
因此即使站点看起来正常，也请确认该设置。15.10 不再循环，而是一次性失败。
详细内容请参阅 :doc:`../config/sso-saml`\ 。

若此前使用过 Microsoft Entra ID（Azure AD）
-------------------------------------------

自 15.10 起，向授权端点请求的响应模式默认值由 ``form_post`` 变更为 ``query``\ 。15.7 之前回调以
跨站 POST 返回，而 |Fess| 的默认值 ``tomcat.sameSiteCookies = lax`` 不会随该请求发送会话
Cookie，因此需要将其改为 ``tomcat.sameSiteCookies = none``\ 。如果仅为此才设置了 ``none``\ ，
可以恢复为默认值。若要保持原有行为，请指定 ``entraid.response.mode=form_post`` 并保留
``tomcat.sameSiteCookies = none``\ 。浏览器仅对同时带有 ``Secure`` 属性的 Cookie 接受
``none``\ ，因此这种方式同样要求通过 HTTPS 提供 |Fess| 。

自 15.10 起，|Fess| 还会在登录完成后于后台解析用户所属的组和角色，而不再让登录等待 Microsoft
Graph。在解析完成之前——或解析未能完全成功时——用户拥有的仅有其自身的用户级权限，以及在
``entraid.default.groups`` 和 ``entraid.default.roles`` 中配置的组和角色。若两者都未配置
（即附带的默认值），这段时间内的搜索将一条文档都搜不到，因为按附带的默认值创建的爬取配置会授予
``{role}guest``\ ，而已登录用户并不持有该角色。解析进行期间，搜索界面会显示相应提示，
未能完全成功时则显示另一条提示（只有直接所属查询和嵌套组遍历都成功，解析才算成功）。
每次刷新访问令牌时都会重新解析，之后一旦成功，提示即会消失，因此对于持续时间超过令牌有效期的会话，失败并不一定就是
最终结果；若要立即重试，请先注销再重新登录。
详细内容请参阅 :doc:`../config/sso-entraid`\ 。

在后台解析还带来一个影响：在解析完成之前，尚无法得知用户已解析的角色。因此，
管理员会被重定向到搜索界面而不是管理仪表板，在此期间打开管理页面也会被送回搜索界面。
这段时间为最多约 1 秒的调度延迟，加上 Microsoft Graph 调用本身（直接所属查询 1 次，
再为每个直接所属的组各 1 次以遍历嵌套组，依次串行执行，且缓存为空时），
因此会随用户所属组的数量增加而变长。在此期间访问只会被拒绝，绝不会被放行；而且无需任何配置即可度过这段时间：授权会在同一会话的每个请求上
重新评估，因此解析完成后重新打开管理界面即可正常访问，无需重新登录。

.. warning::

   请勿通过把 |Fess| 的管理员角色配置到 ``entraid.default.roles`` 来缩短这段时间。
   该属性是单个全局值，\ |Fess| 会在登录时将其应用于每一个 Entra ID 用户，
   并在之后每次解析时重新应用，这会让租户中的所有用户永久获得 |Fess| 管理员权限。

使用 LDAP / Active Directory 集成的情况
------------------------------------------

从 15.10 开始，组和角色的权限名称取自条目 RDN 的值，而不再是从 DN 文本中截取的片段。CN 中包含
在 DN 内被转义的字符（通常是逗号）的组，其权限名称将与 15.7 之前不同。

.. list-table::
   :header-rows: 1

   * - 组条目的 DN
     - 15.7 之前的权限名称
     - 15.10 的权限名称
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

在 15.7 之前，逗号之前部分相同的多个组会合并为同一个权限名称，因此 ``Sales, EMEA`` 与
``Sales, APAC`` 的成员可以读取对方的文档以及 ``Sales`` 组的文档。在 15.10 中，各自获得独立的权限
名称，这种跨组访问不会再发生。

作为代价，\ **以旧权限名称索引的文档将不再对该组的用户可见**\ 。如果爬取设置的「权限」中配置了
旧的权限名称，请更新为新的权限名称并重新爬取（或重新索引）。如果没有使用 CN 中包含逗号等转义字符
的组，权限名称不会发生变化。

``ldap.role.search.user.enabled`` 的行为变更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 15.7 之前，即使设置了 ``ldap.role.search.user.enabled=false``\ ，仍会授予从用户名派生的权限
（``role.search.user.prefix`` 加用户名）。从 15.10 开始该设置将实际生效，为 ``false`` 时不再授予。

在设置为 ``false`` 的环境中，升级后用户会失去以自身命名的权限，因此针对单个用户设置了权限的文档
将无法被该用户检索到。若要保持原有行为，请恢复为随附的默认值 ``true``\ 。

若此前修改过 /api/v2 配置键
------------------------------------------------

从 15.8.0 起，有四个配置键去掉了 ``api.v2.`` 前缀。其取值、默认值和行为均未改变，但\
**没有保留向后兼容的别名**\ ：仍使用旧名称的设置会被静默忽略，实际生效的是随附的默认值。

.. list-table::
   :header-rows: 1

   * - 15.7 及以前
     - 15.8.0 及以后
     - 默认值
   * - ``api.v2.chat.stream.keepalive.interval.ms``
     - ``api.chat.stream.keepalive.interval.ms``
     - ``15000``
   * - ``api.v2.param.max.length``
     - ``api.param.max.length``
     - ``1000``
   * - ``api.v2.param.max.array.size``
     - ``api.param.max.array.size``
     - ``100``
   * - ``api.v2.click.max.rt``
     - ``api.click.max.timestamp``
     - ``9999999999999``

如果曾在 ``fess_config.properties`` 中或通过 ``-Dfess.config.<键>`` JVM 参数设置过这些键，\
请改用新名称。只有显式设置过的情况才会受影响；从未修改过的环境无需处理。

第一个键决定 ``POST /api/v2/chat/stream`` 等待模型响应期间发送 keep-alive 帧的间隔，\
因此设置失效会在 AI 搜索模式中显现。最后一个键的改名也是为了更准确：它限制的是点击日志中\
``rt`` 的取值上限，而该值是时间戳而非响应时间。


.. _upgrade-plugin-versions:

插件版本更新
------------------------

安装在 ``app/WEB-INF/plugin/`` 中的插件，需要替换为与 |Fess| 版本对应的版本。
``bin/fess-setup upgrade plugins`` 会针对所有已安装的插件，安装为此 |Fess| 构建的版本并删除旧版本。
之后请重启 |Fess| 。 ``bin/fess-setup check`` 会报告 OpenSearch 及其插件、已安装的 |Fess| 插件的
状态，出现问题时以退出码 1 结束。它不会读取 ``bin/fess.in.sh`` 、 ``/etc/sysconfig/fess`` 和
``/etc/default/fess`` ，因此当 OpenSearch 不在 ``http://localhost:9200`` 时，请指定 ``--url`` ，
或在运行它的 shell 中设置 ``SEARCH_ENGINE_HTTP_URL`` ；否则它会报告无法连接到引擎。

::

    $ bin/fess-setup upgrade plugins
    $ bin/fess-setup check

``upgrade plugins`` 只处理已安装的插件。 ``fess-script-groovy`` 等用于补充 15.10 从发行包中移除
部分的插件，请按照前面各节的说明，使用 ``bin/fess-setup install plugin`` 安装。

如果在 Docker 版中指定了 ``FESS_PLUGINS``，请按照 ``fess-ds-wikipedia:15.10.0``
的形式更新版本号部分。

回滚步骤
==============

如果升级失败，可以按照以下步骤回滚。

步骤 1: 停止新版本
------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

步骤 2: 恢复旧版本
----------------------------

从备份恢复配置文件和数据。

RPM/DEB 版的情况::

    $ sudo rpm -Uvh --oldpackage --nodeps fess-<old-version>.rpm

或::

    $ sudo dpkg -i fess-<old-version>.deb

.. note::

   RPM 需要 ``--nodeps`` 。15.8.0 的软件包要求存在 ``fess`` 和 ``opensearch`` 用户及组，不指定时
   ``rpm`` 会以 ``Failed dependencies: group(fess) is needed by fess-15.8.0`` 拒绝降级。

.. warning::

   15.8.0 的 DEB 软件包没有将 ``/etc/fess/*`` 注册为 conffile，因此 ``dpkg -i`` 会覆盖编辑过的
   ``/etc/fess/fess_config.properties`` 等文件，且不保留副本。请从步骤 1 中获取的备份恢复。

步骤 3: 恢复数据
----------------------

从快照恢复。请保持 OpenSearch 运行，|Fess| 停止：

1. 启动 OpenSearch::

       $ sudo systemctl start opensearch.service

2. 快照无法恢复到已存在的索引之上，因此请先删除所有 Fess 的索引，包括升级后（例如通过重新索引）
   创建的索引，以及 OpenSearch 插件创建的 ``configsync`` 索引。如果只删除快照中包含的索引，
   重新索引创建的索引会残留，``fess.search`` 会指向两个索引，15.8.0 无法启动::

       $ curl "http://localhost:9200/_cat/indices/fess*,configsync?h=index"
       $ curl -X DELETE "http://localhost:9200/<index name>"

   对第一条命令列出的每个索引，分别执行第二条命令。

3. 恢复快照::

       $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

.. note::

   词典目录（``configsync.config_path`` ，其中包含词典文件）必须与以前一样存在。在丢失了该目录的
   机器上，恢复虽然会完成，但使用词典的索引会一直是 red 状态。

或从备份恢复目录（请指定步骤 1 中创建的归档文件名）::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-<YYYYMMDD>.tar.gz -C /
    $ sudo systemctl start opensearch

Docker 版中，请先切换回旧版本的 Compose 文件，再恢复卷中的内容::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   从管理页面下载的配置数据，可在 |Fess| 启动后，通过「系统信息」→「备份」
   页面的上传功能重新导入并恢复。可以上传的文件仅限于
   ``*.bulk``\ 、以 ``system``\ 开头的 ``*.properties``\ 、以 ``gsa``\ 开头的 ``*.xml``\ 、
   以 ``fess``\ 开头的 ``*.json``\ 、以 ``doc``\ 开头的 ``*.json``\ ，且每次操作只能上传 1 个文件。
   搜索日志等 ``*.ndjson`` 文件不被接受，会导致错误。

.. warning::

   上传 ``fess.json`` 和 ``doc.json`` 会覆盖 |Fess| 自带的索引定义文件本身。
   升级后如果上传旧版本的 ``fess.json`` 或 ``doc.json``，会导致新版本的索引设置和映射丢失。
   请勿在回滚以外的目的下上传这些文件。

.. note::

   上传的 ``system.properties`` 仅会加载到内存中，不会写入文件。
   因此 ``system.properties`` 的内容会在 |Fess| 重启后丢失。
   如需确保可靠恢复，请将备份的文件直接放置到指定位置（ZIP 版为
   ``app/WEB-INF/conf/``\ ，RPM/DEB 版为 ``/etc/fess/``\ ）后再启动。

.. note::

   导入操作以异步方式执行，画面上仅会显示已开始的提示。
   请通过 ``fess.log`` 确认是否真正成功。

步骤 4: 启动和确认服务
----------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

确认运行并验证已恢复正常。

常见问题
==========

Q: 可以无停机时间升级吗？
--------------------------------------------

A: Fess 的升级需要停止服务。要最小化停机时间，请考虑以下方法：

- 提前在测试环境确认步骤
- 提前获取备份
- 确保充足的维护时间

Q: 需要升级 OpenSearch 吗？
-------------------------------------------------

A: 每个 |Fess| 版本对应特定的 OpenSearch 版本。
|Fess| 15.10 对应 OpenSearch 3.9.0。
由于 ``opensearch-analysis-fess`` 等 |Fess| 专用 OpenSearch 插件必须与 OpenSearch 版本完全一致，
因此在升级 OpenSearch 时，请同时将插件更新为对应版本（3.9.0）。

另外，|Fess| 15.10 强制要求安装 k-NN 插件，并会在索引设置中始终发送
``knn.derived_source.enabled``。如果 OpenSearch 版本过旧，会导致新索引创建失败，
因此实质上必须升级 OpenSearch。详情请参阅步骤 4。

Q: 需要重建索引吗？
------------------------------------------

A: 对于 |Fess| 的小版本升级（15.x → 15.10），如果不使用分块向量搜索，
通常不需要重建索引。现有索引可以直接使用，\ ``content_chunker.enabled`` 等选项默认为
禁用，因此行为不会改变。

以下情况需要重建索引并重新索引。

- **新启用分块向量搜索（语义搜索）时**: 由于现有索引不会反映新的映射，
  必须进行重新索引。详情请参阅
  :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）。
- **从 14.x 升级时**: 由于 OpenSearch 会从 2.x 主版本升级到 3.x，
  建议重建索引。
- **在由 15.8 或更早版本创建的文档索引上使用所有者搜索或假名规范化时**: 需要重新索引。
  详情请参阅 :ref:`upgrade-reindex-new-fields`\ 。

.. warning::

   新建索引的操作（包括重新索引）在没有 k-NN 插件的 OpenSearch 中会失败。
   请确认步骤 4 中的注意事项。

Q: 升级后搜索结果不显示
------------------------------------------

A: 请确认以下内容：

1. 确认 OpenSearch 是否启动
2. 确认索引是否存在（``curl http://localhost:9200/_cat/indices``）
3. 重新执行爬取

下一步
==========

升级完成后：

- :doc:`run` - 确认启动和初始设置
- :doc:`security` - 重新检查安全配置
- :doc:`../config/search-semantic` - 分块向量搜索（语义搜索）的配置与迁移步骤
- 在发布说明中确认新功能
