===================================
Fess と他の検索ソリューションの比較
===================================

はじめに
========

社内文書やサイト内の検索を用意するとき、候補には Fess のような検索システムのほか、OpenSearch や Apache Solr などの検索エンジンを使った自社開発、外部の Web 検索サービス、商用のエンタープライズ検索製品があります。
本記事では、まず Fess 15.9 が提供するものを確認しやすい形で整理し、そのうえで他の選択肢との役割の違いを比べます。

.. note::

   Fess についての記述は 15.9 の時点のものです。
   他の製品やサービスについては、変わりにくい構成上の違いだけを扱います。機能、料金、提供状況は変わることがあるため、各製品の最新の資料で確認してください。

Fess が提供するもの
===================

Fess は、OpenSearch を検索エンジンとして使う検索システムです。
クローラー、管理画面、検索画面、API を 1 つのアプリケーションとして提供し、インデックスやクロール設定は OpenSearch に保存します。
Elasticsearch や Solr を検索エンジンとして使うことはできません。
ライセンスは Apache License 2.0 です。

機能の多くはプラグインとして提供され、必要なものだけを導入します。
次の表の「必要なもの」が空欄の項目は、Fess 本体だけで使えます。

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - 項目
     - 15.9 で提供されるもの
     - 必要なもの
   * - Web クロール
     - HTTP/HTTPS のサイトをクロールします。ウェブ認証、リクエストヘッダー、パスマッピングを設定できます
     -
   * - ファイルクロール
     - ``file``\ ・\ ``smb``\ ・\ ``smb1``\ ・\ ``ftp`` のパスをクロールします
     -
   * - クラウドストレージのクロール
     - ``s3://``\ （Amazon S3 と S3 互換ストレージ）、\ ``gcs://``\ （Google Cloud Storage）
     - ``fess-storage-s3``\ ・\ ``fess-storage-gcs``
   * - データベースや SaaS
     - データストアコネクタで取り込みます（一覧は次の節）
     - ``fess-ds-*`` プラグイン
   * - 文書形式
     - Office 文書、PDF、HTML、テキスト、圧縮ファイルなど。画像やスキャンした PDF の OCR は既定で無効です
     - OCR には ``tesseract`` コマンド
   * - アクセス制御
     - ロール・グループ・ユーザー単位で検索結果を出し分けます。SMB とファイルのクロールでは、ファイルのアクセス権をロールとして取り込みます。LDAP（Active Directory を含む）との連携は本体の機能です
     -
   * - シングルサインオン
     - OpenID Connect、SAML、SPNEGO（Kerberos）、Microsoft Entra ID
     - ``fess-sso-oidc``\ ・\ ``fess-sso-saml``\ ・\ ``fess-sso-spnego``\ ・\ ``fess-sso-entraid``
   * - 検索画面
     - 静的なテーマ（HTML・CSS・JavaScript を ZIP にまとめたもの）で表示します。同梱のテーマは ``bootstrap`` です
     -
   * - API
     - 検索、ラベル、サジェスト、人気ワード、ヘルスチェック、AI 検索モードなどの ``/api/v2``\ 、管理用の ``/api/admin``
     -
   * - 旧形式の API
     - ``/api/v1``\ 、\ ``/json``\ ・\ ``/suggest``
     - ``fess-webapp-v1-api``\ 、\ ``fess-webapp-classic-api``
   * - セマンティック検索
     - 本文をチャンクに分けてベクトル化し、キーワード検索の結果と Rank Fusion で統合します。既定で無効です
     - 埋め込みモデル（OpenSearch の ML Commons、または ``fess-llm-*`` プラグイン）
   * - AI 検索モード（RAG）
     - 検索結果を根拠に LLM が回答します。既定で無効です
     - ``fess-llm-ollama``\ ・\ ``fess-llm-openai``\ ・\ ``fess-llm-gemini``\ ・\ ``fess-llm-bedrock`` のいずれか
   * - MCP サーバー
     - AI エージェントから ``/mcp`` で Fess を検索できるようにします
     - ``fess-webapp-mcp``
   * - 画像検索
     - 文章で画像（GIF・JPEG・PNG）を探すマルチモーダル検索です
     - ``fess-webapp-multimodal`` と CLIP のサーバー

Docker イメージには SSO の 4 プラグイン、\ ``fess-storage-s3``\ ・\ ``fess-storage-gcs``\ 、\ ``fess-script-groovy`` が同梱されています。
それ以外のプラグインは［システム］>［プラグイン］から導入し、Fess を再起動します。
プラグインのバージョンは Fess と同じマイナーバージョン（15.9 なら 15.9.x）を選びます。

データストアコネクタ
--------------------

