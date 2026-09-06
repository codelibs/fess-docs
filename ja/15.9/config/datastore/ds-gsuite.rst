==================================
Google Workspaceコネクタ
==================================

概要
====

Google Workspaceコネクタは、Google Drive（旧G Suite）からファイルを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-gsuite`` プラグインが必要です。

15.9での変更点
==============

|Fess| 15.9でコネクタは大幅に再実装されました。既存のデータストア設定をアップグレードする前に、
このセクションを確認してください。

.. warning::

   ``crawl_target`` のデフォルトが ``shared_drives`` になり、 ``legacy`` 以外の値では
   ``impersonate_user`` が必須になりました。そのため、既存の設定をそのままアップグレードすると、
   クロール開始時に ``DataStoreException`` が発生して **起動に失敗します** 。

   これは意図的な動作です。従来の動作ではサービスアカウントに明示的に共有されたファイルにしか
   到達できないため、そのまま動かすと何もインデックスされないクロールが黙って成功してしまいます。
   ``impersonate_user`` にドメイン管理者のアカウントを設定するか、従来の動作を維持する場合は
   ``crawl_target=legacy`` を設定してください。

動作の変更
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 変更点
     - 必要な対応
   * - ``crawl_target`` のデフォルトが ``shared_drives`` になり、 ``impersonate_user`` が必須になった
     - ``impersonate_user`` を設定するか、 ``crawl_target=legacy`` を設定します。設定しない場合、クロールは開始時に失敗します。
   * - デフォルトのOAuthスコープが ``https://www.googleapis.com/auth/drive`` から ``https://www.googleapis.com/auth/drive.readonly`` に変更された
     - Google Workspace管理コンソールのDomain全体への委任は、スコープを明示的に列挙するため、設定の更新が必要です。
   * - ``crawl_target=users`` および ``crawl_target=both`` では ``https://www.googleapis.com/auth/admin.directory.user.readonly`` が追加で必要になった
     - ``scopes`` パラメーターと管理コンソールの委任設定の両方にスコープを追加します。これはクロール開始時に検証されます。
   * - インデックスされるURLがダウンロードリンクからブラウザで開けるリンク（ ``webViewLink`` ）に変更された
     - 新しいURLを反映するには全体の再クロールが必要です。
   * - ``default_permissions`` が追加ではなくフォールバックになった
     - ACLが解決できたドキュメントには、そのACLのみが付与されます。 ``default_permissions`` との和集合ではなくなり、権限は従来より厳しくなります。
   * - リンクを知っている人への共有では検索ロールが付与されなくなった
     - ``allowFileDiscovery=false`` の ``domain`` および ``anyone`` 権限は「リンクを知っている全員」を意味し、Drive自体も検索では見つけられないようにしているためです。
   * - ACLが何も解決できなかったドキュメントは、ロールなしでインデックスされるのではなくスキップされるようになった
     - 引き続きインデックスする場合は ``default_permissions`` を設定します。従来はロールが空だと権限フィルターが無効になるため、そのようなドキュメントは全ユーザーから見えていました。
   * - ``fields`` のデフォルトが ``*`` ではなく明示的なフィールドリストになった
     - 通常使われないフィールドを参照しているクロールスクリプトではnullが返るようになります。従来の動作に戻すには ``fields=*`` を設定します。
   * - GoogleドキュメントのエクスポートがプレーンテキストからMarkdownに、スプレッドシートがCSVからTSVに変更された
     - すべてのGoogleドキュメントのインデックステキストにMarkdownの記法文字が含まれるようになります。全体の再クロールが必要です。
   * - ``refresh_token_interval`` は無視されるようになった
     - トークンの更新は認証ライブラリが行います。既存の設定はそのまま動作し、警告がログに出力されます。
   * - GoogleフォームとGoogleサイトはメタデータのみがインデックスされるようになった
     - Drive APIにエクスポート形式が存在しないためです。従来はこれらがすべてクロールエラーになっていました。

新機能
------

- ``crawl_target`` でクロール対象を選択できます。サービスアカウント自身の視点（ ``legacy`` ）、
  ドメイン内のすべての共有ドライブ（ ``shared_drives`` ）、ディレクトリ内の全ユーザーのマイドライブ
  （ ``users`` ）、またはその両方（ ``both`` ）です。 `クロール対象`_ を参照してください。
