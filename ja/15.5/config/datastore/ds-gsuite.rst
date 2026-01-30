==================================
Google Workspaceコネクタ
==================================

概要
====

Google Workspaceコネクタは、Google Drive（旧G Suite）からファイルを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-gsuite`` プラグインが必要です。

対応サービス
============

- Google Drive（マイドライブ、共有ドライブ）
- Googleドキュメント、スプレッドシート、スライド、フォームなど

前提条件
========

1. プラグインのインストールが必要です
2. Google Cloud Platformプロジェクトの作成が必要です
3. サービスアカウントの作成と認証情報の取得が必要です
4. Google Workspace Domain全体への委任設定が必要です

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # 配置
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Company Google Drive
   * - ハンドラ名
     - GSuiteDataStore
   * - 有効
     - オン

パラメーター設定
----------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``private_key``
     - はい
     - サービスアカウントの秘密鍵（PEM形式、改行は ``\n``）
   * - ``private_key_id``
     - はい
     - 秘密鍵のID
   * - ``client_email``
     - はい
     - サービスアカウントのメールアドレス

スクリプト設定
--------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``file.name``
     - ファイル名
   * - ``file.description``
     - ファイルの説明
   * - ``file.contents``
     - ファイルのテキストコンテンツ
   * - ``file.mimetype``
     - ファイルのMIMEタイプ
   * - ``file.filetype``
     - ファイルタイプ
   * - ``file.created_time``
     - 作成日時
   * - ``file.modified_time``
     - 最終更新日時
   * - ``file.web_view_link``
     - ブラウザで開くリンク
   * - ``file.url``
     - ファイルのURL
   * - ``file.thumbnail_link``
     - サムネイルリンク（短期間有効）
   * - ``file.size``
     - ファイルサイズ（バイト）
   * - ``file.roles``
     - アクセス権限

詳細は `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_ を参照してください。

Google Cloud Platform設定
=========================

1. プロジェクトの作成
---------------------

https://console.cloud.google.com/ にアクセス:

1. 新しいプロジェクトを作成
2. プロジェクト名を入力
3. 組織とロケーションを選択

2. Google Drive APIの有効化
---------------------------

「APIとサービス」→「ライブラリ」で:

1. 「Google Drive API」を検索
2. 「有効にする」をクリック

3. サービスアカウントの作成
---------------------------

「APIとサービス」→「認証情報」で:

1. 「認証情報を作成」→「サービスアカウント」を選択
2. サービスアカウント名を入力（例: fess-crawler）
3. 「作成して続行」をクリック
4. ロールは設定不要（スキップ）
5. 「完了」をクリック

4. サービスアカウントキーの作成
-------------------------------

作成したサービスアカウントで:

1. サービスアカウントをクリック
2. 「キー」タブを開く
3. 「鍵を追加」→「新しい鍵を作成」
4. JSON形式を選択
5. ダウンロードされたJSONファイルを保存

5. Domain全体への委任を有効化
-----------------------------

サービスアカウントの設定で:

1. 「Domain全体への委任を有効にする」にチェック
2. 「保存」をクリック
3. 「OAuth 2 クライアントID」をコピー

6. Google Workspace管理コンソールで承認
---------------------------------------

https://admin.google.com/ にアクセス:

1. 「セキュリティ」→「アクセスとデータ管理」→「APIの制御」を開く
2. 「Domain全体への委任」を選択
3. 「新しく追加」をクリック
4. クライアントIDを入力
5. OAuth スコープを入力:

   ::

       https://www.googleapis.com/auth/drive.readonly

6. 「承認」をクリック

認証情報の設定
==============

JSONファイルから情報を取得
--------------------------

ダウンロードしたJSONファイル:

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

以下の情報をパラメーターに設定:

- ``private_key_id`` → ``private_key_id``
- ``private_key`` → ``private_key`` （改行はそのまま ``\n``）
- ``client_email`` → ``client_email``

秘密鍵の形式
~~~~~~~~~~~~

``private_key`` は改行を ``\n`` で保持します:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

使用例
======

Google Drive全体のクロール
--------------------------

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com

スクリプト:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    filename=file.name

権限付きクロール
----------------

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

スクリプト:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

特定のファイルタイプのみクロール
--------------------------------

Googleドキュメントのみ:

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

トラブルシューティング
======================

認証エラー
----------

**症状**: ``401 Unauthorized`` または ``403 Forbidden``

**確認事項**:

1. サービスアカウントの認証情報が正しいか確認:

   - ``private_key`` の改行が ``\n`` になっているか
   - ``private_key_id`` が正しいか
   - ``client_email`` が正しいか

2. Google Drive APIが有効になっているか確認
3. Domain全体への委任が設定されているか確認
4. Google Workspace管理コンソールで承認されているか確認
5. OAuth スコープが正しいか確認（``https://www.googleapis.com/auth/drive.readonly``）

Domain全体への委任エラー
------------------------

**症状**: ``Not Authorized to access this resource/api``

**解決方法**:

1. Google Workspace管理コンソールで承認を確認:

   - クライアントIDが正しく登録されているか
   - OAuth スコープが正しいか（``https://www.googleapis.com/auth/drive.readonly``）

2. サービスアカウントでDomain全体への委任が有効になっているか確認

ファイルが取得できない
----------------------

**症状**: クロールは成功するがファイルが0件

**確認事項**:

1. Google Driveにファイルが存在するか確認
2. サービスアカウントに読み取り権限があるか確認
3. Domain全体への委任が正しく設定されているか確認
4. 対象ユーザーのDriveにアクセス可能か確認

APIクォータエラー
-----------------

**症状**: ``403 Rate Limit Exceeded`` または ``429 Too Many Requests``

**解決方法**:

1. Google Cloud Platformでクォータを確認
2. クロール間隔を長くする
3. 必要に応じてクォータの増加をリクエスト

秘密鍵のフォーマットエラー
--------------------------

**症状**: ``Invalid private key format``

**解決方法**:

改行が正しく ``\n`` になっているか確認:

::

    # 正しい
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 間違い（実際の改行が含まれている）
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

共有ドライブのクロール
----------------------

.. note::
   サービスアカウントで共有ドライブをクロールする場合、
   共有ドライブにサービスアカウントをメンバーとして追加する必要があります。

1. Google Driveで共有ドライブを開く
2. 「メンバーを管理」をクリック
3. サービスアカウントのメールアドレスを追加
4. 権限レベルを「閲覧者」に設定

大量のファイルがある場合
------------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

1. データストアを複数に分割
2. スケジュール設定で負荷を分散
3. クロール間隔を調整
4. 特定のフォルダのみをクロール

権限とアクセス制御
==================

Google Driveの共有権限を反映
----------------------------

Google Driveの共有設定をFessの権限に反映:

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

スクリプト:

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles`` にGoogle Driveの共有情報が含まれます。

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-microsoft365` - Microsoft 365コネクタ
- :doc:`ds-box` - Boxコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
