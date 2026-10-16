=========================
SharePoint Serverコネクタ
=========================

概要
====

SharePoint Serverコネクタは、オンプレミス版の SharePoint Server（2013、2016、2019、Subscription
Edition）が REST/OData API（および 2013 向けの XML/Atom API）で公開するドキュメントライブラリの
ファイルやリストの項目を取得し、 |Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-sharepoint`` プラグインが必要です。

.. note::

   SharePoint Online（Microsoft 365）をクロールする場合は、このコネクタではなく
   :doc:`ds-microsoft365` を使用してください。このコネクタの OAuth 認証は Azure ACS の
   アプリケーション専用認証にのみ対応しており、Microsoft Graph API との連携機能はありません。

対応バージョン: SharePoint Server 2013 / 2016 / 2019 / Subscription Edition (SE)

取得できるコンテンツ
====================

- ドキュメントライブラリのファイル
- リストの項目（リストアイテム）
- リスト項目の添付ファイル

前提条件
========

1. プラグインのインストールが必要です
2. クロールに使用するアカウントに、クロール対象のサイト・リスト・ドキュメントライブラリへの
   読み取り権限が必要です
3. NTLM / Kerberos（SPNEGO）/ OAuth（ACS）のいずれか1つの認証方式を選択し、
   必要な資格情報を用意してください

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールします:

1. ``fess-ds-sharepoint-X.X.X.jar`` をダウンロード
2. ``$FESS_HOME/app/WEB-INF/lib`` （または ``/usr/share/fess/app/WEB-INF/lib`` ）に配置
3. |Fess| を再起動

または、詳細は :doc:`../../admin/plugin-guide` を参照してください。

設定
====

管理画面から「クローラー」→「データストア」→「新規作成」で設定します。

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 設定例
   * - 名前
     - SharePoint
   * - ハンドラ名
     - SharePointDataStore
   * - 有効
     - オン

パラメーター設定
----------------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

パラメーター一覧
~~~~~~~~~~~~~~~~

**URL / サイト**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``url``
     - はい
     - SharePointサーバーのベースURL（例: ``http://sharepoint.example.com/``）
   * - ``site.name``
     - 条件付き
     - ``/sites/<site.name>/`` 配下のサイトコレクション名。``site.path`` を設定した場合は不要
   * - ``site.path``
     - いいえ
     - サイトのサーバー相対マネージドパス（例: ``/teams/eng``、ルートサイトコレクションは ``/``）。
       設定するとハードコードされた ``/sites/`` プレフィックスの代わりにこの値がそのまま使われ、
       ``site.name`` は不要になる
   * - ``site.list_id``
     - いいえ
     - GUIDでリストを1つ指定してクロール（リストクロールモード）
   * - ``site.list_name``
     - いいえ
     - 表示名でリストを1つ指定してクロール（リストクロールモード）
   * - ``site.doclib_path``
     - いいえ
     - サイト配下のドキュメントライブラリのパス（ドキュメントライブラリクロールモード。例: ``/Shared Documents``）
   * - ``site.exclude_list``
     - いいえ
     - 除外するリストのエンティティ型名の正規表現（カンマ区切り）。サイト全体クロール時のみ有効
   * - ``site.exclude_folder``
     - いいえ
     - 除外するトップレベルフォルダ名の正規表現（カンマ区切り）。サイト全体クロール時のみ有効
   * - ``site.crawl_subsites``
     - いいえ
     - サブサイトを再帰的にクロールするか（デフォルト: ``false``）。詳細は
       `サブサイトとマネージドパス`_ を参照
   * - ``site.max_depth``
     - いいえ
     - ``site.crawl_subsites`` が辿るサブサイトの階層数（デフォルト: ``10``）。ルートを深さ0とする

**認証**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``auth.ntlm.user``
     - いいえ
     - NTLMユーザー名。設定するとNTLM認証が有効になる（``DOMAIN\user`` 形式可）
   * - ``auth.ntlm.password``
     - いいえ
     - NTLMパスワード
   * - ``auth.ntlm.domain``
     - いいえ
     - Windowsドメイン。NTLMの独立したフィールドとして送信される
   * - ``auth.ntlm.workstation``
     - いいえ
     - NTLMネゴシエーションで送信されるワークステーション名
   * - ``auth.kerberos.principal``
     - いいえ
     - クライアントプリンシパル（``user@REALM`` 形式）。設定するとKerberos/SPNEGO認証が有効になる
   * - ``auth.kerberos.keytab``
     - いいえ
     - プリンシパルの鍵を持つキータブファイルのパス。``auth.kerberos.password`` とは排他
   * - ``auth.kerberos.password``
     - いいえ
     - プリンシパルのパスワード。キータブ未設定時のみ使用される
   * - ``auth.kerberos.strip_port``
     - いいえ
     - サービスプリンシパル名からポート番号を除去するか（デフォルト: ``true``）
   * - ``auth.kerberos.use_canonical_hostname``
     - いいえ
     - サービスプリンシパル名を組み立てる前に対象ホストを正規名に解決するか（デフォルト: ``false``）
   * - ``auth.kerberos.krb5_conf``
     - いいえ
     - ``krb5.conf`` のパス。``java.security.krb5.conf`` が未設定の場合のみ適用される
   * - ``auth.kerberos.debug``
     - いいえ
     - ``Krb5LoginModule`` のデバッグ出力を有効にするか（デフォルト: ``false``）
   * - ``auth.oauth.client_id``
     - いいえ
     - Azure ACSのアプリケーション専用OAuthクライアントID。設定するとOAuth認証が有効になる
   * - ``auth.oauth.client_secret``
     - いいえ
     - OAuthクライアントシークレット
   * - ``auth.oauth.tenant``
     - いいえ
     - テナント名（``.sharepoint.com`` を除いた部分）
   * - ``auth.oauth.realm``
     - いいえ
     - Azure ADのレルム（ディレクトリID）

