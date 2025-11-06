============================
アーキテクチャとコード構造
============================

このページでは、|Fess| のアーキテクチャ、コード構造、
主要なコンポーネントについて説明します。
|Fess| の内部構造を理解することで、効率的に開発を進めることができます。

.. contents:: 目次
   :local:
   :depth: 2

全体アーキテクチャ
================

|Fess| は、以下の主要なコンポーネントで構成されています：

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │          ユーザーインターフェース                │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │  検索画面     │      │   管理画面    │        │
    │  │  (JSP/HTML)   │      │   (JSP/HTML)  │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Web アプリケーション層               │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              ビジネスロジック層                   │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              データアクセス層                     │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               データストア                        │
    │              OpenSearch 3.3.0                   │
    └─────────────────────────────────────────────────┘

レイヤーの説明
------------

ユーザーインターフェース層
~~~~~~~~~~~~~~~~~~~~~~~~

ユーザーが直接操作する画面です。
JSP と HTML、JavaScript で実装されています。

- 検索画面: エンドユーザー向けの検索インターフェース
- 管理画面: システム管理者向けの設定・管理インターフェース

Web アプリケーション層
~~~~~~~~~~~~~~~~~~~~

LastaFlute フレームワークを使用した Web アプリケーション層です。

- **Action**: HTTP リクエストを処理し、ビジネスロジックを呼び出す
- **Form**: リクエストパラメータの受け取りとバリデーション
- **Service**: ビジネスロジックの実装

ビジネスロジック層
~~~~~~~~~~~~~~~~

|Fess| の主要な機能を実装する層です。

- **Crawler**: Web サイトやファイルシステムからデータを収集
- **Job**: スケジュール実行されるタスク
- **Helper**: アプリケーション全体で使用されるヘルパークラス

データアクセス層
~~~~~~~~~~~~~~

DBFlute を使用した OpenSearch へのアクセス層です。

- **Behavior**: データ操作のインターフェース
- **Entity**: データの実体
- **Query**: 検索クエリの構築

データストア層
~~~~~~~~~~~~

検索エンジンとして OpenSearch 3.3.0 を使用します。

プロジェクト構造
==============

ディレクトリ構造
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # Web アプリケーション
    │   │   │   │   ├── web/          # 検索画面
    │   │   │   │   │   ├── admin/    # 管理画面
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # サービス層
    │   │   │   ├── crawler/          # クローラー
    │   │   │   │   ├── client/       # クローラークライアント
    │   │   │   │   ├── extractor/    # コンテンツ抽出
    │   │   │   │   ├── filter/       # フィルタ
    │   │   │   │   └── transformer/  # データ変換
    │   │   │   ├── es/               # OpenSearch 関連
    │   │   │   │   ├── client/       # OpenSearch クライアント
    │   │   │   │   ├── query/        # クエリビルダー
    │   │   │   │   └── config/       # 設定管理
    │   │   │   ├── helper/           # ヘルパークラス
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # ジョブ
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # ユーティリティ
    │   │   │   ├── entity/           # エンティティ（自動生成）
    │   │   │   ├── mylasta/          # LastaFlute 設定
    │   │   │   │   ├── action/       # Action 基底クラス
    │   │   │   │   ├── direction/    # アプリケーション設定
    │   │   │   │   └── mail/         # メール設定
    │   │   │   ├── Constants.java    # 定数定義
    │   │   │   └── FessBoot.java     # 起動クラス
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # 設定ファイル
    │   │   │   ├── fess_config.xml         # 追加設定
    │   │   │   ├── fess_message_ja.properties  # メッセージ（日本語）
    │   │   │   ├── fess_message_en.properties  # メッセージ（英語）
    │   │   │   ├── log4j2.xml              # ログ設定
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # JSP ファイル
    │   │       │   │   ├── admin/     # 管理画面 JSP
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # CSS ファイル
    │   │       ├── js/                # JavaScript ファイル
    │   │       └── images/            # 画像ファイル
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # テストクラス
    │           └── it/                # 統合テスト
    ├── pom.xml                        # Maven 設定
    ├── dbflute_fess/                  # DBFlute 設定
    │   ├── dfprop/                    # DBFlute プロパティ
    │   └── freegen/                   # FreeGen 設定
    └── README.md

主要パッケージの詳細
==================

app パッケージ
------------

Web アプリケーション層のコードです。

