==================================
Salesforceコネクタ
==================================

概要
====

Salesforceコネクタは、Salesforceのオブジェクト（標準オブジェクト、カスタムオブジェクト）からデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-salesforce`` プラグインが必要です。

対応オブジェクト
================

- **標準オブジェクト**: Account、Contact、Lead、Opportunity、Case、Solution等
- **カスタムオブジェクト**: 独自に作成したオブジェクト
- **Knowledge記事**: Salesforce Knowledge

前提条件
========

1. プラグインのインストールが必要です
2. Salesforce接続アプリケーション（Connected App）の作成が必要です
3. OAuth認証の設定が必要です
4. オブジェクトへの読み取りアクセス権が必要です

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールします。

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
     - Salesforce CRM
   * - ハンドラ名
     - SalesforceDataStore
   * - 有効
     - オン

パラメーター設定
----------------

OAuth Token認証（推奨）:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

OAuth Password認証:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``base_url``
     - はい
     - SalesforceのURL（本番: ``https://login.salesforce.com``、Sandbox: ``https://test.salesforce.com``）
   * - ``auth_type``
     - はい
     - 認証タイプ（``oauth_token`` または ``oauth_password``）
   * - ``username``
     - はい
     - Salesforceユーザー名
   * - ``client_id``
     - はい
     - 接続アプリケーションのConsumer Key
   * - ``private_key``
     - oauth_tokenの場合
     - 秘密鍵（PEM形式、改行は ``\n``）
   * - ``client_secret``
     - oauth_passwordの場合
     - 接続アプリケーションのConsumer Secret
   * - ``security_token``
     - oauth_passwordの場合
     - ユーザーのセキュリティトークン
   * - ``number_of_threads``
     - いいえ
     - 並列処理スレッド数（デフォルト: 1）
   * - ``ignoreError``
     - いいえ
     - エラー時も処理を継続（デフォルト: true）
   * - ``custom``
     - いいえ
     - カスタムオブジェクト名（カンマ区切り）
   * - ``<オブジェクト>.title``
     - いいえ
     - タイトルに使用するフィールド名
   * - ``<オブジェクト>.contents``
     - いいえ
     - コンテンツに使用するフィールド名（カンマ区切り）

スクリプト設定
--------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``object.type``
     - オブジェクトのタイプ（例: Case、User、Solution）
   * - ``object.title``
     - オブジェクトの名前
   * - ``object.description``
     - オブジェクトの説明
   * - ``object.content``
     - オブジェクトのテキストコンテンツ
   * - ``object.id``
     - オブジェクトのID
   * - ``object.content_length``
     - コンテンツの長さ
   * - ``object.created``
     - 作成日時
   * - ``object.last_modified``
     - 最終更新日時
   * - ``object.url``
     - オブジェクトのURL
   * - ``object.thumbnail``
     - サムネイルURL

Salesforce接続アプリケーションの設定
====================================

1. 接続アプリケーションの作成
-----------------------------

Salesforce Setupで:

1. 「アプリケーションマネージャ」を開く
2. 「新規接続アプリケーション」をクリック
3. 基本情報を入力:

   - 接続アプリケーション名: Fess Crawler
   - API参照名: Fess_Crawler
   - 連絡先メール: your-email@example.com

4. 「APIの有効化（OAuth設定の有効化）」にチェック

2. OAuth Token認証の設定（推奨）
--------------------------------

OAuth設定で:

1. 「デジタル署名を使用」にチェック
2. 証明書をアップロード（後述の手順で作成）
3. 選択したOAuthスコープ:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. 「保存」をクリック
5. Consumer Keyをコピー

証明書の作成:

::

    # 秘密鍵の生成
    openssl genrsa -out private_key.pem 2048

    # 証明書の生成
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # 秘密鍵の確認
    cat private_key.pem

証明書（certificate.crt）をSalesforceにアップロードし、
秘密鍵（private_key.pem）の内容をパラメーターに設定します。

3. OAuth Password認証の設定
---------------------------

OAuth設定で:

1. コールバックURL: ``https://localhost`` （使用しませんが必須）
2. 選択したOAuthスコープ:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. 「保存」をクリック
4. Consumer KeyとConsumer Secretをコピー

セキュリティトークンの取得:

1. Salesforceで個人設定を開く
2. 「私のセキュリティトークンのリセット」をクリック
3. メールで送信されるトークンをコピー

4. 接続アプリケーションの承認
-----------------------------

「管理」→「接続アプリケーションを管理する」で:

1. 作成した接続アプリケーションを選択
2. 「編集」をクリック
3. 「許可されるユーザー」を「管理者が承認したユーザーは事前承認済み」に変更
4. プロファイルまたは権限セットを割り当て

カスタムオブジェクトの設定
==========================

カスタムオブジェクトのクロール
------------------------------

パラメーターで ``custom`` にカスタムオブジェクト名を指定:

::

    custom=FessObj,CustomProduct,ProjectTask

各オブジェクトのフィールドマッピング:

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

フィールドマッピングのルール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``<オブジェクト名>.title`` - タイトルに使用するフィールド（単一フィールド）
- ``<オブジェクト名>.contents`` - コンテンツに使用するフィールド（カンマ区切りで複数指定可）

使用例
======

標準オブジェクトのクロール
--------------------------

パラメーター:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

スクリプト:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

カスタムオブジェクトのクロール
------------------------------

パラメーター:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

スクリプト:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Sandbox環境のクロール
---------------------

パラメーター:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

スクリプト:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

トラブルシューティング
======================

認証エラー
----------

**症状**: ``Authentication failed`` または ``invalid_grant``

**確認事項**:

1. OAuth Token認証の場合:

   - Consumer Keyが正しいか確認
   - 秘密鍵が正しくコピーされているか確認（改行が ``\n`` になっているか）
   - 証明書がSalesforceにアップロードされているか確認
   - ユーザー名が正しいか確認

2. OAuth Password認証の場合:

   - Consumer KeyとConsumer Secretが正しいか確認
   - セキュリティトークンが正しいか確認
   - パスワードとセキュリティトークンを連結していないか確認（別々に設定）

3. 共通:

   - base_urlが正しいか確認（本番環境かSandbox環境か）
   - 接続アプリケーションが承認されているか確認

オブジェクトが取得できない
--------------------------

**症状**: クロールは成功するがオブジェクトが0件

**確認事項**:

1. ユーザーにオブジェクトへの読み取り権限があるか確認
2. カスタムオブジェクトの場合、オブジェクト名が正しいか確認（API参照名）
3. フィールドマッピングが正しいか確認
4. ログでエラーメッセージを確認

カスタムオブジェクトの名前
--------------------------

カスタムオブジェクトのAPI参照名を確認:

1. Salesforce Setupで「オブジェクトマネージャ」を開く
2. カスタムオブジェクトを選択
3. 「API参照名」をコピー（通常は ``__c`` で終わる）

例:

- 表示ラベル: Product
- API参照名: Product__c （これを使用）

フィールド名の確認
------------------

カスタムフィールドのAPI参照名を確認:

1. オブジェクトの「項目とリレーション」を開く
2. カスタム項目を選択
3. 「項目名」をコピー（通常は ``__c`` で終わる）

例:

- 項目の表示ラベル: Product Description
- 項目名: Product_Description__c （これを使用）

APIレート制限
-------------

**症状**: ``REQUEST_LIMIT_EXCEEDED``

**解決方法**:

1. ``number_of_threads`` を減らす（1に設定）
2. クロール間隔を長くする
3. Salesforce APIの使用状況を確認
4. 必要に応じてAPI制限の追加を購入

大量のデータがある場合
----------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

1. オブジェクトを複数のデータストアに分割
2. ``number_of_threads`` を調整（2〜4程度）
3. クロールスケジュールを分散
4. 必要なフィールドのみをマッピング

秘密鍵のフォーマットエラー
--------------------------

**症状**: ``Invalid private key format``

**解決方法**:

秘密鍵の改行が正しく ``\n`` になっているか確認:

::

    # 正しい形式
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 間違った形式（実際の改行が含まれている）
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
