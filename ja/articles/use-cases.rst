=============================
Fess の活用事例とユースケース
=============================

はじめに
========

このページでは、Fess がよく使われる場面を、業種別・規模別・技術的な目的別に紹介します。
それぞれの事例について、解決したい課題、使う Fess の機能とプラグイン、手順を説明している記事を示します。
設定の手順そのものは各記事にあるので、自分の状況に近い事例から読む記事を選んでください。

記事中の機能とプラグイン名は Fess 15.9 に合わせています。
15.9 では、データベースや SaaS の取り込み、SSO、S3・GCS のクロールはプラグインで提供されます。
プラグインのバージョンは Fess と同じ 15.9.x を使い、インストール後は Fess を再起動します。
導入方法は `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__ を参照してください。

.. note::

   以下は一般的な活用パターンです。実際の導入事例については `商用サポート <../support-services.html>`__ にお問い合わせください。

目的から機能を探す
==================

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - やりたいこと
     - 使う機能・プラグイン
     - 読む記事
   * - まず手元で動かして試す
     - Docker Compose（docker-fess）
     - :doc:`guide-02`
   * - 社内サイトとファイルサーバーをまとめて検索する
     - ウェブクロール、ファイルシステムクロール、ファイル認証、ラベル
     - :doc:`guide-04`、:doc:`file-server-search`
   * - 部署や役職で見える文書を変える
     - パーミッション、ロール・グループ、LDAP（Active Directory）
     - :doc:`guide-05`
   * - 既存サイトに検索窓を置く
     - 検索フォーム、Fess Site Search（``fess-webapp-v1-api``）、テーマ
     - :doc:`guide-03`
   * - Git・Confluence・Jira・Slack を検索する
     - ``fess-ds-git``、``fess-ds-atlassian``、``fess-ds-slack``
     - :doc:`datastore-basics`、:doc:`guide-06`
   * - Google Drive・SharePoint Online・Box を検索する
     - ``fess-ds-gsuite``、``fess-ds-microsoft365``、``fess-ds-box``
     - :doc:`datastore-basics`、:doc:`guide-07`
   * - データベース・CSV・Salesforce を検索する
     - ``fess-ds-db``、``fess-ds-csv``、``fess-ds-salesforce``
     - :doc:`datastore-basics`、:doc:`guide-12`
   * - 業務システムから検索する
     - 検索 API（``/api/v2``）、アクセストークン
     - :doc:`guide-11`
   * - 社内のログインで検索させる
     - ``fess-sso-entraid``、``fess-sso-oidc``、``fess-sso-saml``、``fess-sso-spnego``
     - :doc:`guide-15`
   * - 1 つの Fess を複数の組織で使い分ける
     - 仮想ホスト、ロール、ラベル
     - :doc:`guide-13`
   * - 検索されない語や使われ方を調べて改善する
     - ［システム情報］>［検索ログ］
     - :doc:`guide-08`
   * - 意味の近い文書を探す、AI に回答させる
     - セマンティック検索、AI 検索モード、``fess-webapp-mcp``
     - :doc:`guide-18`、:doc:`guide-19`、:doc:`guide-20`
   * - 文書数や利用者の増加に備える
     - OpenSearch の分離・クラスター化、Fess の複数台構成
     - :doc:`guide-14`
   * - 本番で安定して動かす
     - ``/api/v2/health``、バックアップ、ログ
     - :doc:`guide-10`

業種別のユースケース
====================

製造業：分散した技術文書を探す
------------------------------

**課題**: 設計書、仕様書、品質記録が部門ごとのファイルサーバーに分かれていて、図面番号や型番から関連資料を探すのに時間がかかる。

**使う機能**:

- ファイルサーバーを ``smb://`` でクロールし、PDF や Office 文書の本文を検索できるようにします。Windows のアクセス権（ACL）は既定で文書の権限として取り込まれます
- 表示名が「設計」「品質」のようなラベルを作り、対象とするパスで文書を分類して、検索画面で絞り込めるようにします
- スキャンした紙の記録は、OCR を有効にすると本文を検索できます。OCR は既定で無効で、クローラーが動くホストに ``tesseract`` が必要です（`OCR の設定 <https://fess.codelibs.org/ja/stable/config/crawler-ocr.html>`__）

