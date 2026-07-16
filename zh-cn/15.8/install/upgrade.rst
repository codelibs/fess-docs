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

- Fess 14.x → Fess 15.8
- Fess 15.x → Fess 15.8

.. note::

   如果从更旧的版本（13.x 及更早）升级，可能需要逐步升级。
   详情请确认发布说明。

升级前的准备
====================

确认版本兼容性
--------------------

请确认升级目标版本与当前版本的兼容性。

- `发布说明 <https://github.com/codelibs/fess/releases>`__
- `升级指南 <https://fess.codelibs.org/zh-cn/>`__

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
   点击各链接下载（不是单个 ZIP 文件，而是按条目分别下载的独立文件）。

   - ``fess_basic_config.bulk`` - 基本设置（常规设置）
   - ``fess_config.bulk`` - 爬取设置、调度器、标签、关键词匹配等配置信息
   - ``fess_user.bulk`` - 用户、角色、群组
   - ``system.properties`` - 系统设置
   - ``fess.json`` / ``doc.json`` - 索引设置（映射）

   .. note::

      搜索日志、点击日志等日志数据（``search_log.ndjson``、``click_log.ndjson``、
      ``favorite_log.ndjson``、``user_info.ndjson``）也可从同一页面下载。
      如果仅备份配置，则不需要下载这些文件。

2. **备份配置文件**

   TAR.GZ/ZIP 版::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   RPM/DEB 版::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **定制的配置文件**

   如有定制的配置文件，也请备份::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

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

停止容器后，备份卷::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

步骤 2: 停止当前版本
================================

停止 Fess 和 OpenSearch。

TAR.GZ/ZIP 版::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 版 (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

步骤 3: 安装新版本
======================================

根据安装方法，步骤有所不同。

TAR.GZ/ZIP 版
------------

1. 下载并解压新版本::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.tar.gz
       $ tar -xzf fess-15.8.0.tar.gz

2. 复制旧版本的配置::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. 确认配置差异，根据需要进行调整

RPM/DEB 版
---------

安装新版本的包::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   配置文件（``/etc/fess/*``）会自动保留。
   但是，如果添加了新的配置选项，需要手动调整。

Docker 版
--------

1. 获取新版本的 Compose 文件::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. 获取新镜像::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

步骤 4: 升级 OpenSearch（如需要）
=================================================

如果要升级 OpenSearch，请按照以下步骤操作。

.. note::

   本步骤适用于 TAR.GZ/ZIP 版及 RPM/DEB 版中手动运维 OpenSearch 的情况。
   对于 Docker 版，在步骤 3 中获取新镜像时，OpenSearch 和插件也会一并更新，
   因此无需执行本步骤。

.. warning::

   OpenSearch 的主版本升级需要谨慎进行。
   可能会出现索引兼容性问题。

1. 安装新版本的 OpenSearch

2. 重新安装插件::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. note::

      这些插件的版本必须与所使用的 OpenSearch 版本一致。
      Fess 15.8 对应 OpenSearch 3.7.0。如果版本不一致，
      插件安装将会失败。

3. 启动 OpenSearch::

       $ sudo systemctl start opensearch.service

步骤 5: 启动新版本
================================

TAR.GZ/ZIP 版::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d

RPM/DEB 版::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

步骤 6: 运行确认
==================

1. **确认日志**

   确认没有错误::

       $ tail -f /path/to/fess/logs/fess.log

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

1. 确认现有爬取计划
2. 从「系统」→「调度器」执行「Default Crawler」
3. 等待爬取完成
4. 确认搜索结果

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

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

或::

    $ sudo dpkg -i fess-<old-version>.deb

步骤 3: 恢复数据
----------------------

从快照恢复::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

或从备份恢复目录::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

.. note::

   从管理页面下载的配置数据（``*.bulk`` 文件），可在 Fess 启动后，
   通过「系统信息」→「备份」页面的上传功能重新导入并恢复。

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

A: 每个 Fess 版本对应特定的 OpenSearch 版本。
Fess 15.8 对应 OpenSearch 3.7.0。
由于 ``opensearch-analysis-fess`` 等 Fess 专用 OpenSearch 插件必须与 OpenSearch 版本完全一致，
因此在升级 OpenSearch 时，请同时将插件更新为对应版本（3.7.0）。

Q: 需要重建索引吗？
------------------------------------------

A: 小版本升级通常不需要，但主版本升级建议重建。

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
- 在发布说明中确认新功能
