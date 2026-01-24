==================
故障排除
==================

本页面说明 |Fess| 的安装、启动、运维时的常见问题及其解决方法。

安装时的问题
==================

Java 未被识别
-----------------

**症状:**

::

    -bash: java: command not found

或::

    'java' is not recognized as an internal or external command

**原因:**

Java 未安装，或 PATH 环境变量未正确设置。

**解决方法:**

1. 确认 Java 是否已安装::

       $ which java
       $ java -version

2. 如未安装，请安装 Java 21::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. 设置 JAVA_HOME 环境变量::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   要永久设置，请添加到 ``~/.bashrc`` 或 ``/etc/profile``。

插件安装失败
-------------------------------

**症状:**

::

    ERROR: Plugin installation failed

**原因:**

- 网络连接问题
- 插件版本与 OpenSearch 版本不匹配
- 权限问题

**解决方法:**

1. 确认 OpenSearch 版本::

       $ /path/to/opensearch/bin/opensearch --version

2. 将插件版本与 OpenSearch 版本匹配::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1

3. 确认权限::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. 通过代理安装::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

启动时的问题
==========

Fess 无法启动
---------------

**症状:**

执行 Fess 的启动命令时出现错误或立即终止。

**确认项目:**

1. **确认 OpenSearch 是否启动**::

       $ curl http://localhost:9200/

   如果正常，会返回 JSON 响应。

2. **确认端口号冲突**::

       $ sudo netstat -tuln | grep 8080

   如果端口 8080 已被使用，请在配置文件中更改端口号。

3. **确认日志文件**::

       $ tail -f /path/to/fess/logs/fess.log

   从错误消息中找出原因。

4. **确认 Java 版本**::

       $ java -version

   请确认已安装 Java 21 或更高版本。

5. **确认内存不足**::

       $ free -h

   如果内存不足，请调整堆大小或增加系统内存。

OpenSearch 无法启动
---------------------

**症状:**

::

    ERROR: bootstrap checks failed

**原因:**

系统配置不满足 OpenSearch 的要求。

**解决方法:**

1. **设置 vm.max_map_count**::

       $ sudo sysctl -w vm.max_map_count=262144

   永久设置::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **增加文件描述符上限**::

       $ sudo vi /etc/security/limits.conf

   添加以下内容::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **设置内存锁定**::

       $ sudo vi /etc/security/limits.conf

   添加以下内容::

       opensearch  -  memlock  unlimited

4. 重启 OpenSearch::

       $ sudo systemctl restart opensearch

端口号冲突
--------------

**症状:**

::

    Address already in use

**解决方法:**

1. 确认使用中的端口::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. 停止使用中的进程，或更改 Fess 的端口号

   在配置文件 (``system.properties``) 中更改端口号::

       server.port=9080

连接问题
========

Fess 无法连接到 OpenSearch
-------------------------------

**症状:**

日志中显示以下错误::

    Connection refused
    或
    No route to host

**解决方法:**

1. **确认 OpenSearch 是否启动**::

       $ curl http://localhost:9200/

2. **确认连接 URL**

   确认 ``fess.in.sh`` 或 ``fess.in.bat`` 中设置的 URL 是否正确::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **确认防火墙**::

       $ sudo firewall-cmd --list-all

   确认端口 9200 是否开放。

4. **确认网络连接**

   如果在其他主机上运行 OpenSearch::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

无法从浏览器访问 Fess
----------------------------------

**症状:**

无法在浏览器中访问 http://localhost:8080/。

**解决方法:**

1. **确认 Fess 是否启动**::

       $ ps aux | grep fess

2. **尝试在本地主机访问**::

       $ curl http://localhost:8080/

3. **确认防火墙**::

       $ sudo firewall-cmd --list-all

   确认端口 8080 是否开放。

4. **从其他主机访问**

   确认 Fess 是否在本地主机以外监听::

       $ netstat -tuln | grep 8080

   如果是 ``127.0.0.1:8080``，请更改配置为 ``0.0.0.0:8080`` 或特定 IP 地址监听。

性能问题
==================

搜索速度慢
--------

**原因:**

