==========
卸载步骤
==========

本页面说明完全卸载 |Fess| 的步骤。

.. warning::

   **卸载前的重要注意事项**

   - 卸载会删除所有数据
   - 如有重要数据，请务必获取备份
   - 关于备份步骤，请参阅 :doc:`upgrade`

卸载前的准备
============

获取备份
--------

请备份必要的数据：

1. **配置数据**

   从管理页面的「系统」→「备份」下载。
   通过此操作，可以将各种配置（包括爬取配置）以及搜索日志等一并导出。

2. **定制的配置文件**

   TAR.GZ/ZIP 版::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB 版::

       $ sudo cp -r /etc/fess /backup/

.. note::

   |Fess| 的索引和大部分配置都保存在 OpenSearch 中。
   备份索引数据时，请使用 OpenSearch 的快照功能。
   详细步骤请参阅 :doc:`upgrade`。

停止服务
--------

卸载前，停止所有服务。

TAR.GZ/ZIP 版::

    $ ps aux | grep -E 'fess|opensearch'
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 版::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

TAR.GZ/ZIP 版的卸载
===================

步骤 1: 删除 Fess
-----------------

删除安装目录::

    $ rm -rf /path/to/fess-15.7.0

步骤 2: 删除 OpenSearch
-----------------------

删除 OpenSearch 的安装目录::

    $ rm -rf /path/to/opensearch-3.7.0

步骤 3: 删除数据目录（可选）
--------------------------

|Fess| 的索引数据保存在 OpenSearch 中。
默认情况下保存在 OpenSearch 的安装目录内（如 ``opensearch-3.7.0/data``），
但如果通过 ``path.data`` 指定了其他位置，请同时删除该目录::

    $ rm -rf /path/to/data

步骤 4: 删除日志目录（可选）
--------------------------

删除日志文件::

    $ rm -rf /path/to/fess-15.7.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

RPM 版的卸载
============

步骤 1: 卸载 Fess
-----------------

卸载 RPM 包::

    $ sudo rpm -e fess

.. note::

   卸载 |Fess| 包时，包的删除脚本会自动停止并禁用 ``fess`` 服务，
   并删除 ``fess`` 用户和组。
   后续步骤用于确认这些已被确实删除，或用于手动删除数据和配置文件。

步骤 2: 卸载 OpenSearch
-----------------------

::

    $ sudo rpm -e opensearch

步骤 3: 确认服务已禁用
--------------------

通常在删除包时服务会被禁用，但如需保险起见进行确认和禁用，请执行以下命令。

systemd 的情况::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

旧版 SysV init（chkconfig）环境的情况::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

步骤 4: 删除数据目录
------------------

.. warning::

   执行此操作会完全删除所有索引数据。

数据目录在卸载包时不会被删除，因此需要手动删除::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

步骤 5: 删除配置文件
------------------

删除配置文件和环境配置文件::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   在 RPM 中，``/etc/fess`` 内的配置文件可能会以 ``.rpmsave`` 的名称保留。
   要完全删除，请如上所述手动删除。

步骤 6: 删除日志文件
------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

步骤 7: 删除临时目录（可选）
--------------------------

::

    $ sudo rm -rf /var/tmp/fess

步骤 8: 删除用户和组（可选）
--------------------------

通常在删除包时 ``fess`` 用户和组会被删除。
如果仍有残留，或要删除 OpenSearch 用的用户和组，请执行以下命令::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

DEB 版的卸载
============

步骤 1: 卸载 Fess
-----------------

卸载 DEB 包::

    $ sudo dpkg -r fess

如需包括配置文件和环境配置文件在内完全删除，请使用 purge::

    $ sudo dpkg -P fess

.. note::

   使用 ``dpkg -r``（remove）时，作为配置文件（conffile）的 ``/etc/default/fess`` 等会保留。
   使用 ``dpkg -P``（purge）时，这些配置文件以及 ``fess`` 用户和组也会被删除。

步骤 2: 卸载 OpenSearch
-----------------------

::

    $ sudo dpkg -r opensearch

或者，包括配置文件一并删除::

    $ sudo dpkg -P opensearch

步骤 3: 确认服务已禁用
--------------------

通常在删除包时服务会被禁用。如需保险起见进行确认和禁用，请执行以下命令::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

步骤 4: 删除数据目录
------------------

.. warning::

   执行此操作会完全删除所有索引数据。

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

步骤 5: 删除配置文件（如未使用 dpkg -P）
------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

步骤 6: 删除日志文件
------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

步骤 7: 删除用户和组（可选）
--------------------------

如果未使用 ``dpkg -P``，则 ``fess`` 用户和组会保留。
如需删除，请执行以下命令::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Docker 版的卸载
===============

步骤 1: 删除容器和网络
--------------------

删除容器，以及 Docker Compose 创建的网络（``search_net``）::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

步骤 2: 删除卷
------------

.. warning::

   执行此操作会完全删除所有数据。

|Fess| 的数据（索引和词典等）保存在 OpenSearch 的卷中。
首先，确认卷列表::

    $ docker volume ls

删除 OpenSearch 相关的卷::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   卷名会带有 Docker Compose 的项目名（通常是放置 Compose 文件的目录名）作为前缀。
   请使用 ``docker volume ls`` 确认实际名称。

如需一并删除容器和卷，请在 ``down`` 后加上 ``-v`` 选项::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

步骤 3: 删除镜像（可选）
----------------------

如需删除 Docker 镜像以释放磁盘空间::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.7.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

步骤 4: 删除 Compose 文件
-----------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

确认卸载
========

确认所有组件已删除。

确认进程
--------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

如果没有显示任何内容，则进程已停止。

确认端口
--------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

确认端口未被使用。

确认文件
--------

TAR.GZ/ZIP 版::

    $ ls /path/to/fess-15.7.0  # 确认目录不存在

RPM/DEB 版::

    $ ls /var/lib/fess  # 确认目录不存在
    $ ls /etc/fess      # 确认目录不存在

Docker 版::

    $ docker ps -a | grep -E 'fess01|search01'  # 确认容器不存在
    $ docker volume ls | grep search01           # 确认卷不存在

确认包
------

RPM 版::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB 版::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

如果没有显示任何内容，则包已删除。

部分卸载
========

仅删除 Fess 保留 OpenSearch
---------------------------

如果 OpenSearch 也被其他应用程序使用，可以仅删除 Fess。

1. 停止 Fess
2. 删除 Fess 的包或目录
3. 删除 Fess 的数据目录（如 ``/var/lib/fess``）
4. 删除 OpenSearch 中创建的 |Fess| 索引（如 ``fess.*``、``.fess_*``）
5. 不删除 OpenSearch

仅删除 OpenSearch 保留 Fess
---------------------------

.. warning::

   删除 OpenSearch 后，Fess 将无法工作。
   请更改配置以连接到其他 OpenSearch 集群。

1. 停止 OpenSearch
2. 删除 OpenSearch 的包或目录
3. 删除 OpenSearch 的数据目录（如 ``/var/lib/opensearch``）
4. 更新 Fess 的配置以指定其他 OpenSearch 集群

故障排除
========

无法删除包
----------

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
----------

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
============

如果卸载后要重新安装，请确认以下内容：

1. 所有进程已停止
2. 所有文件和目录已删除
3. 端口 8080 和 9200 未被使用
4. 没有残留以前的配置文件

关于重新安装步骤，请参阅 :doc:`install`。

下一步
======

卸载完成后：

- 要安装新版本，请参阅 :doc:`install`
- 要迁移数据，请参阅 :doc:`upgrade`
- 要考虑替代的搜索解决方案，请参阅 Fess 官方网站
