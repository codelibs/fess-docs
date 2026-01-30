==================================
プラグインアーキテクチャ
==================================

概要
====

|Fess| のプラグインシステムにより、コア機能を拡張できます。
プラグインはJARファイルとして配布され、動的にロードされます。

プラグインの種類
================

|Fess| は以下の種類のプラグインをサポートしています:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 種類
     - 説明
   * - データストア
     - 新しいデータソースからのコンテンツ取得（Box、Slack等）
   * - スクリプトエンジン
     - 新しいスクリプト言語のサポート
   * - Webアプリ
     - Webインターフェースの拡張
   * - Ingest
     - インデックス時のデータ加工

プラグイン構造
==============

基本構造
--------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # データストア実装
        └── ExampleDataStoreHandler.java # ハンドラ（オプション）

pom.xmlの例
-----------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.5.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.5.0</fess.version>
            <java.version>21</java.version>
        </properties>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <version>${fess.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

プラグインの登録
================

DIコンテナへの登録
------------------

プラグインは ``fess_ds.xml`` などの設定ファイルで登録されます:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

自動登録
--------

多くのプラグインは、``@PostConstruct`` アノテーションで自動登録します:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

プラグインのライフサイクル
==========================

初期化
------

1. JARファイルがロードされる
2. DIコンテナがコンポーネントを初期化
3. ``@PostConstruct`` メソッドが呼び出される
4. プラグインがマネージャに登録される

終了
----

1. ``@PreDestroy`` メソッドが呼び出される（定義されている場合）
2. リソースのクリーンアップ

依存関係
========

Fess本体との依存
----------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
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

依存ライブラリはプラグインJARと一緒に配布するか、
Maven Shade Pluginでfat JARを作成します。

設定の取得
==========

FessConfigから取得
------------------

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(DataConfig dataConfig, IndexUpdateCallback callback,
                Map<String, String> paramMap, Map<String, String> scriptMap,
                Map<String, Object> defaultDataMap) {

            // パラメーターの取得
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // FessConfigの取得
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

ビルドとインストール
====================

ビルド
------

::

    mvn clean package

インストール
------------

1. **管理画面から**:

   - 「システム」→「プラグイン」→「インストール」
   - プラグイン名を入力してインストール

2. **コマンドライン**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **手動**:

   - JARファイルを ``plugins/`` ディレクトリにコピー
   - |Fess| を再起動

デバッグ
========

ログ出力
--------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

開発モード
----------

開発時は |Fess| をIDEから起動してデバッグできます:

1. ``FessBoot`` クラスをデバッグ実行
2. プラグインのソースをプロジェクトに含める
3. ブレークポイントを設定

公開プラグイン一覧
==================

|Fess| プロジェクトで公開されている主なプラグイン:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プラグイン
     - 説明
   * - fess-ds-box
     - Box.comコネクタ
   * - fess-ds-dropbox
     - Dropboxコネクタ
   * - fess-ds-slack
     - Slackコネクタ
   * - fess-ds-atlassian
     - Confluence/Jiraコネクタ
   * - fess-ds-git
     - Gitリポジトリコネクタ
   * - fess-theme-*
     - カスタムテーマ

これらのプラグインは、開発の参考として
`GitHub <https://github.com/codelibs>`__ で公開されています。

参考情報
========

- :doc:`datastore-plugin` - データストアプラグイン開発
- :doc:`script-engine-plugin` - スクリプトエンジンプラグイン
- :doc:`webapp-plugin` - Webアプリプラグイン
- :doc:`ingest-plugin` - Ingestプラグイン