- 共有ドライブのアイテムに正しいACLが付与されるようになりました。 `権限とアクセス制御`_ を参照してください。
- Driveの変更フィードを利用した差分クロールに対応しました。 `差分クロール`_ を参照してください。
- ``Retry-After`` に対応した指数バックオフによるレート制限対応と、1つの共有ドライブやユーザーの失敗で
  クロール全体が中断しない仕組みを追加しました。 `レート制限とリトライ`_ を参照してください。
- 認証が必要なプロキシ用に ``proxy_username`` と ``proxy_password`` を追加しました。

対応サービス
============

- Google Drive（マイドライブ、共有ドライブ）
- Googleドキュメント、スプレッドシート、スライド、図形描画、Apps Script
- Googleフォーム、Googleサイト（エクスポート形式がないためメタデータのみ）

前提条件
========

1. プラグインのインストールが必要です
2. Google Cloud Platformプロジェクトの作成が必要です
3. サービスアカウントの作成と認証情報の取得が必要です
4. Google Workspace Domain全体への委任設定が必要です
5. ``crawl_target=legacy`` 以外を使用する場合、代理アクセスするGoogle Workspace管理者アカウントが必要です

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
     - GoogleDriveDataStore
   * - 有効
     - オン

パラメーター設定
----------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com

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
   * - ``impersonate_user``
     - 条件付き
     - Domain全体への委任で代理アクセスするGoogle Workspaceのアカウント。 ``crawl_target=legacy`` 以外では必須で、設定しない場合クロールは開始時に失敗します。 ``shared_drives`` と ``both`` はドメイン管理者権限で共有ドライブを列挙するため、このアカウントはドメイン管理者である必要があります。
   * - ``crawl_target``
     - いいえ
     - クロール対象。 ``legacy`` 、 ``shared_drives`` 、 ``users`` 、 ``both`` のいずれか。デフォルト: ``shared_drives`` 。 `クロール対象`_ を参照してください。
   * - ``scopes``
     - いいえ
     - OAuthスコープ（カンマ区切り）。デフォルト: ``https://www.googleapis.com/auth/drive.readonly`` 。 ``crawl_target=users`` および ``both`` では ``https://www.googleapis.com/auth/admin.directory.user.readonly`` が追加で必要です。
   * - ``user_query``
     - いいえ
     - ``crawl_target=users`` および ``both`` で列挙するユーザーを絞り込むAdmin SDKの ``query`` 。デフォルトは未指定（顧客アカウントの全ユーザー）
   * - ``query``
     - いいえ
     - Google Drive API検索クエリ文字列。差分クロールで使用する変更フィードには適用されません
   * - ``corpora``
     - いいえ
     - 検索対象のコーパス。デフォルト: ``allDrives`` 。 ``crawl_target=legacy`` でのみ使用されるため、デフォルトのクロール対象では効果がありません。 ``shared_drives`` は各ドライブを ``drive`` で、 ``users`` は各マイドライブを ``user`` で列挙します
   * - ``spaces``
     - いいえ
     - 検索対象とするスペース（Google Drive APIの ``spaces`` パラメーター。例: ``drive``、``appDataFolder``）。デフォルトは未指定（API既定値）。 ``crawl_target=legacy`` と ``users`` で使用され、 ``shared_drives`` では無視されます
   * - ``fields``
     - いいえ
     - Google Drive APIから取得するファイルフィールドの指定。デフォルトは ``*`` ではなく明示的なフィールドリストです。スクリプトコンテキスト、ACLの解決、インデックスURL、差分クロールに必要なフィールドを網羅していますが、リストにないフィールドはクロールスクリプトでnullになります。従来どおり全フィールドを取得するには ``fields=*`` を設定します
   * - ``default_permissions``
     - いいえ
     - ドキュメントのDrive ACLが何も解決できなかった場合に使用する権限（カンマ区切り、例: ``{role}drive-users``）。追加ではなくフォールバックであり、ACLが解決できたドキュメントにはそのACLのみが付与されます
   * - ``max_size``
     - いいえ
     - インデックス対象の最大ファイルサイズ（バイト）。デフォルト: ``10000000`` （約10MB）
   * - ``number_of_threads``
     - いいえ
     - 並列処理スレッド数。デフォルト: ``1``
   * - ``incremental``
     - いいえ
     - すべてを列挙する代わりにDriveの変更フィードでクロールするかどうか。デフォルト: ``false`` 。クロール開始前にデータストア設定のパラメーター欄から直接読み込まれます。 `差分クロール`_ を参照してください

