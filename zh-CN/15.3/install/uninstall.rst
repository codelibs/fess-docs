==================
卸载步骤
==================

本页面说明完全卸载 |Fess| 的步骤。

.. warning::

   **卸载前的重要注意事项**

   - 卸载会删除所有数据
   - 如有重要数据，必须获取备份
   - 关于备份步骤，请参阅 :doc:`upgrade`

卸载前的准备
======================

获取备份
----------------

请备份必要的数据：

1. **配置数据**

   从管理页面的「系统」→「备份」下载

2. **爬取配置**

   根据需要导出爬取配置

3. **定制的配置文件**

   TAR.GZ/ZIP 版::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB 版::

       $ sudo cp -r /etc/fess /backup/

停止服务
------------

卸载前，停止所有服务。

TAR.GZ/ZIP 版::

    $ ps aux | grep fess
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 版::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

TAR.GZ/ZIP 版的卸载
=============================

步骤 1: 删除 Fess
---------------------

删除安装目录::

    $ rm -rf /path/to/fess-15.3.0

步骤 2: 删除 OpenSearch
--------------------------

删除 OpenSearch 的安装目录::

    $ rm -rf /path/to/opensearch-3.3.0

步骤 3: 删除数据目录（可选）
-------------------------------------------

默认情况下，数据目录在 Fess 的安装目录内，
但如果指定了其他位置，也请删除该目录::

    $ rm -rf /path/to/data

步骤 4: 删除日志目录（可选）
-----------------------------------------

删除日志文件::

    $ rm -rf /path/to/fess/logs
    $ rm -rf /path/to/opensearch/logs

RPM 版的卸载
======================

步骤 1: 卸载 Fess
---------------------------------

卸载 RPM 包::

    $ sudo rpm -e fess

步骤 2: 卸载 OpenSearch
--------------------------------------

::

    $ sudo rpm -e opensearch

步骤 3: 禁用和删除服务
--------------------------------

chkconfig 的情况::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

systemd 的情况::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

步骤 4: 删除数据目录
----------------------------------

.. warning::

   执行此操作会完全删除所有索引数据和配置。

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

步骤 5: 删除配置文件
----------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

步骤 6: 删除日志文件
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

步骤 7: 删除用户和组（可选）
-------------------------------------------

删除系统用户和组::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

DEB 版的卸载
======================

步骤 1: 卸载 Fess
---------------------------------

卸载 DEB 包::

    $ sudo dpkg -r fess

包括配置文件完全删除::

    $ sudo dpkg -P fess

步骤 2: 卸载 OpenSearch
--------------------------------------

::

    $ sudo dpkg -r opensearch

或包括配置文件删除::

    $ sudo dpkg -P opensearch

步骤 3: 禁用服务
--------------------------

::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

步骤 4: 删除数据目录
----------------------------------

.. warning::

   执行此操作会完全删除所有索引数据和配置。

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

步骤 5: 删除配置文件（如未使用 dpkg -P）
---------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

步骤 6: 删除日志文件
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

步骤 7: 删除用户和组（可选）
-------------------------------------------

删除系统用户和组::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Docker 版的卸载
=========================

步骤 1: 删除容器和网络
------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

步骤 2: 删除卷
--------------------------

.. warning::

   执行此操作会完全删除所有数据。

确认卷列表::

    $ docker volume ls

删除 Fess 相关的卷::

    $ docker volume rm fess-es-data
    $ docker volume rm fess-data

或批量删除所有卷::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

步骤 3: 删除镜像（可选）
------------------------------------

删除 Docker 镜像以释放磁盘空间::

    $ docker images | grep fess
    $ docker rmi codelibs/fess:15.3.0

    $ docker images | grep opensearch
    $ docker rmi opensearchproject/opensearch:3.3.0

步骤 4: 删除网络（可选）
----------------------------------------

删除 Docker Compose 创建的网络::

    $ docker network ls
    $ docker network rm <network_name>

步骤 5: 删除 Compose 文件
--------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

确认卸载
====================

确认所有组件已删除。

确认进程
------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

如果没有显示任何内容，则进程已停止。

确认端口
----------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

确认端口未被使用。

确认文件
------------

TAR.GZ/ZIP 版::

    $ ls /path/to/fess-15.3.0  # 确认目录不存在

RPM/DEB 版::

    $ ls /var/lib/fess  # 确认目录不存在
    $ ls /etc/fess      # 确认目录不存在

Docker 版::

    $ docker ps -a | grep fess  # 确认容器不存在
    $ docker volume ls | grep fess  # 确认卷不存在

确认包
--------------

RPM 版::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB 版::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

如果没有显示任何内容，则包已删除。

部分卸载
======================

仅删除 Fess 保留 OpenSearch
-----------------------------------

如果 OpenSearch 被其他应用程序使用，可以仅删除 Fess。

1. 停止 Fess
2. 删除 Fess 的包或目录
3. 删除 Fess 的数据目录（``/var/lib/fess`` 等）
4. 不删除 OpenSearch

仅删除 OpenSearch 保留 Fess
-----------------------------------

.. warning::

   删除 OpenSearch 会导致 Fess 无法工作。
   请更改配置以连接到其他 OpenSearch 集群。

1. 停止 OpenSearch
2. 删除 OpenSearch 的包或目录
3. 删除 OpenSearch 的数据目录（``/var/lib/opensearch`` 等）
4. 更新 Fess 的配置以指定其他 OpenSearch 集群

故障排除
====================

无法删除包
----------------------

**症状:**

``rpm -e`` 或 ``dpkg -r`` 出现错误。

**解决方法:**

1. 确认服务已停止::

       $ sudo systemctl stop fess.service

2. 确认依赖关系::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. 强制删除（最后手段）::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

无法删除目录
------------------------

**症状:**

``rm -rf`` 无法删除目录。

**解决方法:**

1. 确认权限::

       $ ls -ld /path/to/directory

2. 使用 sudo 删除::

       $ sudo rm -rf /path/to/directory

3. 确认进程是否在使用文件::

       $ sudo lsof | grep /path/to/directory

重新安装的准备
==================

如果卸载后要重新安装，请确认以下内容：

1. 所有进程已停止
2. 所有文件和目录已删除
3. 端口 8080 和 9200 未被使用
4. 没有残留以前的配置文件

关于重新安装步骤，请参阅 :doc:`install`。

下一步
==========

卸载完成后：

- 要安装新版本，请参阅 :doc:`install`
- 要迁移数据，请参阅 :doc:`upgrade`
- 要考虑替代搜索解决方案，请参阅 Fess 官方网站
