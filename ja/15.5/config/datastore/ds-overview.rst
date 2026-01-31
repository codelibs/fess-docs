==================================
データストアコネクタの概要
==================================

概要
====

|Fess| のデータストアコネクタは、Webサイトやファイルシステム以外のデータソースから
コンテンツを取得してインデックス化する機能を提供します。

データストアコネクタを使用することで、以下のようなソースからデータを検索可能にできます:

- クラウドストレージ（Box、Dropbox、Google Drive、OneDrive）
- コラボレーションツール（Confluence、Jira、Slack）
- データベース（MySQL、PostgreSQL、Oracle等）
- その他のシステム（Git、Salesforce、Elasticsearch等）

利用可能なコネクタ
==================

|Fess| は多様なデータソースに対応するコネクタを提供しています。
多くのコネクタはプラグインとして提供されており、必要に応じてインストールできます。

クラウドストレージ
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - コネクタ
     - プラグイン
     - 説明
   * - :doc:`ds-box`
     - fess-ds-box
     - Box.comのファイルとフォルダをクロール
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - Dropboxのファイルとフォルダをクロール
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - Google Drive、Gmailなどをクロール
   * - :doc:`ds-microsoft365`
     - fess-ds-office365
     - OneDrive、SharePointなどをクロール

コラボレーションツール
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - コネクタ
     - プラグイン
     - 説明
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - Confluence、Jiraをクロール
   * - :doc:`ds-slack`
     - fess-ds-slack
     - Slackのメッセージとファイルをクロール

開発・運用ツール
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - コネクタ
     - プラグイン
     - 説明
   * - :doc:`ds-git`
     - fess-ds-git
     - Gitリポジトリのソースコードをクロール
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Elasticsearch/OpenSearchからデータを取得
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Salesforceのオブジェクトをクロール

データベース・ファイル
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - コネクタ
     - プラグイン
     - 説明
   * - :doc:`ds-database`
     - （組み込み）
     - JDBC対応データベースからデータを取得
   * - :doc:`ds-csv`
     - fess-ds-csv
     - CSVファイルからデータを取得
   * - :doc:`ds-json`
     - fess-ds-json
     - JSONファイルからデータを取得

コネクタのインストール
======================

プラグインのインストール
------------------------

データストアコネクタのプラグインは、管理画面または `plugin` コマンドでインストールできます。

管理画面から
~~~~~~~~~~~~

1. 管理画面にログイン
2. 「システム」→「プラグイン」に移動
3. 「Available」タブで対象のプラグインを検索
4. 「インストール」をクリック
5. |Fess| を再起動

コマンドライン
~~~~~~~~~~~~~~

::

    # プラグインをインストール
    ./bin/fess-plugin install fess-ds-box

    # インストール済みプラグインを確認
    ./bin/fess-plugin list

Docker環境
~~~~~~~~~~

::

    # 起動時にプラグインをインストール
    docker run -e FESS_PLUGINS="fess-ds-box,fess-ds-dropbox" codelibs/fess:15.5.0

データストア設定の基本
======================

データストアコネクタの設定は、管理画面の「クローラー」→「データストア」で行います。

共通設定項目
------------

すべてのデータストアコネクタに共通する設定項目:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 説明
   * - 名前
     - 設定の識別名
   * - ハンドラ名
     - 使用するコネクタのハンドラ名（例: ``BoxDataStore``）
   * - パラメーター
     - コネクタ固有の設定パラメーター（key=value形式）
   * - スクリプト
     - インデックスフィールドのマッピングスクリプト
   * - ブースト
     - 検索結果の優先度
   * - 有効
     - この設定を有効にするかどうか

パラメーター設定
----------------

パラメーターは改行区切りの ``key=value`` 形式で指定します:

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

スクリプト設定
--------------

スクリプトでは、取得したデータを |Fess| のインデックスフィールドにマッピングします:

::

    url=data.url
    title=data.name
    content=data.content
    mimetype=data.mimetype
    filetype=data.filetype
    filename=data.filename
    created=data.created
    lastModified=data.lastModified
    contentLength=data.contentLength

認証設定
========

多くのデータストアコネクタは、OAuth 2.0またはAPIキーによる認証が必要です。

OAuth 2.0認証
-------------

一般的なOAuth 2.0の設定パラメーター:

::

    client.id=クライアントID
    client.secret=クライアントシークレット
    refresh.token=リフレッシュトークン

または:

::

    access.token=アクセストークン

APIキー認証
-----------

::

    api.key=APIキー
    api.secret=APIシークレット

サービスアカウント認証
----------------------

::

    service.account.email=サービスアカウントのメールアドレス
    service.account.key=秘密鍵（JSON形式または鍵ファイルパス）

パフォーマンスチューニング
==========================

大量のデータを処理する場合の設定:

::

    # バッチサイズ
    batch.size=100

    # リクエスト間の待機時間（ミリ秒）
    interval=1000

    # 並列処理数
    thread.size=1

    # タイムアウト（ミリ秒）
    timeout=30000

トラブルシューティング
======================

コネクタが表示されない
----------------------

1. プラグインが正しくインストールされているか確認
2. |Fess| を再起動
3. ログでエラーがないか確認

認証エラー
----------

1. 認証情報が正しいか確認
2. トークンの有効期限を確認
3. 必要な権限が付与されているか確認
4. サービス側でAPIアクセスが許可されているか確認

データが取得できない
--------------------

1. パラメーターの形式が正しいか確認
2. 対象のフォルダ/ファイルに対するアクセス権を確認
3. フィルター設定を確認
4. ログで詳細なエラーメッセージを確認

デバッグ設定
------------

問題を調査する際は、ログレベルを調整します:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

参考情報
========

- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../../admin/plugin-guide` - プラグイン管理ガイド
- :doc:`../api/admin/api-admin-dataconfig` - データストア設定API
