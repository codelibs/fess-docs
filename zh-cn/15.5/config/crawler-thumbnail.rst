===============
缩略图配置
===============

概述
====

|Fess| 可以在搜索结果中显示缩略图。
缩略图根据搜索结果的 MIME 类型生成。
对于支持的 MIME 类型,在显示搜索结果时会生成缩略图。
可以为每种 MIME 类型配置并添加缩略图生成处理。

要显示缩略图,请以管理员身份登录,在常规设置中启用缩略图显示并保存。

支持的文件格式
==============

图片文件
--------

.. list-table::
   :widths: 15 40 20
   :header-rows: 1

   * - 格式
     - MIME 类型
     - 说明
   * - JPEG
     - ``image/jpeg``
     - 照片等
   * - PNG
     - ``image/png``
     - 透明图片等
   * - GIF
     - ``image/gif``
     - 包括动画 GIF
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - 位图图片
   * - TIFF
     - ``image/tiff``
     - 高质量图片
   * - SVG
     - ``image/svg+xml``
     - 矢量图片
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - PSD 文件

文档文件
--------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - 格式
     - MIME 类型
     - 说明
   * - PDF
     - ``application/pdf``
     - PDF 文档
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Word 文档
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - Excel 电子表格
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - PowerPoint 演示文稿
   * - RTF
     - ``application/rtf``
     - 富文本
   * - PostScript
     - ``application/postscript``
     - PostScript 文件

HTML 内容
---------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - 格式
     - MIME 类型
     - 说明
   * - HTML
     - ``text/html``
     - 从 HTML 页面中嵌入的图片生成缩略图

所需的外部工具
==============

缩略图生成需要以下外部工具。请根据需要支持的文件格式进行安装。

基本工具（必需）
----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 工具
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - 图片转换和调整大小
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   同时支持 ImageMagick 6（``convert`` 命令）和 ImageMagick 7（``magick`` 命令）。

SVG 支持
--------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 工具
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - SVG 转 PNG
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

PDF 支持
--------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 工具
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - PDF 转 PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

MS Office 支持
--------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 工具
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Office 转 PDF
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - PDF 转 PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

对于 Redhat 系列 OS,请安装以下软件包:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

PostScript 支持
---------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - 工具
     - 用途
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - PS 转 PDF
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - PDF 转 PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

HTML 文件缩略图
===============

HTML 的缩略图使用 HTML 中指定的图片或包含的图片。
按以下顺序查找缩略图并在指定时显示:

1. name 属性为 "thumbnail" 的 meta 标签的 content 值
2. property 属性为 "og:image" 的 meta 标签的 content 值
3. img 标签中适合缩略图大小的图片

配置
====

配置文件
--------

缩略图生成器在 ``fess_thumbnail.xml`` 中配置。

::

    src/main/resources/fess_thumbnail.xml

主要配置项（fess_config.properties）
------------------------------------

以下选项可以在 ``app/WEB-INF/classes/fess_config.properties`` 或 ``/etc/fess/fess_config.properties`` 中配置。

::

    # 缩略图的最小宽度（像素）
    thumbnail.html.image.min.width=100

    # 缩略图的最小高度（像素）
    thumbnail.html.image.min.height=100

    # 最大宽高比（宽:高或高:宽）
    thumbnail.html.image.max.aspect.ratio=3.0

    # 生成的缩略图宽度
    thumbnail.html.image.thumbnail.width=100

    # 生成的缩略图高度
    thumbnail.html.image.thumbnail.height=100

    # 输出格式
    thumbnail.html.image.format=png

    # 从 HTML 提取图片的 XPath
    thumbnail.html.image.xpath=//IMG

    # 排除的扩展名
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # 缩略图生成间隔（毫秒）
    thumbnail.generator.interval=0

    # 命令执行超时（毫秒）
    thumbnail.command.timeout=30000

    # 进程销毁超时（毫秒）
    thumbnail.command.destroy.timeout=5000

generate-thumbnail 脚本
=======================

概述
----

``generate-thumbnail`` 是执行实际缩略图生成的 shell 脚本。
使用 RPM/Deb 软件包安装时,它会安装在 ``/usr/share/fess/bin/generate-thumbnail``。

用法
----

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

参数
----

.. list-table::
   :widths: 15 40 30
   :header-rows: 1

   * - 参数
     - 说明
     - 示例
   * - ``type``
     - 文件类型
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - 输入文件 URL
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - 输出文件路径
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - MIME 类型（可选）
     - ``image/gif``

支持的类型
----------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - 类型
     - 说明
     - 使用的工具
   * - ``image``
     - 图片文件
     - ImageMagick (convert/magick)
   * - ``svg``
     - SVG 文件
     - rsvg-convert
   * - ``pdf``
     - PDF 文件
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - MS Office 文件
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - PostScript 文件
     - ps2pdf + pdftoppm + ImageMagick

示例
----

::

    # 为图片文件生成缩略图
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # 为 SVG 文件生成缩略图
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # 为 PDF 文件生成缩略图
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # GIF 文件（指定 MIME 类型以启用格式提示）
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

缩略图存储位置
==============

默认路径
--------

::

    ${FESS_VAR_PATH}/thumbnails/

或

::

    /var/lib/fess/thumbnails/

目录结构
--------

缩略图以基于哈希的目录结构存储。

::

    thumbnails/
    ├── _0/
    │   ├── _1/
    │   │   ├── _2/
    │   │   │   └── _3/
    │   │   │       └── abcdef123456.png
    │   │   └── ...
    │   └── ...
    └── ...

禁用缩略图任务
==============

要禁用缩略图任务,请进行以下设置:

1. 在管理页面的"系统">"常规"中取消勾选"缩略图显示",然后点击"更新"按钮。
2. 在 ``app/WEB-INF/classes/fess_config.properties`` 或 ``/etc/fess/fess_config.properties`` 的 ``thumbnail.crawler.enabled`` 中设置 ``false``。

::

    thumbnail.crawler.enabled=false

3. 重启 Fess 服务。

故障排除
========

缩略图未生成
------------

1. **检查外部工具**

::

    # 检查 ImageMagick
    which convert || which magick

    # 检查 rsvg-convert（用于 SVG）
    which rsvg-convert

    # 检查 pdftoppm（用于 PDF）
    which pdftoppm

2. **检查日志**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **手动运行脚本**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

GIF/TIFF 文件出错
-----------------

使用 ImageMagick 6 时,指定 MIME 类型以启用格式提示。如果 Fess 配置正确,这将自动完成。

错误示例::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

解决方案:

- 升级到 ImageMagick 7
- 或验证 MIME 类型是否正确传递

SVG 缩略图未生成
----------------

1. 检查 ``rsvg-convert`` 是否已安装

::

    which rsvg-convert

2. 手动测试转换

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

权限错误
--------

检查缩略图存储目录的权限。

::

    ls -la /var/lib/fess/thumbnails/

如有必要,修复权限。

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

平台支持
========

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - 平台
     - 支持状态
     - 备注
   * - Linux
     - 完全支持
     - \-
   * - macOS
     - 完全支持
     - 通过 Homebrew 安装外部工具
   * - Windows
     - 不支持
     - 由于依赖 bash 脚本