Fess が本文を取り出せない形式のファイルは、ファイル名やパスでしか見つかりません。
対象の形式は `検索対象ファイル <../supported-files.html>`__ で確認してください。

**読む記事**: :doc:`guide-04` で構成を作り、:doc:`file-server-search` で ACL の前提を確認し、:doc:`guide-05` で部署ごとの出し分けを設定します。

金融・保険業：規程や契約書を権限付きで探す
------------------------------------------

**課題**: 社内規程、マニュアル、契約書が大量にあり、問い合わせや監査のたびに探す手間がかかる。一方で、閲覧できる人を部署ごとに厳密に分けたい。

**使う機能**:

- 文書ごとのパーミッションで、検索結果に出す相手を限定します。新しいクロール設定のパーミッションには ``{role}guest`` が最初から入っているので、公開しない文書では消します
- ログインしていない利用者に検索させない場合は、［全般］の「ログインが必要」を有効にします
- 社内の ID 基盤でのログインには SSO を使います。SAML なら ``fess-sso-saml``、Entra ID なら ``fess-sso-entraid`` です（Docker イメージには 4 つの SSO プラグインが同梱されています）
- 業務システムから検索する場合は、アクセストークンをサーバー側に置いて検索 API を呼びます

**読む記事**: :doc:`guide-05` で権限を設計し、:doc:`guide-15` で SSO と HTTPS を設定します。業務システムとの連携は :doc:`guide-11` です。

教育機関：学内サイトと共有ドライブを横断する
--------------------------------------------

**課題**: 学部ごとの Web サイト、講義資料、学内文書が別々の場所にあり、学生も職員も目的の情報にたどり着けない。

**使う機能**:

- 学内 Web サイトをウェブクロールで取り込みます。機関リポジトリ（DSpace など）は専用のコネクタがないため、公開ページをウェブクロールします
- Google Drive の共有ドライブは ``fess-ds-gsuite``、SharePoint Online は ``fess-ds-microsoft365`` で取り込みます
- 学生向けと職員向けで見える範囲を分ける場合は、ロールとパーミッションで出し分けます。サイトを分けたい場合は仮想ホストを使います

**読む記事**: :doc:`guide-04`、:doc:`guide-07`、:doc:`guide-05`。サイトを分ける場合は :doc:`guide-13` です。

IT・ソフトウェア業：開発情報を 1 か所から探す
---------------------------------------------

**課題**: コードは Git、設計は Confluence、課題は Jira、議論は Slack や Teams に分かれていて、過去の経緯を探しにくい。

**使う機能**:

- ``fess-ds-git`` でリポジトリのファイルを、``fess-ds-atlassian`` で Confluence と Jira を、``fess-ds-slack`` で Slack のメッセージを取り込みます
- Teams のチャネルとチャットは ``fess-ds-microsoft365`` の ``TeamsDataStore`` で取り込めます（`Microsoft 365 コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-microsoft365.html>`__）
- ソースコードの検索に特化した構成として、`docker-codesearch <https://github.com/codelibs/docker-codesearch>`__ が公開されています
- 社内ツールに検索を組み込む場合は検索 API、AI エージェントから検索させる場合は ``fess-webapp-mcp`` を使います

**読む記事**: :doc:`datastore-basics` の後に :doc:`guide-06`。AI エージェントとの連携は :doc:`guide-20` です。

規模別のユースケース
====================

