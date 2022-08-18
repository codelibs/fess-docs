============
バックアップ
============

概要
====

バックアップページでは |Fess| の設定情報のダウンロードとアップロードができます。

ダウンロード
------------

|Fess| は設定情報をインデックスとして保持しています。
ダウンロードするにはインデックス名をクリックしてください。

|image0|

.fess_config
::::::::::::

.fess_config インデックスは |Fess| の設定情報を含んでいます。

.fess_basic_config
::::::::::::

.fess_basic_config インデックスは障害URLを除いた |Fess| の設定情報を含んでいます。

.fess_user
::::::::::

.fess_user インデックスはユーザー、ロールおよびグループの情報を含みます。

system.properties
::::::::::

system.properties 全般設定の情報を含みます。

click_log.ndjson
::::::::::

click_log.ndjson クリックログの情報を含みます。

favorite_log.ndjson
::::::::::

favorite_log.ndjson お気に入りログの情報を含みます。

search_log.ndjson
::::::::::

search_log.ndjson 検索ログの情報を含みます。

user_info.ndjson
::::::::::

user_info.ndjson 検索ユーザの情報を含みます。

アップロード
------------

設定情報をアップロードして取り込むことができます。
リストアが可能なファイルは \*.bulk と system.properties です。

  .. |image0| image:: ../../../resources/images/ja/14.4/admin/backup-1.png
