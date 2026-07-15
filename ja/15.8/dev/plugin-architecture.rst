==================================
プラグインアーキテクチャ
==================================

概要
====

|Fess| のプラグインシステムにより、コア機能を拡張できます。
プラグインは JAR ファイルとして配布され、クラスパスに追加されると
DI コンテナ(Lasta Di)によってコンポーネントが読み込まれ、対応する
ファクトリーやマネージャーへ登録されます。

プラグインの種類
================

|Fess| は、アーティファクト名のプレフィックスによってプラグインの種類を
判別します(``PluginHelper.ArtifactType``)。主な種類は以下のとおりです:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 種類
     - プレフィックス
     - 説明
   * - データストア
     - ``fess-ds-*``
     - 新しいデータソースからのコンテンツ取得(Box、Slack、Git 等)
   * - Webアプリ
     - ``fess-webapp-*``
     - Web インターフェースや検索機能の拡張
   * - スクリプトエンジン
     - ``fess-script-*``
     - 新しいスクリプト言語のサポート
   * - Ingest
     - ``fess-ingest-*``
     - インデックス登録時のドキュメント加工
   * - テーマ
     - ``fess-theme-*``
     - 検索画面デザインのカスタマイズ
   * - サムネイル
     - ``fess-thumbnail-*``
     - サムネイル生成方式の追加
   * - LLM
     - ``fess-llm-*``
     - RAG/チャットで使用する LLM プロバイダーの追加
   * - クローラー
     - ``fess-crawler-*``
     - クローラークライアントの拡張

プラグイン構造
==============

基本構造
--------

データストアプラグインの実装テンプレートである
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ を例にすると、
プラグインは「実装クラス」と「DI 登録ファイル」で構成されます:

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # データストア実装
        └── resources/
            └── fess_ds++.xml             # DIコンポーネント登録

pom.xmlの例
-----------

プラグインは ``fess-parent`` を親 POM とする jar としてビルドします。
``fess`` や ``opensearch`` など、実行時に |Fess| 本体から提供されるライブラリは
``provided`` スコープで宣言します。バージョン番号やビルド設定(フォーマッター・
ライセンスヘッダーなど)は親 POM から継承されます。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

.. note::

   開発中のブランチでは、バージョンは ``15.8.0-SNAPSHOT`` のように ``-SNAPSHOT`` 付きに
   なります。プラグイン固有の依存ライブラリは通常の Maven 依存関係として宣言します。
   これらは |Fess| 本体には含まれないため、プラグインと一緒に配布する必要があります。

プラグインの登録
================

DIコンテナへの登録
------------------

プラグインは、``fess_ds++.xml`` のように末尾が ``++`` の DI 設定ファイルで
コンポーネントを登録します。Lasta Di は、クラスパス上に見つかった ``++`` 付きの
ファイルを、|Fess| 本体の対応する設定ファイル(この例では ``fess_ds.xml``)へ
自動的にマージします。この仕組みにより、プラグインは |Fess| 本体のファイルを
編集することなく、自身のコンポーネントを追加できます。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

プラグインの種類ごとにマージ先のファイルが異なります。例えばスクリプトエンジンは
``fess_se++.xml``、Ingest は ``fess_ingest++.xml``、LLM プロバイダーは
``fess_llm++.xml``、Web アプリは ``app++.xml`` を使用します。

コンポーネントの初期化
----------------------

``<postConstruct name="register">`` は、コンポーネント生成後に呼び出す
メソッドを指定する Lasta Di のライフサイクル設定です。データストアの場合、
``AbstractDataStore`` が持つ ``register()`` メソッドが呼び出され、
自身が ``DataStoreFactory`` に登録されます:

.. code-block:: java

    // AbstractDataStore の実装(通常はオーバーライド不要)
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   これは Java の ``@PostConstruct`` アノテーションではなく、DI 設定ファイルの
   ``<postConstruct>`` 要素による初期化です。登録される名前は ``getName()`` の
   戻り値であり、管理画面でプラグインを選択する際の名前になります。

プラグインのライフサイクル
==========================

初期化
------

1. プラグイン JAR がクラスパスに追加される
2. DI コンテナが ``fess_*++.xml`` をマージし、コンポーネントを生成する
3. ``<postConstruct>`` で指定したメソッド(例: ``register``)が呼び出される
4. プラグインが対応するファクトリー/マネージャーに登録される

