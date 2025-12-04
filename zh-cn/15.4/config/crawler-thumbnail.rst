===============
缩略图配置
===============

缩略图显示
===============

|Fess| 可以在搜索结果中显示缩略图。
缩略图根据搜索结果的 MIME 类型生成。
对于支持的 MIME 类型,在显示搜索结果时会生成缩略图。
可以为每种 MIME 类型配置并添加缩略图生成处理。

要显示缩略图,请以管理员身份登录,在常规设置中启用缩略图显示并保存。

HTML 文件缩略图
======================

HTML 的缩略图使用 HTML 中指定的图片或包含的图片。
按以下顺序查找缩略图并在指定时显示。

- name 属性为 thumbnail 的 meta 标签的 content 值
- property 属性为 og:image 的 meta 标签的 content 值
- img 标签中适合缩略图大小的图片


MS Office 文件缩略图
===========================

MS Office 系列的缩略图使用 LibreOffice 和 ImageMagick 生成。
当安装了 unoconv 和 convert 命令时,将生成缩略图。

软件包安装
------------------

对于 Redhat 系列 OS,请安装以下软件包以创建图片。

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

生成脚本
-----------

使用 RPM/Deb 软件包安装时,MS Office 的缩略图生成脚本会安装在 /usr/share/fess/bin/generate-thumbnail 中。

PDF 文件缩略图
=====================

PDF 的缩略图使用 ImageMagick 生成。
当安装了 convert 命令时,将生成缩略图。

禁用缩略图任务
==================

要禁用缩略图任务,请进行以下设置。

1. 在管理页面的"系统">"常规"中取消勾选"缩略图显示",然后点击"更新"按钮。
2. 在 ``app/WEB-INF/classes/fess_config.properties`` 或 ``/etc/fess/fess_config.properties`` 的 ``thumbnail.crawler.enabled`` 中设置 ``false``。

::

    thumbnail.crawler.enabled=false

3. 重启 Fess 服务。