詳細パラメーター
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 説明
   * - ``domain_permission_format``
     - ``type=domain`` のDrive権限に適用するロールの書式。 ``{domain}`` がドメイン名に置換されます。デフォルト: ``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - クロール終了時にワーカースレッドの完了を待つ時間（秒）。デフォルト: ``60``
   * - ``page_size``
     - ``files.list`` と ``changes.list`` のページサイズ。デフォルト: ``1000`` 。 ``1000`` を超える値は自動的に切り詰められます
   * - ``permission_page_size``
     - ``permissions.list`` と ``drives.list`` のページサイズ。デフォルト: ``100`` 。 ``100`` を超える値は自動的に切り詰められます
   * - ``max_cached_content_size``
     - メモリ上に保持するコンテンツの最大サイズ（バイト）。これを超えるコンテンツは一時ファイルに退避されます。デフォルト: ``1048576`` （1MB）
   * - ``max_retries``
     - Drive APIのレート制限や一時的な失敗に対するリトライの最大回数。デフォルト: ``5``
   * - ``retry_initial_interval_ms``
     - 最初のリトライまでのバックオフ間隔（ミリ秒）。デフォルト: ``1000``
   * - ``max_backoff_ms``
     - 1回の待機時間の上限（ミリ秒）。デフォルト: ``32000``
   * - ``read_timeout``
     - HTTP読み取りタイムアウト（ミリ秒）。デフォルト: ``20000``
   * - ``connect_timeout``
     - HTTP接続タイムアウト（ミリ秒）。デフォルト: ``20000``
   * - ``proxy_host``
     - プロキシサーバーのホスト名。プロキシは ``proxy_host`` と ``proxy_port`` の両方が設定されている場合にのみ使用され、片方だけでは効果がありません
   * - ``proxy_port``
     - プロキシサーバーのポート番号。 ``proxy_host`` を参照してください
   * - ``proxy_username``
     - 認証が必要なプロキシのユーザー名。設定すると、すべてのリクエストに ``Proxy-Authorization`` ヘッダーが付与されます。何が認証され、何が認証されないかは `制限事項`_ を参照してください
   * - ``proxy_password``
     - 認証が必要なプロキシのパスワード
   * - ``ignore_folder``
     - フォルダをスキップするかどうか。デフォルト: ``true``
   * - ``ignore_error``
     - エラー発生時に処理を継続するかどうか。デフォルト: ``true``
   * - ``supported_mimetypes``
     - インデックス対象のMIMEタイプ（正規表現、カンマ区切り）。デフォルト: ``.*`` （全タイプ）
   * - ``include_pattern``
     - インデックス対象URLの正規表現パターン
   * - ``exclude_pattern``
     - 除外するURLの正規表現パターン
   * - ``refresh_token_interval``
     - 15.9以降は無視されます。アクセストークンの更新は認証ライブラリが行います。既存の設定はそのまま動作し、警告がログに出力されます

.. note::

   ``private_key`` 、 ``private_key_id`` 、 ``client_email`` 、 ``proxy_username`` 、
   ``proxy_password`` はスクリプトの評価コンテキストから除去されるため、クロールスクリプトから
   インデックスに登録することはできず、検索結果に現れることもありません。

.. note::

   差分クロールを有効にすると、コネクタは ``start_page_tokens`` と ``crawl_signature`` を
   データストア設定のパラメーター欄に書き戻します。これらはコネクタが管理する値で、設定した
   パラメーターと並んで表示されますが、編集しないでください。編集や削除を行うと、次回の実行で
   すべてのスコープが全体クロールになります。

クロール対象
------------

サービスアカウントは自身のDriveを持たず、どのGoogleグループにも所属しないため、サービスアカウント
自身として認証するクロールでは、サービスアカウントのアドレスに明示的に共有されたファイルにしか
到達できません。 ``crawl_target`` は、誰の視点でDriveをクロールするかを選択します。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 説明
   * - ``legacy``
     - 従来どおりサービスアカウント自身の視点でクロールします。 ``impersonate_user`` は不要です。サービスアカウントに明示的に共有されたファイルのみが見つかります
   * - ``shared_drives``
     - デフォルト。ドメイン内のすべての共有ドライブを列挙し、それぞれを個別に走査します
   * - ``users``
     - Admin SDKでディレクトリ内の全ユーザーを列挙し、各ユーザーに代理アクセスしてマイドライブを走査します
   * - ``both``
     - ``shared_drives`` の後に ``users`` を実行します。複数のスコープに現れるファイルは1回だけインデックスされます

