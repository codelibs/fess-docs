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
     - fess-ds-microsoft365
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
     - fess-ds-db
     - JDBC対応データベースからデータを取得
   * - :doc:`ds-csv`
     - fess-ds-csv
     - CSVファイルからデータを取得
   * - :doc:`ds-json`
     - fess-ds-json
     - JSONファイルからデータを取得

その他
------

以下のコネクタも利用可能です:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - コネクタ
     - プラグイン
     - 説明
   * - SharePoint
     - fess-ds-sharepoint
     - SharePointリポジトリからデータを取得（レガシー版）
   * - Wikipedia
     - fess-ds-wikipedia
     - Wikipediaのコンテンツを取得

コネクタのインストール
======================

プラグインのインストール
------------------------

データストアコネクタのプラグインは、管理画面からインストールできます。

管理画面から
~~~~~~~~~~~~

1. 管理画面にログイン
2. 「システム」→「プラグイン」に移動
3. 「Available」タブで対象のプラグインを検索
4. 「インストール」をクリック
5. |Fess| を再起動


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
   * - 説明
     - 設定の説明文
   * - ハンドラ名
     - 使用するコネクタのハンドラ名（例: ``BoxDataStore``）
   * - パラメーター
     - コネクタ固有の設定パラメーター（key=value形式）
   * - スクリプト
     - インデックスフィールドのマッピングスクリプト
   * - ブースト
     - 検索結果の優先度
   * - 権限
     - このデータストアから取得したドキュメントのアクセス権限
   * - 仮想ホスト
     - この設定を適用する仮想ホスト
   * - 表示順序
     - 設定一覧での表示順序
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

スクリプトでは、取得したデータを |Fess| のインデックスフィールドにマッピングします。

以下はCSV/JSONコネクタでの ``data.*`` プレフィックスを使用した例です:

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

.. note::

   スクリプトで使用するフィールドのプレフィックスはコネクタごとに異なります。
   例えば、Box/Dropbox/Google Drive/OneDriveでは ``file.*`` 、Slackでは ``message.*`` 、
   Jiraでは ``issue.*`` を使用します。
   各コネクタの詳細は個別のドキュメントを参照してください。

認証設定
========

多くのデータストアコネクタは、OAuth 2.0、APIキー、サービスアカウントなどによる認証が必要です。

認証パラメーターはコネクタごとに異なります。
各コネクタの認証設定については、個別のドキュメントを参照してください。

共通パラメーター
================

すべてのデータストアコネクタで使用できる共通パラメーター:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - デフォルト
     - 説明
   * - ``readInterval``
     - ``0``
     - 各レコードの処理間の待機時間（ミリ秒）。大量データ処理時にサーバー負荷を軽減するために使用します。

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
- :doc:`../../api/admin/api-admin-dataconfig` - データストア設定API
