=========
备份
=========

概述
====

在备份页面可以下载和上传 |Fess| 的配置信息。

下载
---------

|Fess| 将配置信息保存为索引。
要下载，请点击索引名称。

|image0|

.. note::

   词典（同义词、停用词等）文件不包含在备份中。
   词典文件保存在搜索引擎的词典目录（ ``FESS_DICTIONARY_PATH`` ）中，如有需要，请另行复制。

fess_config.bulk
::::::::::::::::

fess_config.bulk 包含 |Fess| 的配置信息。

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk 包含除爬取信息、失败URL、作业日志、缩略图队列、用户标签等以外的 |Fess| 配置信息。

fess_user.bulk
::::::::::::::

fess_user.bulk 包含用户、角色和组的信息。

system.properties
:::::::::::::::::

system.properties包含常规配置信息。

fess.json
:::::::::

fess.json包含fess索引的配置信息。

doc.json
::::::::

doc.json包含fess索引的映射信息。

chat_log.ndjson
:::::::::::::::

chat_log.ndjson包含AI聊天使用日志信息。

click_log.ndjson
::::::::::::::::

click_log.ndjson包含点击日志信息。

favorite_log.ndjson
:::::::::::::::::::

favorite_log.ndjson包含收藏日志信息。

search_log.ndjson
:::::::::::::::::

search_log.ndjson包含搜索日志信息。

user_info.ndjson
::::::::::::::::

user_info.ndjson包含搜索用户的信息。

上传
---------

可以上传和导入配置信息。
可以恢复的文件如下。

- ``*.bulk``
- ``system.properties``
- ``fess.json`` 、 ``doc.json`` ：替换 |Fess| 使用的索引定义文件。已有索引的设置和映射不会被立即更改。
- ``gsa*.xml`` ：Google Search Appliance 的配置文件。将作为 Web 爬取配置、文件爬取配置和标签导入。

``*.ndjson`` （搜索日志等日志）无法通过上传来恢复。

\*.bulk 中带有 ``updatedTime`` 的文档，仅在已存储的文档不存在、没有 ``updatedTime`` 或更旧时才会写入。
不比已存储文档更新的文档会被跳过，并以 INFO 级别记录在 ``fess.log`` 中。因此恢复不会撤销备份之后所做的更改，
已安装版本自带的计划作业（``updatedTime`` 为 0）也会原样保留。没有 ``updatedTime`` 的文档总是会被写入。

  .. |image0| image:: ../../../resources/images/en/15.9/admin/backup-1.png
