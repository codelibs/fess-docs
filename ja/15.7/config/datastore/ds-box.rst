==================================
Boxコネクタ
==================================

概要
====

Boxコネクタは、Box.comのクラウドストレージからファイルを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-box`` プラグインが必要です。

前提条件
========

1. プラグインのインストールが必要です
2. Box開発者アカウントとアプリケーションの作成が必要です
3. JWT（JSON Web Token）認証の設定が必要です

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # 配置
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 管理画面からインストール

1. 「システム」→「プラグイン」を開く
2. JARファイルをアップロード
3. |Fess| を再起動

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
     - Company Box Storage
   * - ハンドラ名
     - BoxDataStore
   * - 有効
     - オン

パラメーター設定
----------------

JWT認証の例:

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

パラメーター一覧
~~~~~~~~~~~~~~~~

認証パラメーター（必須）
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - パラメーター
     - 必須
     - 説明
   * - ``client_id``
     - はい
     - BoxアプリのクライアントID
   * - ``client_secret``
     - はい
     - Boxアプリのクライアントシークレット
   * - ``public_key_id``
     - はい
     - 公開鍵のID
   * - ``private_key``
     - はい
     - 秘密鍵（PEM形式、改行は ``\n`` で表現）
   * - ``passphrase``
     - はい
     - 秘密鍵のパスフレーズ
   * - ``enterprise_id``
     - はい
     - BoxエンタープライズID

クロールパラメーター（任意）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - パラメーター
     - デフォルト値
     - 説明
   * - ``max_size``
     - ``10000000``
     - クロール対象の最大ファイルサイズ（バイト）。デフォルトは10MB。
   * - ``supported_mimetypes``
     - ``.*``
     - クロール対象のMIMEタイプ（正規表現）。カンマ区切りで複数指定可能。
   * - ``include_pattern``
     - （なし）
     - クロール対象に含めるURLパターン
   * - ``exclude_pattern``
     - （なし）
     - クロール対象から除外するURLパターン
   * - ``number_of_threads``
     - ``1``
     - クロール処理のスレッド数
   * - ``ignore_folder``
     - ``true``
     - フォルダ自体をインデックス対象外にするかどうか
   * - ``ignore_error``
     - ``true``
     - エラー発生時に処理を継続するかどうか
   * - ``filter_term``
     - （なし）
     - ユーザーフィルタリング条件
   * - ``fields``
     - （全フィールド）
     - Box APIから取得するフィールドの指定

接続パラメーター（任意）
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - パラメーター
     - デフォルト値
     - 説明
   * - ``base_url``
     - ``https://app.box.com``
     - Box APIのベースURL
   * - ``max_retry_count``
     - ``10``
     - API呼び出しの最大リトライ回数
   * - ``proxy_host``
     - （なし）
     - HTTPプロキシのホスト名
   * - ``proxy_port``
     - （なし）
     - HTTPプロキシのポート番号
   * - ``refresh_token_interval``
     - ``3540``
     - トークンの更新間隔（秒）。デフォルトは59分。

スクリプト設定
--------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

主要フィールド
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``file.url``
     - ブラウザでファイルを開くリンク
   * - ``file.contents``
     - ファイルのテキストコンテンツ
   * - ``file.mimetype``
     - ファイルのMIMEタイプ
   * - ``file.filetype``
     - ファイルタイプ
   * - ``file.name``
     - ファイル名
   * - ``file.size``
     - ファイルサイズ（バイト）
   * - ``file.created_at``
     - 作成日時
   * - ``file.modified_at``
     - 最終更新日時
   * - ``file.download_url``
     - Box直接ダウンロードURL
   * - ``file.id``
     - BoxアイテムID
   * - ``file.description``
     - ファイルの説明
   * - ``file.extension``
     - ファイル拡張子
   * - ``file.sha1``
     - ファイルのSHA1ハッシュ
   * - ``file.path_collection``
     - フォルダパスのリスト