15.9 向けには、次のデータストアプラグインが公開されています。
設定方法は各コネクタのリファレンスにあります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 分類
     - プラグイン（対象）
   * - クラウドストレージ
     - ``fess-ds-box``\ （Box）、\ ``fess-ds-dropbox``\ （Dropbox）、\ ``fess-ds-gsuite``\ （Google ドライブ）、\ ``fess-ds-microsoft365``\ （OneDrive、SharePoint Online、Teams など）
   * - コラボレーション
     - ``fess-ds-atlassian``\ （Confluence、Jira）、\ ``fess-ds-slack``\ （Slack）、\ ``fess-ds-notion``\ （Notion）、\ ``fess-ds-backlog``\ （Backlog）、\ ``fess-ds-sharepoint``\ （オンプレミスの SharePoint Server）
   * - 開発・業務システム
     - ``fess-ds-git``\ （Git リポジトリ）、\ ``fess-ds-salesforce``\ （Salesforce）
   * - データ
     - ``fess-ds-db``\ （JDBC で接続できるデータベース）、\ ``fess-ds-csv``\ （CSV）、\ ``fess-ds-json``\ （JSON）、\ ``fess-ds-wikipedia``\ （Wikipedia のダンプ）

ここにないデータソースは、データストアプラグインを自作するか（:doc:`guide-17`）、管理用 API で文書を登録して（:doc:`guide-11`）検索対象にできます。

検索エンジン（OpenSearch・Apache Solr）を使った自社開発との違い
===============================================================

OpenSearch と Apache Solr は検索エンジンです。
インデックスの作成と検索を担いますが、データを集めるクローラーや、利用者が使う検索画面、文書ごとのアクセス制御は含みません。
これらは自分で開発するか、別のソフトウェアを組み合わせます。
たとえば Web クロールには、Apache Nutch のような別のプロジェクトがあります。

Fess は OpenSearch の上に、これらの部分を用意したアプリケーションです。
違いは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - 観点
     - Fess
     - 検索エンジンを使った自社開発
   * - データの収集
     - Web・ファイル・データストアのクロールを管理画面で設定します
     - クローラーや取り込み処理を作るか、別のソフトウェアを組み合わせます
   * - 検索画面
     - テーマで表示します。見た目を変えるにはテーマを作るか、API を使って独自の画面を作ります
     - 自由に作れますが、すべて開発します
   * - アクセス制御
     - ロールとファイルのアクセス権を文書に記録し、検索時にログインユーザーで絞り込みます
     - 文書の権限の取り込みと、検索時の絞り込みを設計して実装します
   * - インデックスの設計
     - Fess が定義したインデックスを使います。日本語を含む多言語のアナライザーが設定済みです
     - 用途に合わせて自由に設計できます
   * - 運用するもの
     - Fess と OpenSearch
     - 検索エンジンと、自社で開発した部分すべて

検索の仕組みを一から設計したい場合や、独自のデータ構造を検索したい場合は、検索エンジンを直接使うほうが向いています。
一方、文書を集めて社内で検索できるようにすることが目的なら、Fess で始めて足りない部分を API やプラグインで補うほうが、開発する範囲を小さくできます。

Fess を既存の OpenSearch クラスターにつなぐこともできます。
CodeLibs のプラグインを導入できない Amazon OpenSearch Service などでは、\ ``search_engine.type`` に ``aws`` または ``vanilla`` を指定します。
この場合、辞書の管理や重複文書の検出など一部の機能は使えません（`検索エンジンの種別 <https://fess.codelibs.org/ja/stable/config/search-engine-type.html>`__ を参照）。

外部の Web 検索サービスを使ったサイト内検索との違い
===================================================

検索サービス事業者のインデックスを使ってサイト内検索を提供する方法もあります。
この方法では、検索できるのは事業者のクローラーが取得した公開ページに限られます。
ログインが必要なページや社内のファイルサーバーは対象にできず、いつクロールされるか、どの順に表示されるかも事業者に依存します。

Fess では、クロールの対象と時期を自分で決め、インデックスを自社の環境に置きます。
検索結果の調整には、キーマッチ（特定の語で特定の文書を上位に出す）、ドキュメントブースト、関連クエリーなどを使えます。
既存のサイトへの組み込み方は 2 つあります。

- 検索フォームを置き、Fess の検索画面（テーマ）に移動させる
- Fess Site Search（FSS）の JavaScript を埋め込み、ページ内に検索結果を表示する

FSS は ``/api/v1`` を呼び出すため、15.9 では ``fess-webapp-v1-api`` プラグインが必要です。
手順は :doc:`guide-03` を参照してください。

商用のエンタープライズ検索製品との違い
======================================