app.web パッケージ
~~~~~~~~~~~~~~~~

検索画面とエンドユーザー向け機能を実装します。

**主要なクラス:**

- ``SearchAction.java``: 検索処理
- ``LoginAction.java``: ログイン処理

**例:**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // 検索処理の実装
        return asHtml(path_IndexJsp);
    }

app.web.admin パッケージ
~~~~~~~~~~~~~~~~~~~~~~~

管理画面の機能を実装します。

**主要なクラス:**

- ``BwCrawlingConfigAction.java``: Web クロール設定
- ``BwSchedulerAction.java``: スケジューラー管理
- ``BwUserAction.java``: ユーザー管理

**命名規則:**

- ``Bw`` プレフィックス: Admin 用 Action
- ``Action`` サフィックス: Action クラス
- ``Form`` サフィックス: Form クラス

app.service パッケージ
~~~~~~~~~~~~~~~~~~~~

ビジネスロジックを実装するサービス層です。

**主要なクラス:**

- ``SearchService.java``: 検索サービス
- ``UserService.java``: ユーザー管理サービス
- ``ScheduledJobService.java``: ジョブ管理サービス

**例:**

.. code-block:: java

    public class SearchService {
        public SearchResponse search(SearchRequestParams params) {
            // 検索ロジックの実装
        }
    }

crawler パッケージ
----------------

データ収集機能を実装します。

crawler.client パッケージ
~~~~~~~~~~~~~~~~~~~~~~~

各種データソースへのアクセスを実装します。

**主要なクラス:**

- ``FessClient.java``: クローラークライアントの基底クラス
- ``WebClient.java``: Web サイトのクロール
- ``FileSystemClient.java``: ファイルシステムのクロール
- ``DataStoreClient.java``: データベースなどのクロール

crawler.extractor パッケージ
~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメントからテキストを抽出します。

**主要なクラス:**

- ``ExtractorFactory.java``: エクストラクターのファクトリ
- ``TikaExtractor.java``: Apache Tika を使用した抽出

crawler.transformer パッケージ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

クロールしたデータを検索用の形式に変換します。

**主要なクラス:**

- ``Transformer.java``: 変換処理のインターフェース
- ``BasicTransformer.java``: 基本的な変換処理

es パッケージ
-----------

OpenSearch との連携を実装します。

es.client パッケージ
~~~~~~~~~~~~~~~~~~

OpenSearch クライアントの実装です。

**主要なクラス:**

- ``FessEsClient.java``: OpenSearch クライアント
- ``SearchEngineClient.java``: 検索エンジンクライアントのインターフェース

es.query パッケージ
~~~~~~~~~~~~~~~~~

検索クエリの構築を実装します。

**主要なクラス:**

- ``QueryHelper.java``: クエリ構築のヘルパー
- ``FunctionScoreQueryBuilder.java``: スコアリング調整

helper パッケージ
---------------

アプリケーション全体で使用されるヘルパークラスです。

**主要なクラス:**

- ``SystemHelper.java``: システム全体のヘルパー
- ``CrawlingConfigHelper.java``: クロール設定のヘルパー
- ``SearchLogHelper.java``: 検索ログのヘルパー
- ``UserInfoHelper.java``: ユーザー情報のヘルパー
- ``ViewHelper.java``: ビュー関連のヘルパー

**例:**

.. code-block:: java

    public class SystemHelper {
        public void initializeSystem() {
            // システム初期化処理
        }
    }

job パッケージ
------------

スケジュール実行されるジョブを実装します。

**主要なクラス:**

- ``CrawlJob.java``: クロールジョブ
- ``SuggestJob.java``: サジェストジョブ
- ``ScriptExecutorJob.java``: スクリプト実行ジョブ

**例:**

.. code-block:: java

    public class CrawlJob extends LaJob {
        @Override
        public void run() {
            // クロール処理の実装
        }
    }

entity パッケージ
---------------

OpenSearch のドキュメントに対応するエンティティクラスです。
このパッケージは DBFlute によって自動生成されます。

**主要なクラス:**

- ``SearchLog.java``: 検索ログ
- ``ClickLog.java``: クリックログ
- ``FavoriteLog.java``: お気に入りログ
- ``User.java``: ユーザー情報
- ``Role.java``: ロール情報

.. note::

   entity パッケージのコードは自動生成されるため、
   直接編集しないでください。
   スキーマを変更して再生成することで更新します。

