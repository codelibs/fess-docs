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

.. important::

   |Fess| 14.x 对应 OpenSearch 2.x 系列，\ |Fess| 15.8 对应 OpenSearch 3.8.0。
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
- :doc:`prerequisites` - |Fess| 15.8 的系统要求（Java、OpenSearch 版本）

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
     缩略图队列等运行时数据，共 25 个索引
   - ``fess_user.bulk`` - 用户、角色、群组
   - ``system.properties`` - 包含常规设置的系统设置
   - ``fess.json`` - 索引设置（分片数、\ ``index.knn`` 等）
   - ``doc.json`` - 文档映射（字段定义）

   .. note::

      ``fess_config.bulk`` 包含 ``fess_basic_config.bulk``。作为升级前的
      配置备份，\ ``fess_basic_config.bulk``\ 、\ ``fess_user.bulk``\ 、
      ``system.properties`` 这 3 个文件就已足够。

   .. note::

      搜索日志、点击日志等日志数据（``search_log.ndjson``、``click_log.ndjson``、
      ``favorite_log.ndjson``、``user_info.ndjson``）也可从同一页面下载。
      如果仅备份配置，则不需要下载这些文件。另外，这些 ``*.ndjson`` 文件无法
      通过备份页面的上传功能重新导入恢复
      （请参阅「回滚步骤」）。

2. **备份配置文件**

   TAR.GZ/ZIP 版::

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
      TAR.GZ/ZIP 版中与之对应的设置位于 ``bin/fess.in.sh``。

3. **定制的配置文件**

   如有定制的配置文件，也请备份::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

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

TAR.GZ/ZIP 版没有附带用于停止的脚本。\ ``bin/fess`` 如果是使用 ``-p`` 选项
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

步骤 3: 安装新版本
======================================

根据安装方法，步骤有所不同。

TAR.GZ/ZIP 版
-------------

1. 下载并解压新版本::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.zip
       $ unzip fess-15.8.0.zip

   .. note::

      |Fess| 的归档版仅以 ZIP 格式发布（不提供
      ``fess-15.8.0.tar.gz``）。

2. 复制旧版本的配置::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.8.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. 如有定制内容，请同时复制以下文件::

       # 日志配置
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.8.0/app/WEB-INF/classes/
       # 已安装的插件
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.8.0/app/WEB-INF/plugin/
       # 主题
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.8.0/app/themes/

   .. warning::

      在管理页面「页面设计」中编辑过的 JSP（``app/WEB-INF/view/``），请不要直接复制过去。
      如果新版本的 JSP 结构发生了变化，画面可能无法正常显示。
      请将修改内容重新应用到新版本的 JSP 上。

4. 如果使用内置 OpenSearch（未设置 ``SEARCH_ENGINE_HTTP_URL`` 而直接启动 ``bin/fess`` 的
   配置），请同时复制索引数据::

       $ cp -r /path/to/old-fess/es/data/. /path/to/fess-15.8.0/es/data/

5. 确认配置差异，根据需要进行调整

RPM/DEB 版
----------

