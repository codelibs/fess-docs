==================================
Microsoft 365コネクタ
==================================

概要
====

Microsoft 365コネクタは、Microsoft 365サービス（OneDrive、OneNote、Teams、SharePoint）からデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-microsoft365`` プラグインが必要です。

対応サービス
============

- **OneDrive**: ユーザードライブ、グループドライブ、共有ドキュメント
- **OneNote**: ノートブック（サイト、ユーザー、グループ）
- **Teams**: チャネル、メッセージ、チャット
- **SharePoint Document Libraries**: ドキュメントライブラリメタデータ
- **SharePoint Lists**: リストとリストアイテム
- **SharePoint Pages**: サイトページ、ニュース記事

前提条件
========

1. プラグインのインストールが必要です
2. Azure ADアプリケーション登録が必要です
3. Microsoft Graph API権限の設定と管理者同意が必要です
4. Java 21以上、Fess 15.2.0以上

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # 配置
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: ソースからビルド

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

インストール後、|Fess| を再起動してください。

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
     - Microsoft 365 OneDrive
   * - ハンドラ名
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - 有効
     - オン

パラメーター設定（共通）
------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

共通パラメーター一覧
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``tenant``
     - はい
     - Azure ADテナントID
   * - ``client_id``
     - はい
     - アプリ登録のクライアントID
   * - ``client_secret``
     - はい
     - アプリ登録のクライアントシークレット
   * - ``number_of_threads``
     - いいえ
     - 並列処理スレッド数（デフォルト: 1）
   * - ``ignore_error``
     - いいえ
     - エラー時も処理を継続（デフォルト: false）
   * - ``include_pattern``
     - いいえ
     - 含めるコンテンツの正規表現パターン
   * - ``exclude_pattern``
     - いいえ
     - 除外するコンテンツの正規表現パターン
   * - ``default_permissions``
     - いいえ
     - デフォルトロール割り当て

Azure ADアプリケーション登録
============================

1. Azure Portalでアプリケーションを登録
---------------------------------------

https://portal.azure.com でAzure Active Directoryを開く:

1. 「アプリの登録」→「新規登録」をクリック
2. アプリケーション名を入力
3. サポートされているアカウントの種類を選択
4. 「登録」をクリック

2. クライアントシークレットの作成
---------------------------------

「証明書とシークレット」で:

1. 「新しいクライアントシークレット」をクリック
2. 説明と有効期限を設定
3. シークレット値をコピー（後で確認できないので注意）

3. API権限の追加
----------------

「APIのアクセス許可」で:

1. 「アクセス許可の追加」をクリック
2. 「Microsoft Graph」を選択
3. 「アプリケーションの許可」を選択
4. 必要な権限を追加（下記参照）
5. 「管理者の同意を与えます」をクリック

データストア別の必要な権限
==========================

OneDriveDataStore
-----------------

必須権限:

- ``Files.Read.All``

条件付き権限:

- ``User.Read.All`` - user_drive_crawler=true の場合
- ``Group.Read.All`` - group_drive_crawler=true の場合
- ``Sites.Read.All`` - shared_documents_drive_crawler=true の場合

OneNoteDataStore
----------------

必須権限:

- ``Notes.Read.All``

条件付き権限:

- ``User.Read.All`` - user_note_crawler=true の場合
- ``Group.Read.All`` - group_note_crawler=true の場合
- ``Sites.Read.All`` - site_note_crawler=true の場合

TeamsDataStore
--------------

必須権限:

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

条件付き権限:

- ``Chat.Read.All`` - chat_id を指定する場合
- ``Files.Read.All`` - append_attachment=true の場合

SharePointDocLibDataStore
-------------------------

必須権限:

- ``Files.Read.All``
- ``Sites.Read.All``

または ``Sites.Selected`` （site_id 指定時、サイト毎に設定必要）

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

必須権限:

- ``Sites.Read.All``

または ``Sites.Selected`` （site_id 指定時、サイト毎に設定必要）

スクリプト設定
==============

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

利用可能なフィールド:

- ``file.name`` - ファイル名
- ``file.description`` - ファイルの説明
- ``file.contents`` - テキストコンテンツ
- ``file.mimetype`` - MIMEタイプ
- ``file.filetype`` - ファイルタイプ
- ``file.created`` - 作成日時
- ``file.last_modified`` - 最終更新日時
- ``file.size`` - ファイルサイズ
- ``file.web_url`` - ブラウザで開くURL
- ``file.roles`` - アクセス権限

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

利用可能なフィールド:

- ``notebook.name`` - ノートブック名
- ``notebook.contents`` - セクションとページの統合コンテンツ
- ``notebook.size`` - コンテンツサイズ（文字数）
- ``notebook.created`` - 作成日時
- ``notebook.last_modified`` - 最終更新日時
- ``notebook.web_url`` - ブラウザで開くURL
- ``notebook.roles`` - アクセス権限

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

利用可能なフィールド:

- ``message.title`` - メッセージタイトル
- ``message.content`` - メッセージコンテンツ
- ``message.created_date_time`` - 作成日時
- ``message.last_modified_date_time`` - 最終更新日時
- ``message.web_url`` - ブラウザで開くURL
- ``message.roles`` - アクセス権限
- ``message.from`` - 送信者情報

SharePoint Document Libraries
------------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

利用可能なフィールド:

- ``doclib.name`` - ドキュメントライブラリ名
- ``doclib.description`` - ライブラリの説明
- ``doclib.content`` - 検索用統合コンテンツ
- ``doclib.created`` - 作成日時
- ``doclib.modified`` - 最終更新日時
- ``doclib.url`` - SharePoint URL
- ``doclib.site_name`` - サイト名

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

利用可能なフィールド:

- ``item.title`` - リストアイテムのタイトル
- ``item.content`` - テキストコンテンツ
- ``item.created`` - 作成日時
- ``item.modified`` - 最終更新日時
- ``item.url`` - SharePoint URL
- ``item.fields`` - すべてのフィールドのマップ
- ``item.roles`` - アクセス権限

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

利用可能なフィールド:

- ``page.title`` - ページタイトル
- ``page.content`` - ページコンテンツ
- ``page.created`` - 作成日時
- ``page.modified`` - 最終更新日時
- ``page.url`` - SharePoint URL
- ``page.type`` - ページタイプ（news/article/page）
- ``page.roles`` - アクセス権限

データストア別の追加パラメーター
================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
-----------------------------

::

    site_id=
    exclude_site_id=
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    ignore_system_pages=true
    page_type_filter=

使用例
======

OneDrive全ドライブのクロール
----------------------------

パラメーター:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

スクリプト:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

特定チームのTeamsメッセージをクロール
------------------------------------

パラメーター:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+09:00

スクリプト:

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

SharePointリストのクロール
--------------------------

パラメーター:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

スクリプト:

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

トラブルシューティング
======================

認証エラー
----------

**症状**: ``Authentication failed`` または ``Insufficient privileges``

**確認事項**:

1. テナントID、クライアントID、クライアントシークレットが正しいか確認
2. Azure Portalで必要なAPI権限が付与されているか確認
3. 管理者の同意が与えられているか確認
4. クライアントシークレットの有効期限を確認

APIレート制限エラー
-------------------

**症状**: ``429 Too Many Requests``

**解決方法**:

1. ``number_of_threads`` を減らす（1または2に設定）
2. クロール間隔を長くする
3. ``ignore_error=true`` を設定して継続処理

データが取得できない
--------------------

**症状**: クロールは成功するがドキュメントが0件

**確認事項**:

1. 対象のデータが存在するか確認
2. API権限が正しく設定されているか確認
3. ユーザー/グループドライブクローラーの設定を確認
4. ログでエラーメッセージを確認

SharePointサイトIDの確認方法
----------------------------

PowerShellで確認:

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

または、Microsoft Graph APIで:

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

大量データのクロール
--------------------

**解決方法**:

1. 複数のデータストアに分割（サイト単位、ドライブ単位など）
2. スケジュール設定で負荷分散
3. ``number_of_threads`` を調整して並列処理
4. 特定のフォルダ/サイトのみをクロール

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-gsuite` - Google Workspaceコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