商用製品と比べる場合、製品ごとに対応範囲が大きく異なるため、一般論での優劣は決められません。
次の観点で、候補の製品と Fess を同じ条件で確認することをおすすめします。

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 観点
     - Fess の場合
   * - 対象のデータソース
     - 前の節の表とデータストアコネクタの一覧で確認します。足りない場合はプラグインを自作できます
   * - アクセス制御
     - ロール・グループ・ユーザー単位で、LDAP と SSO の 4 方式に対応します
   * - 生成 AI
     - AI 検索モード（RAG）、セマンティック検索、MCP サーバー。LLM は Ollama（自社で運用）、OpenAI、Gemini、Amazon Bedrock から選びます
   * - データの置き場所
     - インデックスは自社で運用する OpenSearch に置きます。LLM や埋め込みに外部のサービスを使う場合は、質問や文書の本文がそのサービスに送られます
   * - 運用の形態
     - 自社で運用するソフトウェアです。Docker、Linux（ZIP・RPM・DEB）、Windows に導入できます。Kubernetes でも動かせますが、公式の Helm チャートはありません
   * - 費用とサポート
     - ライセンス費用はかかりません。費用はサーバーと運用の工数です。商用サポートは `各種サポートサービス <https://fess.codelibs.org/ja/support-services.html>`__ で案内しています
   * - 変更の自由度
     - ソースコードが公開されており、テーマ、プラグイン、API で拡張できます

商用製品が向いているのは、必要なコネクタや管理機能が製品にそろっていて、運用をベンダーに任せたい場合です。
Fess が向いているのは、自社の環境にデータを置いたまま、必要な機能を組み合わせて検索基盤を作りたい場合です。

選び方の目安
============

次の質問に順に答えると、Fess が候補になるかを判断できます。

1. 検索したいデータは、Fess のクロール対象かデータストアコネクタに含まれていますか。

   - 含まれていない場合は、プラグインの自作（:doc:`guide-17`）か API での登録（:doc:`guide-11`）に必要な開発量を見積もります。

2. 利用者ごとに見せる文書を変える必要がありますか。

   - ファイルサーバーのアクセス権を使うなら :doc:`file-server-search`、ロールの設計は :doc:`guide-05`、SSO は :doc:`guide-15` を確認します。

3. 検索画面は Fess のテーマで足りますか。

   - 自社のアプリケーションに検索を組み込む場合は、\ ``/api/v2`` を使います（:doc:`guide-11`）。

4. Fess と OpenSearch を自社で運用できますか。

   - 運用できない場合や、運用をベンダーに任せたい場合は、Fess の商用サポートか商用製品を検討します。

5. 生成 AI を使った回答や意味検索が必要ですか。

   - 使う LLM を決め、:doc:`guide-19` と :doc:`guide-18` で必要な構成を確認します。

1 と 4 の答えが「はい」なら、まず Fess を試し、実際の文書で検索結果を確かめるのが確実です。

試して確かめる
==============

比較表だけでは、自分の文書でどう検索できるかはわかりません。
:doc:`guide-02` の手順で Fess を Docker で起動し、検索したい対象の一部をクロールして、次の点を確認します。

- 対象の文書が取り込まれているか（［システム情報］>［ジョブログ］と［障害URL］で、エラーになった URL がないか確認します）
- よく使う語で検索して、期待する文書が上位に出るか
- ログインユーザーを切り替えて、見えるべきでない文書が表示されないか（アクセス制御が必要な場合）

次に読む記事
============

- Fess の構成と、記事全体の読み進め方を知りたい: :doc:`guide-01`
- まず手元で動かしたい: :doc:`guide-02`
- 既存のサイトに検索を組み込みたい: :doc:`guide-03`
- データベースや SaaS のデータを検索したい: :doc:`datastore-basics`
- ファイルサーバーのアクセス権を検索結果に反映したい: :doc:`file-server-search`
- 生成 AI に社内文書から回答させたい: :doc:`guide-19`
- 規模の拡大に備えたい: :doc:`guide-14`
- 活用例を知りたい: :doc:`use-cases`

参考資料
========

- `データストアコネクタの概要 <https://fess.codelibs.org/ja/stable/config/datastore/ds-overview.html>`__
- `ファイルクロールの設定 <https://fess.codelibs.org/ja/stable/admin/fileconfig-guide.html>`__
- `検索対象ファイル <https://fess.codelibs.org/ja/supported-files.html>`__
- `OCR の設定 <https://fess.codelibs.org/ja/stable/config/crawler-ocr.html>`__
- `テーマ <https://fess.codelibs.org/ja/stable/admin/theme-guide.html>`__
- `API の概要 <https://fess.codelibs.org/ja/stable/api/api-overview.html>`__
- `セマンティック検索 <https://fess.codelibs.org/ja/stable/config/search-semantic.html>`__
- `AI 検索（RAG）と LLM 統合の概要 <https://fess.codelibs.org/ja/stable/config/llm-overview.html>`__
- `検索エンジンの種別 <https://fess.codelibs.org/ja/stable/config/search-engine-type.html>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
