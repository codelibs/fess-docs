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
     - 個人アカウントの場合は ``true``、チームアカウントの場合は ``false``（デフォルト: ``false``）
   * - ``max_size``
     - いいえ
     - インデックス対象の最大ファイルサイズ（バイト）（デフォルト: ``10000000``）
   * - ``number_of_threads``
     - いいえ
     - クロールに使用するスレッド数（デフォルト: ``1``）
   * - ``ignore_folder``
     - いいえ
     - フォルダメタデータをスキップするかどうか（デフォルト: ``true``）
   * - ``ignore_error``
     - いいえ
     - コンテンツ抽出時のエラーを無視するかどうか（デフォルト: ``true``）
   * - ``supported_mimetypes``
     - いいえ
     - 許可するMIMEタイプの正規表現パターン（カンマ区切り）（デフォルト: ``.*``）
   * - ``include_pattern``
     - いいえ
     - クロール対象に含めるURLパターン
   * - ``exclude_pattern``
     - いいえ
     - クロール対象から除外するURLパターン
   * - ``default_permissions``
     - いいえ
     - インデックスされたドキュメントのデフォルト権限（カンマ区切り）
   * - ``max_cached_content_size``
     - いいえ
     - メモリにキャッシュするコンテンツの最大サイズ（バイト）。これを超えるコンテンツは一時ファイルに書き出されます（デフォルト: ``1048576``）
   * - ``readInterval``
     - いいえ
     - 各レコードを処理する間に挿入する待機時間（ミリ秒）（デフォルト: ``0``）

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
   * - ``file.id``
     - DropboxファイルID
   * - ``file.path_lower``
     - 小文字のファイルパス
   * - ``file.parent_shared_folder_id``
     - 親共有フォルダID
   * - ``file.content_hash``
     - コンテンツハッシュ
   * - ``file.rev``
     - ファイルリビジョン

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
   * - ``paper.revision``
     - Paperドキュメントのリビジョン

Dropbox認証の設定
=================

アカウント種別とアクセストークン
--------------------------------

このコネクタは ``basic_plan`` パラメーターによって2つの動作モードを切り替えます。
作成すべきアプリとアクセストークンの種類が異なるため、最初に確認してください。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - モード
     - ``basic_plan``
     - 説明
   * - チームアカウント（デフォルト）
     - ``false``
     - Dropbox Business（チーム）アカウント向けです。チーム管理者の権限を持つアクセストークンが必要で、チームメンバーのファイルとチームフォルダを横断的にクロールします。
   * - 個人アカウント
     - ``true``
     - 個人（非チーム）アカウント向けです。通常のスコープ付きアクセストークンを使用し、そのアカウント内のファイルを直接クロールします。

.. note::
   デフォルト（``basic_plan=false``）ではチーム管理用のAPI（チームメンバー一覧、メンバー単位のファイルアクセス、チームフォルダ）を使用するため、
   Dropbox Businessアカウントとチーム管理者権限を持つトークンが必須です。個人アカウントを利用する場合は必ず ``basic_plan=true`` を設定してください。

アクセストークンの取得手順
--------------------------

1. Dropbox App Consoleでアプリを作成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://www.dropbox.com/developers/apps にアクセス:

1. 「Create app」をクリック
2. APIタイプで「Scoped access」を選択
3. アクセスタイプを選択（チームアカウントを横断的にクロールする場合は「Full Dropbox」を推奨）
4. アプリ名を入力して作成

2. 権限の設定
~~~~~~~~~~~~~

「Permissions」タブで必要な権限を選択:

**ファイル・Paperのクロールに必要な権限**:

- ``files.metadata.read`` - ファイルのメタデータ読み取り
- ``files.content.read`` - ファイルおよびPaperドキュメントのコンテンツ読み取り
- ``sharing.read`` - 共有情報の読み取り

**チームアカウント（``basic_plan=false``）で追加で必要な権限**:

- ``members.read`` - チームメンバー一覧の読み取り
- チームデータ／チームスペースへのアクセス権限（メンバー単位のファイルおよびチームフォルダのクロールに必要）

.. note::
   チームアカウントモードでは、チーム管理者として各メンバーやチームフォルダにアクセスします。
   Permissionsタブで上記のチーム関連権限を有効にし、チーム管理者のトークンを生成してください。

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

個人アカウントの設定
====================

個人アカウントでの利用
----------------------

個人アカウント（チームアカウントではない）の場合、
``basic_plan`` パラメーターを ``true`` に設定してください:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

``false``（デフォルト）の場合はチームアカウントとして動作し、チームメンバーやチームフォルダのファイルをクロールします。
``true`` の場合は個人アカウントとして動作し、アカウント内のファイルを直接クロールします。

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

特定のMIMEタイプのみをインデックス対象にするには、``supported_mimetypes`` パラメーターに
許可するMIMEタイプの正規表現をカンマ区切りで指定します。

.. note::
   データストアのスクリプトは1行ごとに ``フィールド名=式`` の独立した式として評価されます。
   そのため、複数行にまたがる ``if`` ブロックで複数のフィールドをまとめて代入することはできません。
   MIMEタイプによる絞り込みは、スクリプトではなく ``supported_mimetypes`` パラメーターで行ってください。

パラメーター（PDFとWordファイルのみ）:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    supported_mimetypes=application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document

スクリプト:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

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

1. ``readInterval`` を設定して各ファイルの処理間隔を空ける
2. ``number_of_threads`` を小さくして同時リクエスト数を減らす
3. データストアをフォルダ単位などで複数に分割し、スケジュールをずらして実行する

.. note::
   ``basic_plan`` はアカウントの種別（チーム／個人）を切り替えるパラメーターであり、
   レート制限の調整には影響しません。アカウントに合わせて正しく設定してください。

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