``auth.kerberos.principal`` 、``auth.ntlm.user`` 、``auth.oauth.client_id`` のうち
**設定できるのは1つだけ** です。詳細は `認証`_ を参照してください。

**リスト**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``list.items.number_per_page``
     - いいえ
     - ``GetListItems`` のページサイズ（デフォルト: ``100``）
   * - ``list.item.content.include_fields``
     - いいえ
     - 指定した場合、これらのリスト項目フィールドのみを ``content`` に連結する（カンマ区切り）
   * - ``list.item.content.exclude_fields``
     - いいえ
     - 組み込みで除外される多数の定型フィールドに加えて ``content`` から除外するフィールド名パターン
       （カンマ区切り、各要素は正規表現）
   * - ``list.is_sub_page``
     - いいえ
     - リスト項目をSitePages/wikiのサブページとして扱うか（デフォルト: ``false``）。ページングの
       フォールバックとWebリンクの形式に影響する

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``http.connection_timeout``
     - いいえ
     - HTTP接続タイムアウト（ミリ秒）。コネクションプール待機のタイムアウトとしても使われる
       （デフォルト: ``30000``）
   * - ``http.socket_timeout``
     - いいえ
     - HTTPソケット（読み取り）タイムアウト（ミリ秒、デフォルト: ``30000``）
   * - ``proxy_host``
     - いいえ
     - HTTPプロキシホスト
   * - ``proxy_port``
     - 条件付き
     - HTTPプロキシポート。``proxy_host`` 指定時は必須（デフォルト: ``-1`` = プロキシなし）

**フィルタリングとコンテンツ**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``include_pattern``
     - いいえ
     - クロール対象とする項目の値が一致すべき正規表現。検索結果に表示されるURLではなく、
       ファイルやリスト項目添付ファイルのサーバー相対パス、リスト項目の場合は ``FileRef``
       と比較される点に注意
   * - ``exclude_pattern``
     - いいえ
     - 一致した項目をクロール対象から除外する正規表現
   * - ``supported_mimetypes``
     - いいえ
     - クロール対象とするファイルのMIMEタイプが一致すべき正規表現（カンマ区切り、デフォルト: ``.*``）
   * - ``max_content_length``
     - いいえ
     - クロールするファイルの最大サイズ（バイト）。超過したファイルは失敗ではなくスキップされる
       （デフォルト: ``-1`` = 無制限）
   * - ``extractor_name``
     - いいえ
     - エクストラクタファクトリがMIMEタイプをマッピングできない場合のみ使われるフォールバックの
       エクストラクタ（デフォルト: ``tikaExtractor``）

**動作**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``sp.version``
     - いいえ
     - ``2013`` を指定すると SharePoint 2013向けのXML/Atom、
       ``GetXxxByServerRelativeUrl`` 系APIに切り替わる（未指定時は SharePoint Online /
       2016以降のREST方言）
   * - ``retry_limit``
     - いいえ
     - SharePointサーバー/クライアント例外発生時のクロール単位あたり最大リトライ回数
       （デフォルト: ``2``）
   * - ``role.skip``
     - いいえ
     - 項目ごとの権限取得を完全にスキップするか（デフォルト: ``false``）。詳細は `権限`_ を参照
   * - ``ignore_error``
     - いいえ
     - ファイルのコンテンツ抽出失敗時に、クロール対象を失敗させる代わりにログを出して
       スキップするか（デフォルト: ``false``）
   * - ``default_permissions``
     - いいえ
     - SharePointから取得した権限に加えて、すべてのドキュメントの権限リストに
       マージされるパーミッション文字列（カンマ区切り）
   * - ``delete_old_docs``
     - いいえ
     - 今回のクロールで再取得されなかったドキュメントを削除するか（コア側デフォルト: ``true``）。
       このプラグインは、いずれかのクロール対象が失敗した場合は今回の実行に限りこの値を
       強制的に ``false`` にする
   * - ``number_of_threads``
     - いいえ
     - 同時に処理するクロール対象の数（デフォルト: ``1`` = スレッドプールなし）。
       プロセッサ数の2倍が上限。詳細は `並列クロールと負荷`_ を参照
   * - ``script_type``
     - いいえ
     - データ設定のスクリプトに使うスクリプトエンジン（デフォルト: ``groovy``）
   * - ``readInterval``
     - いいえ
     - 連続するクロール結果の間の待機時間（ミリ秒、デフォルト: ``0``）。他のパラメーターと違い
       camelCase表記である点に注意

