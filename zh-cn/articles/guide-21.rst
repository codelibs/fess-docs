============================
统一搜索图像和文本（多模态）
============================

前言
====

文件服务器和内部网站上有大量图像，例如产品照片、现场照片等，除了文件名之外没有任何线索。
使用关键词搜索时，只能通过文件名或元数据中包含的词语找到图像。

使用多模态搜索插件 ``fess-webapp-multimodal``，就可以用“山间日落”“狗”这样的词语，搜索内容与之相近的图像。
本文将在 Fess 15.9 中完成以下操作。

- 以 15.9 版本启动用于验证的 Docker 环境 ``docker-multimodalsearch``，爬取图像并进行搜索
- 通过搜索 API 的响应，确认图像是通过向量找到的
- 掌握集成到现有 Fess 时所需的设置以及容易出错的地方

能做什么、不能做什么
====================

首先整理一下 15.9 中 ``fess-webapp-multimodal`` 的适用范围。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 15.9 中的行为
   * - 搜索方向
     - 仅支持用文本查找图像。没有上传图像来查找相似图像的功能
   * - 会被向量化的图像
     - 仅限 MIME 类型为 ``image/gif``、``image/jpeg``、``image/png`` 的文件。BMP 和 TIFF 不会被向量化
   * - PDF 或 Office 文档中的图像
     - 不会被向量化。如果要搜索图像中的文字，请使用 OCR（另一项功能）
   * - 图像以外的文档
     - 照常通过关键词搜索（BM25）进行搜索。搜索结果中图像和文本文档混合排列
   * - 英语以外的搜索词（如中文）
     - 使用支持多语言的 CLIP 模型。``docker-multimodalsearch`` 的默认模型是多语言模型，README 中说明它不限于英语（README 以日语为例）
   * - 文本的语义搜索
     - 不能在同一个 Fess 中同时使用（见后文）

关于 OCR，请参阅 `OCR（图像文字识别）配置 <https://fess.codelibs.org/zh-cn/stable/config/crawler-ocr.html>`__。

工作原理
========

CLIP 是一种将文本和图像转换到同一向量空间的模型。
“狗”这一文本的向量会位于拍有狗的图像的向量附近，因此可以根据向量之间的远近来搜索图像。

从 Fess 15.8 开始，向量的存储和搜索由 Fess 本体负责。
插件只增加了与 CLIP 服务器通信的部分。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 时机
     - 处理
   * - 爬取时
     - 将 GIF/JPEG/PNG 图像发送到 CLIP 服务器转换为向量，并写入本体的向量字段 ``content_chunk_vector``
   * - 搜索时
     - 通过 CLIP 服务器将搜索词转换为向量，查找相近的图像。该搜索与关键词搜索并行执行，并通过 Rank Fusion 合并为一个结果
   * - 结果
     - 通过向量搜索找到的文档，其 ``searcher`` 字段中带有 ``multi_modal``。通过关键词搜索找到的文档为 ``default``

关于 Rank Fusion 的原理，请参阅 `混合搜索与 Rank Fusion（语义 + 关键词） <https://fess.codelibs.org/zh-cn/stable/config/rank-fusion.html>`__。

使用 docker-multimodalsearch 试用
=================================

``docker-multimodalsearch`` 是一个 Docker Compose 环境，汇集了所需的容器和设置，便于立即试用多模态搜索。
在 ``v15.9.0`` 标签中，会启动以下服务。

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - 服务
     - 作用
   * - ``fess01``
     - Fess 本体。镜像为 ``ghcr.io/codelibs/fess:15.9.0-noble``，启动时会安装插件 ``fess-webapp-multimodal:15.9.0``。搜索页面使用图像画廊型主题 ``mosaic``
   * - ``search01``
     - OpenSearch 3.9.0。端口 9200 仅在主机的环回地址（127.0.0.1）上公开
   * - ``clip_server``
     - CLIP 服务器。默认模型为支持多语言的 ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k``\ （512 维），在 CPU 上运行
   * - ``content``
     - 通过 ``http://content/`` 提供示例图像的 nginx。只能从容器之间的网络访问
   * - ``init-fess-verify``
     - 启动时只运行一次，检查索引的向量字段是否与设置一致，然后退出

准备
----