以下はクロール開始時に検証され、不正な組み合わせの場合は実行されずに ``DataStoreException`` が
発生します。

1. ``crawl_target`` は ``legacy`` 、 ``shared_drives`` 、 ``users`` 、 ``both`` のいずれかであること
2. ``crawl_target=legacy`` 以外の場合、 ``impersonate_user`` が設定されていること
3. ``crawl_target`` が ``users`` または ``both`` の場合、 ``scopes`` に
   ``https://www.googleapis.com/auth/admin.directory.user.readonly`` が含まれていること

.. note::

   ``shared_drives`` と ``both`` はドメイン管理者権限で共有ドライブを列挙するため、
   ``impersonate_user`` に指定するアカウントはGoogle Workspaceのドメイン管理者である必要が
   あります。この列挙はクロール範囲全体を決めるものであるため、恒久的な失敗は記録してスキップ
   するのではなくクロールを中断します。1つも共有ドライブを列挙できなかったクロールは部分的な
   成功ではなく、何もインデックスしないまま成功と報告してはならないためです。

差分クロール
------------

``incremental=true`` を設定すると、各スコープ（1つの共有ドライブ、または代理アクセスする1人の
ユーザーの視点）は、すべてを列挙する代わりにDriveの変更フィードを読み込みます。トークンが保存
されていないスコープは全体をクロールし、次回実行のために変更フィードの開始位置を記録します。

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   差分クロールの実行では ``delete_old_docs`` が強制的に ``false`` になり、明示的に
   ``delete_old_docs=true`` を指定しても尊重されずに上書きされます（警告がログに出力されます）。
   古いドキュメントの削除処理は、今回のクロールで登録されなかったこのデータ設定のドキュメントを
   すべて削除するもので、全体クロールを前提としています。差分クロールでは変更のあったドキュメント
   しか処理しないため、この削除処理はインデックスの残り全部を削除してしまいます。

   Driveから消えたドキュメントを削除するには、 ``incremental=false`` の別のデータストア設定を
   スケジュールしてください。

変更フィードの開始位置は、クロールが完了しワーカースレッドがすべて終了した場合にのみ保存されます。
途中で停止したクロールでは保存されず、次回の実行は同じ変更をもう一度読み込みます。

スコープが返す対象を決める設定、すなわち ``crawl_target`` 、 ``impersonate_user`` 、
``user_query`` 、 ``query`` 、 ``corpora`` 、 ``spaces`` のいずれかが変更された場合も、
保存されている開始位置は破棄され、すべてのスコープが全体クロールになります。保存された開始位置は
それを取得した時点の対象範囲しか表しておらず、設定変更後にそこから再開すると、インデックスに
恒久的な欠落が生じるためです。

レート制限とリトライ
--------------------

Drive APIのレート制限や一時的な失敗は、 ``max_retries`` 、 ``retry_initial_interval_ms`` 、
``max_backoff_ms`` の範囲で指数バックオフによりリトライされます。 ``Retry-After`` ヘッダーは
指数バックオフより優先されますが、誤った値によってクロールが何時間も停止しないよう
``max_backoff_ms`` で上限が設けられます。 ``Retry-After`` は秒数形式のみ有効で、HTTP日付形式の
場合は指数バックオフにフォールバックします。

``429`` 、 ``500`` 、 ``502`` 、 ``503`` 、 ``504`` は常にリトライされます。 ``403`` は
レート制限エラーの場合のみリトライされ、それ以外の ``403`` はリトライしても解決しない認可の失敗
であるため、ただちに記録されます。