スクリプト設定
--------------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - キー
     - リスト項目（ItemCrawl）
     - ドキュメントライブラリファイル（FolderCrawl→FileCrawl）
     - 添付ファイル（ItemAttachmentsCrawl→FileCrawl）
   * - ``url``
     - Webリンク
     - ファイルURL
     - ファイルURL
   * - ``host``
     - ホスト名
     - ホスト名
     - ホスト名
   * - ``site``
     - サーバー相対パス（``FileRef``）
     - サーバー相対パス
     - サーバー相対パス
   * - ``title``
     - ``Title`` フィールド、無ければ ``FileLeafRef``/ファイル名
     - ドキュメントライブラリファイル自身の ``Title`` 値（あれば）、無ければファイル名
     - ファイル名
   * - ``titleWithListName``
     - ``"[リスト名] タイトル"``
     - ``"[リスト名] ファイル名"`` （ドキュメントライブラリクロールではリスト名は常に空なので
       実質ファイル名のみ）
     - ``"[リスト名] ファイル名"``
   * - ``listName``
     - リストの表示名、または ``""``
     - 常に ``""``
     - 実際のリスト名
   * - ``content``
     - フィールド値の連結
     - 抽出されたテキスト
     - 抽出されたテキスト
   * - ``digest``
     - ``content`` の要約
     - ``content`` の要約
     - ``content`` の要約
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - 一覧取得結果から
     - 一覧取得結果から
     - 一覧取得結果から
   * - ``created``
     - 一覧取得結果から
     - 一覧取得結果から
     - 一覧取得結果から
   * - ``mimetype``
     - 常に ``text/html``
     - 検出値
     - 検出値
   * - ``filetype``
     - ``mimetype`` から導出
     - ``mimetype`` から導出
     - ``mimetype`` から導出
   * - ``role``
     - 権限リスト（空でない場合のみ）
     - 権限リスト（空でない場合のみ）
     - 権限リスト（空でない場合のみ）
   * - ``list_name``
     - あり
     - **なし**
     - あり
   * - ``list_id``
     - あり
     - **なし**
     - あり
   * - ``item_id``
     - あり
     - **なし**
     - あり

.. note::

   ``content_length`` は ``content.length()`` 、つまり抽出・連結されたテキストの
   文字数（UTF-16コード単位）であり、ファイルのバイトサイズではありません。Box や
   Google Drive、Dropboxコネクタの ``file.size`` （サービス側のメタデータによる実際の
   バイトサイズ）とは値の性質が異なるため、両者を比較しないでください。

**動的キー: ``val_*``**

リスト項目の ``FieldValuesAsText`` （SharePointがそのアイテムについて返す生のフィールド値マップ。
``odata.metadata`` などのOData用メタデータキーを含む）の各キーは、2つの名前で公開されます:
プレフィックスなし（上記の固定キーと同名でない場合のみ）と、常に ``val_`` プレフィックス付きの
両方です。例えば ``Status`` フィールドは ``Status`` と ``val_Status`` の両方になります。

``val_*`` キーが存在するのは **リスト項目クロール（ItemCrawl）のみ** です。ドキュメントライブラリ
ファイル（FolderCrawl→FileCrawl）やリスト項目の添付ファイル（ItemAttachmentsCrawl→FileCrawl）では
``val_*`` キーは一切生成されません。

認証
====

3つの認証方式があり、**設定できるのはそのうち1つだけ** です。``auth.kerberos.principal`` 、
``auth.ntlm.user`` 、``auth.oauth.client_id`` のうち2つ以上を設定すると、リクエストが送信される
前にデータ設定ジョブがバリデーションエラーで失敗します。これは意図的な制限です。HTTPクライアントに
登録される資格情報は1つだけであり、その資格情報が登録されるスコープは ``Negotiate`` チャレンジにも
``NTLM`` チャレンジにも同じように一致してしまうため、複数設定するとログからは原因の分からない401が
返るだけになります。

NTLM
----

::

    auth.ntlm.user={SharePointユーザー名}
    auth.ntlm.password={パスワード}
    auth.ntlm.domain={Windowsドメイン。省略可、デフォルトは未設定}
    auth.ntlm.workstation={NTLMネゴシエーションで送信するワークステーション名。省略可、デフォルトは未設定}

