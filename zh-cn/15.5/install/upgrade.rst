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

- Fess 14.x → Fess 15.5
- Fess 15.x → Fess 15.5

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

   登录管理页面，点击「系统」→「备份」。

   下载以下文件：

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

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

备份 Docker 卷::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v fess-es-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-es-data-backup.tar.gz /data
    $ docker run --rm -v fess-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-data-backup.tar.gz /data
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
-----------

1. 下载并解压新版本::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.5.0/fess-15.5.0.tar.gz
       $ tar -xzf fess-15.5.0.tar.gz

2. 复制旧版本的配置::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.5.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.5.0/bin/

3. 确认配置差异，根据需要进行调整

RPM/DEB 版
--------

安装新版本的包::

    # RPM
    $ sudo rpm -Uvh fess-15.5.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.5.0.deb

.. note::

   配置文件（``/etc/fess/*``）会自动保留。
   但是，如果添加了新的配置选项，需要手动调整。

Docker 版
-------

1. 获取新版本的 Compose 文件::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.5.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.5.0/compose/compose-opensearch3.yaml

2. 获取新镜像::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

步骤 4: 升级 OpenSearch（如需要）
=================================================

如果要升级 OpenSearch，请按照以下步骤操作。

.. warning::

   OpenSearch 的主版本升级需要谨慎进行。
   可能会出现索引兼容性问题。

1. 安装新版本的 OpenSearch

2. 重新安装插件::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

3. 启动 OpenSearch::

       $ sudo systemctl start opensearch.service

步骤 5: 启动新版本
================================

TAR.GZ/ZIP 版::

    $ cd /path/to/fess-15.5.0
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

4. **确认系统信息**

   在管理页面点击「系统」→「系统信息」，确认版本已更新。

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

A: 根据 Fess 版本，可能需要特定版本的 OpenSearch。
请在发布说明中确认推荐的 OpenSearch 版本。

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
