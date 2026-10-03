==================================
OCR（图像文字识别）配置
==================================

概述
====

|Fess| 使用 Apache Tika 从文档中提取文本。
Tika 的 Tesseract OCR 解析器已包含在 |Fess| 中。启用后，可以识别图像和扫描版 PDF 中的文字，并将其作为搜索对象。

满足以下两个条件时，将执行 OCR。

- 运行 |Fess| 爬虫进程的主机上已安装 ``tesseract`` 命令
- |Fess| 中已启用 OCR

OCR 默认处于禁用状态。
如果未安装 ``tesseract``，|Fess| 会跳过 OCR，不会报错。

OCR 的对象
==========

启用 OCR 后，以下内容将成为对象。

- 图像文件（PNG、JPEG、TIFF、GIF、BMP 等）
- 由 Tika 处理的文档中嵌入的图像（Office 文件等）
- 文本层为空的 PDF（扫描版 PDF）

扫描版 PDF 的处理
-----------------

|Fess| 通常使用 PDFBox 从 PDF 中提取文本。
启用 OCR 且 PDFBox 完全无法从 PDF 中获取文本时，|Fess| 会通过 Tika 重新提取该 PDF。
此时 Tika 会将页面转换为图像并执行 OCR。

.. note::
   已包含文本的 PDF 不会成为 OCR 的对象。
   只有部分页面是扫描图像的 PDF（混合 PDF）不在对象范围内。

安装 Tesseract
==============

在运行 |Fess| 的主机上安装 Tesseract。
要识别日文文字，还需要日文的训练数据（traineddata）。

Debian / Ubuntu::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux（请先启用 EPEL）::

    $ sudo dnf install tesseract tesseract-langpack-jpn

可以通过以下命令确认已安装的语言::

    $ tesseract --list-langs

启用 OCR
========

在 ``fess_config.properties`` 中设置以下属性。

- ZIP 版: ``app/WEB-INF/classes/fess_config.properties``
- RPM/DEB 版: ``/etc/fess/fess_config.properties``

::

    # 启用 OCR（默认值: false）
    crawler.document.ocr.enabled=true

    # Tesseract 的语言（多个语言用 + 连接，默认值: eng）
    crawler.document.ocr.language=jpn+eng

    # Tesseract 单次运行的超时时间（秒，默认值: 120）
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 属性
     - 默认值
     - 说明
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - 设置为 ``true`` 即启用 OCR。
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Tesseract 的语言。多个语言用 ``+`` 连接（例如 ``jpn+eng``）。必须已安装对应的 traineddata。
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Tesseract 单次运行（一张图像或 PDF 的一页）的超时时间，单位为秒。

这些设置也可以作为 JVM 系统属性指定。
例如在 ``FESS_JAVA_OPTS`` 中按如下方式指定。这在 Docker 环境中很方便。

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   更改设置后，请重启 |Fess|。

在 Docker 中使用
================

要在 Docker 环境中使用 OCR，请在 |Fess| 镜像中添加 Tesseract。
使用 `docker-fess <https://github.com/codelibs/docker-fess>`__ 的 ``compose/tesseract/Dockerfile`` 构建添加了 Tesseract 的镜像。

``compose/tesseract/Dockerfile`` 示例::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

在 ``compose/compose.yaml`` 中，将 ``image:`` 行替换为 ``build: ./tesseract``，并启用 ``FESS_JAVA_OPTS`` 行。
用法与 ``build: ./playwright`` 相同。

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

更改后，重新构建镜像并启动容器::

    $ docker compose up -d --build

.. note::
   如果使用 ``-noble`` 或 ``-al2023`` 等非 Alpine 的基础镜像，请使用该发行版的包管理器代替 ``apk`` 来添加 Tesseract。

详情请参阅 :doc:`../install/install-docker`。

按爬取配置进行设置
==================

在爬取配置的“配置参数”中指定 ``config.tika.tesseract.config``，可以仅针对该爬取配置覆盖 OCR 设置。

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties`` 是类路径上的资源名称，不是文件系统路径。
请将文件放在 |Fess| 的配置目录中，该目录包含在爬虫的类路径中。

- ZIP 版: ``app/WEB-INF/classes/``
- RPM/DEB 版: ``/etc/fess/``

在 ``tesseract.properties`` 中编写 Tika 的 ``TesseractOCRConfig`` 属性。
能够可靠生效的只有 ``language`` 和 ``timeoutSeconds`` 等简单的键。

::

    language=jpn
    timeoutSeconds=300

对于该爬取配置，此设置优先于上述全局设置。

运维注意事项
============

- OCR 会给 CPU 带来很高的负载，并使爬取的处理时间大幅增加。请考虑减少爬虫的线程数，或仅在需要 OCR 的爬取配置中启用等，以控制负载。
- 在 Web 爬取配置中，新建时的默认设置会将图像 URL（jpg、png、gif 等）从爬取对象中排除。要爬取网站上的图像，请从“从爬取对象中排除的URL”中删除这些项。文件爬取会将图像也作为爬取对象。
- 爬虫的大小限制同样适用。关于按文件类型设置的索引大小上限（默认值 10MB），请参阅 :doc:`crawler-basic`。
- OCR 的精度取决于扫描图像的质量。手写文字通常难以被识别。
- 启用 OCR 之前已编入索引的文件不会自动进行 OCR。启用增量爬取（ :doc:`../admin/general-guide` 中的“检查上次修改时间”）时，修改时间未变化的文件在重新爬取时不会被再次获取。要对这些文件应用 OCR，请临时禁用“检查上次修改时间”后爬取一次，或者先从索引中删除这些文档后重新爬取。

升级注意事项
============

15.8 及更早版本中自带的 ``tika.xml`` 排除了 ``org.apache.tika.parser.ocr.TesseractOCRParser``。
从 15.9 起，自带的 ``tika.xml`` 不再排除该解析器。

如果您一直在使用自定义的 ``tika.xml``，请删除以下行。

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

如果保留此行，即使指定了 ``crawler.document.ocr.enabled=true``，OCR 仍然保持禁用。

``tika.xml`` 的位置如下。

- ZIP 版: ``app/WEB-INF/conf/tika.xml``
- RPM/DEB 版: ``/etc/fess/tika.xml``

确认运行
========

1. 将放有扫描图像（包含文字的图像）的文件夹设为文件爬取的对象。
2. 执行爬取。
3. 使用图像中包含的单词进行搜索，确认该图像显示在搜索结果中。

如果搜索结果中没有显示，请确认以下几点。

- ``tesseract --list-langs`` 中显示所使用的语言
- ``crawler.document.ocr.enabled`` 为 ``true``
- ``tika.xml`` 中没有残留对 ``TesseractOCRParser`` 的排除
- 爬取时的 ``fess-crawler.log`` 中输出了 ``OCR is enabled`` （如果输出 ``Tesseract OCR is not available`` 警告，则表示 |Fess| 无法使用 Tesseract）