``auth.ntlm.domain`` と ``auth.ntlm.workstation`` はどちらもデフォルトで未設定であり、これまでと
同じ資格情報が組み立てられます。ユーザー名に ``DOMAIN\user`` の形でドメインを書き込む方法も
引き続き有効です。``auth.ntlm.domain`` を設定すると、ドメインをNTLMの独立したフィールドとして
送信するようになります。結合形式を拒否するサーバーではこちらを使ってください。

Kerberos（SPNEGO）
------------------

**サポート範囲は次の構成に限られます:** クローラーJVMは1つ、Fessインスタンスごとに ``krb5.conf``
は1つ、認証はキータブまたはパスワード、委任（delegation）なし、チャネルバインディングなし、
NTLM・OAuthとは排他。これ以外の構成はサポート対象外です。

::

    auth.kerberos.principal={クライアントプリンシパル。user@REALM の形式で書く。設定するとKerberosが有効になる}
    auth.kerberos.keytab={プリンシパルの鍵を持つキータブファイルのパス。auth.kerberos.password とは排他}
    auth.kerberos.password={プリンシパルのパスワード。キータブ未設定時のみ使用}
    auth.kerberos.strip_port={true/false。サービスプリンシパル名からポート番号を除去するか。デフォルトtrue}
    auth.kerberos.use_canonical_hostname={true/false。対象ホストを正規名に解決してからSPNを組み立てるか。デフォルトfalse}
    auth.kerberos.krb5_conf={krb5.confのパス。java.security.krb5.conf が未設定の場合のみ適用}
    auth.kerberos.debug={true/false。Krb5LoginModuleのデバッグ出力。デフォルトfalse}

- **``krb5.conf`` は ``jvm.crawler.options`` に設定します**
  （例: ``-Djava.security.krb5.conf=/path/to/krb5.conf``）。データストアのクロールは
  クローラーの **子プロセス** で実行されるため、webapp側にしか影響しない設定をしても効果がなく、
  webappの再起動でも反映されません。反映させるにはクロールジョブを再実行する必要があります。
  ``auth.kerberos.krb5_conf`` は、まだ何もこのプロパティを設定していない場合の簡易手段であり、
  **既に設定済みの値を上書きすることは決してありません** （このプロパティはJVM全体で共有され、
  1つのクローラーJVMがクロールジョブのすべてのデータ設定を実行するため）。上書きしなかった場合は
  両方のパスを記載した警告がログに出力されます。
- **``krb5.conf`` の ``[libdefaults]`` に ``udp_preference_limit = 1`` を設定してください。**
  これがないとJDKはまずUDPで問い合わせ、KDCが応答しない場合（到達不能、ファイアウォールが
  UDP 88をドロップしている、応答がデータグラムサイズを超えている、など）にTCPへフォールバックする
  前に30秒間隔で3回リトライします。ログに何も残らないまま認証1回あたり1分半ほどクロールが
  止まって見えるときは、たいていこれが原因です。
- **プリンシパルは常に ``user@REALM`` の形式で書いてください。** ``default_realm`` はJVM全体で
  共有される設定であり、複数のレルムにまたがる複数のSharePointファームが1つの ``krb5.conf`` を
  共有することもあるため、レルムを省略した ``user`` はそのファイルがたまたま指しているレルムに
  対して解決されてしまいます。
- **``auth.kerberos.use_canonical_hostname`` はデフォルト ``false``** です。Apache HttpClient
  自身のデフォルトとは意図的に異なります。有効にすると、サービスプリンシパル名を組み立てる前に
  対象ホストが逆引きDNSにかけられ、代替アクセスマッピングやロードバランサー配下では、どのSPNも
  登録されていない名前が生成されてしまい、結果として起こる失敗からはDNSが原因だとまったく
  分かりません。SPNが本当に正規名に対して登録されている場合にのみ有効にしてください。
- **IIS Extended Protectionが ``tokenChecking=Require`` に設定されている場合は動作しません。**
  Apache HttpClientはバージョン4.5系・5.x系のどちらもチャネルバインディングに対応していません。
  IISの既定値は ``None`` なので通常は影響を受けませんが、``Require`` になっている環境に対する
  回避策はありません。
- **チケットはクロール用のHTTPクライアントを構築する際に一度だけ取得され、以後更新されません。**
  チケットの有効期間よりも長く動くクロールは、途中から認証に失敗するようになります。
- **``auth.kerberos.password`` は、``auth.ntlm.password`` と同様に平文で保存・表示されます。**
  Fessにはデータストアハンドラのパラメーターをマスキングする仕組みがなく、データ設定編集画面は
  これらをプレーンテキストのテキストエリアとして描画します。可能な場合は
  ``auth.kerberos.keytab`` を使い、キータブファイルには制限的なパーミッションを設定してください。