mylasta パッケージ
----------------

LastaFlute の設定とカスタマイズを行います。

mylasta.action パッケージ
~~~~~~~~~~~~~~~~~~~~~~~

Action の基底クラスを定義します。

- ``FessUserBean.java``: ユーザー情報
- ``FessHtmlPath.java``: HTML パス定義

mylasta.direction パッケージ
~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーション全体の設定を行います。

- ``FessConfig.java``: 設定の読み込み
- ``FessFwAssistantDirector.java``: フレームワーク設定

デザインパターンと実装パターン
============================

|Fess| では、以下のようなデザインパターンが使用されています。

MVC パターン
----------

LastaFlute による MVC パターンで実装されています。

- **Model**: Service、Entity
- **View**: JSP
- **Controller**: Action

例：

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessBaseAction {
        @Resource
        private SearchService searchService;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            SearchResponse response = searchService.search(form);
            return asHtml(path_IndexJsp).renderWith(data -> {
                data.register("response", response);  // View (JSP) へデータ渡し
            });
        }
    }

DI パターン
---------

LastaFlute の DI コンテナを使用します。

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Factory パターン
--------------

各種コンポーネントの生成に使用されます。

.. code-block:: java

    public class ExtractorFactory {
        public Extractor createExtractor(String mimeType) {
            // MIME タイプに応じた Extractor を生成
        }
    }

Strategy パターン
---------------

クローラーやトランスフォーマーで使用されます。

.. code-block:: java

    public interface Transformer {
        Map<String, Object> transform(Map<String, Object> data);
    }

    public class HtmlTransformer implements Transformer {
        // HTML 用の変換処理
    }

設定管理
======

|Fess| の設定は複数のファイルで管理されています。

fess_config.properties
--------------------

アプリケーションの主要な設定を定義します。

.. code-block:: properties

    # ポート番号
    server.port=8080

    # OpenSearch 接続設定
    opensearch.http.url=http://localhost:9201

    # クロール設定
    crawler.document.max.size=10000000

fess_config.xml
--------------

XML 形式の追加設定です。

.. code-block:: xml

    <component name="searchService" class="...SearchService">
        <property name="maxSearchResults">1000</property>
    </component>

fess_message_*.properties
------------------------

多言語対応のメッセージファイルです。

- ``fess_message_ja.properties``: 日本語
- ``fess_message_en.properties``: 英語

データフロー
==========

検索フロー
--------

.. code-block:: text

    1. ユーザーが検索画面で検索
       ↓
    2. SearchAction が検索リクエストを受信
       ↓
    3. SearchService がビジネスロジックを実行
       ↓
    4. SearchEngineClient が OpenSearch に検索クエリを送信
       ↓
    5. OpenSearch が検索結果を返却
       ↓
    6. SearchService が結果を整形
       ↓
    7. SearchAction が JSP に結果を渡して表示

クロールフロー
------------

.. code-block:: text

    1. CrawlJob がスケジュール実行される
       ↓
    2. CrawlingConfigHelper がクロール設定を取得
       ↓
    3. FessClient が対象サイトにアクセス
       ↓
    4. Extractor がコンテンツからテキストを抽出
       ↓
    5. Transformer がデータを検索用の形式に変換
       ↓
    6. SearchEngineClient が OpenSearch にドキュメントを登録

拡張ポイント
==========

|Fess| は、以下のポイントで拡張できます。

カスタムクローラーの追加
--------------------

``FessClient`` を継承して、独自のデータソースに対応できます。

カスタムトランスフォーマーの追加
----------------------------

``Transformer`` を実装して、独自のデータ変換処理を追加できます。

カスタムエクストラクターの追加
--------------------------

``Extractor`` を実装して、独自のコンテンツ抽出処理を追加できます。

カスタムプラグインの追加
--------------------

``Plugin`` インターフェースを実装して、独自のプラグインを作成できます。

参考資料
======

フレームワーク
------------

- `LastaFlute リファレンス <https://github.com/lastaflute/lastaflute>`__
- `DBFlute ドキュメント <https://dbflute.seasar.org/>`__

技術ドキュメント
--------------

- `OpenSearch API リファレンス <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

次のステップ
==========

アーキテクチャを理解したら、以下のドキュメントを参照してください：

- :doc:`workflow` - 実際の開発フロー
- :doc:`building` - ビルドとテスト
- :doc:`contributing` - プルリクエストの作成
