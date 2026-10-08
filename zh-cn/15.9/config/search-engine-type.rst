============
搜索引擎类型
============

概述
====

|Fess| 将数据保存在 OpenSearch 中。 ``search_engine.type`` 用于告知 |Fess| 所连接的 OpenSearch 是哪一种类型，\ |Fess| 创建的索引定义和可用的功能都由它决定。

默认值 ``default`` 以安装了 CodeLibs 的 4 个插件（ ``opensearch-analysis-fess`` 、 ``opensearch-analysis-extension`` 、 ``opensearch-minhash`` 、 ``opensearch-configsync`` ）的 OpenSearch 为前提（请参阅 :doc:`../install/install` ）。如果要连接到不含这些插件的原生 OpenSearch（例如无法自行安装插件的托管服务），请指定 ``vanilla`` 。

类型
====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 值
     - 说明
   * - ``default``
     - 安装了 CodeLibs 插件的 OpenSearch。默认值。
   * - ``vanilla``
     - 不含 CodeLibs 插件的原生 OpenSearch。15.9 新增。索引定义从 ``fess_indices/_vanilla/`` 读取。\ |Fess| 15.8 及更早版本无法识别该值，请在这些版本中指定 ``cloud`` 。
   * - ``aws``
     - 与 ``vanilla`` 相同，用于 Amazon OpenSearch Service（请参阅 :ref:`search-engine-type-aws` ）。
   * - ``cloud``
     - ``vanilla`` 的已弃用别名。启动时会在日志中输出警告。请改为 ``vanilla`` 。
   * - 其他值
     - 与 ``default`` 同样处理。但 ``fess_indices/_<类型>/`` 中的定义文件优先于 ``fess_indices/`` 中的同名文件。

|Fess| 不会自动判断是否安装了插件，需要由用户指定类型。请在首次启动之前设置。索引定义是在创建索引时应用的，因此之后更改该值也不会改变已经创建的索引。

没有插件时无法使用的功能
========================

使用 ``vanilla`` 和 ``aws`` （包括已弃用的 ``cloud`` ）时，无法使用以下功能。依赖这些功能的管理界面项目不会显示。

* **字典管理**\ ：不显示 [系统 > 字典]。字典管理页面和字典管理 API（ ``/api/admin/dict/`` ）也无法使用。维护页面中的“重置字典”和“重新加载文档索引”同样不会显示。Analyzer 使用索引定义中包含的规则，而不是字典文件。
* **折叠重复的搜索结果**\ ：“常规”中的“折叠重复结果”不会显示，并且始终为禁用状态。
* **重复文档检测**\ ：不会计算用于查找内容相同的文档的内容签名。文档报告的“重复文档”选项卡不会显示（“休眠文档”仍可使用）。用于查找相似文档的搜索参数 ``sdh`` 会被忽略。
* **Analyzer**\ ：日语、韩语和简体中文不使用 CodeLibs 的分词器，而是使用 OpenSearch 标准的 Kuromoji、Nori 和 SmartCN Analyzer 进行切分，因此切分结果与 ``default`` 不同。越南语（ ``*_vi`` 字段）和繁体中文（ ``*_zh-tw`` 字段）使用不登记任何词语的空 Analyzer。这些语言的文档仍会登记到与语言无关的 ``content`` 字段和 ``title`` 字段中。

所需的 OpenSearch 插件
======================

``vanilla`` 和 ``aws`` 的索引定义使用 OpenSearch 官方插件提供的 Analyzer 和向量字段类型。所连接的 OpenSearch 需要安装以下插件。

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` （k-NN）

不需要 CodeLibs 的插件。对于自行运维的 OpenSearch，请使用 ``opensearch-plugin install`` 安装，例如 ``bin/opensearch-plugin install analysis-nori`` 。关于 Amazon OpenSearch Service，请参阅 :ref:`search-engine-type-aws` 。

当类型为 ``vanilla`` 或 ``aws`` 时，\ |Fess| 会在启动时列出已安装的插件（ ``GET /_cat/plugins`` ）。只要缺少上述插件中的任何一个，就会在日志中输出一条指出缺少哪些插件的警告，并继续启动。如果因服务不允许该 API 等原因导致请求失败，则跳过检查。

设置类型
========

Docker
------

在 ``compose.yaml`` 的 ``fess01`` 服务中指定环境变量 ``SEARCH_ENGINE_TYPE`` 。

::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` 可用于 |Fess| 15.9 及更高版本的镜像。使用更早的镜像时，请指定 ``SEARCH_ENGINE_TYPE=cloud`` 。其他 Docker 设置请参阅 :doc:`../install/install-docker` 。