- ``auth.kerberos.debug=true`` にすると、``Krb5LoginModule`` はFessのログではなく
  クローラープロセスの標準出力に書き込みます。

OAuth（ACS）
------------

::

    auth.oauth.client_id={OAuthクライアントID}
    auth.oauth.client_secret={OAuthクライアントシークレット}
    auth.oauth.tenant={テナント名。.sharepoint.com を除いた部分}
    auth.oauth.realm={Azure ADのレルム（ディレクトリID）}

``auth.oauth.client_id`` を設定すると、Windows Azure Access Control Service
（``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``）に対する
クライアントクレデンシャル（アプリケーション専用）フローが有効になります。アクセストークンは
クロール用のHTTPクライアント構築時に一度だけ取得され、すべてのリクエストに ``Bearer``
``Authorization`` ヘッダーとして付与されます。401が返った場合は1回だけ更新して再試行します。
**MicrosoftはACSを非推奨としており廃止が予定されています。** OAuthを設定したクロールのたびに
この旨の警告がログに出力されます。このプラグインにはEntra IDのアプリ登録（証明書またはクライアント
シークレットによる）フローは実装されておらず、レガシーなACSアプリケーション専用認証のみに
対応しています。

OAuthを有効にする判定は ``auth.oauth.client_id`` の有無だけで行われます。``client_secret`` 、
``tenant`` 、``realm`` は無条件に読み込まれ、省略すると空のまま黙って使われるため、専用の
バリデーションメッセージなしにトークン取得が失敗することがあります。

**``sp.version=2013`` とOAuthの組み合わせは一度も機能したことがありません。** このプラグインが
SharePoint 2013向けに行うすべてのAPI呼び出しはXML/Atomクライアントを経由しますが、そのクライアントの
どのコードパスもOAuthトークンをリクエストに付与しません。そのため両方を設定すると、すべての
リクエストが未認証のまま送信されます。クロールはこの事実をそのままログに警告として出力しますが、
ジョブを失敗させることはありません。SharePoint 2013には ``auth.ntlm.*`` を使用してください。

権限
====

``role.skip=true`` （デフォルト ``false``）を設定すると、項目ごとの権限取得を完全にスキップします:
``GetListItemRole`` は一切呼び出されず、項目に ``role`` キーが設定されることもなく、ドキュメントには
データ設定自体の静的な権限設定と、設定していれば ``default_permissions`` だけが適用されます —
SharePoint由来の権限はまったく反映されません。

権限を取得する場合、SharePoint自身のユーザー・セキュリティグループ・SharePointグループは展開され、
Fessの検索用ロールにマッピングされます:

- **オンプレミスAD** のアカウントやグループ（ログイン名にバックスラッシュを含み、Azureの
  クレームプレフィックスで始まらないもの）は、標準のADユーザー/グループ用ロールヘルパーで
  マッピングされます。
- **Azure AD（Entra ID）** のアカウント（ログイン名が ``i:0#.f|membership|`` で始まるもの）は
  **2通り** にマッピングされます — Azureクレームの完全な値による1つと、そのクレームの ``@`` より
  前のADアカウント部分による1つで、同じユーザーに対してEntra ID形式とAD形式の両方のロールが
  追加されます。いくつかのクレーム形式プレフィックス（特別な「全員」グループである
  ``spo-grid-all-users`` を含む）のいずれかでAzureと判定されたセキュリティグループも、同様に
  両方の形式でマッピングされます。
- **SharePointグループ** は自身のメンバーシップ（ユーザー、セキュリティグループ、ネストした
  グループ）を再帰的に展開します。互いを含み合うグループ間の無限再帰を止めるための、訪問済み
  グループのガードも備えています。

``default_permissions`` （カンマ区切り）は、上記すべての **後に** マージされます。そのため
SharePointが項目に対して権限を一切返さなかった場合（``role.skip=true`` の場合と「SharePointが
何も返さなかった」場合の両方に該当）でも適用されます。最終的な権限リストは、データ設定自体の
静的な権限設定・SharePoint由来のロール（``role.skip`` していない場合）・``default_permissions``
の和集合を重複排除したものになります。

サブサイトとマネージドパス
==========================

``site.path`` を設定すると、ハードコードされた ``/sites/`` プレフィックスの代わりにサーバー相対
マネージドパスがそのまま使われ、``site.name`` は不要になります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - シナリオ
     - 設定
   * - ルートサイトコレクション
     - ``site.path=/``
   * - ``/teams/eng`` サイト
     - ``site.path=/teams/eng``
   * - 従来どおり ``/sites/mysite/``
     - ``site.name=mysite`` （``site.path`` は設定しない）

``site.crawl_subsites`` （デフォルト ``false``）を有効にすると、サイト全体クロール（
``site.list_name`` も ``site.doclib_path`` も設定していないクロール）が、``_api/web/webinfos``
で見つかったサブサイトへ再帰的に展開されます。未設定のままであれば、クロールがこれまでどおり
まったく同じリクエストしか出さないこと（``webinfos`` すら一度も要求しないこと）は保証されています。

