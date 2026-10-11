=========
バックアップ
=========

概要
====

バックアップページでは |Fess| の設定情報のダウンロードとアップロードができます。

ダウンロード
---------

|Fess| は設定情報をインデックスとして保持しています。
ダウンロードするにはインデックス名をクリックしてください。

|image0|

fess_config.bulk
::::::::::::::::

fess_config.bulk は |Fess| の設定情報を含んでいます。

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk は障害URLを除いた |Fess| の設定情報を含んでいます。

fess_user.bulk
::::::::::::::

fess_user.bulk はユーザー、ロールおよびグループの情報を含みます。

system.properties
:::::::::::::::::

system.propertiesは全般設定の情報を含みます。

fess.json
:::::::::

fess.jsonはfessインデックスの設定情報を含みます。

doc.json
::::::::

doc.jsonはfessインデックスのマッピング情報を含みます。

chat_log.ndjson
:::::::::::::::

chat_log.ndjsonはAIチャットの利用ログの情報を含みます。

click_log.ndjson
::::::::::::::::

click_log.ndjsonはクリックログの情報を含みます。

favorite_log.ndjson
:::::::::::::::::::

favorite_log.ndjsonはお気に入りログの情報を含みます。

search_log.ndjson
:::::::::::::::::

search_log.ndjsonは検索ログの情報を含みます。

user_info.ndjson
::::::::::::::::

user_info.ndjsonは検索ユーザの情報を含みます。

アップロード
---------

設定情報をアップロードして取り込むことができます。
リストアが可能なファイルは \*.bulk と system.properties です。

\*.bulk 内のドキュメントのうち ``updatedTime`` を持つものは、保存済みのドキュメントが存在しない、
``updatedTime`` を持たない、またはそれより古い場合にだけ書き込まれます。新しくないドキュメントは
スキップされ、 ``fess.log`` に INFO レベルで記録されます。そのため、バックアップ取得後の変更が
巻き戻されることはなく、インストール済みの版が同梱するスケジュールジョブ（ ``updatedTime`` は 0）も
そのまま残ります。 ``updatedTime`` を持たないドキュメントは常に書き込まれます。

  .. |image0| image:: ../../../resources/images/ja/15.9/admin/backup-1.png