ファイル一覧の取得に失敗しても、クロール全体は中断されなくなりました。残りの共有ドライブや
ユーザーのクロールは継続され、失敗はクローラーのログと管理画面の障害URL一覧に記録されます。

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
     - ファイルのURL。 ``webViewLink`` が使用されます。存在しない場合は ``https://drive.google.com/open?id=<ファイルID>`` が使用されます
   * - ``file.thumbnail_link``
     - サムネイルリンク（短期間有効）
   * - ``file.size``
     - ファイルサイズ（バイト）
   * - ``file.roles``
     - アクセス権限
   * - ``file.web_content_link``
     - ダウンロードリンク
   * - ``file.id``
     - Google DriveファイルID
   * - ``file.file_extension``
     - ファイル拡張子
   * - ``file.original_filename``
     - アップロード時のファイル名
   * - ``file.md5_checksum``
     - MD5チェックサム
   * - ``file.owners``
     - ファイルのオーナー
   * - ``file.parents``
     - 親フォルダID
   * - ``file.shared``
     - 共有されているかどうか
   * - ``file.version``
     - ファイルバージョン番号
   * - ``file.icon_link``
     - ファイルタイプアイコンURL
   * - ``file.kind``
     - リソースの種類（``drive#file``）

.. note::

   値が設定されるのは ``fields`` パラメーターで指定したフィールドのみです。取得していない
   フィールドはスクリプト内でnullになります。従来どおり全フィールドを取得するには
   ``fields=*`` を設定してください。