サブサイトのドキュメントは、ルートサイトのものと同じデータ設定内に、それぞれのサーバー相対パスの
もとでインデックス登録されます。あるドキュメントがサブサイト由来かルートサイト由来かをインデックス側
から区別する情報はありません。

``site.max_depth`` （デフォルト ``10``）は、``site.crawl_subsites=true`` のときにルートサイトから
何階層下のサブサイトまで辿るかを制限します。ルートサイト自身が深さ0なので、``site.max_depth=1`` は
ルートの直接の子サイトまでしか辿りません。``site.crawl_subsites=true`` のまま ``site.max_depth`` に
``1`` 未満を設定すると、この機能は実質的に無効化され（サブサイトは一切クロールされません）、
クロール開始時に警告としてログに出力されます。

サブサイトを有効にすると、発見されたサブサイト数にほぼ比例して（``site.max_depth`` を上限として）
**クロール全体の所要時間が増大します** — サブサイトごとに、フォルダ一覧・リスト一覧の取得、
そして深さの上限に達していなければ ``webinfos`` の呼び出しが、ルートサイトのクロールに
加えて発生するためです。

例に示したとおり、`並列クロールと負荷`_ の節で説明する ``number_of_threads`` や ``readInterval`` は
サブサイトを含むクロール全体にも同様に適用されます。

並列クロールと負荷
==================

``number_of_threads`` （デフォルト ``1``）は、同時に処理するクロール対象の数です。デフォルトの
ままではこれまでどおり、すべての対象がクロールスレッド上で処理され、**スレッドプールはまったく
作成されません。**

この値は、Fessを実行しているマシンの **プロセッサ数の2倍を上限** としてキャップされます。データ
設定がホストの処理能力を超える並列度を要求できないようにするためです。``1`` 未満の値や、空・
解析不能な値は、尊重されたり失敗させられたりするのではなく ``1`` にフォールバックします。
キャップされた場合や ``1`` 未満だった場合は要求値と実際の値の両方がログに出力され、解析できない
場合は警告がログに出力されます。**空欄の場合は何もログに出力されません** — 空欄はそのパラメーターが
単に設定されていないことを意味するためです。

HTTPコネクションプールはこの値に連動してサイズが調整されます。Apache HttpClientは既定では1ルート
あたり2コネクションしか許可せず、このクロールは丸ごと1つのルートとして扱われるため、コネクション
プールを大きくしなければ3番目以降のスレッドはリクエストを送る代わりにコネクション待ちに費やす
時間の方が長くなってしまいます。

**``readInterval`` は、この値を何に設定しても、ドキュメントの受け渡しを1件ずつのペースで
制御し続けます。** スレッドはクロールの発見・取得を速くしますが、ドキュメントがインデクサーに
届く速さを速くするわけではありません。これは意図的な設計です — 運用者が設定した間隔をスレッド数で
割ってしまうと、その間隔で制限しようとしていた負荷そのものを逆に増幅させてしまうためです。
1件のドキュメント処理を終えたワーカーは、それより前のドキュメントがまだ受け渡し中であれば、
ただ待機します。

``number_of_threads`` を上げることで実際に増えるのは、**SharePointに対するリクエストの
レート** です。後述の503バックオフと ``X-SharePointHealthScore`` による待機は、クロール対象
ごとに、それをクロールしているスレッド上で適用されるため、``n`` 個のスレッドは単一スレッドの
クロールの最大 ``n`` 倍のリクエストを送ることになります — ファームが「今は忙しい」と伝えている
最中も含めてです。オンプレミスファームに対しては、この値は段階的に上げてください。

スレッド数を増やしても効果に上限がある理由が2つあります:

- **各SharePointグループのメンバーシップは、最初に読み込まれるときだけ1スレッドずつ順番に
  読み込まれます。** 権限はクロール全体で共有されるキャッシュを通じて解決され、そのキャッシュは
  グループのメンバー取得の間ロックで保護されます。このロックがあるおかげで、あるスレッドが
  「メンバーがまだ読み込み中のグループ」を別のスレッドに渡してしまい、そのグループが保護している
  項目を権限抜きでインデックスしてしまう事態を防いでいます。一度キャッシュに載ったグループへの
  以降の参照は安価な参照になるため、これは **コールドキャッシュのコスト** です — 異なるグループが
  多いサイトのクロールは序盤が単一スレッドに近い速度になり、少数のグループを項目が共有している
  サイトではほとんど影響がありません。権限をまったく読まない ``role.skip=true`` はこのコストを
  完全に回避します。
- サイトごとの発見処理は逐次的です。1サイトのフォルダ一覧とリスト一覧は1つのクロール対象なので、
  その対象の処理が終わって発見結果がキューに入るまで、スレッド間で分担する作業がありません。

