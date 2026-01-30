==================================
Dropboxコネクタ
==================================

概要
====

Dropboxコネクタは、Dropboxのクラウドストレージからファイルを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-dropbox`` プラグインが必要です。

対応サービス
============

- Dropbox（ファイルストレージ）
- Dropbox Paper（ドキュメント）

前提条件
========

1. プラグインのインストールが必要です
2. Dropbox開発者アカウントとアプリケーションの作成が必要です
3. アクセストークンの取得が必要です

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールします:

1. Maven Centralから ``fess-ds-dropbox-X.X.X.jar`` をダウンロード
2. プラグイン管理画面からアップロードしてインストール
3. |Fess| を再起動

または、詳細は :doc:`../../admin/plugin-guide` を参照してください。

設定方法
========

管理画面から「クローラー」→「データストア」→「新規作成」で設定します。

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 設定例
   * - 名前
     - Company Dropbox
   * - ハンドラ名
     - DropboxDataStore または DropboxPaperDataStore
   * - 有効
     - オン

パラメーター設定
----------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``access_token``
     - はい
     - Dropboxのアクセストークン（App Consoleで生成）
   * - ``basic_plan``
     - いいえ
     - Basicプランの場合は ``true``（デフォルト: ``false``）

スクリプト設定
--------------

Dropboxファイルの場合
~~~~~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

利用可能なフィールド:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``file.url``
     - ファイルのプレビューリンク
   * - ``file.contents``
     - ファイルのテキストコンテンツ
   * - ``file.mimetype``
     - ファイルのMIMEタイプ
   * - ``file.filetype``
     - ファイルタイプ
   * - ``file.name``
     - ファイル名
   * - ``file.path_display``
     - ファイルのパス
   * - ``file.size``
     - ファイルサイズ（バイト）
   * - ``file.client_modified``
     - クライアント側での最終更新日時
   * - ``file.server_modified``
     - サーバー側での最終更新日時
   * - ``file.roles``
     - ファイルのアクセス権限

Dropbox Paperの場合
~~~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

利用可能なフィールド:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``paper.url``
     - Paperドキュメントのプレビューリンク
   * - ``paper.contents``
     - Paperドキュメントのテキストコンテンツ
   * - ``paper.mimetype``
     - MIMEタイプ
   * - ``paper.filetype``
     - ファイルタイプ
   * - ``paper.title``
     - Paperドキュメントのタイトル
   * - ``paper.owner``
     - Paperドキュメントの所有者
   * - ``paper.roles``
     - ドキュメントのアクセス権限

Dropbox認証の設定
=================

アクセストークンの取得手順
--------------------------

1. Dropbox App Consoleでアプリを作成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://www.dropbox.com/developers/apps にアクセス:

1. 「Create app」をクリック
2. APIタイプで「Scoped access」を選択
3. アクセスタイプで「Full Dropbox」または「App folder」を選択
4. アプリ名を入力して作成

2. 権限の設定
~~~~~~~~~~~~~

「Permissions」タブで必要な権限を選択:

**ファイルのクロールに必要な権限**:

- ``files.metadata.read`` - ファイルのメタデータ読み取り
- ``files.content.read`` - ファイルのコンテンツ読み取り
- ``sharing.read`` - 共有情報の読み取り

**Paperのクロールに追加で必要な権限**:

- ``files.content.read`` - Paperドキュメントの読み取り

3. アクセストークンの生成
~~~~~~~~~~~~~~~~~~~~~~~~~

「Settings」タブで:

1. 「Generated access token」セクションまでスクロール
2. 「Generate」ボタンをクリック
3. 生成されたトークンをコピー（このトークンは一度しか表示されません）

.. warning::
   アクセストークンは安全に保管してください。このトークンがあれば
   Dropboxアカウントにアクセスできます。

4. トークンの設定
~~~~~~~~~~~~~~~~~

取得したトークンをパラメーターに設定:

::

    access_token=sl.your-dropbox-token-here

Basicプランの設定
=================

Dropbox Basicプランの制限
-------------------------

Dropbox Basicプランの場合、API制限が異なります。
``basic_plan`` パラメーターを ``true`` に設定してください:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

これにより、APIレート制限に対応した処理が行われます。

使用例
======

Dropboxファイル全体のクロール
------------------------------

パラメーター:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

スクリプト:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

Dropbox Paperドキュメントのクロール
-----------------------------------

パラメーター:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

スクリプト:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

権限付きクロール
----------------

パラメーター:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    default_permissions={role}admin

スクリプト（Dropboxファイル）:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

スクリプト（Dropbox Paper）:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

特定のファイルタイプのみクロール
--------------------------------

スクリプトでフィルタリング:

::

    # PDFとWordファイルのみ
    if (file.mimetype == "application/pdf" || file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        last_modified=file.client_modified
    }

トラブルシューティング
======================

認証エラー
----------

**症状**: ``Invalid access token`` または ``401 Unauthorized``

**確認事項**:

1. アクセストークンが正しくコピーされているか確認
2. トークンの有効期限が切れていないか確認（長期トークンを使用）
3. Dropbox App Consoleで必要な権限が付与されているか確認
4. アプリが無効化されていないか確認

ファイルが取得できない
----------------------

**症状**: クロールは成功するがファイルが0件

**確認事項**:

1. アプリの「Access type」が適切か確認:

   - 「Full Dropbox」: Dropbox全体にアクセス可能
   - 「App folder」: 特定フォルダのみアクセス可能

2. 必要な権限が付与されているか確認:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Dropboxアカウントにファイルが存在するか確認

APIレート制限エラー
-------------------

**症状**: ``429 Too Many Requests`` エラー

**解決方法**:

1. Basicプランの場合、``basic_plan=true`` を設定
2. クロール間隔を長くする
3. 複数のアクセストークンを使用して負荷分散

Paperドキュメントが取得できない
-------------------------------

**症状**: Paperドキュメントがクロールされない

**確認事項**:

1. ハンドラ名が ``DropboxPaperDataStore`` になっているか確認
2. 権限に ``files.content.read`` が含まれているか確認
3. Paperドキュメントが実際に存在するか確認

大量のファイルがある場合
------------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

1. データストアを複数に分割（フォルダ単位など）
2. スケジュール設定で負荷を分散
3. Basicプランの場合、APIレート制限に注意

権限とアクセス制御
==================

Dropboxの共有権限を反映
-----------------------

Dropboxの共有設定をFessの権限に反映できます:

パラメーター:

::

    access_token=sl.your-dropbox-token-here
    default_permissions={role}dropbox-users

スクリプト:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.roles
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

``file.roles`` または ``paper.roles`` にDropboxの共有情報が含まれます。

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-box` - Boxコネクタ
- :doc:`ds-gsuite` - Google Workspaceコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