- Docker（``docker compose`` 命令）、Git、bash
- 互联网连接（用于获取镜像和 CLIP 模型。根据 README，模型约 1.6 GB）
- 在 Linux 上，需要为 OpenSearch 调高 ``vm.max_map_count``\ （与 :doc:`guide-02` 中的准备步骤相同）

获取 15.9 版本
--------------

``docker-multimodalsearch`` 的默认分支跟随正在开发的下一个版本，因此请指定 ``v15.9.0`` 标签进行获取。

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

打开 ``.env``，将主题的获取来源改为 15.9 用的分支。

::

    FESS_THEMES_REF=15.9.x

``v15.9.0`` 的 ``.env.example`` 中仍为 ``FESS_THEMES_REF=main``，但 ``fess-themes`` 的 ``main`` 上的 ``mosaic`` 主题目前面向 Fess 15.10 及以上版本（``minFessVersion: 15.10``）。
15.9 用的 ``mosaic`` 位于 ``15.9.x`` 分支。

``.env`` 中的 ``FESS_VERSION=15.9.0`` 和 ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0`` 保持不变。
插件版本必须与 Fess 版本一致。

设置并启动
----------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh`` 会创建数据目录、获取主题并准备缩略图生成脚本。
首次执行 ``docker compose up -d`` 时，会构建 ``clip_server`` 的镜像并下载 CLIP 模型。
``fess01`` 会等待 ``clip_server`` 准备就绪后再启动，因此首次启动需要几分钟。

使用以下命令确认状态。

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

如果 ``fess01`` 变为 ``(healthy)``，``init-fess-verify`` 以 ``Exited (0)`` 结束，并且日志中输出了以下行，则说明向量字段已按设置创建。

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

爬取示例图像
------------

获取示例图像（动物、交通工具、食物、自然、建筑）以及 HTML 和 PDF。

::

    $ bash bin/fetch-sample-images.sh

接着在管理页面中进行爬取。

1. 使用 ``admin`` / ``admin`` 登录 ``http://localhost:8080/admin/``，如有提示则设置新密码
2. 在 [爬虫] > [Web] 中点击 [新建]，在「名称」中输入 ``content``，在「URL」中输入 ``http://content/``，然后点击 [创建]
3. 在 [系统] > [调度器] 中打开「Default Crawler」，点击 [立即开始]
4. 在 [系统信息] > [爬网信息] 中等待爬取完成

图像的向量会在这次爬取过程中写入。
根据 README，随附的示例会注册 43 条（图像 37 条、HTML 5 条、PDF 1 条）。
条数仅供参考。

搜索
----

打开 ``http://localhost:8080/``，用 ``狗``、``山间日落`` 或 ``mountain sunset`` 进行搜索。
默认模型支持多语言，因此无论用中文还是英语都会返回图像。

``mosaic`` 主题以缩略图画廊的形式显示结果，并为每个结果加上「关键词」「视觉」「混合」徽章。
「视觉」表示按图像相似度找到的结果，「混合」表示通过关键词和图像两方面都找到的结果。

缩略图会在爬取后由后台任务生成。
如果爬取刚结束时部分缩略图没有显示，请稍等片刻后重新加载。

停止时执行 ``docker compose down``。
数据会保留在 ``./data`` 下。

确认运行情况
============

查看搜索 API 的 ``searcher``
----------------------------

是否使用了向量搜索，可以通过搜索 API 响应中的 ``searcher`` 来确认。
如果安装了 ``jq``，请按如下方式执行。

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=狗' | jq -c '.response.data[] | {url, searcher}'

``searcher`` 的值含义如下。

- ``["multi_modal"]``：通过图像相似度找到
- ``["default"]``：通过关键词搜索找到
- 两者都包含：通过两种方式都找到

如果所有结果都只有 ``["default"]``，说明没有执行向量搜索。
请确认是否属于下文“不执行向量搜索的搜索”中的情况。

默认情况下，API 的响应中不包含 ``searcher``。
``docker-multimodalsearch`` 通过启动选项（``-Dfess.config.query.additional.api.response.fields=searcher``）设置了 ``fess_config.properties`` 的 ``query.additional.api.response.fields=searcher``，因此响应中会包含它。
有关搜索 API 的详细信息，请参阅 `搜索 API <https://fess.codelibs.org/zh-cn/stable/api/api-search.html>`__。

查看向量是否已写入
------------------

如果搜索完全没有返回图像，请在 OpenSearch 中统计带有向量的文档数（此环境的 9200 端口只能从主机使用）。

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

