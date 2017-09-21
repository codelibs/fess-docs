=======
アップグレード
=======

|Fess| 10.xからのアップグレード
=======

以前のバージョンから更新するためには、次の手順を参照してください。

データのバックアップ
-----------

設定データは以下のファイルになります。

* バックアップページの.fess_basic_configおよび.fess_user (詳細は管理者ガイドのバックアップを参照してください)
* /etc/fessまたはapp/WEB-INF/confのsystem.properties
* /etc/fessまたはapp/WEB-INF/confのfess_config.properties

パッケージの更新
---------------

|Fess| のプロセスを停止して、RPMまたはDEBパッケージをインストールしてください。
詳細はインストールガイドのインストールを参照してください。

|Fess| 11ではElasticsearch 5.1以上が必要になります。
また、|Fess| 11のインデックスはElasticsearchの仕様変更により|Fess| 10.xのものと互換性がありません。
Elasticsearch 5へのアップグレードする際には、|Fess| の既存のインデックスを削除してからElasticsearchのパッケージを更新してください。

設定のリストア
--------------

fess_config.propertiesの設定を確認し、既存の設定を反映してから、|Fess| を起動してください。
設定をリストアするためには、.fess_basic_configおよび.fess_userのバルクファイルをバックアップページからアップロードしてください。

クローラの起動
-------------

スケジューラページでDefault Crawlerジョブを開始して、インデックスを生成してください。