上記以外にも多数のフィールドが利用可能です。
詳細は `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_ を参照してください。

Google形式ファイルのテキスト抽出
--------------------------------

Google形式のファイルはダウンロードできないため、エクスポートが必要です。エクスポート形式は
固定の対応表ではなくDrive APIが実際に返す形式から選択され、エクスポートは10MBが上限です。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 種類
     - エクスポート形式
   * - Googleドキュメント
     - Markdown（ ``text/markdown`` ）。利用できない場合はプレーンテキスト、次にHTML
   * - Googleスプレッドシート
     - TSV（ ``text/tab-separated-values`` ）。利用できない場合はCSV
   * - Googleスライド
     - プレーンテキスト
   * - Google図形描画
     - PNG。インデックスするテキストがないため、メタデータのみが登録されます
   * - Apps Script
     - エクスポートされたJSONから、スクリプトのソースが抽出されてインデックスされます
   * - Googleフォーム、Googleサイト
     - エクスポート不可。メタデータのみが登録され、エラーにはなりません

.. note::

   GoogleドキュメントがMarkdownでエクスポートされるようになったため、すべてのGoogleドキュメントの
   インデックステキストにMarkdownの記法文字が含まれます。すでにインデックスされているドキュメントに
   反映するには、全体の再クロールが必要です。

.. note::

   エクスポート形式はクロールごとに1回Drive APIから取得されます。この取得に失敗した場合は、
   Driveが従来から対応している変換（Googleドキュメントはプレーンテキスト、Googleスプレッドシートは
   CSV）にフォールバックし、警告がログに出力されます。

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
3. ``crawl_target`` が ``users`` または ``both`` の場合は「Admin SDK API」も有効にする

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

   ``crawl_target`` が ``users`` または ``both`` の場合は、両方のスコープを入力します:

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. 「承認」をクリック

.. warning::

   委任の設定はスコープを明示的に列挙するため、以前のバージョンからアップグレードする場合は
   更新が必要です。15.9でデフォルトのスコープが ``https://www.googleapis.com/auth/drive`` から
   ``https://www.googleapis.com/auth/drive.readonly`` に変更されており、ここで許可するスコープは
   データストア設定の ``scopes`` パラメーターと一致している必要があります。

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

すべての共有ドライブのクロール
------------------------------

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com

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
    role=file.roles
    filename=file.name

全ユーザーのマイドライブのクロール
----------------------------------

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=users
    impersonate_user=admin@example.com
    scopes=https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

ユーザーを絞り込む場合は、Admin SDKのクエリを追加します:

::

    user_query=orgUnitPath=/Sales

従来の動作を維持する場合
------------------------

``crawl_target=legacy`` は15.9より前の動作を維持し、サービスアカウントに明示的に共有された
ファイルのみが見つかります。 ``impersonate_user`` は不要です。

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=legacy

権限付きクロール
----------------

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

``default_permissions`` は、Drive ACLが何も解決できなかったドキュメントにのみ使用されます。

特定のファイルタイプのみクロール
--------------------------------

Googleドキュメントのみをクロールする場合は、 ``supported_mimetypes`` パラメーターを使用します。

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
    supported_mimetypes=application/vnd\.google-apps\.document

スクリプト:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    filename=file.name

トラブルシューティング
======================

クロールが開始できない
----------------------

**症状**: クロールが ``DataStoreException`` ですぐに終了する

**解決方法**:

1. ``parameter 'crawl_target' must be one of ...`` : ``crawl_target`` の値が ``legacy`` 、
   ``shared_drives`` 、 ``users`` 、 ``both`` のいずれでもありません
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'`` :
   ``impersonate_user`` にドメイン管理者のアカウントを設定するか、 ``crawl_target=legacy``
   を設定します
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'`` :
   ``scopes`` とDomain全体への委任の設定にこのスコープを追加します

既存の設定をそのままアップグレードした場合、これは想定どおりの結果です。
`15.9での変更点`_ を参照してください。

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
5. OAuth スコープが正しいか確認（ ``https://www.googleapis.com/auth/drive.readonly`` 。
   ``crawl_target`` が ``users`` または ``both`` の場合は
   ``https://www.googleapis.com/auth/admin.directory.user.readonly`` も必要）

Domain全体への委任エラー
------------------------

**症状**: ``Not Authorized to access this resource/api``

**解決方法**:

1. Google Workspace管理コンソールで承認を確認:

   - クライアントIDが正しく登録されているか
   - OAuth スコープが正しいか。委任の設定はスコープを明示的に列挙するため、15.9のスコープ変更に
     合わせて更新が必要です

2. サービスアカウントでDomain全体への委任が有効になっているか確認
3. ``crawl_target`` が ``shared_drives`` または ``both`` の場合、 ``impersonate_user`` に
   指定したアカウントがドメイン管理者であるか確認

ファイルが取得できない
----------------------

**症状**: クロールは成功するがファイルが0件

**確認事項**:

1. ``crawl_target`` が意図した値になっているか確認。 ``legacy`` の場合、サービスアカウントは
   自身のDriveを持たずどのグループにも所属しないため、明示的に共有されたファイルしか見つかりません
2. Google Driveにファイルが存在するか確認
3. サービスアカウントに読み取り権限があるか確認
4. Domain全体への委任が正しく設定されているか確認
5. 対象ユーザーのDriveにアクセス可能か確認

ドキュメントがスキップされる
----------------------------

**症状**: クローラーのログに ``Skipped ... because no permission could be resolved`` が出力される

**解決方法**:

ドキュメントのDrive ACLから検索ロールが1つも解決できなかったため、インデックスされずに
スキップされました。ロールなしでインデックスすると、そのドキュメントでは |Fess| の権限フィルターが
無効になり全ユーザーから見えてしまうため、スキップされます。スキップはクロールの失敗ではないため、
クローラーのログにのみ出力され、障害URL一覧には表示されません。

1. フォールバックの権限を付けてインデックスする場合は ``default_permissions`` を設定します
2. 共有ドライブのACLを読み取れるよう、 ``impersonate_user`` に指定したアカウントがドメイン管理者で
   あるか確認します
3. ドキュメントがリンク共有のみになっていないか確認します。 ``allowFileDiscovery=false`` の
   ``domain`` および ``anyone`` 権限には検索ロールが付与されません。Drive自体もそのような
   ドキュメントを検索で見つけられないようにしているためです

APIクォータエラー
-----------------

**症状**: ``403 Rate Limit Exceeded`` または ``429 Too Many Requests``

**解決方法**:

1. このような失敗は指数バックオフで自動的にリトライされます。それでも失敗する場合は
   ``max_retries`` または ``max_backoff_ms`` を大きくします
2. ``number_of_threads`` を小さくしてリクエスト頻度を下げます
3. Google Cloud Platformでクォータを確認
4. クロール間隔を長くする
5. 必要に応じてクォータの増加をリクエスト

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
   ``crawl_target=shared_drives`` （デフォルト）では、ドメイン管理者権限で共有ドライブを列挙する
   ため、サービスアカウントを個々の共有ドライブのメンバーに追加する必要はありません。代わりに
   ``impersonate_user`` にドメイン管理者を指定してください。

``crawl_target=legacy`` の場合は、各共有ドライブにサービスアカウントを追加する必要があります。

1. Google Driveで共有ドライブを開く
2. 「メンバーを管理」をクリック
3. サービスアカウントのメールアドレスを追加
4. 権限レベルを「閲覧者」に設定

大量のファイルがある場合
------------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

1. ``incremental=true`` を有効にして、前回からの変更のみをクロールする
2. ``crawl_target=both`` を使わず、共有ドライブとユーザーを別々のデータストア設定に分割する
3. ``query`` 、 ``user_query`` 、 ``supported_mimetypes`` で対象を絞り込む
4. スケジュール設定で負荷を分散
5. クロール間隔を調整

権限とアクセス制御
==================

Drive権限からFessロールへの変換
-------------------------------

ドキュメントのACLは、追加のAPI呼び出し回数がファイル数ではなく共有ドライブ数に比例するよう、
次の3段階で解決されます。

1. ファイル一覧に含まれるインラインの権限。追加のコストはかかりません
2. インラインの権限が返らない共有ドライブのアイテムについては、共有ドライブ自体のACL。ドメイン
   管理者権限でドライブごとに1回だけ取得され、キャッシュされます
3. 個別に追加の権限を持つアイテムについては、そのアイテム自身の権限

各Drive権限は次のように |Fess| の検索ロールに変換されます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Drive権限
     - 検索ロール
   * - ``user``
     - そのユーザーのメールアドレスに対応する検索ロール。ファイルのオーナーも常にこの形式で追加されます
   * - ``group``
     - そのグループのメールアドレスに対応する検索ロール。Googleグループのメンバーは展開されません。 |Fess| 側でSSOやLDAPによって解決することを想定しています
   * - ``domain``
     - ``domain_permission_format`` の ``{domain}`` をドメイン名に置換したもの。デフォルト: ``{group}{domain}``
   * - ``anyone``
     - ``guest`` ロール
   * - 上記のうち ``allowFileDiscovery=false`` のもの、および削除済みの権限
     - ロールなし。リンク共有はDrive自体でも検索で見つけられないためです

解決結果が空の場合は、追加ではなくフォールバックとして ``default_permissions`` が使用されます。
``default_permissions`` も未設定の場合、ドキュメントはスキップされます。

Google Driveの共有権限を反映
----------------------------

Google Driveの共有設定をFessの権限に反映:

パラメーター:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

制限事項
========

- Driveの「削除」を示す変更通知には、削除だけでなくアクセス権の喪失も含まれます。
  ``crawl_target=users`` または ``both`` の場合、あるユーザーのアクセス権を剥奪すると、
  別のユーザーがまだ読めるドキュメントであってもインデックスから削除されます。そのファイルに
  次の変更があったとき、または次回の全体クロールで復帰します。
- 差分クロール中にスコープが全体クロールにフォールバックした場合も古いドキュメントの削除処理は
  抑止されたままのため、スコープの開始位置が記録されていない間にDriveから削除されたドキュメントは
  インデックスに残ります。これを削除するには ``incremental=false`` の別のデータストア設定が必要です。
- 削除の反映は、インデックスされたURLにDriveのファイルIDが含まれていることを前提としています。
  ``webViewLink`` とフォールバックURLはこの条件を満たしますが、クロールスクリプトで ``url`` を
  ファイルIDを含まない値に書き換えている場合、削除は反映されません。
- 変更フィードは ``query`` で絞り込まれません。 ``query`` を設定して ``incremental=true`` に
  している場合、クエリに一致しない変更されたファイルもインデックスされます。
- 大規模なドメインで ``crawl_target=both`` を使用すると、およそ
  ``2 + 共有ドライブ数 + ユーザー数`` 回の一覧取得が行われます。共有ドライブとユーザーを別々の
  データストア設定に分割することが現実的な回避策です。
- ``proxy_username`` と ``proxy_password`` は ``Proxy-Authorization`` リクエストヘッダーとして
  送信されるため、認証できるのは平文HTTPのリクエストのみです。Google APIの通信はすべてHTTPSであり、
  認証が必要なプロキシ経由のHTTPS接続は ``CONNECT`` によって確立されますが、これはリクエスト
  ヘッダーではなくJDKの ``java.net.Authenticator`` によって処理されます。このような環境では、
  JVMオプション ``-Djdk.http.auth.tunneling.disabledSchemes=`` と ``Authenticator`` の設定が
  必要です。

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-microsoft365` - Microsoft 365コネクタ
- :doc:`ds-box` - Boxコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