非 Docker 环境
--------------

``bin/fess.in.sh`` 不会读取 ``SEARCH_ENGINE_TYPE`` 。请使用以下任一方法指定。

* 在 ``fess_config.properties`` 中写入 ``search_engine.type`` （ZIP 版为 ``app/WEB-INF/classes/fess_config.properties`` ，RPM/DEB 版为 ``/etc/fess/fess_config.properties`` ）。
* 在 ZIP 版的 ``bin/fess.in.sh`` （Windows 为 ``bin\fess.in.bat`` ）中，向 ``FESS_JAVA_OPTS`` 追加 JVM 选项。

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

更改后请重启 |Fess| 。爬虫等作业进程会从 |Fess| 继承该设置，因此无需单独指定。

连接设置
========

与 OpenSearch 的连接，其设置方法与其他类型相同。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 设置
     - 说明
   * - ``search_engine.http.url``
     - OpenSearch 的 HTTP 端点。如果指定了环境变量 ``SEARCH_ENGINE_HTTP_URL`` ，则以该环境变量为准。
   * - ``search_engine.username`` / ``search_engine.password``
     - HTTP Basic 认证的用户名和密码。仅在两者都指定时才会使用。在 Docker 中，通过环境变量 ``SEARCH_ENGINE_USERNAME`` 和 ``SEARCH_ENGINE_PASSWORD`` 指定。
   * - ``search_engine.http.ssl.certificate_authorities``
     - 用于验证 HTTPS 端点的服务器证书的 CA 证书文件（X.509）的路径。如果证书由 Java 默认信任的 CA 签发，则不需要。

``fess_config.properties`` 的项目也可以在 ``FESS_JAVA_OPTS`` 中以 ``-Dfess.config.<项目名>`` 的形式指定来覆盖（请参阅 :doc:`../install/install-docker` ）。

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

使用 Amazon OpenSearch Service 的域时，请将 ``search_engine.type`` 指定为 ``aws`` （ ``vanilla`` 的行为相同）。

前提条件
--------

* 域的 OpenSearch 为 3.x。\ |Fess| 会在启动时检查引擎，如果不是 OpenSearch 3 则不会启动。
* “所需的 OpenSearch 插件”中列出的插件可在该域中使用。在 Amazon OpenSearch Service 中，Nori 是可选软件包，请在启动 |Fess| 之前将其关联到该域。
* 端点使用 HTTPS。
* 已启用细粒度访问控制（fine-grained access control），并创建了供 |Fess| 登录的内部用户（HTTP Basic 认证）。目前尚不支持使用 AWS IAM 凭证对请求签名（SigV4），因此无法使用只接受 IAM 签名请求的域。

配置示例
--------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

启动时的检查
------------

* 类型为 ``aws`` 时，同样会执行“所需的 OpenSearch 插件”中说明的插件检查。如果忘记关联 Nori，\ ``fess.log`` 中会输出警告。
* 如果域以 HTTP 401 或 403 拒绝请求，\ |Fess| 会在日志中输出警告。因此导致启动失败时，错误消息中会提示检查用户名、密码和域的访问策略。

DNS 缓存的 TTL
--------------

托管服务的端点可能会随时间解析为不同的 IP 地址，而 JVM 会缓存 DNS 的解析结果。将缓存时间设置得较短，\ |Fess| 就能跟上地址的变化。请在以下两处指定 ``-Dsun.net.inetaddr.ttl=5`` （单位为秒）。

1. |Fess| 主体：追加到 ``FESS_JAVA_OPTS`` 中。

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. 作业进程：爬虫、建议、分块和缩略图进程由 |Fess| 作为独立的 JVM 启动，不会继承 ``FESS_JAVA_OPTS`` 。请在 ``fess_config.properties`` 的 ``jvm.crawler.options`` 、 ``jvm.suggest.options`` 、 ``jvm.chunk.options`` 和 ``jvm.thumbnail.options`` 末尾追加相同的选项。这些值每行写一个选项，每行以 ``\n\`` 结尾。

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   请在现有各行之后追加该行，其余 3 个项目也同样处理。

在 Docker 中，请通过 Compose 文件的环境变量指定 ``FESS_JAVA_OPTS`` 。要更改 ``jvm.*.options`` ，请挂载修改后的 ``fess_config.properties`` （请参阅 :doc:`../install/install-docker` ）。
