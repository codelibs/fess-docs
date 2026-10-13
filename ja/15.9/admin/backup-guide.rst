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

.. note::

   辞書（シノニム、ストップワードなど）のファイルはバックアップの対象に含まれません。
   辞書ファイルは検索エンジンの辞書ディレクトリ（ ``FESS_DICTIONARY_PATH`` ）に保存されているため、必要に応じて別途コピーしてください。

fess_config.bulk
::::::::::::::::

fess_config.bulk は |Fess| の設定情報を含んでいます。

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk は、クロール情報、障害URL、ジョブログ、サムネイルキュー、ユーザータグなどを除いた |Fess| の設定情報を含んでいます。

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
リストアが可能なファイルは次のとおりです。

- ``*.bulk``
- ``system.properties``
- ``fess.json`` 、 ``doc.json`` ： |Fess| が使用するインデックスの定義ファイルを置き換えます。既存のインデックスの設定やマッピングはその場では変更されません。
- ``gsa*.xml`` ：Google Search Appliance の設定ファイルです。ウェブクロール設定、ファイルクロール設定、ラベルとして取り込まれます。

``*.ndjson`` （検索ログなどのログ）はアップロードして復元することはできません。

\*.bulk 内のドキュメントのうち ``updatedTime`` を持つものは、保存済みのドキュメントが存在しない、
``updatedTime`` を持たない、またはそれより古い場合にだけ書き込まれます。新しくないドキュメントは
スキップされ、 ``fess.log`` に INFO レベルで記録されます。そのため、バックアップ取得後の変更が
巻き戻されることはなく、インストール済みの版が同梱するスケジュールジョブ（ ``updatedTime`` は 0）も
そのまま残ります。 ``updatedTime`` を持たないドキュメントは常に書き込まれます。

.. note::

   スキップの記録は INFO レベルなので、既定のログレベル（ ``warn`` ）では ``fess.log`` に出力されません。記録を確認するときは、復元の前にログレベルを ``info`` にしてください。管理画面の [システム > 全般] の「ログレベル」で変更でき（ |Fess| を再起動すると元に戻ります）、Linux では ``FESS_LOG_LEVEL=info`` でも指定できます。詳しくは :doc:`../config/admin-logging` を参照してください。

.. note::

   15.9 の |Fess| は、Web 認証とファイル認証の ``password`` をアプリケーションの暗号鍵（ ``fess_config.properties`` の
   ``app.cipher.key`` ）で暗号化して保存します。そのため、 ``fess_basic_config.bulk`` と ``fess_config.bulk`` にも
   暗号化された値が含まれます。バックアップを別のインストールに復元するときは、同じ ``app.cipher.key`` を引き継いでください。
   鍵が異なると、これらの認証情報を使うクロールはエラーで失敗します。15.9 より前のバックアップには平文で含まれており、
   そのまま使えます。

   なお、 ``*.bulk`` にはこれら以外の値が暗号化されずに含まれます。 ``*.bulk`` は機密ファイルとして保管してください。

  .. |image0| image:: ../../../resources/images/ja/15.9/admin/backup-1.png
