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

fess_config.bulk
::::::::::::::::

fess_config.bulk 包含 |Fess| 的配置信息。

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk 包含除故障URL外的 |Fess| 配置信息。

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
可以恢复的文件是 \*.bulk 和 system.properties。

  .. |image0| image:: ../../../resources/images/en/15.4/admin/backup-1.png