**503応答** は他のエラーと同様に ``retry_limit`` 回までリトライされますが、リトライのたびに
待機時間が増加します: 2秒、4秒、8秒と30秒を上限に倍増し、それぞれ実際の待機時間はその値の
70〜129%でランダム化されます。503を返し続けるクロール対象は、実際にリトライが行われるたびに
この待機を払いますが、最後のリトライの後には払いません — ``retry_limit`` に達して結局
諦められる対象を、無意味に遅延させることはしません。

**すべてのレスポンス** — 成功・失敗を問わず、クロールが破棄しようとしている一覧のページも含めて
— は ``X-SharePointHealthScore`` レスポンスヘッダー（0がアイドル、10が非常に忙しい）を
チェックされます。スコアが9以上になると、クロールは次の処理を行う前に待機します: スコア9は
上記の最初の503リトライと同じ約2秒、スコア10は約4秒、以降9を超えるごとに倍増します。**これには
上限がなく、クロール全体を通じて積み重なります** — 継続的に高負荷なファームがヘルススコア9で
張り付いていると、このデータストアが送る **リクエスト1件ごとに** 約2秒が加算され続け
（フォルダ一覧・リスト一覧の1ページごとも含めて）、本来なら数時間で終わるはずのクロールが
桁違いに長くなることがあります。クロールが予想外に大幅に遅くなった場合は、まず何よりも先に
その時間帯のファームのヘルススコアを確認してください。

設定例
======

いずれもNTLM認証を前提とした例です。Kerberos・OAuthを使う場合は `認証`_ を参照して
``auth.ntlm.*`` の行を置き換えてください。

リストのクロール
----------------

パラメーター:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

スクリプト:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

ドキュメントライブラリのクロール
--------------------------------

パラメーター:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

スクリプト:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

``/teams/`` サイトのクロール
----------------------------

``site.path`` を使うと、``/sites/`` 以外のマネージドパスにあるサイトのドキュメントライブラリを
直接指定できます。

パラメーター:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

スクリプト:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

サブサイト再帰クロール
----------------------

ルートサイトコレクションを起点に、深さ3階層までサブサイトを辿ります。

パラメーター:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

スクリプト:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

制限事項
========

- **増分クロール・差分クロールには一切対応していません。** 変更トークンや差分クエリ、
  「前回以降に更新された項目だけ」のフィルタリングはこのプラグインのどこにも存在せず、
  実行のたびに設定されたすべてのリスト・フォルダ・ファイルを完全に一覧取得します。
  ``delete_old_docs`` は、今回の完全クロールで再び見つからなかったドキュメントを削除するか
  どうかを制御するだけの後始末であり、差分取得ではありません。
- **ファイル名・フォルダ名中の ``%`` と ``#``** は、デフォルト（``2013`` 以外）の
  コードパスでサポートされています。この2文字をファイル名・フォルダ名に使えるのは
  SharePoint Server 2019とSubscription Editionだけで、2016は明示的に拒否し、2013も拒否します。
  デフォルトのコードパスは、デコード済みパスを受け取る ``...ByServerRelativePath(decodedUrl=...)``
  系エンドポイントでこうしたファイルにアクセスし、インデックスに登録するリンクの中でも
  この2文字をエスケープします。**``sp.version=2013`` ではこうしたファイルにアクセスできません。**
  古い ``...ByServerRelativeUrl(...)`` 系エンドポイントを使い、これは引数をエンコード済みURLとして
  解釈するためです。これは不具合ではなく意図的な制限です。SharePoint 2013のファーム自体が
  そうした名前を保持できないため、問題になるのは ``sp.version=2013`` を2019や
  Subscription Editionのサーバーに対して使った場合だけであり、その組み合わせは推奨されません。
  詳細は `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  と `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__
  を参照してください。
- **IIS Extended Protectionが ``tokenChecking=Require`` の環境ではサポートできません。**
  Apache HttpClientはバージョン4.5系・5.x系のどちらもチャネルバインディングを実装していません。
  IISの既定値は ``None`` なのでほとんどのファームは影響を受けませんが、``Require`` に設定された
  ファームに対する回避策はありません。
- **データ設定パラメーターに書いたパスワードは平文で保存・表示されます。** これは
  ``auth.ntlm.password`` と ``auth.kerberos.password`` の両方に当てはまります。Fessには
  データストアハンドラのパラメーターをマスキングする仕組みがなく、データ設定編集画面はこれらを
  プレーンテキストのテキストエリアとして描画します。Kerberosが使える環境では
  ``auth.kerberos.password`` より ``auth.kerberos.keytab`` を優先し、キータブファイルには
  制限的なパーミッションを設定してください。