必要なサーバーの台数やメモリは、利用者数や文書数だけでは決まりません。
本文の長さ、添付ファイルの割合、ログインして使うかどうかで負荷が変わるため、まず小さく動かして計測し、足りないものを増やします。
判断の手順は :doc:`guide-14` の「規模の目安について」にまとめています。
本番環境のサーバーの推奨要件（CPU 4 コア以上、メモリ 8GB 以上など）は `システム要件 <https://fess.codelibs.org/ja/stable/install/prerequisites.html>`__ を参照してください。

1 台で始める
------------

部署単位の導入や試験運用では、Fess と OpenSearch を 1 台のサーバーで動かします。
Docker Compose を使う場合は、``compose.yaml`` と ``compose-opensearch3.yaml`` の 2 つのファイルで起動します。
手順は :doc:`guide-02` にあります。

1 台構成でも、次の 2 点は最初から決めておきます。

- バックアップの取り方。設定は［システム情報］>［バックアップ］で取得できますが、辞書は含まれません（:doc:`guide-10`）
- Docker の場合、［システム］>［全般］で変えた設定はコンテナ内の ``system.properties`` に保存され、コンテナを作り直すと元に戻ります（:doc:`guide-02` の「停止と再開」）

利用部署が増えたら
------------------

検索やクロールが遅くなったら、まず原因が Fess 本体か、クローラーか、OpenSearch かを確かめます。
多くの場合、次の順に拡張します。

1. 1 台のまま、Fess・クローラー・OpenSearch のヒープとクロールの並列度を調整する
2. OpenSearch を別のサーバーに分ける
3. OpenSearch を 3 台のクラスターにする
4. Fess を複数台にして、ロードバランサーで振り分ける

Fess を複数台にする場合は、［全般］の設定、``fess_config.properties`` の ``app.cipher.key``、インストールしたプラグインを全台でそろえます。
Fess 15.9 のログインセッションは各台のメモリに保存されるため、ログインして使う画面を振り分けるときは、ロードバランサーでスティッキーセッションを有効にします。
セッションを OpenSearch に保存して台をまたいで共有する機能は、15.10 以降で使えます。

**読む記事**: :doc:`guide-14`、:doc:`guide-10`。

全社で使う
----------

全社規模では、上の構成に加えて次を検討します。

- クロールを担当する Fess を 1 台に決めます（``scheduler.target.name`` とジョブの「対象」）。検索を受ける台にクロールの負荷をかけないためです
- ``/api/v2/health`` をロードバランサーと監視に使います。OpenSearch のクラスターが ``RED`` の場合や接続できない場合は 503 を返します
- 組織ごとに検索画面や対象を分ける場合は、仮想ホストを使うか、Fess のインスタンスを分けます（:doc:`guide-13`）
- 検索ログで、結果が 0 件の語やクリックされない語を定期的に確認します（:doc:`guide-08`）

Kubernetes で動かすこともできますが、公式の Helm チャートは提供されていません。
Docker Compose のファイルを変換するか、マニフェストを自分で作ります（`Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__ の FAQ）。

大規模な環境での導入は、`商用サポート <../support-services.html>`__ の利用も検討してください。

技術的なユースケース
====================

社内 Wiki・ナレッジベースの横断検索
-----------------------------------

Wiki の種類によって、取り込み方が変わります。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 対象
     - 取り込み方
     - 参照先
   * - Confluence
     - ``fess-ds-atlassian``\ （``ConfluenceDataStore``）
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Notion コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Backlog コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-backlog.html>`__
   * - MediaWiki など Web で閲覧できる Wiki
     - ウェブクロール（ログインが必要ならウェブ認証も設定）
     - :doc:`guide-04`

データストアで取り込んだ文書にも、パーミッションの ``{role}guest`` が最初から入っています。
限られた人だけが読めるスペースを取り込む場合は、:doc:`guide-06` の「先に決めること：検索結果を誰に見せるか」を先に読んでください。

ファイルサーバーの統合検索
--------------------------