メタデータフィールド
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``file.type``
     - アイテムタイプ（"file"または"folder"）
   * - ``file.file_version``
     - ファイルバージョン情報
   * - ``file.sequence_id``
     - シーケンスID
   * - ``file.etag``
     - ETagハッシュ
   * - ``file.trashed_at``
     - ゴミ箱移動日時
   * - ``file.purged_at``
     - 完全削除日時
   * - ``file.content_created_at``
     - コンテンツ作成日時
   * - ``file.content_modified_at``
     - コンテンツ更新日時
   * - ``file.created_by``
     - 作成者情報
   * - ``file.modified_by``
     - 更新者情報
   * - ``file.owned_by``
     - 所有者情報
   * - ``file.shared_link``
     - 共有リンク情報
   * - ``file.parent``
     - 親フォルダ情報
   * - ``file.item_status``
     - アイテムステータス
   * - ``file.version_number``
     - バージョン番号
   * - ``file.comment_count``
     - コメント数
   * - ``file.permissions``
     - 権限情報
   * - ``file.tags``
     - タグ情報
   * - ``file.lock``
     - ロック情報
   * - ``file.is_package``
     - パッケージフラグ
   * - ``file.is_watermark``
     - ウォーターマークフラグ
   * - ``file.collections``
     - コレクション情報
   * - ``file.representations``
     - 表現形式情報
   * - ``file.api``
     - BoxファイルAPIオブジェクト（コラボレーション・権限情報取得用）

詳細は `Box File Object <https://developer.box.com/reference#file-object>`_ を参照してください。

Box認証の設定
=============

JWT認証の設定手順
-----------------

1. Box Developer Consoleでアプリケーションを作成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://app.box.com/developers/console にアクセス:

1. 「Create New App」をクリック
2. 「Custom App」を選択
3. 認証方法で「Server Authentication (with JWT)」を選択
4. アプリ名を入力して作成

2. アプリケーションの設定
~~~~~~~~~~~~~~~~~~~~~~~~~

「Configuration」タブで設定:

**Application Scopes**:

- 「Read all files and folders stored in Box」にチェック

**Advanced Features**:

- 「Generate a Public/Private Keypair」をクリック
- 生成されたJSONファイルをダウンロード（重要！）

**App Access Level**:

- 「App + Enterprise Access」を選択

3. エンタープライズで承認
~~~~~~~~~~~~~~~~~~~~~~~~~

Box管理コンソールで:

1. 「Apps」→「Custom Apps」を開く
2. 作成したアプリを承認

4. 認証情報の取得
~~~~~~~~~~~~~~~~~

ダウンロードしたJSONファイルから以下の情報を取得:

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

秘密鍵の形式
~~~~~~~~~~~~

``private_key`` は改行を ``\n`` に置き換えて1行にします:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

使用例
======

企業のBoxストレージ全体をクロール
---------------------------------

パラメーター:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

スクリプト:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

特定のフォルダのみをクロール
----------------------------

``include_pattern`` パラメーターでフォルダパスによるフィルタリングが可能です。

パラメーター:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    include_pattern=.*Documents/Projects/.*

スクリプト:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

PDFファイルのみをクロール
-------------------------

``supported_mimetypes`` パラメーターでMIMEタイプによるフィルタリングが可能です。

パラメーター:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    supported_mimetypes=application/pdf

スクリプト:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

トラブルシューティング
======================

認証エラー
----------

**症状**: ``Authentication failed`` または ``Invalid grant``

**確認事項**:

1. ``client_id`` と ``client_secret`` が正しいか確認
2. 秘密鍵が正しくコピーされているか確認（改行が ``\n`` になっているか）
3. パスフレーズが正しいか確認
4. Box管理コンソールでアプリが承認されているか確認
5. ``enterprise_id`` が正しいか確認

秘密鍵のフォーマットエラー
--------------------------

**症状**: ``Invalid private key format``

**解決方法**:

秘密鍵の改行が正しく ``\n`` に変換されているか確認:

::

    # 正しい形式
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # 間違った形式（実際の改行が含まれている）
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

ファイルが取得できない
----------------------

**症状**: クロールは成功するがファイルが0件

**確認事項**:

1. Application Scopesで「Read all files and folders」が有効か確認
2. App Access Levelが「App + Enterprise Access」になっているか確認
3. Boxストレージに実際にファイルが存在するか確認
4. サービスアカウントに適切な権限があるか確認

大量のファイルがある場合
------------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

データストア設定で処理を分割:

1. クロール間隔を調整
2. 複数のデータストアに分けて設定（フォルダ単位など）
3. ``number_of_threads`` パラメーターでスレッド数を増やす
4. スケジュール設定で負荷を分散

権限とアクセス制御
==================

Boxのファイル権限を反映
-----------------------

.. note::
   現在の実装ではBoxの詳細な権限情報は取得されません。
   必要に応じて ``role`` フィールドを使用してアクセス制御を設定できます。

スクリプトで権限を設定:

::

    url=file.url
    title=file.name
    content=file.contents
    role="{role}box-users"
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-dropbox` - Dropboxコネクタ
- :doc:`ds-gsuite` - Google Workspaceコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