- **``sp.version=2013`` とOAuthの組み合わせは一度も機能したことがありません。** SharePoint
  2013向けのすべてのAPI呼び出しはXML/Atomクライアントを経由しますが、そのクライアントのどの
  コードパスもOAuthトークンをリクエストに付与しないため、両方を設定するとすべてのリクエストが
  未認証のまま送信されます。SharePoint 2013には ``auth.ntlm.*`` を使用してください。
- **``/sites/`` および ``site.path`` で設定した1つのマネージドパス以外は、自動的には
  発見されません。** ``site.crawl_subsites`` は設定したルートサイトからの再帰のみを行い、
  ``site.path`` はそこで設定した1つのマネージドパスだけに到達します。ファーム上の
  すべてのマネージドパスを網羅するものではありません。

トラブルシューティング
======================

認証が無言で失敗する場合
------------------------

**症状**: 401などが返るが、ログにはっきりした原因が出ない

**確認事項**:

1. ``auth.kerberos.principal`` 、``auth.ntlm.user`` 、``auth.oauth.client_id`` のうち
   複数を設定していないか確認する（2つ以上設定するとジョブ開始前にバリデーションエラーになる）
2. Kerberosを使う場合、``jvm.crawler.options`` に
   ``-Djava.security.krb5.conf=...`` が設定されているか確認する。webapp側にしか設定していないと
   反映されない。設定変更後はクロールジョブを再実行する（webappの再起動では反映されない）
3. Kerberosの ``krb5.conf`` の ``[libdefaults]`` に ``udp_preference_limit = 1`` が
   設定されているか確認する。無い場合、KDCが無応答だと認証1回あたり約90秒
   （30秒×3回のUDPリトライ）ハングしたように見えることがある
4. プリンシパルが ``user@REALM`` 形式で書かれているか確認する（レルムを省略すると
   ``krb5.conf`` の ``default_realm`` に依存してしまう）
5. OAuthの場合、``client_secret`` / ``tenant`` / ``realm`` が空でないか確認する
   （存在チェックは ``client_id`` にしか行われないため、他が空でも起動時エラーにならない）
6. IIS側のExtended Protectionが ``tokenChecking=Require`` になっていないか確認する
   （この場合は回避策がない）
7. 長時間動作するクロールでは、Kerberosチケットの有効期間が途中で切れ、後半だけ認証に
   失敗することがある（チケットはHTTPクライアント構築時に一度だけ取得され、更新されない）

クロールが遅い場合（503とヘルススコア）
---------------------------------------

**症状**: クロールが予想より大幅に遅い、またはタイムアウトする

**確認事項**:

1. その時間帯のSharePointファームの ``X-SharePointHealthScore`` を確認する。9以上になると
   リクエストのたびに待機が発生し（9で約2秒、10で約4秒、以降倍増、合計に上限なし）、
   高負荷なファームではクロール全体が桁違いに長くなることがある
2. 503応答が続いていないか確認する。503は ``retry_limit`` 回までリトライされ、
   そのたびに2秒→4秒→8秒（上限30秒）の待機が入る
3. ``number_of_threads`` を上げすぎていないか確認する。スレッド数はSharePointへの
   リクエスト数にほぼそのまま比例するため、ヘルススコアの悪化を招くことがある。
   オンプレミスファームに対しては段階的に増やす
4. ``site.crawl_subsites=true`` の場合、サブサイト数にほぼ比例してクロール全体の
   所要時間が伸びる。``site.max_depth`` で範囲を絞れないか検討する

インデックスが0件の場合
-----------------------

**症状**: クロールは正常終了するが検索結果が0件

**確認事項**:

1. クローラーのログ（``app/WEB-INF/env/crawler/resources/log4j2.xml`` で
   ``org.codelibs.fess.ds`` を ``DEBUG`` にして確認）にエラーや警告が出ていないか確認する
2. ``url`` / ``site.name`` （または ``site.path``）/ ``site.list_name`` などの
   パラメーターにタイプミスがないか確認する。``site.path`` を設定した場合は ``site.name`` は
   不要になる点に注意する
3. 認証が実際に成功しているか確認する（401が返っていないか）。``role.skip`` や
   ``default_permissions`` の設定ミスより、そもそもリクエストが認証されていないケースが多い
4. ``include_pattern`` / ``exclude_pattern`` を設定している場合は、これらが検索結果に表示
   されるURLではなく、サーバー相対パス（ドキュメントライブラリのファイルやリスト項目添付
   ファイルの場合）または ``FileRef`` （リスト項目の場合）に対してマッチする点を確認する。
   フルURLを想定したパターンになっていないか見直す
5. ``supported_mimetypes`` や ``max_content_length`` の設定で対象ファイルが除外されて
   いないか確認する
6. ``site.exclude_list`` / ``site.exclude_folder`` の正規表現が意図せず対象を除外して
   いないか確認する

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-microsoft365` - Microsoft 365コネクタ（SharePoint Online向け）
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../../admin/plugin-guide` - プラグイン管理ガイド