Fess 15.9 のファイルクロールが扱うプロトコルは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パスの形式
     - 対象
   * - ``smb://``
     - Windows の共有フォルダーや、SMB で共有している NAS
   * - ``smb1://``
     - SMB1 にしか対応していない古いサーバー
   * - ``file:``
     - Fess のサーバーから見えるディレクトリ。NFS の共有は、OS でマウントしてからこの形式で指定します
   * - ``ftp://``
     - FTP サーバー
   * - ``s3://`` / ``gcs://``
     - Amazon S3 互換ストレージ / Google Cloud Storage。``fess-storage-s3`` / ``fess-storage-gcs`` が必要です（Docker イメージには同梱）

既定で有効なのは ``file``、``smb``、``smb1``、``ftp`` です（``crawler.file.protocols``）。
SMB の ACL を検索結果に反映するには、クロール設定のパーミッションから ``{role}guest`` を消す必要があります。
理由と確認方法は :doc:`file-server-search` に、具体的な設定は :doc:`guide-04` にあります。
Namazu や Hyper Estraier などの全文検索から置き換える場合の手順は、:doc:`legacy-search-migration` を参照してください。

Web サイト内検索
----------------

公開サイトに検索機能を付ける方法は 3 つあり、組み合わせて使えます。

- 検索フォームを置き、Fess の検索画面に移動させます。Fess 側の追加設定は不要です
- Fess Site Search（FSS）で、既存のページの中に検索結果を表示します。FSS は ``/api/v1`` を呼ぶため、15.9 ではプラグイン ``fess-webapp-v1-api`` が必要です。FSS の JavaScript は Fess からは配信されないので、FSS JS Generator で生成して自分のサイトに置きます
- Fess の検索画面をテーマで既存サイトの見た目に合わせます

手順は :doc:`guide-03` にあります。
独自の検索画面を作る場合は、``/api/v2/search`` を使います（:doc:`guide-11`）。

データベースの検索
------------------

製品マスターや FAQ のように、データベースに入っている情報は ``fess-ds-db`` で取り込みます。
JDBC に対応したデータベース（MySQL、PostgreSQL、Oracle、SQL Server など）が対象で、接続先に合う JDBC ドライバーを別に用意します。
SELECT 文で取得した列を、スクリプトで ``title`` や ``content`` などのフィールドに対応付けます。

検索結果のリンクは、元の業務画面の URL を組み立てて ``url`` に入れておくと、利用者がそのまま元のデータを開けます。
手順は :doc:`guide-12` にあります。

生成 AI と組み合わせる
----------------------

- キーワードが一致しなくても意味の近い文書を探す：セマンティック検索（:doc:`guide-18`）
- 社内文書を根拠に AI に回答させる：AI 検索モード。ベクトル検索がなくても使えます（:doc:`guide-19`）
- Claude Code などの AI エージェントから Fess を検索させる：``fess-webapp-mcp``\ （:doc:`guide-20`）

どの方法でも、検索される文書は通常の検索と同じパーミッションで絞り込まれます（AI 検索モードはログインしている利用者、MCP はアクセストークンの権限。MCP で認証を使わない場合はゲストの権限）。
AI に渡る文書もこの権限で決まるので、先に :doc:`guide-05` の権限設計を済ませておきます。

導入の進め方
============

1. :doc:`guide-02` で Fess を起動し、対象の一部をクロールして検索を試す
2. 上の表から、自分の課題に合う記事を選んで設定する
3. 権限（:doc:`guide-05`）と運用（:doc:`guide-10`）を決めてから、利用者に公開する

参考資料
========

- `クイックスタート <../quick-start.html>`__
- `ドキュメント <../documentation.html>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `データストアコネクタガイド <https://fess.codelibs.org/ja/stable/config/datastore/index.html>`__
- `ディスカッションフォーラム <https://discuss.codelibs.org/c/FessJA/>`__
- `GitHub <https://github.com/codelibs/fess>`__
