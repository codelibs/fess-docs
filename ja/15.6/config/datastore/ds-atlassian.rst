==================================
Atlassianコネクタ
==================================

概要
====

Atlassianコネクタは、Atlassian製品（Jira、Confluence）からデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-atlassian`` プラグインが必要です。

対応製品
========

- Jira（Cloud / Server / Data Center）
- Confluence（Cloud / Server / Data Center）

前提条件
========

1. プラグインのインストールが必要です
2. Atlassian製品への適切な認証情報が必要です
3. Cloud版の場合はOAuth 2.0、Server版の場合はOAuth 1.0aまたはBasic認証が利用可能です

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールします:

1. Maven Centralから ``fess-ds-atlassian-X.X.X.jar`` をダウンロード
2. プラグイン管理画面からアップロードしてインストール
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
     - Company Jira/Confluence
   * - ハンドラ名
     - JiraDataStore または ConfluenceDataStore
   * - 有効
     - オン

パラメーター設定
----------------

Cloud版（OAuth 2.0）の例:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Server版（Basic認証）の例:

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Server版（OAuth 1.0a）の例:

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``home``
     - はい
     - AtlassianインスタンスのURL
   * - ``is_cloud``
     - はい
     - Cloud版の場合は ``true``、Server版の場合は ``false``
   * - ``auth_type``
     - はい
     - 認証タイプ: ``oauth``、``oauth2``、``basic``
   * - ``oauth.consumer_key``
     - OAuth 1.0aの場合
     - コンシューマーキー（通常は ``OauthKey``）
   * - ``oauth.private_key``
     - OAuth 1.0aの場合
     - RSA秘密鍵（PEM形式）
   * - ``oauth.secret``
     - OAuth 1.0aの場合
     - 検証コード
   * - ``oauth.access_token``
     - OAuth 1.0aの場合
     - アクセストークン
   * - ``oauth2.client_id``
     - OAuth 2.0の場合
     - クライアントID
   * - ``oauth2.client_secret``
     - OAuth 2.0の場合
     - クライアントシークレット
   * - ``oauth2.access_token``
     - OAuth 2.0の場合
     - アクセストークン
   * - ``oauth2.refresh_token``
     - いいえ
     - リフレッシュトークン（OAuth 2.0）
   * - ``oauth2.token_url``
     - いいえ
     - トークンURL（OAuth 2.0、デフォルト値あり）
   * - ``basic.username``
     - Basic認証の場合
     - ユーザー名
   * - ``basic.password``
     - Basic認証の場合
     - パスワード
   * - ``issue.jql``
     - いいえ
     - JQL（Jiraのみ、高度な検索条件）

スクリプト設定
--------------

Jiraの場合
~~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

利用可能なフィールド:

- ``issue.view_url`` - 課題のURL
- ``issue.summary`` - 課題のサマリー
- ``issue.description`` - 課題の説明
- ``issue.comments`` - 課題のコメント
- ``issue.last_modified`` - 最終更新日時

Confluenceの場合
~~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

利用可能なフィールド:

- ``content.view_url`` - ページのURL
- ``content.title`` - ページのタイトル
- ``content.body`` - ページの本文
- ``content.comments`` - ページのコメント
- ``content.last_modified`` - 最終更新日時

OAuth 2.0認証の設定
===================

Cloud版の場合（推奨）
---------------------

1. Atlassian Developer Consoleでアプリケーションを作成
2. OAuth 2.0認証情報を取得
3. 必要なスコープを設定:

   - Jira: ``read:jira-work``、``read:jira-user``
   - Confluence: ``read:confluence-content.all``、``read:confluence-user``

4. アクセストークンとリフレッシュトークンを取得

OAuth 1.0a認証の設定
====================

Server版の場合
--------------

1. JiraまたはConfluenceでApplication Linkを作成
2. RSA鍵ペアを生成:

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. 公開鍵をApplication Linkに登録
4. 秘密鍵をパラメーターに設定

Basic認証の設定
===============

Server版のシンプルな設定
------------------------

.. warning::
   Basic認証はセキュリティ上推奨されません。可能な限りOAuth認証を使用してください。

Basic認証を使用する場合:

1. 管理者権限を持つユーザーアカウントを用意
2. ユーザー名とパスワードをパラメーターに設定
3. HTTPSを使用してセキュアな接続を確保

JQLによる高度な検索
===================

Jiraの課題をJQLで絞り込む
--------------------------

特定の条件に合致する課題のみをクロール:

::

    # 特定のプロジェクトのみ
    issue.jql=project = "MYPROJECT"

    # 特定のステータスを除外
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # 期間を指定
    issue.jql=updated >= -30d

    # 複数条件の組み合わせ
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

JQLの詳細は `Atlassian JQLドキュメント <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_ を参照してください。

使用例
======

Jira Cloudのクロール
--------------------

パラメーター:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

スクリプト:

::

    url=issue.view_url
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\n\nコメント:\n" + issue.comments
    last_modified=issue.last_modified

Confluence Serverのクロール
---------------------------

パラメーター:

::

    home=https://wiki.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

スクリプト:

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\nコメント:\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

トラブルシューティング
======================

認証エラー
----------

**症状**: ``401 Unauthorized`` または ``403 Forbidden``

**確認事項**:

1. 認証情報が正しいか確認
2. Cloud版の場合、適切なスコープが設定されているか確認
3. Server版の場合、ユーザーに適切な権限があるか確認
4. OAuth 2.0の場合、トークンの有効期限を確認

接続エラー
----------

**症状**: ``Connection refused`` または接続タイムアウト

**確認事項**:

1. ``home`` URLが正しいか確認
2. ファイアウォール設定を確認
3. Atlassianインスタンスが稼働しているか確認
4. ``is_cloud`` パラメーターが正しく設定されているか確認

データが取得できない
--------------------

**症状**: クロールは成功するがドキュメントが0件

**確認事項**:

1. JQLで絞り込みすぎていないか確認
2. ユーザーに読み取り権限があるプロジェクト/スペースか確認
3. スクリプト設定が正しいか確認
4. ログでエラーが発生していないか確認

OAuth 2.0トークンの更新
-----------------------

**症状**: しばらくすると認証エラーが発生

**解決方法**:

OAuth 2.0のアクセストークンは有効期限があります。リフレッシュトークンを設定することで自動更新が可能です:

::

    oauth2.refresh_token=your_refresh_token

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Atlassian Developer <https://developer.atlassian.com/>`_