終了
----

1. DI コンテナの終了時に、``<preDestroy>`` で指定したメソッドが呼び出される
   (定義されている場合)
2. リソースのクリーンアップ

.. note::

   データストアの場合、実行中のクロールは ``AbstractDataStore.stop()`` によって
   停止フラグが立てられ、レコード処理ループが安全に終了します。

依存関係
========

Fess本体との依存
----------------

|Fess| 本体のクラスは実行時にサーバーのクラスパス上に存在するため、
``provided`` スコープで依存します(プラグイン JAR には含めません)。

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

外部ライブラリ
--------------

プラグインは独自の依存ライブラリを含めることができます:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

これらは |Fess| 本体に含まれないため、プラグインと一緒に配布する必要があります。

設定の取得
==========

パラメーターとFessConfigの取得
------------------------------

データストアの ``storeData()`` では、管理画面で設定したパラメーターを
``DataStoreParams`` から取得します。値の取得には ``getAsString()`` を使用します
(``DataStoreParams`` は ``Map`` を実装していないため ``get()`` は文字列を返しません)。
また、|Fess| の設定値は ``ComponentUtil.getFessConfig()`` から取得できます:

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // ハンドラー名として使用される。クラスの単純名を返すのが慣例
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // パラメーターの取得
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // FessConfig の取得
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

``storeData()`` の詳しい実装方法(データ取得・スクリプト評価・インデックス登録の
流れ)は :doc:`datastore-plugin` を参照してください。

ビルドとインストール
====================

ビルド
------

::

    mvn clean package

``target/`` ディレクトリに JAR ファイル(例: ``fess-ds-example-15.8.0.jar``)が
生成されます。

インストール
------------

1. **管理画面から**:

   - 「システム」→「プラグイン」→「インストール」を開く
   - プラグインリポジトリの一覧から選択するか、ビルドした JAR ファイルを
     アップロードしてインストール

2. **手動**:

   - JAR ファイルを ``app/WEB-INF/plugin/`` ディレクトリにコピー
   - |Fess| を再起動

インストール手順の詳細は :doc:`../admin/plugin-guide` を参照してください。

デバッグ
========

ログ出力
--------

|Fess| は Log4j2 を使用します。ロガーは ``LogManager.getLogger()`` で取得します:

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   パスワードやトークンなどの機微な情報はログに出力しないでください。

開発モード
----------

開発時は |Fess| を IDE から起動してデバッグできます:

1. ``org.codelibs.fess.FessBoot`` クラスをデバッグ実行する
2. プラグインのソースをプロジェクトに含める
3. ブレークポイントを設定する

公開プラグイン一覧
==================

|Fess| プロジェクトでは、多数のプラグインが公開されています。以下は代表例です
(すべてを網羅したものではありません):

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プラグイン
     - 説明
   * - ``fess-ds-box``
     - Box コネクター
   * - ``fess-ds-dropbox``
     - Dropbox コネクター
   * - ``fess-ds-slack``
     - Slack コネクター
   * - ``fess-ds-atlassian``
     - JIRA / Confluence コネクター
   * - ``fess-ds-git``
     - Git リポジトリコネクター
   * - ``fess-llm-openai``
     - OpenAI LLM プロバイダー
   * - ``fess-theme-*``
     - カスタムテーマ

このほかにも、``fess-ds-csv`` / ``fess-ds-db`` / ``fess-ds-json`` /
``fess-ds-microsoft365`` / ``fess-ds-sharepoint`` などのデータストアコネクターや、
``fess-llm-ollama`` / ``fess-llm-gemini`` などの LLM プロバイダーが公開されています。
これらのプラグインは、開発の参考として
`GitHub <https://github.com/codelibs>`__ で公開されています。

参考情報
========

- :doc:`datastore-plugin` - データストアプラグイン開発
- :doc:`script-engine-plugin` - スクリプトエンジンプラグイン
- :doc:`webapp-plugin` - Webアプリプラグイン
- :doc:`ingest-plugin` - Ingestプラグイン
- :doc:`theme-development` - テーマのカスタマイズ
- :doc:`../admin/plugin-guide` - プラグインのインストール