- 索引大小大
- 内存不足
- 磁盘 I/O 慢
- 查询复杂

**解决方法:**

1. **增加堆大小**

   编辑 ``fess.in.sh``::

       FESS_HEAP_SIZE=4g

   同时调整 OpenSearch 的堆大小::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **优化索引**

   从管理页面的「系统」→「调度器」定期执行优化。

3. **使用 SSD**

   如果磁盘 I/O 是瓶颈，请迁移到 SSD。

4. **启用缓存**

   在配置文件中启用查询缓存。

爬取速度慢
-----------

**原因:**

- 爬取间隔长
- 目标网站响应慢
- 线程数少

**解决方法:**

1. **调整爬取间隔**

   在管理页面的爬取配置中缩短「间隔」（毫秒单位）。

   .. warning::

      间隔太短会对目标网站造成负担。请设置适当的值。

2. **增加线程数**

   在配置文件中增加爬取线程数::

       crawler.thread.count=10

3. **调整超时值**

   对于响应慢的网站，请增加超时值。

数据问题
==========

不显示搜索结果
--------------------

**原因:**

- 索引未创建
- 爬取失败
- 搜索查询错误

**解决方法:**

1. **确认索引**::

       $ curl http://localhost:9200/_cat/indices?v

   确认 |Fess| 的索引是否存在。

2. **确认爬取日志**

   从管理页面的「系统」→「日志」确认爬取日志，检查是否有错误。

3. **重新执行爬取**

   从管理页面的「系统」→「调度器」执行「Default Crawler」。

4. **简化搜索查询**

   先使用简单关键词搜索，确认是否返回结果。

索引损坏
------------------------

**症状:**

搜索时出现错误或返回意外结果。

**解决方法:**

1. **删除并重建索引**

   .. warning::

      删除索引会丢失所有搜索数据。请务必获取备份。

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **重新执行爬取**

   从管理页面执行「Default Crawler」，重建索引。

Docker 特有的问题
===============

容器无法启动
------------------

**症状:**

``docker compose up`` 容器无法启动。

**解决方法:**

1. **确认日志**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **确认内存不足**

   增加分配给 Docker 的内存（从 Docker Desktop 的设置）。

3. **确认端口冲突**::

       $ docker ps

   确认其他容器是否在使用端口 8080 或 9200。

4. **确认 Docker Compose 文件**

   确认 YAML 文件是否有语法错误::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

容器启动但无法访问 Fess
----------------------------------------

**解决方法:**

1. **确认容器状态**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **确认日志**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **确认网络设置**::

       $ docker network ls
       $ docker network inspect <network_name>

Windows 特有的问题
================

路径问题
--------

**症状:**

路径包含空格或日文时出现错误。

**解决方法:**

请安装到不包含空格或日文的目录。

例::

    C:\opensearch  (推荐)
    C:\Program Files\opensearch  (不推荐)

无法注册为服务
------------------------

**解决方法:**

使用 NSSM 等第三方工具注册为 Windows 服务。

详情请参阅 :doc:`install-windows`。

其他问题
==========

更改日志级别
--------------

要确认详细日志，请将日志级别更改为 DEBUG。

编辑 ``log4j2.xml``::

    <Logger name="org.codelibs.fess" level="debug"/>

重置数据库
--------------------

要重置配置，请删除 OpenSearch 的索引::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   执行此命令会删除所有配置数据。

支持信息
==========

如果问题无法解决，请使用以下支持资源：

社区支持
------------------

- **Issues**: https://github.com/codelibs/fess/issues

  报告问题时，请包含以下信息：

  - Fess 版本
  - OpenSearch 版本
  - 操作系统和版本
  - 错误消息（从日志中摘录）
  - 重现步骤

- **论坛**: https://discuss.codelibs.org/

商业支持
----------

如需商业支持，请联系 N2SM, Inc.：

- **网站**: https://www.n2sm.net/

收集调试信息
================

报告问题时，收集以下信息会有所帮助：

1. **版本信息**::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **系统信息**::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **日志文件**::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **配置文件**（删除机密信息后）::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **OpenSearch 状态**::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