安装新版本的包::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   RPM 版中，``/etc/fess/*`` 的配置文件被注册为 ``%config(noreplace)``，
   因此在升级时会被保留（新的默认文件会以 ``.rpmnew`` 的形式并存）。
   如果添加了新的配置选项，需要手动调整。

.. warning::

   DEB 版中，``/etc/fess/*`` 并未注册为 conffile（conffile 仅有
   ``/etc/default/fess``\ 、\ ``/etc/init.d/fess``\ 、\ ``/usr/lib/systemd/system/fess.service``
   这 3 个）。因此执行 ``dpkg -i`` 时，``/etc/fess/fess_config.properties`` 等文件会被
   新版本的文件覆盖。请在升级后，重新应用步骤 1 中备份的配置。
   另外，``/etc/fess/system.properties`` 是不包含在软件包中的运行时生成文件，
   因此不会被覆盖。

Docker 版
---------

1. 获取新版本的 Compose 文件::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. 获取新镜像::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

步骤 4: 升级 OpenSearch
====================================

|Fess| 15.8 对应 OpenSearch 3.8.0。如果所连接的 OpenSearch 版本比这更旧，
请按照以下步骤升级。

.. note::

   本步骤适用于 TAR.GZ/ZIP 版及 RPM/DEB 版中手动运维 OpenSearch 的情况。
   对于 Docker 版，在步骤 3 中获取新镜像时，OpenSearch 和插件也会一并更新，
   因此无需执行本步骤。

.. important::

   无论是否使用分块向量搜索（语义搜索），\ |Fess| 15.8 都会在搜索索引的设置中始终
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

1. 安装新版本的 OpenSearch

2. 重新安装插件::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      这些插件的版本必须与所使用的 OpenSearch 版本一致。
      |Fess| 15.8 对应 OpenSearch 3.8.0。如果版本不一致，
      插件安装将会失败。

3. 启动 OpenSearch::

       $ sudo systemctl start opensearch.service

步骤 5: 启动新版本
================================

TAR.GZ/ZIP 版::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d -p /path/to/fess-15.8.0/fess.pid

.. note::

   指定 ``-p`` 后会创建 PID 文件，下次停止时可以使用
   ``kill $(cat /path/to/fess-15.8.0/fess.pid)`` 来停止。

RPM/DEB 版::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

步骤 6: 运行确认
==================

1. **确认日志**

   确认没有错误。

   TAR.GZ/ZIP 版::

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

1. 确认现有爬取计划
2. 从「系统」→「调度器」执行「Default Crawler」
3. 等待爬取完成
4. 确认搜索结果

.. warning::

   由于重新索引会以新的映射重建索引，在没有 k-NN 插件的 OpenSearch 中会失败。
   请确认步骤 4 中的注意事项。

15.8 特有的迁移工作
===================

从 15.7 及更早版本升级到 15.8 时，需要根据所使用的功能执行以下工作。

若此前使用过语义搜索
----------------------------------

在 |Fess| 15.7 及更早版本中提供语义搜索功能的 ``fess-webapp-semantic-search`` 插件，
已在 15.8 中并入核心，现已不再需要（已弃用）。需要移除该插件、删除
``-Dfess.semantic_search.*`` 及 ``-Drank.fusion.searchers=default,semantic``\ ，
并解除旧的 ingest pipeline。详细步骤请参阅
:ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）。

若此前使用过 AI 搜索模式（RAG Chat）
---------------------------------------------

自 15.8 起，AI 搜索模式（RAG Chat）功能已拆分为 ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、
``fess-llm-gemini`` 等插件。请在管理页面「系统」→「插件」中安装与所使用的
提供商对应的插件。

若此前使用过 SPNEGO（Windows 集成认证）
---------------------------------------

自 15.8 起，如果客户端主体的 Kerberos 领域与服务器的领域不同，SPNEGO 登录将被拒绝。
如果用户来自 AD 域树的子域或建立了信任关系的林，请在管理页面「系统」→「通用」或
``app/WEB-INF/conf/system.properties`` 的 ``spnego.allowed.realms`` 中以逗号分隔列出
这些领域。否则，在 15.7 之前能够登录的用户将因 ``Kerberos realm is not allowed`` 而被拒绝。
详细内容请参阅 :doc:`../config/sso-spnego`\ 。

此外，15.8 中 ``spnego.allow.unsecure.basic`` 与 ``spnego.allow.localhost`` 的代码默认值也从
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
   升级到 15.8 并不会使其变得更严格：宽松的行为会被静默沿用，15.8 只会在 SPNEGO 初始化时
   向 ``fess.log`` 输出一条警告。请在管理页面「系统」→「通用」或 ``system.properties`` 中
   有意识地关闭这两项。其中 ``spnego.allow.localhost=true`` 更为危险：SPNEGO 库会把来自同一
   主机的请求以服务器的 OS 用户身份进行认证，完全不做 Kerberos 验证，在同一主机上部署反向
   代理时并不安全。

若此前使用过 SAML 认证（SSO）
-----------------------------

自 15.8 起，|Fess| 会将每个 SAML 响应与自身发出的 AuthnRequest 的 ID 进行绑定校验，
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
因此即使站点看起来正常，也请确认该设置。15.8 不再循环，而是一次性失败。
详细内容请参阅 :doc:`../config/sso-saml`\ 。

若此前使用过 Microsoft Entra ID（Azure AD）
-------------------------------------------

自 15.8 起，向授权端点请求的响应模式默认值由 ``form_post`` 变更为 ``query``\ 。15.7 之前回调以
跨站 POST 返回，而 |Fess| 的默认值 ``tomcat.sameSiteCookies = lax`` 不会随该请求发送会话
Cookie，因此需要将其改为 ``tomcat.sameSiteCookies = none``\ 。如果仅为此才设置了 ``none``\ ，
可以恢复为默认值。若要保持原有行为，请指定 ``entraid.response.mode=form_post`` 并保留
``tomcat.sameSiteCookies = none``\ 。

自 15.8 起，|Fess| 还会在登录完成后于后台解析用户所属的组和角色，而不再让登录等待 Microsoft
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

插件版本更新
------------------------

安装在 ``app/WEB-INF/plugin/`` 中的插件，需要替换为与 |Fess| 版本对应的版本。
如果在 Docker 版中指定了 ``FESS_PLUGINS``，请按照 ``fess-ds-wikipedia:15.8.0``
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
   如需确保可靠恢复，请将备份的文件直接放置到指定位置（TAR.GZ/ZIP 版为
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
|Fess| 15.8 对应 OpenSearch 3.8.0。
由于 ``opensearch-analysis-fess`` 等 |Fess| 专用 OpenSearch 插件必须与 OpenSearch 版本完全一致，
因此在升级 OpenSearch 时，请同时将插件更新为对应版本（3.8.0）。

另外，|Fess| 15.8 强制要求安装 k-NN 插件，并会在索引设置中始终发送
``knn.derived_source.enabled``。如果 OpenSearch 版本过旧，会导致新索引创建失败，
因此实质上必须升级 OpenSearch。详情请参阅步骤 4。

Q: 需要重建索引吗？
------------------------------------------

A: 对于 |Fess| 的小版本升级（15.x → 15.8），如果不使用分块向量搜索，
通常不需要重建索引。现有索引可以直接使用，\ ``content_chunker.enabled`` 等选项默认为
禁用，因此行为不会改变。

以下情况需要重建索引并重新索引。

- **新启用分块向量搜索（语义搜索）时**: 由于现有索引不会反映新的映射，
  必须进行重新索引。详情请参阅
  :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）。
- **从 14.x 升级时**: 由于 OpenSearch 会从 2.x 主版本升级到 3.x，
  建议重建索引。

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