如果 ``count`` 为 0，说明爬取时没有生成向量。
请检查 ``docker compose logs fess01`` 或爬虫日志中是否出现 ``Failed to convert an image to a vector.`` 警告。

不执行向量搜索的搜索
--------------------

在以下情况下，不会执行向量搜索，只返回关键词搜索的结果。
这种情况不会报错，很难察觉，请务必注意。

- 指定了排序顺序的搜索（``sort`` 参数）。如果在 [系统] > [通用] 中设置了「默认排序值」，``mosaic`` 主题会将该值作为 ``sort`` 发送，因此普通搜索也属于这种情况
- 搜索词中使用了搜索语法的搜索：短语（``"山间日落"``）、通配符（``dog*``）、加权（``dog^2``）、排除（``-dog``）、``allintitle:``、``allinurl:``
- 没有搜索词、只有标签等筛选条件的搜索
- 第 101 条及以后的页面（起始位置达到 ``rank.fusion.window_size``\ （默认值 200）的一半及以上时）
- 无法连接 CLIP 服务器时（``fess.log`` 中会输出 ``Embedding provider is unavailable`` 等 WARN）

另一方面，即使在搜索词中同时使用 ``filetype:jpg`` 之类的字段指定或标签筛选，也会执行向量搜索，并按该条件进行筛选。

集成到现有 Fess
===============

如果不使用 ``docker-multimodalsearch``，而是集成到现有的 Fess 15.9 中，请按以下步骤操作。

1. 安装插件
-----------

通过以下任一方式安装 ``fess-webapp-multimodal`` 的 15.9.x，然后重启 Fess。

- 管理页面的 [系统] > [插件] > [安装]
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- 使用 Docker 时，将 ``fess-webapp-multimodal:15.9.0`` 添加到环境变量 ``FESS_PLUGINS`` 中

详细信息请参阅 `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__。

2. 准备 CLIP 服务器
-------------------

插件连接的是与 Jina 的 CLIP 服务器格式相同的 HTTP API。
向量化使用 ``POST /post``，连接检查使用 ``GET /health``。
如果 ``/health`` 不返回 2xx，插件会在向量搜索处于禁用的状态下运行。
连接目标通过 ``content_chunker.embedding.clip.api.url`` 指定，默认值为 ``http://localhost:51000``。

- 插件仓库中的 ``docker/compose.yaml`` 会启动 ``jinaai/clip-server``。其配置 ``docker/clip_config.yaml`` 没有指定模型，因此会使用默认模型（README 中为 ViT-B/32，512 维）。此外，该 Compose 文件要求使用 GPU
- 如果要使用英语以外的搜索词（如中文），请像 ``docker-multimodalsearch`` 的 ``docker/clip-server`` 那样，准备运行多语言模型的服务器

3. 在 system.properties 中设置
------------------------------

多模态搜索的设置写在 ``system.properties`` 中。
其位置为：ZIP 版是 ``app/WEB-INF/conf/system.properties``，RPM/DEB 版是 ``/etc/fess/system.properties``，Docker 版是 ``/opt/fess/system.properties``。

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- ``content_chunker.embedding.dimension`` 要与 CLIP 模型输出的维数一致（ViT-B/32 系列为 512）
- ``content_chunker.search.enabled`` 只在启动时读取，因此设置后请重启 Fess
- 通过启动选项传递时，请使用 ``-Dfess.system.<键名>``。写在 ``fess_config.properties`` 或 ``-Dfess.config.<键名>`` 中会被忽略，而且不会出现警告
- ``system.properties`` 中的值优先于 ``-Dfess.system.*``。两处都写时，使用文件中的值
- 在 docker-fess 的 Compose 文件中，``fess01`` 没有卷，执行 ``docker compose down`` 后 ``system.properties`` 会丢失。在 Docker 中，可靠的方法是在环境变量 ``FESS_JAVA_OPTS`` 中列出 ``-Dfess.system.<键名>=<值>``\ （``docker-multimodalsearch`` 的 ``compose.yaml`` 也采用这种方法）

键的列表请参阅 `语义搜索（内容分块 + 向量搜索） <https://fess.codelibs.org/zh-cn/stable/config/search-semantic.html>`__ 中的“配置参考”。
多模态搜索也使用相同的 ``content_chunker.*``。

4. 重新创建索引
---------------

