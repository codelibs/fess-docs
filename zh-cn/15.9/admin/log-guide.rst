=========
日志文件
=========

概述
====

本节介绍如何下载 |Fess| 输出的日志文件。

配置方法
======

显示方法
------

要打开下图所示的日志文件页面，请点击左侧菜单中的 [系统信息 > 日志文件]。

|image0|

下载
---------

点击显示的日志文件名即可下载日志文件。

``server_*.log``
::::::::::::::::

记录 |Fess| 作为应用服务器的日志。

fess.log
::::::::

记录 |Fess| 作为应用程序的日志。

fess-crawler.log
::::::::::::::::

记录爬虫的日志。

audit.log
:::::::::

记录登录信息和管理界面的访问日志。

fess-thumbnail.log
::::::::::::::::::

记录缩略图功能的日志。

fess-suggest.log
::::::::::::::::

记录建议功能的日志。

fess-urls.log
:::::::::::::

记录单次爬虫所需的时间。

searchlog.log
:::::::::::::

记录搜索日志。
当 [系统 > 通用] 中的"搜索日志"启用时，在默认设置下每次搜索都会追加 1 行（JSON）。
1 行中包含该次搜索返回的文档的字段（ ``logging.search.docs.fields`` ），因此其大小会随返回的件数增加（ ``num=100`` 时，1 行可能达到 70 KB 左右）。
日志的轮转和保留期限请参见 :doc:`../config/admin-logging`。
如果不想在搜索日志中包含返回文档的字段，请在 ``fess_config.properties`` 中设置 ``logging.search.docs.enabled=false``；如果不想输出到此文件，请设置 ``logging.search.use.logfile=false``。

gc-crawler.log
::::::::::::::

记录爬虫进程的GC日志（由默认的"Default Crawler"任务输出）。

gc-fess.log
:::::::::::

记录 |Fess| 本体的GC日志。仅当环境变量 ``FESS_USE_GC_LOGGING`` 设置为非空值时才会输出（参见 :doc:`../install/run`）。

.. |image0| image:: ../../../resources/images/en/15.9/admin/log-1.png
