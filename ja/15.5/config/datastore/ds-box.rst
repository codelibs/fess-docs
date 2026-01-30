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
3. JWT（JSON Web Token）認証またはOAuth 2.0認証の設定が必要です

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

JWT認証の例（推奨）:

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

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

スクリプトでフォルダパスによるフィルタリングも可能:

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

スクリプトでMIMEタイプによるフィルタリング:

::

    if (file.mimetype == "application/pdf") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        created=file.created_at
        last_modified=file.modified_at
    }

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
3. スケジュール設定で負荷を分散

権限とアクセス制御
==================

Boxのファイル権限を反映
-----------------------

.. note::
   現在の実装ではBoxの詳細な権限情報は取得されません。
   必要に応じて ``role`` フィールドを使用してアクセス制御を設定できます。

デフォルト権限の設定:

::

    # パラメーター
    default_permissions={role}box-users

スクリプトで権限を設定:

::

    url=file.url
    title=file.name
    content=file.contents
    role=["box-users"]
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