向量字段 ``content_chunk_vector`` 的映射是在创建索引时按当时设置的维数创建的。
如果在进行上述设置之前曾经启动过 Fess，请在 [系统信息] > [维护] 中启用「更新别名」并执行「重新索引」。
详细信息请参阅 `维护 <https://fess.codelibs.org/zh-cn/stable/admin/maintenance-guide.html>`__。

5. 启用缩略图
-------------

在图像搜索中，没有缩略图就无法区分结果。
缩略图默认处于禁用状态。

- 在 [系统] > [通用] 中启用「显示缩略图」并保存
- 生成图像、PDF 和 Office 文档的缩略图需要 ImageMagick 等外部工具。Docker 的默认（Alpine）镜像中不包含这些工具，因此请使用 ``-noble`` 镜像（例如 ``ghcr.io/codelibs/fess:15.9.0-noble``）

所需工具请参阅 `缩略图配置 <https://fess.codelibs.org/zh-cn/stable/config/crawler-thumbnail.html>`__。

6. 爬取并确认
-------------

爬取包含 GIF/JPEG/PNG 图像的网站或文件夹。
图像的向量会在爬取时写入。

如果要在搜索 API 中确认 ``searcher``，请在 ``fess_config.properties`` 中设置 ``query.additional.api.response.fields=searcher``\ （如果使用启动选项，则为 ``-Dfess.config.query.additional.api.response.fields=searcher``）。

调度器中的「Content Chunk Vector Indexer」任务保持禁用即可（默认为禁用）。
图像的向量由爬虫写入，因此不需要该任务。
如果启用它，文本文档也会通过 CLIP 的文本端进行向量化，并且 ``content`` 字段会被拆分。

运维注意事项
============

不能与文本的语义搜索同时使用
----------------------------

插件会将本体语义搜索的搜索处理（``semanticChunkSearcher``）替换为 CLIP 用的处理。
此外，``content_chunker.embedding.name`` 只能设置一个值。
因此，:doc:`guide-18` 中的文本语义搜索与多模态搜索不能在同一个 Fess 中同时使用。
如果两者都需要，请分别搭建 Fess。

另外，如果通过 ``rank.fusion.searchers`` 限定了所使用的搜索处理，不包含 ``multi_modal`` 时向量搜索会被排除。
通常请将此设置留空。

更换模型时要一直做到重新爬取
----------------------------

模型和维数务必一起修改。
维数在创建索引时就固定在映射中，因此修改后需要执行以下步骤。

1. 在 [系统信息] > [维护] 中执行「重新索引」（启用「更新别名」），用新的维数重新创建索引
2. 重新爬取

重新索引只会复制文档，不会重新计算向量。
即使维数相同，更换模型或 CLIP 服务器后向量空间也会改变，因此请先删除文档再重新爬取。
在 ``docker-multimodalsearch`` 中，修改 ``.env`` 中的 ``CLIP_MODEL_NAME`` 和 ``MULTIMODAL_DIMENSION``。
具体步骤见 README 的“Model swap”。

CPU 与 GPU
----------

``docker-multimodalsearch`` 的默认模型（512 维）以在 CPU 上运行为前提，默认值为 ``CLIP_DEVICE=cpu``。
如果更换为更大的 ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k``\ （1024 维），建议使用 GPU；设置 ``CLIP_DEVICE=auto`` 后，如果有 GPU 就会使用。

总结
====

- ``fess-webapp-multimodal`` 是用文本查找 GIF/JPEG/PNG 图像的功能。无法用图像进行搜索，也无法将嵌入在文档中的图像向量化
- 如果要试用，请使用 ``docker-multimodalsearch`` 的 ``v15.9.0``，并指定 ``FESS_THEMES_REF=15.9.x``
- 将 ``content_chunker.*`` 设置写在 ``system.properties``\ （或 ``-Dfess.system.*``）中
- 是否使用了向量搜索，可通过搜索 API 的 ``searcher`` 中的 ``multi_modal`` 确认
- 英语以外的搜索词（如中文）需要多语言模型，并且不能与文本的语义搜索在同一个 Fess 中同时使用

延伸阅读
========

- :doc:`guide-18` — 用向量搜索文本文档（与多模态不同的配置）
- :doc:`guide-02` — 使用 Docker 运行 Fess 的基础
- :doc:`guide-11` — 通过搜索 API 与业务系统集成

参考资料
========

- `docker-multimodalsearch（v15.9.0） <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal（15.9.0） <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
